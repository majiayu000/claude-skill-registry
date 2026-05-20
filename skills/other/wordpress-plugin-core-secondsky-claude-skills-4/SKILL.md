---
name: wordpress-plugin-core
description: WordPress plugin development with hooks, security, REST API, custom post types. Use for plugin creation, $wpdb queries, Settings API, or encountering SQL injection, XSS, CSRF, nonce errors.

  Keywords: wordpress plugin development, wordpress security, wordpress hooks, wordpress filters, wordpress database, wpdb prepare, sanitize_text_field, esc_html, wp_nonce, custom post type, register_post_type, settings api, rest api, admin-ajax, wordpress sql injection, wordpress xss, wordpress csrf, plugin header, activation hook, deactivation hook, wordpress coding standards, wordpress plugin architecture
license: MIT
---

# WordPress Plugin Development (Core)

**Status**: Production Ready
**Last Updated**: 2025-11-27
**Dependencies**: None (WordPress 5.9+, PHP 7.4+)
**Latest Versions**: WordPress 6.7+, PHP 8.0+ recommended

---

## Quick Start (10 Minutes)

### 1. Choose Plugin Structure

Three architecture patterns available (see `references/plugin-architectures.md` for detailed examples):
- **Simple** (functions only) - Small plugins <5 functions
- **OOP** - Medium plugins with related functionality
- **PSR-4** (Namespaced + Composer) - Modern standard (2025), most maintainable

### 2. Create Plugin Header

Every plugin MUST have a header comment in the main file:

```php
<?php
/**
 * Plugin Name:       My Awesome Plugin
 * Description:       Brief description.
 * Version:           1.0.0
 * Requires at least: 5.9
 * Requires PHP:      7.4
 * Text Domain:       my-plugin
 */

if ( ! defined( 'ABSPATH' ) ) exit;
```

**CRITICAL**: Plugin Name is required, Text Domain must match plugin slug exactly.

### 3. Security Foundation (5 Essentials)

```php
// 1. Unique Prefix (4-5 chars)
function mypl_init() { /* code */ }
add_action( 'init', 'mypl_init' );

// 2. ABSPATH Check (every file)
if ( ! defined( 'ABSPATH' ) ) exit;

// 3. Nonces for Forms
wp_nonce_field( 'mypl_action', 'mypl_nonce' );

// 4. Sanitize Input, Escape Output
$clean = sanitize_text_field( $_POST['input'] );
echo esc_html( $output );

// 5. Prepared Statements
$wpdb->get_results( $wpdb->prepare( "SELECT * FROM {$wpdb->prefix}table WHERE id = %d", $id ) );
```

---

## The 5-Step Security Foundation

### Step 1: Use Unique Prefix for Everything

**Rules**: 4-5 chars minimum, apply to functions, classes, constants, options, transients, meta keys. Avoid `wp_`, `__`, `_`.

```php
// GOOD
function mypl_init() {}
class MyPL_Settings {}
add_option( 'mypl_option', 'value' );

// BAD - Will conflict
function init() {}
class Settings {}
```

### Step 2: Check Capabilities, Not Admin Status

```php
// WRONG
if ( is_admin() ) { /* SECURITY HOLE */ }

// CORRECT
if ( current_user_can( 'manage_options' ) ) { /* Secure */ }
```

**Common Capabilities**: `manage_options` (Admin), `edit_posts` (Editor), `publish_posts` (Author)

### Step 3: The Security Trinity

**Input → Processing → Output** (Sanitize → Validate → Escape):

```php
// SANITIZATION (Input)
$name = sanitize_text_field( $_POST['name'] );
$email = sanitize_email( $_POST['email'] );
$url = esc_url_raw( $_POST['url'] );
$html = wp_kses_post( $_POST['content'] );

// VALIDATION (Logic)
if ( ! is_email( $email ) ) wp_die( 'Invalid email' );

// ESCAPING (Output)
echo esc_html( $name );
echo '<a href="' . esc_url( $url ) . '">' . esc_html( $text ) . '</a>';
```

**Rule**: Sanitize INPUT, escape OUTPUT. Never trust user data.

### Step 4: Nonces (CSRF Protection)

One-time tokens proving requests came from your site.

```php
// Form
<form method="post">
    <?php wp_nonce_field( 'mypl_action', 'mypl_nonce' ); ?>
    <input type="text" name="data" />
</form>

// Verify
if ( ! wp_verify_nonce( $_POST['mypl_nonce'], 'mypl_action' ) ) wp_die( 'Security check failed' );

// AJAX
check_ajax_referer( 'mypl-ajax-nonce', 'nonce' );
```

### Step 5: Prepared Statements for Database

**CRITICAL**: Always use `$wpdb->prepare()` for user input.

