---
name: woo-hooks-filters
description: Master the WordPress hook system for WooCommerce — actions, filters, hook priorities, WooCommerce-specific hooks, and extensibility patterns. Use when adding functionality via hooks or understanding the WooCommerce execution flow.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Hooks & Filters

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.wordpress.org/plugins/hooks/` for WordPress Hooks fundamentals
2. Web-search `site:developer.woocommerce.com hooks` for WooCommerce-specific hooks
3. Web-search `woocommerce action filter reference` for comprehensive hook listings

## How Hooks Work

### Actions

Fire at specific points in execution — used for side effects (sending emails, writing logs, rendering HTML):
- `do_action( 'hook_name', $arg1, $arg2 )` — fires the action
- `add_action( 'hook_name', 'callback', $priority, $accepted_args )` — registers a listener
- `remove_action( 'hook_name', 'callback', $priority )` — unregisters a listener
- Lower `$priority` = runs earlier (default 10)

### Filters

Transform data as it flows through the system — must return a value:
- `apply_filters( 'filter_name', $value, $arg1, $arg2 )` — applies the filter
- `add_filter( 'filter_name', 'callback', $priority, $accepted_args )` — registers a filter
- Callback receives `$value` as first argument, must return the (possibly modified) value
- Chained: each filter's return value is the next filter's input

### Priority

- Default: `10`
- Lower numbers run first (1 before 10 before 99)
- Use early priorities (1–5) to modify data before others see it
- Use late priorities (20+) to act on fully-processed data

## Key WooCommerce Hooks

### Product Hooks

| Hook | Type | When |
|------|------|------|
| `woocommerce_product_get_price` | Filter | Price is retrieved |
| `woocommerce_before_single_product` | Action | Before product page renders |
| `woocommerce_after_single_product_summary` | Action | After product summary |
| `woocommerce_product_options_general_product_data` | Action | General tab in product edit |
| `woocommerce_process_product_meta` | Action | Product is saved |

### Cart Hooks

| Hook | Type | When |
|------|------|------|
| `woocommerce_before_cart` | Action | Before cart page |
| `woocommerce_cart_calculate_fees` | Action | Calculate cart fees |
| `woocommerce_before_calculate_totals` | Action | Before totals calculation |
| `woocommerce_add_to_cart` | Action | Item added to cart |
| `woocommerce_cart_item_price` | Filter | Cart item price display |

### Checkout Hooks

| Hook | Type | When |
|------|------|------|
| `woocommerce_before_checkout_form` | Action | Before checkout form |
| `woocommerce_checkout_fields` | Filter | Modify checkout fields |
| `woocommerce_checkout_process` | Action | Validate checkout |
| `woocommerce_checkout_order_processed` | Action | Order created from checkout |
| `woocommerce_payment_complete` | Action | Payment completed |

### Order Hooks

| Hook | Type | When |
|------|------|------|
| `woocommerce_order_status_changed` | Action | Order status transition |
| `woocommerce_order_status_{from}_to_{to}` | Action | Specific status transition |
| `woocommerce_new_order` | Action | New order created |
| `woocommerce_thankyou` | Action | Thank-you page |

### Admin Hooks

| Hook | Type | When |
|------|------|------|
| `woocommerce_admin_order_data_after_order_details` | Action | After order details in admin |
| `woocommerce_product_data_tabs` | Filter | Product data tabs |
| `woocommerce_product_data_panels` | Action | Product data panels content |
| `woocommerce_get_settings_pages` | Filter | Register settings pages |

### Lifecycle Hooks

| Hook | Type | When |
|------|------|------|
| `woocommerce_init` | Action | WooCommerce initialized |
| `woocommerce_loaded` | Action | WooCommerce classes loaded |
| `before_woocommerce_init` | Action | Before WC initializes (declare features here) |
| `woocommerce_after_register_taxonomy` | Action | After taxonomies registered |

## Hook Patterns

### Conditional Hook Registration

Register hooks only when needed:
- `is_admin()` — admin-only hooks
- `wp_doing_ajax()` — AJAX-only hooks
- `is_checkout()`, `is_cart()` — page-specific hooks

### Class-Based Hook Registration

Use class methods as callbacks: `add_action( 'hook', [ $this, 'method' ] )` or `add_action( 'hook', [ __CLASS__, 'static_method' ] )`

### Removing WooCommerce Default Behavior

`remove_action()` / `remove_filter()` with the exact callback and priority that was used to add it. For class methods on singletons, reference the instance: `remove_action( 'hook', [ WC()->structured_data, 'method' ] )`

### Dynamic Hook Names

WooCommerce uses dynamic hooks based on context:
- `woocommerce_product_get_{$prop}` — getter filter for any product property
- `woocommerce_order_status_{$status}` — status-specific action
- `woocommerce_widget_{$widget_id}_args` — widget-specific filter

## Best Practices

- Always specify `$accepted_args` when your callback needs more than one argument
- Use late priorities when you need the final value (after other plugins have filtered)
- Prefer `add_filter` over directly modifying globals
- Use `has_action()` / `has_filter()` to check if a hook is already registered
- Never call `do_action()` / `apply_filters()` on WooCommerce core hooks from your code (fire your own hooks instead)
- Prefix your custom hook names: `do_action( 'my_extension_after_process', $data )`

Fetch the WooCommerce hook reference for current hook names, parameters, and deprecation notices before implementing.
