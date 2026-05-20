---
name: registry-system
description: |
  Auto-generated registry system for this Next.js application.
  Covers Data-Only pattern, zero dynamic imports policy, registry structure, and rebuild process.
  Use this skill when working with registries or understanding import patterns.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Registry System Skill

Patterns for working with the auto-generated registry system that provides O(1) lookups for blocks, entities, themes, and more.

## Architecture Overview

```
REGISTRY SYSTEM (Pre-built at build time):

core/lib/registries/
├── block-registry.ts        # BLOCK_REGISTRY - Page builder blocks
├── entity-registry.ts       # ENTITY_REGISTRY - Entity configurations
├── entity-registry.client.ts # Client-safe entity registry
├── theme-registry.ts        # THEME_REGISTRY - Theme configurations
├── plugin-registry.ts       # PLUGIN_REGISTRY - Plugin configurations
├── namespace-registry.ts    # NAMESPACE_REGISTRY - Route namespaces
├── scope-registry.ts        # SCOPE_REGISTRY - API scopes
├── route-handlers.ts        # ROUTE_HANDLERS - API route handlers
├── middleware-registry.ts   # MIDDLEWARE_REGISTRY - Middleware configs
├── permissions-registry.ts  # PERMISSIONS_REGISTRY - Permission matrix
├── billing-registry.ts      # BILLING_REGISTRY - Plans and billing
├── translation-registry.ts  # TRANSLATION_REGISTRY - i18n configs
├── testing-registry.ts      # TESTING_REGISTRY - Test fixtures
├── docs-registry.ts         # DOCS_REGISTRY - Documentation index
└── index.ts                 # Unified exports

Build script: node core/scripts/build/registry.mjs
```

> **📍 Context-Aware Paths:** Registries are auto-generated from core + theme. In consumer projects,
> theme configs go in `contents/themes/{theme}/config/`. Core registries are read-only.
> See `core-theme-responsibilities` skill for complete rules.

## When to Use This Skill

- Understanding registry patterns
- Importing from registries correctly
- Debugging registry generation issues
- Working with entity, block, or theme configurations
- Avoiding dynamic import violations

## Key Concepts

### Data-Only Pattern

```
Registries = Data (pre-computed, static)
Services = Logic (methods that use registries)
```

**Registries provide:**
- O(1) lookups by key
- Type-safe TypeScript interfaces
- Pre-computed at build time
- Zero runtime I/O

**Services provide:**
- Business logic methods
- Filtering and querying
- Validation and transformation

### Performance Impact

| Approach | Time | Notes |
|----------|------|-------|
| Dynamic Import | ~140ms | Per operation, I/O bound |
| Static Registry | ~6ms | O(1) lookup |
| **Improvement** | **~17,255x** | Build-time vs runtime |

## Import Patterns

### Correct Usage

```typescript
// ✅ CORRECT - Import from registries
import { BLOCK_REGISTRY } from '@/core/lib/registries/block-registry'
import { ENTITY_REGISTRY } from '@/core/lib/registries/entity-registry'
import { THEME_REGISTRY } from '@/core/lib/registries/theme-registry'

// Access by key
const heroBlock = BLOCK_REGISTRY['hero']
const customerEntity = ENTITY_REGISTRY['customers']

// ✅ CORRECT - Use services for logic
import { BlockService } from '@/core/lib/services/block.service'
import { EntityTypeService } from '@/core/lib/services/entity-type.service'

const heroConfig = BlockService.getBySlug('hero')
const allEntities = EntityTypeService.getAll()
```

### Forbidden Patterns

```typescript
// ❌ FORBIDDEN - Direct imports from @/contents
import { hero } from '@/contents/themes/default/blocks/hero'
import { customerEntityConfig } from '@/contents/themes/default/entities/customers'
import * as theme from '@/contents/themes/default'

// ❌ FORBIDDEN - Dynamic imports from @/contents
const module = await import('@/contents/themes/default/blocks/hero')
const config = await import(`@/contents/themes/${themeName}/config`)

// ❌ FORBIDDEN - Dynamic registry imports
const { ENTITY_REGISTRY } = await import('@/core/lib/registries/entity-registry')
```

## Available Registries

| Registry | Key Type | Value Type | Purpose |
|----------|----------|------------|---------|
| `BLOCK_REGISTRY` | slug | `BlockConfig` | Page builder blocks |
| `ENTITY_REGISTRY` | slug | `EntityRegistryEntry` | Entity configurations |
| `THEME_REGISTRY` | name | `ThemeConfig` | Theme settings |
| `PLUGIN_REGISTRY` | name | `PluginConfig` | Plugin configurations |
| `NAMESPACE_REGISTRY` | namespace | `NamespaceConfig` | Route namespaces |
| `SCOPE_REGISTRY` | scope | `ScopeConfig` | API permission scopes |
| `PERMISSIONS_REGISTRY` | permission | `PermissionConfig` | Permission definitions |
| `BILLING_REGISTRY` | planSlug | `PlanConfig` | Billing plans |
| `MIDDLEWARE_REGISTRY` | name | `MiddlewareConfig` | Route middlewares |
| `ROUTE_HANDLERS` | path | `RouteHandler` | API route handlers |

## Registry Structure

