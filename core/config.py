import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)
PRODUCT_FILE = os.path.join(
    DATA_DIR,
    "products.csv"
)
SALE_FILE = os.path.join(
    DATA_DIR,
    "sales.csv"
)
PRODUCT_HEADERS = [
    "product_id",
    "product_name",
    "category",
    "price",
    "quantity",
    "supplier",
    "date_added"
]
SALE_HEADERS = [
    "sale_id",
    "product_id",
    "product_name",
    "quantity",
    "price",
    "total",
    "sale_date"
]
LOW_STOCK_LIMIT = 5