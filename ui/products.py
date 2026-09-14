import tkinter as tk
from tkinter import ttk, messagebox
from core.inventory import Inventory
from core.validators import validate_product

class Products:
    def __init__(self, parent):
        self.inventory = Inventory()
        self.frame = tk.Frame(
            parent,
            bg="#F4F7FB"
        )
        self.editing_id = None
        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.supplier_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        title_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        title_frame.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )
        tk.Label(
            title_frame,
            text="Product Management",
            font=("Arial", 22, "bold"),
            bg="#F4F7FB",
            fg="#111827"
        ).pack(
            anchor="w"
        )
        search_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        search_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )
        tk.Label(
            search_frame,
            text="Search Product:",
            font=("Arial", 10, "bold"),
            bg="#F4F7FB"
        ).pack(
            side="left"
        )
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=35
        )
        search_entry.pack(
            side="left",
            padx=8
        )
        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_products
        ).pack(
            side="left",
            padx=3
        )
        ttk.Button(
            search_frame,
            text="Show All",
            command=self.load_products
        ).pack(
            side="left",
            padx=3
        )
        form = ttk.LabelFrame(
            self.frame,
            text="Product Details",
            padding=12
        )
        form.pack(
            fill="x",
            padx=25,
            pady=10
        )
        ttk.Label(
            form,
            text="Product Name"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=6,
            sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.name_var,
            width=23
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=6
        )
        ttk.Label(
            form,
            text="Category"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=6,
            sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.category_var,
            width=23
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=6
        )
        ttk.Label(
            form,
            text="Price"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=6,
            sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.price_var,
            width=23
        ).grid(
            row=1,
            column=1,
            padx=5,
            pady=6
        )
        ttk.Label(
            form,
            text="Quantity"
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=6,
            sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.quantity_var,
            width=23
        ).grid(
            row=1,
            column=3,
            padx=5,
            pady=6
        )
        ttk.Label(
            form,
            text="Supplier"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=6,
            sticky="w"
        )
        ttk.Entry(
            form,
            textvariable=self.supplier_var,
            width=23
        ).grid(
            row=2,
            column=1,
            padx=5,
            pady=6
        )
        self.save_button = ttk.Button(
            form,
            text="Add Product",
            command=self.save_product
        )
        self.save_button.grid(
            row=2,
            column=2,
            padx=5,
            pady=8
        )
        button_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )
        ttk.Button(
            form,
            text="Clear",
            command=self.clear_form
        ).grid(
            row=2,
            column=3,
            padx=5,
            pady=8
        )
        ttk.Button(
            button_frame,
            text="Update Selected",
            command=self.edit_product
        ).pack(
            side="left",
            padx=4
        )
        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_product
        ).pack(
            side="left",
            padx=4
        )
        ttk.Button(
            button_frame,
            text="Refresh",
            command=self.load_products
        ).pack(
            side="right",
            padx=4
        )
        table_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )
        columns = (
            "ID",
            "Name",
            "Category",
            "Price",
            "Quantity",
            "Supplier",
            "Date Added"
        )
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        widths = {
            "ID": 70,
            "Name": 170,
            "Category": 120,
            "Price": 100,
            "Quantity": 90,
            "Supplier": 140,
            "Date Added": 170
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
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

    def load_products(self):
        products = (self.inventory.get_products())
        self.display_products(products)
        self.clear_form()

    def display_products(
        self,
        products
    ):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for product in products:
            self.tree.insert(
                "",
                "end",
                values=(
                    product["product_id"],
                    product["product_name"],
                    product["category"],
                    f"₹ {float(product['price']):.2f}",
                    product["quantity"],
                    product["supplier"],
                    product["date_added"]
                )
            )

    def search_products(self):
        keyword = (self.search_var.get().strip())
        if not keyword:
            self.load_products()
            return
        products = (self.inventory.search_products(keyword))
        self.display_products(products)

    def save_product(self):
        name = self.name_var.get()
        category = self.category_var.get()
        price = self.price_var.get()
        quantity = self.quantity_var.get()
        supplier = self.supplier_var.get()
        valid, message = validate_product(
            name,
            category,
            price,
            quantity,
            supplier
        )
        if not valid:
            messagebox.showerror(
                "Validation Error",
                message
            )
            return
        try:
            if self.editing_id is None:
                success = (
                    self.inventory.add_product(
                        name.strip(),
                        category.strip(),
                        price,
                        quantity,
                        supplier.strip()
                    )
                )
                if success:
                    messagebox.showinfo(
                        "Success",
                        "Product added successfully."
                    )
                else:
                    messagebox.showerror(
                        "Error",
                        "Product could not be added."
                    )
            else:
                success = (
                    self.inventory.update_product(
                        self.editing_id,
                        name.strip(),
                        category.strip(),
                        price,
                        quantity,
                        supplier.strip()
                    )
                )
                if success:
                    messagebox.showinfo(
                        "Success",
                        "Product updated successfully."
                    )
                else:
                    messagebox.showerror(
                        "Error",
                        "Product could not be updated."
                    )
            self.load_products()
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Something went wrong:\n{error}"
            )

    def edit_product(self):
        selected = (
            self.tree.selection()
        )
        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select a product to update."
            )
            return
        values = self.tree.item(
            selected[0],
            "values"
        )
        product_id = values[0]
        product = (
            self.inventory.find_product(
                product_id
            )
        )
        if product is None:
            messagebox.showerror(
                "Error",
                "Product not found."
            )
            return
        self.editing_id = product_id
        self.name_var.set(
            product["product_name"]
        )
        self.category_var.set(
            product["category"]
        )
        self.price_var.set(
            product["price"]
        )
        self.quantity_var.set(
            product["quantity"]
        )
        self.supplier_var.set(
            product["supplier"]
        )
        self.save_button.config(
            text="Update Product"
        )

    def delete_product(self):
        selected = (
            self.tree.selection()
        )
        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select a product to delete."
            )
            return
        values = self.tree.item(
            selected[0],
            "values"
        )
        product_id = values[0]
        product_name = values[1]
        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete:\n\n"
            f"{product_name} ({product_id})?"
        )
        if not answer:
            return
        success = (
            self.inventory.delete_product(
                product_id
            )
        )
        if success:
            messagebox.showinfo(
                "Deleted",
                "Product deleted successfully."
            )
            self.load_products()
        else:
            messagebox.showerror(
                "Error",
                "Product could not be deleted."
            )

    def clear_form(self):
        self.editing_id = None
        self.name_var.set("")
        self.category_var.set("")
        self.price_var.set("")
        self.quantity_var.set("")
        self.supplier_var.set("")
        self.save_button.config(text="Add Product")