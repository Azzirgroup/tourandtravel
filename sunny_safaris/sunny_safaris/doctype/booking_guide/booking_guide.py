# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BookingGuide(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		guide: DF.Link | None
		guide_name: DF.Data | None
		guide_type: DF.Select | None
		assignment_date: DF.Date | None
		assignment_status: DF.Select | None
		notes: DF.Text | None
	# end: auto-generated types

	def validate(self):
		self.set_guide_name()

	def set_guide_name(self):
		if self.guide:
			employee_name = frappe.db.get_value("Employee", self.guide, "employee_name")
			if employee_name:
				self.guide_name = employee_name
