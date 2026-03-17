---
name: clawpify
description: Query and manage Shopify stores via GraphQL Admin API. Use for products, orders, customers, inventory, discounts, and all Shopify data operations.
dependencies:
  - Tool: shopify_graphql (from MCP server or custom function)
---

# Shopify GraphQL Admin API

A comprehensive skill for interacting with Shopify's GraphQL Admin API. This skill enables Claude to query and manage all aspects of Shopify store data.

## When to Use This Skill

Use this skill when the user asks about:
- Products (list, search, create, update, delete)
- Orders (view, cancel, fulfill)
- Customers (list, create, update)
- Inventory (check levels, adjust quantities)
- Discounts (create codes, manage promotions)
- Any other Shopify store operations

## Critical Operations Requiring Permission

IMPORTANT: Before executing any of the following operations, you MUST ask for explicit user permission:

- Refunds: Create refunds (permanent financial transactions)
- Order Cancellations: Cancel orders (may trigger refunds)
- Gift Card Deactivation: Permanently disable gift cards
- Inventory Adjustments: Modify stock levels
- Product Deletions: Permanently remove products
- Discount Activations: Change pricing for customers

Always show what will be changed and wait for user confirmation.

## How to Use

1. Use the `shopify_graphql` tool to execute queries
2. Check for `errors` (GraphQL issues) and `userErrors` (validation issues)
3. Use pagination with `first`/`after` for large result sets
4. Format all IDs as: `gid://shopify/Resource/123`

## Available References

For detailed patterns and examples, refer to the reference documents:
- products.md - Products and variants management
- orders.md - Order operations
- customers.md - Customer management
- inventory.md - Inventory and locations
- discounts.md - Discount codes and promotions
- collections.md - Product collections
- fulfillments.md - Order fulfillment and shipping
- refunds.md - Process refunds
- draft-orders.md - Draft order creation
- gift-cards.md - Gift card management
- webhooks.md - Event subscriptions
- locations.md - Store locations
- marketing.md - Marketing activities
- markets.md - Multi-market setup
- menus.md - Navigation menus
- metafields.md - Custom data fields
- pages.md - Store pages
- blogs.md - Blog management
- files.md - File uploads
- shipping.md - Shipping configuration
- shop.md - Store information
- subscriptions.md - Subscription management
- translations.md - Content translations
- segments.md - Customer segments
- bulk-operations.md - Bulk data operations

## Quick Examples

### List Recent Orders
```graphql
query {
  orders(first: 10, sortKey: CREATED_AT, reverse: true) {
    nodes {
      id
      name
      totalPriceSet {
        shopMoney { amount currencyCode }
      }
      customer { displayName }
    }
  }
}
```

### Search Products
```graphql
query {
  products(first: 10, query: "title:*shirt* AND status:ACTIVE") {
    nodes {
      id
      title
      status
    }
  }
}
```

### Check Inventory
```graphql
query GetInventory($id: ID!) {
  inventoryItem(id: $id) {
    id
    inventoryLevels(first: 5) {
      nodes {
        quantities(names: ["available"]) {
          name
          quantity
        }
        location { name }
      }
    }
  }
}
```

## Error Handling

Always check responses:
- `errors` array = GraphQL syntax issues
- `userErrors` in mutations = validation problems

## Best Practices

1. Request only needed fields to optimize response size
2. Use pagination for lists that may grow
3. Check userErrors in all mutation responses
4. Ask permission before dangerous operations
5. Format results clearly for the user
6. Use bulk operations for large data exports/imports
7. Handle rate limits with exponential backoff
