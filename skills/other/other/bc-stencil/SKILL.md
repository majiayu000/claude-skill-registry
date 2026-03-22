---
name: bc-stencil
description: Build BigCommerce Stencil themes — Handlebars templates, front matter, theme objects, SCSS, JavaScript modules, config.json, schema.json, and Stencil CLI. Use when creating or customizing BigCommerce storefront themes.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Stencil Theme Development

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.bigcommerce.com/docs/storefront/stencil` for Stencil overview
2. Fetch `https://developer.bigcommerce.com/docs/storefront/stencil/themes/context/object-reference` for theme object reference
3. Web-search `site:developer.bigcommerce.com stencil handlebars helpers` for Handlebars helper reference

## Architecture

### How Stencil Works

Stencil is BigCommerce's server-rendered theme engine:
1. Template files (Handlebars `.html`) define page structure
2. **Front matter** (YAML) at the top of each template declares what data to fetch
3. BigCommerce injects **theme objects** (product, category, cart, settings, etc.) into the template context
4. Handlebars helpers and partials render the data
5. SCSS compiles to CSS, JS bundles with webpack
6. Stencil CLI provides local development with hot reload

### Template Hierarchy

```
templates/
├── layout/
│   ├── base.html              # Master layout — header, footer, body
│   └── empty.html             # Minimal layout (checkout, etc.)
├── pages/
│   ├── home.html              # Homepage
│   ├── product.html           # Product detail page
│   ├── category.html          # Category listing
│   ├── cart.html              # Cart page
│   ├── checkout.html          # Checkout page
│   ├── account/               # Customer account pages
│   └── ...
├── components/
│   ├── common/                # Header, footer, navigation
│   ├── products/              # Product cards, options, gallery
│   ├── cart/                  # Cart items, totals
│   └── ...
└── ...
```

## Front Matter

### What It Does

YAML block at the top of template files that declares data requirements:

```yaml
---
product:
  videos:
    limit: {{theme_settings.product_videos_count}}
  reviews:
    limit: {{theme_settings.product_reviews_count}}
  related_products:
    limit: {{theme_settings.related_products_count}}
  similar_by_views:
    limit: {{theme_settings.similar_by_views_count}}
---
```

### How It Works

- BigCommerce reads the front matter before rendering
- Fetches the specified data from its APIs
- Injects results into the Handlebars template context
- Controls what data is available on each page

### Common Front Matter Resources

- `product` — product details, images, videos, reviews, related products
- `category` — category info, products in category
- `cart` — cart items, totals
- `customer` — logged-in customer data
- `shop_by_brand` — brand listing
- `new_products`, `featured_products`, `top_products` — product collections

## Theme Objects

### Key Objects

| Object | Available On | Contains |
|--------|-------------|----------|
| `product` | Product page | name, price, images, options, variants, description, reviews |
| `category` | Category page | name, description, products, subcategories |
| `cart` | Cart page | items, subtotal, taxes, grand_total |
| `customer` | When logged in | name, email, addresses, orders |
| `settings` | All pages | store name, currency, logo, URLs |
| `theme_settings` | All pages | config.json setting values |
| `breadcrumbs` | Most pages | navigation breadcrumbs |
| `page` | CMS pages | title, content, URL |

### Accessing Data

```handlebars
{{product.title}}
{{product.price.without_tax.formatted}}
{{#each product.images}}
  <img src="{{getImage this 'product_size'}}" alt="{{this.alt}}">
{{/each}}
```

## Handlebars Helpers

### Control Flow

- `{{#if condition}}...{{else}}...{{/if}}` — conditional
- `{{#unless condition}}...{{/unless}}` — inverse conditional
- `{{#each collection}}...{{/each}}` — iteration
- `{{#with object}}...{{/with}}` — context shifting

### BigCommerce Custom Helpers

- `{{getImage image 'size_name'}}` — generate image URL at specific size
- `{{cdn 'path/to/asset'}}` — CDN-prefixed asset URL
- `{{stylesheet 'path/to/css'}}` — include stylesheet
- `{{inject 'variable' value}}` — pass data to JavaScript context
- `{{jsContext}}` — output injected variables as JSON for JS consumption
- `{{lang 'translation_key'}}` — internationalization
- `{{money price}}` — format currency
- `{{truncate text length}}` — truncate string
- `{{any collection}}` — check if collection has items
- `{{all condition1 condition2}}` — logical AND
- `{{compare a '===' b}}` — comparison

### Partials

Include reusable template fragments:
- `{{> components/products/card product}}` — render a partial with context
- `{{> components/common/header}}` — include a component
- Partials live in `templates/components/`

## Styling (SCSS)

### Structure

```
assets/scss/
├── settings/               # Variables, mixins
│   ├── foundation/
│   └── citadel/
├── components/             # Component styles
├── layouts/                # Layout styles
├── tools/                  # Utility mixins
└── theme.scss              # Main entry point
```

### Theme Settings in SCSS

Access `config.json` values: `stencilColor("primary")`, `stencilNumber("font-size")`, `stencilString("font-family")`

## JavaScript

### Module System

Stencil uses webpack for JS bundling:
- ES6 module imports
- Entry point in `assets/js/app.js`
- Page-specific modules loaded conditionally
- jQuery available globally (Cornerstone ships with it)

### Accessing Theme Data in JS

Use `{{inject}}` in templates and `{{jsContext}}` to pass server data to client JS:
```handlebars
{{inject 'productId' product.id}}
<script>{{jsContext}}</script>
```
Access in JS via `this.context` in PageManager subclasses.

### PageManager

Cornerstone's page lifecycle manager:
- Extend `PageManager` for page-specific JS
- `onReady()` — DOM ready, initialize functionality
- Registered per page type in `assets/js/app.js`

## Configuration

### config.json

Theme configuration with settings and variations:
- `settings` — default values for all theme settings
- `variations` — named presets (Light, Bold, Warm, etc.)
- `read_only_files` — files that cannot be edited in Theme Editor

### schema.json

Defines the Theme Editor UI:
- Sections, groups, and fields that appear in the visual editor
- Field types: `color`, `font`, `select`, `checkbox`, `text`, `range`, `imageDimension`
- Maps to `config.json` settings keys

## Best Practices

- Fork Cornerstone as your starting point — don't start from scratch
- Use front matter to control data loading — don't over-fetch
- Use `{{inject}}` to pass data to JS — don't scrape the DOM
- Use `{{cdn}}` for all asset URLs — ensures CDN delivery
- Define schema.json entries for all customizable settings
- Use SCSS variables linked to config.json for consistent theming
- Escape user content: `{{{sanitize html}}}` for HTML, `{{variable}}` auto-escapes
- Test across theme variations
- Keep bundle size small — conditionally load JS per page

Fetch the Stencil documentation and theme object reference for exact helper syntax, front matter keys, and object structure before implementing.
