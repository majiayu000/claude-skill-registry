---
name: treido-structure
description: Treido project structure specialist. Use for file placement, boundaries, naming, and import organization. Not for feature implementation.
---

# treido-structure

Project architect expertise — knows exactly where everything belongs in Treido.

## When to Apply

- Creating new files
- Deciding component placement
- Understanding project layout
- Debugging import issues
- File naming questions

## Domain Expertise

### App Structure (AUTHORITATIVE)

```
app/
├── [locale]/              # i18n routing (bg, en)
│   ├── (main)/           # Public layout group
│   │   ├── page.tsx      # Route page
│   │   └── _components/  # Route-private UI
│   ├── (auth)/           # Auth layout group
│   └── (seller)/         # Seller layout group
├── actions/              # Shared server actions
├── api/                  # Route handlers
└── globals.css           # Tailwind tokens SSOT
```

### Component Placement Decision Tree

```
Is it a shadcn primitive (Button, Card, Input)?
  └─ Yes → components/ui/
  └─ No → Is it reusable across routes?
      └─ Yes → components/shared/
      └─ No → app/[locale]/(group)/route/_components/
```

| Type | Location | Rule |
|------|----------|------|
| shadcn primitive | `components/ui/` | No app logic |
| Reusable composite | `components/shared/` | Can import ui/, lib/ |
| Route-private | `app/**/_components/` | Not exported |
| Layout shell | `components/layout/` | Header, Footer |

### Server Actions & API

| Type | Location | Naming |
|------|----------|--------|
| Server actions | `app/actions/*.ts` | verbNoun.ts |
| Route handlers | `app/api/**/route.ts` | Always `route.ts` |
| Webhooks | `app/api/webhook/*/route.ts` | By provider |

### Support Locations

| Purpose | Location |
|---------|----------|
| Supabase clients | `lib/supabase/server.ts` |
| Pure utilities | `lib/utils/` |
| Custom hooks | `hooks/` |
| i18n messages | `messages/{en,bg}.json` |

### Import Rules

| Rule | Example |
|------|---------|
| Absolute imports | `@/components/ui/button` |
| No barrel imports | Import from file directly |
| Layer boundaries | `ui/` never imports `app/` or `lib/` |

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `ProductCard.tsx` |
| Hooks | use* | `useCart.ts` |
| Actions | camelCase verb | `addToCart.ts` |
| Route handlers | `route.ts` | Always exactly this |
| Private folders | `_` prefix | `_components/` |

## ✅ Do

```tsx
// Correct placement
import { Button } from '@/components/ui/button';
import { ProductCard } from '@/components/shared/product-card';
import { addToCart } from '@/app/actions/cart';
```

## ❌ Don't

```tsx
// Barrel import
import { Button } from '@/components/ui';

// Wrong layer
// In components/ui/button.tsx:
import { formatPrice } from '@/lib/utils';  // ui/ shouldn't import lib/
```

## Review Checklist

- New files follow the placement decision tree
- `components/ui/*` stays primitive-only (no app logic imports)
- Imports use `@/` and avoid barrels
