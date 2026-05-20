---
name: wordpress
description: |
  WordPress framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with WordPress projects, or when the user mentions WordPress.
  Provides theme development, plugin architecture, REST API, blocks, and security guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: php
  extensions: ".php"
---

# WordPress Framework Guide

> Applies to: WordPress 6.0+, PHP 8.0+, Plugin Development, Theme Development, REST API, Block Editor (Gutenberg)
> Language Guide: @.claude/skills/php-guide/SKILL.md

## Overview

WordPress is a content management system (CMS) powering over 40% of the web. This guide covers modern WordPress development including plugin architecture, theme development, REST API endpoints, the Block Editor (Gutenberg), and security essentials.

**Use WordPress when:**
- Content management system is needed
- Blog or publishing platform
- E-commerce with WooCommerce
- Custom applications with familiar admin UI
- Rapid prototyping with existing ecosystem

**Consider alternatives when:**
- Building pure API backend (use Laravel/Symfony)
- High-performance requirements (consider headless)
- Complex business logic applications
- Microservices architecture

## Guardrails

### WordPress-Specific Rules

- Use `declare(strict_types=1)` in all PHP files
- Prevent direct file access: `if (!defined('ABSPATH')) { exit; }`
- Use namespaces for all plugin/theme classes
- Escape all output: `esc_html()`, `esc_attr()`, `esc_url()`, `wp_kses_post()`
- Sanitize all input: `sanitize_text_field()`, `sanitize_email()`, `absint()`
- Verify nonces on all form submissions and AJAX requests
- Check capabilities before performing actions: `current_user_can()`
- Use `$wpdb->prepare()` for all database queries (never concatenate)
- Register all scripts/styles through `wp_enqueue_scripts` hook
- Use text domains and `__()` / `_e()` for all user-facing strings
- Set `show_in_rest => true` for post types and taxonomies that need Gutenberg/REST support
- Use `register_post_meta()` to expose meta fields in the REST API
- Always include `uninstall.php` or `register_uninstall_hook()` for cleanup

### Anti-Patterns

- Do not use `query_posts()` (use `WP_Query` or `get_posts()`)
- Do not modify core files (use hooks and filters)
- Do not hardcode URLs (use `home_url()`, `admin_url()`, `plugin_dir_url()`)
- Do not store business logic in template files
- Do not skip nonce verification on any form or AJAX handler
- Do not use `extract()` on untrusted data
- Do not echo unsanitized user input
- Do not use `$_GET`/`$_POST` directly without sanitization

## Project Structure

### Plugin Structure

```
my-plugin/
├── my-plugin.php              # Main plugin file (header, constants, bootstrap)
├── includes/
│   ├── class-plugin.php       # Main plugin class (singleton)
│   ├── class-activator.php    # Activation hooks
│   ├── class-deactivator.php  # Deactivation hooks
│   ├── admin/
│   │   ├── class-admin.php    # Admin functionality
│   │   └── partials/          # Admin templates
│   ├── public/
│   │   ├── class-public.php   # Public functionality
│   │   └── partials/          # Public templates
│   ├── api/
│   │   └── class-rest-api.php # REST API endpoints
│   └── blocks/
│       └── my-block/          # Gutenberg blocks
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
├── languages/                 # Translation files (.pot, .po, .mo)
├── templates/                 # Overridable template files
├── tests/phpunit/
├── composer.json
├── package.json
└── readme.txt                 # WordPress.org readme
```

### Theme Structure

```
my-theme/
├── style.css                  # Theme metadata (required)
├── functions.php              # Theme setup and hooks
├── index.php                  # Fallback template (required)
├── header.php / footer.php    # Header/footer templates
├── single.php / page.php      # Single post / page templates
├── archive.php / 404.php      # Archive / error templates
├── search.php / sidebar.php   # Search / sidebar templates
├── inc/                       # Customizer, template functions, hooks
├── template-parts/            # Reusable content partials
├── assets/                    # CSS, JS, images
├── parts/                     # Template parts (FSE)
├── patterns/                  # Block patterns
├── templates/                 # Block templates (FSE)
└── theme.json                 # Theme configuration (FSE)
```

