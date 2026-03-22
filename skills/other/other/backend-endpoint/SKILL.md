---
name: backend-endpoint
description: Create a new Encore.ts API endpoint with service, types, and schema. Use when adding backend API routes, CRUD services, or new backend features.
metadata:
  author: traceway
  version: "1.0.0"
---

# Create Backend API Endpoint

Use this skill when the user asks to add a new API endpoint, backend service, or CRUD operations to the Encore.ts backend.

## File structure for a new service

Each service in `backend/app/` follows this layout:

```
backend/app/<service_name>/
├── api.ts       # Endpoint definitions (Encore api() calls)
├── service.ts   # Business logic (DB queries via Drizzle)
├── types.ts     # Request/response interfaces
└── encore.service.ts  # (optional) Encore service config
```

## Step-by-step

1. **Define types** in `types.ts`:

```typescript
import { ScopeQuery } from "../core/types";

export interface MyEntity {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface ListMyEntitiesResponse {
  items: MyEntity[];
}

export interface GetMyEntityRequest extends ScopeQuery {
  id: string;
}

export interface DeleteMyEntityRequest extends ScopeQuery {
  id: string;
}

export type CreateMyEntityRequest = ScopeQuery & Omit<MyEntity, "id" | "created_at" | "updated_at">;
```

2. **Add schema table** in `backend/app/core/schema.ts` (if new table needed):

```typescript
export const myEntities = p.pgTable(
  "my_entities",
  {
    id: p.uuid().primaryKey(),
    orgId: p.uuid("org_id").notNull().references(() => organizations.id, { onDelete: "cascade" }),
    projectId: p.uuid("project_id").notNull().references(() => projects.id, { onDelete: "cascade" }),
    name: p.text().notNull(),
    createdAt: p.timestamp("created_at", { withTimezone: true }).notNull(),
    updatedAt: p.timestamp("updated_at", { withTimezone: true }).notNull(),
  },
  (table) => [
    p.index("my_entities_org_project_idx").on(table.orgId, table.projectId),
  ]
);
```

3. **Write service** in `service.ts`:

```typescript
import { and, asc, eq } from "drizzle-orm";
import { db } from "../core/database";
import { myEntities } from "../core/schema";
import { MyEntity } from "./types";

function toApi(row: typeof myEntities.$inferSelect): MyEntity {
  return {
    id: row.id,
    name: row.name,
    created_at: row.createdAt.toISOString(),
    updated_at: row.updatedAt.toISOString(),
  };
}

export const MyEntitiesService = {
  async list(orgId: string, projectId: string): Promise<MyEntity[]> {
    const rows = await db
      .select()
      .from(myEntities)
      .where(and(eq(myEntities.orgId, orgId), eq(myEntities.projectId, projectId)))
      .orderBy(asc(myEntities.createdAt));
    return rows.map(toApi);
  },

  async get(orgId: string, projectId: string, id: string): Promise<MyEntity | null> {
    const [row] = await db
      .select()
      .from(myEntities)
      .where(and(
        eq(myEntities.id, id),
        eq(myEntities.orgId, orgId),
        eq(myEntities.projectId, projectId)
      ))
      .limit(1);
    return row ? toApi(row) : null;
  },

  // ... create, update, delete follow same pattern
};
```

4. **Write API endpoints** in `api.ts`:

```typescript
import { APIError, api } from "encore.dev/api";
import { ScopeQuery } from "../core/types";
import { validateScope } from "../core/utils";
import { MyEntitiesService } from "./service";
import { ListMyEntitiesResponse, GetMyEntityRequest } from "./types";

export const listMyEntities = api(
  { expose: true, auth: true, method: "GET", path: "/internal/my-entities" },
  async (scope: ScopeQuery): Promise<ListMyEntitiesResponse> => {
    validateScope(scope);
    const items = await MyEntitiesService.list(scope.org_id, scope.project_id);
    return { items };
  }
);

export const getMyEntity = api(
  { expose: true, auth: true, method: "GET", path: "/internal/my-entities/:id" },
  async (req: GetMyEntityRequest) => {
    validateScope(req);
    const item = await MyEntitiesService.get(req.org_id, req.project_id, req.id);
    if (!item) throw APIError.notFound("Entity not found");
    return item;
  }
);
```

## Key conventions

- **Auth**: All endpoints use `auth: true` and call `validateScope(scope)` first
- **Paths**: Use `/internal/` prefix for browser-facing endpoints
- **Scope**: Every query is scoped to `org_id` + `project_id` — never leak across orgs
- **IDs**: Use `crypto.randomUUID()` (via `newId()` from `core/utils`) for new records
- **Timestamps**: Use `new Date()` for DB writes, `.toISOString()` for API responses
- **Drizzle column naming**: camelCase in TS, snake_case in SQL (e.g., `orgId` maps to `"org_id"`)
- **Error handling**: Use `APIError.notFound()`, `APIError.invalidArgument()`, etc. from `encore.dev/api`
- **Response types**: Always define explicit response interfaces in `types.ts`

## After creating the endpoint

1. Generate a migration if schema changed: `cd backend/app && npx drizzle-kit generate`
2. Run typecheck: `cd backend/app && npm run typecheck`
3. If the UI needs these types, regenerate: `cd ui && npm run generate-types:file`
