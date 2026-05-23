---
name: shopify-api
description: Comprehensive guide and tools for working with Shopify's Admin (REST & GraphQL) and Storefront APIs. Use this skill when the user needs to interact with Shopify data, manage resources (products, orders, customers), or build custom storefront integrations.
---

# Shopify API Skill

This skill allows you to effectively interact with Shopify's ecosystem through its various APIs.

## API Selection Guide

Choose the right API for your task:

1.  **Admin GraphQL API** (Preferred): Use for most backend operations. It's the primary API for Shopify, offering more features and efficiency than REST.
2.  **Admin REST API**: Use for simple resource management if GraphQL is too complex for the specific task or if dealing with legacy systems.
3.  **Storefront API**: Use for building custom shopping experiences (headless commerce). It is unauthenticated or uses public access tokens.

## Authentication

### Admin API (Custom Apps)

Most internal apps use a custom app access token.

-   **Header**: `X-Shopify-Access-Token: <shpat_...>`
-   **URL**: `https://{shop}.myshopify.com/admin/api/{version}/{endpoint}`

### OAuth (Public Apps)

For apps distributed on the App Store.

-   **Header**: `X-Shopify-Access-Token: <access_token>`
-   **Flow**: Requires an OAuth exchange to get the offline/online token.

## 1. Admin GraphQL API

### Endpoint
`POST https://{shop}.myshopify.com/admin/api/{version}/graphql.json`

### Common Patterns

#### Querying Products
```graphql
query getProducts($first: Int!) {
  products(first: $first) {
    edges {
      node {
        id
        title
        handle
      }
      cursor
    }
    pageInfo {
      hasNextPage
    }
  }
}
```

#### Mutation (Update Product)
```graphql
mutation productUpdate($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}
```

#### Pagination
GraphQL uses cursor-based pagination. Always request `pageInfo { hasNextPage }` and the `cursor` of the last edge to fetch the next page using the `after` argument.

## 2. Admin REST API

### Endpoint
`https://{shop}.myshopify.com/admin/api/{version}/{resource}.json`

### Pagination
REST API uses link headers for pagination. Do not use `page` parameter for most resources; use `page_info`.

**Example Request:**
`GET /admin/api/2025-10/products.json?limit=50`

**Response Header:**
`Link: <...page_info=...>; rel="next", <...>; rel="previous"`

## 3. Storefront API

### Endpoint
`POST https://{shop}.myshopify.com/api/{version}/graphql.json`

### Authentication
-   **Header**: `X-Shopify-Storefront-Access-Token: <public_token>`

### Example Query
```graphql
query {
  shop {
    name
  }
  products(first: 5) {
    edges {
      node {
        title
        priceRange {
          minVariantPrice {
            amount
            currencyCode
          }
        }
      }
    }
  }
}
```

## Rate Limits

Shopify APIs use a leaky bucket algorithm.
-   **REST**: 40 requests/bucket, refilled at 2/sec (Standard).
-   **GraphQL**: Cost-based. 1000 cost points/bucket, refill rate varies (50/sec standard).

**Handling**: Check `X-Shopify-Shop-Api-Call-Limit` header (REST) or `extensions.cost` (GraphQL). Implement exponential backoff for `429 Too Many Requests`.
