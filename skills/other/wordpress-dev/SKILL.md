---
name: wordpress-dev
description: WordPress development best practices - coding standards, custom post types, security, performance, hooks/filters, and template hierarchy. Use for any WordPress theme or plugin development guidance.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# WordPress Development Best Practices

Comprehensive development guidance for WordPress themes and plugins following 2025 standards.

## What This Skill Provides

1. **Coding Standards** - PHP, JS, CSS conventions following WordPress standards
2. **Custom Post Types** - Complete CPT registration and management guide
3. **Security** - Sanitization, escaping, nonces, capability checks
4. **Performance** - Caching, query optimization, asset loading
5. **Hooks & Filters** - Actions and filters reference with examples
6. **Template Hierarchy** - Theme template structure and overrides

## Quick Reference

### Do's

- Use WordPress APIs (don't reinvent the wheel)
- Sanitize all input (`sanitize_*` functions)
- Escape all output (`esc_*` functions)
- Use prepared statements for SQL (`$wpdb->prepare`)
- Enqueue scripts/styles properly (`wp_enqueue_*`)
- Use transients for expensive operations
- Follow the template hierarchy
- Use hooks instead of modifying core
- Prefix all functions, classes, and global variables
- Use WP-CLI for automation tasks

### Don'ts

- Modify WordPress core files (NEVER)
- Use `query_posts()` - use `WP_Query` instead
- Echo untrusted data without escaping
- Store sensitive data in plain text options
- Use `extract()` on untrusted data
- Suppress errors with `@` operator
- Use deprecated functions
- Hard-code URLs or file paths
- Skip nonce verification on forms
- Use `mysql_*` functions - use `$wpdb`

## Documentation

Detailed documentation available in `/docs/`:

| File | Contents |
|------|----------|
| [coding-standards.md](docs/coding-standards.md) | PHP, JS, CSS naming and formatting |
| [custom-post-types.md](docs/custom-post-types.md) | CPT registration, labels, capabilities |
| [security.md](docs/security.md) | Input/output handling, nonces, SQL safety |
| [performance.md](docs/performance.md) | Caching, optimization, lazy loading |
| [hooks-filters.md](docs/hooks-filters.md) | Common actions/filters with examples |
| [template-hierarchy.md](docs/template-hierarchy.md) | Template files and overrides |

## Code Templates

Ready-to-use templates in `/templates/`:

| Template | Purpose |
|----------|---------|
| `custom-post-type.php` | CPT registration boilerplate |
| `taxonomy.php` | Custom taxonomy registration |
| `meta-box.php` | Admin meta box with save handling |
| `rest-api-endpoint.php` | Custom REST API endpoint |
| `plugin-skeleton/` | Complete plugin starter files |

## Usage Examples

### Create a Custom Post Type

Ask Claude:
- "Create a 'Property' custom post type for real estate"
- "Add a custom post type for team members with a photo field"
- "Register a 'Portfolio' CPT with custom taxonomies"

### Security Review

Ask Claude:
- "Review this form handler for security issues"
- "Check if this plugin follows WordPress security best practices"
- "Add proper sanitization and escaping to this code"

### Performance Optimization

Ask Claude:
- "Optimize this WP_Query for better performance"
- "Add caching to this expensive database operation"
- "Review asset loading for this theme"

## Code Generation

Use the scaffold script to generate boilerplate:

```bash
# Generate a custom post type
python3 /root/.claude/skills/wordpress-dev/scripts/scaffold.py \
  --type cpt \
  --name "Property" \
  --slug "property" \
  --output /path/to/theme/inc/

# Generate a custom taxonomy
python3 /root/.claude/skills/wordpress-dev/scripts/scaffold.py \
  --type taxonomy \
  --name "Property Type" \
  --slug "property-type" \
  --post-type "property" \
  --output /path/to/theme/inc/
```

## WordPress 6.x / Block Theme Notes

### Full Site Editing (FSE)

For block themes (WordPress 6.0+):

```
theme/
├── theme.json          # Global styles and settings
├── templates/          # Block templates (HTML)
│   ├── index.html
│   ├── single.html
│   └── page.html
├── parts/              # Block template parts
│   ├── header.html
│   └── footer.html
└── patterns/           # Block patterns
    └── hero.php
```

### theme.json Best Practices

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 2,
  "settings": {
    "color": {
      "palette": [
        {"slug": "primary", "color": "#1a1a1a", "name": "Primary"}
      ]
    },
    "typography": {
      "fontFamilies": [
        {"fontFamily": "Inter, sans-serif", "slug": "body", "name": "Body"}
      ]
    },
    "spacing": {
      "units": ["px", "rem", "%"]
    }
  }
}
```

## Common Patterns

### Safe Database Query

```php
global $wpdb;
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_type = %s AND post_status = %s",
        'property',
        'publish'
    )
);
```

### AJAX Handler

```php
// Register AJAX action
add_action('wp_ajax_my_action', 'my_ajax_handler');
add_action('wp_ajax_nopriv_my_action', 'my_ajax_handler');

function my_ajax_handler() {
    // Verify nonce
    check_ajax_referer('my_nonce', 'security');

    // Check capability
    if (!current_user_can('edit_posts')) {
        wp_send_json_error('Unauthorized', 403);
    }

    // Sanitize input
    $data = sanitize_text_field($_POST['data']);

    // Process and respond
    wp_send_json_success(['message' => 'Done']);
}
```

### Enqueue Scripts Properly

```php
function theme_enqueue_assets() {
    // CSS
    wp_enqueue_style(
        'theme-style',
        get_stylesheet_uri(),
        [],
        filemtime(get_stylesheet_directory() . '/style.css')
    );

    // JS with dependencies
    wp_enqueue_script(
        'theme-main',
        get_theme_file_uri('/assets/js/main.js'),
        ['jquery'],
        filemtime(get_theme_file_path('/assets/js/main.js')),
        true // In footer
    );

    // Localize for AJAX
    wp_localize_script('theme-main', 'themeData', [
        'ajaxUrl' => admin_url('admin-ajax.php'),
        'nonce'   => wp_create_nonce('theme_nonce'),
    ]);
}
add_action('wp_enqueue_scripts', 'theme_enqueue_assets');
```

## Related Skills

- **wordpress-admin**: Page/post management, WP-CLI, REST API
- **seo-optimizer**: Yoast/Rank Math audit and optimization
- **visual-qa**: Screenshot testing with animation handling
- **brand-guide**: Brand documentation generation

## Resources

- [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/)
- [Theme Developer Handbook](https://developer.wordpress.org/themes/)
- [Plugin Developer Handbook](https://developer.wordpress.org/plugins/)
- [Block Editor Handbook](https://developer.wordpress.org/block-editor/)
- [REST API Handbook](https://developer.wordpress.org/rest-api/)
