---
name: Schema Architect
version: 1.0.0
description: Intelligently generates and validates Shopify Liquid Schema JSON based on Liquid logic.
allowed-tools:
  - generate_schema
---

## Capabilities

This skill abstracts the complexity of writing valid JSON schema for Shopify sections. Not only does it fix syntax errors, but it also intelligently infers the `type` of settings required based on how variables are used in the liquid code.

## Tools Usage Guide

### 1. `generate_schema`

Analyzes Liquid code and produces a valid `{% schema %}...{% endschema %}` block.

- **Param** `liquid_content`: The full liquid content of a section file.
- **Returns**: A JSON object containing the suggested schema.

#### Example

**Input**:

```liquid
<h1>{{ section.settings.heading }}</h1>
{% if section.settings.show_image %}
  <img src="{{ section.settings.image | image_url }}" />
{% endif %}
```

**Output**:

```json
{
  "name": "Generated Section",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Default Heading"
    },
    {
      "type": "checkbox",
      "id": "show_image",
      "label": "Show Image",
      "default": true
    },
    {
      "type": "image_picker",
      "id": "image",
      "label": "Image"
    }
  ]
}
```
