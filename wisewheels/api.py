import frappe


def custom_logic(doc, method):
    frappe.msgprint("Hook executed!")


def validate_service(doc, method):
    frappe.msgprint("Validate Hook Triggered")


def service_created(doc, method):
    frappe.msgprint("Service Created Successfully")

    # Run email in background
    frappe.enqueue(
        "wisewheels.api.send_thank_you_email",
        service_name=doc.name
    )


def send_thank_you_email(service_name):

    # Fetch the Service document
    service = frappe.get_doc("services", service_name)

    # Fetch the linked Customer Details document
    customer = frappe.get_doc(
        "customer_details",
        service.customer
    )

    # Don't send if email is empty
    if not customer.email:
        return

    frappe.sendmail(
        recipients=[customer.email],
        subject="WiseWheels - Service Booking Confirmation",
        message=f"""
        Dear {customer.customer_name},

        Thank you for choosing WiseWheels.

        Your service request has been received successfully.

        Our mechanic will contact you shortly.

        Regards,
        WiseWheels Team
        """
    )
@frappe.whitelist()
def get_customer():

    doc = frappe.get_doc("customer_details", "CUSTOMER-002")

    print(doc.customer_name)

def scheduler_test():
    frappe.logger().info("Scheduler executed successfully!")


def user_login(login_manager):
    print("User Logged In")

def create_multiselect(doc, method):
    multiselect = frappe.new_doc("multiselect")
    multiselect.sname = doc.sname
    multiselect.section = doc.section

    multiselect.insert(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def get_migrate_api():

    Migrate = frappe.qb.DocType("migrate")
    Api = frappe.qb.DocType("api")

    # -------------------------
    # 1. Query Builder
    # -------------------------
    data = (
        frappe.qb.from_(Migrate)
        .join(Api)
        .on(Migrate.appliername == Api.name)
        .select(
            Migrate.name,
            Migrate.appliername,
            Migrate.grade,
            Api.kidname,
            Api.mark
        )
    ).run(as_dict=True)

    updated_doc = None

    # -------------------------
    # 2. Document API
    # -------------------------
    if data:
        doc = frappe.get_doc("migrate", data[0]["name"])
        doc.grade = "B"
        doc.save(ignore_permissions=True)
        updated_doc = doc.as_dict()

    # -------------------------
    # 3. Database API
    # -------------------------
    for row in data:
        frappe.db.set_value(
            "migrate",
            row["name"],
            "grade",
            "A+",
            update_modified=False
        )

    # -------------------------
    # 4. Return latest data
    # -------------------------
    updated_data = (
        frappe.qb.from_(Migrate)
        .join(Api)
        .on(Migrate.appliername == Api.name)
        .select(
            Migrate.name,
            Migrate.appliername,
            Migrate.grade,
            Api.kidname,
            Api.mark
        )
    ).run(as_dict=True)

    return {
        "query_builder_result": data,
        "document_api_updated_record": updated_doc,
        "database_api_updated_records": updated_data
    }