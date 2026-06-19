// Copyright (c) 2026, Rono and contributors
// For license information, please see license.txt

frappe.pages["fleet-status"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Fleet Status"),
		single_column: true,
	});

	page.set_primary_action(__("Refresh"), () => load(), "refresh");
	page.add_inner_button(__("New Vehicle"), () => frappe.new_doc("Vehicle"));

	const ui = sunny_safaris.ui;
	const $body = $('<div class="ss-wrap"></div>').appendTo(page.body);
	const STATUS = { Available: "green", "On Safari": "blue", "In Workshop": "orange" };

	function detail_cell(row) {
		if (!row.detail) return `<span class="ss-muted">&mdash;</span>`;
		const d = row.detail;
		if (row.detail_type === "Workshop Job Card") {
			return `<a href="/app/workshop-job-card/${encodeURIComponent(d.name)}">${frappe.utils.escape_html(d.name)}</a> <span class="ss-muted">(${frappe.utils.escape_html(d.job_status || "")})</span>`;
		}
		const date = d.operation_date ? frappe.datetime.str_to_user(d.operation_date) : "";
		return `<a href="/app/safari-operations-sheet/${encodeURIComponent(d.name)}">${frappe.utils.escape_html(d.name)}</a>${date ? ` <span class="ss-muted">· ${date}</span>` : ""}`;
	}

	function load() {
		frappe.call({
			method: "sunny_safaris.sunny_safaris.page.fleet_status.fleet_status.get_fleet",
			callback: (r) => render(r.message || []),
		});
	}

	function render(rows) {
		const c = rows.reduce((a, r) => ((a[r.status] = (a[r.status] || 0) + 1), a), {});
		const tiles = ui.grid([
			ui.stat({ label: __("Total Vehicles"), value: rows.length, accent: "blue" }),
			ui.stat({ label: __("Available"), value: c["Available"] || 0, accent: "green" }),
			ui.stat({ label: __("On Safari"), value: c["On Safari"] || 0, accent: "purple" }),
			ui.stat({ label: __("In Workshop"), value: c["In Workshop"] || 0, accent: "orange" }),
		], 180);

		let table;
		if (!rows.length) {
			table = ui.card(__("Fleet"), `<div class="ss-muted">${__("No vehicles found.")}</div>`);
		} else {
			const trs = rows
				.map(
					(r) => `<tr>
						<td><a href="/app/vehicle/${encodeURIComponent(r.vehicle)}">${frappe.utils.escape_html(r.vehicle)}</a></td>
						<td>${frappe.utils.escape_html(r.make_model || "")}</td>
						<td>${ui.pill(r.status, STATUS)}</td>
						<td>${detail_cell(r)}</td>
						<td class="ss-right">${frappe.format(r.odometer, { fieldtype: "Int" })}</td>
					</tr>`
				)
				.join("");
			table =
				`<table class="ss-table"><thead><tr>
					<th>${__("Vehicle")}</th><th>${__("Make / Model")}</th><th>${__("Status")}</th>
					<th>${__("Current")}</th><th class="ss-right">${__("Odometer")}</th>
				</tr></thead><tbody>${trs}</tbody></table>`;
		}

		$body.html(ui.hero(__("Fleet Status"), __("Live vehicle availability")) + tiles + table);
	}

	load();
};