```php
// WRONG - SQL Injection
$wpdb->get_results( "SELECT * FROM {$wpdb->prefix}table WHERE id = {$_GET['id']}" );

// CORRECT
$wpdb->get_results( $wpdb->prepare( "SELECT * FROM {$wpdb->prefix}table WHERE id = %d", $_GET['id'] ) );
```

**Placeholders**: `%s` (String), `%d` (Integer), `%f` (Float)

**LIKE Queries**: Use `$wpdb->esc_like()` before adding wildcards:
```php
$search = '%' . $wpdb->esc_like( $term ) . '%';
$wpdb->get_results( $wpdb->prepare( "... WHERE title LIKE %s", $search ) );
```

---

## Critical Rules

### Always Do

✅ **Use unique prefix** (4-5 chars) for all global code (functions, classes, options, transients)
✅ **Add ABSPATH check** to every PHP file: `if ( ! defined( 'ABSPATH' ) ) exit;`
✅ **Check capabilities** (`current_user_can()`) not just `is_admin()`
✅ **Verify nonces** for all forms and AJAX requests
✅ **Use $wpdb->prepare()** for all database queries with user input
✅ **Sanitize input** with `sanitize_*()` functions before saving
✅ **Escape output** with `esc_*()` functions before displaying
✅ **Flush rewrite rules** on activation when registering custom post types
✅ **Use uninstall.php** for permanent cleanup (not deactivation hook)
✅ **Follow WordPress Coding Standards** (tabs for indentation, Yoda conditions)

### Never Do

❌ **Never use extract()** - Creates security vulnerabilities
❌ **Never trust $_POST/$_GET** without sanitization
❌ **Never concatenate user input into SQL** - Always use prepare()
❌ **Never use `is_admin()` alone** for permission checks
❌ **Never output unsanitized data** - Always escape
❌ **Never use generic function/class names** - Always prefix
❌ **Never use short PHP tags** `<?` or `<?=` - Use `<?php` only
❌ **Never delete user data on deactivation** - Only on uninstall
❌ **Never register uninstall hook repeatedly** - Only once on activation
❌ **Never use `register_uninstall_hook()` in main flow** - Use uninstall.php instead

---

## Known Issues Prevention

This skill prevents **20** documented issues:

### Issue #1: SQL Injection
**Error**: Database compromised via unescaped user input
**Source**: https://patchstack.com/articles/sql-injection/ (15% of all vulnerabilities)
**Why It Happens**: Direct concatenation of user input into SQL queries
**Prevention**: Always use `$wpdb->prepare()` with placeholders

```php
// VULNERABLE
$wpdb->query( "DELETE FROM {$wpdb->prefix}table WHERE id = {$_GET['id']}" );

// SECURE
$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->prefix}table WHERE id = %d", $_GET['id'] ) );
```

### Issue #2: XSS (Cross-Site Scripting)
**Error**: Malicious JavaScript executed in user browsers
**Source**: https://patchstack.com (35% of all vulnerabilities)
**Why It Happens**: Outputting unsanitized user data to HTML
**Prevention**: Always escape output with context-appropriate function

```php
// VULNERABLE
echo $_POST['name'];
echo '<div class="' . $_POST['class'] . '">';

// SECURE
echo esc_html( $_POST['name'] );
echo '<div class="' . esc_attr( $_POST['class'] ) . '">';
```

### Issue #3: CSRF (Cross-Site Request Forgery)
**Error**: Unauthorized actions performed on behalf of users
**Source**: https://blog.nintechnet.com/25-wordpress-plugins-vulnerable-to-csrf-attacks/
**Why It Happens**: No verification that requests originated from your site
**Prevention**: Use nonces with `wp_nonce_field()` and `wp_verify_nonce()`

```php
// VULNERABLE
if ( $_POST['action'] == 'delete' ) {
    delete_user( $_POST['user_id'] );
}

// SECURE
if ( ! wp_verify_nonce( $_POST['nonce'], 'mypl_delete_user' ) ) {
    wp_die( 'Security check failed' );
}
delete_user( absint( $_POST['user_id'] ) );
```

### Issue #4: Missing Capability Checks
**Error**: Regular users can access admin functions
**Source**: WordPress Security Review Guidelines
**Why It Happens**: Using `is_admin()` instead of `current_user_can()`
**Prevention**: Always check capabilities, not just admin context

```php
// VULNERABLE
if ( is_admin() ) {
    // Any logged-in user can trigger this
}

// SECURE
if ( current_user_can( 'manage_options' ) ) {
    // Only administrators can trigger this
}
```

### Issue #5: Direct File Access
**Error**: PHP files executed outside WordPress context
**Source**: WordPress Plugin Handbook
**Why It Happens**: No ABSPATH check at top of file
**Prevention**: Add ABSPATH check to every PHP file

```php
// Add to top of EVERY PHP file
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
```

### Additional Issues (#6-20)

