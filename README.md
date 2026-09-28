# workshop-storefront

Customer-facing storefront for the workshop shop. It shows product cards and
the checkout receipt, and calls the shop's order API for everything else.

## What it depends on

The order API lives in [sonar-gitar-workshop/workshop-template](https://github.com/sonar-gitar-workshop/workshop-template)
and every `workshop-*` fork of it, a separate repository and a separate
deployment. This repository holds no copy of that code, so a field renamed there
breaks the storefront here silently. Both test suites stay green, and customers
see a broken receipt or product card.

The whole dependency is `shop_client.py`:

| Shop endpoint | Fields the storefront reads | Used by |
|---|---|---|
| `GET /products/<sku>` | `sku`, `name`, `price_cents` | `product_page.py` product cards |
| `POST /orders` | `id`, `items[].sku`, `items[].quantity`, `items[].unit_price_cents`, `total_cents` | `receipt.py` checkout receipt |
| `GET /orders/<order_id>` | `id`, `total_cents` | `order_status.py` order lookup |

The storefront sends `sku` and `quantity` only, never a price. The contract on
the shop side is `docs/order-api.md` in the shop repository. Keep the two in
step.

## Why it is set up this way

This pair exists to exercise cross-repo analysis in the Gitar workshop. A
breaking change is invisible from inside either repository. Renaming
`total_cents` in the shop is a self-consistent commit there, passes its own
tests, and leaves the storefront's receipt reading a field that no longer
exists.

## Running it

```
pip install -r requirements.txt
SHOP_API_URL=http://localhost:5000 python -c "from product_page import home_page; print(home_page())"
pytest -v
```

The tests use a recorded copy of the shop's responses, so they pass without a
running shop.
