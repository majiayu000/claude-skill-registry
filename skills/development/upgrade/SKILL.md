---
name: next-upgrade
description: Next.js version migrations using official guides and codemods.
metadata:
  labels: [nextjs, upgrade, migration, codemods]
  triggers:
    files: ['package.json']
    keywords: [next upgrade, migration guide, codemod]
---

# Next.js Upgrade Protocol

Automated and manual migration steps for Next.js version upgrades (e.g., v14 → v15).

## **Priority: P1 (OPERATIONAL)**

## **1. Detection & Planning**

- Check `package.json` for current `next`, `react`, and `react-dom` versions.
- **Incremental Upgrades**: Jumps across multiple major versions (e.g., 13 → 15) MUST be done incrementally (13 → 14 then 14 → 15).

## **2. Automated Codemods**

Run Next.js codemods to handle breaking syntax changes:

```bash
npx @next/codemod@latest <transform> <path>
```

**Common Transforms (v15):**

- `next-async-request-api`: Transforms `params`, `searchParams`, `cookies()`, and `headers()` into awaited Promises.
- `next-request-geo-ip`: Migrates legacy geo/ip properties.
- `next-dynamic-access-named-export`: Fixes dynamic import syntax.

## **3. Dependency Update**

Upgrade Next.js and peer dependencies in sync:

```bash
# Using npm
npm install next@latest react@latest react-dom@latest

# Update Types
npm install --save-dev @types/react@latest @types/react-dom@latest
```

## **4. Manual Verification Rules**

1. **Async Context**: Verify all uses of `cookies()`, `headers()`, and route `params` are now awaited.
2. **Metadata**: Ensure `generateMetadata` types match the new async `params` signature.
3. **Caching**: In v15+, `fetch` defaults to `{ cache: 'no-store' }`. If you need the old behavior, explicitly set `{ cache: 'force-cache' }`.

## **5. Testing Build**

- Run `npm run build` immediately after codemods and package updates.
- Check for "Hydration failed" or "Turbopack" compatibility errors if using `--turbo`.
