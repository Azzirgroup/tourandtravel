// Copyright (c) 2026, Rono and contributors
// Shared helper for creating a Safari Booking from CRM documents.
// Loaded into every CRM form via doctype_js (guarded so it defines once).

frappe.provide("sunny_safaris");

if (!sunny_safaris.create_safari_booking) {
	sunny_safaris.create_safari_booking = function (values) {
		frappe.model.with_doctype("Safari Booking", function () {
			const doc = frappe.model.get_new_doc("Safari Booking");
			Object.keys(values || {}).forEach((key) => {
				if (values[key]) {
					doc[key] = values[key];
				}
			});
			frappe.set_route("Form", "Safari Booking", doc.name);
		});
	};

	sunny_safaris.add_booking_button = function (frm, values_fn) {
		frm.add_custom_button(
			__("Safari Booking"),
			() => sunny_safaris.create_safari_booking(values_fn(frm)),
			__("Create")
		);
	};
}
