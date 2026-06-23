# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe

SUMMARY_FIELDS = (
	"safari_total_bookings",
	"safari_confirmed_bookings",
	"safari_total_booking_value",
	"safari_total_paid",
	"safari_outstanding_balance",
	"safari_last_booking_date",
)


def compute_customer_summary(customer):
	"""Roll up a customer's safari bookings into the Customer summary fields."""
	bookings = frappe.get_all(
		"Safari Booking",
		filters={"customer": customer, "docstatus": ["<", 2]},
		fields=[
			"booking_status",
			"total_amount",
			"deposit_paid",
			"balance_paid",
			"balance_amount",
			"start_date",
		],
	)

	active = [b for b in bookings if b.booking_status != "Cancelled"]
	dates = sorted(b.start_date for b in bookings if b.start_date)

	return {
		"safari_total_bookings": len(bookings),
		"safari_confirmed_bookings": sum(1 for b in bookings if b.booking_status == "Confirmed"),
		"safari_total_booking_value": sum(b.total_amount or 0 for b in active),
		"safari_total_paid": sum((b.deposit_paid or 0) + (b.balance_paid or 0) for b in active),
		"safari_outstanding_balance": sum(b.balance_amount or 0 for b in active),
		"safari_last_booking_date": dates[-1] if dates else None,
	}


def update_customer_safari_summary(doc, method=None):
	"""Safari Booking doc event: refresh the linked customer's safari summary."""
	customer = doc.get("customer")
	if not customer or not frappe.db.exists("Customer", customer):
		return
	# Custom fields may not exist yet on a fresh install/migrate.
	if not frappe.db.has_column("Customer", "safari_total_bookings"):
		return

	frappe.db.set_value(
		"Customer",
		customer,
		compute_customer_summary(customer),
		update_modified=False,
	)


def recompute_all_customers():
	"""Backfill the safari summary for every customer that has a booking."""
	if not frappe.db.has_column("Customer", "safari_total_bookings"):
		return

	customers = frappe.get_all(
		"Safari Booking",
		filters={"customer": ["is", "set"]},
		distinct=True,
		pluck="customer",
	)
	for customer in customers:
		if customer and frappe.db.exists("Customer", customer):
			frappe.db.set_value(
				"Customer", customer, compute_customer_summary(customer), update_modified=False
			)
	frappe.db.commit()
