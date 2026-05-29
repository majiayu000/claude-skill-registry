---
name: woo-frontend
description: Customize WooCommerce frontend — template overrides, theme integration, shortcodes, hooks for product/cart/checkout display, and WooCommerce block themes. Use when modifying the storefront appearance or building WooCommerce themes.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Frontend & Template Customization

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com template structure` for template hierarchy
2. Web-search `site:developer.wordpress.org themes` for WordPress Theme Handbook
3. Web-search `woocommerce template override guide` for override patterns

## Template System

### How Templates Work

WooCommerce uses a template override system:
- Core templates live in `woocommerce/templates/` within the plugin
- Themes override by copying to `{theme}/woocommerce/{template-path}`
- `wc_get_template()` and `wc_get_template_part()` handle the lookup chain

### Template Lookup Order

1. `{child-theme}/woocommerce/{template}.php`
2. `{parent-theme}/woocommerce/{template}.php`
3. `woocommerce/templates/{template}.php` (plugin default)

### Key Template Files

| Template | Path | Purpose |
|----------|------|---------|
| Single product | `content-single-product.php` | Product page layout |
| Product archive | `archive-product.php` | Shop/category page |
| Product loop item | `content-product.php` | Product card in loop |
| Cart | `cart/cart.php` | Cart page |
| Checkout | `checkout/form-checkout.php` | Checkout form |
| My Account | `myaccount/my-account.php` | Customer account |
| Emails | `emails/*.php` | Transactional emails |

### Template Parts

`wc_get_template_part( 'content', 'product' )` loads `content-product.php` — used for reusable template fragments.

## Template Hooks

### Product Page Hooks (Sequence)

```
woocommerce_before_single_product
  woocommerce_before_single_product_summary
    (product image/gallery)
  woocommerce_single_product_summary
    woocommerce_template_single_title         (5)
    woocommerce_template_single_rating        (10)
    woocommerce_template_single_price         (10)
    woocommerce_template_single_excerpt       (20)
    woocommerce_template_single_add_to_cart   (30)
    woocommerce_template_single_meta          (40)
    woocommerce_template_single_sharing       (50)
  woocommerce_after_single_product_summary
    woocommerce_output_product_data_tabs      (10)
    woocommerce_upsell_display                (15)
    woocommerce_output_related_products       (20)
woocommerce_after_single_product
```

### Shop/Archive Hooks

```
woocommerce_before_shop_loop
woocommerce_before_shop_loop_item
  woocommerce_before_shop_loop_item_title
  woocommerce_shop_loop_item_title
  woocommerce_after_shop_loop_item_title
woocommerce_after_shop_loop_item
woocommerce_after_shop_loop
```

## Enqueuing Assets

### CSS

Enqueue via `wp_enqueue_scripts` action:
- `wp_enqueue_style( 'handle', plugin_dir_url(__FILE__) . 'assets/css/style.css', [], '1.0.0' )`
- Conditional loading: wrap in `is_product()`, `is_cart()`, `is_checkout()`, etc.

### JavaScript

- `wp_enqueue_script( 'handle', $url, ['jquery'], '1.0.0', true )`
- Pass data to JS: `wp_localize_script()` or `wp_add_inline_script()`
- Use `wp_enqueue_script` with `strategy => 'defer'` for performance

### WooCommerce Conditional Functions

| Function | Returns true on |
|----------|----------------|
| `is_shop()` | Main shop page |
| `is_product_category()` | Category archive |
| `is_product_tag()` | Tag archive |
| `is_product()` | Single product page |
| `is_cart()` | Cart page |
| `is_checkout()` | Checkout page |
| `is_account_page()` | My Account page |
| `is_woocommerce()` | Any WooCommerce page |

## Theme Integration

### Declaring WooCommerce Support

```php
add_action( 'after_setup_theme', function() {
    add_theme_support( 'woocommerce' );
    add_theme_support( 'wc-product-gallery-zoom' );
    add_theme_support( 'wc-product-gallery-lightbox' );
    add_theme_support( 'wc-product-gallery-slider' );
});
```

### Block Themes (FSE)

Full Site Editing themes use:
- Block templates instead of PHP templates
- `templates/` and `parts/` directories with HTML files
- `theme.json` for global styles and settings
- WooCommerce block patterns for product displays

## Email Templates

### Customizing Emails

- Override templates in `{theme}/woocommerce/emails/`
- Use `woocommerce_email_header` and `woocommerce_email_footer` hooks
- Style with `email-styles.php` template
- Custom email classes extend `WC_Email`

## Best Practices

- Override templates only when hooks are insufficient
- Keep overridden templates up to date with WooCommerce releases (check `@version` tag)
- Use hooks (`add_action` / `add_filter`) over template overrides when possible
- Conditionally load assets only on pages where they're needed
- Use `wc_get_template()` in plugins to make templates overridable by themes
- Escape all dynamic output in templates
- Support block themes by providing block template alternatives

Fetch the WooCommerce template structure docs and theme handbook for exact template paths, hook sequences, and override patterns before implementing.
