import frappe
from frappe import _


def update_serial_no(doc, method):
    item_code = (doc.get("item_code") or "").strip()
    serial_no = (doc.get("serial_no") or doc.get("sr_no") or "").strip()

    # If required fields are missing, skip custom naming
    if not item_code or not serial_no:
        return

    new_name = f"{item_code}:{serial_no}"

    # Enforce uniqueness
    if frappe.db.exists("Serial No", new_name):
        frappe.throw(_("Serial No with same Item Code and Serial No already exists."))

    # Set the document name
    doc.name = new_name