## Template Hierarchy

WordPress resolves templates from most specific to least specific. Pattern: `{type}-{slug}.php -> {type}-{id}.php -> {type}.php -> index.php`

- **Single**: `single-{post-type}-{slug}` -> `single-{post-type}` -> `single` -> `singular` -> `index`
- **Page**: `page-{slug}` -> `page-{id}` -> `page` -> `singular` -> `index`
- **Archive**: `archive-{post-type}` -> `archive` -> `index`
- **Category**: `category-{slug}` -> `category-{id}` -> `category` -> `archive` -> `index`
- **Taxonomy**: `taxonomy-{tax}-{term}` -> `taxonomy-{tax}` -> `taxonomy` -> `archive`
- **Search/404**: `search.php` / `404.php` -> `index.php`

## Plugin Basics

### Main Plugin File

```php
<?php
/**
 * Plugin Name: My Plugin
 * Plugin URI: https://example.com/my-plugin
 * Description: A modern WordPress plugin
 * Version: 1.0.0
 * Requires at least: 6.0
 * Requires PHP: 8.0
 * Author: Your Name
 * Text Domain: my-plugin
 * Domain Path: /languages
 */

declare(strict_types=1);

namespace MyPlugin;

if (!defined('ABSPATH')) {
    exit;
}

define('MY_PLUGIN_VERSION', '1.0.0');
define('MY_PLUGIN_PATH', plugin_dir_path(__FILE__));
define('MY_PLUGIN_URL', plugin_dir_url(__FILE__));
define('MY_PLUGIN_BASENAME', plugin_basename(__FILE__));

require_once MY_PLUGIN_PATH . 'vendor/autoload.php';

register_activation_hook(__FILE__, [Activator::class, 'activate']);
register_deactivation_hook(__FILE__, [Deactivator::class, 'deactivate']);

add_action('plugins_loaded', function (): void {
    Plugin::getInstance()->init();
});
```

### Singleton Plugin Class

```php
<?php
declare(strict_types=1);

namespace MyPlugin;

final class Plugin
{
    private static ?self $instance = null;

    public static function getInstance(): self
    {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {}

    public function init(): void
    {
        load_plugin_textdomain('my-plugin', false, dirname(MY_PLUGIN_BASENAME) . '/languages');

        if (is_admin()) {
            new Admin\Admin();
        }

        new Frontend\Frontend();
        new Api\RestApi();
        new Blocks\BlockManager();
    }
}
```

## Hooks and Filters

### Common Hook Patterns

```php
// Actions (do something at a specific point)
add_action('init', [$this, 'registerPostTypes']);
add_action('wp_enqueue_scripts', [$this, 'enqueueAssets']);
add_action('admin_enqueue_scripts', [$this, 'enqueueAdminAssets']);
add_action('save_post', [$this, 'onSavePost'], 10, 3);
add_action('wp_ajax_my_action', [$this, 'handleAjax']);
add_action('wp_ajax_nopriv_my_action', [$this, 'handleAjax']);
add_action('rest_api_init', [$this, 'registerRoutes']);

// Filters (modify data and return it)
add_filter('the_content', [$this, 'filterContent']);
add_filter('the_title', [$this, 'filterTitle'], 10, 2);
add_filter('excerpt_length', fn() => 30);
add_filter('post_class', [$this, 'addPostClasses'], 10, 3);

// Custom hooks (for extensibility)
do_action('my_plugin_after_save', $postId, $data);
$value = apply_filters('my_plugin_format_price', $price, $currency);
```

### Asset Enqueuing

