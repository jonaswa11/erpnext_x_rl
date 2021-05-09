import frappe

@frappe.whitelist()
def get_salesorders_by_date(date):
    return frappe.db.sql(f"""SELECT name FROM `tabSales Order` WHERE orderdate="{date}";""", as_dict=True)

@frappe.whitelist()
def get_items_of_order(order_id):
    return frappe.db.sql(f"""SELECT item_code, qty FROM `tabSales Order Item` WHERE parent="{order_id}";""", as_dict=True)