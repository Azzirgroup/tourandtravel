# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SupplierReservation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		supplier: DF.Link | None
		supplier_name: DF.Data | None
		supplier_type: DF.Select | None
		reservation_date: DF.Date | None
		reservation_status: DF.Select | None
		confirmation_number: DF.Data | None
		amount: DF.Currency | None
		notes: DF.Text | None
	# end: auto-generated types

	def validate(self):
		self.set_supplier_name()

	def set_supplier_name(self):
		if self.supplier:
			supplier_name = frappe.db.get_value("Supplier", self.supplier, "supplier_name")
			if supplier_name:
				self.supplier_name = supplier_name
