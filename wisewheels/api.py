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


def send_welcome_email(customer_name):

    customer = frappe.get_doc("customer_details", customer_name)

    frappe.sendmail(
        recipients=[customer.email],
        subject="Welcome to WiseWheels",
        message=f"""
        Hello {customer.customer_name},

        Welcome to WiseWheels!

        Your registration has been completed successfully.

        Thank you for choosing us.

        Regards,
        WiseWheels Team
        """
    )

def customer_created(doc, method):

    frappe.enqueue(
        "wisewheels.api.send_welcome_email",
        customer_name=doc.name
    )


def before_job(job):
     frappe.log_error(
        title="BEFORE JOB",
        message=f"Method: {method}\nKwargs: {kwargs}\nTransaction Type: {transaction_type}"
    )


def after_job(job, result):
    frappe.logger().info(f"AFTER JOB: {job}")

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
@frappe.whitelist()
def get_recent_todos():
    todos = frappe.get_list(
        "ToDo",
        fields=["name", "description", "owner"],
        order_by="creation desc",
        limit_page_length=5
    )

    for todo in todos:
        todo["email"] = frappe.db.get_value(
            "User",
            todo["owner"],
            "email"
        )

    current_time = frappe.utils.now()

    return {
        "timestamp": current_time,
        "records": todos
    }

@frappe.whitelist()
def create_task(task_subject):
    task = frappe.new_doc("Task")
    task.subject = task_subject
    task.save()

    return task.name