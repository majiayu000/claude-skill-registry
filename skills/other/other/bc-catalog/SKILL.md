---
name: bc-catalog
description: Work with BigCommerce catalog — products, variants, options, modifiers, categories, brands, metafields, images, and bulk operations. Use when managing product data programmatically or building catalog integrations.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Catalog Management

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.bigcommerce.com/docs/rest-catalog` for Catalog API reference
2. Web-search `site:developer.bigcommerce.com catalog products variants options` for product data model
3. Web-search `bigcommerce product options vs modifiers` for variant architecture

## Product Data Model

### Product Hierarchy

```
Product
├── Options (define variant axes — e.g., Color, Size)
│   └── Option Values (Red, Blue, Small, Large)
├── Variants (specific combinations — Red/Small, Blue/Large)
│   ├── SKU, Price, Weight, Image
│   └── Inventory per variant
├── Modifiers (non-variant options — e.g., Engraving Text)
│   └── Modifier Values
├── Images (gallery images)
├── Videos
├── Custom Fields (key-value pairs shown on product page)
├── Metafields (hidden structured data for integrations)
└── Reviews
```

### Products

Core fields:
- `name`, `type`, `sku`, `description`
- `price`, `sale_price`, `retail_price`, `cost_price`
- `weight`, `width`, `height`, `depth`
- `is_visible`, `availability`, `condition`
- `categories` — array of category IDs
- `brand_id` — associated brand

Product types: `physical`, `digital`

### Options vs Modifiers

| Feature | Options | Modifiers |
|---------|---------|-----------|
| Creates variants | Yes | No |
| Affects SKU | Yes | No |
| Affects inventory | Yes | No |
| Example | Color, Size | Gift wrapping, Engraving text |
| API path | `/products/{id}/options` | `/products/{id}/modifiers` |

### Variants

Each unique combination of option values creates a variant:
- Own `sku`, `price`, `weight`, `image_url`
- Own `inventory_level` and `inventory_warning_level`
- Identified by `id` and array of `option_values`
- Up to 600 variants per product (3 options × ~200 values)

## Categories

### Hierarchy

Categories are tree-structured:
- `parent_id` — 0 for top-level, otherwise parent category ID
- `sort_order` — display order
- `is_visible` — visibility on storefront
- Can nest multiple levels deep

### Category Assignment

Products belong to one or more categories:
- Set via `categories` array on product
- A product can be in multiple categories
- Channel assignments can further control visibility per storefront

## Brands

Simple flat taxonomy:
- `name`, `page_title`, `meta_keywords`, `meta_description`
- `image_url` — brand logo
- Assigned to products via `brand_id`

## Metafields

### What They Are

Key-value data storage for products, categories, brands, customers, and orders:
- **Not visible** on the storefront by default (unlike custom fields)
- Used for integration data (external IDs, sync timestamps, etc.)
- Namespaced: `app_id` + `namespace` + `key` = unique
- Permissions: `app_only`, `read`, `write`, `read_and_sf_access`

### API

- `POST /v3/catalog/products/{id}/metafields`
- Fields: `key`, `value`, `namespace`, `permission_set`, `description`
- Use `read_and_sf_access` permission to expose in GraphQL Storefront API

## Images

### Product Images

- `POST /v3/catalog/products/{id}/images` — upload or reference by URL
- Fields: `image_url` or `image_file`, `is_thumbnail`, `sort_order`, `description`
- Multiple images per product (gallery)
- One designated as thumbnail

### Variant Images

Each variant can have its own image via `image_url` field on the variant.

## Custom Fields

Visible key-value pairs displayed on the product page:
- `name` — field label
- `value` — field value
- Displayed in the "Additional Information" section
- Managed via `/v3/catalog/products/{id}/custom-fields`

## Bulk Operations

### Batch Create/Update Products

```
POST /v3/catalog/products
[
  { "name": "Product 1", "type": "physical", "price": 29.99, ... },
  { "name": "Product 2", "type": "physical", "price": 39.99, ... }
]
```

### Batch Update

```
PUT /v3/catalog/products
[
  { "id": 123, "price": 34.99 },
  { "id": 456, "price": 44.99 }
]
```

### Batch Delete

`DELETE /v3/catalog/products?id:in=123,456,789`

## Querying Products

### Filtering

- `id:in=1,2,3` — by IDs
- `name:like=Widget` — name search
- `sku=ABC-123` — exact SKU match
- `categories:in=10,20` — by category
- `brand_id=5` — by brand
- `price:min=10&price:max=100` — price range
- `availability=available` — availability filter
- `is_visible=true` — visibility filter
- `include=images,variants,custom_fields` — include sub-resources

### Pagination

`?page=1&limit=50` — default 50, max 250 per page.

## Best Practices

- Use options for variant-defining attributes (color, size) and modifiers for everything else
- Use metafields for integration data — don't pollute custom fields
- Use `include=images,variants` to fetch sub-resources in one request
- Use batch endpoints for bulk imports/updates
- Respect rate limits — batch operations count as one request per batch
- Use webhooks (`store/product/updated`, `store/product/inventory/updated`) for real-time sync
- Set appropriate `permission_set` on metafields based on who needs access

Fetch the BigCommerce Catalog API reference for exact endpoint paths, request schemas, and filter options before implementing.
