---
name: shopify-metafields
description: Guide for working with Shopify Metafields. Covers definitions, storing custom data, accessing via Liquid, and GraphQL mutations.
---

# Shopify Metafields

Metafields allow you to store additional data on Shopify resources (Products, Orders, Customers, Shops) that aren't included in the default schema (e.g., "washing instructions" for a product).

## 1. Concepts

-   **Namespace**: Grouping folder (e.g., `my_app`, `global`).
-   **Key**: Specific field name (e.g., `washing_instructions`).
-   **Type**: Data type (e.g., `single_line_text_field`, `number_integer`, `json`).
-   **Owner**: The resource attaching the data (Product ID, Shop ID).

## 2. Metafield Definitions (Standard)

Always use **Metafield Definitions** (pinned metafields) when possible. This integrates them into the Admin UI and ensures standard processing.

-   **Create**: Settings > Custom Data > [Resource] > Add definition.
-   **Access**: `namespace.key`

## 3. Accessing in Liquid

To display metafield data on the Storefront:

```liquid
<!-- Accessing a product metafield -->
<p>Washing: {{ product.metafields.my_app.washing_instructions }}</p>

<!-- Accessing a file/image metafield -->
{% assign file = product.metafields.my_app.size_chart.value %}
<img src="{{ file | image_url: width: 500 }}" />

<!-- Checking existence -->
{% if product.metafields.my_app.instructions != blank %}
   ...
{% endif %}
```

## 4. Reading via API (GraphQL)

```graphql
query {
  product(id: "gid://shopify/Product/123") {
    title
    metafield(namespace: "my_app", key: "instructions") {
      value
      type
    }
  }
}
```

## 5. Writing via API (GraphQL)

To create or update a metafield, use `metafieldsSet`.

```graphql
mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      namespace
      key
      value
    }
    userErrors {
      field
      message
    }
  }
}

/* Variables */
{
  "metafields": [
    {
      "ownerId": "gid://shopify/Product/123",
      "namespace": "my_app",
      "key": "instructions",
      "type": "single_line_text_field",
      "value": "Wash cold, tumble dry."
    }
  ]
}
```

## 6. Private Metafields

If you want data to be **hidden from other apps** and the storefront, use Private Metafields. Note: These cannot be accessed via Liquid directly.

-   Use `privateMetafield` queries/mutations.
-   Requires explicit `read_private_metafields` / `write_private_metafields` scope (rarely used now, `app_data` metafields are preferred for app-specific valid storage).
