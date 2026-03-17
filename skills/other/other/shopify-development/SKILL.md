---
version: 4.1.0-fractal
name: shopify-development
description: |
  Build Shopify apps, extensions, themes using GraphQL Admin API, Shopify CLI, Polaris UI, and Liquid.
  TRIGGER: "shopify", "shopify app", "checkout extension", "admin extension", "POS extension",
  "shopify theme", "liquid template", "polaris", "shopify graphql", "shopify webhook",
  "shopify billing", "app subscription", "metafields", "shopify functions"
---

# Shopify Development Skill

Use this skill when the user asks about:

- Building Shopify apps or extensions
- Creating checkout/admin/POS UI customizations
- Developing themes with Liquid templating
- Integrating with Shopify GraphQL or REST APIs
- Implementing webhooks or billing
- Working with metafields or Shopify Functions

---

## ROUTING: What to Build

**IF user wants to integrate external services OR build merchant tools OR charge for features:**
→ Build an **App** (see `references/app-development.md`)

**IF user wants to customize checkout OR add admin UI OR create POS actions OR implement discount rules:**
→ Build an **Extension** (see `references/extensions.md`)

**IF user wants to customize storefront design OR modify product/collection pages:**
→ Build a **Theme** (see `references/themes.md`)

**IF user needs both backend logic AND storefront UI:**
→ Build **App + Theme Extension** combination

---

## Shopify CLI Commands

Install CLI:

```bash
npm install -g @shopify/cli@latest
```

Create and run app:

```bash
shopify app init          # Create new app
shopify app dev           # Start dev server with tunnel
shopify app deploy        # Build and upload to Shopify
```

Generate extension:

```bash
shopify app generate extension --type checkout_ui_extension
shopify app generate extension --type admin_action
shopify app generate extension --type admin_block
shopify app generate extension --type pos_ui_extension
shopify app generate extension --type function
```

Theme development:

```bash
shopify theme init        # Create new theme
shopify theme dev         # Start local preview at localhost:9292
shopify theme pull --live # Pull live theme
shopify theme push --development  # Push to dev theme
```

---

## Access Scopes

Configure in `shopify.app.toml`:

```toml
[access_scopes]
scopes = "read_products,write_products,read_orders,write_orders,read_customers"
```

Common scopes:

- `read_products`, `write_products` - Product catalog access
- `read_orders`, `write_orders` - Order management
- `read_customers`, `write_customers` - Customer data
- `read_inventory`, `write_inventory` - Stock levels
- `read_fulfillments`, `write_fulfillments` - Order fulfillment

---

## GraphQL Patterns (Validated against API 2026-01)

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Query Products](./sub-skills/query-products.md)
### 2. [Query Orders](./sub-skills/query-orders.md)
### 3. [Set Metafields](./sub-skills/set-metafields.md)
### 4. [API Usage](./sub-skills/api-usage.md)
### 5. [Security](./sub-skills/security.md)
### 6. [Performance](./sub-skills/performance.md)
