// Copyright (c) 2026, Rono and contributors
// Adds "Create > Safari Booking" to the Lead form.

frappe.ui.form.on("Lead", {
	refresh(frm) {
		if (frm.is_new()) return;
		sunny_safaris.add_booking_button(frm, (frm) => ({
			lead: frm.doc.name,
			customer_name: frm.doc.company_name || frm.doc.lead_name,
		}));
	},
});
