# Copyright (c) 2026, harini and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class feedback(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		feedback: DF.SmallText | None
		ref: DF.Link | None
		referfield: DF.DynamicLink | None
	# end: auto-generated types

	pass
