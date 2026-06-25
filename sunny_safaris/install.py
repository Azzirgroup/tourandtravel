import frappe

# Number Cards rendered on the Sunny Safaris workspace.
# These must exist as `Number Card` documents for the workspace tiles to render,
# so we create them on install and keep them in sync on every migrate.
NUMBER_CARDS = [
	{
		"name": "Total Safari Bookings",
		"label": "Total Safari Bookings",
		"document_type": "Safari Booking",
		"function": "Count",
		"color": "#fb8c00",
		"filters_json": "[]",
	},
	{
		"name": "Confirmed Bookings",
		"label": "Confirmed Bookings",
		"document_type": "Safari Booking",
		"function": "Count",
		"color": "#1976d2",
		"filters_json": '[["Safari Booking","booking_status","=","Confirmed"]]',
	},
	{
		"name": "Booking Revenue",
		"label": "Booking Revenue",
		"document_type": "Safari Booking",
		"function": "Sum",
		"aggregate_function_based_on": "total_amount",
		"color": "#00897b",
		"filters_json": '[["Safari Booking","booking_status","!=","Cancelled"]]',
	},
	{
		"name": "Total Operations Sheets",
		"label": "Total Operations Sheets",
		"document_type": "Safari Operations Sheet",
		"function": "Count",
		"color": "#7c4dff",
		"filters_json": "[]",
	},
	{
		"name": "Open Workshop Job Cards",
		"label": "Open Workshop Job Cards",
		"document_type": "Workshop Job Card",
		"function": "Count",
		"color": "#43a047",
		"filters_json": '[["Workshop Job Card","job_status","not in",["Completed","Cancelled"]]]',
	},
]

# Custom fields the app adds to standard ERPNext doctypes. The Customer "Safari"
# summary lives on Customer itself (instead of a duplicate "Safari Client" master)
# and is kept current by the Safari Booking doc events in hooks.py. Vehicle/Item
# carry a bidirectional link to the auto-created hire item.
APP_CUSTOM_FIELDS = {
	"Customer": [
		{
			"fieldname": "safari_tab",
			"label": "Safari",
			"fieldtype": "Tab Break",
			"insert_after": "default_price_list",
		},
		{
			"fieldname": "safari_summary_section",
			"label": "Booking Summary",
			"fieldtype": "Section Break",
			"insert_after": "safari_tab",
		},
		{
			"fieldname": "safari_total_bookings",
			"label": "Total Safari Bookings",
			"fieldtype": "Int",
			"read_only": 1,
			"no_copy": 1,
			"insert_after": "safari_summary_section",
		},
		{
			"fieldname": "safari_confirmed_bookings",
			"label": "Confirmed Bookings",
			"fieldtype": "Int",
			"read_only": 1,
			"no_copy": 1,
			"insert_after": "safari_total_bookings",
		},
		{
			"fieldname": "safari_total_booking_value",
			"label": "Total Booking Value",
			"fieldtype": "Currency",
			"read_only": 1,
			"no_copy": 1,
			"insert_after": "safari_confirmed_bookings",
		},
		{
			"fieldname": "safari_summary_col",
			"fieldtype": "Column Break",
			"insert_after": "safari_total_booking_value",
		},
		{
			"fieldname": "safari_total_paid",
			"label": "Total Paid",
			"fieldtype": "Currency",
			"read_only": 1,
			"no_copy": 1,
			"insert_after": "safari_summary_col",
		},
		{
			"fieldname": "safari_outstanding_balance",
			"label": "Outstanding Balance",
			"fieldtype": "Currency",
			"read_only": 1,
			"no_copy": 1,
			"insert_after": "safari_total_paid",
		},
		{
			"fieldname": "safari_last_booking_date",
			"label": "Last Booking Date",
			"fieldtype": "Date",
			"read_only": 1,
			"no_copy": 1,
			"insert_after": "safari_outstanding_balance",
		},
	],
	# Bidirectional link between an ERPNext Vehicle and its auto-created hire Item.
	"Vehicle": [
		{
			"fieldname": "is_hired",
			"label": "Is Hired",
			"fieldtype": "Check",
			"default": "0",
			"insert_after": "model",
			"description": "Vehicle is hired/rented from a third party (not company-owned).",
		},
		{
			"fieldname": "safari_hire_item",
			"label": "Hire Item",
			"fieldtype": "Link",
			"options": "Item",
			"read_only": 1,
			"no_copy": 1,
			"insert_after": "vehicle_value",
		},
	],
	"Item": [
		{
			"fieldname": "safari_vehicle",
			"label": "Vehicle",
			"fieldtype": "Link",
			"options": "Vehicle",
			"read_only": 1,
			"no_copy": 1,
			"insert_after": "item_group",
		},
	],
	# Link sales / payment documents back to the booking they settle.
	"Sales Invoice": [
		{
			"fieldname": "safari_booking",
			"label": "Safari Booking",
			"fieldtype": "Link",
			"options": "Safari Booking",
			"insert_after": "project",
		},
	],
	"Payment Entry": [
		{
			"fieldname": "safari_booking",
			"label": "Safari Booking",
			"fieldtype": "Link",
			"options": "Safari Booking",
			"insert_after": "project",
		},
	],
}

