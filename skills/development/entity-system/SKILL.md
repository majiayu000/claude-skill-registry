---
name: entity-system
description: |
  Config-driven entity system for creating automatic CRUDs.
  Includes: config, fields, types, service, messages (i18n), migrations.
  Use this skill to create, modify, or understand system entities.
allowed-tools: Read, Glob, Grep, Bash(python:*)
version: 1.0.0
---

# Entity System Skill

Config-driven system for defining entities with automatic CRUDs, similar to WordPress Custom Post Types.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          ENTITY CONFIGURATION                            │
│                                                                          │
│  contents/themes/{theme}/entities/{entity}/                              │
│  ├── {entity}.config.ts    ← Main configuration                          │
│  ├── {entity}.fields.ts    ← Field definitions                           │
│  ├── {entity}.types.ts     ← TypeScript types                            │
│  ├── {entity}.service.ts   ← Optional but recommended                    │
│  ├── messages/                                                           │
│  │   ├── en.json           ← English translations                        │
│  │   ├── es.json           ← Spanish translations                        │
│  │   └── {locale}.json     ← Additional locales if project requires      │
│  └── migrations/                                                         │
│      ├── 001_{entity}_table.sql                                          │
│      ├── 002_{entity}_metas.sql (if metadata enabled)                    │
│      └── sample_data.json  ← Sample data for seeding                     │
└──────────────────────────────────────────────────────────────────────────┘
```

> **📍 Context-Aware Paths:** Entity configs go in `contents/themes/{theme}/entities/` in both contexts.
> Core entities are read-only in consumer projects.
> See `core-theme-responsibilities` skill for complete rules.

## When to Use This Skill

- Creating a new entity (CRUD resource)
- Adding/modifying fields on an entity
- Understanding entity configuration structure
- Generating migrations for entity tables
- Creating sample data for development

## Entity Configuration Structure

### EntityConfig (4 Sections)

```typescript
interface EntityConfig {
  // 1. BASIC IDENTIFICATION
  slug: string           // URL/table name (single source of truth)
  enabled: boolean
  names: { singular: string, plural: string }
  icon: LucideIcon

  // 2. ACCESS AND SCOPE
  access: {
    public: boolean      // Accessible without auth
    api: boolean         // Has external API endpoints
    metadata: boolean    // Supports key-value metadata
    shared: boolean      // Shared among team members (no userId filter)
  }

  // 3. UI/UX FEATURES
  ui: {
    dashboard: {
      showInMenu: boolean
      showInTopbar: boolean
      filters?: EntityFilterConfig[]
    }
    public: {
      hasArchivePage: boolean
      hasSinglePage: boolean
    }
    features: {
      searchable: boolean
      sortable: boolean
      filterable: boolean
      bulkOperations: boolean
      importExport: boolean
    }
  }

  // 4. INTERNATIONALIZATION
  i18n: {
    fallbackLocale: 'en' | 'es'
    loaders: Record<'en' | 'es', () => Promise<object>>
  }

  // FIELDS (imported separately)
  fields: EntityField[]
}
```

> **Note:** Permissions are defined centrally in `config/permissions.config.ts`, not in entity config.

### Field Types

```typescript
type EntityFieldType =
  // Basic
  | 'text' | 'textarea' | 'number' | 'boolean' | 'date' | 'datetime'
  | 'email' | 'url' | 'json'

  // Selection
  | 'select' | 'multiselect' | 'radio' | 'buttongroup' | 'tags' | 'combobox'

  // Media
  | 'file' | 'image' | 'video' | 'audio' | 'media-library'

  // Specialized
  | 'phone' | 'rating' | 'range' | 'doublerange'
  | 'markdown' | 'richtext' | 'code'
  | 'timezone' | 'currency' | 'country' | 'address'

  // Relations
  | 'relation' | 'relation-multi' | 'relation-prop' | 'relation-prop-multi'
  | 'reference' | 'user'
