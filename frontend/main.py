import datetime
import re
import customtkinter
import tkinter as tk
from tkinter import messagebox, ttk
from sqlalchemy import func, literal

from backend.Operations import Inventory, Sales, Customers, Business_operations
from backend.Declarations import Db_class_declarations as DB

root = customtkinter.CTk()
root.title("Company name")
root.attributes('-type', 'dialog')
root.resizable(False, False)
root.geometry('800x600')
root.grid_columnconfigure((0), weight=1)

tab_view = customtkinter.CTkTabview(root)
tab_view.grid(row=1, padx=40, pady=40, sticky='ew')

sales_tab = tab_view.add("Sales")
clients_tab = tab_view.add("Customers")
inventory_tab = tab_view.add("Inventory")
b_sales = False
b_clients = False
b_inventory = False


def refresh():
    root.__init__()


def add_inventory():
    w_stock = re.match(r'\d+', i_stock.get())
    w_price = re.match(r'\d+|\d+\.\d.', i_price.get())
    if w_stock and w_price:
        i_warning.configure(text="")
    else:
        i_warning.configure(text_color='red')
        i_price.configure(border_color='grey')
        i_stock.configure(border_color='grey')
        if not w_price:
            i_warning.configure(text="Price must be a number")
            i_price.configure(border_color='red')
        if not w_stock:
            i_warning.configure(text=f"{i_warning.cget('text')}\nStock must be an integer")
            i_stock.configure(border_color='red')
        return

    item = i_name.get()
    stock = int(i_stock.get())
    price = float(i_price.get())

    item = Inventory.add_item(session=DB.session, name=item, amount=stock, price=price)
    if isinstance(item, DB.DBItem):
        i_warning.configure(text = "Item added successfully\n\n"
                            f"Item added: {item} \n"
                            f"{stock} stock at EUR {price}/Unity \n"
                            f"Total value: {stock * price}",
                          text_color='green')
    else:
        i_warning.configure(text=item, text_color='red')


def add_customer():
    name = c_name.get()
    idcard = c_idcard.get()
    address = c_address.get()

    customer = Customers.add_customer(session=DB.session, name=name, identity_card=idcard, address=address)
    if isinstance(customer, DB.DBCustomer):
        c_warning.configure(text = "Customer added successfully",
                            text_color='green')
    else:
        c_warning.configure(text=customer, text_color='red')


def add_sale_items():
    amount = p_amount.get()
    if not re.match(r"\d+", amount):
        s_warning.configure(text_color='red')
        s_warning.configure(text="Amount must be a number")
        return
    else:
        s_warning.configure(text="")

    item = p_name.get()
    receipt.configure(state="normal")
    curr = receipt.get("0.0", "end")
    text=f'{curr} - {item} \t\t\t\t\t(x{amount})'
    receipt.delete("0.0", "end")
    receipt.insert("0.0", text)
    receipt.configure(state="disabled")


def lessen_sale_items():
    item = p_name.get()
    curr = receipt.get("0.0", "end")
    actu = ''
    for p in curr.split('\n'):
        if item not in p and not p == '\n':
            actu = f'{actu}{p}'
    receipt.configure(state="normal")
    receipt.delete("0.0", "end")
    receipt.insert("0.0", actu)
    receipt.configure(state="disabled")


# Items TAB
inventory_tab.grid_columnconfigure(0, weight=1)
# customtkinter.CTkLabel(inventory_tab, text="Add Item:").grid(column=0, row=0)
i_switch = customtkinter.CTkSwitch(inventory_tab, text="Watch tables")
i_switch.grid(row=0, column=0, columnspan=4)
if not i_switch.get():
    i_warning = customtkinter.CTkLabel(inventory_tab, text="", text_color='red')
    i_warning.grid(row=1, column=0)

    i_name = customtkinter.CTkEntry(inventory_tab, placeholder_text="Name")
    i_name.grid(row=2, column=0)
    i_stock = customtkinter.CTkEntry(inventory_tab, placeholder_text="Initial Stock")
    i_stock.grid(row=3, column=0)
    i_price = customtkinter.CTkEntry(inventory_tab, placeholder_text="Price per unit")
    i_price.grid(row=4, column=0)

    customtkinter.CTkButton(inventory_tab, text="Add item", command=add_inventory).grid(row=5, column=0)
else:
    print('halo')




# Customers TAB
clients_tab.grid_columnconfigure(0, weight=1)
# customtkinter.CTkLabel(clients_tab, text="Add Customer:").grid(row=0, column=0)
c_switch = customtkinter.CTkSwitch(sales_tab, text="Watch tables")
c_switch.grid(row=0, column=0, columnspan=4)
c_warning = customtkinter.CTkLabel(clients_tab, text="", text_color='red')
c_warning.grid(row=1, column=0)