**For comprehensive error coverage beyond the Top 5**, load `references/error-catalog.md` which includes:
- **Functionality**: Prefix collision, rewrite rules not flushed, deprecated functions, text domain mismatch, plugin dependencies, autosave triggers
- **Performance**: Scripts loaded everywhere, transients not cleaned, admin-ajax.php performance
- **Security**: Missing sanitization on save, incorrect LIKE queries, using extract(), missing REST API permission callbacks, uninstall hook issues
- **Data Integrity**: Data deleted on deactivation

Each issue includes: error description, source, why it happens, prevention code, impact severity, and frequency.

---

## Plugin Architecture Patterns

Choose the right architecture for your plugin size and complexity:

### Decision Guide

**Simple (Functions Only)**
- **When**: Small plugins (<5 functions), single feature
- **Pros**: Easy to start, minimal boilerplate
- **Cons**: Doesn't scale, hard to organize beyond ~5 functions
- **Example**: Simple shortcode plugin, basic widget

**OOP (Singleton Pattern)**
- **When**: Medium plugins (5-20 functions), related functionality
- **Pros**: Better organization, encapsulation, testable
- **Cons**: More boilerplate than simple, not using modern PHP features
- **Example**: Custom post type plugin, admin settings page

**PSR-4 (Namespaced + Composer)**
- **When**: Large/modern plugins, team development, 2025+ standard
- **Pros**: Modern PHP, namespaces, autoloading, best practices
- **Cons**: Requires Composer, more initial setup
- **Example**: E-commerce extension, multi-feature plugin

### Complete Examples

For full implementation examples with directory structure, activation hooks, and code patterns, load `references/plugin-architectures.md`.

---

## Common Implementation Patterns

This skill provides production-ready patterns for 8 common WordPress plugin features:

1. **Custom Post Types** - Register CPTs with Gutenberg support, flush rewrite rules
2. **Custom Taxonomies** - Hierarchical (categories) or flat (tags) taxonomies
3. **Meta Boxes** - Save custom fields with proper security (nonces, capabilities, autosave checks)
4. **Settings API** - WordPress-native settings pages with sanitization
5. **REST API Endpoints** - Modern API endpoints with permission callbacks and validation
6. **AJAX Handlers** - Legacy admin-ajax.php pattern (use REST API for new projects)
7. **Custom Database Tables** - Create tables with dbDelta, versioning
8. **Transients for Caching** - Cache expensive operations, clear on updates

**For complete implementation code**, load `references/common-patterns.md` when implementing any of these features. Each pattern includes:
- Full working code examples
- Security requirements checklist
- Common mistakes to avoid
- Best practices and performance tips

---


---

## Distribution & Auto-Updates

Plugins hosted outside WordPress.org can provide automatic updates using **Plugin Update Checker** by YahnisElsts (recommended).

**Quick Solutions:**
- **Public Repos**: Plugin Update Checker (GitHub/GitLab/BitBucket)
- **Private Plugins**: Plugin Update Checker + authentication token
- **Commercial Plugins**: Freemius or Custom Update Server
- **No Coding**: Git Updater plugin

**For complete implementation**, load `references/github-auto-updates.md` which includes:
- Plugin Update Checker setup (5 minutes)
- GitHub Releases workflow
- Private repository authentication
- Security best practices (checksums, tokens, rate limiting)
- Alternative solutions comparison
- ZIP structure requirements

---

## Dependencies

**Required**:
- WordPress 5.9+ (recommend 6.7+)
- PHP 7.4+ (recommend 8.0+)

**Optional**:
- Composer 2.0+ - For PSR-4 autoloading
- WP-CLI 2.0+ - For command-line plugin management
- Query Monitor - For debugging and performance analysis

---

## Official Documentation

- **WordPress Plugin Handbook**: https://developer.wordpress.org/plugins/
- **WordPress Coding Standards**: https://developer.wordpress.org/coding-standards/
- **WordPress REST API**: https://developer.wordpress.org/rest-api/
- **WordPress Database Class ($wpdb)**: https://developer.wordpress.org/reference/classes/wpdb/
- **WordPress Security**: https://developer.wordpress.org/apis/security/
- **Settings API**: https://developer.wordpress.org/plugins/settings/settings-api/
- **Custom Post Types**: https://developer.wordpress.org/plugins/post-types/
- **Transients API**: https://developer.wordpress.org/apis/transients/
- **Context7 Library ID**: /websites/developer_wordpress

---

## Troubleshooting

**Fatal Errors**: Enable `WP_DEBUG`, check `wp-content/debug.log`, verify prefixed names

**404 on CPTs**: Flush rewrite rules (add `flush_rewrite_rules();` temporarily in wp-admin)

**Nonce Failures**: Check matching names, correct action, 24-hour expiration

