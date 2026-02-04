---
name: acc-api-doc-template
description: Generates API documentation for PHP projects. Creates endpoint documentation with parameters, responses, and examples.
---

# API Documentation Template Generator

Generate comprehensive API documentation for REST endpoints.

## Document Structure

```markdown
# API Reference

## Overview
{API description and base URL}

## Authentication
{Auth methods}

## Endpoints

### {Resource}
- [GET /{resource}](#get-resource)
- [POST /{resource}](#post-resource)
- [GET /{resource}/{id}](#get-resource-id)
- [PUT /{resource}/{id}](#put-resource-id)
- [DELETE /{resource}/{id}](#delete-resource-id)

## Error Handling
{Error format and codes}

## Rate Limiting
{Rate limit info}
```

## Section Templates

### Overview Section

```markdown
## Overview

**Base URL:** `https://api.example.com/v1`

**Content Type:** `application/json`

**API Version:** v1 (2025-01-15)

### Request Format

All requests should include:
- `Content-Type: application/json` header
- Authentication header (see Authentication section)
- Request body as JSON for POST/PUT requests
```

### Authentication Section

```markdown
## Authentication

### Bearer Token

Include the token in the Authorization header:

```http
Authorization: Bearer {token}
```

### API Key

Include the API key in the X-API-Key header:

```http
X-API-Key: {api_key}
```

### Obtaining Tokens

```http
POST /auth/token
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secret"
}
```

**Response:**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_at": "2025-01-16T12:00:00Z"
}
```
```

### Endpoint Template

```markdown
## {HTTP Method} /{path}

{Brief description of what this endpoint does}

### Request

**URL:** `{HTTP Method} /api/v1/{path}`

**Authentication:** Required / Optional

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `{param}` | {type} | Yes/No | {description} |

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `{param}` | {type} | {default} | {description} |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `{field}` | {type} | Yes/No | {description} |

**Example Request:**

```http
{METHOD} /api/v1/{path}
Authorization: Bearer {token}
Content-Type: application/json

{
    "field": "value"
}
```

### Response

**Success Response:** `{status code} {status text}`

| Field | Type | Description |
|-------|------|-------------|
| `{field}` | {type} | {description} |

**Example Response:**

```json
{
    "id": "123",
    "field": "value",
    "created_at": "2025-01-15T10:00:00Z"
}
```

### Errors

| Status | Code | Description |
|--------|------|-------------|
| 400 | `VALIDATION_ERROR` | Invalid request body |
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 404 | `NOT_FOUND` | Resource not found |
| 422 | `UNPROCESSABLE` | Business rule violation |
```

### Error Handling Section

```markdown
## Error Handling

### Error Response Format

All errors follow this format:

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": {
            "field": ["Specific field error"]
        }
    }
}
```

### HTTP Status Codes

| Status | Meaning |
|--------|---------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created |
| 204 | No Content - Successful deletion |
| 400 | Bad Request - Invalid syntax |
| 401 | Unauthorized - Invalid credentials |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation failed |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

### Common Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Request validation failed |
| `UNAUTHORIZED` | Authentication required |
| `FORBIDDEN` | Insufficient permissions |
| `NOT_FOUND` | Resource not found |
| `CONFLICT` | Resource already exists |
| `RATE_LIMITED` | Too many requests |
```

### Rate Limiting Section

```markdown
## Rate Limiting

API requests are rate limited per API key:

| Plan | Limit | Window |
|------|-------|--------|
| Free | 100 | per hour |
| Pro | 1000 | per hour |
| Enterprise | 10000 | per hour |

### Rate Limit Headers

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests allowed |
| `X-RateLimit-Remaining` | Requests remaining |
| `X-RateLimit-Reset` | Unix timestamp when limit resets |

### Rate Limit Response

When rate limited, you'll receive:

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705320000

{
    "error": {
        "code": "RATE_LIMITED",
        "message": "Rate limit exceeded. Retry after 60 seconds."
    }
}
```
```

## Complete Endpoint Example

```markdown
## POST /orders

Create a new order for the authenticated user.

### Request

**URL:** `POST /api/v1/orders`

**Authentication:** Required

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `items` | array | Yes | Order items |
| `items[].product_id` | string | Yes | Product UUID |
| `items[].quantity` | integer | Yes | Quantity (1-100) |
| `shipping_address` | object | Yes | Delivery address |
| `shipping_address.street` | string | Yes | Street address |
| `shipping_address.city` | string | Yes | City name |
| `shipping_address.postal_code` | string | Yes | Postal/ZIP code |
| `shipping_address.country` | string | Yes | ISO 3166-1 alpha-2 |
| `coupon_code` | string | No | Discount code |

**Example Request:**

```http
POST /api/v1/orders
Authorization: Bearer eyJhbGci...
Content-Type: application/json

{
    "items": [
        {
            "product_id": "550e8400-e29b-41d4-a716-446655440000",
            "quantity": 2
        }
    ],
    "shipping_address": {
        "street": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "country": "US"
    },
    "coupon_code": "SAVE10"
}
```

### Response

**Success Response:** `201 Created`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Order UUID |
| `status` | string | Order status |
| `items` | array | Order items with prices |
| `subtotal` | object | Subtotal amount |
| `discount` | object | Discount amount |
| `total` | object | Total amount |
| `created_at` | string | ISO 8601 timestamp |

**Example Response:**

```json
{
    "id": "ord_123456",
    "status": "pending",
    "items": [
        {
            "product_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Widget Pro",
            "quantity": 2,
            "unit_price": {"amount": 2999, "currency": "USD"},
            "total": {"amount": 5998, "currency": "USD"}
        }
    ],
    "subtotal": {"amount": 5998, "currency": "USD"},
    "discount": {"amount": 600, "currency": "USD"},
    "total": {"amount": 5398, "currency": "USD"},
    "shipping_address": {
        "street": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "country": "US"
    },
    "created_at": "2025-01-15T10:30:00Z"
}
```

### Errors

| Status | Code | Description |
|--------|------|-------------|
| 400 | `INVALID_PRODUCT` | Product ID is malformed |
| 404 | `PRODUCT_NOT_FOUND` | Product doesn't exist |
| 422 | `OUT_OF_STOCK` | Insufficient inventory |
| 422 | `INVALID_COUPON` | Coupon code invalid or expired |
| 422 | `MIN_ORDER_VALUE` | Order below minimum value |
```

## Generation Instructions

When generating API documentation:

1. **Identify** all endpoints from routes or actions
2. **Document** request parameters (path, query, body)
3. **Document** response fields with types
4. **Provide** realistic example requests/responses
5. **List** all possible error responses
6. **Include** authentication requirements
7. **Group** endpoints by resource
