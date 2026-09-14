import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from core.config import (
    PRODUCT_FILE,
    SALE_FILE,
    PRODUCT_HEADERS,
    SALE_HEADERS
)
from core.database import (create_data_folder, initialize_file)
from ui.dashboard import Dashboard
from ui.products import Products
from ui.sales import Sales
from ui.statistics import Statistics

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        self.root.configure(bg="#F4F7FB")
        self.setup_style()
        self.create_files()
        self.create_header()
        self.create_sidebar()
        self.create_content()
        self.pages = {}
        self.initialize_pages()
        self.show_page("Dashboard")

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass
        style.configure(
            "Treeview",
            background="white",
            foreground="#1F2937",
            rowheight=32,
            fieldbackground="white",
            font=("Arial", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#E5E7EB",
            foreground="#111827",
            font=("Arial", 10, "bold")
        )
        style.map(
            "Treeview",
            background=[
                ("selected", "#DBEAFE")
            ],
            foreground=[
                ("selected", "#111827")
            ]
        )
        style.configure(
            "TButton",
            font=("Arial", 10)
        )
        style.configure(
            "TLabel",
            background="#F4F7FB",
            foreground="#1F2937"
        )
        style.configure(
            "TLabelframe",
            background="#F4F7FB"
        )
        style.configure(
            "TLabelframe.Label",
            background="#F4F7FB",
            foreground="#1F2937",
            font=("Arial", 10, "bold")
        )

    def create_files(self):
        create_data_folder()
        initialize_file(
            PRODUCT_FILE,
            PRODUCT_HEADERS
        )
        initialize_file(
            SALE_FILE,
            SALE_HEADERS
        )

    def create_header(self):
        header = tk.Frame(
            self.root,
            bg="#2563EB",
            height=80
        )
        header.pack(
            side="top",
            fill="x"
        )
        header.pack_propagate(False)
        left = tk.Frame(
            header,
            bg="#2563EB"
        )
        left.pack(
            side="left",
            padx=25
        )
        tk.Label(
            left,
            text="INVENTORY MANAGEMENT SYSTEM",
            font=("Arial", 18, "bold"),
            bg="#2563EB",
            fg="white"
        ).pack(
            anchor="w",
            pady=(12, 0)
        )
        tk.Label(
            left,
            text="Inventory Administration Dashboard",
            font=("Arial", 10),
            bg="#2563EB",
            fg="#DBEAFE"
        ).pack(anchor="w")
        tk.Label(
            header,
            text=datetime.now().strftime(
                "%d %b %Y"
            ),
            font=("Arial", 11, "bold"),
            bg="#2563EB",
            fg="white"
        ).pack(
            side="right",
            padx=25
        )

    def create_sidebar(self):
        self.sidebar = tk.Frame(
            self.root,
            bg="#111827",
            width=220
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )
        self.sidebar.pack_propagate(False)
        buttons = [
            ("Dashboard", "Dashboard"),
            ("Products", "Products"),
            ("Sales", "Sales"),
            ("Statistics", "Statistics")
        ]
        for text, page in buttons:
            button = tk.Button(
                self.sidebar,
                text="   " + text,
                command=lambda p=page:
                    self.show_page(p),
                bg="#111827",
                fg="#D1D5DB",
                activebackground="#1F2937",
                activeforeground="white",
                font=("Arial", 11),
                anchor="w",
                relief="flat",
                bd=0,
                padx=10,
                pady=12,
                cursor="hand2"
            )
            button.pack(
                fill="x",
                padx=10,
                pady=2
            )
        tk.Frame(
            self.sidebar,
            bg="#374151",
            height=1
        ).pack(
            fill="x",
            padx=15,
            pady=20
        )
        tk.Button(
            self.sidebar,
            text="   Exit",
            command=self.exit_application,
            bg="#111827",
            fg="#FCA5A5",
            activebackground="#1F2937",
            activeforeground="#FCA5A5",
            font=("Arial", 11),
            anchor="w",
            relief="flat",
            bd=0,
            padx=10,
            pady=12,
            cursor="hand2"
        ).pack(
            fill="x",
            padx=10
        )

    def create_content(self):
        self.content = tk.Frame(
            self.root,
            bg="#F4F7FB"
        )
        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

    def initialize_pages(self):
        self.pages["Dashboard"] = Dashboard(
            self.content,
            self.show_page
        )
        self.pages["Products"] = Products(self.content)
        self.pages["Sales"] = Sales(self.content)
        self.pages["Statistics"] = Statistics(self.content)

    def show_page(self, page_name):
        for page in self.pages.values():
            page.frame.pack_forget()
        page = self.pages.get(page_name)
        if page:
            page.frame.pack(
                fill="both",
                expand=True
            )
            if page_name == "Dashboard":
                page.update_cards()
            elif page_name == "Products":
                page.load_products()
            elif page_name == "Sales":
                page.load_sales()
            elif page_name == "Statistics":
                page.update_statistics()

    def exit_application(self):
        answer = messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit?"
        )
        if answer:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(
        root
    )
    root.mainloop()