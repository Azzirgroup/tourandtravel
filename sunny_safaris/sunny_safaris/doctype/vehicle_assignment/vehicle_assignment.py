# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VehicleAssignment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		vehicle: DF.Link | None
		vehicle_name: DF.Data | None
		driver: DF.Link | None
		driver_name: DF.Data | None
		assignment_date: DF.Date | None
		assignment_status: DF.Select | None
		notes: DF.Text | None
	# end: auto-generated types

	def validate(self):
		self.set_vehicle_name()
		self.set_driver_name()

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
