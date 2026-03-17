---
name: shopify-products
description: >
  Create and manage Shopify products via the Admin API.
  Workflow: gather product data, choose method (API or CSV), execute, verify.
  Use when adding products, bulk importing, updating variants, managing inventory,
  uploading product images, or assigning products to collections.
compatibility: claude-code-only
---

# Shopify Products

Create, update, and bulk-import Shopify products. Produces live products in the store via the GraphQL Admin API or CSV import.

## Prerequisites

- Admin API access token (use the **shopify-setup** skill if not configured)
- Store URL and API version from `shopify.config.json` or `.dev.vars`

## Workflow

### Step 1: Gather Product Data

Determine what the user wants to create or update:

- **Product basics**: title, description (HTML), product type, vendor, tags
- **Variants**: options (size, colour, material), prices, SKUs, inventory quantities
- **Images**: URLs to upload, or local files
- **SEO**: page title, meta description, URL handle
- **Organisation**: collections, product type, tags

Accept data from:
- Direct conversation (user describes products)
- Spreadsheet/CSV file (user provides a file)
- Website scraping (user provides a URL to extract from)

### Step 2: Choose Method

| Scenario | Method |
|----------|--------|
| 1-5 products | GraphQL mutations |
| 6-20 products | GraphQL with batching |
| 20+ products | CSV import via admin |
| Updates to existing | GraphQL mutations |
| Inventory adjustments | `inventorySetQuantities` mutation |

### Step 3a: Create via GraphQL (Recommended)

**Single product with variants**:

```bash
curl -s https://{store}/admin/api/2025-01/graphql.json \
  -H "Content-Type: application/json" \
  -H "X-Shopify-Access-Token: {token}" \
  -d '{
    "query": "mutation productCreate($product: ProductCreateInput!) { productCreate(product: $product) { product { id title } userErrors { field message } } }",
    "variables": {
      "product": {
        "title": "Example T-Shirt",
        "descriptionHtml": "<p>Premium cotton tee</p>",
        "vendor": "My Brand",
        "productType": "T-Shirts",
        "tags": ["summer", "cotton"],
        "options": ["Size", "Colour"],
        "variants": [
          {"optionValues": [{"optionName": "Size", "name": "S"}, {"optionName": "Colour", "name": "Black"}], "price": "29.95"},
          {"optionValues": [{"optionName": "Size", "name": "M"}, {"optionName": "Colour", "name": "Black"}], "price": "29.95"},
          {"optionValues": [{"optionName": "Size", "name": "L"}, {"optionName": "Colour", "name": "Black"}], "price": "29.95"}
        ]
      }
    }
  }'
```

See `references/graphql-mutations.md` for all mutation patterns.

**Batching multiple products**: Create products sequentially with a short delay between each to respect rate limits (1,000 cost points/second).

### Step 3b: Bulk Import via CSV

For 20+ products, generate a CSV and import through Shopify admin:

1. Generate CSV using the format in `references/csv-format.md`
2. Use the template from `assets/product-csv-template.csv`
3. Navigate to `https://{store}.myshopify.com/admin/products/import`
4. Upload the CSV file
5. Review the preview and confirm import

Use browser automation to assist with the upload if needed.

### Step 4: Upload Product Images

Images require a two-step process — staged upload then attach:

```graphql
mutation {
  stagedUploadsCreate(input: [{
    filename: "product-image.jpg"
    mimeType: "image/jpeg"
    httpMethod: POST
    resource: IMAGE
  }]) {
    stagedTargets {
      url
      resourceUrl
      parameters { name value }
    }
  }
}
```

Then upload to the staged URL, and attach with `productCreateMedia`.

**Shortcut**: If images are already hosted at a public URL, pass `src` directly in the product creation:

```json
{
  "images": [
    { "src": "https://example.com/image.jpg", "alt": "Product front view" }
  ]
}
```

### Step 5: Assign to Collections

After creation, add products to collections:

```graphql
mutation {
  collectionAddProducts(
    id: "gid://shopify/Collection/123456"
    productIds: ["gid://shopify/Product/789"]
  ) {
    collection { title productsCount }
    userErrors { field message }
  }
}
```

To find collection IDs:

```graphql
{
  collections(first: 50) {
    edges {
      node { id title handle }
    }
  }
}
```

### Step 6: Verify

Query back the created products to confirm:

```graphql
{
  products(first: 10, reverse: true) {
    edges {
      node {
        id title status
        variants(first: 5) { edges { node { title price inventoryQuantity } } }
        images(first: 3) { edges { node { url altText } } }
      }
    }
  }
}
```

Provide the admin URL for the user to review: `https://{store}.myshopify.com/admin/products`

---

## Critical Patterns

### Product Status

New products default to `DRAFT`. To make them visible:

```json
{ "status": "ACTIVE" }
```

Always confirm with the user before setting status to `ACTIVE`.

### Variant Limits

Shopify allows max **100 variants** per product and **3 options** (e.g. Size, Colour, Material). If you need more, split into separate products.

### Inventory Tracking

To set inventory quantities, use `inventorySetQuantities` after product creation:

```graphql
mutation {
  inventorySetQuantities(input: {
    reason: "correction"
    name: "available"
    quantities: [{
      inventoryItemId: "gid://shopify/InventoryItem/123"
      locationId: "gid://shopify/Location/456"
      quantity: 50
    }]
  }) {
    inventoryAdjustmentGroup { reason }
    userErrors { field message }
  }
}
```

### Price Formatting

Prices are strings, not numbers. Always quote them: `"price": "29.95"` not `"price": 29.95`.

### HTML Descriptions

Product descriptions accept HTML. Keep it simple — Shopify's editor handles basic tags:
- `<p>`, `<strong>`, `<em>`, `<ul>`, `<ol>`, `<li>`, `<h2>`-`<h6>`
- `<a href="...">` for links
- `<img>` is stripped — use product images instead

### Bulk Operations for Large Imports

For 50+ products via API, use Shopify's bulk operation:

```graphql
mutation {
  bulkOperationRunMutation(
    mutation: "mutation ($input: ProductInput!) { productCreate(input: $input) { product { id } userErrors { message } } }"
    stagedUploadPath: "tmp/bulk-products.jsonl"
  ) {
    bulkOperation { id status }
    userErrors { message }
  }
}
```

This accepts a JSONL file with one product per line, processed asynchronously.

---

## Asset Files

- `assets/product-csv-template.csv` — Blank CSV template with Shopify import headers

## Reference Files

- `references/graphql-mutations.md` — Key GraphQL mutations for product CRUD
- `references/csv-format.md` — Shopify CSV import column format and examples
