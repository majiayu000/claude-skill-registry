---
name: nextjs-patterns
description: Build with Next.js for BigCommerce — App Router, Server/Client Components, data fetching, ISR, middleware, API routes, and Catalyst patterns. Use when building headless BigCommerce storefronts with Next.js.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Next.js Patterns for BigCommerce

## Before writing code

**Fetch live docs**:
1. Fetch `https://nextjs.org/docs` for Next.js documentation
2. Fetch `https://www.catalyst.dev/` for Catalyst-specific patterns
3. Web-search `nextjs app router data fetching patterns` for current best practices

## App Router Fundamentals

### File-Based Routing

```
app/
├── page.tsx                   # /
├── layout.tsx                 # Root layout
├── products/
│   ├── page.tsx               # /products
│   └── [slug]/
│       └── page.tsx           # /products/:slug
├── cart/
│   └── page.tsx               # /cart
├── api/
│   └── webhooks/
│       └── route.ts           # /api/webhooks (API route)
└── not-found.tsx              # 404 page
```

### Special Files

| File | Purpose |
|------|---------|
| `page.tsx` | Route component |
| `layout.tsx` | Shared layout (persists across navigation) |
| `loading.tsx` | Loading UI (Suspense boundary) |
| `error.tsx` | Error boundary |
| `not-found.tsx` | 404 page |
| `route.ts` | API route handler |
| `template.tsx` | Re-rendered layout (no persistence) |

## Server vs Client Components

### Server Components (Default)

- Run on the server only — no JS sent to client
- Can `await` async operations directly
- Access server-only resources (DB, API tokens, env vars)
- Cannot use hooks, browser APIs, or event handlers

### Client Components

Mark with `'use client'` directive:
- Run in the browser
- Use React hooks (`useState`, `useEffect`, etc.)
- Handle user interactions (onClick, onChange)
- Access browser APIs

### Pattern for BigCommerce

```typescript
// Server Component — fetches data
async function ProductPage({ params }: { params: { slug: string } }) {
  const product = await getProduct(params.slug); // Server-side fetch
  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={product.id} /> {/* Client component */}
    </div>
  );
}

// Client Component — handles interactivity
'use client';
function AddToCartButton({ productId }: { productId: number }) {
  const [loading, setLoading] = useState(false);
  const handleClick = async () => { /* add to cart */ };
  return <button onClick={handleClick}>Add to Cart</button>;
}
```

## Data Fetching

### Server Component Fetching

```typescript
async function ProductsPage() {
  const products = await fetch(`${STORE_URL}/graphql`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${STOREFRONT_TOKEN}` },
    body: JSON.stringify({ query: PRODUCTS_QUERY }),
    next: { revalidate: 300 }, // ISR: revalidate every 5 minutes
  }).then(r => r.json());
  return <ProductGrid products={products.data.site.products} />;
}
```

### Caching & Revalidation

| Strategy | Use Case | Config |
|----------|----------|--------|
| **Static** | Rarely changing data | `{ cache: 'force-cache' }` |
| **ISR** | Product/category pages | `{ next: { revalidate: 300 } }` |
| **Dynamic** | Cart, checkout, account | `{ cache: 'no-store' }` |
| **On-Demand** | After webhook events | `revalidateTag('products')` |

### On-Demand Revalidation

Trigger revalidation from webhooks:
```typescript
// app/api/webhooks/route.ts
export async function POST(request: Request) {
  const body = await request.json();
  if (body.scope === 'store/product/updated') {
    revalidateTag('products');
  }
  return Response.json({ revalidated: true });
}
```

## API Routes

### Webhook Handlers

```typescript
// app/api/webhooks/orders/route.ts
export async function POST(request: Request) {
  const body = await request.json();
  // Verify webhook authenticity
  // Process order event
  return Response.json({ received: true });
}
```

### Proxy Routes

Proxy BigCommerce API calls to hide credentials:
```typescript
// app/api/products/route.ts
export async function GET() {
  const response = await fetch(`${BC_API_URL}/v3/catalog/products`, {
    headers: { 'X-Auth-Token': process.env.BC_ACCESS_TOKEN! },
  });
  const data = await response.json();
  return Response.json(data);
}
```

## Middleware

### Authentication

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth_token');
  if (request.nextUrl.pathname.startsWith('/account') && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}
```

### Geolocation / Channel Routing

Route users to the correct channel based on locale or region.

## Image Optimization

```typescript
import Image from 'next/image';

<Image
  src={product.imageUrl}
  alt={product.name}
  width={500}
  height={500}
  priority={isAboveFold} // Preload for LCP images
/>
```

Configure `remotePatterns` in `next.config.js` for BigCommerce CDN domains.

## Environment Variables

```
# .env.local
BIGCOMMERCE_STORE_HASH=abc123
BIGCOMMERCE_ACCESS_TOKEN=xxx        # Server-only (no NEXT_PUBLIC_ prefix)
NEXT_PUBLIC_STORE_URL=https://...   # Available in browser
BIGCOMMERCE_STOREFRONT_TOKEN=yyy    # Client-side GraphQL
```

## Catalyst-Specific Patterns

### GraphQL Client

Catalyst includes a typed GraphQL client:
- Queries in `client/queries/` directory
- Mutations in `client/mutations/` directory
- Auto-generated types from GraphQL schema

### Component Library

Catalyst provides pre-built components:
- Product cards, galleries, options
- Cart drawer, cart page
- Navigation, breadcrumbs, search
- Customer account pages

## Best Practices

- Use Server Components by default — add `'use client'` only when needed
- Fetch data in Server Components — pass data down to Client Components as props
- Use ISR for product/category pages — balance freshness and build speed
- Use on-demand revalidation with BigCommerce webhooks
- Keep API tokens server-side — never expose via `NEXT_PUBLIC_` prefix
- Use `next/image` for automatic optimization
- Implement loading states with `loading.tsx` or Suspense
- Handle errors gracefully with `error.tsx` boundaries

Fetch the Next.js documentation and Catalyst source for exact API, configuration options, and current patterns before implementing.
