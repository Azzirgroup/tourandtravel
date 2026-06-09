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
	{
		"name": "Safari Clients",
		"label": "Safari Clients",
		"document_type": "Safari Client",
		"function": "Count",
		"color": "#e53935",
		"filters_json": "[]",
	},
]

# Dashboard Charts rendered on the Sunny Safaris workspace.
DASHBOARD_CHARTS = [
	{
		"name": "Safari Bookings by Status",
		"chart_type": "Group By",
		"document_type": "Safari Booking",
		"group_by_based_on": "booking_status",
		"group_by_type": "Count",
		"type": "Donut",
		"color": "#fb8c00",
	},
	{
		"name": "Safari Bookings by Package",
		"chart_type": "Group By",
		"document_type": "Safari Booking",
		"group_by_based_on": "package_type",
		"group_by_type": "Count",
		"type": "Pie",
		"color": "#1976d2",
	},
	{
		"name": "Booking Revenue Trend",
		"chart_type": "Sum",
		"document_type": "Safari Booking",
		"based_on": "start_date",
		"value_based_on": "total_amount",
		"timeseries": 1,
		"timespan": "Last Year",
		"time_interval": "Monthly",
		"type": "Bar",
		"color": "#00897b",
	},
	{
		"name": "Bookings Over Time",
		"chart_type": "Count",
		"document_type": "Safari Booking",
		"based_on": "creation",
		"timeseries": 1,
		"timespan": "Last Year",
		"time_interval": "Monthly",
		"type": "Line",
		"color": "#7c4dff",
	},
	{
		"name": "Workshop Job Cards by Status",
		"chart_type": "Group By",
		"document_type": "Workshop Job Card",
		"group_by_based_on": "job_status",
		"group_by_type": "Count",
		"type": "Donut",
		"color": "#43a047",
	},
	{
		"name": "Operations by Dispatch Status",
		"chart_type": "Group By",
		"document_type": "Safari Operations Sheet",
		"group_by_based_on": "dispatch_status",
		"group_by_type": "Count",
		"type": "Pie",
		"color": "#e53935",
	},
]


def after_install():
	setup_workspace_resources()


def after_migrate():
	setup_workspace_resources()


def setup_workspace_resources():
	"""Create/refresh all workspace data dependencies (number cards, charts, clients)."""
	create_number_cards()
	create_dashboard_charts()

	from sunny_safaris.sunny_safaris.doctype.safari_client.safari_client import sync_safari_clients

	sync_safari_clients()

	# The number cards / charts above must exist before the workspace tiles can
	# resolve them, so force the workspace + sidebar definitions last.
	resync_workspaces()


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


def create_dashboard_charts():
	"""Idempotently create/update the workspace Dashboard Charts."""
	for spec in DASHBOARD_CHARTS:
		if not frappe.db.exists("DocType", spec["document_type"]):
			continue

		if frappe.db.exists("Dashboard Chart", spec["name"]):
			chart = frappe.get_doc("Dashboard Chart", spec["name"])
		else:
			chart = frappe.new_doc("Dashboard Chart")
			chart.name = spec["name"]

		chart.update(
			{
				"chart_name": spec["name"],
				"chart_type": spec["chart_type"],
				"document_type": spec["document_type"],
				"based_on": spec.get("based_on"),
				"value_based_on": spec.get("value_based_on"),
				"group_by_based_on": spec.get("group_by_based_on"),
				"group_by_type": spec.get("group_by_type"),
				"number_of_groups": 0,
				"timeseries": spec.get("timeseries", 0),
				"timespan": spec.get("timespan", "Last Year"),
				"time_interval": spec.get("time_interval", "Monthly"),
				"type": spec["type"],
				"color": spec.get("color"),
				"is_public": 1,
				"filters_json": "[]",
			}
		)
		chart.save(ignore_permissions=True)

	frappe.db.commit()
