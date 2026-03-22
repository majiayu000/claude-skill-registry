---
name: woo-api
description: Build and consume WooCommerce REST API v3 endpoints — authentication, custom endpoints, extending existing resources, webhooks, and batch operations. Use when creating custom API endpoints or integrating external systems with WooCommerce.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce REST API Development

## Before writing code

**Fetch live docs**:
1. Fetch `https://woocommerce.github.io/woocommerce-rest-api-docs/` for API reference
2. Fetch `https://developer.wordpress.org/rest-api/` for WordPress REST API handbook
3. Web-search `site:developer.woocommerce.com rest api extending` for extension patterns

## REST API Architecture

### Foundation

WooCommerce REST API v3 extends the WordPress REST API:
- Base: `/wp-json/wc/v3/`
- Built on `WP_REST_Controller` pattern
- Supports JSON request/response
- Versioned — v3 is current; v1/v2 are legacy

### Built-In Endpoints

| Resource | Endpoint | Methods |
|----------|----------|---------|
| Products | `/wc/v3/products` | GET, POST, PUT, DELETE |
| Product Variations | `/wc/v3/products/{id}/variations` | GET, POST, PUT, DELETE |
| Orders | `/wc/v3/orders` | GET, POST, PUT, DELETE |
| Customers | `/wc/v3/customers` | GET, POST, PUT, DELETE |
| Coupons | `/wc/v3/coupons` | GET, POST, PUT, DELETE |
| Reports | `/wc/v3/reports` | GET |
| Settings | `/wc/v3/settings` | GET, PUT |
| Shipping Zones | `/wc/v3/shipping/zones` | GET, POST, PUT, DELETE |
| Tax Rates | `/wc/v3/taxes` | GET, POST, PUT, DELETE |
| Webhooks | `/wc/v3/webhooks` | GET, POST, PUT, DELETE |
| System Status | `/wc/v3/system_status` | GET |

## Authentication

### API Keys

WooCommerce generates consumer key/secret pairs:
- **Over HTTPS**: Pass as query params `consumer_key` & `consumer_secret`, or HTTP Basic Auth
- **Over HTTP**: OAuth 1.0a signature required
- Keys have permissions: `read`, `write`, `read_write`
- Generate at WooCommerce > Settings > Advanced > REST API

### Application Passwords (WordPress 5.6+)

WordPress-native auth — username + application password via HTTP Basic Auth. Works for all WP REST API endpoints including WooCommerce.

### Cookie/Nonce Authentication

For internal (same-site) JavaScript:
- Use `wp_create_nonce( 'wp_rest' )` — set as `X-WP-Nonce` header
- Automatically handled by `wp.apiFetch` in WordPress scripts

## Custom Endpoints

### Registering Routes

Use `rest_api_init` action to register routes:
- `register_rest_route( 'my-extension/v1', '/items', $args )`
- Define `methods`, `callback`, `permission_callback`, `args` (with `validate_callback` and `sanitize_callback`)

### Controller Pattern

Extend `WP_REST_Controller` for structured endpoints:
- `register_routes()` — define route patterns
- `get_items()` — handle collection GET
- `get_item()` — handle single GET
- `create_item()` — handle POST
- `update_item()` — handle PUT/PATCH
- `delete_item()` — handle DELETE
- `get_item_schema()` — JSON Schema for the resource
- `get_item_permissions_check()` — authorization

### Extending WooCommerce Endpoints

Add fields to existing WooCommerce resources:
- `register_rest_field( 'product', 'my_field', $args )` — add fields to product responses
- `$args` includes `get_callback`, `update_callback`, `schema`

### Filtering Responses

- `woocommerce_rest_prepare_{post_type}` — filter response before sending (e.g., `woocommerce_rest_prepare_product_object`)
- `woocommerce_rest_pre_insert_{post_type}` — filter object before saving
- `woocommerce_rest_{post_type}_query` — filter query args

## Webhooks

### Built-In Webhooks

WooCommerce webhooks fire on resource events:
- Topics: `order.created`, `order.updated`, `product.created`, `customer.created`, etc.
- Configured in WooCommerce > Settings > Advanced > Webhooks
- Delivered via HTTP POST with JSON payload and signature header

### Custom Webhook Topics

Filter `woocommerce_valid_webhook_events` and `woocommerce_webhook_topic_hooks` to add custom topics.

## Batch Operations

POST to `/wc/v3/products/batch` with `create`, `update`, `delete` arrays to perform bulk operations in a single request.

## Best Practices

- Always use `permission_callback` — never leave it empty or return `true` for non-public endpoints
- Validate and sanitize all input parameters
- Return proper HTTP status codes (200, 201, 400, 401, 403, 404)
- Use JSON Schema for endpoint argument validation
- Use `WP_REST_Response` for responses with proper status codes
- Paginate list endpoints with `per_page`, `page`, `offset`
- Include `_links` for HATEOAS-style discoverability
- Use webhooks for real-time integrations instead of polling

Fetch the WooCommerce REST API docs and WordPress REST API handbook for exact endpoint paths, parameters, and authentication details before implementing.
