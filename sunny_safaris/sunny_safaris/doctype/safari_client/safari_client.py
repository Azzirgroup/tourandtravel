# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SafariClient(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		cancelled_bookings: DF.Int
		completed_bookings: DF.Int
		confirmed_bookings: DF.Int
		customer: DF.Link
		customer_group: DF.Link | None
		customer_name: DF.Data | None
		first_booking_date: DF.Date | None
		last_booking_date: DF.Date | None
		notes: DF.TextEditor | None
		outstanding_balance: DF.Currency
		territory: DF.Link | None
		total_booking_value: DF.Currency
		total_bookings: DF.Int
		total_operations: DF.Int
		total_paid: DF.Currency
	# end: auto-generated types

	def validate(self):
		self.update_summary()

	def update_summary(self):
		"""Recompute the rolled-up booking figures for this client."""
		bookings = frappe.get_all(
			"Safari Booking",
			filters={"customer": self.customer, "docstatus": ["<", 2]},
			fields=[
				"booking_status",
				"total_amount",
				"deposit_paid",
				"balance_paid",
				"balance_amount",
				"start_date",
			],
		)

		self.total_bookings = len(bookings)
		self.confirmed_bookings = sum(1 for b in bookings if b.booking_status == "Confirmed")
		self.completed_bookings = sum(1 for b in bookings if b.booking_status == "Completed")
		self.cancelled_bookings = sum(1 for b in bookings if b.booking_status == "Cancelled")

		# Cancelled bookings are excluded from financial roll-ups.
		active = [b for b in bookings if b.booking_status != "Cancelled"]
		self.total_booking_value = sum(b.total_amount or 0 for b in active)
		self.total_paid = sum((b.deposit_paid or 0) + (b.balance_paid or 0) for b in active)
		self.outstanding_balance = sum(b.balance_amount or 0 for b in active)

		dates = sorted(b.start_date for b in bookings if b.start_date)
		self.first_booking_date = dates[0] if dates else None
		self.last_booking_date = dates[-1] if dates else None

		self.total_operations = frappe.db.count(
			"Safari Operations Sheet", {"customer": self.customer, "docstatus": ["<", 2]}
		)


def update_for_booking(doc, method=None):
	"""Doc event on Safari Booking: ensure the client master exists and is current."""
	customer = doc.get("customer")
	if not customer or not frappe.db.exists("Customer", customer):
		return

	if frappe.db.exists("Safari Client", customer):
		client = frappe.get_doc("Safari Client", customer)
		client.save(ignore_permissions=True)
	else:
		client = frappe.new_doc("Safari Client")
		client.customer = customer
		client.insert(ignore_permissions=True)


def sync_safari_clients():
	"""Create a Safari Client master for every customer that has a Safari Booking.

	Idempotent — safe to run on every migrate.
	"""
	if not frappe.db.exists("DocType", "Safari Booking"):
		return

	customers = frappe.get_all(
		"Safari Booking",
		filters={"customer": ["is", "set"]},
		distinct=True,
		pluck="customer",
	)

	for customer in customers:
		if not customer or not frappe.db.exists("Customer", customer):
			continue
		if frappe.db.exists("Safari Client", customer):
			doc = frappe.get_doc("Safari Client", customer)
			doc.save(ignore_permissions=True)
		else:
			doc = frappe.new_doc("Safari Client")
			doc.customer = customer
			doc.insert(ignore_permissions=True)

	frappe.db.commit()
