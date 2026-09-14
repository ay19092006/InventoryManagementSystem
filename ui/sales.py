import tkinter as tk
from tkinter import ttk, messagebox
from core.inventory import Inventory
from core.validators import validate_sale_quantity

class Sales:
    def __init__(self, parent):
        self.inventory = Inventory()
        self.frame = tk.Frame(
            parent,
            bg="#F4F7FB"
        )
        self.product_id_var = tk.StringVar()
        self.product_name_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.total_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.frame,
            text="Sales & Billing",
            font=("Arial", 22, "bold"),
            bg="#F4F7FB",
            fg="#111827"
        )
        title.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )
        tk.Label(
            self.frame,
            text="Create a sale and update inventory",
            font=("Arial", 11),
            bg="#F4F7FB",
            fg="#6B7280"
        ).pack(
            anchor="w",
            padx=25
        )
        form = ttk.LabelFrame(
            self.frame,
            text="Sale Details",
            padding=20
        )
        form.pack(
            padx=25,
            pady=20,
            anchor="nw"
        )
        ttk.Label(
            form,
            text="Product ID"
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=8,
            sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.product_id_var,
            width=28
        ).grid(
            row=0,
            column=1,
            padx=8,
            pady=8
        )
        ttk.Button(
            form,
            text="Find Product",
            command=self.find_product
        ).grid(
            row=0,
            column=2,
            padx=8,
            pady=8
        )
        ttk.Label(
            form,
            text="Product Name"
        ).grid(
            row=1,
            column=0,
            padx=8,
            pady=8,
            sticky="w"
        )
        ttk.Label(
            form,
            textvariable=self.product_name_var
        ).grid(
            row=1,
            column=1,
            padx=8,
            pady=8,
            sticky="w"
        )
        ttk.Label(
            form,
            text="Price"
        ).grid(
            row=2,
            column=0,
            padx=8,
            pady=8,
            sticky="w"
        )
        ttk.Label(
            form,
            textvariable=self.price_var
        ).grid(
            row=2,
            column=1,
            padx=8,
            pady=8,
            sticky="w"
        )
        ttk.Label(
            form,
            text="Available Stock"
        ).grid(
            row=3,
            column=0,
            padx=8,
            pady=8,
            sticky="w"
        )
        ttk.Label(
            form,
            textvariable=self.stock_var
        ).grid(
            row=3,
            column=1,
            padx=8,
            pady=8,
            sticky="w"
        )
        ttk.Label(
            form,
            text="Sale Quantity"
        ).grid(
            row=4,
            column=0,
            padx=8,
            pady=8,
            sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.quantity_var,
            width=28
        ).grid(
            row=4,
            column=1,
            padx=8,
            pady=8
        )
        ttk.Button(
            form,
            text="Calculate Total",
            command=self.calculate_total
        ).grid(
            row=5,
            column=1,
            padx=8,
            pady=15
        )
        tk.Label(
            self.frame,
            textvariable=self.total_var,
            font=("Arial", 20, "bold"),
            bg="#F4F7FB",
            fg="#2563EB"
        ).pack(
            anchor="w",
            padx=45,
            pady=10
        )
        ttk.Button(
            self.frame,
            text="Complete Sale",
            command=self.complete_sale
        ).pack(
            anchor="w",
            padx=45,
            pady=10
        )
        table_label = tk.Label(
            self.frame,
            text="Sales History",
            font=("Arial", 14, "bold"),
            bg="#F4F7FB",
            fg="#111827"
        )
        table_label.pack(
            anchor="w",
            padx=25,
            pady=(15, 5)
        )
        table_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )
        columns = (
            "Sale ID",
            "Product ID",
            "Product",
            "Quantity",
            "Price",
            "Total",
            "Date"
        )
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        widths = {
            "Sale ID": 80,
            "Product ID": 90,
            "Product": 160,
            "Quantity": 80,
            "Price": 100,
            "Total": 100,
            "Date": 160
        }
        for column in columns:
            self.tree.heading(
                column,
                text=column
            )
            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )
        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(
            side="right",
            fill="y"
        )

    def find_product(self):
        product_id = (self.product_id_var.get().strip())
        if not product_id:
            messagebox.showwarning(
                "Input Required",
                "Enter a Product ID."
            )
            return
        product = (self.inventory.find_product(product_id))
        if product is None:
            messagebox.showerror(
                "Not Found",
                "Product not found."
            )
            self.product_name_var.set("")
            self.price_var.set("")
            self.stock_var.set("")
            return
        self.product_name_var.set(product["product_name"])
        self.price_var.set(f"₹ {float(product['price']):.2f}")
        self.stock_var.set(product["quantity"])
        self.total_var.set("")

    def calculate_total(self):
        product_id = (self.product_id_var.get().strip())
        product = (self.inventory.find_product(product_id))
        if product is None:
            messagebox.showerror(
                "Error",
                "Find a valid product first."
            )
            return
        valid, message = (
            validate_sale_quantity(
                self.quantity_var.get()
            )
        )
        if not valid:
            messagebox.showerror(
                "Invalid Quantity",
                message
            )
            return
        quantity = int(self.quantity_var.get())
        stock = int(product["quantity"])
        if quantity > stock:
            messagebox.showerror(
                "Insufficient Stock",
                "Requested quantity is greater "
                "than available stock."
            )
            return
        price = float(product["price"])
        total = (price * quantity)
        self.total_var.set(f"Total Amount: ₹ {total:.2f}")

    def complete_sale(self):
        product_id = (self.product_id_var.get().strip())
        valid, message = (
            validate_sale_quantity(
                self.quantity_var.get()
            )
        )
        if not valid:
            messagebox.showerror(
                "Invalid Quantity",
                message
            )
            return
        quantity = int(
            self.quantity_var.get()
        )
        success, result = (
            self.inventory.record_sale(
                product_id,
                quantity
            )
        )
        if success:
            messagebox.showinfo(
                "Sale Completed",
                "Sale completed successfully.\n\n"
                f"Total Amount: ₹ {result:.2f}"
            )
            self.clear_sale_form()
            self.load_sales()
        else:
            messagebox.showerror(
                "Sale Failed",
                str(result)
            )

    def load_sales(self):
        sales = (self.inventory.get_sales())
        for item in self.tree.get_children():
            self.tree.delete(item)
        for sale in sales:
            self.tree.insert(
                "",
                "end",
                values=(
                    sale["sale_id"],
                    sale["product_id"],
                    sale["product_name"],
                    sale["quantity"],
                    f"₹ {float(sale['price']):.2f}",
                    f"₹ {float(sale['total']):.2f}",
                    sale["sale_date"]
                )
            )

    def clear_sale_form(self):
        self.product_id_var.set("")
        self.product_name_var.set("")
        self.price_var.set("")
        self.stock_var.set("")
        self.quantity_var.set("")
        self.total_var.set("")