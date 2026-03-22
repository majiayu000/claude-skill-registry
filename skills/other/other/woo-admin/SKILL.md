---
name: woo-admin
description: Build WooCommerce admin interfaces — settings pages, admin menus, product data tabs/panels, order meta boxes, WooCommerce Admin (React analytics), and reports. Use when creating admin-facing configuration or display pages.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Admin UI Development

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com settings api` for Settings API guide
2. Web-search `site:developer.wordpress.org plugins administration-menus` for WordPress admin menus
3. Web-search `woocommerce admin custom settings page` for current patterns

## Settings API

### WC_Settings_API (For Gateways/Methods)

Payment gateways and shipping methods use `WC_Settings_API`:
- Define fields in `init_form_fields()` as associative array
- Field types: `text`, `textarea`, `select`, `multiselect`, `checkbox`, `password`, `title`, `decimal`, `color`
- Rendered automatically via `$this->generate_settings_html()`
- Saved/loaded automatically via `get_option()` / `update_option()`

### WC_Settings_Page (Custom Settings Tabs)

Add a new tab to WooCommerce > Settings:
1. Extend `WC_Settings_Page`
2. Set `$this->id` and `$this->label`
3. Implement `get_settings_for_default_section()` — return settings array
4. Register via `woocommerce_get_settings_pages` filter

### Settings Field Format

Each field is an array with keys:
- `id` — option name (stored in `wp_options`)
- `title` — field label
- `type` — `text`, `select`, `checkbox`, `textarea`, `number`, `sectionend`, `title`
- `default` — default value
- `desc` — description text
- `options` — for select/multiselect
- `css` — inline CSS for the input

## Admin Menus

### Adding Sub-Menus Under WooCommerce

`add_submenu_page( 'woocommerce', $page_title, $menu_title, $capability, $slug, $callback )`

### Top-Level Menus

`add_menu_page()` for standalone admin sections — less common for WC extensions.

### Capability Checks

- `manage_woocommerce` — WooCommerce admin capability
- `edit_shop_orders` — order management
- `edit_products` — product management
- Always check capabilities in menu and page callbacks

## Product Data Panels

### Adding Tabs

Filter `woocommerce_product_data_tabs`:
```php
$tabs['my_tab'] = [
    'label'    => __( 'My Tab', 'my-plugin' ),
    'target'   => 'my_tab_data',
    'class'    => [ 'show_if_simple', 'show_if_variable' ],
    'priority' => 60,
];
```

### Adding Panel Content

Action `woocommerce_product_data_panels`:
- Render HTML inside a `<div id="my_tab_data" class="panel">` matching the tab target
- Use `woocommerce_wp_text_input()`, `woocommerce_wp_select()`, etc.

### Saving Panel Data

Action `woocommerce_process_product_meta` — receives `$post_id`:
- Sanitize input: `sanitize_text_field( $_POST['my_field'] )`
- Save: `$product->update_meta_data( '_my_field', $value )` then `$product->save()`

## Order Admin Customization

### Meta Boxes

Add custom meta boxes to the order edit screen:
- `add_meta_box( $id, $title, $callback, 'woocommerce_page_wc-orders', $context, $priority )`
- For HPOS: use screen ID `woocommerce_page_wc-orders` (not `shop_order`)
- For legacy: use post type `shop_order`

### Order Actions

Filter `woocommerce_order_actions` to add custom order actions.

### Bulk Actions

Filter `bulk_actions-edit-shop_order` (legacy) or `bulk_actions-woocommerce_page_wc-orders` (HPOS).

## WooCommerce Admin (React-Based)

### Analytics & Reports

WooCommerce Admin is a React SPA for:
- Revenue, Orders, Products, Categories, Coupons, Taxes, Downloads reports
- Dashboard with customizable widgets
- Activity panel (orders, reviews, stock)

### Extending Analytics

Use `@woocommerce/data` and `@woocommerce/components` packages:
- Add custom report pages via `woocommerce_admin_reports_pages` filter (PHP)
- Register custom analytics data stores
- Extend existing reports with additional columns

## Admin Notices

### WooCommerce Admin Notices

- `WC_Admin_Notices::add_custom_notice( $name, $html )` — persistent notices
- `wc_admin_notice()` helper for one-time notices
- `admin_notices` action for standard WordPress admin notices

## Best Practices

- Use WooCommerce Settings API for gateway/method settings
- Use `WC_Settings_Page` for custom settings tabs
- Always check capabilities (`manage_woocommerce`, `edit_products`, etc.)
- Use HPOS-compatible screen IDs for order meta boxes
- Sanitize all admin form input before saving
- Use nonces for all admin form submissions
- Localize admin strings with `__()` / `esc_html__()`

Fetch the WooCommerce Settings API docs and WordPress admin handbook for exact field types, hook names, and screen IDs before implementing.
