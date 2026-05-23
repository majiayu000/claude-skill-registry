---
name: php-standards
description: PHP coding standards for Oh My Brand! theme. WordPress Coding Standards, strict typing, escaping, sanitization, DocBlocks, and security practices. Use when writing PHP functions, classes, or render templates.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# PHP Standards

PHP coding standards and security practices for the Oh My Brand! WordPress FSE theme.

---

## When to Use

- Writing new PHP functions, classes, or methods
- Creating block render templates (`render.php`)
- Building helper functions (`helpers.php`)
- Working with WordPress hooks and filters
- Handling user input or output

---

## Reference Files

| File | Purpose |
|------|---------|
| [file-structure.php](references/file-structure.php) | File and class structure |
| [escaping-examples.php](references/escaping-examples.php) | Output escaping patterns |
| [sanitization-examples.php](references/sanitization-examples.php) | Input sanitization |
| [nonce-examples.php](references/nonce-examples.php) | Nonce verification |
| [hooks-examples.php](references/hooks-examples.php) | Actions and filters |

---

## File Header

Every PHP file must include:

```php
<?php
/**
 * Short description of the file.
 *
 * @package theme-oh-my-brand
 */

declare(strict_types=1);
```

See [file-structure.php](references/file-structure.php) for complete structure.

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `GalleryBlock` |
| Functions | snake_case with prefix | `omb_get_gallery_images()` |
| Methods | snake_case | `get_images()` |
| Variables | snake_case | `$gallery_images` |
| Constants | SCREAMING_SNAKE | `OMB_VERSION` |
| Files | kebab-case | `gallery-block.php` |

### Function Prefix

Use `omb_` prefix for theme functions:

```php
// ✅ Good - prefixed
function omb_register_blocks(): void { }

// ❌ Bad - no prefix
function register_blocks(): void { }
```

---

## Type Declarations

Use type hints for all function parameters and return types:

```php
function format_gallery_images(array $images, int $limit = 10): array {
    // Implementation
}
```

### Common Type Patterns

| Type | Usage |
|------|-------|
| `string` | Text values |
| `int` | Integer numbers |
| `float` | Decimal numbers |
| `bool` | Boolean values |
| `array` | Arrays (use PHPDoc for element types) |
| `?string` | Nullable string |
| `void` | No return value |

---

## Output Escaping

**All output must be escaped** based on context:

| Function | Use Case |
|----------|----------|
| `esc_html()` | Text content |
| `esc_attr()` | HTML attributes |
| `esc_url()` | URLs |
| `wp_kses_post()` | Rich HTML content |
| `wp_json_encode()` | JavaScript values |
| `esc_html__()` | Translated text |
| `esc_attr__()` | Translated attributes |

See [escaping-examples.php](references/escaping-examples.php) for examples.

---

## Input Sanitization

Sanitize all input data before use:

| Function | Use Case |
|----------|----------|
| `sanitize_text_field()` | Text input |
| `sanitize_textarea_field()` | Textarea |
| `sanitize_email()` | Email |
| `absint()` | Integer |
| `esc_url_raw()` | URL for database |
| `sanitize_file_name()` | File name |
| `sanitize_html_class()` | HTML class |

See [sanitization-examples.php](references/sanitization-examples.php) for examples.

---

## Nonce Verification

Use nonces for form submissions and AJAX:

| Function | Purpose |
|----------|---------|
| `wp_nonce_field()` | Add nonce to form |
| `wp_create_nonce()` | Create nonce for AJAX |
| `wp_verify_nonce()` | Verify form nonce |
| `check_ajax_referer()` | Verify AJAX nonce |

See [nonce-examples.php](references/nonce-examples.php) for examples.

---

## WordPress Hooks

| Hook Type | Function | Custom Hook |
|-----------|----------|-------------|
| Actions | `add_action()` | `do_action()` |
| Filters | `add_filter()` | `apply_filters()` |

### Common Actions

```php
add_action('init', 'omb_register_blocks');
add_action('wp_enqueue_scripts', 'omb_enqueue_assets');
add_action('after_setup_theme', 'omb_setup_theme');
```

### Hook Priority

```php
add_action('init', 'omb_early_init', 5);    // Earlier
add_action('init', 'omb_normal_init');       // Default: 10
add_action('init', 'omb_late_init', 20);     // Later
```

See [hooks-examples.php](references/hooks-examples.php) for examples.

---

## Error Handling

Use early returns and guard clauses:

```php
function omb_get_gallery_html(int $gallery_id): string {
    if ($gallery_id <= 0) {
        return '';
    }

    $gallery = get_post($gallery_id);

    if (!$gallery instanceof WP_Post) {
        return '';
    }

    return omb_render_gallery($gallery);
}
```

---

## Related Skills

- [html-standards](../html-standards/SKILL.md) - Semantic HTML and accessibility
- [css-standards](../css-standards/SKILL.md) - BEM naming and styling
- [phpunit-testing](../phpunit-testing/SKILL.md) - PHP unit testing
- [native-block-development](../native-block-development/SKILL.md) - Block render templates

---

## References

- [WordPress PHP Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/php/)
- [WordPress Data Validation](https://developer.wordpress.org/plugins/security/data-validation/)
- [WordPress Nonces](https://developer.wordpress.org/plugins/security/nonces/)