# Records that existed in earlier versions and should be removed on upgrade.
OBSOLETE_RECORDS = [
	("Number Card", "Safari Clients"),
	# Analytics charts removed from the workspace.
	("Dashboard Chart", "Safari Bookings by Status"),
	("Dashboard Chart", "Safari Bookings by Package"),
	("Dashboard Chart", "Booking Revenue Trend"),
	("Dashboard Chart", "Bookings Over Time"),
	("Dashboard Chart", "Workshop Job Cards by Status"),
	("Dashboard Chart", "Operations by Dispatch Status"),
]


def after_install():
	setup_workspace_resources()


def after_migrate():
	setup_workspace_resources()


def setup_workspace_resources():
	"""Create/refresh all workspace data dependencies (custom fields, cards, charts)."""
	remove_obsolete_records()
	create_app_custom_fields()

	from sunny_safaris.overrides.vehicle import ensure_item_group

	ensure_item_group()

	from sunny_safaris.overrides.safari_billing import ensure_safari_package_item

	ensure_safari_package_item()

	create_number_cards()

	from sunny_safaris.overrides.safari_summary import recompute_all_customers

	recompute_all_customers()

	# The number cards / charts above must exist before the workspace tiles can
	# resolve them, so force the workspace + sidebar definitions last.
	resync_workspaces()


def create_app_custom_fields():
	"""Add the app's custom fields to standard doctypes (Customer, Vehicle, Item)."""
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	create_custom_fields(APP_CUSTOM_FIELDS, ignore_validate=True)


def remove_obsolete_records():
	"""Delete records shipped by earlier versions of the app."""
	for doctype, name in OBSOLETE_RECORDS:
		frappe.delete_doc_if_exists(doctype, name)
	frappe.db.commit()


# (app, *relative path parts) for each app-owned record file that should always
# mirror the repo, regardless of the modified-timestamp skip in import_file.
WORKSPACE_FILES = [
	("sunny_safaris", "sunny_safaris", "workspace", "sunny_safaris", "sunny_safaris.json"),
	("sunny_safaris", "workspace_sidebar", "sunny_safaris.json"),
	("sunny_safaris", "desktop_icon", "sunny_safaris.json"),
]


def resync_workspaces():
	"""Force-reimport the workspace, sidebar and desktop icon from app files.

	Frappe's import_file skips non-DocType records when the database `modified`
	timestamp is newer than the file's (e.g. after a UI edit on Frappe Cloud, or
	on a redeploy with an unchanged timestamp). Forcing the import makes the
	app's shipped definition the source of truth on every migrate.
	"""
	import os

	from frappe.modules.import_file import import_file_by_path

	for app, *parts in WORKSPACE_FILES:
		path = frappe.get_app_path(app, *parts)
		if not os.path.exists(path):
			continue
		try:
			import_file_by_path(path, force=True)
		except Exception:
			frappe.log_error(title="Sunny Safaris: workspace resync failed", message=frappe.get_traceback())

	frappe.db.commit()


def create_number_cards():
	"""Idempotently create/update the workspace Number Cards."""
	for spec in NUMBER_CARDS:
		if not frappe.db.exists("DocType", spec["document_type"]):
			continue

		if frappe.db.exists("Number Card", spec["name"]):
			card = frappe.get_doc("Number Card", spec["name"])
		else:
			card = frappe.new_doc("Number Card")
			card.name = spec["name"]

		card.update(
			{
				"label": spec["label"],
				"type": "Document Type",
				"document_type": spec["document_type"],
				"function": spec["function"],
				"aggregate_function_based_on": spec.get("aggregate_function_based_on"),
				"is_public": 1,
				"show_percentage_stats": 1,
				"stats_time_interval": "Daily",
				"color": spec["color"],
				"filters_json": spec["filters_json"],
			}
		)
		card.save(ignore_permissions=True)

	frappe.db.commit()
