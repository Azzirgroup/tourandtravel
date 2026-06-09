# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WorkshopJobCard(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		asset: DF.Link | None
		asset_name: DF.Data | None
		registration_number: DF.Data | None
		job_description: DF.Text | None
		job_type: DF.Select | None
		priority: DF.Select | None
		job_start_date: DF.Date | None
		job_end_date: DF.Date | None
		estimated_hours: DF.Float | None
		actual_hours: DF.Float | None
		mechanic: DF.Link | None
		mechanic_name: DF.Data | None
		foreman: DF.Link | None
		foreman_name: DF.Data | None
		job_status: DF.Select | None
		parts_used: list | None
		labour_cost: DF.Currency | None
		parts_cost: DF.Currency | None
		total_cost: DF.Currency | None
		diagnosis: DF.Text | None
		work_performed: DF.Text | None
		foreman_approval: DF.Select | None
		foreman_approval_date: DF.Date | None
		notes: DF.Text | None
		amended_from: DF.Link | None
	# end: auto-generated types

	def validate(self):
		self.set_asset_details()
		self.set_mechanic_name()
		self.set_foreman_name()
		self.calculate_total_cost()
		self.set_approval_date()

	def set_asset_details(self):
		if self.asset:
			asset = frappe.db.get_value("Asset", self.asset, ["asset_name", "serial_no"])
			if asset:
				self.asset_name = asset[0]
				self.registration_number = asset[1]

	def set_mechanic_name(self):
		if self.mechanic:
			employee_name = frappe.db.get_value("Employee", self.mechanic, "employee_name")
			if employee_name:
				self.mechanic_name = employee_name

	def set_foreman_name(self):
		if self.foreman:
			employee_name = frappe.db.get_value("Employee", self.foreman, "employee_name")
			if employee_name:
				self.foreman_name = employee_name

	def calculate_total_cost(self):
		parts_cost = 0
		if self.parts_used:
			for item in self.parts_used:
				if item.amount:
					parts_cost += item.amount
		self.parts_cost = parts_cost
		
		labour_cost = self.labour_cost or 0
		self.total_cost = parts_cost + labour_cost

	def set_approval_date(self):
		if self.foreman_approval == "Approved" and not self.foreman_approval_date:
			self.foreman_approval_date = frappe.utils.today()
