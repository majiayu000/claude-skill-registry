---
name: feature-slicing
description: |
  Apply Feature-Sliced Design (FSD) architecture to frontend projects. Triggers on: FSD, feature slicing,
  frontend architecture, layer structure, module boundaries, scalable frontend, slice organization.

  Use when: creating new features/components/pages, restructuring React/Next.js/Vue/Remix projects,
  organizing frontend code, setting up project structure, fixing import violations, or migrating legacy codebases.
---

# Feature-Sliced Design Architecture

Frontend architecture methodology with strict layer hierarchy and import rules for scalable, maintainable applications. FSD organizes code by **business domain** rather than technical role.

> **Official Docs:** [feature-sliced.design](https://feature-sliced.design) | **GitHub:** [feature-sliced](https://github.com/feature-sliced)

---

## THE IMPORT RULE (Critical)

**Modules can ONLY import from layers strictly below them. Never sideways or upward.**

```
app → pages → widgets → features → entities → shared
 ↓      ↓        ↓          ↓          ↓         ✓
 ✓      ✓        ✓          ✓          ✓      (external only)
```

| Violation | Example | Fix |
|-----------|---------|-----|
| Cross-slice (same layer) | `features/auth` → `features/user` | Extract to `entities/` or `shared/` |
| Upward import | `entities/user` → `features/auth` | Move shared code down |
| Shared importing up | `shared/` → `entities/` | Shared has NO internal deps |

**Exception:** `app/` and `shared/` have no slices, so internal cross-imports are allowed within them.

---

## Layer Hierarchy

| Layer | Purpose | Has Slices | Required |
|-------|---------|------------|----------|
| `app/` | Initialization, routing, providers, global styles | No | Yes |
| `pages/` | Route-based screens (one slice per route) | Yes | Yes |
| `widgets/` | Complex reusable UI blocks (header, sidebar) | Yes | No |
| `features/` | User interactions with business value (login, checkout) | Yes | No |
| `entities/` | Business domain models (user, product, order) | Yes | No |
| `shared/` | Project-agnostic infrastructure (UI kit, API client, utils) | No | Yes |

**Minimal setup:** `app/`, `pages/`, `shared/` — add other layers as complexity grows.

---

## Quick Decision Trees

### "Where does this code go?"

```
Code Placement:
├─ App-wide config, providers, routing    → app/
├─ Full page / route component            → pages/
├─ Complex reusable UI block              → widgets/
├─ User action with business value        → features/
├─ Business domain object (data model)    → entities/
└─ Reusable, domain-agnostic code         → shared/
```

### "Feature or Entity?"

| Entity (noun) | Feature (verb) |
|---------------|----------------|
| `user` — user data model | `auth` — login/logout actions |
| `product` — product info | `add-to-cart` — adding to cart |
| `comment` — comment data | `write-comment` — creating comments |
| `order` — order record | `checkout` — completing purchase |

**Rule:** Entities represent THINGS with identity. Features represent ACTIONS with side effects.

### "Which segment?"

```
Segments (within a slice):
├─ ui/      → React components, styles
├─ api/     → Backend calls, data fetching, DTOs
├─ model/   → Types, schemas, stores, business logic
├─ lib/     → Slice-specific utilities
└─ config/  → Feature flags, constants
```

**Naming:** Use purpose-driven names (`api/`, `model/`) not essence-based (`hooks/`, `types/`).

---

## Directory Structure

```
src/
├── app/                    # App layer (no slices)
│   ├── providers/          # React context, QueryClient, theme
│   ├── routes/             # Router configuration
│   └── styles/             # Global CSS, theme tokens
├── pages/                  # Page slices
│   └── {page-name}/
│       ├── ui/             # Page components
│       ├── api/            # Loaders, server actions
│       ├── model/          # Page-specific state
│       └── index.ts        # Public API
├── widgets/                # Widget slices
│   └── {widget-name}/
│       ├── ui/             # Composed UI
│       └── index.ts
├── features/               # Feature slices
│   └── {feature-name}/
│       ├── ui/             # Feature UI
│       ├── api/            # Feature API calls
│       ├── model/          # State, schemas
│       └── index.ts
├── entities/               # Entity slices
│   └── {entity-name}/
│       ├── ui/             # Entity UI (Card, Avatar)
│       ├── api/            # CRUD operations
│       ├── model/          # Types, mappers, validation
│       └── index.ts
└── shared/                 # Shared layer (no slices)
    ├── ui/                 # Design system components
    ├── api/                # API client, interceptors
    ├── lib/                # Utilities (dates, validation)
    ├── config/             # Environment, constants
    ├── routes/             # Route path constants
    └── i18n/               # Translations
```

---

## Public API Pattern

Every slice MUST expose a public API via `index.ts`. External code imports ONLY from this file.

```typescript
// entities/user/index.ts
export { UserCard } from './ui/UserCard';
export { UserAvatar } from './ui/UserAvatar';
export { getUser, updateUser } from './api/userApi';
export type { User, UserRole } from './model/types';
export { userSchema } from './model/schema';
```

```typescript
// ✅ Correct
import { UserCard, type User } from '@/entities/user';

// ❌ Wrong
import { UserCard } from '@/entities/user/ui/UserCard';
```

**Avoid wildcard exports** — they expose internals and harm tree-shaking:
```typescript
// ❌
export * from './ui';

// ✅
export { UserCard } from './ui/UserCard';
```

---

## Cross-Entity References (@x Notation)

When entities legitimately reference each other, use the `@x` notation:

```
entities/
├── product/
│   ├── @x/
│   │   └── order.ts    # API specifically for order entity
│   └── index.ts
└── order/
    └── model/types.ts  # Imports from product/@x/order
```

```typescript
// entities/product/@x/order.ts
export type { ProductId } from '../model/types';

// entities/order/model/types.ts
import type { ProductId } from '@/entities/product/@x/order';
```

**Guidelines:** Keep cross-imports minimal. Consider merging entities if references are extensive.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Cross-slice import | `features/a` → `features/b` | Extract shared logic down |
| Generic segments | `components/`, `hooks/` | Use `ui/`, `lib/`, `model/` |
| Wildcard exports | `export * from './button'` | Explicit named exports |
| Business logic in shared | Domain logic in `shared/lib` | Move to `entities/` |
| Single-use widgets | Widget used by one page | Keep in page slice |
| Skipping public API | Import from internal paths | Always use `index.ts` |
| Making everything a feature | All interactions as features | Only reused actions |

---

## TypeScript Configuration

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

## Reference Documentation

| File | Purpose |
|------|---------|
| [references/LAYERS.md](references/LAYERS.md) | Complete layer specifications, flowcharts |
| [references/PUBLIC-API.md](references/PUBLIC-API.md) | Export patterns, @x notation, tree-shaking |
| [references/IMPLEMENTATION.md](references/IMPLEMENTATION.md) | Code patterns: entities, features, React Query |
| [references/NEXTJS.md](references/NEXTJS.md) | App Router integration, page re-exports |
| [references/MIGRATION.md](references/MIGRATION.md) | Incremental migration strategy |
| [references/CHEATSHEET.md](references/CHEATSHEET.md) | Quick reference, import matrix |

## Resources

### Official Sources
- **Official Documentation**: https://feature-sliced.design
- **GitHub Organization**: https://github.com/feature-sliced
- **Official Examples**: https://github.com/feature-sliced/examples
- **Specification**: https://feature-sliced.design/docs/reference

### Community
- **Awesome FSD**: https://github.com/feature-sliced/awesome (curated articles, videos, tools)
