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