```

### Field Definition

```typescript
interface EntityField {
  name: string
  type: EntityFieldType
  required: boolean
  defaultValue?: unknown
  validation?: ZodSchema

  display: {
    label: string
    description?: string
    placeholder?: string
    showInList: boolean
    showInDetail: boolean
    showInForm: boolean
    order: number
    columnWidth?: number  // 1-12 grid
  }

  api: {
    searchable: boolean
    sortable: boolean
    filterable?: boolean
    readOnly: boolean
  }

  // For select/multiselect
  options?: { value: string, label: string }[]

  // For relations
  relation?: {
    entity: string
    titleField?: string
    parentId?: string
    userFiltered?: boolean
  }
}
```

## Auto-Generated Features

From an EntityConfig, the system automatically provides:

1. **Database Table** - Via migrations
2. **API Endpoints** - `/api/v1/{slug}` with CRUD operations
3. **Dashboard UI** - List, create, edit, delete views
4. **Form Components** - Auto-generated from fields
5. **Validation** - Server and client-side from field config
6. **i18n Support** - Labels, placeholders, messages
7. **Search & Filtering** - Based on field API config
8. **Metadata System** - Key-value pairs (if enabled)
9. **Server Actions** - Direct CRUD from Client Components

## Server Actions (Client Component CRUD)

Server Actions permiten ejecutar operaciones CRUD desde Client Components sin pasar por HTTP.

### Server Actions Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SERVER ACTIONS FLOW                              │
│                                                                      │
│  Client Component          Server Action           GenericEntityService
│  ─────────────────         ─────────────           ────────────────────
│        │                         │                         │
│        │ createEntity(slug,data) │                         │
│        │ ─────────────────────►  │                         │
│        │                         │                         │
│        │                   ┌─────┴─────┐                   │
│        │                   │ 1. Auth   │                   │
│        │                   │ (session) │                   │
│        │                   ├───────────┤                   │
│        │                   │ 2. Perms  │                   │
│        │                   │ (registry)│                   │
│        │                   └─────┬─────┘                   │
│        │                         │                         │
│        │                         │ create(slug,uid,tid,data)
│        │                         │ ─────────────────────► │
│        │                         │                   ┌────┴────┐
│        │                         │                   │ Validate│
│        │                         │                   │ Hooks   │
│        │                         │                   │ SQL+RLS │
│        │                         │                   └────┬────┘
│        │                         │ ◄───────────────────── │
│        │ ◄─────────────────────  │                         │
│        │    EntityActionResult   │                         │
└─────────────────────────────────────────────────────────────────────┘
```

### Server Actions vs API HTTP

| Escenario | Server Actions | API HTTP |
|-----------|----------------|----------|
| Client Component mutations | Recommended | No |
| Server Component data fetching | No | Yes |
| External integrations | No | Yes |
| Webhooks | No | Yes |
| Cache revalidation automática | Yes | Manual |

### Available Functions

| Function | Required Permission | Description |
|----------|---------------------|-------------|
| `createEntity(slug, data, config?)` | `{slug}.create` | Create entity |
| `updateEntity(slug, id, data, config?)` | `{slug}.update` | Update entity |
| `deleteEntity(slug, id, config?)` | `{slug}.delete` | Delete one |
| `deleteEntities(slug, ids, config?)` | `{slug}.delete` | Delete many |
| `getEntity(slug, id)` | `{slug}.read` | Get by ID |
| `listEntities(slug, options?)` | `{slug}.list` | List with filters |
| `entityExists(slug, id)` | `{slug}.read` | Check existence |
| `countEntities(slug, where?)` | `{slug}.list` | Count records |

### Usage Example

