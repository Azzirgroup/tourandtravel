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
		self.check_resource_availability()

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

	def check_resource_availability(self):
		"""Prevent saving/submitting if vehicle/driver/guide is already assigned on the same date."""
		if not self.operation_date:
			return

		# Exclude this operations sheet when checking (None for new docs)
		ops_name = self.name if getattr(self, "name", None) else None
		unavailable = get_unavailable_resources(
			self.operation_date, operations_sheet=ops_name, booking=self.booking if self.booking else None
		)
		conflicts = []
		if self.vehicle and self.vehicle in unavailable.get("vehicles", []):
			conflicts.append(f"Vehicle {self.vehicle} is already assigned on {self.operation_date}.")
		if self.driver and self.driver in unavailable.get("drivers", []):
			conflicts.append(f"Driver {self.driver} is already assigned on {self.operation_date}.")
		if self.guide and self.guide in unavailable.get("guides", []):
			conflicts.append(f"Guide {self.guide} is already assigned on {self.operation_date}.")
		if conflicts:
			frappe.throw("\n".join(conflicts))

	def on_submit(self):
		"""On submit: prevent submitting if other submitted sheets use the same resources,
		and mark conflicting draft sheets as `Conflict` so users are aware.
		"""
		if not self.operation_date:
			return

		# Prevent submit if another SUBMITTED sheet already uses any of these resources
		submitted_filters = {"docstatus": 1, "operation_date": self.operation_date, "name": ["!=", self.name]}
		for r in frappe.get_all(
			"Safari Operations Sheet",
			filters=submitted_filters,
			fields=["name", "vehicle", "driver", "guide"],
		):
			if (self.vehicle and self.vehicle == r.vehicle) or (
				self.driver and self.driver == r.driver
			) or (self.guide and self.guide == r.guide):
				frappe.throw(
					f"Cannot submit: resource conflict with submitted Operations Sheet {r.name}"
				)

		# Mark conflicting DRAFT sheets as Conflict (so users can notice and act)
		draft_filters = {"docstatus": 0, "operation_date": self.operation_date, "name": ["!=", self.name]}
		for r in frappe.get_all(
			"Safari Operations Sheet",
			filters=draft_filters,
			fields=["name", "vehicle", "driver", "guide"],
		):
			conflict = False
			if self.vehicle and self.vehicle == r.vehicle:
				conflict = True
			if self.driver and self.driver == r.driver:
				conflict = True
			if self.guide and self.guide == r.guide:
				conflict = True
			if conflict:
				# update dispatch_status without running validation on the other doc
				try:
					frappe.db.set_value("Safari Operations Sheet", r.name, "dispatch_status", "Conflict")
				except Exception:
					# fallback: log and continue
					frappe.log_error(f"Failed to mark {r.name} as Conflict on submit of {self.name}")

	def on_cancel(self):
		"""When this sheet is cancelled, clear Conflict markers on other draft sheets that referenced it.
		This is conservative: it only clears Conflict where the resource exactly matches this sheet's.
		"""
		if not self.operation_date:
			return

		draft_filters = {"docstatus": 0, "operation_date": self.operation_date, "name": ["!=", self.name]}
		for r in frappe.get_all(
			"Safari Operations Sheet",
			filters=draft_filters,
			fields=["name", "vehicle", "driver", "guide", "dispatch_status"],
		):
			if r.dispatch_status == "Conflict":
				# only clear if the conflicting resource was this sheet's
				if (self.vehicle and self.vehicle == r.vehicle) or (
					self.driver and self.driver == r.driver
				) or (self.guide and self.guide == r.guide):
					try:
						frappe.db.set_value("Safari Operations Sheet", r.name, "dispatch_status", "Draft")
					except Exception:
						frappe.log_error(f"Failed to clear Conflict on {r.name} after cancelling {self.name}")


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
