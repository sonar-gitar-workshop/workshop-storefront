"""Checkout receipt shown to the customer after the shop accepts an order."""

from shop_client import place_order


def format_money(cents):
    return f"${cents / 100:,.2f}"


def checkout(cart):
    order = place_order(cart)
    lines = [f"Order {order['id']}"]
    for sku, quantity, unit_price_cents in order["lines"]:
        lines.append(f"  {sku} x {quantity}  {format_money(unit_price_cents * quantity)}")
    lines.append(f"Total charged: {format_money(order['total_cents'])}")
    return "\n".join(lines)
