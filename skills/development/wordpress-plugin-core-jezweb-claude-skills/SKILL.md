---
name: wordpress-plugin-core
description: |
  Build secure WordPress plugins with hooks, database interactions, Settings API, custom post types, and REST API. Covers Simple, OOP, and PSR-4 architecture patterns plus the Security Trinity. Includes WordPress 6.7-6.9 breaking changes.

  Use when creating plugins or troubleshooting SQL injection, XSS, CSRF, REST API vulnerabilities, wpdb::prepare errors, nonce edge cases, or WordPress 6.8+ bcrypt migration.
user-invocable: true
---

# WordPress Plugin Development (Core)

**Last Updated**: 2026-01-21
**Latest Versions**: WordPress 6.9+ (Dec 2, 2025), PHP 8.0+ recommended, PHP 8.5 compatible
**Dependencies**: None (WordPress 5.9+, PHP 7.4+ minimum)

---

## Quick Start

**Architecture Patterns**: Simple (functions only, <5 functions) | OOP (medium plugins) | PSR-4 (modern/large, recommended 2025+)

**Plugin Header** (only Plugin Name required):
```php
<?php
/**
 * Plugin Name: My Plugin
 * Version: 1.0.0
 * Requires at least: 5.9
 * Requires PHP: 7.4
 * Text Domain: my-plugin
 */

if ( ! defined( 'ABSPATH' ) ) exit;
```

**Security Foundation** (5 essentials before writing functionality):
```php
// 1. Unique Prefix
define( 'MYPL_VERSION', '1.0.0' );
function mypl_init() { /* code */ }
add_action( 'init', 'mypl_init' );

// 2. ABSPATH Check (every PHP file)
if ( ! defined( 'ABSPATH' ) ) exit;

// 3. Nonces
wp_nonce_field( 'mypl_action', 'mypl_nonce' );
wp_verify_nonce( $_POST['mypl_nonce'], 'mypl_action' );

// 4. Sanitize Input, Escape Output
$clean = sanitize_text_field( $_POST['input'] );
echo esc_html( $output );

// 5. Prepared Statements
global $wpdb;
$wpdb->get_results( $wpdb->prepare( "SELECT * FROM {$wpdb->prefix}table WHERE id = %d", $id ) );
```

---

## Security Foundation (Detailed)

### Unique Prefix (4-5 chars minimum)
Apply to: functions, classes, constants, options, transients, meta keys. Avoid: `wp_`, `__`, `_`.

```php
function mypl_function() {}  // ✅
class MyPL_Class {}          // ✅
function init() {}           // ❌ Will conflict
```

### Capabilities Check (Not is_admin())
```php
// ❌ WRONG - Security hole
if ( is_admin() ) { /* delete data */ }

// ✅ CORRECT
if ( current_user_can( 'manage_options' ) ) { /* delete data */ }
```

Common: `manage_options` (Admin), `edit_posts` (Editor/Author), `read` (Subscriber)

### Security Trinity (Input → Processing → Output)
```php
// Sanitize INPUT
$name = sanitize_text_field( $_POST['name'] );
$email = sanitize_email( $_POST['email'] );
$html = wp_kses_post( $_POST['content'] );  // Allow safe HTML
$ids = array_map( 'absint', $_POST['ids'] );

// Validate LOGIC
if ( ! is_email( $email ) ) wp_die( 'Invalid' );

// Escape OUTPUT
echo esc_html( $name );
echo '<a href="' . esc_url( $url ) . '">';
echo '<div class="' . esc_attr( $class ) . '">';
```

### Nonces (CSRF Protection)
```php
// Form
<?php wp_nonce_field( 'mypl_action', 'mypl_nonce' ); ?>
if ( ! wp_verify_nonce( $_POST['mypl_nonce'], 'mypl_action' ) ) wp_die( 'Failed' );

// AJAX
check_ajax_referer( 'mypl-ajax-nonce', 'nonce' );
wp_localize_script( 'mypl-script', 'mypl_ajax_object', array(
    'ajaxurl' => admin_url( 'admin-ajax.php' ),
    'nonce'   => wp_create_nonce( 'mypl-ajax-nonce' ),
) );
```

