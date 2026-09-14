def validate_product(
    product_name,
    category,
    price,
    quantity,
    supplier
):
    product_name = product_name.strip()
    category = category.strip()
    supplier = supplier.strip()
    if not product_name:
        return False, (
            "Product name is required."
        )
    if not category:
        return False, (
            "Category is required."
        )
    if not supplier:
        return False, (
            "Supplier name is required."
        )
    try:
        price_value = float(price)
        if price_value < 0:
            return False, (
                "Price cannot be negative."
            )
    except ValueError:
        return False, (
            "Price must be a valid number."
        )
    try:
        quantity_value = int(quantity)
        if quantity_value < 0:
            return False, (
                "Quantity cannot be negative."
            )
    except ValueError:
        return False, (
            "Quantity must be a whole number."
        )
    return True, ""

def validate_sale_quantity(quantity):
    try:
        quantity_value = int(quantity)
        if quantity_value <= 0:
            return False, (
                "Quantity must be greater than zero."
            )
    except ValueError:
        return False, (
            "Quantity must be a valid whole number."
        )

    return True, ""