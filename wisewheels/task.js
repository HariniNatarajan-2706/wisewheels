let d = new frappe.ui.Dialog({
    title: "Create Task",
    fields: [
        {
            label: "Task Subject",
            fieldname: "task_subject",
            fieldtype: "Data",
            reqd: 1
        }
    ],
    primary_action_label: "Create Task",
    primary_action(values) {
        frappe.call({
            method: "wisewheels.api.create_task",
            args: {
                task_subject: values.task_subject
            },
            callback: function(response) {
                d.hide();

                frappe.msgprint({
                    title: __("Success"),
                    indicator: "green",
                    message: __("Task created successfully: " + response.message)
                });
            }
        });
    }
});

d.show();