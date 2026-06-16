// Copyright (c) 2026, Rono and contributors
// Adds "Create > Safari Booking" to the Quotation form.

frappe.ui.form.on("Quotation", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.docstatus === 2) return;
		sunny_safaris.add_booking_button(frm, (frm) => {
			const values = {
				quotation: frm.doc.name,
				contact: frm.doc.contact_person,
				customer_name: frm.doc.customer_name || frm.doc.party_name,
				total_amount: frm.doc.rounded_total || frm.doc.grand_total,
			};
			if (frm.doc.quotation_to === "Customer") {
				values.customer = frm.doc.party_name;
			} else if (frm.doc.quotation_to === "Lead") {
				values.lead = frm.doc.party_name;
			}
			return values;
		});
	},
});
