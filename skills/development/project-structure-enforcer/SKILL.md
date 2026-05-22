---
name: project-structure-enforcer
description: Enforce 2026 folder structure standards - feature-based organization, max nesting depth, unidirectional imports. Blocks structural violations. Use when creating files or reviewing project architecture.
context: fork
agent: code-quality-reviewer
version: 1.0.0
author: SkillForge AI Agent Hub
tags: [structure, architecture, enforcement, blocking, imports, organization]
user-invocable: false
---
Enforce 2026 folder structure best practices with **BLOCKING** validation.

## Validation Rules

### BLOCKING Rules (exit 1)

| Rule | Check | Example Violation |
|------|-------|-------------------|
| **Max Nesting** | Max 4 levels from src/ or app/ | `src/a/b/c/d/e/file.ts` |
| **No Barrel Files** | No index.ts re-exports | `src/components/index.ts` |
| **Component Location** | React components in components/ or features/ | `src/utils/Button.tsx` |
| **Hook Location** | Custom hooks in hooks/ directory | `src/components/useAuth.ts` |
| **Import Direction** | Unidirectional: shared → features → app | `features/` importing from `app/` |

## Expected Folder Structures

### React/Next.js (Frontend)

```
src/
├── app/              # Next.js App Router (pages)
│   ├── (auth)/       # Route groups
│   ├── api/          # API routes
│   └── layout.tsx
├── components/       # Reusable UI components
│   ├── ui/           # Primitive components
│   └── forms/        # Form components
├── features/         # Feature modules (self-contained)
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types.ts
│   └── dashboard/
├── hooks/            # Global custom hooks
├── lib/              # Third-party integrations
├── services/         # API clients
├── types/            # Global TypeScript types
└── utils/            # Pure utility functions
```

### FastAPI (Backend)

```
app/
├── routers/          # API route handlers
│   ├── router_users.py
│   ├── router_auth.py
│   └── deps.py       # Shared dependencies
├── services/         # Business logic layer
│   ├── user_service.py
│   └── auth_service.py
├── repositories/     # Data access layer
│   ├── user_repository.py
│   └── base_repository.py
├── schemas/          # Pydantic models
│   ├── user_schema.py
│   └── auth_schema.py
├── models/           # SQLAlchemy models
│   ├── user_model.py
│   └── base.py
├── core/             # Config, security, deps
│   ├── config.py
│   ├── security.py
│   └── database.py
└── utils/            # Utility functions
```

## Nesting Depth Rules

Maximum 4 levels from `src/` or `app/`:

```
ALLOWED (4 levels):
  src/features/auth/components/LoginForm.tsx
  app/routers/v1/users/router_users.py

BLOCKED (5+ levels):
  src/features/dashboard/widgets/charts/line/LineChart.tsx
  ↳ Flatten to: src/features/dashboard/charts/LineChart.tsx
```

## No Barrel Files

Barrel files (`index.ts` that only re-export) cause tree-shaking issues with Vite/webpack:

```typescript
// BLOCKED: src/components/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Modal } from './Modal';

// GOOD: Import directly
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
```

**Why?** Barrel files:
- Break tree-shaking (entire barrel is imported)
- Cause circular dependency issues
- Slow down build times
- Make debugging harder

## Import Direction (Unidirectional Architecture)

Code must flow in ONE direction:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   shared/lib  →  components  →  features  →  app       │
│                                                         │
│   (lowest)                                 (highest)    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Allowed Imports

| Layer | Can Import From |
|-------|-----------------|
| `shared/`, `lib/` | Nothing (base layer) |
| `components/` | `shared/`, `lib/`, `utils/` |
| `features/` | `shared/`, `lib/`, `components/`, `utils/` |
| `app/` | Everything above |

### Blocked Imports

```typescript
// BLOCKED: shared/ importing from features/
// File: src/shared/utils.ts
import { authConfig } from '@/features/auth/config';  // ❌

// BLOCKED: features/ importing from app/
// File: src/features/auth/useAuth.ts
import { RootLayout } from '@/app/layout';  // ❌

// BLOCKED: Cross-feature imports
// File: src/features/auth/useAuth.ts
import { DashboardContext } from '@/features/dashboard/context';  // ❌
// Fix: Extract to shared/ if needed by multiple features
```

### Type-Only Imports (Exception)

Type-only imports across features are allowed:

