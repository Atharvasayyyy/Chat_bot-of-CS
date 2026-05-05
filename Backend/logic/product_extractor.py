# logic/product_extractor.py

import re

def extract_product(user_input, orders_text):
    if not orders_text:
        return None

    text = user_input.lower()

    # 🔥 Extract product names using regex
    products = re.findall(r'Product:\s*(.+)', orders_text)

    products = [p.strip().lower() for p in products]

    # Match full product
    for product in products:
        if product in text:
            return product

    # Partial match
    for product in products:
        for word in product.split():
            if word in text:
                return product

    return None