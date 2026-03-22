---
name: woo-custom-fields
description: Work with WooCommerce product attributes, custom meta fields, taxonomies, custom product tabs, and variation data. Use when adding custom data to products, orders, or customers.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Custom Fields & Attributes

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com product data custom fields` for product custom fields guide
2. Web-search `site:developer.wordpress.org plugins metadata` for WordPress metadata API
3. Web-search `woocommerce custom product attributes programmatically` for attribute creation

## Product Attributes

### Global Attributes

Defined in WooCommerce > Attributes — shared across all products:
- Stored as custom taxonomies: `pa_{attribute_slug}` (e.g., `pa_color`, `pa_size`)
- Terms are the possible values (Red, Blue, Small, Large)
- Can be used for filtering, variations, and layered navigation
- Managed via `wc_create_attribute()`, `wc_update_attribute()`, `wc_delete_attribute()`

### Custom (Local) Product Attributes

Per-product attributes — not global taxonomies:
- Stored in product meta as part of `_product_attributes` array
- Visible on the product page under "Additional Information" tab
- Set via `$product->set_attributes()` with `WC_Product_Attribute` objects

### Setting Attributes Programmatically

Create `WC_Product_Attribute` objects:
- `set_id()` — 0 for custom attributes, taxonomy ID for global
- `set_name()` — taxonomy name (`pa_color`) or custom label
- `set_options()` — array of term IDs (global) or string values (custom)
- `set_visible()` — show on product page
- `set_variation()` — used for variations

## Product Meta

### Core Meta Keys

| Key | Description |
|-----|-------------|
| `_price` | Current active price |
| `_regular_price` | Regular price |
| `_sale_price` | Sale price |
| `_sku` | Stock Keeping Unit |
| `_stock` | Stock quantity |
| `_stock_status` | instock / outofstock / onbackorder |
| `_weight`, `_length`, `_width`, `_height` | Dimensions |
| `_virtual`, `_downloadable` | Product type flags |

### Custom Meta

- `$product->update_meta_data( '_my_custom_field', $value )` then `$product->save()`
- `$product->get_meta( '_my_custom_field' )` — retrieve value
- Prefix custom keys with `_` to hide from the Custom Fields meta box

### Adding Product Edit Fields

Use hooks to add fields to the product edit screen:
- `woocommerce_product_options_general_product_data` — General tab
- `woocommerce_product_options_inventory_product_data` — Inventory tab
- `woocommerce_product_options_shipping_product_data` — Shipping tab
- `woocommerce_product_options_advanced` — Advanced tab
- Save with: `woocommerce_process_product_meta` action

### Field Rendering Functions

- `woocommerce_wp_text_input( $args )` — text input
- `woocommerce_wp_textarea_input( $args )` — textarea
- `woocommerce_wp_select( $args )` — dropdown select
- `woocommerce_wp_checkbox( $args )` — checkbox
- `woocommerce_wp_hidden_input( $args )` — hidden field

## Custom Product Tabs

### Adding to Product Page

Filter `woocommerce_product_tabs` to add, remove, or reorder tabs:
- Return array with `title`, `priority`, `callback` keys
- Remove default tabs by unsetting keys: `description`, `additional_information`, `reviews`

### Adding to Product Edit (Admin)

Filter `woocommerce_product_data_tabs` to add tabs in the product editor:
- Return array with `label`, `target`, `class`, `priority`
- Render panel content via `woocommerce_product_data_panels` action

## Order Meta

- `$order->update_meta_data( '_my_field', $value )` then `$order->save()`
- `$order->get_meta( '_my_field' )` — retrieve value
- HPOS-compatible: always use CRUD methods, never `update_post_meta()`

## Customer Meta

- `$customer->update_meta_data()` / `$customer->get_meta()` via `WC_Customer`
- Or `update_user_meta()` / `get_user_meta()` for WordPress user meta

## Custom Taxonomies

### Registering Custom Taxonomies

Use `register_taxonomy()` on `init` hook:
- Associate with `product` post type for product classification
- Set `show_in_rest` for REST API / block editor support
- Hierarchical (like categories) or flat (like tags)

## Best Practices

- Use global attributes for values shared across products (color, size, brand)
- Use custom meta for product-specific data not used in filtering
- Prefix custom meta keys with underscore to hide from the generic meta box
- Always use CRUD methods (`update_meta_data` / `get_meta`) for HPOS compatibility
- Sanitize all input before saving: `sanitize_text_field()`, `wc_clean()`, `absint()`
- Escape all output: `esc_html()`, `esc_attr()`, `wp_kses_post()`

Fetch the WooCommerce product data and metadata documentation for exact hook names, field function signatures, and attribute API before implementing.
