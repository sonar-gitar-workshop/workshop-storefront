"""Product card on the storefront home page."""

from receipt import format_money
from shop_client import get_product

FEATURED = ["WIDGET-A", "GADGET-B", "DESK-LAMP"]


def product_card(sku):
    product = get_product(sku)
    return f"{product['name']} ({product['sku']}) - {format_money(product['price_cents'])}"


def home_page():
    return "\n".join(product_card(sku) for sku in FEATURED)