**AJAX Returns 0/-1**: Verify action name matches `wp_ajax_{action}`, nonce sent/verified, handler hooked

**HTML Stripped**: Use `wp_kses_post()` instead of `sanitize_text_field()`

**DB Queries Fail**: Always use `$wpdb->prepare()`, include `$wpdb->prefix`, verify syntax

---

## When to Load References

This skill uses **progressive disclosure** - main file contains essentials, reference files have detailed implementation. Load references based on your current task:

### `references/common-patterns.md` (465 lines)
**Load when**: Implementing specific WordPress features
**Contains**:
- Custom Post Types (registration, Gutenberg support, rewrite rules)
- Custom Taxonomies (hierarchical vs flat, REST API)
- Meta Boxes (security requirements, save hooks, autosave checks)
- Settings API (register_setting, sections, fields hierarchy)
- REST API Endpoints (permission callbacks, validation, responses)
- AJAX Handlers (nonce verification, wp_ajax hooks, JavaScript integration)
- Custom Database Tables (dbDelta, character encoding, versioning)
- Transients for Caching (cache patterns, invalidation, expiration)

### `references/plugin-architectures.md` (220 lines)
**Load when**: Choosing plugin structure or migrating between patterns
**Contains**:
- Simple Pattern (functions only, <5 functions)
- OOP Pattern (singleton, encapsulation, medium plugins)
- PSR-4 Pattern (namespaces, Composer autoloading, modern standard)
- Decision tree for pattern selection
- Complete directory structures with all files
- Activation/deactivation hook examples
- Migration paths between patterns

### `references/error-catalog.md` (Issues #6-20, 573 lines)
**Load when**: Debugging issues beyond Top 5 security vulnerabilities
**Contains**:
- Functionality issues (prefix collision, rewrite rules, deprecated functions, text domains, dependencies, autosave)
- Performance issues (scripts everywhere, transients cleanup, admin-ajax.php alternatives)
- Security issues (sanitization, extract(), REST permissions, uninstall hooks)
- Data integrity issues (deactivation vs uninstall)
**Each issue includes**: Error description, source/reference, why it happens, prevention code, impact severity, frequency

### `references/advanced-topics.md` (150 lines)
**Load when**: Implementing i18n, WP-CLI, cron jobs, or dependency checking
**Contains**:
- Internationalization (i18n) - load_plugin_textdomain(), translation workflow, .pot/.po/.mo files
- WP-CLI Commands - custom command creation, progress bars, output functions
- Scheduled Events (Cron) - wp_schedule_event(), custom schedules, activation hooks
- Plugin Dependencies Check - version requirements, soft dependencies, user-friendly error messages

### `references/security-checklist.md` (527 lines)
**Load when**: Performing security audit or reviewing code for vulnerabilities
**Contains**:
- Complete security audit checklist
- OWASP Top 10 for WordPress
- Code examples for each vulnerability type
- Testing procedures and tools
- Security plugin recommendations

### `references/github-auto-updates.md` (1,224 lines)
**Load when**: Setting up auto-updates for plugins hosted outside WordPress.org
**Contains**:
- Plugin Update Checker (recommended) - 5-minute setup
- GitHub Releases workflow and automation
- Private repository authentication (tokens, wp-config.php)
- Alternative solutions (Git Updater, Custom Server, Freemius)
- Security best practices (checksums, signing, rate limiting)
- ZIP structure requirements and common mistakes
- Deployment automation examples

### `references/common-hooks.md` (234 lines)
**Load when**: Working with WordPress hooks and need hook reference
**Contains**:
- Action hooks reference (init, admin_menu, save_post, etc.)
- Filter hooks reference (the_content, post_type_args, etc.)
- Hook priority and execution order
- Common hook combinations and patterns

---

## Complete Setup Checklist

Use this checklist to verify your plugin:

- [ ] Plugin header complete with all fields
- [ ] ABSPATH check at top of every PHP file
- [ ] All functions/classes use unique prefix
- [ ] All forms have nonce verification
- [ ] All user input is sanitized
- [ ] All output is escaped
- [ ] All database queries use $wpdb->prepare()
- [ ] Capability checks (not just is_admin())
- [ ] Custom post types flush rewrite rules on activation
- [ ] Deactivation hook only clears temporary data
- [ ] uninstall.php handles permanent cleanup
- [ ] Text domain matches plugin slug
- [ ] Scripts/styles only load where needed
- [ ] WP_DEBUG enabled during development
- [ ] Tested with Query Monitor for performance
- [ ] No deprecated function warnings
- [ ] Works with latest WordPress version

---

**Questions? Issues?**

1. Check `references/error-catalog.md` for additional issues #6-20
2. Verify all steps in the security foundation
3. Check official docs: https://developer.wordpress.org/plugins/
4. Enable WP_DEBUG and check debug.log
5. Use Query Monitor plugin to debug hooks and queries
