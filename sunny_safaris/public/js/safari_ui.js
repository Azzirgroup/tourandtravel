// Copyright (c) 2026, Rono and contributors
// Shared UI helpers for Sunny Safaris desk pages (KPI tiles, cards, charts).

frappe.provide("sunny_safaris.ui");

(function (ui) {
	const esc = (v) => frappe.utils.escape_html(v == null ? "" : String(v));

	ui.hero = function (title, subtitle) {
		return `<div class="ss-hero"><div>
			<h2>${esc(title)}</h2>
			${subtitle ? `<div class="ss-hero-sub">${esc(subtitle)}</div>` : ""}
		</div></div>`;
	};

	ui.stat = function ({ label, value, sub, accent = "blue" }) {
		return `<div class="ss-stat ss-accent-${accent}">
			<div class="ss-stat-label">${esc(label)}</div>
			<div class="ss-stat-value">${value == null ? "" : value}</div>
			${sub ? `<div class="ss-stat-sub">${sub}</div>` : ""}
		</div>`;
	};

	ui.grid = function (items, min) {
		return `<div class="ss-grid" style="--ss-min:${min || 200}px">${items.join("")}</div>`;
	};

	ui.card = function (title, innerHtml) {
		return `<div class="ss-card">
			<div class="ss-card-head">${esc(title)}</div>
			<div class="ss-card-body">${innerHtml || ""}</div>
		</div>`;
	};

	ui.pill = function (value, colorMap) {
		const color = (colorMap && colorMap[value]) || "gray";
		return `<span class="indicator-pill ${color}">${esc(value)}</span>`;
	};

	ui.currency = function (v) {
		return format_currency(v || 0);
	};

	// Mount a frappe Chart into an element id. Safe no-op if frappe.Chart missing.
	ui.chart = function (selector, opts) {
		if (!frappe.Chart) return null;
		const el = typeof selector === "string" ? document.querySelector(selector) : selector;
		if (!el) return null;
		return new frappe.Chart(el, opts);
	};

	ui.PALETTE = ["#2bb673", "#5e9cea", "#f5a623", "#9b7bd4", "#e8705f", "#2bb6a3", "#f06292"];
})(sunny_safaris.ui);
