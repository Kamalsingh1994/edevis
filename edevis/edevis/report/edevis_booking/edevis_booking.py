import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Rechnungs-datum"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": _("Rechnungs-nummer"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 180,
        },
        {
            "label": _("Rechnungsnummer und Kundenname"),
            "fieldname": "customer_info",
            "fieldtype": "Data",
            "width": 250,
        },
        {
            "label": _("Bruttobetrag"),
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": _("Kundennummer = Debitorenkonto"),
            "fieldname": "debit_to",
            "fieldtype": "Link",
            "options": "Account",
            "width": 250,
        },
        {
            "label": _("Erlöskonto"),
            "fieldname": "income_account",
            "fieldtype": "Link",
            "options": "Account",
            "width": 250,
        },
    ]

def get_data(filters):
    conditions = get_conditions(filters)

    return frappe.db.sql(
        f"""
        SELECT 
            si.posting_date,
            si.name,
            CONCAT(si.name, ', ', si.customer_name) AS customer_info,
            si.grand_total,
            si.debit_to,
            (
                SELECT sii.account_head
                FROM `tabSales Taxes and Charges` sii
                WHERE sii.parent = si.name
                ORDER BY sii.idx ASC
                LIMIT 1
            ) AS income_account
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1
        {conditions}
        ORDER BY si.posting_date DESC
        """,
        filters,
        as_dict=True
    )


def get_conditions(filters):
    conds = ""
    if filters.get("from_date") and filters.get("to_date"):
        conds += " AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s"
    return conds
