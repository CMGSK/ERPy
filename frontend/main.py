import re
import tkinter as tk
from tkinter import messagebox, ttk
from sqlalchemy import func, literal

from backend.Operations import Inventory, Business_operations
from backend.Declarations import Db_class_declarations as DB


class ERP:

    def __init__(self, root):
        self.root = root
        self.root.title("Company Name")

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill='both', expand=True)

        self.add_inventory_tab()
        self.add_sale_tab()
        self.add_user_tab()

    def add_inventory_tab(self):
        inventory_frame = ttk.Frame(self.tabs)
        self.tabs.add(inventory_frame, text="Inventory management")

        tk.Label(inventory_frame, text="Add Item:").pack()
        tk.Label(inventory_frame, text="Name:").pack()
        self.item_name_input = tk.Entry(inventory_frame)
        self.item_name_input.pack()
        tk.Label(inventory_frame, text="Stock:").pack()
        self.item_amount_input = tk.Entry(inventory_frame)
        self.item_amount_input.pack()
        tk.Label(inventory_frame, text="Price/U:").pack()
        self.item_price_input = tk.Entry(inventory_frame)
        self.item_price_input.pack()

        tk.Button(inventory_frame, text="Add New", command=self.add_item).pack()

    def add_sales_tab(self):
        sales_frame = ttk.Frame(self.tabs)
        self.tabs.add(sales_frame, text="Sales management")

        self.arr_items = []
        self.n_items_sale = 1

        tk.Label(sales_frame, text="New sale:").pack()

        # TODO: Add the customer

        for i in range(self.n_items_sale):
            tk.Label(sales_frame, text="Item:").grid(row=0, column=0, padx=5, pady=5)
            self.selector = ttk.Combobox(sales_frame, state="readonly")
            self.selector.grid(row=0, column=1, padx=5, pady=5)
            self.selector.bind("<<ComboboxSelected>>", self.display_selected)

            self.selector['values'] = self.load_items_with_id

            self.selected_label = tk.Label(sales_frame, text="")
            self.selected_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

            self.arr_items[i-1] = self.selected_label.cget("text")

            separator = ttk.Separator(root, orient='horizontal')
            separator.pack(fill='x', padx=10, pady=10)

        tk.Button(sales_frame, text="More items", command=self.add_item_to_sale).pack()
        tk.Button(sales_frame, text="Submit sale", command=self.add_sale).pack()


    def add_item_to_sale(self):
        self.n_items_sale += 1


    def display_selected(self):
        selected = self.selector.get()
        self.selected_label.config(text=f'Selected Item: {selected}')


    def load_items_with_id(self):
        return DB.session.query(func.array_agg(func.concat(
            literal('['),
            DB.DBItem.id, literal('] - '),
            DB.DBItem.name
        ))).scalar()


    def add_sale(self):

        # TODO: Add the customer and the counter

        arr_obj = []
        for i, item in enumerate(self.arr_items):
            obj = DB.session.query(DB.DBItem).filter_by(id=re.search(r'\[(.?)]', item).group(1)).first()
            arr_obj[i] = obj

        sale = Business_operations.process_sale(DB.session, "customer", arr_obj)
        for obj in arr_obj:
            detail = DB.DBSaleDetail(sale_id=sale.id, item_id=obj.id, amount=1)
            DB.session.add(detail)
            DB.session.commit()


    def add_item(self):
        item_name = self.item_name_input.get()
        item_amount = int(self.item_amount_input.get())
        item_price = float(self.item_price_input.get())

        result = Inventory.add_item(session=DB.session, name=item_name, amount=item_amount, price=item_price)
        if result == "Success":
            messagebox.showinfo("Item added successfully",
                                f"Item added: {item_name} \n"
                                f"{item_amount} stock at EUR {item_price}/Unity \n"
                                f"Total value: {item_amount * item_price}")
        else:
            messagebox.showinfo(f"Error", f'An error has occurred: \n{result}')


if __name__ == '__main__':
    root = tk.Tk()
    app = ERP(root)
    root.mainloop()