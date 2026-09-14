import tkinter as tk
from tkinter import ttk, messagebox
from core.inventory import Inventory
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class Statistics:
    def __init__(self, parent):
        self.inventory = Inventory()
        self.frame = tk.Frame(
            parent,
            bg="#F4F7FB"
        )
        self.total_products = tk.StringVar()
        self.total_quantity = tk.StringVar()
        self.inventory_value = tk.StringVar()
        self.low_stock = tk.StringVar()
        self.out_of_stock = tk.StringVar()
        self.total_sales = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self.frame,
            text="Inventory Statistics",
            font=("Arial", 22, "bold"),
            bg="#F4F7FB",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )
        tk.Label(
            self.frame,
            text="View inventory performance and stock summary",
            font=("Arial", 11),
            bg="#F4F7FB",
            fg="#6B7280"
        ).pack(
            anchor="w",
            padx=25
        )
        cards = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        cards.pack(
            fill="x",
            padx=25,
            pady=25
        )
        self.create_card(
            cards,
            "Total Products",
            self.total_products,
            0
        )
        self.create_card(
            cards,
            "Total Quantity",
            self.total_quantity,
            1
        )
        self.create_card(
            cards,
            "Inventory Value",
            self.inventory_value,
            2
        )
        self.create_card(
            cards,
            "Low Stock",
            self.low_stock,
            3
        )
        self.create_card(
            cards,
            "Out of Stock",
            self.out_of_stock,
            4
        )
        self.create_card(
            cards,
            "Total Sales",
            self.total_sales,
            5
        )
        button_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        button_frame.pack(
            anchor="w",
            padx=25,
            pady=10
        )
        ttk.Button(
            button_frame,
            text="Refresh Statistics",
            command=self.update_statistics
        ).pack(
            side="left",
            padx=5
        )
        ttk.Button(
            button_frame,
            text="Show Stock Chart",
            command=self.show_chart
        ).pack(
            side="left",
            padx=5
        )

    def create_card(
        self,
        parent,
        title,
        variable,
        column
    ):
        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid"
        )
        card.grid(
            row=0,
            column=column,
            padx=5,
            sticky="nsew"
        )
        parent.columnconfigure(
            column,
            weight=1
        )
        tk.Label(
            card,
            text=title,
            font=("Arial", 9),
            bg="white",
            fg="#6B7280"
        ).pack(
            padx=12,
            pady=(15, 4)
        )
        tk.Label(
            card,
            textvariable=variable,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            padx=12,
            pady=(0, 15)
        )

    def update_statistics(self):
        statistics = (self.inventory.get_statistics())
        self.total_products.set(str(statistics["total_products"]))
        self.total_quantity.set(str(statistics["total_quantity"]))
        self.inventory_value.set(f"₹ {statistics['inventory_value']:.2f}")
        self.low_stock.set(str(statistics["low_stock"]))
        self.out_of_stock.set(str(statistics["out_of_stock"]))
        self.total_sales.set(f"₹ {statistics['total_sales']:.2f}")

    def show_chart(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror(
                "Matplotlib Not Installed",
                "Install Matplotlib using:\n\n"
                "pip install matplotlib"
            )
            return
        products = (self.inventory.get_products())
        if not products:
            messagebox.showinfo(
                "No Data",
                "There are no products to display."
            )
            return
        names = [
            product["product_name"]
            for product in products
        ]
        quantities = [
            int(product["quantity"])
            for product in products
        ]
        plt.figure(figsize=(10, 5))
        plt.bar(
            names,
            quantities
        )
        plt.title("Current Stock by Product")
        plt.xlabel("Product")
        plt.ylabel("Quantity")
        plt.xticks(
            rotation=45,
            ha="right"
        )
        plt.tight_layout()
        plt.show()