---
name: Next.js Rendering Strategies
description: SSG, SSR, ISR, Streaming, and Partial Prerendering (PPR).
metadata:
  labels: [nextjs, rendering, isr, ssr, ssg]
  triggers:
    files: ['**/page.tsx', '**/layout.tsx']
    keywords: [generateStaticParams, dynamic, dynamicParams, PPR, streaming]
---

# Rendering Strategies (App Router)

## **Priority: P0 (CRITICAL)**

Choose rendering strategy based on data freshness and scaling needs. See [Strategy Matrix](references/strategy-matrix.md).

## Guidelines

- **SSG (Default)**: Build-time render. Use `generateStaticParams`.
- **SSR**: Per-request render. Triggered by `cookies()`, `headers()`, or `cache: 'no-store'`.
- **Streaming**: Wrap slow components in `<Suspense>` to avoid blocking.
- **ISR**: Post-build updates. Use `revalidate` (time) or `revalidatePath` (on-demand).
- **PPR**: Static shell + dynamic holes. Experimental `ppr` config.
- **Runtime**: Node.js (Full) or Edge (Lighter/Faster).

## Scaling & Hydration

- **Static Shell**: Render layout as static, personalize via Suspense.
- **Error Boundaries**: Use `error.tsx` with `reset()` to catch runtime errors.
- **Hydration Safety**: Avoid `typeof window` or `Date.now()` in initial render. Use `useEffect`.

## Anti-Patterns

- **No Root Awaits**: Avoid waterfalls in `page.tsx`. Use Streaming.
- **Bailouts**: Understand [Suspense Bailout Rules](references/SUSPENSE_BAILOUT.md).

## References

- [Strategy Selection Matrix](references/strategy-matrix.md)
- [Implementation Details](references/implementation-details.md)
- [Scaling Patterns](references/scaling-patterns.md)
