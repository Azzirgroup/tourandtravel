# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SafariBooking(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		customer: DF.Link | None
		customer_name: DF.Data | None
		contact: DF.Link | None
		lead: DF.Link | None
		opportunity: DF.Link | None
		quotation: DF.Link | None
		sales_order: DF.Link | None
		project: DF.Link | None
		start_date: DF.Date | None
		end_date: DF.Date | None
		duration_days: DF.Int | None
		number_of_adults: DF.Int | None
		number_of_children: DF.Int | None
		total_guests: DF.Int | None
		package_type: DF.Select | None
		destination: DF.Data | None
		nationality: DF.Data | None
		booking_status: DF.Select | None
		payment_status: DF.Select | None
		travelers: list | None
		vehicle_assignments: list | None
		guides: list | None
		total_amount: DF.Currency | None
		deposit_amount: DF.Currency | None
		deposit_paid: DF.Currency | None
		balance_amount: DF.Currency | None
		balance_paid: DF.Currency | None
		supplier_reservations: list | None
		notes: DF.Text | None
	# end: auto-generated types

	def validate(self):
		self.calculate_duration()
		self.calculate_total_guests()
		self.calculate_financials()
		self.set_customer_name()

	def on_submit(self):
		# Move the workflow status off "Draft" once the booking is confirmed,
		# unless the user already advanced it to a later stage.
		if self.booking_status in (None, "", "Draft"):
			self.db_set("booking_status", "Confirmed")

	def on_cancel(self):
		self.db_set("booking_status", "Cancelled")

	def calculate_duration(self):
		if self.start_date and self.end_date:
			from datetime import datetime
			start = frappe.utils.getdate(self.start_date)
			end = frappe.utils.getdate(self.end_date)
			self.duration_days = (end - start).days + 1

	def calculate_total_guests(self):
		self.total_guests = (self.number_of_adults or 0) + (self.number_of_children or 0)

	def calculate_financials(self):
		if self.total_amount and self.deposit_amount:
			self.balance_amount = self.total_amount - self.deposit_amount

	def set_customer_name(self):
		if self.customer:
			customer = frappe.db.get_value("Customer", self.customer, "customer_name")
			if customer:
				self.customer_name = customer


@frappe.whitelist()
def get_unavailable_resources(start_date: str, end_date: str, booking: str | None = None):
	"""Vehicles / drivers / guides already committed to other trips that overlap the dates.

	Used by the booking form to filter selections to available resources only.
	"""
	empty = {"vehicles": [], "drivers": [], "guides": []}
	if not start_date or not end_date:
		return empty

	# Other (non-cancelled) bookings whose [start, end] overlaps this range.
	booking_filters = {
		"docstatus": ["<", 2],
		"booking_status": ["!=", "Cancelled"],
		"start_date": ["<=", end_date],
		"end_date": [">=", start_date],
	}
	if booking:
		booking_filters["name"] = ["!=", booking]
	others = frappe.get_all("Safari Booking", filters=booking_filters, pluck="name")

	vehicles, drivers, guides = set(), set(), set()

	if others:
		for r in frappe.get_all(
			"Vehicle Assignment",
			filters={"parenttype": "Safari Booking", "parent": ["in", others]},
			fields=["vehicle", "driver"],
		):
			vehicles.add(r.vehicle)
			drivers.add(r.driver)
		guides.update(
			frappe.get_all(
				"Booking Guide",
				filters={"parenttype": "Safari Booking", "parent": ["in", others]},
				pluck="guide",
			)
		)

	# Operations sheets scheduled inside the range (excluding this booking's own).
	for r in frappe.get_all(
		"Safari Operations Sheet",
		filters={"docstatus": ["<", 2], "operation_date": ["between", [start_date, end_date]]},
		fields=["vehicle", "driver", "guide", "booking"],
	):
		if booking and r.booking == booking:
			continue
		vehicles.add(r.vehicle)
		drivers.add(r.driver)
		guides.add(r.guide)

	return {
		"vehicles": sorted(v for v in vehicles if v),
		"drivers": sorted(d for d in drivers if d),
		"guides": sorted(g for g in guides if g),
	}


@frappe.whitelist()
def make_sales_invoice(source_name: str):
	"""Create a Sales Invoice for a booking with a single 'Safari Package' line."""
	from sunny_safaris.overrides.safari_billing import SAFARI_PACKAGE_ITEM, ensure_safari_package_item

	booking = frappe.get_doc("Safari Booking", source_name)
	ensure_safari_package_item()

	si = frappe.new_doc("Sales Invoice")
	si.customer = booking.customer
	si.safari_booking = booking.name
	si.append(
		"items",
		{
			"item_code": SAFARI_PACKAGE_ITEM,
			"qty": 1,
			"rate": booking.total_amount or 0,
		},
	)
	si.run_method("set_missing_values")
	return si
