# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

import frappe

HIRE_ITEM_GROUP = "Vehicle Hire"
HIRE_UOM = "Day"


def ensure_item_group():
	"""Make sure the 'Vehicle Hire' item group exists."""
	if frappe.db.exists("Item Group", HIRE_ITEM_GROUP):
		return
	parent = "All Item Groups" if frappe.db.exists("Item Group", "All Item Groups") else None
	frappe.get_doc(
		{
			"doctype": "Item Group",
			"item_group_name": HIRE_ITEM_GROUP,
			"parent_item_group": parent,
			"is_group": 0,
		}
	).insert(ignore_permissions=True)


def create_hire_item(doc, method=None):
	"""Vehicle doc event: create/refresh a linked 'Vehicle Hire' service Item."""
	plate = doc.name  # Vehicle is autonamed by license_plate
	label = " ".join(p for p in [doc.get("make"), doc.get("model")] if p) or plate
	item_code = f"Vehicle Hire - {plate}"

	ensure_item_group()
	uom = HIRE_UOM if frappe.db.exists("UOM", HIRE_UOM) else "Nos"

	if frappe.db.exists("Item", item_code):
		item = frappe.get_doc("Item", item_code)
	else:
		item = frappe.new_doc("Item")
		item.item_code = item_code

	item.update(
		{
			"item_name": f"Vehicle Hire - {label}",
			"item_group": HIRE_ITEM_GROUP,
			"stock_uom": uom,
			"sales_uom": uom,
			"is_stock_item": 0,
			"is_sales_item": 1,
			"is_purchase_item": 0,
			"include_item_in_manufacturing": 0,
			"description": f"Charter / hire of vehicle {plate}",
		}
	)
	if frappe.db.has_column("Item", "safari_vehicle"):
		item.safari_vehicle = doc.name
	item.save(ignore_permissions=True)

	# Link the item back onto the vehicle (no recursion: direct DB write).
	if frappe.db.has_column("Vehicle", "safari_hire_item"):
		frappe.db.set_value("Vehicle", doc.name, "safari_hire_item", item.name, update_modified=False)