### Typical Registry File

```typescript
/**
 * Auto-generated Entity Registry
 * Generated at: 2025-12-30T21:56:23.717Z
 * Entities discovered: 4
 * DO NOT EDIT - This file is auto-generated by scripts/build-registry.mjs
 */

// 1. Static imports (generated)
import { customerEntityConfig } from '@/contents/themes/default/entities/customers/customers.config'
import { taskEntityConfig } from '@/contents/themes/default/entities/tasks/tasks.config'

// 2. TypeScript interface
export interface EntityRegistryEntry {
  name: string
  config: EntityConfig
  tableName?: string
  relativePath: string
  depth: number
  parent: string | null
  children: string[]
  source: 'core' | 'theme' | 'plugin'
}

// 3. Main registry object
export const ENTITY_REGISTRY: Record<string, EntityRegistryEntry> = {
  'customers': {
    name: 'customers',
    config: customerEntityConfig,
    tableName: 'customers',
    relativePath: 'customers',
    depth: 0,
    parent: null,
    children: [],
    source: 'theme'
  },
  // ... more entries
}

// 4. Type export
export type EntityName = keyof typeof ENTITY_REGISTRY

// 5. Metadata
export const ENTITY_METADATA = {
  totalEntities: 4,
  generatedAt: '2025-12-30T21:56:23.717Z',
  entities: ['customers', 'pages', 'posts', 'tasks']
}
```

## Rebuild Command

```bash
# One-time build (default)
node core/scripts/build/registry.mjs

# Watch mode (auto-rebuild on changes)
node core/scripts/build/registry.mjs --watch

# Build with verbose output
node core/scripts/build/registry.mjs --verbose
```

**When to rebuild:**
- After adding/removing entities
- After adding/removing blocks
- After modifying entity configs
- After changing theme configurations
- After adding/removing plugins

## Allowed Exceptions

### 1. i18n/Translations (Lazy-load per locale)
```typescript
const messages = await import(`@/core/messages/${locale}/${namespace}.json`)
```

### 2. React Code-Splitting (>100KB components)
```typescript
const HeavyChart = lazy(() => import('./HeavyChart'))
```

### 3. Type-Only Imports (Eliminated at compile)
```typescript
export type Messages = typeof import('./es/index.ts').default
```

### 4. Build Scripts Only (Development)
```typescript
// core/scripts/build-theme.ts
const config = await import(`./${themeName}/theme.config`)
```

### 5. Development Tools (NODE_ENV gated)
```typescript
if (process.env.NODE_ENV === 'development') {
  const benchmark = await import('./dev-tools/benchmark')
}
```

### 6. Heavy User-Triggered Libraries (>500KB)
```typescript
export async function extractTextFromPDF(file: File) {
  const pdfjsLib = await import('pdfjs-dist')  // ~2MB, only when needed
}
```

## Using Services with Registries

### BlockService

```typescript
import { BlockService } from '@/core/lib/services/block.service'

// Get block by slug
const hero = BlockService.getBySlug('hero')

// Get all blocks
const blocks = BlockService.getAll()

// Get blocks by category
const heroBlocks = BlockService.getByCategory('hero')

// Get blocks by scope
const pageBlocks = BlockService.getByScope('pages')
```

### EntityTypeService

```typescript
import { EntityTypeService } from '@/core/lib/services/entity-type.service'

// Get entity config
const customerConfig = EntityTypeService.getBySlug('customers')

// Get all entities
const entities = EntityTypeService.getAll()

// Check if entity exists
const exists = EntityTypeService.exists('customers')
```

## Anti-Patterns

```typescript
// NEVER: Import directly from contents
import { hero } from '@/contents/themes/default/blocks/hero'

// CORRECT: Use registry
import { BLOCK_REGISTRY } from '@/core/lib/registries/block-registry'
const hero = BLOCK_REGISTRY['hero']

// NEVER: Dynamic import from contents
const block = await import(`@/contents/themes/${theme}/blocks/${slug}`)

// CORRECT: Use service
import { BlockService } from '@/core/lib/services/block.service'
const block = BlockService.getBySlug(slug)

// NEVER: Modify registry files manually
// Registry files have "DO NOT EDIT" header

// CORRECT: Modify source files and rebuild
// node core/scripts/build/registry.mjs

// NEVER: Store logic in registries
export const ENTITY_REGISTRY = {
  customers: {
    validate: (data) => { ... }  // Logic doesn't belong here!
  }
}

// CORRECT: Logic goes in services
export class CustomerService {
  static validate(data: CreateCustomer) { ... }
}
```

## Checklist

Before working with registries:

- [ ] Importing from `@/core/lib/registries/` not `@/contents/`
- [ ] Using services for logic, registries for data
- [ ] Rebuilding after config changes (`node core/scripts/build/registry.mjs`)
- [ ] Not modifying auto-generated registry files
- [ ] Using typed registry keys (e.g., `ENTITY_REGISTRY['customers']`)
- [ ] Checking registry exists before accessing (or using services)

## Related Skills

- **`monorepo-architecture`** - Package hierarchy, dependency rules, Model B distribution
- `entity-system` - Entity configuration patterns
- `page-builder-blocks` - Block configuration patterns
- `service-layer` - Service patterns with registries
