---
name: woo-data-stores
description: Work with WooCommerce CRUD data stores — WC_Product, WC_Order, WC_Customer, WC_Coupon data objects, custom data stores, HPOS migration, and getters/setters. Use when creating or modifying WooCommerce data objects or implementing custom data stores.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce CRUD & Data Stores

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com crud data stores` for CRUD documentation
2. Web-search `site:github.com woocommerce woocommerce HPOS` for HPOS architecture
3. Fetch `https://github.com/woocommerce/woocommerce/wiki` for architecture decisions

## CRUD Architecture

### Data Objects

WooCommerce's core entities extend `WC_Data`:
- `WC_Product` — products (and subtypes: `WC_Product_Simple`, `WC_Product_Variable`, etc.)
- `WC_Order` — orders (and `WC_Order_Refund`)
- `WC_Customer` — customer profiles
- `WC_Coupon` — discount coupons
- `WC_Shipping_Zone` — shipping zones

### WC_Data Base Class

All CRUD objects inherit from `WC_Data`:
- `$data` — array of core properties with defaults
- `$meta_data` — array of `WC_Meta_Data` objects
- `$id` — object ID
- `$object_type` — string identifier (e.g., 'product', 'order')
- `$data_store` — the `WC_Data_Store` instance handling persistence

### Getters and Setters

- `get_{prop}( $context = 'view' )` — retrieve a property
  - `'view'` context — runs `woocommerce_{object_type}_get_{prop}` filter (for display)
  - `'edit'` context — returns raw stored value (for forms/admin)
- `set_{prop}( $value )` — set a property (in memory, not persisted until `save()`)
- `save()` — persist to database (calls data store's `create()` or `update()`)
- `delete( $force_delete )` — remove from database

### Meta Data

- `get_meta( $key, $single, $context )` — get meta value
- `update_meta_data( $key, $value, $meta_id )` — set meta (in memory)
- `delete_meta_data( $key )` — mark meta for deletion
- `save_meta_data()` — persist meta changes (called automatically by `save()`)

## Data Stores

### What Data Stores Do

Data stores abstract the persistence layer. The CRUD object calls generic methods (`read`, `create`, `update`, `delete`) on its data store, which handles the actual SQL.

### Built-In Data Stores

| Object | Data Store | Storage |
|--------|-----------|---------|
| Product | `WC_Product_Data_Store_CPT` | `wp_posts` + `wp_postmeta` |
| Order (legacy) | `WC_Order_Data_Store_CPT` | `wp_posts` + `wp_postmeta` |
| Order (HPOS) | `Automattic\WooCommerce\Internal\DataStores\Orders\OrdersTableDataStore` | `wp_wc_orders` + related tables |
| Customer | `WC_Customer_Data_Store` | `wp_users` + `wp_usermeta` |
| Coupon | `WC_Coupon_Data_Store_CPT` | `wp_posts` + `wp_postmeta` |

### Custom Data Stores

You can swap data stores via the `woocommerce_{object}_data_store` filter:
1. Implement `WC_Object_Data_Store_Interface` (or extend an existing data store)
2. Implement methods: `create()`, `read()`, `update()`, `delete()`, `read_meta()`, `update_meta()`, `delete_meta()`
3. Filter: `add_filter( 'woocommerce_product_data_store', function() { return 'My_Custom_Store'; } )`

## HPOS (High-Performance Order Storage)

### What Changed

HPOS moves order data from `wp_posts`/`wp_postmeta` to dedicated tables:
- **`wp_wc_orders`** — core order fields (status, currency, total, customer_id, dates)
- **`wp_wc_orders_meta`** — order meta
- **`wp_wc_order_addresses`** — billing/shipping addresses
- **`wp_wc_order_operational_data`** — internal operational data

### Why HPOS

- Massive performance improvement for stores with many orders
- Orders no longer pollute the `wp_posts` table
- Dedicated indexes for order queries
- Cleaner separation of concerns

### Compatibility Modes

- **Sync enabled** — both posts and custom tables are written (transition period)
- **Authoritative: Custom tables** — custom tables are the source of truth
- **Authoritative: Posts** — legacy mode, posts are source of truth

### Declaring HPOS Compatibility

```php
add_action( 'before_woocommerce_init', function() {
    if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
        \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
            'custom_order_tables', __FILE__, true
        );
    }
});
```

### HPOS-Compatible Code

- **DO**: Use `$order->get_meta()`, `$order->update_meta_data()`, `$order->save()`
- **DO**: Use `wc_get_orders()` with proper args for querying
- **DON'T**: Use `get_post_meta()`, `update_post_meta()` on orders
- **DON'T**: Use `WP_Query` to query orders directly
- **DON'T**: Assume `$order->get_id()` is a `wp_posts` ID

## Querying

### wc_get_orders()

The proper way to query orders (HPOS-compatible):
- Accepts args like `status`, `customer_id`, `date_created`, `meta_key`, `meta_value`
- Returns array of `WC_Order` objects
- Under the hood, delegates to the active order data store

### wc_get_products()

Query products — delegates to `WC_Product_Query`:
- `type`, `status`, `sku`, `category`, `tag`, `price`, `meta_key`, etc.
- Returns array of `WC_Product` objects

## Best Practices

- Always use CRUD getters/setters, never access `$data` directly
- Always call `save()` after modifying an object
- Use `'edit'` context for admin forms, `'view'` context for frontend display
- Use `wc_get_orders()` / `wc_get_products()` for queries, not `WP_Query`
- Declare HPOS compatibility in every extension
- Test with HPOS authoritative mode enabled

Fetch the WooCommerce CRUD and HPOS documentation for exact method signatures, query parameters, and compatibility requirements before implementing.
