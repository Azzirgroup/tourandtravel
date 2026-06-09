// Copyright (c) 2026, Rono and contributors
// For license information, please see license.txt

frappe.ui.form.on("Safari Client", {
	refresh(frm) {
		if (frm.doc.customer && !frm.is_new()) {
			frm.add_custom_button(__("Recalculate Summary"), () => {
				frm.save();
			});
			frm.add_custom_button(__("New Booking"), () => {
				frappe.new_doc("Safari Booking", { customer: frm.doc.customer });
			});
		}
	},
});
