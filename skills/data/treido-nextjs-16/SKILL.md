---
name: treido-nextjs-16
description: Next.js 16 App Router specialist for Treido. Use for routing, layouts, Server vs Client Components, caching ('use cache'), and request entrypoints (proxy.ts). Not for styling.
---

# treido-nextjs-16

Deep expertise in Next.js 16 App Router patterns.

## Core Knowledge

### Request Hook (CRITICAL)

**Treido uses `proxy.ts`, NOT `middleware.ts`**.

| File | Role | Status |
|------|------|--------|
| `proxy.ts` | Request routing, i18n, auth | ✅ Active |
| `middleware.ts` | N/A | ❌ Do not create |

This is an intentional repo convention. Do not suggest adding a root `middleware.ts` unless explicitly requested.

### Component Types (I KNOW THIS)

| Type | Directive | Can Use |
|------|-----------|---------|
| Server Component | None (default) | async/await, DB, secrets, fetch |
| Client Component | `'use client'` | hooks, events, browser APIs |

**Default to Server Components**. Add `'use client'` only when needed.

### Caching (AUTHORITATIVE)

Next.js 16 caching uses `'use cache'` + profiles:

```tsx
'use cache';
import { cacheLife, cacheTag } from 'next/cache';

export async function getProduct(id: string) {
  cacheLife('products');  // Profile from next.config.ts
  cacheTag(`product:${id}`);
  
  // Pure read, no auth
  const supabase = createStaticClient();
  return supabase.from('products').select('id, title, price').eq('id', id).single();
}
```

### Cache Constraints (CRITICAL)

`'use cache'` functions **CANNOT**:
- Call `cookies()`
- Call `headers()`  
- Access auth context
- Use `createClient()` (uses cookies)

`'use cache'` functions **CAN**:
- Use `createStaticClient()` (pure)
- Accept serializable params
- Return serializable data

### Revalidation (AUTHORITATIVE)

```tsx
import { revalidateTag, revalidatePath } from 'next/cache';

// After mutation
export async function updateProduct(id: string, data: ProductData) {
  // ... update logic
  
  revalidateTag(`product:${id}`);  // Specific product
  revalidateTag('products');       // Product listings
}
```

### Data Fetching Pattern

```tsx
// ✅ Server Component - direct fetch
async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await getProduct(id);  // Cached server function
  return <ProductView product={product} />;
}

// ❌ Client Component - avoid for initial data
'use client';
function ProductPage({ id }) {
  const [product, setProduct] = useState(null);
  useEffect(() => { fetchProduct(id).then(setProduct) }, [id]);  // Bad
}
```

### Route Groups (KNOWLEDGE)

```
app/[locale]/
├── (main)/           # Public layout
│   ├── layout.tsx    # Shared header/footer
│   └── products/
├── (auth)/           # Auth layout
│   ├── layout.tsx    # Minimal UI
│   └── login/
└── (seller)/         # Seller layout
    ├── layout.tsx    # Seller nav
    └── dashboard/
```

Groups with `(name)` don't affect URL.

## ✅ Do

```tsx
// Server Component with cached data
async function CategoryPage({ params }) {
  const { slug } = await params;
  const products = await getCategoryProducts(slug);
  return <ProductGrid products={products} />;
}

// Small client island for interactivity
'use client';
function FilterSidebar({ onFilterChange }) {
  const [filters, setFilters] = useState({});
  // Handle user interaction
}
```

## ❌ Don't

```tsx
// Don't make entire pages client components
'use client';
export default function ProductPage() {
  // Everything is now client-side
}

// Don't fetch in useEffect for initial data
useEffect(() => {
  fetch('/api/products').then(r => r.json()).then(setProducts);
}, []);

// Don't create middleware.ts
// middleware.ts - NO!
```

## Verification

Sanity-check after changes:
- No accidental `'use client'` on full pages
- Cached functions stay pure (no `cookies()`/`headers()`/auth)
- Routes/layouts behave correctly for both locales
