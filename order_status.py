"""Order status page, where a customer looks up an order they already placed."""

from receipt import format_money
from shop_client import get_order


def order_status(order_id):
    order = get_order(order_id)
    return f"Order {order['id']} - {format_money(order['total_cents'])} charged"
