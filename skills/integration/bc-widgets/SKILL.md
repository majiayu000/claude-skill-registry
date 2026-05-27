---
name: bc-widgets
description: Build BigCommerce widgets and use Script Manager — widget templates, widget placements, Page Builder integration, Script Manager API for injecting JavaScript/CSS, and storefront content customization. Use when adding custom content blocks or injecting scripts into the storefront.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Widgets & Script Manager

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.bigcommerce.com/docs/storefront/widgets` for Widget SDK
2. Web-search `site:developer.bigcommerce.com scripts api` for Script Manager API
3. Web-search `bigcommerce page builder widgets custom` for custom widget patterns

## Widget System

### Architecture

Widgets are reusable content components managed via API:
- **Widget Template** — Handlebars template defining the HTML output
- **Widget** — an instance of a template with specific configuration data
- **Placement** — positions a widget in a specific theme region on specific pages
- **Page Builder** — admin drag-and-drop UI that creates widgets and placements

### How It Fits Together

```
Widget Template (Handlebars + JSON schema)
    ↓
Widget (template + configuration data)
    ↓
Placement (widget + region + page)
    ↓
Rendered on storefront
```

## Widget Templates

### Creating a Template

`POST /v3/content/widget-templates`:
```json
{
  "name": "Banner with CTA",
  "storefront_api_query": "query { site { settings { storeName } } }",
  "schema": [
    {
      "type": "tab",
      "label": "Content",
      "sections": [
        {
          "label": "Banner",
          "settings": [
            {
              "type": "text",
              "label": "Heading",
              "id": "heading",
              "default": "Welcome"
            },
            {
              "type": "text",
              "label": "Button Text",
              "id": "buttonText",
              "default": "Shop Now"
            },
            {
              "type": "text",
              "label": "Button URL",
              "id": "buttonUrl",
              "default": "/shop"
            }
          ]
        }
      ]
    }
  ],
  "template": "<div class='banner'><h2>{{heading}}</h2><a href='{{buttonUrl}}'>{{buttonText}}</a></div>"
}
```

### Schema Field Types

| Type | Description |
|------|-------------|
| `text` | Text input |
| `textarea` | Multi-line text |
| `number` | Numeric input |
| `boolean` | Toggle/checkbox |
| `select` | Dropdown select |
| `color` | Color picker |
| `imageManager` | Image upload/select |
| `productId` | Product picker |
| `categoryId` | Category picker |
| `range` | Slider |
| `alignment` | Text alignment |

### Template Syntax

Widget templates use Handlebars:
- `{{setting_id}}` — access setting values
- `{{{html_setting}}}` — unescaped HTML
- `{{#if condition}}...{{/if}}` — conditionals
- `{{#each items}}...{{/each}}` — iteration
- Access GraphQL data via `storefront_api_query` results

### GraphQL in Widgets

Widgets can include a `storefront_api_query` that fetches data at render time:
- Useful for dynamic content (featured products, customer data)
- Query results available in the template context
- Limited to the GraphQL Storefront API schema

## Widgets

### Creating a Widget

`POST /v3/content/widgets`:
```json
{
  "name": "Homepage Banner",
  "widget_template_uuid": "template-uuid-here",
  "widget_configuration": {
    "heading": "Summer Sale!",
    "buttonText": "Shop Deals",
    "buttonUrl": "/sale"
  }
}
```

## Placements

### Creating a Placement

`POST /v3/content/placements`:
```json
{
  "widget_uuid": "widget-uuid-here",
  "template_file": "pages/home",
  "region": "home_below_menu",
  "sort_order": 1,
  "status": "active"
}
```

### Regions

Regions are defined in Stencil theme templates using:
```handlebars
{{{region name="home_below_menu"}}}
```

Common regions: `home_below_menu`, `home_below_featured`, `product_below_price`, `category_below_header`

## Script Manager

### What It Does

Inject JavaScript, CSS, or HTML snippets into storefront pages without theme modification.

### API Endpoints

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/v3/content/scripts` | GET, POST, PUT, DELETE | Script CRUD |

### Creating a Script

`POST /v3/content/scripts`:
```json
{
  "name": "Analytics Tracker",
  "description": "Track page views",
  "html": "<script src='https://analytics.example.com/tracker.js'></script>",
  "src": "",
  "auto_uninstall": true,
  "load_method": "default",
  "location": "head",
  "visibility": "all_pages",
  "kind": "script_tag",
  "consent_category": "analytics",
  "channel_id": 1
}
```

### Script Properties

| Property | Options | Description |
|----------|---------|-------------|
| `location` | `head`, `footer` | Where to inject |
| `visibility` | `all_pages`, `storefront`, `checkout`, `order_confirmation` | Which pages |
| `load_method` | `default`, `async`, `defer` | Script loading strategy |
| `kind` | `script_tag`, `src` | Inline HTML or external URL |
| `auto_uninstall` | `true/false` | Remove when app is uninstalled |
| `consent_category` | `essential`, `functional`, `analytics`, `targeting` | Cookie consent category |

### Use Cases

- Analytics (Google Analytics, Meta Pixel)
- Chat widgets (Intercom, Zendesk)
- A/B testing tools
- Custom CSS overrides
- Third-party integrations

## Best Practices

- Use widgets for structured, reusable content — not one-off HTML
- Define complete JSON schemas for Page Builder integration
- Use `auto_uninstall: true` for app-managed scripts
- Set appropriate `consent_category` for GDPR compliance
- Use `load_method: 'defer'` for non-critical scripts
- Place widgets in well-defined theme regions
- Test widget rendering across different theme variations
- Use Script Manager API for scripts that don't require theme changes
- Prefer widgets over scripts for content — they're manageable in Page Builder

Fetch the BigCommerce Widget SDK and Script Manager API documentation for exact schema types, placement regions, and script properties before implementing.
