---
name: bc-api-graphql
description: Use the BigCommerce GraphQL Storefront API — queries, mutations, authentication tokens, customer impersonation, cart operations, and schema exploration. Use when building storefront features that need client-side data fetching.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce GraphQL Storefront API

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.bigcommerce.com/docs/storefront/graphql` for GraphQL overview
2. Web-search `site:developer.bigcommerce.com graphql storefront api reference` for schema reference
3. Web-search `bigcommerce graphql storefront token` for token creation

## Architecture

### What It Is

A client-side GraphQL API designed for storefront applications:
- Endpoint: `https://{store_domain}/graphql`
- Designed for browser/frontend usage (not server-to-server)
- Fetch exactly the data you need in a single request
- Supports: products, categories, cart, checkout, customer, site settings, content

### When to Use

- **Stencil themes** — client-side AJAX calls for dynamic content
- **Headless storefronts** — Catalyst/Next.js primary data source
- **Single-page applications** — React, Vue, Angular storefronts
- **Progressive enhancement** — add dynamic features to server-rendered pages

### GraphQL vs REST

| Feature | GraphQL Storefront | REST API |
|---------|-------------------|----------|
| Audience | Frontend/browser | Backend/server |
| Auth | Storefront token | API account token |
| Data shape | Client-defined | Server-defined |
| Rate limits | Complexity-based | Request count |
| Mutations | Cart, checkout, login | Full CRUD |

## Authentication

### Storefront API Token

Create via REST API:

```
POST /v3/storefront/api-token
{
  "channel_id": 1,
  "expires_at": 1893456000,
  "allowed_cors_origins": ["https://my-storefront.com"]
}
```

Returns a token to use as `Authorization: Bearer {token}` header.

### Customer Impersonation Token

For accessing customer-specific data (addresses, orders, wishlists):

```
POST /v3/storefront/api-token-customer-impersonation
{
  "channel_id": 1,
  "expires_at": 1893456000
}
```

Combine with `X-Bc-Customer-Id` header for customer-specific queries.

### Stencil Theme Context

In Stencil themes, the GraphQL token is available automatically:
- Use `{{inject 'graphQLToken' settings.storefront_api.token}}` in templates
- Or fetch from `/api/storefront/graphql-token` endpoint

## Key Queries

### Products

```graphql
query Products($first: Int, $after: String) {
  site {
    products(first: $first, after: $after) {
      edges {
        node {
          entityId
          name
          path
          prices {
            price { value currencyCode }
            salePrice { value currencyCode }
          }
          defaultImage {
            url(width: 500)
            altText
          }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
```

### Single Product

```graphql
query Product($productId: Int!) {
  site {
    product(entityId: $productId) {
      entityId
      name
      description
      prices { price { value currencyCode } }
      images { edges { node { url(width: 800) altText } } }
      productOptions { edges { node { entityId displayName } } }
      variants { edges { node { entityId sku } } }
    }
  }
}
```

### Categories

```graphql
query Categories {
  site {
    categoryTree {
      entityId
      name
      path
      children { entityId name path }
    }
  }
}
```

### Cart

```graphql
query Cart {
  site {
    cart {
      entityId
      lineItems {
        physicalItems {
          entityId
          name
          quantity
          listPrice { value currencyCode }
        }
      }
      amount { value currencyCode }
    }
  }
}
```

### Customer (Requires Impersonation Token)

```graphql
query Customer {
  customer {
    entityId
    firstName
    lastName
    email
    addresses { edges { node { address1 city } } }
  }
}
```

## Mutations

### Cart Operations

```graphql
mutation AddToCart($cartId: String!, $lineItems: [CartLineItemInput!]!) {
  cart {
    addCartLineItems(input: {
      cartEntityId: $cartId
      data: { lineItems: $lineItems }
    }) {
      cart { entityId }
    }
  }
}
```

### Create Cart

```graphql
mutation CreateCart($lineItems: [CartLineItemInput!]!) {
  cart {
    createCart(input: { lineItems: $lineItems }) {
      cart { entityId }
    }
  }
}
```

### Customer Login

```graphql
mutation Login($email: String!, $password: String!) {
  login(email: $email, password: $password) {
    result
    customer { entityId firstName }
  }
}
```

## Pagination

Uses Relay-style cursor pagination:
- `first: N` — number of items
- `after: "cursor"` — cursor from `pageInfo.endCursor`
- `pageInfo { hasNextPage endCursor }` — pagination metadata

## Complexity Limits

GraphQL queries have complexity limits instead of request-count rate limits:
- Each field has a cost
- Nested connections multiply costs
- Use `first` arguments to limit results
- Avoid deeply nested queries

## Best Practices

- Request only the fields you need — avoid `SELECT *` mentality
- Use pagination (`first` + `after`) for large collections
- Cache responses where appropriate (products, categories change infrequently)
- Use customer impersonation tokens only when customer-specific data is needed
- Set appropriate token expiration (not too long)
- Restrict CORS origins for storefront tokens
- Use fragments for reusable field sets
- Handle errors in the `errors` array of the GraphQL response

Fetch the BigCommerce GraphQL Storefront API reference for the current schema, available queries/mutations, and authentication patterns before implementing.