### Prepared Statements
```php
// ❌ SQL Injection
$wpdb->get_results( "SELECT * FROM table WHERE id = {$_GET['id']}" );

// ✅ Prepared (%s=String, %d=Integer, %f=Float)
$wpdb->get_results( $wpdb->prepare( "SELECT * FROM {$wpdb->prefix}table WHERE id = %d", $_GET['id'] ) );

// LIKE Queries
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

This skill prevents **29** documented issues:

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

### Issue #6: Prefix Collision
**Error**: Functions/classes conflict with other plugins
**Source**: WordPress Coding Standards
**Why It Happens**: Generic names without unique prefix
**Prevention**: Use 4-5 character prefix on ALL global code

```php
// CAUSES CONFLICTS
function init() {}
class Settings {}
add_option( 'api_key', $value );

// SAFE
function mypl_init() {}
class MyPL_Settings {}
add_option( 'mypl_api_key', $value );
```

### Issue #7: Rewrite Rules Not Flushed (and Performance)
**Error**: Custom post types return 404 errors, or database overload from repeated flushing
**Source**: [WordPress Plugin Handbook](https://developer.wordpress.org/plugins/), [Permalink Manager Pro](https://permalinkmanager.pro/blog/flush-rewrite-rules/)
**Why It Happens**: Forgot to flush rewrite rules after registering CPT, OR calling flush on every page load
**Prevention**: Flush ONLY on activation/deactivation, NEVER on every page load

```php
// ✅ CORRECT - Only flush on activation
function mypl_activate() {
    mypl_register_cpt();
    flush_rewrite_rules();
}
register_activation_hook( __FILE__, 'mypl_activate' );

function mypl_deactivate() {
    flush_rewrite_rules();
}
register_deactivation_hook( __FILE__, 'mypl_deactivate' );

// ❌ WRONG - Causes database overload on EVERY page load
add_action( 'init', 'mypl_register_cpt' );
add_action( 'init', 'flush_rewrite_rules' );  // BAD! Performance killer!

// ❌ WRONG - In functions.php
function mypl_register_cpt() {
    register_post_type( 'book', ... );
    flush_rewrite_rules();  // BAD! Runs every time
}
```

**User-Facing Fix**: If CPT shows 404, manually flush by going to Settings → Permalinks → Save Changes.

### Issue #8: Transients Not Cleaned
**Error**: Database accumulates expired transients
**Source**: WordPress Transients API Documentation
**Why It Happens**: No cleanup on uninstall
**Prevention**: Delete transients in uninstall.php

```php
// uninstall.php
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

global $wpdb;
$wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_mypl_%'" );
$wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_timeout_mypl_%'" );
```

### Issue #9: Scripts Loaded Everywhere
**Error**: Performance degraded by unnecessary asset loading
**Source**: WordPress Performance Best Practices
**Why It Happens**: Enqueuing scripts/styles without conditional checks
**Prevention**: Only load assets where needed

```php
// BAD - Loads on every page
add_action( 'wp_enqueue_scripts', function() {
    wp_enqueue_script( 'mypl-script', $url );
} );

// GOOD - Only loads on specific page
add_action( 'wp_enqueue_scripts', function() {
    if ( is_page( 'my-page' ) ) {
        wp_enqueue_script( 'mypl-script', $url, array( 'jquery' ), '1.0', true );
    }
} );
```

### Issue #10: Missing Sanitization on Save
**Error**: Malicious data stored in database
**Source**: WordPress Data Validation
**Why It Happens**: Saving $_POST data without sanitization
**Prevention**: Always sanitize before saving

```php
// VULNERABLE
update_option( 'mypl_setting', $_POST['value'] );

// SECURE
update_option( 'mypl_setting', sanitize_text_field( $_POST['value'] ) );
```

### Issue #11: Incorrect LIKE Queries
**Error**: SQL syntax errors or injection vulnerabilities
**Source**: WordPress $wpdb Documentation
**Why It Happens**: LIKE wildcards not escaped properly
**Prevention**: Use `$wpdb->esc_like()`

```php
// WRONG
$search = '%' . $term . '%';

// CORRECT
$search = '%' . $wpdb->esc_like( $term ) . '%';
$results = $wpdb->get_results( $wpdb->prepare( "... WHERE title LIKE %s", $search ) );
```

### Issue #12: Using extract()
**Error**: Variable collision and security vulnerabilities
**Source**: WordPress Coding Standards
**Why It Happens**: extract() creates variables from array keys
**Prevention**: Never use extract(), access array elements directly

```php
// DANGEROUS
extract( $_POST );
// Now $any_array_key becomes a variable

