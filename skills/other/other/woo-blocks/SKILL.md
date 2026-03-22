---
name: woo-blocks
description: Build WooCommerce Blocks — Gutenberg block integration, block-based cart/checkout extensions, Store API, and the @woocommerce/blocks-checkout package. Use when extending the block editor for WooCommerce or customizing block-based checkout/cart.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WooCommerce Blocks Development

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.woocommerce.com blocks extensibility` for blocks extension docs
2. Fetch `https://developer.wordpress.org/block-editor/` for Block Editor handbook
3. Web-search `woocommerce checkout blocks extension api` for checkout extension patterns

## Architecture Overview

### What WooCommerce Blocks Are

React-based blocks for the WordPress block editor (Gutenberg):
- **Cart Block** — replaces `[woocommerce_cart]` shortcode
- **Checkout Block** — replaces `[woocommerce_checkout]` shortcode (default since WC 8.3)
- **Product Blocks** — grids, filters, search, featured products
- **Mini Cart Block** — header cart widget

### Store API

A dedicated REST API powering the block-based cart and checkout:
- Base: `/wp-json/wc/store/v1/`
- Endpoints: `cart`, `cart/items`, `checkout`, `products`, `batch`
- Nonce-authenticated (no API keys needed — runs in the customer's session)
- Separate from the WooCommerce REST API v3 (which is admin-facing)

### Key Packages

| Package | Purpose |
|---------|---------|
| `@woocommerce/blocks-checkout` | Checkout extension API |
| `@woocommerce/blocks-registry` | Block type registration |
| `@woocommerce/blocks-components` | Shared React components |
| `@woocommerce/settings` | Access WC settings in JS |
| `@wordpress/blocks` | Core block registration |
| `@wordpress/block-editor` | Editor components |
| `@wordpress/element` | React wrapper |

## Extending Checkout Blocks

### Integration Points

The block-based checkout provides extension points:
- **Inner Blocks** — add custom blocks within checkout layout
- **Slot Fills** — inject content into predefined areas (before/after payment, shipping, etc.)
- **Filters** — modify text, labels, and data displayed in checkout
- **Store API extensions** — add custom data to cart/checkout API responses

### Checkout Extension API (PHP Side)

Use `ExtendSchema` and `StoreApi` classes to:
1. Extend the Store API response with custom data
2. Add custom endpoint data to cart items, shipping, or checkout
3. Process custom data during checkout via `ExtendSchema::register_endpoint_data()`

### Checkout Extension API (JS Side)

Use `@woocommerce/blocks-checkout` exports:
- `registerCheckoutFilters` — modify displayed values (item names, prices, subtotals)
- `ExperimentalOrderMeta` — slot for adding custom order meta display
- `ExperimentalDiscountsMeta` — slot for custom discount display

### Registering a Checkout Block

1. Register the block server-side with `register_block_type()`
2. Declare the block as a checkout inner block via `BlockRegistry`
3. Provide `edit` and `save` React components
4. Enqueue scripts for the frontend and editor

## Building Custom Product Blocks

### Block Registration

Register with `register_block_type()`:
- `block.json` — metadata file defining name, attributes, supports, editor/frontend scripts
- `edit.js` — editor component
- `save.js` — save component (or `null` for dynamic)
- `render.php` — server-side rendering for dynamic blocks

### Server-Side Rendering

Use dynamic blocks with `render_callback` or `render.php` for product data:
- Access WooCommerce data via PHP (products, cart, etc.)
- Return HTML string from the render function
- Preferred for data-dependent blocks

## Store API Extension

### Adding Custom Data to Cart/Checkout

Register custom data via `woocommerce_blocks_loaded` action:
- Use `Automattic\WooCommerce\StoreApi\Schemas\ExtendSchema`
- Define namespace, schema, and data callback
- Data appears in Store API responses under `extensions.{namespace}`

### Processing Custom Checkout Data

Register `checkout_data` processing via `woocommerce_store_api_checkout_update_order_from_request`:
- Receives the order and the full checkout request
- Save custom data to order meta

## Declaring Block Compatibility

```php
add_action( 'before_woocommerce_init', function() {
    if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
        \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
            'cart_checkout_blocks', __FILE__, true
        );
    }
});
```

## Best Practices

- Declare `cart_checkout_blocks` compatibility in every extension
- Use the Store API (not REST API v3) for frontend/cart/checkout interactions
- Use `@woocommerce/blocks-checkout` hooks rather than DOM manipulation
- Enqueue block scripts only when the block is present on the page
- Follow Gutenberg coding standards for block development
- Test with both classic and block-based checkout
- Use `block.json` for block metadata (WordPress standard)

Fetch the WooCommerce Blocks extension docs and Block Editor handbook for exact API methods, slot names, and filter signatures before implementing.
