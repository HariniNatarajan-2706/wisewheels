import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class customer_details(Document):

    def before_cancel(self):
        if getdate(self.expiry_date) >= getdate(today()):
            frappe.throw("This voucher is still valid. It cannot be cancelled.")

    def on_cancel(self):
        self.db_set("voucher_status", "Cancelled")

    def before_rename(self, old, new, merge=False):
        if self.account_type == "premium":
            frappe.throw("Premium customers cannot be renamed.")
    def after_rename(self, old, new, merge=False):
        frappe.msgprint(f"Customer renamed successfully from '{old}' to '{new}'.")