// SAFE
$name = isset( $_POST['name'] ) ? sanitize_text_field( $_POST['name'] ) : '';
```

### Issue #13: Missing Permission Callback in REST API
**Error**: Endpoints accessible to everyone, allowing unauthorized access or privilege escalation
**Source**: [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/), [Patchstack CVE Database](https://patchstack.com/articles/critical-suretriggers-plugin-vulnerability-exploited-within-4-hours/)
**Why It Happens**: No `permission_callback` specified, or missing `show_in_index => false` for sensitive endpoints
**Prevention**: Always add permission_callback AND hide sensitive endpoints from REST index

**Real 2025-2026 Vulnerabilities**:
- **All in One SEO (3M+ sites)**: Missing permission check allowed contributor-level users to view global AI access token
- **AI Engine Plugin (CVE-2025-11749, CVSS 9.8 Critical)**: Failed to set `show_in_index => false`, exposed bearer token in /wp-json/ index, full admin privileges granted to unauthenticated attackers
- **SureTriggers**: Insufficient authorization checks exploited within 4 hours of disclosure
- **Worker for Elementor (CVE-2025-66144)**: Subscriber-level privileges could invoke restricted features

```php
// ❌ VULNERABLE - Missing permission_callback (WordPress 5.5+ requires it!)
register_rest_route( 'myplugin/v1', '/data', array(
    'methods'  => 'GET',
    'callback' => 'my_callback',
) );

// ✅ SECURE - Basic protection
register_rest_route( 'myplugin/v1', '/data', array(
    'methods'             => 'GET',
    'callback'            => 'my_callback',
    'permission_callback' => function() {
        return current_user_can( 'edit_posts' );
    },
) );

// ✅ SECURE - Hide sensitive endpoints from REST index
register_rest_route( 'myplugin/v1', '/admin', array(
    'methods'             => 'POST',
    'callback'            => 'my_admin_callback',
    'permission_callback' => function() {
        return current_user_can( 'manage_options' );
    },
    'show_in_index'       => false,  // Don't expose in /wp-json/
) );
```

**2025-2026 Statistics**: 64,782 total vulnerabilities tracked, 333 new in one week, 236 remained unpatched. REST API auth issues represent significant percentage.

### Issue #14: Uninstall Hook Registered Repeatedly
**Error**: Option written on every page load
**Source**: WordPress Plugin Handbook
**Why It Happens**: register_uninstall_hook() called in main flow
**Prevention**: Use uninstall.php file instead

```php
// BAD - Runs on every page load
register_uninstall_hook( __FILE__, 'mypl_uninstall' );

// GOOD - Use uninstall.php file (preferred method)
// Create uninstall.php in plugin root
```

### Issue #15: Data Deleted on Deactivation
**Error**: Users lose data when temporarily disabling plugin
**Source**: WordPress Plugin Development Best Practices
**Why It Happens**: Confusion about deactivation vs uninstall
**Prevention**: Only delete data in uninstall.php, never on deactivation

```php
// WRONG - Deletes user data on deactivation
register_deactivation_hook( __FILE__, function() {
    delete_option( 'mypl_user_settings' );
} );

// CORRECT - Only clear temporary data on deactivation
register_deactivation_hook( __FILE__, function() {
    delete_transient( 'mypl_cache' );
} );

// CORRECT - Delete all data in uninstall.php
```

### Issue #16: Using Deprecated Functions
**Error**: Plugin breaks on WordPress updates
**Source**: WordPress Deprecated Functions List
**Why It Happens**: Using functions removed in newer WordPress versions
**Prevention**: Enable WP_DEBUG during development

```php
// In wp-config.php (development only)
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
```

### Issue #17: Text Domain Mismatch
**Error**: Translations don't load
**Source**: WordPress Internationalization
**Why It Happens**: Text domain doesn't match plugin slug
**Prevention**: Use exact plugin slug everywhere

```php
// Plugin header
// Text Domain: my-plugin

