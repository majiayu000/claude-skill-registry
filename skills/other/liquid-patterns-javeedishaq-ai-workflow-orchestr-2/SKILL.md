---
name: liquid-patterns
description: Common Liquid code patterns for Shopify theme development. Use when writing Liquid templates, handling translations, product displays, or theme customizations.
---

# Shopify Liquid Patterns

## Translation in Liquid

```liquid
{% comment %} Use locale files for hardcoded text {% endcomment %}
{{ 'products.benefits.lifetime_guarantee' | t }}

{% comment %} With default fallback {% endcomment %}
{{ 'products.benefits.lifetime_description' | t: default: 'Fallback text' }}

{% comment %} Dynamic key translation {% endcomment %}
{% assign key = 'products.' | append: product.type | append: '.title' %}
{{ key | t }}
```

## Product Display Patterns

### Product Card

```liquid
<div class="product-card" data-product-id="{{ product.id }}">
  {% if product.featured_image %}
    <img
      src="{{ product.featured_image | image_url: width: 400 }}"
      alt="{{ product.featured_image.alt | escape }}"
      loading="lazy"
      width="400"
      height="{{ 400 | divided_by: product.featured_image.aspect_ratio | round }}"
    >
  {% endif %}

  <h3>{{ product.title }}</h3>

  {% if product.compare_at_price > product.price %}
    <span class="price--sale">{{ product.price | money }}</span>
    <span class="price--compare">{{ product.compare_at_price | money }}</span>
  {% else %}
    <span class="price">{{ product.price | money }}</span>
  {% endif %}
</div>
```

### Variant Selector

```liquid
{% for option in product.options_with_values %}
  <div class="option-selector">
    <label for="option-{{ forloop.index }}">{{ option.name }}</label>
    <select id="option-{{ forloop.index }}" name="options[{{ option.name }}]">
      {% for value in option.values %}
        <option
          value="{{ value }}"
          {% if option.selected_value == value %}selected{% endif %}
        >
          {{ value }}
        </option>
      {% endfor %}
    </select>
  </div>
{% endfor %}
```

## Image Handling

```liquid
{% comment %} Responsive images with srcset {% endcomment %}
{% assign image = product.featured_image %}
<img
  src="{{ image | image_url: width: 600 }}"
  srcset="{{ image | image_url: width: 300 }} 300w,
          {{ image | image_url: width: 600 }} 600w,
          {{ image | image_url: width: 900 }} 900w"
  sizes="(max-width: 600px) 300px, (max-width: 900px) 600px, 900px"
  alt="{{ image.alt | escape }}"
  loading="lazy"
>
```

## Collection Loops

```liquid
{% paginate collection.products by 12 %}
  <div class="product-grid">
    {% for product in collection.products %}
      {% render 'product-card', product: product %}
    {% endfor %}
  </div>

  {% if paginate.pages > 1 %}
    {% render 'pagination', paginate: paginate %}
  {% endif %}
{% endpaginate %}
```

## Metafield Access

```liquid
{% comment %} Product metafield {% endcomment %}
{% if product.metafields.custom.badge_type %}
  <span class="badge-type">{{ product.metafields.custom.badge_type.value }}</span>
{% endif %}

{% comment %} Shop metafield {% endcomment %}
{{ shop.metafields.global.announcement | metafield_tag }}
```

## Conditional Rendering

```liquid
{% comment %} Check for specific template {% endcomment %}
{% if template.name == 'product' %}
  {% comment %} Product-specific code {% endcomment %}
{% endif %}

{% comment %} Check customer status {% endcomment %}
{% if customer %}
  {{ 'account.welcome' | t: name: customer.first_name }}
{% else %}
  {{ 'account.login_prompt' | t }}
{% endif %}
```

## Form Patterns

### Add to Cart Form

```liquid
{% form 'product', product %}
  <input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}">

  <div class="quantity">
    <label for="quantity">{{ 'products.quantity' | t }}</label>
    <input type="number" id="quantity" name="quantity" value="1" min="1">
  </div>

  <button
    type="submit"
    name="add"
    {% unless product.available %}disabled{% endunless %}
  >
    {% if product.available %}
      {{ 'products.add_to_cart' | t }}
    {% else %}
      {{ 'products.sold_out' | t }}
    {% endif %}
  </button>
{% endform %}
```

## Section Schema

```liquid
{% schema %}
{
  "name": "Custom Section",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Section Heading"
    },
    {
      "type": "image_picker",
      "id": "image",
      "label": "Image"
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

## Swiss Military Terminology

Always use:
- ✅ "badge" (NOT "écusson")
- ✅ "section" (NOT "peloton")

```liquid
{% comment %} Correct {% endcomment %}
{{ 'products.badge.title' | t }}

{% comment %} Wrong - never use {% endcomment %}
{{ 'products.ecusson.title' | t }}
```
