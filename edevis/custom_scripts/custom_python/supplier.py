import frappe
from frappe import _

def after_insert(doc, method):
    company = getattr(doc, 'company', None)
    if not company:
        company = frappe.defaults.get_user_default("Company") or frappe.db.get_value("Company", {}, "name")
    create_and_link_credit_account(doc, company)

def create_and_link_credit_account(doc, company):
    create_credit_account = frappe.db.get_single_value("Edevis Settings", "auto_create_supplier_credit_accounts")

    if create_credit_account:
        credit_account = create_credit_account_for_supplier(doc, company)

        if not credit_account:
            return

        account_doc = frappe.new_doc("Party Account")
        account_doc.update({
            "parent": doc.name,
            "company": company,
            "account": credit_account,
            "parenttype": "Supplier",
            "parentfield": "accounts"
        })
        account_doc.insert(ignore_permissions=True)

def create_credit_account_for_supplier(doc, company):
    parent_account = frappe.db.get_single_value("Edevis Settings", "creditors_parent_account")

    if not parent_account:
        frappe.log_error(
            _("Failed to create Credit Account for supplier {} as no Creditors Parent Account is setup in the {}"
              .format(
                  frappe.utils.get_link_to_form("Supplier", doc.name),
                  frappe.utils.get_link_to_form("Edevis Settings", "Edevis Settings")
              )),
            _("failed to create supplier credit account")
        )
        frappe.throw(
            _("Failed to create Credit Account for this supplier, please set up Creditors Parent Account in {}.")
            .format(frappe.utils.get_link_to_form("Edevis Settings", "Edevis Settings"))
        )
        return None

    account_account_name = f"{doc.name} - {doc.supplier_name}"

    try:
        existing_account = frappe.db.exists("Account", {
            "account_name": account_account_name,
            "company": company
        })
        if existing_account:
            return existing_account

        new_account_doc = frappe.get_doc({
            'doctype': 'Account',
            'account_name': account_account_name,
            'parent_account': parent_account,
            'company': company,
            'account_type': "Payable"
        })
        new_account_doc.insert()
        return new_account_doc.name

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            _("Something went wrong while creating credit account for {}"
              .format(frappe.utils.get_link_to_form("Supplier", doc.name)))
        )
        return None
