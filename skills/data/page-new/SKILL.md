---
name: page-new
description: "Create a new Next.js page with App Router best practices"
---

# Create New Page

Generate a new Next.js 15 page following modern App Router patterns.

## Page Specification

$ARGUMENTS

## Next.js 15 App Router Standards

### 1. **File Structure**
```
app/
   [route]/
      page.tsx          # Main page component
      layout.tsx        # Layout (optional)
      loading.tsx       # Loading UI
      error.tsx         # Error UI
      not-found.tsx     # 404 UI
```

### 2. **Server Components by Default**
- Fetch data directly in components
- No need for getServerSideProps/getStaticProps
- Async components supported
- Better performance

### 3. **Metadata**
```typescript
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description for SEO',
  openGraph: { /* OG tags */ }
}
```

### 4. **Data Fetching Patterns**

**Server Component** (preferred)
```typescript
async function Page() {
  const data = await fetchData()
  return <div>{data}</div>
}
```

**Client Component** (when needed)
```typescript
'use client'
function Page() {
  const { data } = useSWR('/api/data')
  return <div>{data}</div>
}
```

## What to Generate

1. **Page Component** - `app/[route]/page.tsx`
2. **TypeScript Types** - Props and data types
3. **Loading State** - `loading.tsx`
4. **Error Boundary** - `error.tsx`
5. **Metadata** - SEO and OG tags
6. **Example Data Fetching** - Server or client patterns

## Page Patterns

**Static Page** (default)
- Pre-rendered at build time
- Best for marketing pages, blogs
- Fast performance

**Dynamic Page** (revalidation)
```typescript
export const revalidate = 60 // Revalidate every 60 seconds
```

**Dynamic Route** (`[slug]`)
```typescript
export async function generateStaticParams() {
  // Generate paths at build time
}
```

**Streaming** (with Suspense)
```typescript
<Suspense fallback={<Loading />}>
  <AsyncComponent />
</Suspense>
```

## Best Practices

**Structure**
- Server Components for data fetching
- Client Components only when needed ('use client')
- Streaming with Suspense for slow data
- Parallel data fetching
- Proper TypeScript typing

**Performance**
- Image optimization (next/image)
- Font optimization (next/font)
- Lazy loading below the fold
- Code splitting automatically
- Prefetch links (default behavior)

**SEO**
- Metadata for every page
- Semantic HTML
- Open Graph tags
- Structured data (JSON-LD)
- Alt text for images

**Error Handling**
- error.tsx for runtime errors
- not-found.tsx for 404s
- Graceful degradation
- User-friendly error messages

**Accessibility**
- Semantic HTML5 elements
- ARIA labels
- Keyboard navigation
- Focus management

## When to Use Client Components

Use `'use client'` when you need:
- Event listeners (onClick, onChange, etc.)
- State hooks (useState, useReducer)
- Effect hooks (useEffect, useLayoutEffect)
- Browser-only APIs (localStorage, window)
- Custom hooks that use above

Otherwise, use Server Components (default).

## Styling Integration

Choose based on project:
- **Tailwind CSS** - Utility classes (recommended)
- **CSS Modules** - Scoped styles
- **Styled Components** - CSS-in-JS (requires 'use client')

Generate a complete, production-ready Next.js page with proper TypeScript types, error handling, and SEO optimization.