```php
public function enqueueAssets(): void
{
    wp_enqueue_style('my-plugin-style', MY_PLUGIN_URL . 'assets/css/public.css', [], MY_PLUGIN_VERSION);

    wp_enqueue_script('my-plugin-script', MY_PLUGIN_URL . 'assets/js/public.js', ['jquery'], MY_PLUGIN_VERSION, true);

    wp_localize_script('my-plugin-script', 'MyPluginData', [
        'ajaxUrl' => admin_url('admin-ajax.php'),
        'nonce'   => wp_create_nonce('my_plugin_nonce'),
        'strings' => [
            'loading' => __('Loading...', 'my-plugin'),
            'error'   => __('An error occurred.', 'my-plugin'),
        ],
    ]);
}
```

## REST API

### Custom Endpoint Pattern

```php
<?php
declare(strict_types=1);

namespace MyPlugin\Api;

use WP_REST_Controller;
use WP_REST_Request;
use WP_REST_Response;
use WP_REST_Server;
use WP_Error;

final class BooksController extends WP_REST_Controller
{
    protected $namespace = 'my-plugin/v1';
    protected $rest_base = 'books';

    public function registerRoutes(): void
    {
        register_rest_route($this->namespace, '/' . $this->rest_base, [
            [
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => [$this, 'getItems'],
                'permission_callback' => [$this, 'getItemsPermissions'],
                'args'                => $this->getCollectionParams(),
            ],
            [
                'methods'             => WP_REST_Server::CREATABLE,
                'callback'            => [$this, 'createItem'],
                'permission_callback' => [$this, 'createItemPermissions'],
            ],
        ]);
    }

    public function getItems(WP_REST_Request $request): WP_REST_Response
    {
        $query = new \WP_Query([
            'post_type'      => 'book',
            'posts_per_page' => $request->get_param('per_page') ?? 10,
            'paged'          => $request->get_param('page') ?? 1,
        ]);

        $items = array_map(fn($post) => $this->formatItem($post), $query->posts);
        $response = new WP_REST_Response($items, 200);
        $response->header('X-WP-Total', $query->found_posts);
        $response->header('X-WP-TotalPages', $query->max_num_pages);

        return $response;
    }

    public function getItemsPermissions(): bool { return true; }
    public function createItemPermissions(): bool { return current_user_can('publish_posts'); }
}
```

**REST API conventions:**
- Extend `WP_REST_Controller` for full CRUD endpoints
- Always define `permission_callback` (use `__return_true` for truly public)
- Sanitize input parameters with `sanitize_callback` in `args`
- Return `WP_Error` for error responses with proper status codes
- Use pagination headers: `X-WP-Total`, `X-WP-TotalPages`
- Version your namespace: `my-plugin/v1`

## Block Editor (Gutenberg)

### Block Registration (PHP)

```php
// Register from block.json (preferred)
register_block_type(MY_PLUGIN_PATH . 'blocks/my-block');

// Dynamic block with server render
register_block_type('my-plugin/featured-items', [
    'render_callback' => [$this, 'renderFeaturedItems'],
    'attributes'      => [
        'count' => ['type' => 'number', 'default' => 3],
    ],
]);
```

### block.json

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "my-plugin/my-block",
    "version": "1.0.0",
    "title": "My Block",
    "category": "widgets",
    "icon": "admin-generic",
    "supports": {
        "html": false,
        "align": ["wide", "full"],
        "color": { "background": true, "text": true },
        "spacing": { "margin": true, "padding": true }
    },
    "attributes": {
        "content": { "type": "string", "default": "" }
    },
    "textdomain": "my-plugin",
    "editorScript": "file:./index.js",
    "editorStyle": "file:./index.css",
    "style": "file:./style-index.css",
    "render": "file:./render.php"
}
```

### Block JavaScript (index.js)

```javascript
import { registerBlockType } from '@wordpress/blocks';
import { useBlockProps, InspectorControls } from '@wordpress/block-editor';
import { PanelBody, ToggleControl } from '@wordpress/components';
import { __ } from '@wordpress/i18n';
import ServerSideRender from '@wordpress/server-side-render';

