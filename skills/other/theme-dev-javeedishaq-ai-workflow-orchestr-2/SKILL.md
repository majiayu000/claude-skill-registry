---
name: theme-dev
description: Shopify theme development workflows and best practices. Use for theme deployment, local development, asset management, and theme customization.
---

# Shopify Theme Development

## MyArmy Theme Configuration

| Environment | Theme ID | Store |
|-------------|----------|-------|
| Production | 185946079581 | 087ffd-4a.myshopify.com |
| Development | 188598124893 | 087ffd-4a.myshopify.com |

## Development Commands

```bash
cd shopify-theme

# Start local development with hot reload
shopify theme dev --store=087ffd-4a.myshopify.com

# Preview specific theme
shopify theme dev --theme=188598124893 --store=087ffd-4a.myshopify.com

# Open theme preview in browser
shopify theme open --theme=188598124893 --store=087ffd-4a.myshopify.com
```

## Deployment

```bash
# Push to production (CAREFUL!)
shopify theme push --theme=185946079581 --store=087ffd-4a.myshopify.com --allow-live

# Push to development theme
shopify theme push --theme=188598124893 --store=087ffd-4a.myshopify.com

# Push only specific files
shopify theme push --theme=188598124893 --store=087ffd-4a.myshopify.com \
  --only="sections/product-*" --only="locales/*"

# Push only locale files
shopify theme push --theme=185946079581 --store=087ffd-4a.myshopify.com \
  --allow-live --only="locales/"
```

## Theme Structure

```
shopify-theme/
├── assets/               # CSS, JS, images
├── config/
│   ├── settings_data.json
│   └── settings_schema.json
├── layout/               # theme.liquid, password.liquid
├── locales/              # Language files (en, de, fr, it)
│   ├── en.default.json
│   ├── fr.json
│   ├── de.json
│   └── it.json
├── sections/             # Section templates
├── snippets/             # Reusable components
└── templates/            # Page templates
```

## Locale Files

All 4 language files must stay in sync:

```bash
# Check locale file consistency
diff <(jq -r 'paths | join(".")' locales/en.default.json | sort) \
     <(jq -r 'paths | join(".")' locales/de.json | sort)
```

### Locale Structure

```json
{
  "products": {
    "benefits": {
      "lifetime_guarantee": "Lifetime Guarantee",
      "lifetime_description": "Description here..."
    }
  }
}
```

### Swiss Terminology (CRITICAL)

```json
// ✅ CORRECT
"badge_title": "Custom Badge"

// ❌ WRONG
"ecusson_title": "Écusson personnalisé"
```

## Section Development

### Section File Structure

```liquid
{% comment %} sections/custom-section.liquid {% endcomment %}

<section class="custom-section">
  <div class="container">
    {% if section.settings.heading %}
      <h2>{{ section.settings.heading }}</h2>
    {% endif %}

    {% for block in section.blocks %}
      {% case block.type %}
        {% when 'text' %}
          <p>{{ block.settings.content }}</p>
        {% when 'image' %}
          {{ block.settings.image | image_url: width: 800 | image_tag }}
      {% endcase %}
    {% endfor %}
  </div>
</section>

{% schema %}
{
  "name": "Custom Section",
  "tag": "section",
  "class": "custom-section-wrapper",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading"
    }
  ],
  "blocks": [
    {
      "type": "text",
      "name": "Text Block",
      "settings": [
        {
          "type": "richtext",
          "id": "content",
          "label": "Content"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Custom Section"
    }
  ]
}
{% endschema %}
```

## Asset Management

### Image Optimization

```bash
# Optimize before adding to assets/
cd landing && npm run optimize:image path/to/image.png

# Convert to WebP
cd landing && npm run convert-originals
```

### CSS/JS Best Practices

- Keep critical CSS inline in layout
- Lazy load non-critical assets
- Use `asset_url` filter for all assets

```liquid
{{ 'custom.css' | asset_url | stylesheet_tag }}
{{ 'custom.js' | asset_url | script_tag }}
```

## Testing Workflow

1. Make changes locally
2. Test with `shopify theme dev`
3. Push to development theme
4. Test in development theme
5. Push to production (after verification)

```bash
# Full workflow
shopify theme dev --store=087ffd-4a.myshopify.com
# Test changes...
shopify theme push --theme=188598124893 --store=087ffd-4a.myshopify.com
# Verify in Shopify admin...
shopify theme push --theme=185946079581 --store=087ffd-4a.myshopify.com --allow-live
```

## Troubleshooting

### Theme Pull

```bash
# Pull latest production theme
shopify theme pull --theme=185946079581 --store=087ffd-4a.myshopify.com

# Pull only specific directories
shopify theme pull --theme=185946079581 --store=087ffd-4a.myshopify.com \
  --only="sections/*" --only="locales/*"
```

### Authentication

```bash
# Re-authenticate if needed
shopify auth logout
shopify auth login --store=087ffd-4a.myshopify.com
```

### Theme Check (Linting)

```bash
# Run Shopify theme check
shopify theme check

# Auto-fix issues
shopify theme check --auto-fix
```

## Environment Variables

Required in `.env`:

```bash
SHOPIFY_ACCESS_TOKEN=shpat_...
SHOPIFY_STORE_DOMAIN=087ffd-4a.myshopify.com
SHOPIFY_PRODUCTION_THEME_ID=185946079581
SHOPIFY_DEVELOPMENT_THEME_ID=188598124893
```

Sync from 1Password:

```bash
npm run secrets:sync
```
