---
name: woo-catalog
description: Work with WooCommerce catalog — product types, categories, tags, attributes, product queries, search, related products, and product visibility. Use when managing products programmatically or customizing the catalog display.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Catalog & Products

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com products` for product documentation
2. Fetch `https://woocommerce.github.io/code-reference/` for class reference
3. Web-search `woocommerce custom product type implementation` for custom product types

## Product Types

### Built-In Types

| Type | Class | Description |
|------|-------|-------------|
| Simple | `WC_Product_Simple` | Single product, no options |
| Variable | `WC_Product_Variable` | Product with variations (size, color) |
| Variation | `WC_Product_Variation` | Individual variation of a variable product |
| Grouped | `WC_Product_Grouped` | Collection of related simple products |
| External/Affiliate | `WC_Product_External` | Linked to external URL |

### Virtual & Downloadable Flags

Any product can be marked:
- **Virtual** — no shipping (services, memberships)
- **Downloadable** — digital delivery (files, licenses)

### Custom Product Types

1. Extend `WC_Product` (or `WC_Product_Simple`)
2. Register the type via `woocommerce_product_type_selector` filter
3. Register the class via `woocommerce_product_class` filter or `woocommerce_product_type_{type}` class name filter

## Product Factory

`WC_Product_Factory` resolves a product ID to the correct class:
- `wc_get_product( $id )` — returns the correct `WC_Product_*` subclass
- Uses `woocommerce_product_class` filter to allow custom type resolution

## Product CRUD

### Creating Products

```php
$product = new WC_Product_Simple();
$product->set_name( 'My Product' );
$product->set_regular_price( '29.99' );
$product->set_status( 'publish' );
$product->save();
```

### Querying Products

`wc_get_products( $args )` — primary query method:
- `type` — product type(s)
- `status` — post status
- `sku` — SKU lookup
- `category` — category slug(s)
- `tag` — tag slug(s)
- `limit`, `page`, `offset` — pagination
- `orderby`, `order` — sorting
- `meta_key`, `meta_value` — meta queries
- `return` — `'objects'` (default) or `'ids'`

### WC_Product_Query

Object-oriented query builder — same as `wc_get_products()` but chainable.

## Categories & Taxonomies

### Product Categories

Taxonomy: `product_cat` (hierarchical)
- `wp_set_object_terms( $product_id, $term_ids, 'product_cat' )`
- `get_the_terms( $product_id, 'product_cat' )`
- Or CRUD: `$product->set_category_ids( [ 12, 15 ] )`

### Product Tags

Taxonomy: `product_tag` (non-hierarchical)
- `$product->set_tag_ids( [ 5, 8 ] )`

### Product Type

Taxonomy: `product_type` — internal, determines the product class.

### Custom Taxonomies

Register with `register_taxonomy()` associated with `product` post type. Set `show_in_rest => true` for block editor and API support.

## Product Visibility

### Catalog Visibility

`$product->set_catalog_visibility( $visibility )`:
- `visible` — shop and search
- `catalog` — shop only
- `search` — search only
- `hidden` — not visible (accessible via direct URL)

### Stock Status

`$product->set_stock_status( $status )`:
- `instock`, `outofstock`, `onbackorder`
- Controls visibility when "Hide out of stock" setting is enabled

## Product Images

- `$product->set_image_id( $attachment_id )` — featured image
- `$product->set_gallery_image_ids( [ $id1, $id2 ] )` — gallery

## Variable Products & Variations

### Variable Product Setup

1. Create `WC_Product_Variable`
2. Define attributes with `set_attributes()` (mark as `variation = true`)
3. Create `WC_Product_Variation` for each combination
4. Each variation has its own price, SKU, stock, image

### Variation Attributes

Each variation specifies attribute values:
- `$variation->set_attributes( [ 'pa_color' => 'red', 'pa_size' => 'large' ] )`
- Empty value = "Any" (matches all)

## Related Products & Upsells

- `$product->set_upsell_ids( $ids )` — upsell products
- `$product->set_cross_sell_ids( $ids )` — cross-sells (shown in cart)
- Related products auto-calculated from shared categories/tags (filterable via `woocommerce_related_products` filter)

## Best Practices

- Use `wc_get_product()` to load products — never `new WC_Product( $id )` directly
- Use `wc_get_products()` for queries — not `WP_Query` with `post_type => 'product'`
- Use CRUD methods for all property access
- Declare product type support: `show_if_simple`, `show_if_variable` classes on admin tabs
- Cache product data when iterating over large collections
- Use `wc_clean()` to sanitize product input data

Fetch the WooCommerce product documentation and code reference for exact method signatures, query parameters, and product type registration patterns before implementing.
