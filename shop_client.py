"""Client for the workshop shop's order API.

The shop lives in a separate repository, sonar-gitar-workshop/workshop-template,
and every workshop-* fork of it. This client holds no copy of that code, so a
field renamed there breaks the storefront here while both test suites stay green.
The contract this file depends on is the shop's docs/order-api.md.
"""

import os

import requests

SHOP_API_URL = os.environ.get("SHOP_API_URL", "http://localhost:5000")


def get_product(sku):
    """GET /products/<sku>. Reads `sku`, `name` and `price_cents`."""
    response = requests.get(f"{SHOP_API_URL}/products/{sku}", timeout=5)
    response.raise_for_status()
    product = response.json()
    return {
        "sku": product["sku"],
        "name": product["name"],
        "price_cents": product["price_cents"],
    }


def place_order(cart):
    """POST /orders with SKU and quantity only. Reads `id`, `items` and `total_cents`."""
    payload = {
        "items": [{"sku": sku, "quantity": quantity} for sku, quantity in cart.items()]
    }
    response = requests.post(f"{SHOP_API_URL}/orders", json=payload, timeout=5)
    response.raise_for_status()
    order = response.json()
    return {
        "id": order["id"],
        "lines": [
            (item["sku"], item["quantity"], item["unit_price_cents"])
            for item in order["items"]
        ],
        "total_cents": order["total_cents"],
    }


def get_order(order_id):
    """GET /orders/<order_id>. Same response fields as POST /orders."""
    response = requests.get(f"{SHOP_API_URL}/orders/{order_id}", timeout=5)
    response.raise_for_status()
    order = response.json()
    return {"id": order["id"], "total_cents": order["total_cents"]}
