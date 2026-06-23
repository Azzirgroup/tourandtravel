# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe

ACTIVE_DISPATCH = ("Ready", "Dispatched", "In Progress")
OPEN_JOB = ("Draft", "Pending", "In Progress")


@frappe.whitelist()
def get_fleet():
	"""Return every vehicle with its current status (In Workshop / On Safari / Available)."""
	vehicles = frappe.get_all(
		"Vehicle",
		fields=["name", "make", "model", "last_odometer"],
		order_by="name asc",
	)

	result = []
	for v in vehicles:
		job = frappe.get_all(
			"Workshop Job Card",
			filters={"asset": v.name, "docstatus": ["<", 2], "job_status": ["in", OPEN_JOB]},
			fields=["name", "job_status"],
			order_by="modified desc",
			limit=1,
		)
		ops = frappe.get_all(
			"Safari Operations Sheet",
			filters={"vehicle": v.name, "docstatus": ["<", 2], "dispatch_status": ["in", ACTIVE_DISPATCH]},
			fields=["name", "booking", "operation_date", "dispatch_status"],
			order_by="operation_date desc",
			limit=1,
		)

		if job:
			status, detail_type, detail = "In Workshop", "Workshop Job Card", job[0]
		elif ops:
			status, detail_type, detail = "On Safari", "Safari Operations Sheet", ops[0]
		else:
			status, detail_type, detail = "Available", None, None

		result.append(
			{
				"vehicle": v.name,
				"make_model": " ".join(p for p in [v.make, v.model] if p),
				"odometer": v.last_odometer,
				"status": status,
				"detail_type": detail_type,
				"detail": detail,
			}
		)

	return result




#EOF
