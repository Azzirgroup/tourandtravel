// Copyright (c) 2026, Rono and contributors
// For license information, please see license.txt

frappe.ui.form.on("Safari Booking", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.docstatus === 2) return;

		// A booking can have many operations sheets (one per day / dispatch).
		frm.add_custom_button(
			__("Operations Sheet"),
			() => {
				frappe.model.with_doctype("Safari Operations Sheet", function () {
					const doc = frappe.model.get_new_doc("Safari Operations Sheet");
					doc.booking = frm.doc.name;
					doc.customer = frm.doc.customer;
					doc.customer_name = frm.doc.customer_name;
					doc.operation_date = frm.doc.start_date;
					frappe.set_route("Form", "Safari Operations Sheet", doc.name);
				});
			},
			__("Create")
		);
	},
});
