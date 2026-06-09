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
			asset_name = frappe.db.get_value("Asset", self.vehicle, "asset_name")
			if asset_name:
				self.vehicle_name = asset_name

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
