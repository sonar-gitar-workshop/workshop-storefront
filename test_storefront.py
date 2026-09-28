"""Tests run against a recorded copy of the shop's responses, not the live shop."""

import pytest

import shop_client
from product_page import product_card
from order_status import order_status
from receipt import checkout

RECORDED = {
    ("GET", "/products/WIDGET-A"): {
        "sku": "WIDGET-A",
        "name": "Workshop Widget",
        "price_cents": 2500,
    },
    ("POST", "/orders"): {
        "id": "1",
        "items": [{"sku": "WIDGET-A", "quantity": 2, "unit_price_cents": 2500}],
        "total_cents": 5000,
    },
    ("GET", "/orders/1"): {"id": "1", "total_cents": 5000},
}


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def raise_for_status(self):
        pass

    def json(self):
        return self.body


@pytest.fixture(autouse=True)
def recorded_shop(monkeypatch):
    def fake(method):
        def call(url, **_kwargs):
            path = url.removeprefix(shop_client.SHOP_API_URL)
            return FakeResponse(RECORDED[(method, path)])

        return call

    monkeypatch.setattr(shop_client.requests, "get", fake("GET"))
    monkeypatch.setattr(shop_client.requests, "post", fake("POST"))


def test_product_card():
    assert product_card("WIDGET-A") == "Workshop Widget (WIDGET-A) - $25.00"


def test_checkout_receipt():
    receipt = checkout({"WIDGET-A": 2})
    assert "Order 1" in receipt
    assert "Total charged: $50.00" in receipt


def test_order_status():
    assert order_status("1") == "Order 1 - $50.00 charged"