registerBlockType('my-plugin/my-block', {
    edit: ({ attributes, setAttributes }) => {
        const blockProps = useBlockProps();
        return (
            <>
                <InspectorControls>
                    <PanelBody title={__('Settings', 'my-plugin')}>
                        <ToggleControl
                            label={__('Show Image', 'my-plugin')}
                            checked={attributes.showImage}
                            onChange={(val) => setAttributes({ showImage: val })}
                        />
                    </PanelBody>
                </InspectorControls>
                <div {...blockProps}>
                    <ServerSideRender block="my-plugin/my-block" attributes={attributes} />
                </div>
            </>
        );
    },
    save: () => null, // Dynamic block: rendered server-side
});
```

## Security Essentials

### Input Sanitization

```php
$title    = sanitize_text_field($_POST['title']);
$email    = sanitize_email($_POST['email']);
$url      = esc_url_raw($_POST['url']);
$content  = wp_kses_post($_POST['content']);
$filename = sanitize_file_name($_POST['filename']);
$key      = sanitize_key($_POST['key']);
$int      = absint($_POST['number']);
```

### Output Escaping

```php
echo esc_html($title);       // HTML context
echo esc_attr($attribute);   // Attribute context
echo esc_url($url);          // URL context
echo esc_js($script);        // JS context
echo wp_kses_post($content); // Allow safe HTML
```

### Nonce Verification

```php
// Generate nonce field in form
wp_nonce_field('my_action', 'my_nonce');

// Verify nonce on submission
if (!wp_verify_nonce($_POST['my_nonce'], 'my_action')) {
    wp_die(__('Security check failed.', 'my-plugin'));
}

// AJAX nonce check
check_ajax_referer('my_plugin_nonce', 'nonce');
```

### Capability Checks

```php
if (!current_user_can('edit_posts')) {
    wp_die(__('Insufficient permissions.', 'my-plugin'));
}

// REST API permission callback
'permission_callback' => fn() => current_user_can('edit_post', $id)
```

## Commands Reference

```bash
# Development
npm run build                 # Build blocks/assets
npm run start                 # Watch mode for blocks
composer install              # PHP dependencies

# Testing
./vendor/bin/phpunit                         # Run tests
./vendor/bin/phpunit --coverage-html coverage # Coverage report

# Code Quality
./vendor/bin/phpcs               # PHP CodeSniffer (WPCS)
./vendor/bin/phpcbf              # Auto-fix coding standards
./vendor/bin/phpstan analyse     # Static analysis

# WP-CLI essentials
wp plugin activate my-plugin     # Activate plugin
wp plugin list --status=active   # List active plugins
wp theme activate my-theme       # Activate theme
wp db export backup.sql          # Database backup
wp post list --post_type=book    # List posts
wp cache flush                   # Clear object cache
wp transient delete --all        # Clear transients
wp cron event run --all          # Run scheduled events
wp rewrite flush                 # Flush rewrite rules
```

### Custom WP-CLI Command

```php
if (defined('WP_CLI') && WP_CLI) {
    WP_CLI::add_command('mycommand', MyPlugin\CLI\MyCommand::class);
}
```

## Advanced Topics

For detailed patterns and full implementation examples, see:

- [references/patterns.md](references/patterns.md) -- Custom post types, taxonomies, meta boxes, Gutenberg blocks, WooCommerce integration, database operations, testing, caching, performance

## External References

- [WordPress Developer Resources](https://developer.wordpress.org/)
- [Plugin Developer Handbook](https://developer.wordpress.org/plugins/)
- [Theme Developer Handbook](https://developer.wordpress.org/themes/)
- [REST API Handbook](https://developer.wordpress.org/rest-api/)
- [Block Editor Handbook](https://developer.wordpress.org/block-editor/)
- [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/)
- [WP-CLI Documentation](https://developer.wordpress.org/cli/commands/)
