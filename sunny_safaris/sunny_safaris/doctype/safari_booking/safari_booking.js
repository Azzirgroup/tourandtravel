// Copyright (c) 2026, Rono and contributors
// For license information, please see license.txt

frappe.ui.form.on("Safari Booking", {
	onload(frm) {
		set_availability_queries(frm);
	},

	refresh(frm) {
		set_availability_queries(frm);
		load_availability(frm);

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

		// Invoice the booking (single "Safari Package" line = total amount).
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(
				__("Sales Invoice"),
				() => {
					frappe.model.open_mapped_doc({
						method: "sunny_safaris.sunny_safaris.doctype.safari_booking.safari_booking.make_sales_invoice",
						frm: frm,
					});
				},
				__("Create")
			);
		}
	},

	start_date: (frm) => load_availability(frm),
	end_date: (frm) => load_availability(frm),

	vehicle_assignments_add: (frm) => warn_if_no_dates(frm),
	guides_add: (frm) => warn_if_no_dates(frm),
});

// Fetch the resources already committed to overlapping trips and cache on the form.
function load_availability(frm) {
	if (!frm.doc.start_date || !frm.doc.end_date) {
		frm._unavail = { vehicles: [], drivers: [], guides: [] };
		return;
	}
	frappe.call({
		method: "sunny_safaris.sunny_safaris.doctype.safari_booking.safari_booking.get_unavailable_resources",
		args: { start_date: frm.doc.start_date, end_date: frm.doc.end_date, booking: frm.doc.name },
		callback: (r) => {
			frm._unavail = r.message || { vehicles: [], drivers: [], guides: [] };
		},
	});
}

// Restrict each link field's options to resources that are free for the dates.
function set_availability_queries(frm) {
	const exclude = (key) => () => {
		const list = (frm._unavail && frm._unavail[key]) || [];
		return list.length ? { filters: { name: ["not in", list] } } : {};
	};
	frm.set_query("vehicle", "vehicle_assignments", exclude("vehicles"));
	frm.set_query("driver", "vehicle_assignments", exclude("drivers"));
	frm.set_query("guide", "guides", exclude("guides"));
}

function warn_if_no_dates(frm) {
	if (!frm.doc.start_date || !frm.doc.end_date) {
		frappe.show_alert({
			message: __("Set Start and End dates first so availability can be checked."),
			indicator: "orange",
		});
	}
}
