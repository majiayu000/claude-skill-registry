---
name: Liquid Render Skill
version: 1.0.0
description: Locally render Liquid templates using a virtual lab (Node.js engine).
allowed-tools:
  - render_liquid
  - save_preview
---

## Capabilities

This skill allows you to "compile" Liquid logic instantly without waiting for Shopify. You can check if your logic (loops, filters, math) is correct.
It also allows you to render a snippet into an HTML file (`save_preview`) so you can open it with Playwright and see the result.

## Dependencies

- **Local MCP Server**: This skill comes with a built-in Node.js server.
- **Node.js**: Required to run the server.

## Tools Usage Guide

### 1. `render_liquid`

Render a piece of code and get the HTML string back.

- **Param** `template`: `{% if products.size > 0 %}...{% endif %}`
- **Param** `data`: `{ "products": [{"title": "Shirt"}] }`

### 2. `save_preview` (Best for UI Testing)

Render liquid code into a real `.html` file that you can inspect visually.

- **Param** `template`: The code.
- **Param** `data`: Mock data.
- **Param** `filename`: (Optional) e.g., `my_test.html`.

## Workflow: Virtual Lab

1.  **Mock Data**: Agent invents JSON data describing a scenario (e.g. `product_with_50_variants.json`).
2.  **Render**: Agent calls `save_preview`.
3.  **Verify**: Agent calls `playwright_navigate(url="file:///path/to/my_test.html")` to see the result.

## Limitations

- This uses `liquidjs` (Node.js), not the official Shopify Ruby engine.
- Standard filters like `| asset_url` are mocked to return strings, so CSS/Images might not load if they rely on CDN.
- Use this for LOGIC testing mainly.