// In code - MUST MATCH EXACTLY
__( 'Text', 'my-plugin' );
_e( 'Text', 'my-plugin' );
```

### Issue #18: Missing Plugin Dependencies
**Error**: Fatal error when required plugin is inactive
**Source**: WordPress Plugin Dependencies
**Why It Happens**: No check for required plugins
**Prevention**: Check for dependencies on plugins_loaded

```php
add_action( 'plugins_loaded', function() {
    if ( ! class_exists( 'WooCommerce' ) ) {
        add_action( 'admin_notices', function() {
            echo '<div class="error"><p>My Plugin requires WooCommerce.</p></div>';
        } );
        return;
    }
    // Initialize plugin
} );
```

### Issue #19: Autosave Triggering Meta Save
**Error**: Meta saved multiple times, performance issues
**Source**: WordPress Post Meta
**Why It Happens**: No autosave check in save_post hook
**Prevention**: Check for DOING_AUTOSAVE constant

```php
add_action( 'save_post', function( $post_id ) {
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }

    // Safe to save meta
} );
```

### Issue #20: admin-ajax.php Performance
**Error**: Slow AJAX responses
**Source**: https://deliciousbrains.com/comparing-wordpress-rest-api-performance-admin-ajax-php/
**Why It Happens**: admin-ajax.php loads entire WordPress core
**Prevention**: Use REST API for new projects (10x faster)

```php
// OLD: admin-ajax.php (still works but slower)
add_action( 'wp_ajax_mypl_action', 'mypl_ajax_handler' );

// NEW: REST API (10x faster, recommended)
add_action( 'rest_api_init', function() {
    register_rest_route( 'myplugin/v1', '/endpoint', array(
        'methods'             => 'POST',
        'callback'            => 'mypl_rest_handler',
        'permission_callback' => function() {
            return current_user_can( 'edit_posts' );
        },
    ) );
} );
```

### Issue #21: Missing show_in_rest for Block Editor
**Error**: Custom post types show classic editor instead of Gutenberg block editor
**Source**: [WordPress VIP Documentation](https://docs.wpvip.com/wordpress-on-vip/block-editor/), [GitHub Issue #7595](https://github.com/WordPress/gutenberg/issues/7595)
**Why It Happens**: Forgot to set `show_in_rest => true` when registering custom post type
**Prevention**: Always include show_in_rest for CPTs that need block editor

```php
// ❌ WRONG - Block editor won't work
register_post_type( 'book', array(
    'public' => true,
    'supports' => array('editor'),
    // Missing show_in_rest!
) );

// ✅ CORRECT
register_post_type( 'book', array(
    'public' => true,
    'show_in_rest' => true,  // Required for block editor
    'supports' => array('editor'),
) );
```

**Critical Rule**: Only post types registered with `'show_in_rest' => true` are compatible with the block editor. The block editor is dependent on the WordPress REST API. For post types that are incompatible with the block editor—or have `show_in_rest => false`—the classic editor will load instead.

### Issue #22: wpdb::prepare() Table Name Escaping
**Error**: SQL syntax error from quoted table names, or hardcoded prefix breaks on different installations
**Source**: [WordPress Coding Standards Issue #2442](https://github.com/WordPress/WordPress-Coding-Standards/issues/2442)
**Why It Happens**: Using table names as placeholders adds quotes around the table name
**Prevention**: Table names must NOT be in prepare() placeholders

```php
// ❌ WRONG - Adds quotes around table name
$table = $wpdb->prefix . 'my_table';
$wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM %s WHERE id = %d",
    $table, $id
) );
// Result: SELECT * FROM 'wp_my_table' WHERE id = 1
// FAILS - table name is quoted

// ❌ WRONG - Hardcoded prefix
$wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM wp_my_table WHERE id = %d",
    $id
) );
// FAILS if user changed table prefix

// ✅ CORRECT - Table name NOT in prepare()
$table = $wpdb->prefix . 'my_table';
$wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$table} WHERE id = %d",
    $id
) );

// ✅ CORRECT - Using wpdb->prefix for built-in tables
$wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID = %d",
    $id
) );
```

### Issue #23: Nonce Verification Edge Cases
**Error**: Confusing user experience from nonce failures, or false sense of security
**Source**: [MalCare: wp_verify_nonce()](https://www.malcare.com/blog/wp_verify_nonce/), [Pressidium: Understanding Nonces](https://pressidium.com/blog/nonces-in-wordpress-all-you-need-to-know/)
**Why It Happens**: Misunderstanding nonce behavior and limitations
**Prevention**: Understand nonce edge cases and always combine with capability checks

**Edge Cases**:

1. **Time-Based Return Values**:
```php
$result = wp_verify_nonce( $nonce, 'action' );
// Returns 1: Valid, generated 0-12 hours ago
// Returns 2: Valid, generated 12-24 hours ago
// Returns false: Invalid or expired
```

2. **Nonce Reusability**: WordPress doesn't track if a nonce has been used. They can be used multiple times within the 12-24 hour window.

3. **Session Invalidation**: A nonce is only valid when tied to a valid session. If a user logs out, all their nonces become invalid, causing confusing UX if they had a form open.

4. **Caching Problems**: Cache issues can cause mismatches when caching plugins serve an older nonce.

5. **NOT a Substitute for Authorization**:
```php
// ❌ INSUFFICIENT - Only checks origin, not permission
if ( wp_verify_nonce( $_POST['nonce'], 'delete_user' ) ) {
    delete_user( $_POST['user_id'] );
}

