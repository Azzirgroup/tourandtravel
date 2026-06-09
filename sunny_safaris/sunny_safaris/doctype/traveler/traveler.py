# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Traveler(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		passenger_name: DF.Data | None
		passport_number: DF.Data | None
		nationality: DF.Data | None
		date_of_birth: DF.Date | None
		gender: DF.Select | None
		age: DF.Int | None
		special_requirements: DF.Text | None
		dietary_restrictions: DF.Text | None
		medical_conditions: DF.Text | None
	# end: auto-generated types

	def validate(self):
		self.calculate_age()

	def calculate_age(self):
		if self.date_of_birth:
			from datetime import date
			today = frappe.utils.getdate(date.today())
			birth_date = frappe.utils.getdate(self.date_of_birth)
			self.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
