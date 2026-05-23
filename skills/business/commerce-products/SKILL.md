---
name: commerce-products
description: Manage products, variants, and pricing in StateSet iCommerce. Use when listing/creating products, updating variants, or running `stateset-direct products`.
---

# Commerce Products

Manage product catalog entries and variants for storefront and order flows.

## How It Works

1. List and search products by name, slug, or SKU.
2. Create or update product records and variants.
3. Activate or deactivate products as needed.
4. Report the catalog changes.

## Usage

- CLI: `stateset "list products"` or `stateset-direct products <action>`
- Writes require `--apply`.
- MCP tools: `list_products`, `get_product`, `get_product_variant`, `create_product`.

## Output

```json
{"status":"ok","product_id":"prod_123","sku":"WIDGET-001"}
```

## Present Results to User

- Product or variant identifiers affected.
- Pricing or status changes applied.
- Any validation checks performed.

## Troubleshooting

- SKU not found: confirm variant SKU or create the product first.
- Product inactive: activate before using in checkout.

## References
- references/product-commands.md
- /home/dom/stateset-icommerce/examples/cli-reference.md
- /home/dom/stateset-icommerce/cli/src/commands/products.js
