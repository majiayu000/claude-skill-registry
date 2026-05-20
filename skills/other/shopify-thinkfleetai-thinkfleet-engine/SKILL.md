---
name: shopify
description: "Manage Shopify stores — products, orders, customers, inventory, and fulfillments via the Admin REST API."
metadata: {"thinkfleetbot":{"emoji":"🛍️","requires":{"bins":["curl","jq"],"env":["SHOPIFY_STORE_URL","SHOPIFY_ACCESS_TOKEN"]}}}
---

# Shopify

Manage products, orders, customers, and inventory via the Shopify Admin API.

## Environment Variables

- `SHOPIFY_STORE_URL` - Store URL (e.g. `https://my-store.myshopify.com`)
- `SHOPIFY_ACCESS_TOKEN` - Admin API access token

## List products

```bash
curl -s -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "$SHOPIFY_STORE_URL/admin/api/2024-01/products.json?limit=10" | jq '.products[] | {id, title, status, variants: [.variants[] | {id, price, inventory_quantity}]}'
```

## Get product by ID

```bash
curl -s -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "$SHOPIFY_STORE_URL/admin/api/2024-01/products/PRODUCT_ID.json" | jq '.product | {id, title, body_html, vendor, product_type, tags}'
```

## Create product

```bash
curl -s -X POST -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "$SHOPIFY_STORE_URL/admin/api/2024-01/products.json" \
  -d '{"product":{"title":"New Product","body_html":"<p>Description</p>","vendor":"My Store","variants":[{"price":"29.99","sku":"WIDGET-001"}]}}' | jq '.product | {id, title}'
```

## List orders

```bash
curl -s -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "$SHOPIFY_STORE_URL/admin/api/2024-01/orders.json?status=any&limit=10" | jq '.orders[] | {id, order_number, financial_status, fulfillment_status, total_price, customer: .customer.email}'
```

## List customers

```bash
curl -s -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "$SHOPIFY_STORE_URL/admin/api/2024-01/customers.json?limit=10" | jq '.customers[] | {id, email, first_name, last_name, orders_count, total_spent}'
```

## Update inventory

```bash
curl -s -X POST -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "$SHOPIFY_STORE_URL/admin/api/2024-01/inventory_levels/set.json" \
  -d '{"location_id":LOCATION_ID,"inventory_item_id":ITEM_ID,"available":100}' | jq '.'
```

## Notes

- API version `2024-01` used; update as needed.
- Rate limit: 2 requests/second for standard plans.
- Always confirm before creating/updating products or fulfilling orders.
