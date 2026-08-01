import frappe
from frappe.model.document import Document


class mechanic(Document):

    def before_delete(self):
        if not self.id_card_returned:
            frappe.throw("Employee record cannot be deleted until the ID card is returned.")