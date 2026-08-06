import frappe

def execute():
    last_record = frappe.get_all(
        "migrate",
        order_by="creation desc",
        limit=1,
        pluck="name"
    )

    if last_record:
        frappe.delete_doc("migrate", last_record[0])