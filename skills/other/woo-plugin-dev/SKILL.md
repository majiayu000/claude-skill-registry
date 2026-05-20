---
name: woo-plugin-dev
description: Create WooCommerce extensions/plugins — file structure, main plugin file, activation/deactivation hooks, custom database tables, autoloading, and WordPress plugin API. Use when building new WooCommerce extensions or structuring plugin code.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Extension / Plugin Development

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.wordpress.org/plugins/` for WordPress Plugin Handbook
2. Fetch `https://developer.woocommerce.com/docs/extension-guidelines/` for WooCommerce extension guidelines
3. Web-search `site:developer.woocommerce.com extension development best practices` for current patterns

## Main Plugin File

### Required Headers

```php
<?php
/**
 * Plugin Name: My WooCommerce Extension
 * Plugin URI:  https://example.com/my-extension
 * Description: A WooCommerce extension that does X.
 * Version:     1.0.0
 * Author:      Your Name
 * Author URI:  https://example.com
 * License:     GPL-2.0-or-later
 * Text Domain: my-woo-extension
 * Domain Path: /languages
 * Requires at least: 6.4
 * Requires PHP: 8.0
 * Requires Plugins: woocommerce
 * WC requires at least: 8.0
 * WC tested up to: 9.5
 */
```

### Guarding Against Direct Access

Every PHP file starts with: `defined( 'ABSPATH' ) || exit;`

### WooCommerce Dependency Check

Before initializing, verify WooCommerce is active:
- Check `class_exists( 'WooCommerce' )` in a `plugins_loaded` hook
- Or use `Requires Plugins: woocommerce` header (WordPress 6.5+)

## Activation & Deactivation

### Activation Hook

`register_activation_hook( __FILE__, 'my_plugin_activate' )` — runs on first activation:
- Create custom database tables (via `dbDelta()`)
- Add default options (`add_option()`)
- Schedule recurring actions (Action Scheduler)
- Flush rewrite rules if registering custom post types

### Deactivation Hook

`register_deactivation_hook( __FILE__, 'my_plugin_deactivate' )` — runs when deactivated:
- Unschedule cron/Action Scheduler events
- Flush rewrite rules
- Do NOT delete data (that's for uninstall)

### Uninstall

Use `uninstall.php` (preferred) or `register_uninstall_hook()`:
- Delete custom options, transients, custom tables
- Clean up user meta, post meta
- Only runs when user explicitly deletes the plugin

## Custom Database Tables

### Using `$wpdb` and `dbDelta()`

Create tables on activation:
- Use `$wpdb->prefix` for table name prefix
- Define schema with `dbDelta()` from `wp-admin/includes/upgrade.php`
- `dbDelta()` is idempotent — handles CREATE and ALTER
- Store DB version in an option to manage schema upgrades

### Table Naming

Convention: `{$wpdb->prefix}wc_my_extension_tablename`

## Autoloading

### Composer PSR-4

Standard approach for namespaced classes:
- Configure `autoload.psr-4` in `composer.json`
- `require __DIR__ . '/vendor/autoload.php'` in main plugin file
- Namespace convention: `MyVendor\MyExtension\`

### WordPress File-Based

Legacy approach: `require_once` individual files in an `includes/` directory. Still common in WooCommerce core.

## Plugin Architecture Patterns

### Singleton Main Class

Common WooCommerce extension pattern:
- Private constructor
- Static `instance()` method
- `init()` method that registers all hooks
- Accessed via global function (e.g., `my_extension()`)

### Service Container (Advanced)

For larger extensions, use a lightweight DI container or service provider pattern with constructor injection.

### Feature Flags

Use WooCommerce's `FeaturesUtil` to declare compatibility:
- `custom_order_tables` — HPOS support
- `cart_checkout_blocks` — Block checkout support

## Coding Standards

### WordPress Coding Standards (WPCS)

- **Tabs** for indentation (not spaces)
- **Yoda conditions**: `if ( 'value' === $var )`
- **Braces** on same line for functions/control structures
- **Spaces** inside parentheses: `if ( $condition )`
- **Prefix** all globals: functions, classes, hooks, options, constants
- **Escaping** all output: `esc_html()`, `esc_attr()`, `esc_url()`, `wp_kses()`
- **Sanitizing** all input: `sanitize_text_field()`, `absint()`, `wp_unslash()`
- **Nonces** for all form submissions and AJAX

## Best Practices

- Use `Requires Plugins: woocommerce` header (WordPress 6.5+)
- Declare HPOS compatibility in every extension
- Use Composer autoloading for new code
- Prefix everything to avoid naming collisions
- Internationalize all user-facing strings with `__()`, `_e()`, `esc_html__()`
- Load text domain via `load_plugin_textdomain()`
- Use WordPress built-in functions over raw PHP equivalents (`wp_remote_get()` vs `curl`)
- Never modify WooCommerce core files — always use hooks

Fetch the WordPress Plugin Handbook and WooCommerce extension guidelines for exact patterns and current requirements before implementing.