```typescript
'use client'

import { createEntity, updateEntity, deleteEntity } from '@nextsparkjs/core/actions'

// CREATE - Auth and permissions verified automatically
async function handleCreate(data: FormData) {
  const result = await createEntity('schools', {
    name: data.get('name'),
    status: 'active'
  })

  if (result.success) {
    console.log('Created:', result.data)
  } else {
    console.error('Error:', result.error)
  }
}

// UPDATE with custom revalidation
async function handleUpdate(id: string, data: Partial<School>) {
  const result = await updateEntity('schools', id, data, {
    revalidatePaths: ['/dashboard/overview'],
    revalidateTags: ['school-stats'],
  })
}

// DELETE with redirect
async function handleDelete(id: string) {
  await deleteEntity('schools', id, {
    redirectTo: '/dashboard/schools'
  })
}
```

### Return Types

```typescript
// For operations that return data
type EntityActionResult<T> =
  | { success: true; data: T }
  | { success: false; error: string }

// For void operations (delete)
type EntityActionVoidResult =
  | { success: true }
  | { success: false; error: string }

// List result
interface ListEntityResult<T> {
  data: T[]
  total: number
  limit: number
  offset: number
}
```

### Action Configuration

```typescript
interface ActionConfig {
  revalidatePaths?: string[]  // Paths to revalidate
  revalidateTags?: string[]   // Cache tags
  redirectTo?: string         // Redirect after action
}
```

### Automatic Security

1. **Auth**: userId from `getTypedSession()` (server-side)
2. **Team**: teamId from httpOnly cookie `activeTeamId`
3. **Permissions**: Verified against `permissions.config.ts`
4. **Validation**: Fields validated against entity schema
5. **RLS**: Queries executed with Row-Level Security
6. **Team Isolation**: All operations filter by active teamId (prevents cross-team access for multi-team users)

### Team Isolation (Multi-Team Users)

Users can belong to multiple teams. Server Actions automatically filter by the active team cookie to prevent accidental cross-team data access:

```
User belongs to: TeamA, TeamB
Active team cookie: TeamA

getEntity('campaigns', 'id-from-teamB')  → Returns null (filtered out)
updateEntity('campaigns', 'id-from-teamB', data) → Error: not found
deleteEntity('campaigns', 'id-from-teamB') → Error: not found
```

This isolation is automatic and cannot be bypassed from client code.

### Server Actions Anti-Patterns

```typescript
// NEVER: Ignore the result
await createEntity('schools', data) // Without checking success

// CORRECT: Always check result
const result = await createEntity('schools', data)
if (!result.success) {
  toast.error(result.error)
}

// NEVER: Use for Server Components (no 'use client')
// Server Actions are for CLIENT Components only

// CORRECT: In Server Components use service directly
import { GenericEntityService } from '@nextsparkjs/core/services'
const data = await GenericEntityService.list('schools', userId, { teamId })
```

### List Entities Example

```typescript
'use client'

import { listEntities } from '@nextsparkjs/core/actions'

async function loadCampaigns() {
  const result = await listEntities<Campaign>('campaigns', {
    where: { status: 'active' },
    orderBy: 'createdAt',
    orderDir: 'desc',
    limit: 20,
    offset: 0,
    search: 'marketing', // Full-text search on searchable fields
  })

  if (result.success) {
    const { data, total, limit, offset } = result.data
    console.log(`Showing ${data.length} of ${total} campaigns`)
  }
}
```

### Server Actions Files

| File | Purpose |
|------|---------|
| `core/lib/actions/entity.actions.ts` | Server Actions (entry points) |
| `core/lib/actions/types.ts` | TypeScript types |
| `core/lib/services/generic-entity.service.ts` | Business logic |
| `core/lib/permissions/check.ts` | Permission verification |

## Metadata System

When `access.metadata: true` is set in the entity config, the entity supports dynamic key-value metadata.

### Migration Required

A separate migration creates the `{entity}_metas` table:

