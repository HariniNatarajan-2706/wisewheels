import frappe
from frappe.model.document import Document

class demo_doc_type(Document):

    def before_cancel(self):
        frappe.msgprint("before_cancel() executed")
    def on_trash(self):
        if self.status == "Approved":
            frappe.throw("Approved records cannot be deleted.")

    def after_delete(self):
        frappe.msgprint(f"'{self.name}' has been deleted successfully.")

    def before_save(self):
        if not self.remark:
            self.remark = "Default Description"
