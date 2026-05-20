---
name: bc-orders
description: Work with BigCommerce orders — order lifecycle, statuses, line items, shipments, refunds, order metafields, and fulfillment. Use when building order management integrations or processing orders programmatically.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Order Management

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.bigcommerce.com rest orders` for Orders API reference
2. Web-search `bigcommerce order api v2 v3` for endpoint availability
3. Web-search `bigcommerce order status list` for status definitions

## API Endpoints

### V2 Orders (Primary)

Orders are primarily managed via V2 API:

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/v2/orders` | GET, POST, PUT | Orders CRUD |
| `/v2/orders/{id}/products` | GET | Order line items |
| `/v2/orders/{id}/shipping_addresses` | GET | Shipping addresses |
| `/v2/orders/{id}/coupons` | GET | Applied coupons |
| `/v2/orders/{id}/shipments` | GET, POST, PUT, DELETE | Shipments |
| `/v2/orders/{id}/taxes` | GET | Tax details |
| `/v2/order_statuses` | GET | Available order statuses |

### V3 Order Extensions

| Endpoint | Description |
|----------|-------------|
| `/v3/orders/{id}/metafields` | Order metafields |
| `/v3/orders/{id}/payment_actions` | Payment actions (capture, void) |
| `/v3/orders/settings` | Order-level settings |
| `/v3/orders/{id}/transactions` | Payment transactions |

## Order Lifecycle

### Status Flow

```
Incomplete → Pending → Awaiting Payment → Awaiting Fulfillment
    → Partially Shipped → Shipped → Completed
    → Awaiting Pickup → Picked Up
    → Cancelled / Declined / Refunded / Disputed
```

### Standard Statuses

| ID | Status | Description |
|----|--------|-------------|
| 0 | Incomplete | Checkout not completed |
| 1 | Pending | Awaiting processing |
| 2 | Shipped | All items shipped |
| 3 | Partially Shipped | Some items shipped |
| 4 | Refunded | Fully refunded |
| 5 | Cancelled | Order cancelled |
| 6 | Declined | Payment declined |
| 7 | Awaiting Payment | Payment not yet received |
| 8 | Awaiting Pickup | Ready for customer pickup |
| 9 | Awaiting Shipment | Awaiting fulfillment |
| 10 | Completed | Order completed |
| 11 | Awaiting Fulfillment | Ready to be fulfilled |
| 12 | Manual Verification Required | Payment needs manual review |
| 13 | Disputed | Payment dispute opened |
| 14 | Partially Refunded | Partial refund issued |

### Custom Statuses

Create custom statuses via admin or API — they map to one of the standard status groups for reporting.

## Order Structure

### Order Fields

Key fields returned by `GET /v2/orders/{id}`:
- `id` — order number
- `status_id` — current status
- `status` — status label
- `subtotal_inc_tax`, `subtotal_ex_tax`
- `total_inc_tax`, `total_ex_tax`
- `discount_amount`
- `shipping_cost_inc_tax`, `shipping_cost_ex_tax`
- `items_total` — total number of items
- `payment_method` — payment provider
- `currency_code`
- `billing_address` — billing address object
- `customer_id` — associated customer
- `date_created`, `date_modified`

### Line Items

`GET /v2/orders/{id}/products` returns:
- `product_id`, `variant_id`
- `name`, `sku`, `quantity`
- `price_inc_tax`, `price_ex_tax`
- `total_inc_tax`, `total_ex_tax`
- `product_options` — selected options

## Creating Orders

### Server-Side Order Creation

`POST /v2/orders` with:
- `customer_id` or `billing_address`
- `products` array with `product_id`, `quantity`, and optionally `price_inc_tax`
- `status_id`
- `shipping_addresses` array

Useful for: POS integrations, phone orders, order imports.

## Shipments

### Creating Shipments

`POST /v2/orders/{id}/shipments`:
```json
{
  "tracking_number": "1Z999AA10123456784",
  "shipping_method": "UPS Ground",
  "shipping_provider": "ups",
  "items": [
    { "order_product_id": 15, "quantity": 1 }
  ]
}
```

### Shipment Flow

1. Create shipment with tracking info and items
2. Order status auto-updates to "Partially Shipped" or "Shipped"
3. Customer receives shipping notification email
4. Tracking info displayed in customer order history

## Refunds

### Creating Refunds

`POST /v3/orders/{id}/payment_actions/refund`:
```json
{
  "items": [
    {
      "item_type": "PRODUCT",
      "item_id": 123,
      "quantity": 1,
      "reason": "Customer requested return"
    }
  ]
}
```

### Refund Types

- **Full refund** — refund the entire order amount
- **Partial refund** — refund specific items or custom amount
- **Line-item refund** — refund specific products with quantities

## Order Metafields

Store custom data on orders (V3):
- `POST /v3/orders/{id}/metafields`
- Used for: external IDs, fulfillment notes, integration data
- `namespace` + `key` = unique per order

## Querying Orders

### Filters

- `min_id` / `max_id` — ID range
- `min_date_created` / `max_date_created` — date range
- `status_id` — filter by status
- `customer_id` — filter by customer
- `email` — filter by customer email
- `payment_method` — filter by payment provider
- `is_deleted` — include/exclude deleted orders

### Pagination

V2 uses `page` and `limit` parameters, plus `Link` headers for navigation.

## Best Practices

- Use webhooks (`store/order/created`, `store/order/statusUpdated`) for real-time order processing
- Fetch order details via API after receiving webhook (webhooks only contain the order ID)
- Handle all order statuses — don't assume a linear flow
- Use metafields for integration-specific data, not order notes
- Create shipments with tracking info for best customer experience
- Process refunds through the API for accurate financial records
- Implement idempotency — check if an order was already processed before acting

Fetch the BigCommerce Orders API reference for exact endpoint paths, request/response schemas, and status definitions before implementing.
