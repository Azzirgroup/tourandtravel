// Copyright (c) 2026, Rono and contributors
// For license information, please see license.txt

frappe.ui.form.on("Safari Operations Sheet", {
	onload(frm) {
		set_availability_queries(frm);
	},

	refresh(frm) {
		set_availability_queries(frm);
		load_availability(frm);
	},

	operation_date(frm) {
		load_availability(frm);
	},
});

// Fetch resources busy on this operation date and cache on the form.
function load_availability(frm) {
	if (!frm.doc.operation_date) {
		frm._unavail = { vehicles: [], drivers: [], guides: [] };
		return;
	}
	frappe.call({
		method: "sunny_safaris.sunny_safaris.doctype.safari_operations_sheet.safari_operations_sheet.get_unavailable_resources",
		args: {
			operation_date: frm.doc.operation_date,
			operations_sheet: frm.doc.name,
			booking: frm.doc.booking,
		},
		callback: (r) => {
			frm._unavail = r.message || { vehicles: [], drivers: [], guides: [] };
		},
	});
}

// Restrict each link field to resources free on the date.
function set_availability_queries(frm) {
	const exclude = (key) => () => {
		const list = (frm._unavail && frm._unavail[key]) || [];
		return list.length ? { filters: { name: ["not in", list] } } : {};
	};
	frm.set_query("vehicle", exclude("vehicles"));
	frm.set_query("driver", exclude("drivers"));
	frm.set_query("guide", exclude("guides"));
}
