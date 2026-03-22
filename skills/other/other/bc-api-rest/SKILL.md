---
name: bc-api-rest
description: Use BigCommerce REST APIs — V2 and V3 endpoints, authentication, rate limiting, pagination, filtering, batch operations, and error handling. Use when integrating with BigCommerce data via REST API.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce REST API Development

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.bigcommerce.com/docs/rest` for REST API overview
2. Web-search `site:developer.bigcommerce.com rest-management` for Management API reference
3. Web-search `bigcommerce api v3 rate limits pagination` for rate limit details

## API Architecture

### Two API Versions

| Version | Base URL | Notes |
|---------|----------|-------|
| V2 | `/stores/{hash}/v2/` | Legacy — orders, some customer endpoints |
| V3 | `/stores/{hash}/v3/` | Modern — most resources, JSON:API-like |

V3 is preferred for all new development. V2 is still required for some resources that haven't been migrated.

### Base URL

`https://api.bigcommerce.com/stores/{store_hash}/v3/`

The `store_hash` is found in the API Path when creating credentials.

## Authentication

### API Account Tokens

For server-to-server requests:
```
X-Auth-Token: {access_token}
Content-Type: application/json
Accept: application/json
```

### OAuth Tokens

For apps using the OAuth flow — same header format, token obtained during installation.

### Scopes

Tokens have scopes that control access:
- `store_v2_products` / `store_v2_products_read_only`
- `store_v2_orders` / `store_v2_orders_read_only`
- `store_v2_customers` / `store_v2_customers_read_only`
- `store_v2_content`, `store_v2_marketing`, `store_v2_information`
- `store_themes_manage`, `store_cart`, `store_checkout`

## Key V3 Endpoints

### Catalog

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/v3/catalog/products` | GET, POST, PUT, DELETE | Products CRUD |
| `/v3/catalog/products/{id}/variants` | GET, POST, PUT, DELETE | Product variants |
| `/v3/catalog/products/{id}/images` | GET, POST, PUT, DELETE | Product images |
| `/v3/catalog/categories` | GET, POST, PUT, DELETE | Categories |
| `/v3/catalog/brands` | GET, POST, PUT, DELETE | Brands |
| `/v3/catalog/products/channel-assignments` | GET, PUT | Channel product assignments |

### Orders (V2 — legacy but current)

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/v2/orders` | GET, POST, PUT | Orders |
| `/v2/orders/{id}/products` | GET | Order line items |
| `/v2/orders/{id}/shipments` | GET, POST, PUT | Shipments |
| `/v2/orders/{id}/shipping_addresses` | GET | Shipping addresses |

### Customers

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/v3/customers` | GET, POST, PUT, DELETE | Customers CRUD |
| `/v3/customers/addresses` | GET, POST, PUT, DELETE | Customer addresses |
| `/v3/customers/attribute-values` | GET, PUT, DELETE | Customer attributes |

### Other Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/v3/channels` | Storefronts/channels |
| `/v3/carts` | Server-side cart |
| `/v3/checkouts` | Server-side checkout |
| `/v3/payments` | Payment processing |
| `/v3/content/widgets` | Widgets |
| `/v3/themes` | Theme management |
| `/v3/hooks` | Webhooks |
| `/v3/storefront/api-token` | Storefront API tokens |

## Pagination

### V3 Pagination

Query parameters:
- `page` — page number (default 1)
- `limit` — items per page (default 50, max 250)

Response includes `meta.pagination`:
```json
{
  "data": [...],
  "meta": {
    "pagination": {
      "total": 250,
      "count": 50,
      "per_page": 50,
      "current_page": 1,
      "total_pages": 5
    }
  }
}
```

### V2 Pagination

Uses `Link` header with `rel="next"` and `rel="previous"`.

## Filtering

### V3 Query Parameters

- `id:in=1,2,3` — filter by multiple IDs
- `name:like=Widget%25` — partial name match
- `date_modified:min=2024-01-01` — date range
- `include=images,variants` — include sub-resources
- `sort=name` / `sort=-date_created` — sort ascending/descending
- `include_fields=name,price` — select specific fields
- `exclude_fields=description` — exclude specific fields

## Rate Limiting

### Default Limits

Typically 450 requests per 30-second window (varies by plan):
- Standard: 150 requests/30s
- Plus: 200 requests/30s
- Pro: 400 requests/30s
- Enterprise: 450+ requests/30s

### Headers

- `X-Rate-Limit-Requests-Left` — remaining requests in window
- `X-Rate-Limit-Time-Reset-Ms` — ms until window resets
- `X-Rate-Limit-Requests-Quota` — total requests allowed
- HTTP 429 when exceeded — retry after reset

### Best Practices for Rate Limits

- Check `X-Rate-Limit-Requests-Left` before batches
- Implement exponential backoff on 429 responses
- Use batch endpoints where available
- Cache responses that don't change frequently

## Batch Operations

Some V3 endpoints support batch operations:
- POST `/v3/catalog/products` — create multiple products (array)
- PUT `/v3/catalog/products` — update multiple products (array)
- DELETE `/v3/catalog/products?id:in=1,2,3` — delete multiple

## Error Handling

### Response Format

```json
{
  "status": 422,
  "title": "Unprocessable Entity",
  "type": "https://developer.bigcommerce.com/api-docs/getting-started/api-status-codes",
  "errors": {
    "name": "Product name is required"
  }
}
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (successful delete) |
| 400 | Bad Request (invalid parameters) |
| 401 | Unauthorized (invalid token) |
| 403 | Forbidden (insufficient scope) |
| 404 | Not Found |
| 409 | Conflict (duplicate resource) |
| 422 | Unprocessable Entity (validation error) |
| 429 | Rate Limited |
| 500 | Internal Server Error |

## Best Practices

- Use V3 for all new development — V2 only where V3 equivalent doesn't exist
- Include `Accept: application/json` and `Content-Type: application/json` headers
- Use `include` to fetch sub-resources in one request (avoid N+1)
- Use `include_fields` / `exclude_fields` to minimize response size
- Implement rate limit handling with exponential backoff
- Use batch endpoints for bulk operations
- Cache read-heavy data that changes infrequently
- Handle 429 responses gracefully — don't retry immediately

Fetch the BigCommerce REST API reference for exact endpoint paths, query parameters, request/response schemas, and current rate limits before implementing.
