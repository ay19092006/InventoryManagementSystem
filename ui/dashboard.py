import tkinter as tk
from tkinter import ttk
from core.inventory import Inventory

class Dashboard:
    def __init__(
        self,
        parent,
        show_page
    ):
        self.parent = parent
        self.show_page = show_page
        self.inventory = Inventory()
        self.frame = tk.Frame(
            parent,
            bg="#F4F7FB"
        )
        self.total_products = tk.StringVar()
        self.total_quantity = tk.StringVar()
        self.inventory_value = tk.StringVar()
        self.low_stock = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        title_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        title_frame.pack(
            fill="x",
            padx=25,
            pady=(25, 10)
        )
        tk.Label(
            title_frame,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            bg="#F4F7FB",
            fg="#111827"
        ).pack(
            anchor="w"
        )
        tk.Label(
            title_frame,
            text="Overview of your inventory",
            font=("Arial", 11),
            bg="#F4F7FB",
            fg="#6B7280"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )
        cards_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        cards_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )
        self.create_card(
            cards_frame,
            "Total Products",
            self.total_products,
            0
        )
        self.create_card(
            cards_frame,
            "Total Stock",
            self.total_quantity,
            1
        )
        self.create_card(
            cards_frame,
            "Inventory Value",
            self.inventory_value,
            2
        )
        self.create_card(
            cards_frame,
            "Low Stock",
            self.low_stock,
            3
        )
        action_frame = tk.Frame(
            self.frame,
            bg="#F4F7FB"
        )
        action_frame.pack(
            padx=25,
            pady=20,
            anchor="w"
        )
        ttk.Button(
            action_frame,
            text="Products",
            command=lambda:
                self.show_page("Products")
        ).pack(
            side="left",
            padx=(0, 10)
        )
        ttk.Button(
            action_frame,
            text="Sales",
            command=lambda:
                self.show_page("Sales")
        ).pack(
            side="left",
            padx=10
        )
        ttk.Button(
            action_frame,
            text="Statistics",
            command=lambda:
                self.show_page("Statistics")
        ).pack(
            side="left",
            padx=10
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
            padx=8,
            sticky="nsew"
        )
        parent.columnconfigure(
            column,
            weight=1
        )
        tk.Label(
            card,
            text=title,
            font=("Arial", 10),
            bg="white",
            fg="#6B7280"
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 5)
        )
        tk.Label(
            card,
            textvariable=variable,
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 18)
        )

    def update_cards(self):
        statistics = (
            self.inventory.get_statistics()
        )
        self.total_products.set(
            str(
                statistics["total_products"]
            )
        )
        self.total_quantity.set(
            str(
                statistics["total_quantity"]
            )
        )
        self.inventory_value.set(
            f"₹ {statistics['inventory_value']:.2f}"
        )
        self.low_stock.set(
            str(
                statistics["low_stock"]
            )
        )