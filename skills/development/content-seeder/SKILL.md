---
name: Content Seeder
version: 1.0.0
description: Generates realistic dummy data (text, images, products) based on Shopify Schema inputs.
allowed-tools:
  - generate_dummy_data
---

## Capabilities

Helps developers populate empty theme sections with testing data. By passing a Shopify JSON Schema (from `{% schema %}`), this skill returns a JSON object of settings filled with plausible content (Lorem Ipsum, Unsplash images, names, etc.).

## Tools Usage Guide

### 1. `generate_dummy_data`

Parses a Shopify Schema settings array and generates a corresponding settings object populated with dummy data.

- **Param** `schema_json`: The JSON string of the section schema (specifically the `settings` array).
- **Returns**: A JSON object where keys are setting IDs and values are generated content.

#### Example

**Input Schema**:

```json
[
  { "type": "text", "id": "heading", "label": "Heading" },
  { "type": "image_picker", "id": "banner", "label": "Banner Image" }
]
```

**Output**:

```json
{
  "heading": "Elegant Sustainable Fashion",
  "banner": "shopify://shop_images/fashion_banner_mockup.jpg"
}
```
