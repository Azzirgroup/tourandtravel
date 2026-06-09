# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCardPart(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		item_code: DF.Link | None
		item_name: DF.Data | None
		quantity: DF.Float | None
		unit_price: DF.Currency | None
		amount: DF.Currency | None
	# end: auto-generated types

	def validate(self):
		self.set_item_name()
		self.calculate_amount()

	def set_item_name(self):
		if self.item_code:
			item_name = frappe.db.get_value("Item", self.item_code, "item_name")
			if item_name:
				self.item_name = item_name

	def calculate_amount(self):
		if self.quantity and self.unit_price:
			self.amount = self.quantity * self.unit_price
