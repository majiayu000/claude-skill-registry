---
name: woo-security
description: Implement WooCommerce security — nonces, capabilities, input sanitization, output escaping, data validation, PCI compliance considerations, and WordPress security best practices. Use when hardening a WooCommerce store or reviewing security posture.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Security

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.wordpress.org plugins security` for WordPress security handbook
2. Web-search `site:developer.woocommerce.com security best practices` for WooCommerce security
3. Web-search `wordpress security hardening latest` for current hardening guidance

## Nonces (CSRF Protection)

### How Nonces Work

WordPress nonces prevent Cross-Site Request Forgery:
- Generate: `wp_create_nonce( 'my_action' )` or `wp_nonce_field( 'my_action', 'my_nonce' )` (for forms)
- Verify: `wp_verify_nonce( $_POST['my_nonce'], 'my_action' )` or `check_admin_referer( 'my_action', 'my_nonce' )`
- Valid for 24 hours (two 12-hour ticks)

### AJAX Nonces

- Generate: `wp_create_nonce( 'my_ajax_action' )`
- Pass to JS via `wp_localize_script()`: `['nonce' => wp_create_nonce('my_ajax_action')]`
- Verify in handler: `check_ajax_referer( 'my_ajax_action', 'nonce' )`

### REST API Nonces

- Cookie auth uses `X-WP-Nonce` header with `wp_create_nonce( 'wp_rest' )`
- API key auth doesn't need nonces (keys provide authentication)

## Capabilities (Authorization)

### WordPress Capability System

Always check capabilities before performing actions:
- `current_user_can( 'manage_woocommerce' )` — WooCommerce admin
- `current_user_can( 'edit_shop_orders' )` — order management
- `current_user_can( 'edit_products' )` — product management
- `current_user_can( 'view_woocommerce_reports' )` — view reports

### WooCommerce Capabilities

| Capability | Access |
|------------|--------|
| `manage_woocommerce` | Full WooCommerce admin |
| `edit_products` | Create/edit products |
| `edit_shop_orders` | Manage orders |
| `view_woocommerce_reports` | View analytics/reports |
| `edit_shop_coupons` | Manage coupons |

### Custom Capabilities

Register custom capabilities via `add_cap()` on role objects during plugin activation.

## Input Sanitization

### Sanitization Functions

Always sanitize data before using or storing it:

| Function | Use For |
|----------|---------|
| `sanitize_text_field()` | Single-line text input |
| `sanitize_textarea_field()` | Multi-line text |
| `sanitize_email()` | Email addresses |
| `sanitize_url()` | URLs |
| `absint()` | Positive integers |
| `intval()` | Integers (any sign) |
| `floatval()` | Float numbers |
| `wp_kses()` | HTML with allowed tags |
| `wp_kses_post()` | HTML safe for post content |
| `wc_clean()` | WooCommerce string/array sanitizer |
| `wc_sanitize_textarea()` | WooCommerce textarea sanitizer |

### Array Sanitization

`wc_clean()` recursively sanitizes arrays — use for multi-value inputs.

### File Upload Validation

- Validate MIME type with `wp_check_filetype()`
- Use `wp_handle_upload()` for proper file upload processing
- Never trust file extensions — validate content

## Output Escaping

### Escaping Functions

Always escape data on output:

| Function | Context |
|----------|---------|
| `esc_html()` | Inside HTML tags |
| `esc_attr()` | HTML attribute values |
| `esc_url()` | URLs (href, src) |
| `esc_js()` | Inline JavaScript |
| `esc_textarea()` | Inside textarea elements |
| `wp_kses()` | HTML with specific allowed tags |
| `wp_kses_post()` | HTML safe for post content |

### Translation + Escaping

Combine translation with escaping:
- `esc_html__()` / `esc_html_e()` — escaped translated strings
- `esc_attr__()` / `esc_attr_e()` — escaped for attributes
- `wp_kses( sprintf(...), $allowed_html )` — formatted HTML

### The Rule

**Sanitize early (on input), escape late (on output).** Never trust any data from users, databases, or external APIs.

## Data Validation

### Validation Patterns

- Validate data type, format, and range before processing
- Use `is_email()`, `wp_http_validate_url()`, WordPress validators
- WooCommerce validators: `wc_format_decimal()`, `wc_is_valid_url()`
- Return errors via `WP_Error` or `wc_add_notice( $msg, 'error' )`

## SQL Injection Prevention

### Prepared Statements

Always use `$wpdb->prepare()` for custom queries:
- `$wpdb->prepare( "SELECT * FROM {$wpdb->prefix}my_table WHERE id = %d", $id )`
- Placeholders: `%d` (integer), `%s` (string), `%f` (float)
- Never concatenate user input into SQL strings

### Use CRUD/APIs Instead

Prefer WooCommerce CRUD and WordPress APIs over raw SQL:
- `wc_get_orders()`, `wc_get_products()` — safe query builders
- `$order->get_meta()`, `$product->get_price()` — safe data access

## PCI Compliance Considerations

- **Never** store raw credit card numbers
- Use tokenized payment methods (Stripe, Braintree SDKs handle card data client-side)
- Serve checkout over HTTPS
- Keep WordPress, WooCommerce, and all plugins up to date
- Use payment gateways that are PCI DSS compliant

## Additional Hardening

- Set `DISALLOW_FILE_EDIT` in wp-config.php
- Limit login attempts (plugin or `.htaccess`)
- Use strong admin passwords and enforce password policies
- Enable two-factor authentication for admin users
- Keep all software updated (WordPress, WooCommerce, plugins, PHP)
- Use HTTPS everywhere
- Set secure cookie flags
- Restrict REST API access where appropriate (`rest_authentication_errors` filter)
- Disable XML-RPC if not needed: `add_filter( 'xmlrpc_enabled', '__return_false' )`

## Best Practices

- Check nonces on every form submission and AJAX request
- Check capabilities before every privileged operation
- Sanitize ALL input — even from trusted sources
- Escape ALL output — even data from the database
- Use `$wpdb->prepare()` for any custom SQL
- Never store sensitive data in plain text
- Use WordPress APIs instead of raw PHP functions for security-sensitive operations
- Run security audits with WPScan or similar tools

Fetch the WordPress Security handbook and WooCommerce security documentation for exact function signatures, capability mappings, and current best practices before implementing.
