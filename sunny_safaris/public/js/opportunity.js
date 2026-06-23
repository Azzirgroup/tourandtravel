// Copyright (c) 2026, Rono and contributors
// Adds "Create > Safari Booking" to the Opportunity form.

frappe.ui.form.on("Opportunity", {
	refresh(frm) {
		if (frm.is_new()) return;
		sunny_safaris.add_booking_button(frm, (frm) => {
			const values = {
				opportunity: frm.doc.name,
				contact: frm.doc.contact_person,
				customer_name: frm.doc.customer_name || frm.doc.party_name,
			};
			if (frm.doc.opportunity_from === "Customer") {
				values.customer = frm.doc.party_name;
			} else if (frm.doc.opportunity_from === "Lead") {
				values.lead = frm.doc.party_name;
			}
			return values;
		});
	},
});
