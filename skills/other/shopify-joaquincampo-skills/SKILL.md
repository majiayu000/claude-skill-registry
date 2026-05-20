---
name: shopify
description: Shopify app and storefront development. Use when writing, reviewing, or scaffolding Shopify apps (Remix/React Router), Hydrogen storefronts, theme app extensions, checkout UI extensions, Shopify Functions, or any code that touches Shopify APIs (Admin GraphQL, Storefront, App Bridge, Polaris). Triggers on shopify.app.toml, @shopify/* imports, Polaris components, Shopify CLI commands, Hydrogen/Oxygen, metafields/metaobjects, webhooks, or any Shopify development task.
---

# Shopify Development (2026)

Comprehensive guide for building Shopify apps, extensions, Hydrogen storefronts, and integrations using current best practices.

## DevMCP Server

Shopify provides an official MCP server for AI-assisted development. If not already configured:

```bash
# Claude Code
claude mcp add --transport stdio shopify-dev-mcp -- npx -y @shopify/dev-mcp@latest
```

The DevMCP server provides tools to search Shopify docs, explore API schemas (Admin GraphQL, Storefront, Functions, Liquid, Polaris, POS UI Extensions), and get up-to-date answers. **Use it** for API field lookups and schema exploration.

## Stack & Tooling

| Layer | Current (2026) |
|---|---|
| App framework | React Router (formerly Remix) via `@shopify/shopify-app-react-router` |
| Scaffold | `shopify app init` → React Router template |
| CLI | `@shopify/cli` — init, dev, deploy, generate extension |
| UI (embedded apps) | **Polaris Web Components** (not Polaris React — deprecated) |
| UI (extensions) | Polaris Web Components + **Preact** (not React) — 64KB bundle limit |
| App Bridge | CDN v4 — `https://cdn.shopify.com/shopifycloud/app-bridge.js` |
| APIs | Admin GraphQL (primary), Storefront GraphQL, Functions API |
| Custom data | Metafields + Metaobjects via TOML or GraphQL |
| Headless | Hydrogen + Oxygen (React Router v7, Vite, edge rendering) |
| Functions | Wasm — Rust (recommended) or JavaScript (Javy) |
| Config | `shopify.app.toml` — single source of truth |

**Critical**:
- REST Admin API is **legacy** since October 1, 2024. As of April 1, 2025, all new public apps must use **GraphQL Admin API exclusively**.
- Shopify Scripts: no editing/publishing after **April 15, 2026**; all scripts stop executing **June 30, 2026**. Migrate to Functions now.
- Polaris React (`@shopify/polaris`) is **deprecated** (maintenance mode only). Use Polaris Web Components.
- UI Extensions (checkout, admin, POS) must use **Preact** (not React) for API 2025-10+. 64KB bundle size limit enforced at deploy.

## Scaffolding

```bash
shopify app init                        # Interactive — choose React Router template
shopify app dev                         # Local dev with tunnel + hot reload
shopify app generate extension          # Add extensions (checkout UI, functions, theme, admin, POS)
shopify app deploy                      # Deploy app version (config + all extensions)
```

### Directory Structure (React Router template)

```
my-app/
├── shopify.app.toml          # App config, scopes, webhooks, metaobjects
├── app/
│   ├── entry.server.tsx      # Server entry
│   ├── root.tsx              # Root layout
│   ├── routes/
│   │   ├── app.tsx           # Authenticated layout (App Bridge + Polaris)
│   │   ├── app._index.tsx    # App home page
│   │   └── webhooks.tsx      # Webhook handler
│   └── shopify.server.ts     # shopifyApp() config — auth, session storage
├── extensions/               # All extensions live here
│   ├── checkout-ui/
│   ├── theme-extension/
│   └── my-function/
├── prisma/
│   └── schema.prisma         # Session table (required)
└── package.json
```

## Authentication & Sessions

- **App Bridge v4 (CDN) automatically handles session tokens** — no manual JWT fetch needed. The manual setup guide is for legacy App Bridge 2.0 only.
- Embedded apps use session tokens (JWT, 1-minute lifetime). Third-party cookies are blocked by browsers.
- `@shopify/shopify-app-react-router` (recommended) or `@shopify/shopify-app-remix` (v4, still works) handle OAuth + token exchange automatically.
- Session storage: Prisma adapter (`@shopify/shopify-app-session-storage-prisma`) — the Session table is required.
- Use `authenticate.admin(request)` in loaders/actions for authenticated Admin API access.
- Use `authenticate.public.checkout(request)` for checkout extension requests.
- **Never** expose Admin API tokens in client-side code.
- Use **offline access tokens** for bulk operations and webhooks (online tokens expire in 24h).

```typescript
// app/shopify.server.ts
import { shopifyApp } from "@shopify/shopify-app-react-router";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import prisma from "./db.server";

const shopify = shopifyApp({
  sessionStorage: new PrismaSessionStorage(prisma),
  // API key, secret, scopes, and app URL are read from
  // shopify.app.toml + environment variables automatically
});
export default shopify;
export const authenticate = shopify.authenticate;

// In a route loader:
export async function loader({ request }: LoaderFunctionArgs) {
  const { admin } = await authenticate.admin(request);
  const response = await admin.graphql(`{ shop { name } }`);
  const { data } = await response.json();
  return { shopName: data.shop.name };
}
```

> **Migration note**: If on `@shopify/shopify-app-remix`, migrate to `@shopify/shopify-app-react-router` — see [migration guide](https://github.com/Shopify/shopify-app-template-react-router/wiki/Upgrading-from-Remix).

## Polaris Web Components (NOT Polaris React)

Polaris React is **deprecated**. Use Polaris Web Components — framework-agnostic custom HTML elements.

### Setup

```html
<head>
  <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
  <script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
  <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
</head>
```

### Usage in React (App Home)

```tsx
function ProductForm() {
  const [name, setName] = useState("");
  return (
    <s-page title="New Product">
      <s-layout>
        <s-layout-section>
          <s-card>
            <s-form-layout>
              <s-text-field
                label="Product name"
                value={name}
                onInput={(e) => setName(e.currentTarget.value)}
                required
              />
              <s-button variant="primary" type="submit">Save</s-button>
            </s-form-layout>
          </s-card>
        </s-layout-section>
      </s-layout>
    </s-page>
  );
}
```

### Key Patterns

- Elements are prefixed with `s-` (e.g., `s-card`, `s-button`, `s-badge`, `s-data-table`).
- Use `onInput` for real-time updates, `onChange` for on-blur/enter validation.
- All form values are **strings** — parse numbers/booleans yourself.
- `tone` applies semantic color (`critical`, `success`, `info`); `variant` sets visual weight (`primary`, `secondary`).
- Links with `target="auto"` auto-detect internal (`_self`) vs external (`_blank`).
- **Do not** apply custom CSS to Polaris components — they have built-in design system styling.

### Navigation (App Bridge)

```tsx
// Handle Shopify navigation events in Remix/React Router
useEffect(() => {
  const handler = (event) => {
    const href = event.target.getAttribute("href");
    if (href) navigate(href);
  };
  document.addEventListener("shopify:navigate", handler);
  return () => document.removeEventListener("shopify:navigate", handler);
}, [navigate]);
```

Use `<s-navigation-menu>` for sidebar nav. Use `shopify.navigate()` for programmatic navigation. **Never** use `<a>` tags or `redirect` from `react-router` in embedded apps — use `Link` from `react-router` or the redirect helper from `authenticate.admin`.

## Admin GraphQL API

### Query Patterns

```typescript
// Simple query
const response = await admin.graphql(`
  query {
    products(first: 10) {
      edges {
        node { id title handle }
      }
    }
  }
`);

// Mutation with variables
const response = await admin.graphql(`
  mutation createProduct($input: ProductInput!) {
    productCreate(input: $input) {
      product { id title }
      userErrors { field message }
    }
  }
`, { variables: { input: { title: "New Product" } } });

// Always check userErrors
const { data } = await response.json();
if (data.productCreate.userErrors.length > 0) {
  throw new Error(data.productCreate.userErrors[0].message);
}
```

### Rate Limiting

- Admin GraphQL uses **calculated query cost** (cost points, not request count).
- Complex queries with nested connections cost more points.
- Use `cursor`-based pagination for large datasets.
- For bulk data: use **bulk operations** (`bulkOperationRunQuery` / `bulkOperationRunMutation`) — up to 5 concurrent queries **and** 5 concurrent mutations per shop in API 2026-01+ (previously 1 each).
- Use **offline access tokens** for bulk operations (online tokens expire before completion).

### API Version

Always pin to a stable version (e.g., `2026-01`). Set in `shopify.app.toml`:

```toml
[webhooks]
api_version = "2026-01"
```

## Storefront API

- For **all customer-facing** data: products, collections, cart, checkout.
- **No rate limits** on request count — scales for buyer traffic surges.
- Requires Storefront access token (public, safe for client-side).
- Use in Hydrogen storefronts, mobile apps, or headless frontends.

## Metafields & Metaobjects

### When to Use Which

| Use Case | Tool |
|---|---|
| Add custom field to existing resource (product, order, customer) | Metafield |
| Create standalone reusable structured data | Metaobject |
| App-internal data model | Metaobject with `$app:` prefix in TOML |

### App-Owned Metafields (TOML)

```toml
# shopify.app.toml — auto-created on `shopify app dev`
[[metaobjects]]
type = "$app:qrcode"

  [metaobjects.access]
  admin = "merchant_read_write"
  storefront = "public_read"

  [[metaobjects.fields]]
  key = "title"
  type = "single_line_text_field"
  name = "Title"
  required = true

  [[metaobjects.fields]]
  key = "product"
  type = "product_reference"
  name = "Product"
```

### Merchant-Owned Metafields (GraphQL)

```graphql
mutation {
  metafieldDefinitionCreate(definition: {
    name: "Warranty Info"
    namespace: "custom"       # NOT $app — merchant-owned
    key: "warranty_info"
    type: "multi_line_text_field"
    ownerType: PRODUCT
    access: { storefront: PUBLIC_READ }
  }) {
    createdDefinition { name namespace key }
  }
}
```

- `$app` namespace = app-owned (read-only in admin by default).
- `custom` or other namespaces = merchant-owned.
- Use TOML for app-owned; GraphQL for merchant-owned.

## Webhooks

### Configuration (TOML)

```toml
[webhooks]
api_version = "2026-01"

[[webhooks.subscriptions]]
topics = ["orders/create", "products/update"]
uri = "/webhooks"

[[webhooks.subscriptions]]
compliance_topics = ["customers/data_request", "customers/redact", "shop/redact"]
uri = "https://app.example.com/webhooks"
```

### Mandatory Compliance (Required for App Store)

Every public app **must** handle these three webhooks:
1. `customers/data_request` — respond with customer data you store
2. `customers/redact` — delete customer personal data
3. `shop/redact` — delete all shop data after uninstall

Validate HMAC on every webhook. Return 401 for invalid HMAC, 200 for valid.

### GraphQL Subscriptions

```graphql
mutation {
  webhookSubscriptionCreate(
    topic: ORDERS_CREATE
    webhookSubscription: {
      callbackUrl: "https://app.example.com/webhooks"
      format: JSON
    }
  ) {
    webhookSubscription { id }
    userErrors { field message }
  }
}
```

## Shopify Functions (Wasm)

Extend Shopify backend logic (discounts, validation, delivery, payment customization) as sandboxed WebAssembly modules.

### Language Choice

- **Rust**: 3x faster than JS. Required for public apps with complex logic or high line-item counts. Stays within instruction count limits.
- **JavaScript** (via Javy → Wasm): Viable for prototyping and simple logic (<5ms realistic cases). Lower barrier to entry.

### Execution Order in Checkout

1. Cart Transform → 2. Discount (cart lines) → 3. Fulfillment/Order Routing → 4. Delivery Customization → 5. Discount (delivery) → 6. Payment Customization → 7. Cart Validation

### Scaffold & Build

```bash
shopify app generate extension    # Choose function type
shopify app function schema       # Regenerate GraphQL schema
shopify app function run          # Test locally
```

### Structure

```
extensions/my-discount/
├── shopify.extension.toml     # Extension config (target, API version)
├── src/
│   ├── run.graphql            # Input query — what data the function receives
│   └── run.rs (or run.js)     # Function logic
├── schema.graphql             # Generated API schema
└── Cargo.toml (or package.json)
```

**Performance**: Functions run during checkout — delays block purchases. Minimize instruction count. Avoid unnecessary data in `run.graphql`.

## Extensions

### Types

| Extension | Purpose |
|---|---|
| `theme_app_extension` | Liquid blocks/snippets in Online Store themes |
| `checkout_ui_extension` | Custom UI at checkout extension points |
| `admin_action` | Dropdown actions on admin resource pages |
| `admin_block` | Embedded blocks on admin resource pages |
| `pos_ui_extension` | POS interface extensions |
| Functions | Backend logic (discounts, delivery, validation, payments) |

### Theme App Extensions

Required for all new App Store apps (replaces manual theme code editing).

```
extensions/theme-extension/
├── shopify.extension.toml
├── blocks/
│   └── rating.liquid
├── snippets/
├── assets/
└── locales/
```

### Checkout UI Extensions

20+ extension points (e.g., `Checkout::Dynamic::Render`). Use Polaris Web Components. Keep lightweight — mobile-first.

**Critical: React is deprecated for UI extensions as of API 2025-10.** Must use **Preact** for any API version 2025-10+. Vanilla React + ui-react package exceeds the **64KB bundle limit**.

```toml
# shopify.extension.toml
api_version = "2026-01"

[[extensions]]
name = "my-checkout-ext"
handle = "my-checkout-ext"
type = "ui_extension"
```

```json
// package.json dependencies for UI extensions
{
  "dependencies": {
    "preact": "^10.10.x",
    "@preact/signals": "^2.3.x",
    "@shopify/ui-extensions": "2026.1.x"
  }
}
```

```json
// tsconfig.json for Preact JSX
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "preact"
  }
}
```

## Hydrogen & Oxygen (Headless)

### Stack

- **Hydrogen**: React framework (React Router v7 + Vite) with Storefront API utilities, streaming SSR, granular caching.
- **Oxygen**: Shopify's edge runtime (based on Cloudflare workerd). Multiple preview environments. CI/CD via GitHub.
- **Vite-first**: Legacy Remix compiler no longer supported — must use Vite.

### Key Patterns

```typescript
// Caching — be explicit
const { storefront } = await context.storefront.query(PRODUCT_QUERY, {
  cache: CacheLong(),    // or CacheShort(), CacheNone(), CacheCustom()
});

// Streaming for performance
export default function Product() {
  return (
    <Suspense fallback={<ProductSkeleton />}>
      <Await resolve={recommendedProducts}>
        {(products) => <ProductGrid products={products} />}
      </Await>
    </Suspense>
  );
}
```

### AI Integration (2026)

Hydrogen on Oxygen supports **Storefront MCP** — build AI agents into storefronts for personalized recommendations and checkout guidance using real-time Storefront API data.

## App Store Submission Checklist

1. **GraphQL only** — no REST API calls
2. **Session tokens** — no cookie-based auth
3. **Mandatory compliance webhooks** — all three implemented and HMAC-validated
4. **Theme app extensions** — no manual theme code injection
5. **Polaris Web Components** — consistent admin UI
6. **Performance** — must not reduce Lighthouse score by >10 points
7. **Privacy** — GDPR/CCPA compliant, data handling documented
8. **Credentials** — provide valid test credentials with full feature access
9. **Screencast** — complete walkthrough of setup + functionality
10. **No Shopify trademarks** in app icon/banner/screenshots
11. Review timeline: 7–14 days. Statuses: Draft → Submitted → Reviewed → Published.

## Common Pitfalls

- Using `<a>` or bare `redirect()` in embedded apps (breaks iframe). Use `Link` from `react-router` or the redirect helper from `authenticate.admin`.
- Using Polaris React (`@shopify/polaris`) instead of Polaris Web Components — deprecated, maintenance-only.
- Using React in UI extensions targeting API 2025-10+ — must use **Preact** (64KB bundle limit).
- Exposing Admin API tokens client-side.
- Using REST API in new apps (legacy since Oct 2024; blocked for new public apps since April 2025).
- Not validating webhook HMAC.
- Using online access tokens for bulk operations (they expire in 24h).
- Heavy checkout extensions that slow mobile performance.
- Not handling `userErrors` in GraphQL mutations.
- Missing the `$app:` namespace prefix for app-owned metaobjects.
- Forgetting to run `shopify app function schema` after changing API version.
- Using `@shopify/shopify-app-remix` for new projects instead of `@shopify/shopify-app-react-router`.
