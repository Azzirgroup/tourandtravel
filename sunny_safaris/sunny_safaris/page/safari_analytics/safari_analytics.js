// Copyright (c) 2026, Rono and contributors
// For license information, please see license.txt

frappe.pages["safari-analytics"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Safari Analytics"),
		single_column: true,
	});
	page.set_primary_action(__("Refresh"), () => load(), "refresh");

	const ui = sunny_safaris.ui;
	const $body = $('<div class="ss-wrap"></div>').appendTo(page.body);

	function load() {
		frappe.call({
			method: "sunny_safaris.sunny_safaris.page.safari_analytics.safari_analytics.get_analytics",
			freeze: true,
			callback: (r) => r.message && render(r.message),
		});
	}

	function render(d) {
		const k = d.kpis;
		const tiles = ui.grid([
			ui.stat({ label: __("Total Bookings"), value: k.total_bookings, accent: "blue" }),
			ui.stat({ label: __("Confirmed"), value: k.confirmed, accent: "teal" }),
			ui.stat({ label: __("Revenue"), value: ui.currency(k.revenue), accent: "green" }),
			ui.stat({ label: __("Collected"), value: ui.currency(k.collected), accent: "purple" }),
			ui.stat({ label: __("Outstanding"), value: ui.currency(k.outstanding), accent: "red" }),
			ui.stat({ label: __("Customers"), value: k.customers, accent: "blue" }),
			ui.stat({ label: __("Fleet Vehicles"), value: k.fleet, accent: "teal" }),
			ui.stat({ label: __("Open Job Cards"), value: k.open_jobs, accent: "orange" }),
		], 180);

		// chart card shells
		const charts = [
			["c_rev", __("Revenue Trend (12 mo)")],
			["c_bookings", __("Bookings Over Time")],
			["c_status", __("Bookings by Status")],
			["c_package", __("Bookings by Package")],
			["c_jobs", __("Job Cards by Status")],
			["c_dispatch", __("Operations by Dispatch Status")],
		];
		const cardsHtml = charts
			.map(([id, title]) => ui.card(title, `<div id="${id}" class="ss-chart"></div>`))
			.join("");

		$body.html(
			ui.hero(__("Safari Analytics"), __("Bookings, revenue and operations at a glance")) +
				tiles +
				`<div class="ss-cols-2">${cardsHtml}</div>`
		);

		const C = d.charts;
		ui.chart("#c_rev", {
			data: { labels: C.revenue_by_month.labels, datasets: [{ name: __("Revenue"), values: C.revenue_by_month.values }] },
			type: "bar",
			height: 260,
			colors: ["#2bb673"],
			axisOptions: { xIsSeries: true },
		});
		ui.chart("#c_bookings", {
			data: { labels: C.bookings_by_month.labels, datasets: [{ name: __("Bookings"), values: C.bookings_by_month.values }] },
			type: "line",
			height: 260,
			colors: ["#5e9cea"],
			lineOptions: { regionFill: 1, hideDots: 0 },
			axisOptions: { xIsSeries: true },
		});
		ui.chart("#c_status", {
			data: { labels: C.bookings_by_status.labels, datasets: [{ values: C.bookings_by_status.values }] },
			type: "donut",
			height: 260,
			colors: ui.PALETTE,
		});
		ui.chart("#c_package", {
			data: { labels: C.bookings_by_package.labels, datasets: [{ values: C.bookings_by_package.values }] },
			type: "pie",
			height: 260,
			colors: ui.PALETTE,
		});
		ui.chart("#c_jobs", {
			data: { labels: C.jobcards_by_status.labels, datasets: [{ values: C.jobcards_by_status.values }] },
			type: "donut",
			height: 260,
			colors: ui.PALETTE,
		});
		ui.chart("#c_dispatch", {
			data: { labels: C.dispatch_by_status.labels, datasets: [{ values: C.dispatch_by_status.values }] },
			type: "pie",
			height: 260,
			colors: ui.PALETTE,
		});
	}

	load();
};
