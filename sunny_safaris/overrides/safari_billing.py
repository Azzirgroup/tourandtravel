# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe

SAFARI_PACKAGE_ITEM = "Safari Package"
SAFARI_ITEM_GROUP = "Services"


def ensure_safari_package_item():
	"""Make sure the generic 'Safari Package' service item exists for invoicing."""
	if frappe.db.exists("Item", SAFARI_PACKAGE_ITEM):
		return
	group = SAFARI_ITEM_GROUP if frappe.db.exists("Item Group", SAFARI_ITEM_GROUP) else "All Item Groups"
	uom = "Nos" if frappe.db.exists("UOM", "Nos") else "Unit"
	frappe.get_doc(
		{
			"doctype": "Item",
			"item_code": SAFARI_PACKAGE_ITEM,
			"item_name": SAFARI_PACKAGE_ITEM,
			"item_group": group,
			"stock_uom": uom,
			"sales_uom": uom,
			"is_stock_item": 0,
			"is_sales_item": 1,
			"is_purchase_item": 0,
			"include_item_in_manufacturing": 0,
			"description": "Safari booking package (lump-sum charge).",
		}
	).insert(ignore_permissions=True)


def recompute_booking_payment(booking_name):
	"""Roll the linked Sales Invoices' settled amounts onto the booking."""
	if not booking_name or not frappe.db.exists("Safari Booking", booking_name):
		return
	if not frappe.db.has_column("Sales Invoice", "safari_booking"):
		return

	invoices = frappe.get_all(
		"Sales Invoice",
		filters={"safari_booking": booking_name, "docstatus": 1},
		fields=["grand_total", "outstanding_amount"],
	)
	invoiced = sum(i.grand_total or 0 for i in invoices)
	paid = sum((i.grand_total or 0) - (i.outstanding_amount or 0) for i in invoices)

	total = frappe.db.get_value("Safari Booking", booking_name, "total_amount") or 0
	# Outstanding is tracked against the booking value when set, else against invoiced.
	basis = total or invoiced
	outstanding = max(basis - paid, 0)

	if paid <= 0:
		status = "Unpaid"
	elif basis and paid >= basis:
		status = "Paid"
	else:
		status = "Partial"

	frappe.db.set_value(
		"Safari Booking",
		booking_name,
		{
			"amount_paid": paid,
			"outstanding_amount": outstanding,
			"payment_status": status,
		},
		update_modified=False,
	)


def update_booking_from_invoice(doc, method=None):
	"""Sales Invoice doc event."""
	if doc.get("safari_booking"):
		recompute_booking_payment(doc.safari_booking)


def set_payment_safari_booking(doc, method=None):
	"""Payment Entry doc event: inherit safari_booking from a referenced invoice.

	ERPNext's get_payment_entry does not copy custom fields, so populate it here
	whenever a payment references a Sales Invoice tied to a booking.
	"""
	if doc.get("safari_booking"):
		return
	if not frappe.db.has_column("Payment Entry", "safari_booking"):
		return
	for ref in doc.get("references") or []:
		if ref.reference_doctype == "Sales Invoice" and ref.reference_name:
			booking = frappe.db.get_value("Sales Invoice", ref.reference_name, "safari_booking")
			if booking:
				doc.safari_booking = booking
				break


def update_booking_from_payment(doc, method=None):
	"""Payment Entry doc event: refresh every booking touched by this payment."""
	bookings = set()
	if doc.get("safari_booking"):
		bookings.add(doc.safari_booking)
	for ref in doc.get("references") or []:
		if ref.reference_doctype == "Sales Invoice" and ref.reference_name:
			booking = frappe.db.get_value("Sales Invoice", ref.reference_name, "safari_booking")
			if booking:
				bookings.add(booking)
	for booking in bookings:
		recompute_booking_payment(booking)