// ✅ CORRECT - Combine with capability check
if ( wp_verify_nonce( $_POST['nonce'], 'delete_user' ) &&
     current_user_can( 'delete_users' ) ) {
    delete_user( absint( $_POST['user_id'] ) );
}
```

**Key Principle (2025)**: Nonces should never be relied on for authentication or authorization. Always assume nonces can be compromised. Protect your functions using current_user_can().

### Issue #24: Hook Priority and Argument Count
**Error**: Hook callback doesn't receive expected arguments, or runs in wrong order
**Source**: [Kinsta: WordPress Hooks Bootcamp](https://kinsta.com/blog/wordpress-hooks/)
**Why It Happens**: Default is only 1 argument, priority defaults to 10
**Prevention**: Specify argument count and priority explicitly when needed

```php
// ❌ WRONG - Only receives $post_id
add_action( 'save_post', 'my_save_function' );
function my_save_function( $post_id, $post, $update ) {
    // $post and $update are NULL!
}

// ✅ CORRECT - Specify argument count
add_action( 'save_post', 'my_save_function', 10, 3 );
function my_save_function( $post_id, $post, $update ) {
    // Now all 3 arguments are available
}

// Priority matters (lower number = runs earlier)
add_action( 'init', 'first_function', 5 );   // Runs first
add_action( 'init', 'second_function', 10 );  // Default priority
add_action( 'init', 'third_function', 15 );   // Runs last
```

**Best Practices**:
- Always prefix custom hook names to avoid collisions: `do_action( 'mypl_data_processed' )` not `do_action( 'data_processed' )`
- Filters must RETURN modified data, not echo it
- Hook placement affects backwards compatibility - choose carefully

### Issue #25: Custom Post Type URL Conflicts
**Error**: Individual CPT posts return 404 errors despite permalinks flushed
**Source**: [Permalink Manager Pro: URL Conflicts](https://permalinkmanager.pro/blog/wordpress-url-conflicts/)
**Why It Happens**: CPT slug matches a page slug, creating URL conflict
**Prevention**: Use different slug for CPT or rename the page

```php
// ❌ CONFLICT - Page and CPT use same slug
// Page URL: example.com/portfolio/
register_post_type( 'portfolio', array(
    'rewrite' => array( 'slug' => 'portfolio' ),
) );
// Individual posts 404: example.com/portfolio/my-project/

// ✅ SOLUTION 1 - Use different slug for CPT
register_post_type( 'portfolio', array(
    'rewrite' => array( 'slug' => 'projects' ),
) );
// Posts: example.com/projects/my-project/
// Page: example.com/portfolio/

// ✅ SOLUTION 2 - Use hierarchical slug
register_post_type( 'portfolio', array(
    'rewrite' => array( 'slug' => 'work/portfolio' ),
) );
// Posts: example.com/work/portfolio/my-project/

// ✅ SOLUTION 3 - Rename the page slug
// Change page from /portfolio/ to /our-portfolio/
```

### Issue #26: WordPress 6.8 bcrypt Password Hashing Migration
**Error**: Custom password hash handling breaks after WordPress 6.8 upgrade
**Source**: [WordPress Core Make](https://make.wordpress.org/core/2025/02/17/wordpress-6-8-will-use-bcrypt-for-password-hashing/), [GitHub Issue #21022](https://core.trac.wordpress.org/ticket/21022)
**Why It Happens**: WordPress 6.8+ switched from phpass to bcrypt password hashing
**Prevention**: Use WordPress password functions, don't handle hashes directly

**What Changed** (WordPress 6.8, April 2025):
- Default password hashing algorithm changed from phpass to bcrypt
- New hash prefix: `$wp$2y$` (SHA-384 pre-hashed bcrypt)
- Existing passwords automatically rehashed on next login
- Popular bcrypt plugins (roots/wp-password-bcrypt) now redundant

```php
// ✅ SAFE - These functions continue to work without changes
wp_hash_password( $password );
wp_check_password( $password, $hash );