```sql
-- migrations/002_{entity}_metas.sql
CREATE TABLE IF NOT EXISTS "{entity}_metas" (
  "id" TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  "{entity}Id" TEXT NOT NULL REFERENCES "{entity}"(id) ON DELETE CASCADE,
  "metaKey" TEXT NOT NULL,
  "metaValue" JSONB NOT NULL DEFAULT '{}'::jsonb,
  "dataType" TEXT,                              -- Optional: string, number, boolean, json
  "isPublic" BOOLEAN NOT NULL DEFAULT FALSE,    -- Visible without auth
  "isSearchable" BOOLEAN NOT NULL DEFAULT FALSE, -- Indexed for search
  "createdAt" TIMESTAMPTZ NOT NULL DEFAULT now(),
  "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT {entity}_metas_unique_key UNIQUE ("{entity}Id", "metaKey")
);

-- Indexes
CREATE INDEX "idx_{entity}_metas_entity_id" ON "{entity}_metas"("{entity}Id");
CREATE INDEX "idx_{entity}_metas_key" ON "{entity}_metas"("metaKey");
CREATE INDEX "idx_{entity}_metas_value_gin" ON "{entity}_metas" USING GIN ("metaValue");
```

### When to Use Metas vs Fields

| Use Case | Fields | Metas |
|----------|--------|-------|
| Structured, validated data | ✅ | ❌ |
| Shown in forms/lists | ✅ | ❌ |
| Searchable/sortable | ✅ | ❌ |
| Dynamic/extensible data | ❌ | ✅ |
| Plugin-specific data | ❌ | ✅ |
| User preferences/settings | ❌ | ✅ |
| Third-party integrations | ❌ | ✅ |

### API Access

Metas are accessed via query parameter (covered in `entity-api` skill):
```
GET /api/v1/products/123?metas=all
GET /api/v1/products/123?metas=category,tags
```

## Child Entities

Child entities are 1:N relationships where the child only exists in the context of its parent (e.g., order items, post comments).

### Configuration in EntityConfig

```typescript
export const orderEntityConfig: EntityConfig = {
  slug: 'orders',
  // ... other config

  childEntities: {
    'items': {
      table: 'order_items',           // Convention: {parent}_{child}
      showInParentView: true,         // Show in parent detail view
      hasOwnRoutes: false,            // Only via /orders/{id}/child/items

      fields: [
        {
          name: 'productName',
          type: 'text',
          required: true,
          display: { label: 'Product' }
        },
        {
          name: 'quantity',
          type: 'number',
          required: true,
          display: { label: 'Qty' }
        }
      ],

      display: {
        title: 'Order Items',
        description: 'Products in this order',
        mode: 'table'                 // 'table' | 'cards' | 'list'
      }
    }
  }
}
```

### ChildEntityDefinition Interface

```typescript
interface ChildEntityDefinition {
  table: string                    // Database table name
  fields: ChildEntityField[]       // Child entity fields
  showInParentView: boolean        // Show in parent view
  hasOwnRoutes: boolean            // Has independent routes?
  // Note: Permissions are defined centrally in permissions.config.ts
  display: {
    title: string
    description?: string
    mode: 'table' | 'cards' | 'list'
  }
}
```

### Migration Required

```sql
-- migrations/002_{parent}_{child}.sql
CREATE TABLE "order_items" (
  "id" TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  "parentId" TEXT NOT NULL REFERENCES "orders"(id) ON DELETE CASCADE,
  "productName" VARCHAR(255) NOT NULL,
  "quantity" INTEGER NOT NULL,
  "createdAt" TIMESTAMPTZ NOT NULL DEFAULT now(),
  "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX "idx_order_items_parentId" ON "order_items"("parentId");

-- RLS: Access via parent ownership
ALTER TABLE "order_items" ENABLE ROW LEVEL SECURITY;

CREATE POLICY "order_items_via_parent" ON "order_items"
  FOR ALL TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM "orders"
      WHERE "orders".id = "parentId"
      AND "orders"."userId" = public.get_auth_user_id()
    )
  );
```

### Key Properties

