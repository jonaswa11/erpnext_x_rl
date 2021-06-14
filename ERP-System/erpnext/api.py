import frappe

# get item names from Sales Order
@frappe.whitelist()
def get_salesorders_by_date(date):
    return frappe.db.sql(f"""SELECT name FROM `tabSales Order` WHERE orderdate="{date}";""", as_dict=True)

# get item code from Sales Order
@frappe.whitelist()
def get_items_of_order(order_id):
    return frappe.db.sql(f"""SELECT item_code, qty FROM `tabSales Order Item` WHERE parent="{order_id}";""", as_dict=True)

# get units in stock for each Item
@frappe.whitelist()
def get_units_in_stock(item_id):
    return frappe.db.sql(f"""SELECT unitsinstock FROM `tabItem` WHERE item_code="{item_id}";""", as_dict=True)

# name of the last Material Request
@frappe.whitelist()
def get_last_material_request_id():
    return frappe.db.sql(f"""SELECT name FROM `tabMaterial Request` ORDER BY name DESC LIMIT 1;""", as_dict=True)

# get quantities from Purchase Order
@frappe.whitelist()
def get_total_qty_by_rl_name(rl_name):
    return frappe.db.sql(f"""SELECT total_qty FROM `tabPurchase Order` WHERE rl_name="{rl_name}";""", as_dict=True)

# get item code from Stock Entries
@frappe.whitelist()
def get_stock_entry_detail():
    return frappe.db.sql(f"""SELECT item_code, qty FROM `tabStock Entry Detail`;""", as_dict=True)

