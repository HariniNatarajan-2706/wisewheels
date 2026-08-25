import frappe


def execute(filters=None):
    columns = [
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Vehicle Number",
            "fieldname": "vehicle_number",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Service Amount",
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120
        }
    ]

    data = [
        {
            "customer": "Arun",
            "vehicle_number": "TN37AB1234",
            "amount": 2500
        },
        {
            "customer": "Priya",
            "vehicle_number": "TN38CD5678",
            "amount": 1800
        },
        {
            "customer": "Rahul",
            "vehicle_number": "TN39EF9012",
            "amount": 3200
        }
    ]

    return columns, data