// ⚠️ NEEDS UPDATE - Direct phpass hash handling
if ( strpos( $hash, '$P$' ) === 0 ) {
    // Custom phpass logic - needs update for bcrypt
}

// ✅ NEW - Detect hash type
if ( strpos( $hash, '$wp$2y$' ) === 0 ) {
    // bcrypt hash (WordPress 6.8+)
} elseif ( strpos( $hash, '$P$' ) === 0 ) {
    // phpass hash (WordPress <6.8)
}
```

**Action Required**:
- Review plugins that directly handle password hashes
- Remove bcrypt plugins when upgrading to 6.8+
- No action needed for standard wp_hash_password/wp_check_password usage

### Issue #27: WordPress 6.9 WP_Dependencies Deprecation
**Error**: "Deprecated: Function WP_Dependencies->add_data() was called with an argument that is deprecated"
**Source**: [WordPress 6.9 Documentation](https://wordpress.org/documentation/wordpress-version/version-6-9/), [WordPress Support Forum](https://wordpress.org/support/topic/after-automatic-updating-to-6-9-deprecated-function-wp_dependencies/)
**Why It Happens**: WordPress 6.9 (Dec 2, 2025) deprecated WP_Dependencies object methods
**Prevention**: Test plugins with WP_DEBUG enabled on WordPress 6.9, replace deprecated methods

**Affected Plugins** (confirmed):
- WooCommerce (fixed in 10.4.2)
- Yoast SEO (fixed in 26.6)
- Elementor (requires 3.24+)

**Breaking Changes**: WordPress 6.9 removed or modified several deprecated functions that older themes and plugins relied on, breaking custom menu walkers, classic widgets, media modals, and customizer features.

**Action Required**:
- Test plugins with WP_DEBUG enabled on WordPress 6.9
- Replace deprecated WP_Dependencies methods
- Check for deprecation notices in debug.log
- While top 1,000 plugins patched within hours, unmaintained plugins often lag behind

### Issue #28: Translation Loading Changes in WordPress 6.7
**Error**: Translations don't load or debug notices appear
**Source**: [WooCommerce Developer Blog](https://developer.woocommerce.com/2024/11/11/developer-advisory-translation-loading-changes-in-wordpress-6-7/), [WordPress 6.7 Field Guide](https://make.wordpress.org/core/2024/10/23/wordpress-6-7-field-guide/)
**Why It Happens**: WordPress 6.7+ changed when/how translations load
**Prevention**: Load translations after 'init' priority 10, ensure text domain matches plugin slug

```php
// ❌ WRONG - Loading too early
add_action( 'init', 'load_plugin_textdomain' );

// ✅ CORRECT - Load after 'init' priority 10
add_action( 'init', 'load_plugin_textdomain', 11 );

// Ensure text domain matches plugin slug EXACTLY
// Plugin header: Text Domain: my-plugin
__( 'Text', 'my-plugin' );  // Must match exactly
```

**Action Required**:
- Review when load_plugin_textdomain() is called
- Ensure text domain matches plugin slug exactly
- Test with WP_DEBUG enabled

### Issue #29: wpdb::prepare() Missing Placeholders Error
**Error**: "The query argument of wpdb::prepare() must have a placeholder"
**Source**: [WordPress $wpdb Documentation](https://developer.wordpress.org/reference/classes/wpdb/), [SitePoint: Working with Databases](https://www.sitepoint.com/working-with-databases-in-wordpress/)
**Why It Happens**: Using prepare() without any placeholders
**Prevention**: Don't use prepare() if no dynamic data

```php
// ❌ WRONG
$wpdb->prepare( "SELECT * FROM {$wpdb->posts}" );
// Error: The query argument of wpdb::prepare() must have a placeholder

// ✅ CORRECT - Don't use prepare() if no dynamic data
$wpdb->get_results( "SELECT * FROM {$wpdb->posts}" );

// ✅ CORRECT - Use prepare() for dynamic data
$wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID = %d",
    $post_id
) );
```

**Additional wpdb::prepare() Mistakes**:

1. **Percentage Sign Handling**:
```php
// ❌ WRONG
$wpdb->prepare( "SELECT * FROM {$wpdb->posts} WHERE post_title LIKE '%test%'" );

