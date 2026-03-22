---
name: bc-webhooks
description: Implement BigCommerce webhooks — event topics, webhook management, payload handling, verification, retry logic, and event-driven architecture. Use when building real-time integrations that react to store events.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Webhooks

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.bigcommerce.com/docs/integrations/webhooks` for webhooks guide
2. Web-search `site:developer.bigcommerce.com webhooks events reference` for event topics
3. Web-search `bigcommerce webhook payload format` for payload structure

## How Webhooks Work

### Event-Driven Notifications

When events occur in a BigCommerce store, HTTP POST requests are sent to your endpoint:
1. Register a webhook via the REST API (or admin)
2. BigCommerce fires the webhook when the event occurs
3. Your endpoint receives a POST with the event payload
4. Respond with 200 OK to acknowledge receipt
5. Use the event data to trigger your business logic

### Webhook Lifecycle

- Created via `POST /v3/hooks`
- Active immediately after creation
- BigCommerce retries on failure (non-2xx response)
- Deactivated after repeated failures
- Manageable via REST API (list, update, delete)

## Managing Webhooks

### Create

```
POST /v3/hooks
{
  "scope": "store/order/created",
  "destination": "https://your-app.com/webhooks/orders",
  "is_active": true,
  "headers": {
    "X-Custom-Header": "my-verification-value"
  }
}
```

### List

`GET /v3/hooks` — returns all registered webhooks.

### Update

`PUT /v3/hooks/{id}` — update destination, scope, or active status.

### Delete

`DELETE /v3/hooks/{id}` — remove a webhook.

## Event Topics

### Order Events

| Topic | When |
|-------|------|
| `store/order/created` | New order placed |
| `store/order/updated` | Order modified |
| `store/order/archived` | Order archived |
| `store/order/statusUpdated` | Order status changed |
| `store/order/message/created` | Order message added |
| `store/order/refund/created` | Refund issued |

### Product Events

| Topic | When |
|-------|------|
| `store/product/created` | New product created |
| `store/product/updated` | Product modified |
| `store/product/deleted` | Product deleted |
| `store/product/inventory/updated` | Stock level changed |
| `store/product/inventory/order/updated` | Inventory changed due to order |

### Customer Events

| Topic | When |
|-------|------|
| `store/customer/created` | New customer registered |
| `store/customer/updated` | Customer profile modified |
| `store/customer/deleted` | Customer deleted |
| `store/customer/address/created` | Address added |
| `store/customer/address/updated` | Address modified |

### Cart Events

| Topic | When |
|-------|------|
| `store/cart/created` | New cart created |
| `store/cart/updated` | Cart modified |
| `store/cart/deleted` | Cart deleted |
| `store/cart/converted` | Cart converted to order |
| `store/cart/abandoned` | Cart abandoned |
| `store/cart/lineItem/*` | Line item changes |

### Other Events

| Topic | When |
|-------|------|
| `store/shipment/created` | Shipment created |
| `store/shipment/updated` | Shipment modified |
| `store/subscriber/created` | Newsletter subscriber added |
| `store/category/created` | Category created |
| `store/category/updated` | Category modified |
| `store/sku/created` | SKU created |
| `store/sku/updated` | SKU modified |
| `store/app/uninstalled` | App uninstalled |

## Payload Format

### Standard Payload

```json
{
  "scope": "store/order/created",
  "store_id": "1234567",
  "data": {
    "type": "order",
    "id": 5678
  },
  "hash": "abc123def456...",
  "created_at": 1706140800,
  "producer": "stores/{store_hash}"
}
```

### Key Fields

- `scope` — the event topic
- `store_id` — the store's numeric ID
- `data.type` — resource type
- `data.id` — resource ID (use to fetch full details via API)
- `hash` — unique event hash for deduplication
- `created_at` — Unix timestamp

### Important: Lightweight Payloads

Webhook payloads contain **only the resource ID**, not the full resource. You must make a follow-up REST API call to fetch the complete data:

```
// Webhook says: order 5678 was created
// Fetch full order: GET /v2/orders/5678
```

## Retry Logic

### BigCommerce Retry Behavior

- Retries on non-2xx responses
- Exponential backoff between retries
- Deactivates webhook after consecutive failures (typically ~30 days of failures)
- `is_active` set to `false` when deactivated

### Your Handler Requirements

- Respond with 200 OK quickly (within a few seconds)
- Process the event asynchronously if it requires heavy computation
- Handle duplicate deliveries (use `hash` for idempotency)
- Handle out-of-order delivery (events may arrive out of sequence)

## Verification

### Custom Headers

Include custom headers in webhook registration for basic verification:
```json
{
  "headers": {
    "X-Webhook-Secret": "my-secret-value"
  }
}
```

Verify the header value in your handler to confirm the request is from BigCommerce.

## Best Practices

- Always respond with 200 OK quickly — process asynchronously
- Use the `hash` field for idempotency (deduplication)
- Implement custom header verification for security
- Fetch full resource data via API after receiving the webhook
- Handle webhook deactivation — monitor and re-register if needed
- Subscribe only to events you need — don't subscribe to everything
- Use a message queue (SQS, Redis, RabbitMQ) for reliable async processing
- Log all received webhooks for debugging

Fetch the BigCommerce webhooks documentation for the complete list of event topics, payload formats, and retry behavior before implementing.
