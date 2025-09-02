import frappe

def execute():
    taxes = frappe.db.get_all(
        "Sales Taxes and Charges",
        filters={"charge_type": "Actual"},
        fields=["name", "parent"]
    )

    for tax in taxes:
        frappe.db.set_value(
            "Sales Taxes and Charges",
            tax.name,
            "description",
            "Versandkosten"
        )
    frappe.db.commit()