// ✅ CORRECT
$search = '%' . $wpdb->esc_like( $term ) . '%';
$wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_title LIKE %s",
    $search
) );
```

2. **Mixing Argument Formats**:
```php
// ❌ WRONG - Can't mix individual args and array
$wpdb->prepare( "... WHERE id = %d AND name = %s", $id, array( $name ) );

// ✅ CORRECT - Pick one format
$wpdb->prepare( "... WHERE id = %d AND name = %s", $id, $name );
// OR
$wpdb->prepare( "... WHERE id = %d AND name = %s", array( $id, $name ) );
```

---

## Plugin Architecture Patterns

### Simple (Functions Only)
Small plugins (<5 functions):
```php
function mypl_init() { /* code */ }
add_action( 'init', 'mypl_init' );
```

### OOP (Singleton)
Medium plugins:
```php
class MyPL_Plugin {
    private static $instance = null;
    public static function get_instance() {
        if ( null === self::$instance ) self::$instance = new self();
        return self::$instance;
    }
    private function __construct() {
        add_action( 'init', array( $this, 'init' ) );
    }
}
MyPL_Plugin::get_instance();
```

### PSR-4 (Modern, Recommended 2025+)
Large/team plugins:
```
my-plugin/
├── my-plugin.php
├── composer.json → "psr-4": { "MyPlugin\\": "src/" }
└── src/Admin.php

// my-plugin.php
require_once __DIR__ . '/vendor/autoload.php';
use MyPlugin\Admin;
new Admin();
```

---

## Common Patterns

**Custom Post Types** (CRITICAL: Flush rewrite rules on activation, show_in_rest for block editor):
```php
// show_in_rest => true REQUIRED for Gutenberg block editor
register_post_type( 'book', array(
    'public' => true,
    'show_in_rest' => true,  // Without this, block editor won't work!
    'supports' => array( 'editor', 'title' ),
) );
register_activation_hook( __FILE__, function() {
    mypl_register_cpt();
    flush_rewrite_rules();  // NEVER call on every page load
} );
```

**Custom Taxonomies**:
```php
register_taxonomy( 'genre', 'book', array( 'hierarchical' => true, 'show_in_rest' => true ) );
```

**Meta Boxes**:
```php
add_meta_box( 'book_details', 'Book Details', 'mypl_meta_box_html', 'book' );
// Save: Check nonce, DOING_AUTOSAVE, current_user_can('edit_post')
update_post_meta( $post_id, '_book_isbn', sanitize_text_field( $_POST['book_isbn'] ) );
```

**Settings API**:
```php
register_setting( 'mypl_options', 'mypl_api_key', array( 'sanitize_callback' => 'sanitize_text_field' ) );
add_settings_section( 'mypl_section', 'API Settings', 'callback', 'my-plugin' );
add_settings_field( 'mypl_api_key', 'API Key', 'field_callback', 'my-plugin', 'mypl_section' );
```

**REST API** (10x faster than admin-ajax.php):
```php
register_rest_route( 'myplugin/v1', '/data', array(
    'methods'             => 'POST',
    'callback'            => 'mypl_rest_callback',
    'permission_callback' => fn() => current_user_can( 'edit_posts' ),
) );
```

**AJAX** (Legacy, use REST API for new projects):
```php
add_action( 'wp_ajax_mypl_action', 'mypl_ajax_handler' );
check_ajax_referer( 'mypl-ajax-nonce', 'nonce' );
wp_send_json_success( array( 'message' => 'Success' ) );
```

**Custom Tables**:
```php
global $wpdb;
$sql = "CREATE TABLE {$wpdb->prefix}mypl_data (id bigint AUTO_INCREMENT PRIMARY KEY, ...)";
require_once ABSPATH . 'wp-admin/includes/upgrade.php';
dbDelta( $sql );
```

**Transients** (Caching):
```php
$data = get_transient( 'mypl_data' );
if ( false === $data ) {
    $data = expensive_operation();
    set_transient( 'mypl_data', $data, 12 * HOUR_IN_SECONDS );
}
```

---

## Bundled Resources

**Templates**: `plugin-simple/`, `plugin-oop/`, `plugin-psr4/`, `examples/meta-box.php`, `examples/settings-page.php`, `examples/custom-post-type.php`, `examples/rest-endpoint.php`, `examples/ajax-handler.php`

**Scripts**: `scaffold-plugin.sh`, `check-security.sh`, `validate-headers.sh`

**References**: `security-checklist.md`, `hooks-reference.md`, `sanitization-guide.md`, `wpdb-patterns.md`, `common-errors.md`

---

## Advanced Topics

**i18n** (Internationalization):
```php
load_plugin_textdomain( 'my-plugin', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );
__( 'Text', 'my-plugin' );  // Return translated
_e( 'Text', 'my-plugin' );  // Echo translated
esc_html__( 'Text', 'my-plugin' );  // Translate + escape
```

**WP-CLI**:
```php
if ( defined( 'WP_CLI' ) && WP_CLI ) {
    WP_CLI::add_command( 'mypl', 'MyPL_CLI_Command' );
}
```

**Cron Events**:
```php
register_activation_hook( __FILE__, fn() => wp_schedule_event( time(), 'daily', 'mypl_daily_task' ) );
register_deactivation_hook( __FILE__, fn() => wp_clear_scheduled_hook( 'mypl_daily_task' ) );
add_action( 'mypl_daily_task', 'mypl_do_daily_task' );
```

**Plugin Dependencies**:
```php
if ( ! class_exists( 'WooCommerce' ) ) {
    deactivate_plugins( plugin_basename( __FILE__ ) );
    add_action( 'admin_notices', fn() => echo '<div class="error"><p>Requires WooCommerce</p></div>' );
}
```

---

## Distribution & Auto-Updates

**GitHub Auto-Updates** (Plugin Update Checker by YahnisElsts):
```php
// 1. Install: git submodule add https://github.com/YahnisElsts/plugin-update-checker.git
// 2. Add to main plugin file
require plugin_dir_path( __FILE__ ) . 'plugin-update-checker/plugin-update-checker.php';
use YahnisElsts\PluginUpdateChecker\v5\PucFactory;

