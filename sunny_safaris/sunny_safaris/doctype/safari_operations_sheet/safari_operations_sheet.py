# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SafariOperationsSheet(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		booking: DF.Link | None
		booking_reference: DF.Data | None
		customer: DF.Link | None
		customer_name: DF.Data | None
		operation_date: DF.Date | None
		start_time: DF.Time | None
		end_time: DF.Time | None
		vehicle: DF.Link | None
		vehicle_name: DF.Data | None
		driver: DF.Link | None
		driver_name: DF.Data | None
		guide: DF.Link | None
		guide_name: DF.Data | None
		dispatch_status: DF.Select | None
		pickup_location: DF.Data | None
		dropoff_location: DF.Data | None
		route: DF.Text | None
		fuel_check: DF.Select | None
		vehicle_condition: DF.Select | None
		equipment_check: DF.Select | None
		notes: DF.Text | None
		amended_from: DF.Link | None
	# end: auto-generated types

	def validate(self):
		self.set_booking_details()
		self.set_vehicle_name()
		self.set_driver_name()
		self.set_guide_name()

	def set_booking_details(self):
		if self.booking:
			booking = frappe.db.get_value("Safari Booking", self.booking, ["customer", "name"])
			if booking:
				self.customer = booking[0]
				self.booking_reference = booking[1]
				self.set_customer_name()

	def set_customer_name(self):
		if self.customer:
			customer_name = frappe.db.get_value("Customer", self.customer, "customer_name")
			if customer_name:
				self.customer_name = customer_name

	def set_vehicle_name(self):
		if self.vehicle:
			model = frappe.db.get_value("Vehicle", self.vehicle, "model")
			if model:
				self.vehicle_name = model

	def set_driver_name(self):
		if self.driver:
			employee_name = frappe.db.get_value("Employee", self.driver, "employee_name")
			if employee_name:
				self.driver_name = employee_name

	def set_guide_name(self):
		if self.guide:
			employee_name = frappe.db.get_value("Employee", self.guide, "employee_name")
			if employee_name:
				self.guide_name = employee_name


@frappe.whitelist()
def get_unavailable_resources(operation_date: str, operations_sheet: str | None = None, booking: str | None = None):
	"""Vehicles / drivers / guides committed elsewhere on this operation date."""
	empty = {"vehicles": [], "drivers": [], "guides": []}
	if not operation_date:
		return empty

	vehicles, drivers, guides = set(), set(), set()

	# Other operations sheets on the same day.
	ops_filters = {"docstatus": ["<", 2], "operation_date": operation_date}
	if operations_sheet:
		ops_filters["name"] = ["!=", operations_sheet]
	for r in frappe.get_all(
		"Safari Operations Sheet", filters=ops_filters, fields=["vehicle", "driver", "guide"]
	):
		vehicles.add(r.vehicle)
		drivers.add(r.driver)
		guides.add(r.guide)

	# Bookings whose date range covers this day (excluding this sheet's own booking).
	booking_filters = {
		"docstatus": ["<", 2],
		"booking_status": ["!=", "Cancelled"],
		"start_date": ["<=", operation_date],
		"end_date": [">=", operation_date],
	}
	if booking:
		booking_filters["name"] = ["!=", booking]
	others = frappe.get_all("Safari Booking", filters=booking_filters, pluck="name")
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

	return {
		"vehicles": sorted(v for v in vehicles if v),
		"drivers": sorted(d for d in drivers if d),
		"guides": sorted(g for g in guides if g),
	}
