# Copyright (c) 2026, Rono and contributors
# For license information, please see license.txt

from frappe import _


def get_dashboard_data(data):
	"""Add Sunny Safaris transactions to the Customer 'Connections' tab."""
	data.setdefault("transactions", [])
	data.setdefault("non_standard_fieldnames", {})

	# Safari Client is keyed by the customer name itself.
	data["non_standard_fieldnames"]["Safari Client"] = "name"

	data["transactions"].append(
		{
			"label": _("Safari"),
			"items": ["Safari Client", "Safari Booking", "Safari Operations Sheet"],
		}
	)
	return data
