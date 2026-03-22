---
name: woo-performance
description: Optimize WooCommerce performance — object caching, transients, HPOS, database optimization, Action Scheduler, lazy loading, and query optimization. Use when improving store performance or diagnosing slowness.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Performance Optimization

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com performance` for performance guide
2. Web-search `woocommerce hpos performance benefits` for HPOS optimization details
3. Web-search `wordpress object caching best practices` for caching patterns

## HPOS (High-Performance Order Storage)

### Why It Matters

HPOS moves orders from `wp_posts`/`wp_postmeta` to dedicated tables:
- Dramatically faster order queries (custom indexes)
- Reduces `wp_posts` table bloat
- Better database performance at scale
- Required for WooCommerce's future direction

### Enabling HPOS

WooCommerce > Settings > Advanced > Features:
- Enable "Custom order tables"
- Run the migration tool to migrate existing orders
- Enable "Sync" during transition period
- Once verified, disable sync and use custom tables as authoritative

### Compatibility Requirements

Extensions must:
- Use CRUD methods (`$order->get_meta()`, `$order->set_status()`, `$order->save()`)
- NOT use `get_post_meta()` / `update_post_meta()` on orders
- NOT use `WP_Query` with `post_type => 'shop_order'`
- Declare compatibility via `FeaturesUtil::declare_compatibility()`

## Object Caching

### WordPress Object Cache

`wp_cache_get()` / `wp_cache_set()` — in-memory cache per request:
- With Redis/Memcached: persistent across requests
- Always use cache groups: `wp_cache_set( $key, $data, 'my_plugin' )`
- Set appropriate expiration
- Use `wp_cache_delete()` when data changes

### Transients

`set_transient()` / `get_transient()` — cached values with expiration:
- Stored in DB without object cache, in-memory with object cache
- Use for: API responses, computed values, rate calculations
- Always handle cache miss (regenerate data when transient expires)
- Delete transients when underlying data changes

### WooCommerce Cache Helpers

- `WC_Cache_Helper` — manages WooCommerce-specific caching
- `wc_get_transient_version( 'product' )` — cache versioning for products
- Cache invalidation on product/order changes via version bumps

## Database Optimization

### Query Optimization

- Use `wc_get_orders()` / `wc_get_products()` instead of `WP_Query`
- Limit queries: always use `limit`/`per_page` parameters
- Avoid `meta_query` on large tables — use HPOS custom columns instead
- Use `'fields' => 'ids'` when you only need IDs
- Avoid `'no_found_rows' => false` on large result sets

### Index Optimization

- Ensure custom tables have proper indexes on queried columns
- WooCommerce HPOS tables include optimized indexes by default
- For custom tables: add indexes on columns used in WHERE, JOIN, ORDER BY

### Background Processing

Move heavy operations out of the request cycle:
- **Action Scheduler** — WooCommerce's job queue
- Schedule: `as_schedule_single_action( $timestamp, 'hook_name', $args )`
- Recurring: `as_schedule_recurring_action( $timestamp, $interval, 'hook_name', $args )`
- Handles retries, failure logging, and concurrent execution

## Frontend Performance

### Asset Loading

- Conditionally load CSS/JS only on relevant pages
- Use `wp_enqueue_script` with `strategy => 'defer'` or `'async'`
- Combine/minify assets in production
- Use `wp_script_add_data( $handle, 'strategy', 'defer' )`

### Cart Fragments

AJAX cart fragment refreshing can be a bottleneck:
- Filter `woocommerce_cart_fragments` to minimize data
- Disable on pages where cart widget isn't shown
- Use `wc_cart_fragments_params` localized data

### Image Optimization

- Use WordPress responsive images (`srcset`, `sizes`)
- Enable lazy loading: `loading="lazy"` on product images
- Use WebP format where supported
- Configure image sizes: `add_image_size()` and WooCommerce image settings

## Action Scheduler

### Using Action Scheduler

WooCommerce's built-in background job processor:
- `as_schedule_single_action( time(), 'my_hook', $args, 'my-group' )` — run once
- `as_schedule_recurring_action( time(), HOUR_IN_SECONDS, 'my_hook', $args )` — recurring
- `as_enqueue_async_action( 'my_hook', $args )` — ASAP execution
- `as_unschedule_action( 'my_hook', $args )` — cancel
- Monitor via WooCommerce > Status > Scheduled Actions

### When to Use

- Sending batch emails
- Syncing inventory with external systems
- Generating reports
- Processing large data imports/exports
- Cleaning up expired data

## Best Practices

- Enable HPOS for new stores and migrate existing ones
- Use persistent object cache (Redis/Memcached) in production
- Cache expensive computations and API responses with transients
- Use Action Scheduler for background processing — never process heavy tasks during HTTP requests
- Profile with Query Monitor plugin to identify slow queries
- Conditionally load assets only on pages where needed
- Use `wc_get_orders()` / `wc_get_products()` with appropriate limits
- Avoid N+1 query patterns — batch load related data

Fetch the WooCommerce performance documentation and HPOS migration guide for exact configuration, migration steps, and optimization techniques before implementing.
