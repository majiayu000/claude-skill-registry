---
name: mern-api-docs
description: Generate OpenAPI documentation from Zod schemas and API routes.
argument-hint: "[--serve] [--export <path>]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Generate and serve OpenAPI (Swagger) documentation derived from Zod schemas and Next.js API routes.

## Arguments
- `--serve` — Start Swagger UI at `/api/docs`
- `--export <path>` — Export OpenAPI spec to file (default: `openapi.json`)
- (no args) — Generate spec and report endpoints documented

## What gets created

```
apps/web/
├── app/api/docs/route.ts           # Swagger UI endpoint
├── src/lib/openapi.ts              # OpenAPI spec generator
└── openapi.json                    # Generated spec (if --export)
```

## How it works

1. **Scans** `packages/shared/schemas/` for Zod schemas
2. **Scans** `apps/web/src/app/api/` for route handlers
3. **Extracts** request/response types from Zod schemas
4. **Generates** OpenAPI 3.0 spec with:
   - Endpoints from file structure
   - Request bodies from `Create*Schema`
   - Response schemas from `*ResponseSchema`
   - Query params from `*QuerySchema`
   - Path params from `[id]` segments

## Schema conventions for docs

```typescript
// packages/shared/schemas/todo-item.ts

/** @description Create a new todo item */
export const CreateTodoItemSchema = z.object({
  /** @description Item title (required) */
  title: z.string().min(1).max(200),
  /** @description Optional description */
  description: z.string().optional(),
});

/** @description Todo item response */
export const TodoItemSchema = z.object({
  id: z.string(),
  title: z.string(),
  // ...
});
```

JSDoc comments become OpenAPI descriptions.

## Swagger UI

When `--serve` is used, Swagger UI is available at `/api/docs`:
- Interactive API explorer
- Try-it-out functionality (with auth)
- Schema visualization

## Workflow
1. Ensure schemas follow naming conventions
2. Run skill to generate/update spec
3. Review generated documentation
4. Optionally serve Swagger UI

## Output
- Endpoints documented count
- Schemas extracted count
- Missing documentation warnings
- Spec file location (if exported)

## Reference
For setup and customization, see `reference/mern-api-docs-reference.md`
