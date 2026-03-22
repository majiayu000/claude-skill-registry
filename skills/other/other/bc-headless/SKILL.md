---
name: bc-headless
description: Build headless commerce with BigCommerce — Catalyst (Next.js reference storefront), GraphQL Storefront API, server-side APIs, embedded checkout, and headless architecture patterns. Use when building decoupled storefronts or integrating BigCommerce as a headless backend.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Headless Commerce

## Before writing code

**Fetch live docs**:
1. Fetch `https://www.catalyst.dev/` for Catalyst documentation
2. Web-search `site:developer.bigcommerce.com headless` for headless guide
3. Web-search `site:github.com bigcommerce catalyst` for Catalyst source and examples

## Headless Architecture

### What Headless Means for BigCommerce

Decouple the frontend from BigCommerce:
- BigCommerce serves as the **commerce backend** — catalog, orders, customers, payments
- Your custom frontend handles **presentation** — React, Next.js, Vue, etc.
- Communication via **APIs** — GraphQL Storefront API and REST API
- Checkout via **Embedded Checkout** or **Custom Checkout** (Checkout API + Payments API)

### Why Headless

- Full frontend control (design, UX, performance)
- Use modern frameworks (Next.js, Remix, Astro)
- Composable architecture — mix BigCommerce with CMS, search, etc.
- Better performance with SSR/SSG/ISR
- Multi-channel frontend from single BigCommerce backend

## Catalyst

### What It Is

BigCommerce's official Next.js reference storefront:
- Built on **Next.js 14+** with App Router
- Uses **GraphQL Storefront API** for data
- **Tailwind CSS** for styling
- Full-featured: PLP, PDP, cart, checkout, customer account, search
- Designed as a starting point to fork and customize

### Getting Started

```bash
npx create-catalyst-storefront@latest my-store
```

Prompts for:
- BigCommerce store URL
- Channel ID
- Storefront API token

### Project Structure

```
my-store/
├── app/                     # Next.js App Router pages
│   ├── (default)/           # Default locale group
│   │   ├── page.tsx         # Homepage
│   │   ├── product/         # Product pages
│   │   ├── category/        # Category pages
│   │   ├── cart/            # Cart page
│   │   └── account/         # Customer account
│   └── layout.tsx           # Root layout
├── client/                  # BigCommerce API client
│   ├── queries/             # GraphQL queries
│   └── mutations/           # GraphQL mutations
├── components/              # React components
├── lib/                     # Utilities
├── public/                  # Static assets
├── .env.local               # Environment variables
├── next.config.js           # Next.js config
├── tailwind.config.js       # Tailwind config
└── package.json
```

### Key Environment Variables

```
BIGCOMMERCE_STORE_HASH=your_store_hash
BIGCOMMERCE_ACCESS_TOKEN=your_access_token
BIGCOMMERCE_CHANNEL_ID=1
BIGCOMMERCE_STOREFRONT_TOKEN=your_storefront_token
BIGCOMMERCE_CUSTOMER_IMPERSONATION_TOKEN=your_token
```

## Data Fetching Patterns

### Server Components (Recommended)

Fetch data in Next.js Server Components using the GraphQL client:
```typescript
// app/product/[slug]/page.tsx
async function ProductPage({ params }: { params: { slug: string } }) {
  const product = await getProduct({ path: `/${params.slug}` });
  return <ProductDetail product={product} />;
}
```

### Client-Side Fetching

For interactive features (cart, search-as-you-type):
- Use React hooks with the GraphQL Storefront API
- Storefront API token for unauthenticated requests
- Customer impersonation token for personalized data

### Caching Strategy

- **Static Generation (SSG)** — product and category pages at build time
- **Incremental Static Regeneration (ISR)** — revalidate on interval or on-demand
- **Server-Side Rendering (SSR)** — cart, checkout, account pages
- **Client-Side** — search, cart updates, wishlist

## Checkout in Headless

### Embedded Checkout (Recommended)

Embed BigCommerce's checkout in your headless site:
1. Create cart via API → get `redirect_urls.checkout_url`
2. Embed using `@bigcommerce/checkout-sdk` `embedCheckout()`
3. BigCommerce handles payment processing (no PCI scope)

### Custom Checkout

Full API-driven checkout:
1. Cart API → Checkout API → Orders API → Payments API
2. Requires your own checkout UI
3. Payment processing via Payments API (PCI implications if handling raw card data)
4. Use tokenized payment methods to reduce PCI scope

## Authentication in Headless

### Customer Login

- Use the Customer Login API (JWT-based SSO) to create sessions
- Or implement custom auth and use Customer Impersonation Tokens for API access
- Catalyst includes built-in authentication flows

### Session Management

- BigCommerce sessions are cookie-based on the BigCommerce domain
- For headless: use Customer Login API to set the cookie, then redirect to your domain
- Or manage auth entirely on your side and use impersonation tokens

## Integration with Other Services

### Composable Commerce Stack

BigCommerce + headless enables composable architecture:
- **CMS**: Contentful, Sanity, Strapi for content
- **Search**: Algolia, Bloomreach for product search
- **Personalization**: Dynamic Yield, Nosto for recommendations
- **PIM**: Akeneo, Salsify for product information
- **OMS**: for order management

## Best Practices

- Start with Catalyst — fork and customize rather than building from scratch
- Use GraphQL Storefront API for frontend data fetching
- Use REST API for server-side operations (order management, catalog sync)
- Use Embedded Checkout to avoid PCI scope
- Implement ISR for product/category pages — balance freshness and performance
- Use customer impersonation tokens for personalized data
- Handle webhook events for real-time data sync
- Set up proper CORS configuration for Storefront API tokens
- Use environment variables for all credentials

Fetch the Catalyst documentation and BigCommerce headless guide for exact setup steps, GraphQL queries, and current best practices before implementing.
