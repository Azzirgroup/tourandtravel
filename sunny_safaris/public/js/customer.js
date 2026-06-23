// Copyright (c) 2026, Rono and contributors
// Adds "Create > Safari Booking" to the Customer form.

frappe.ui.form.on("Customer", {
	refresh(frm) {
		if (frm.is_new()) return;
		sunny_safaris.add_booking_button(frm, (frm) => ({
			customer: frm.doc.name,
			customer_name: frm.doc.customer_name,
		}));
	},
});
