# Cross-repo dependencies

This storefront calls the shop order API over HTTP. The API lives in
sonar-gitar-workshop/workshop-template and in every workshop-* repository in
the sonar-gitar-workshop organization, which are forks of it.

- `shop_client.py` reads `sku`, `name` and `price_cents` from `GET /products/<sku>`.
- `shop_client.py` posts `items[].sku` and `items[].quantity` to `POST /orders`
  and reads `id`, `items[].unit_price_cents` and `total_cents` back.
- `shop_client.py` reads `id` and `total_cents` from `GET /orders/<order_id>`.
- `receipt.py` prints the charged total from `total_cents`.
- `product_page.py` prints prices from `price_cents`.

A change here to any of those reads must match the order API in the shop
repositories, i.e. `app.py` and `docs/order-api.md`.
