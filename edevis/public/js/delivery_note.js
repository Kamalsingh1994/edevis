frappe.ui.form.on("Delivery Note", {
    onload(frm) {
        frm.remove_custom_button("Installation Note", "Create");
        frm.remove_custom_button("Delivery Trip", "Create");
    },
    refresh(frm) {
        if (frm.doc.docstatus == 1) {
            setTimeout(() => {
                frm.remove_custom_button("Installation Note", "Create");
                frm.remove_custom_button("Delivery Trip", "Create");
            }, 10);

            frm.add_custom_button(__("Proforma Invoice"), function () {
                frappe.call({
                    method: "frappe.client.insert",
                    args: {
                        doc: {
                            doctype: "Proforma Invoice",
                            delivery_note: frm.doc.name
                        }
                    },
                    callback: function (response) {
                        if (!response.exc) {

                            frappe.set_route("proforma-invoice", response.message.name);
                        } else {
                            frappe.msgprint("Error creating Proforma Invoice");
                        }
                    }
                });
            }, __("Create"));
        }
    },
})




frappe.ui.form.on('Delivery Note Item', {
    custom_available_serial_no(frm, cdt, cdn) {
        render_serial_nos(frm, cdt, cdn);
    }
});

function render_serial_nos(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    if (!row.item_code || !row.warehouse) {
        frappe.msgprint("Please select Item Code and Warehouse first.");
        return;
    }

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Serial No",
            filters: {
                item_code: row.item_code,
                warehouse: row.warehouse,
                status: "Active"
            },
            fields: ["name"]
        },
        callback: function (r) {
            if (r.message && r.message.length > 0) {
                let serial_nos = r.message;

                let existing_serials = row.serial_no ? row.serial_no.split('\n') : [];
                let existing_serial_set = new Set(existing_serials);

                let filtered_serials = serial_nos.filter(s => !existing_serial_set.has(s.name));

                if (filtered_serials.length === 0) {
                    frappe.msgprint("All available serial numbers are already selected.");
                    return;
                }

                let modal_id = "custom-serial-modal";
                let modal_html = `
                    <div class="modal fade" id="${modal_id}" tabindex="-1" role="dialog" aria-labelledby="serialModalLabel" aria-hidden="true">
                      <div class="modal-dialog modal-lg" role="document">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title">Select Serial Numbers</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                              <span aria-hidden="true">&times;</span>
                            </button>
                          </div>
                          <div class="modal-body">
                            <table class="table table-bordered">
                              <thead>
                                <tr><th>Select</th><th>Serial No</th></tr>
                              </thead>
                              <tbody>
                                ${filtered_serials.map(s => `
                                  <tr>
                                    <td><input type="checkbox" value="${s.name}"></td>
                                    <td>${s.name}</td>
                                  </tr>`).join('')}
                              </tbody>
                            </table>
                          </div>
                          <div class="modal-footer">
                            <button type="button" class="btn btn-primary" id="add-serials-btn">Add Selected</button>
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                          </div>
                        </div>
                      </div>
                    </div>`;

                $(`#${modal_id}`).remove();

                $('body').append(modal_html);

                $(`#${modal_id}`).modal('show');

                $(document).off('click', '#add-serials-btn').on('click', '#add-serials-btn', function () {
                    let selected_serial_nos = [];
                    $(`#${modal_id}`).find('input[type=checkbox]:checked').each(function () {
                        selected_serial_nos.push($(this).val());
                    });

                    let new_serials = existing_serials.concat(selected_serial_nos);
                    let unique_serials = [...new Set(new_serials)];

                    frappe.model.set_value(cdt, cdn, "serial_no", unique_serials.join('\n'));

                    $(`#${modal_id}`).modal('hide');
                });

            } else {
                frappe.msgprint("No active serial numbers found for this item and warehouse.");
            }
        }
    });
}