| Property | Required | Description |
|----------|----------|-------------|
| `table` | Yes | Table name. Convention: `{parent}_{child}` |
| `fields` | Yes | Child entity fields (same structure as entity fields) |
| `showInParentView` | Yes | Display in parent detail view |
| `hasOwnRoutes` | Yes | If `true`: also `/api/v1/{child}`. If `false`: only via parent |
| `display.mode` | Yes | `table` (rows), `cards` (cards), `list` (simple) |

### Limitations

- **One level deep**: Child entities cannot have their own children
- **Cascade deletion**: Deleting parent deletes all children
- **No public routes**: Children don't have public pages

### API Access

Child entity endpoints (covered in `entity-api` skill):
```
GET    /api/v1/orders/{id}/child/items
POST   /api/v1/orders/{id}/child/items
GET    /api/v1/orders/{id}/child/items/{itemId}
PATCH  /api/v1/orders/{id}/child/items/{itemId}
DELETE /api/v1/orders/{id}/child/items/{itemId}
```

## Scripts

### Scaffold New Entity
```bash
python .claude/skills/entity-system/scripts/scaffold-entity.py --entity products --theme default
```

### Generate Migration
```bash
python .claude/skills/entity-system/scripts/generate-migration.py --entity products --theme default
```

### Generate Metas Migration
```bash
python .claude/skills/entity-system/scripts/generate-metas-migration.py --entity products --theme default
```

### Generate Child Entity Migration
```bash
python .claude/skills/entity-system/scripts/generate-child-migration.py --parent orders --child items --theme default
```

### Generate Sample Data
```bash
python .claude/skills/entity-system/scripts/generate-sample-data.py --entity products --count 10
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `core/lib/entities/types.ts` | All entity type definitions |
| `core/lib/entities/migration-helper.ts` | Migration SQL generation |
| `core/lib/entities/registry.ts` | Entity registry (auto-generated) |
| `core/lib/entities/queries.ts` | Database query helpers |
| `core/lib/entities/helpers.ts` | Utility functions |

## Naming Conventions

- **Slug**: kebab-case, plural (`tasks`, `blog-posts`)
- **Table**: Same as slug (`tasks`, `blog_posts`)
- **API Path**: `/api/v1/{slug}`
- **Config file**: `{singular}.config.ts` (`task.config.ts`)
- **Fields file**: `{slug}.fields.ts` (`tasks.fields.ts`)

## Anti-Patterns

```typescript
// ❌ NEVER: Add system fields manually
fields: [
  { name: 'id', type: 'text', ... },      // Auto-included
  { name: 'teamId', type: 'text', ... },  // Auto-included (team-mode entities)
  { name: 'createdAt', type: 'datetime' }, // Auto-included
  { name: 'updatedAt', type: 'datetime' }, // Auto-included
]

// ❌ NEVER: Use dynamic imports for entity configs
const config = await import(`@/contents/entities/${slug}`)

// ❌ NEVER: Define tableName explicitly (derived from slug)
tableName: 'my_custom_table'

// ✅ CORRECT: Only declare business fields
fields: [
  { name: 'title', type: 'text', ... },
  { name: 'status', type: 'select', ... },
]
```

## Checklist for New Entity

- [ ] Created `{entity}.config.ts` with all 5 sections
- [ ] Created `{entity}.fields.ts` with field definitions
- [ ] Created `{entity}.types.ts` with TypeScript interfaces
- [ ] Created `messages/` with required locales (en.json, es.json, + others if project defines)
- [ ] Created migration in `migrations/001_{entity}_table.sql`
- [ ] Created `_metas` migration if `access.metadata: true`
- [ ] Added entity to theme's entity registry
- [ ] Ran `node core/scripts/build/registry.mjs`

## References

- Load `references/entity-types.md` for complete type definitions
- Load `references/field-examples.md` for field configuration examples
- Load `references/migration-patterns.md` for SQL patterns
