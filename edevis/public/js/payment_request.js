frappe.ui.form.on("Payment Request", {
    onload: function(frm) {
        // Check if this is the first time the form is loaded
        // and if custom_actual_amount is empty/zero
        if (!frm.doc.custom_actual_amount || frm.doc.custom_actual_amount == 0) {
            if (frm.doc.grand_total && frm.doc.grand_total > 0) {
                frm.set_value('custom_actual_amount', frm.doc.grand_total);
            }
        }
    },
    validate: function(frm) {
        if (frm.doc.custom_actual_amount > 0 && frm.doc.custom_portion > 0) {
            frm.set_value('grand_total', (frm.doc.custom_portion / 100) * frm.doc.custom_actual_amount);
        }
    },
    // Handle when custom_portion (percentage) changes
    custom_portion: function(frm) {
        // Recalculate grand_total based on custom_portion percentage of custom_actual_amount
        if (frm.doc.custom_actual_amount > 0 && frm.doc.custom_portion > 0) {
            
            // Calculate new grand_total: (custom_portion / 100) * custom_actual_amount
            let new_grand_total = (frm.doc.custom_portion / 100) * frm.doc.custom_actual_amount;
            
            // Update grand_total field
            frm.set_value('grand_total', new_grand_total);
        }
    },
})