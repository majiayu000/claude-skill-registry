---
name: add-schema
description: Create Zod schemas and inferred TypeScript types for a new entity
---

# Add Schema Skill

Create Zod schemas and inferred TypeScript types for a new entity in the x4-mono monorepo.

## Arguments

The user describes the entity. If unclear, ask for:

- Entity name (PascalCase, e.g., `Comment`, `TeamMember`)
- Fields with types and constraints
- Whether it relates to existing entities (User, Project, etc.)

## Where to Add

- **Schemas**: `packages/shared/utils/validators.ts`
- **Types**: Inferred inline with `z.infer<>` (exported next to the schema)
- **Group**: Add under a `// --- EntityName ---` section comment

## Schema Patterns

Follow the existing patterns in `packages/shared/utils/validators.ts`:

### Create Schema (input for mutations — no id, no timestamps)

```typescript
export const CreateEntitySchema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().max(1000).optional(),
  // Foreign keys as uuid strings
  projectId: z.string().uuid(),
});
export type CreateEntity = z.infer<typeof CreateEntitySchema>;
```

### Update Schema (includes id, all fields optional)

```typescript
export const UpdateEntitySchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(255).optional(),
  description: z.string().max(1000).optional(),
});
export type UpdateEntity = z.infer<typeof UpdateEntitySchema>;
```

### Response Schema (matches Drizzle return types exactly)

```typescript
export const EntityResponseSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  description: z.string().nullable(), // nullable columns → .nullable() not .optional()
  status: z.string(), // text() columns → z.string() not z.enum()
  ownerId: z.string().uuid(),
  createdAt: z.coerce.date(),
  updatedAt: z.coerce.date(),
});
export type EntityResponse = z.infer<typeof EntityResponseSchema>;
```

### List Response Schema

```typescript
export const EntityListResponseSchema = z.object({
  items: z.array(EntityResponseSchema),
  total: z.number().int(),
  limit: z.number().int(),
  offset: z.number().int(),
});
export type EntityListResponse = z.infer<typeof EntityListResponseSchema>;
```

## Return Type Rules

These must match Drizzle's actual return types:

| Drizzle Column              | Zod Schema                                  |
| --------------------------- | ------------------------------------------- |
| `text("status")`            | `z.string()` (not `z.enum()`)               |
| `text("field")` (nullable)  | `z.string().nullable()` (not `.optional()`) |
| `varchar("name").notNull()` | `z.string()`                                |
| `boolean("active")`         | `z.boolean()`                               |
| `uuid("id")`                | `z.string().uuid()`                         |
| `timestamp("created_at")`   | `z.coerce.date()`                           |

## Existing Shared Schemas

Reuse these rather than recreating:

- `PaginationSchema` — `{ limit, offset }`
- `IdParamSchema` — `{ id: z.string().uuid() }`

## Workflow

1. Read `packages/shared/utils/validators.ts` to see existing patterns
2. Add new schemas grouped under a `// --- EntityName ---` comment
3. Export all schemas and inferred types
4. Run `bun turbo type-check` to verify
5. If a database table exists, verify response schema matches Drizzle return types