c_name = customtkinter.CTkEntry(clients_tab, placeholder_text="Full name")
c_name.grid(row=2, column=0)
c_idcard = customtkinter.CTkEntry(clients_tab, placeholder_text="ID Card")
c_idcard.grid(row=3, column=0)
c_address = customtkinter.CTkEntry(clients_tab, placeholder_text="Address")
c_address.grid(row=4, column=0)

customtkinter.CTkButton(clients_tab, text="Add customer", command=add_customer).grid(row=5, column=0)


# Sales TAB
sales_tab.grid_columnconfigure((0), weight=1)
# customtkinter.CTkLabel(sales_tab, text="Add Sales").grid(row=0, column=0, columnspan=4)
s_switch = customtkinter.CTkSwitch(sales_tab, text="Watch tables")
s_switch.grid(row=0, column=0, columnspan=4)

s_warning = customtkinter.CTkLabel(sales_tab, text="", text_color='red')
s_warning.grid(row=1, column=1)

# TODO: add filter
customtkinter.CTkLabel(sales_tab, text="Select the costumer:").grid(row=2, column=0, sticky='w')
# all_customers = [f'[{c.identity_card}] {c.name}' for p in Inventory.get_all_items(DB.session)]
all_customers = ['[D-481972] Larry K. Tulla',
                 '[F-987240] Miquel Hawk',
                 '[JK00393197P] Paula Perez']
customtkinter.CTkComboBox(sales_tab, values=all_customers).grid(row=3, column=0, sticky="ew", columnspan=4)

customtkinter.CTkLabel(sales_tab, text="Current sale:").grid(row=4, column=0, sticky='w', pady=(20,0))
receipt = customtkinter.CTkTextbox(sales_tab)
receipt.configure(state='disabled')
receipt.grid(row=5, column=0, sticky='ew', columnspan=4)
# TODO: add filter
customtkinter.CTkLabel(sales_tab, text="Select item to add:").grid(row=6, column=0, sticky='w')
customtkinter.CTkLabel(sales_tab, text="Select amount:").grid(row=6, column=3)
# all_products = [f'{p.name}' for p in Inventory.get_all_items(DB.session)]
all_products = ['Product example 1 - 10Ud.',
                'Product example 1',
                'Product example 2',
                'Product example 3 - 1Kg',
                'Product example 3 - 5Kg']
p_name = customtkinter.CTkComboBox(sales_tab, values=all_products)
p_name.grid(row=7, column=0, sticky="ew", columnspan=3)
p_amount = customtkinter.CTkEntry(sales_tab)
p_amount.grid(row=7, column=3, sticky='e', columnspan=1)
customtkinter.CTkButton(sales_tab, text='Add items to sale', command=add_sale_items).grid(row=8, column=1, sticky='w', pady=(20,20), padx=(30,30))
customtkinter.CTkButton(sales_tab, text='Delete item from sale', command=lessen_sale_items, fg_color='red', hover_color='dark red').grid(row=8, column=2, sticky='w', pady=(20,20), padx=(30,30))




# def add_item_to_sale(self):
#     self.n_items_sale += 1
#
#
# def display_selected(self, event):
#     selected = self.selector.get()
#     self.selected_label.config(text=f'Selected Item: {selected}')
#
#
# def load_items_with_id(self):
#     return DB.session.query(func.array_agg(func.concat(
#         literal('['),
#         DB.DBItem.id, literal('] - '),
#         DB.DBItem.name
#     ))).scalar()
#
#
# def add_sale(self):
#
#     # TODO: Add the customer and the counter
#
#     arr_obj = []
#     for i, item in enumerate(self.arr_items):
#         obj = DB.session.query(DB.DBItem).filter_by(id=re.search(r'\[(.?)]', item).group(1)).first()
#         arr_obj[i] = obj
#
#     sale = Sales.add_sale(session=DB.session, customer="TODO", total=3.3, date=datetime.date)
#     if isinstance(sale, DB.DBSale):
#         for obj in arr_obj:
#             detail = DB.DBSaleDetail(sale_id=sale.id, item_id=obj.id, amount=1)
#             DB.session.add(detail)
#             DB.session.commit()
#
#         #TODO: ...
#     else:
#         messagebox.showinfo(f"Error", f'An error has occurred: \n{sale}')
#
#
# def add_item(self):
#     item_name = self.item_name_input.get()
#     item_amount = int(self.item_amount_input.get())
#     item_price = float(self.item_price_input.get())
#
#     item = Inventory.add_item(session=DB.session, name=item_name, amount=item_amount, price=item_price)
#     if isinstance(item, DB.DBItem):
#         messagebox.showinfo("Item added successfully",
#                             f"Item added: {item_name} \n"
#                             f"{item_amount} stock at EUR {item_price}/Unity \n"
#                             f"Total value: {item_amount * item_price}")
#     else:
#         messagebox.showinfo(f"Error", f'An error has occurred: \n{item}')
#
#

root.mainloop()