$updateChecker = PucFactory::buildUpdateChecker(
    'https://github.com/yourusername/your-plugin/',
    __FILE__,
    'your-plugin-slug'
);
$updateChecker->getVcsApi()->enableReleaseAssets();  // Use GitHub Releases

// Private repos: Define token in wp-config.php
if ( defined( 'YOUR_PLUGIN_GITHUB_TOKEN' ) ) {
    $updateChecker->setAuthentication( YOUR_PLUGIN_GITHUB_TOKEN );
}
```

**Deployment**:
```bash
git tag 1.0.1 && git push origin main && git push origin 1.0.1
# Create GitHub Release with ZIP (exclude .git, tests)
```

**Alternatives**: Git Updater (no coding), Custom Update Server (full control), Freemius (commercial)

**Security**: Use HTTPS, never hardcode tokens, validate licenses, rate limit update checks

**CRITICAL**: ZIP must contain plugin folder: `plugin.zip/my-plugin/my-plugin.php`

**Resources**: See `references/github-auto-updates.md`, `examples/github-updater.php`

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

**Fatal Error**: Enable WP_DEBUG, check wp-content/debug.log, verify prefixed names, check dependencies

**404 on CPT**: Flush rewrite rules via Settings → Permalinks → Save

**Nonce Fails**: Check nonce name/action match, verify not expired (24h default)

**AJAX Returns 0/-1**: Verify action name matches `wp_ajax_{action}`, check nonce sent/verified

**HTML Stripped**: Use `wp_kses_post()` not `sanitize_text_field()` for safe HTML

**Query Fails**: Use `$wpdb->prepare()`, check `$wpdb->prefix`, verify syntax

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

1. Check `references/common-errors.md` for extended troubleshooting
2. Verify all steps in the security foundation
3. Check official docs: https://developer.wordpress.org/plugins/
4. Enable WP_DEBUG and check debug.log
5. Use Query Monitor plugin to debug hooks and queries

---

**Last verified**: 2026-01-21 | **Skill version**: 2.0.0 | **Changes**: Added 9 new issues from WordPress 6.7-6.9 research (bcrypt migration, WP_Dependencies deprecation, translation loading, REST API CVEs 2025-2026, wpdb::prepare() edge cases, nonce limitations, hook gotchas, CPT URL conflicts). Updated from 20 to 29 documented errors prevented. Error count: 20 → 29. Version: 1.x → 2.0.0 (major version due to significant WordPress version-specific content additions).
