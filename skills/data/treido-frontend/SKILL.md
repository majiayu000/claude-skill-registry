---
name: treido-frontend
description: Build and modify Treido marketplace UI with Next.js 16 App Router, React 19, Tailwind v4, and shadcn/ui. Use when working on pages, components, layouts, styling, or i18n. Triggers include UI changes, component creation, styling fixes, adding user-facing text, fixing layout issues, or any work in app/[locale]/, components/, hooks/, or messages/ directories.
deprecated: true
---

# Treido Frontend

> Deprecated (2026-01-29). Use `treido-orchestrator` + `treido-impl-frontend` (and `treido-audit-*` + `treido-verify`).

## Quick Start

1. Identify the exact file(s) to modify
2. Check if Server or Client Component is needed
3. Make the change (1-3 files max per batch)
4. Run verification: `pnpm -s typecheck && pnpm -s lint && pnpm -s styles:gate`

## Decision Tree

```
Is this UI work?
├─ Yes → Which type?
│   ├─ New page/route → Create in app/[locale]/(group)/
│   ├─ Reusable component → components/shared/
│   ├─ Route-specific component → app/[locale]/(group)/**/_components/
│   ├─ shadcn primitive modification → components/ui/ (rare)
│   └─ Styling only → Check Tailwind v4 rules below
└─ No → Wrong skill. Use treido-backend or treido-supabase
```

## File Boundaries

| Type | Location | Rule |
|------|----------|------|
| Pages/routes | `app/[locale]/(group)/` | One page per route |
| Route-private UI | `app/[locale]/(group)/**/_components/` | Never import across route groups |
| Shared composites | `components/shared/` | Reusable across routes |
| shadcn primitives | `components/ui/` | No app logic, no hooks |
| Hooks | `hooks/` | Reusable client-side logic |
| i18n messages | `messages/en.json`, `messages/bg.json` | Always update both |

## Server vs Client Components

**Default to Server Components.** Add `"use client"` only when needed:

- Event handlers (onClick, onChange, etc.)
- React hooks (useState, useEffect, useRef)
- Browser-only APIs (window, localStorage)
- Third-party client libraries

Keep client boundaries small. Wrap only the interactive part.

## Tailwind v4 Rules (Non-Negotiable)

Run `pnpm -s styles:gate` to validate. These patterns are **forbidden**:

```tsx
// ❌ FORBIDDEN
className="bg-[#ff0000]"     // arbitrary color
className="p-[13px]"         // arbitrary spacing
className="bg-gradient-to-r" // gradients
className="text-blue-500"    // palette colors (use semantic tokens)

// ✅ CORRECT
className="bg-destructive"   // semantic token
className="p-4"              // standard spacing
className="text-foreground"  // semantic token
```

**For complete Tailwind v4 rules:** See [references/tailwind.md](references/tailwind.md)

## i18n (next-intl)

All user-facing strings must use `next-intl`:

```tsx
// ❌ FORBIDDEN
<p>Welcome to Treido</p>

// ✅ CORRECT
import { useTranslations } from 'next-intl';
const t = useTranslations('HomePage');
<p>{t('welcome')}</p>
```

Update both message files:
- `messages/en.json`
- `messages/bg.json`

## Caching Rules

For Server Components with `'use cache'`:

```tsx
// ✅ CORRECT
'use cache';
import { cacheLife, cacheTag } from 'next/cache';

export async function getCachedData() {
  cacheLife('hours');
  cacheTag('products');
  // ... fetch data
}

// ❌ FORBIDDEN inside cached functions
import { cookies, headers } from 'next/headers';
```

## Verification

After every change:

```bash
pnpm -s typecheck && pnpm -s lint && pnpm -s styles:gate
```

## Common Patterns

**For shadcn component patterns:** See [references/shadcn.md](references/shadcn.md)
**For Next.js App Router patterns:** See [references/nextjs.md](references/nextjs.md)
