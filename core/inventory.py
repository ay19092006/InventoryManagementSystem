from datetime import datetime
from core.config import (
    PRODUCT_FILE,
    SALE_FILE,
    PRODUCT_HEADERS,
    SALE_HEADERS,
    LOW_STOCK_LIMIT
)
from core.database import (
    read_file,
    write_file,
    append_file
)

class Inventory:
    def get_products(self):
        return read_file(
            PRODUCT_FILE
        )
    
    def generate_product_id(self):
        products = self.get_products()
        if not products:
            return "P001"
        numbers = []
        for product in products:
            try:
                number = int(
                    product["product_id"][1:]
                )
                numbers.append(number)
            except:
                pass
        if not numbers:
            return "P001"
        next_number = (
            max(numbers) + 1
        )
        return f"P{next_number:03d}"

    def add_product(
        self,
        product_name,
        category,
        price,
        quantity,
        supplier
    ):
        products = self.get_products()
        product_id = (self.generate_product_id())
        product = {
            "product_id":
                product_id,
            "product_name":
                product_name,
            "category":
                category,
            "price":
                f"{float(price):.2f}",
            "quantity":
                str(int(quantity)),
            "supplier":
                supplier,
            "date_added":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
        }
        products.append(product)
        success = write_file(
            PRODUCT_FILE,
            PRODUCT_HEADERS,
            products
        )
        return success

    def update_product(
        self,
        product_id,
        product_name,
        category,
        price,
        quantity,
        supplier
    ):
        products = self.get_products()
        found = False
        for product in products:
            if (
                product["product_id"]
                == product_id
            ):
                product["product_name"] = (
                    product_name
                )
                product["category"] = (
                    category
                )
                product["price"] = (
                    f"{float(price):.2f}"
                )
                product["quantity"] = (
                    str(int(quantity))
                )
                product["supplier"] = (
                    supplier
                )
                found = True
                break
        if not found:
            return False
        return write_file(
            PRODUCT_FILE,
            PRODUCT_HEADERS,
            products
        )

    def delete_product(
        self,
        product_id
    ):
        products = self.get_products()
        original_count = len(
            products
        )
        products = [
            product
            for product in products
            if product["product_id"]
            != product_id
        ]
        if len(products) == original_count:
            return False
        return write_file(
            PRODUCT_FILE,
            PRODUCT_HEADERS,
            products
        )

    def find_product(
        self,
        product_id
    ):
        products = self.get_products()
        for product in products:
            if (
                product["product_id"]
                == product_id
            ):
                return product
        return None

    def search_products(
        self,
        keyword
    ):
        products = self.get_products()
        keyword = keyword.lower()
        results = []
        for product in products:
            if (
                keyword
                in product["product_id"].lower()
                or keyword
                in product["product_name"].lower()
                or keyword
                in product["category"].lower()
                or keyword
                in product["supplier"].lower()
            ):
                results.append(product)
        return results

    def get_sales(self):
        return read_file(SALE_FILE)

    def generate_sale_id(self):
        sales = self.get_sales()
        if not sales:
            return "S001"
        numbers = []
        for sale in sales:
            try:
                number = int(sale["sale_id"][1:])
                numbers.append(number)
            except:
                pass
        if not numbers:
            return "S001"
        next_number = (max(numbers) + 1)
        return f"S{next_number:03d}"

    def record_sale(
        self,
        product_id,
        quantity
    ):
        product = self.find_product(product_id)
        if product is None:
            return False, ("Product not found.")
        quantity = int(quantity)
        available_quantity = int(product["quantity"])
        if quantity > available_quantity:
            return False, ("Not enough stock available.")
        price = float(product["price"])
        total = (price * quantity)
        products = self.get_products()
        for item in products:
            if (
                item["product_id"]
                == product_id
            ):
                item["quantity"] = str(
                    available_quantity
                    - quantity
                )
                break
        updated = write_file(
            PRODUCT_FILE,
            PRODUCT_HEADERS,
            products
        )
        if not updated:
            return False, ("Inventory could not be updated.")
        sale = {
            "sale_id":
                self.generate_sale_id(),
            "product_id":
                product_id,
            "product_name":
                product["product_name"],
            "quantity":
                str(quantity),
            "price":
                f"{price:.2f}",
            "total":
                f"{total:.2f}",
            "sale_date":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
        }
        saved = append_file(
            SALE_FILE,
            SALE_HEADERS,
            sale
        )
        if not saved:
            return False, ("Sale could not be saved.")
        return True, total

    def get_statistics(self):
        products = self.get_products()
        sales = self.get_sales()
        total_products = len(products)
        total_quantity = 0
        inventory_value = 0
        low_stock = 0
        out_of_stock = 0
        for product in products:
            try:
                quantity = int(product["quantity"])
                price = float(product["price"])
                total_quantity += quantity
                inventory_value += (quantity * price)
                if (
                    quantity > 0
                    and quantity <= LOW_STOCK_LIMIT
                ):
                    low_stock += 1
                if quantity == 0:
                    out_of_stock += 1
            except:
                pass
        total_sales = 0
        for sale in sales:
            try:
                total_sales += float(sale["total"])
            except:
                pass
        return {
            "total_products":
                total_products,
            "total_quantity":
                total_quantity,
            "inventory_value":
                inventory_value,
            "low_stock":
                low_stock,
            "out_of_stock":
                out_of_stock,
            "total_sales":
                total_sales
        }