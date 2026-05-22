---
name: shopify-liquid
description: Guide for using the Liquid template language within Shopify Theme App Extensions and Themes. Use this skill when building App Embed Blocks, App Blocks, or modifying Shopify Themes.
---

# Shopify Liquid Skill

Liquid is the template language used by Shopify to load dynamic content on storefronts.

## 1. Core Syntax

-   **Output**: `{{ ... }}` - Prints content to the page.
-   **Tags**: `{% ... %}` - Logic (if, for, assign).
-   **Filters**: `{{ value | filter }}` - Modifies output.

## 2. Theme App Extensions (App Blocks)

Modern apps inject code into themes using **App Blocks**, avoiding direct legacy code edits.

### `schema` Tag
Defines settings available in the Theme Editor.

```liquid
{% schema %}
{
  "name": "Star Rating",
  "target": "section",
  "settings": [
    {
      "type": "color",
      "id": "star_color",
      "label": "Star Color",
      "default": "#ff0000"
    }
  ]
}
{% endschema %}
```

### Accessing Settings
Use `block.settings.id` to access values defined in schema.

```liquid
<div style="color: {{ block.settings.star_color }}">
  ★★★★★
</div>
```

### App Embed Blocks
Scripts that run globally (e.g., analytics, chat bubbles).

```liquid
{% schema %}
{
  "name": "Chat Bubble",
  "target": "body",
  "javascript": "chat.js",
  "settings": []
}
{% endschema %}
```

## 3. Common Objects

-   **`product`**:
    -   `{{ product.title }}`
    -   `{{ product.variants.first.id }}`
    -   `{{ product.featured_image | image_url: width: 400 }}`
-   **`cart`**:
    -   `{{ cart.item_count }}`
    -   `{{ cart.currency.iso_code }}`
-   **`customer`**:
    -   `{% if customer %}` checks if logged in.
-   **`shop`**:
    -   `{{ shop.name }}`
    -   `{{ shop.permanent_domain }}`

## 4. Useful Filters

-   **Money**: `{{ product.price | money }}` -> `$10.00`
-   **Asset URL**: `{{ 'style.css' | asset_url }}` (Reference assets in `assets/` folder)
-   **JSON**: `{{ product | json }}` (Useful for passing data to JS)

## 5. Using with JavaScript

Pass Liquid data to JavaScript using data attributes or global variables.

**Pattern: Data Attributes (Preferred)**
```liquid
<div id="my-app" data-product-id="{{ product.id }}" data-shop="{{ shop.permanent_domain }}"></div>

<script>
  const app = document.getElementById('my-app');
  const productId = app.dataset.productId;
</script>
```

**Pattern: Global Object (Legacy)**
```liquid
<script>
  window.ShopifyData = {
    product: {{ product | json }},
    cart: {{ cart | json }}
  };
</script>
```

## 6. App Proxies
When the request comes from an App Proxy, `liquid` renders the response before sending it to the layout.

-   If you return `Content-Type: application/liquid`, Shopify will parse the Liquid in your response.