```typescript
// ALLOWED: Type-only import from another feature
import type { User } from '@/features/users/types';
```

## Component Location Rules

### React Components (PascalCase .tsx)

```
ALLOWED:
  src/components/Button.tsx
  src/components/ui/Card.tsx
  src/features/auth/components/LoginForm.tsx
  src/app/dashboard/page.tsx

BLOCKED:
  src/utils/Button.tsx       # Components not in utils/
  src/services/Modal.tsx     # Components not in services/
  src/hooks/Dropdown.tsx     # Components not in hooks/
```

### Custom Hooks (useX pattern)

```
ALLOWED:
  src/hooks/useAuth.ts
  src/hooks/useLocalStorage.ts
  src/features/auth/hooks/useLogin.ts

BLOCKED:
  src/components/useAuth.ts   # Hooks not in components/
  src/utils/useDebounce.ts    # Hooks not in utils/
  src/services/useFetch.ts    # Hooks not in services/
```

## Python File Location Rules

### Routers

```
ALLOWED:
  app/routers/router_users.py
  app/routers/routes_auth.py
  app/routers/api_v1.py

BLOCKED:
  app/users_router.py          # Not in routers/
  app/services/router_users.py # Router in services/
```

### Services

```
ALLOWED:
  app/services/user_service.py
  app/services/auth_service.py

BLOCKED:
  app/user_service.py           # Not in services/
  app/routers/user_service.py   # Service in routers/
```

## Common Violations

### 1. Too Deep Nesting
```
BLOCKED: Max nesting depth exceeded: 5 levels (max: 4)
  File: src/features/dashboard/widgets/charts/line/LineChart.tsx
  Consider flattening: src/features/dashboard/charts/LineChart.tsx
```

### 2. Barrel File Created
```
BLOCKED: Barrel files (index.ts) discouraged - causes tree-shaking issues
  File: src/components/index.ts
  Import directly from source files instead
```

### 3. Component in Wrong Location
```
BLOCKED: React components must be in components/, features/, or app/
  File: src/utils/Button.tsx
  Move to: src/components/Button.tsx
```

### 4. Invalid Import Direction
```
BLOCKED: Import direction violation (unidirectional architecture)
  features/ cannot import from app/
  Import direction: features -> shared, lib, components

Allowed flow: shared/lib -> components -> features -> app
```

### 5. Cross-Feature Import
```
BLOCKED: Cannot import from other features (cross-feature dependency)
  File: src/features/auth/useAuth.ts
  Import: from '@/features/dashboard/context'
  Extract shared code to shared/ or lib/
```

## Migration Guide

### Flattening Deep Nesting

```bash
# Before (5 levels)
src/features/dashboard/widgets/charts/line/LineChart.tsx
src/features/dashboard/widgets/charts/line/LineChartTooltip.tsx

# After (4 levels) - Flatten last two levels
src/features/dashboard/charts/LineChart.tsx
src/features/dashboard/charts/LineChartTooltip.tsx
```

### Removing Barrel Files

```bash
# Before
src/components/index.ts  # Re-exports everything
import { Button, Input } from '@/components';

# After - Direct imports
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
```

### Fixing Cross-Feature Imports

```bash
# Before - Cross-feature dependency
src/features/auth/useAuth.ts imports from src/features/users/types

# After - Extract to shared
src/shared/types/user.ts
src/features/auth/useAuth.ts imports from src/shared/types/user
src/features/users/... imports from src/shared/types/user
```

## Related Skills

- `backend-architecture-enforcer` - FastAPI layer separation
- `clean-architecture` - DDD patterns
- `type-safety-validation` - TypeScript strictness

## Capability Details

### folder-structure
**Keywords:** folder structure, directory structure, project layout, organization
**Solves:**
- Enforce feature-based organization
- Validate proper file placement
- Maintain consistent project structure

### nesting-depth
**Keywords:** nesting, depth, levels, max depth, deep nesting
**Solves:**
- Limit directory nesting to 4 levels
- Prevent overly complex structures
- Improve navigability

### import-direction
**Keywords:** import, unidirectional, circular, dependency direction
**Solves:**
- Enforce unidirectional imports
- Prevent circular dependencies
- Maintain clean architecture

### component-location
**Keywords:** component location, file placement, where to put
**Solves:**
- Validate React component placement
- Enforce hook location rules
- Block barrel files
