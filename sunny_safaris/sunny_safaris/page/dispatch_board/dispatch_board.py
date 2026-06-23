# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe


@frappe.whitelist()
def get_dispatches(date: str | None = None):
	"""Return the operations sheets scheduled for a given date (default: today)."""
	date = date or frappe.utils.today()
	rows = frappe.get_all(
		"Safari Operations Sheet",
		filters={"operation_date": date, "docstatus": ["<", 2]},
		fields=[
			"name",
			"booking",
			"customer_name",
			"vehicle",
			"vehicle_name",
			"driver_name",
			"guide_name",
			"start_time",
			"pickup_location",
			"dropoff_location",
			"dispatch_status",
		],
		order_by="start_time asc, name asc",
	)
	return {"date": date, "dispatches": rows}
