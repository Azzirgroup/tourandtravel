app_name = "sunny_safaris"
app_title = "Sunny Safaris"
app_publisher = "Rono"
app_description = "ERPNext customizations for sunny safaris Ltd."
app_email = "ronoelisha625@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "sunny_safaris",
# 		"logo": "/assets/sunny_safaris/logo.png",
# 		"title": "Sunny Safaris",
# 		"route": "/sunny_safaris",
# 		"has_permission": "sunny_safaris.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/sunny_safaris/css/safari.css"
app_include_js = "/assets/sunny_safaris/js/safari_ui.js"

# include js, css files in header of web template
# web_include_css = "/assets/sunny_safaris/css/sunny_safaris.css"
# web_include_js = "/assets/sunny_safaris/js/sunny_safaris.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sunny_safaris/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# Add "Create > Safari Booking" to CRM documents.
doctype_js = {
	"Lead": ["public/js/safari_booking_helper.js", "public/js/lead.js"],
	"Opportunity": ["public/js/safari_booking_helper.js", "public/js/opportunity.js"],
	"Quotation": ["public/js/safari_booking_helper.js", "public/js/quotation.js"],
	"Customer": ["public/js/safari_booking_helper.js", "public/js/customer.js"],
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sunny_safaris/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sunny_safaris.utils.jinja_methods",
# 	"filters": "sunny_safaris.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sunny_safaris.install.before_install"
after_install = "sunny_safaris.install.after_install"

# Migration
# ------------
after_migrate = ["sunny_safaris.install.after_migrate"]

# Uninstallation
# ------------

# before_uninstall = "sunny_safaris.uninstall.before_uninstall"
# after_uninstall = "sunny_safaris.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sunny_safaris.utils.before_app_install"
# after_app_install = "sunny_safaris.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sunny_safaris.utils.before_app_uninstall"
# after_app_uninstall = "sunny_safaris.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sunny_safaris.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

doc_events = {
	"Safari Booking": {
		"on_update": "sunny_safaris.overrides.safari_summary.update_customer_safari_summary",
		"on_submit": "sunny_safaris.overrides.safari_summary.update_customer_safari_summary",
		"on_cancel": "sunny_safaris.overrides.safari_summary.update_customer_safari_summary",
	},
	"Vehicle": {
		"after_insert": "sunny_safaris.overrides.vehicle.create_hire_item",
	},
	"Sales Invoice": {
		"on_submit": "sunny_safaris.overrides.safari_billing.update_booking_from_invoice",
		"on_cancel": "sunny_safaris.overrides.safari_billing.update_booking_from_invoice",
		"on_update_after_submit": "sunny_safaris.overrides.safari_billing.update_booking_from_invoice",
	},
	"Payment Entry": {
		"validate": "sunny_safaris.overrides.safari_billing.set_payment_safari_booking",
		"on_submit": "sunny_safaris.overrides.safari_billing.update_booking_from_payment",
		"on_cancel": "sunny_safaris.overrides.safari_billing.update_booking_from_payment",
	},
}

override_doctype_dashboards = {
	"Customer": "sunny_safaris.overrides.customer_dashboard.get_dashboard_data"
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sunny_safaris.tasks.all"
# 	],
# 	"daily": [
# 		"sunny_safaris.tasks.daily"
# 	],
# 	"hourly": [
# 		"sunny_safaris.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sunny_safaris.tasks.weekly"
# 	],
# 	"monthly": [
# 		"sunny_safaris.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "sunny_safaris.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "sunny_safaris.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sunny_safaris.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sunny_safaris.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sunny_safaris.utils.before_request"]
# after_request = ["sunny_safaris.utils.after_request"]

# Job Events
# ----------
# before_job = ["sunny_safaris.utils.before_job"]
# after_job = ["sunny_safaris.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sunny_safaris.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# Require all whitelisted methods to have type annotations
require_type_annotated_api_methods = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

