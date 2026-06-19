# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_months, getdate, today

OPEN_JOB = ("Draft", "Pending", "In Progress")


def _month_keys(n=12):
	start = getdate(today()).replace(day=1)
	first = add_months(start, -(n - 1))
	return [getdate(add_months(first, i)) for i in range(n)]


def _group(doctype, field):
	# doctype/field are fixed constants in this module (never user input).
	rows = frappe.db.sql(
		f"""
		select coalesce(`{field}`, 'Not Set') as label, count(*) as value
		from `tab{doctype}`
		where docstatus < 2
		group by `{field}`
		order by value desc
		""",
		as_dict=True,
	)
	return {
		"labels": [r.label for r in rows],
		"values": [r.value for r in rows],
	}


@frappe.whitelist()
def get_analytics():
	booking = "Safari Booking"

	total_bookings = frappe.db.count(booking, {"docstatus": ["<", 2]})
	confirmed = frappe.db.count(booking, {"docstatus": ["<", 2], "booking_status": "Confirmed"})

	totals = frappe.db.sql(
		"""
		select
			coalesce(sum(total_amount), 0) as revenue,
			coalesce(sum(amount_paid), 0) as collected,
			coalesce(sum(outstanding_amount), 0) as outstanding,
			count(distinct customer) as customers
		from `tabSafari Booking`
		where docstatus < 2 and ifnull(booking_status, '') != 'Cancelled'
		""",
		as_dict=True,
	)[0]

	open_jobs = frappe.db.count("Workshop Job Card", {"docstatus": ["<", 2], "job_status": ["in", OPEN_JOB]})
	fleet = frappe.db.count("Vehicle")

	# Monthly revenue + bookings (last 12 months)
	months = _month_keys(12)
	first = months[0].strftime("%Y-%m-01")
	monthly = frappe.db.sql(
		"""
		select date_format(start_date, '%%Y-%%m') as m,
			count(name) as cnt, coalesce(sum(total_amount), 0) as amt
		from `tabSafari Booking`
		where docstatus < 2 and ifnull(booking_status, '') != 'Cancelled'
			and start_date >= %s
		group by m
		""",
		(first,),
		as_dict=True,
	)
	mmap = {r.m: r for r in monthly}
	month_labels = [d.strftime("%b %y") for d in months]
	revenue_series = [float(mmap.get(d.strftime("%Y-%m"), {}).get("amt", 0) or 0) for d in months]
	booking_series = [int(mmap.get(d.strftime("%Y-%m"), {}).get("cnt", 0) or 0) for d in months]

	return {
		"kpis": {
			"total_bookings": total_bookings,
			"confirmed": confirmed,
			"revenue": totals.revenue,
			"collected": totals.collected,
			"outstanding": totals.outstanding,
			"customers": totals.customers,
			"fleet": fleet,
			"open_jobs": open_jobs,
		},
		"charts": {
			"bookings_by_status": _group(booking, "booking_status"),
			"bookings_by_package": _group(booking, "package_type"),
			"jobcards_by_status": _group("Workshop Job Card", "job_status"),
			"dispatch_by_status": _group("Safari Operations Sheet", "dispatch_status"),
			"revenue_by_month": {"labels": month_labels, "values": revenue_series},
			"bookings_by_month": {"labels": month_labels, "values": booking_series},
		},
	}
