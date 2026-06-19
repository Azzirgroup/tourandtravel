// Copyright (c) 2026, Rono and contributors
// For license information, please see license.txt

frappe.pages["dispatch-board"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Dispatch Board"),
		single_column: true,
	});

	const date_field = page.add_field({
		fieldname: "operation_date",
		label: __("Date"),
		fieldtype: "Date",
		default: frappe.datetime.get_today(),
		change: () => load(),
	});

	page.set_primary_action(__("Refresh"), () => load(), "refresh");
	page.add_inner_button(__("New Operations Sheet"), () => {
		frappe.new_doc("Safari Operations Sheet", { operation_date: date_field.get_value() });
	});

	const ui = sunny_safaris.ui;
	const $body = $('<div class="ss-wrap"></div>').appendTo(page.body);

	const STATUS = { Draft: "gray", Ready: "blue", Dispatched: "purple", "In Progress": "orange", Completed: "green" };

	function load() {
		const date = date_field.get_value() || frappe.datetime.get_today();
		frappe.call({
			method: "sunny_safaris.sunny_safaris.page.dispatch_board.dispatch_board.get_dispatches",
			args: { date },
			callback: (r) => render((r.message && r.message.dispatches) || [], date),
		});
	}

	function render(rows, date) {
		const by = (s) => rows.filter((d) => d.dispatch_status === s).length;
		const tiles = ui.grid([
			ui.stat({ label: __("Total Dispatches"), value: rows.length, accent: "blue" }),
			ui.stat({ label: __("Ready"), value: by("Ready"), accent: "teal" }),
			ui.stat({ label: __("Dispatched"), value: by("Dispatched"), accent: "purple" }),
			ui.stat({ label: __("In Progress"), value: by("In Progress"), accent: "orange" }),
			ui.stat({ label: __("Completed"), value: by("Completed"), accent: "green" }),
		], 170);

		let table;
		if (!rows.length) {
			table = ui.card(
				__("Dispatches"),
				`<div class="ss-muted">${__("No operations sheets scheduled for this date.")}</div>`
			);
		} else {
			const trs = rows
				.map((d) => {
					const time = d.start_time ? frappe.datetime.str_to_user(d.start_time, true).split(" ").pop() : "";
					return `<tr>
						<td><a href="/app/safari-operations-sheet/${encodeURIComponent(d.name)}">${frappe.utils.escape_html(d.name)}</a></td>
						<td>${time}</td>
						<td>${frappe.utils.escape_html(d.customer_name || "")}</td>
						<td>${frappe.utils.escape_html(d.vehicle_name || d.vehicle || "")}</td>
						<td>${frappe.utils.escape_html(d.driver_name || "")}</td>
						<td>${frappe.utils.escape_html(d.guide_name || "")}</td>
						<td>${frappe.utils.escape_html(d.pickup_location || "")}</td>
						<td>${ui.pill(d.dispatch_status, STATUS)}</td>
					</tr>`;
				})
				.join("");
			table =
				`<table class="ss-table"><thead><tr>
					<th>${__("Operations Sheet")}</th><th>${__("Time")}</th><th>${__("Customer")}</th>
					<th>${__("Vehicle")}</th><th>${__("Driver")}</th><th>${__("Guide")}</th>
					<th>${__("Pickup")}</th><th>${__("Status")}</th>
				</tr></thead><tbody>${trs}</tbody></table>`;
		}

		$body.html(
			ui.hero(__("Dispatch Board"), __("Dispatches for {0}", [frappe.datetime.str_to_user(date)])) +
				tiles +
				table
		);
	}

	load();
};
