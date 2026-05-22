---
name: ship-hero
description: Expert guidance for integrating with ShipHero's GraphQL API for fulfillment, inventory, orders, and returns management. Use when (1) authenticating with ShipHero API, (2) managing orders (create, update, cancel, query), (3) managing products and inventory levels, (4) creating and tracking shipments, (5) processing returns, (6) working with purchase orders, (7) setting up webhooks for real-time events, (8) implementing 3PL multi-tenant operations, or (9) optimizing GraphQL query costs and pagination.
---

# ShipHero API Integration

## API Overview

ShipHero provides a GraphQL API for managing e-commerce fulfillment operations.

**Endpoints:**
- GraphQL: `https://public-api.shiphero.com/graphql`
- Auth: `https://public-api.shiphero.com/auth/token`

## Quick Start

### Authentication

Get a JWT token (expires in 28 days):
```bash
curl -X POST https://public-api.shiphero.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{"email": "EMAIL", "password": "PASSWORD"}'
```

Use the token in all requests:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

For detailed auth patterns including token refresh: See [references/authentication.md](references/authentication.md)

### Basic Query Pattern

All queries return `request_id`, `complexity`, and `data`:
```graphql
query {
  products {
    request_id
    complexity
    data(first: 25) {
      pageInfo { hasNextPage endCursor }
      edges {
        node { id sku name }
      }
    }
  }
}
```

## Core Operations

### Orders
```graphql
# Create order
mutation {
  order_create(data: {
    order_number: "ORD-123"
    shop_name: "my-shop"
    shipping_address: { first_name: "John", last_name: "Doe", address1: "123 Main St", city: "NYC", state: "NY", zip: "10001", country: "US" }
    line_items: [{ sku: "SKU-001", quantity: 1, price: "29.99", product_name: "Widget" }]
  }) {
    order { id order_number }
  }
}
```

### Inventory
```graphql
# Add inventory
mutation {
  inventory_add(data: {
    sku: "SKU-001"
    warehouse_id: "WAREHOUSE_UUID"
    quantity: 50
    reason: "Restocking"
  }) {
    warehouse_product { on_hand }
  }
}
```

For complete operations: See [references/graphql-operations.md](references/graphql-operations.md)

## Rate Limits & Query Optimization

**Credits:**
- Starting: 4,004 credits
- Restore rate: 60 credits/second
- Max operation cost: 4,004 credits
- Hard limit: 7,000 requests per 5 minutes

**Optimization tips:**
1. Always specify `first` or `last` parameter (default 100 is expensive)
2. Use `analyze: true` to preview query cost before executing
3. Request only needed fields
4. Use filters (`created_at_min`, `updated_at_min`) to narrow results

```graphql
# Preview query cost
query {
  orders(analyze: true) {
    complexity  # Returns estimated cost without executing
  }
}
```

## Webhooks

Register webhooks for real-time events:
```graphql
mutation {
  webhook_create(data: {
    name: "Shipment Update"  # Must match exactly
    url: "https://your-endpoint.com/webhook"
    shop_name: "api"
  }) {
    webhook { shared_signature_secret }  # Save this!
  }
}
```

**Available webhooks:** Inventory Update, Inventory Change, Shipment Update, Order Canceled, Order Packed Out, Return Update, PO Update, and more.

For full webhook reference: See [references/webhooks.md](references/webhooks.md)

## 3PL Operations

For 3PL accounts managing multiple customers:

**Option 1:** Use customer's credentials directly

**Option 2:** Add `customer_account_id` to requests:
```graphql
query {
  orders(customer_account_id: "CUSTOMER_UUID") {
    data(first: 25) { ... }
  }
}
```

## Converting Legacy IDs

Convert legacy integer IDs to UUIDs:
```graphql
query {
  uuid(legacy_id: 12345, entity_type: "order") {
    uuid
  }
}
```

## Error Handling

Capture `request_id` from all responses for debugging:
```graphql
{
  orders {
    request_id  # Always include for support
    data { ... }
  }
}
```

Common error codes: 3 (Invalid Argument), 5 (Not Found), 16 (Unauthenticated)

## Python Client Example

```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(
    url="https://public-api.shiphero.com/graphql",
    headers={"Authorization": f"Bearer {token}"}
)
client = Client(transport=transport)

result = client.execute(gql("""
    query { products { data(first: 10) { edges { node { sku } } } } }
"""))
```

## Reference Files

- **[references/graphql-operations.md](references/graphql-operations.md)**: Complete query/mutation examples for orders, products, inventory, shipments, returns, purchase orders
- **[references/webhooks.md](references/webhooks.md)**: Webhook types, registration, verification, best practices
- **[references/authentication.md](references/authentication.md)**: Token management, refresh patterns, 3PL auth
