---
name: bc-performance
description: Optimize BigCommerce storefront performance — CDN, image optimization, lazy loading, Stencil theme optimization, API response caching, GraphQL query efficiency, and Core Web Vitals. Use when improving store speed or diagnosing performance issues.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Performance Optimization

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.bigcommerce.com performance` for performance guide
2. Web-search `bigcommerce stencil theme performance optimization` for theme tuning
3. Web-search `bigcommerce core web vitals optimization` for CWV improvements

## Platform-Level Performance

### BigCommerce CDN

BigCommerce automatically serves storefronts via its global CDN:
- Static assets (JS, CSS, images) cached at edge
- Akamai-powered infrastructure
- Automatic HTTPS/SSL
- No CDN configuration needed from developers

### Server-Side Rendering

Stencil themes are server-rendered by BigCommerce:
- HTML generated on BigCommerce infrastructure
- Response times depend on template complexity and front matter data
- Minimize front matter requests for faster server response

## Stencil Theme Optimization

### Reduce Front Matter Data

Front matter declares what data to load per page — only request what you need:
- Remove unused front matter sections (e.g., `related_products` if not displayed)
- Reduce `limit` values to minimum needed
- Use `{{#if}}` to conditionally render sections, but note the data is still fetched

### JavaScript Optimization

- **Bundle size**: minimize third-party dependencies
- **Code splitting**: use dynamic imports for page-specific code
- **Defer non-critical JS**: use `defer` or `async` attributes
- **Remove unused jQuery plugins** if the theme ships jQuery
- **Tree shaking**: ensure webpack is configured for dead code elimination

### CSS Optimization

- Remove unused SCSS — audit with coverage tools
- Minimize use of `@extend` (causes CSS bloat)
- Use CSS custom properties for runtime theming instead of SCSS variables where appropriate
- Critical CSS: inline above-the-fold styles

### Image Optimization

- Use BigCommerce's image CDN — images are auto-resized via `{{getImage}}` helper
- Specify appropriate image dimensions: `{{getImage product.image 'product_size'}}`
- Use modern formats: BigCommerce CDN serves WebP when supported
- Lazy load below-the-fold images: `loading="lazy"`
- Use responsive images with `srcset` and `sizes`

### Template Optimization

- Minimize Handlebars helper nesting depth
- Reduce the number of partials per page
- Cache computed values — don't repeat the same helper call
- Use `{{#if}}` to skip rendering for empty data

## API Performance

### REST API Optimization

- Use `include` to fetch sub-resources in one request (avoid N+1)
- Use `include_fields` / `exclude_fields` to reduce response payload
- Implement caching for read-heavy data (products, categories)
- Respect rate limits — batch operations where possible
- Use webhooks instead of polling for real-time data

### GraphQL Optimization

- Request only needed fields — avoid over-fetching
- Use pagination (`first`/`after`) — never request all items
- Use fragments for reusable field sets
- Be aware of query complexity limits
- Cache GraphQL responses on your side (Catalyst uses Next.js caching)

### Caching Patterns

| Data Type | Cache Strategy | TTL |
|-----------|---------------|-----|
| Product catalog | CDN / ISR | 5–60 minutes |
| Category tree | CDN / ISR | 5–60 minutes |
| Cart | No cache | Real-time |
| Customer data | No cache | Real-time |
| Store settings | Long cache | 1–24 hours |
| Static assets | CDN | Long-term (versioned) |

## Core Web Vitals

### LCP (Largest Contentful Paint)

- Optimize hero images: correct size, preload, no lazy load
- Minimize server response time (reduce front matter)
- Preload critical fonts: `<link rel="preload" href="font.woff2" as="font">`

### FID / INP (Interaction to Next Paint)

- Minimize main thread blocking — defer heavy JS
- Break up long tasks
- Use `requestIdleCallback` for non-critical work
- Reduce JavaScript bundle size

### CLS (Cumulative Layout Shift)

- Set explicit dimensions on images and embeds
- Reserve space for dynamic content (ads, lazy-loaded elements)
- Avoid inserting content above existing content
- Use `font-display: swap` with size-adjusted fallback fonts

## Headless (Catalyst) Performance

### Next.js Optimizations

- **Static Generation**: pre-render product/category pages at build
- **ISR**: revalidate on interval for fresh data without full rebuild
- **Edge Functions**: run logic at CDN edge
- **Image Optimization**: `next/image` for automatic resizing, WebP, lazy loading
- **Font Optimization**: `next/font` for zero-CLS web fonts

### GraphQL Caching in Catalyst

- Server-side: Next.js data cache with revalidation
- Client-side: SWR or React Query for client-fetched data
- Storefront API responses can be cached at CDN level

## Best Practices

- Measure before optimizing — use Lighthouse, WebPageTest, Chrome DevTools
- Minimize front matter data — only fetch what the page displays
- Lazy load images below the fold
- Defer non-critical JavaScript
- Reduce third-party script impact (analytics, chat, pixels)
- Use BigCommerce CDN for all assets — don't self-host
- Cache API responses for read-heavy data
- Use ISR/SSG for headless storefronts
- Monitor Core Web Vitals in Google Search Console
- Test performance across device types and connection speeds

Fetch the BigCommerce performance documentation and Stencil optimization guide for current CDN features, image handling, and performance best practices before implementing.
