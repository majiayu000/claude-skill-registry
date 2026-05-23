---
name: type-generation
description: Regenerate TypeScript types from the OpenAPI spec to keep the frontend in sync with the backend. Use after API changes.
metadata:
  author: traceway
  version: "1.0.0"
---

# Type Generation Workflow

Use this skill when the API shape has changed and the frontend needs updated types, or when the user asks to sync types between backend and frontend.

## Overview

The type flow is:

1. Backend (Encore.ts or Rust daemon) defines API endpoints
2. OpenAPI spec is generated from the running API
3. `openapi-typescript` converts the spec to TypeScript types
4. Frontend imports types from `ui/src/lib/api-types.ts`

## Option A: Generate from existing openapi.json file

If `openapi.json` at the repo root is already up to date:

```bash
cd ui && npm run generate-types:file
```

This reads `../openapi.json` and writes `src/lib/api-types.ts`.

## Option B: Generate from running daemon

If the Rust daemon is running locally (port 3000):

```bash
cd ui && npm run generate-types
```

This fetches from `http://localhost:3000/api/openapi.json`.

## Option C: Full sync (daemon → openapi.json → types)

If you need to update both the spec file and types:

```bash
./scripts/sync-openapi.sh
```

This script:
1. Detects a running daemon or starts one temporarily
2. Fetches the live OpenAPI spec
3. Normalizes JSON for stable diffs
4. Writes `openapi.json` at repo root
5. Runs `openapi-typescript` to generate `ui/src/lib/api-types.ts`

## After generating types

1. Check for new types to re-export in `ui/src/lib/api.ts`:

```typescript
// In ui/src/lib/api.ts — add re-exports for new schema types
export type NewEntity = Schemas['NewEntity'];
export type NewEntityResponse = Schemas['NewEntityResponse'];
```

2. Add fetch helpers if needed:

```typescript
export async function getNewEntities(): Promise<NewEntity[]> {
  const res = await fetch(`${API_BASE}/internal/new-entities?org_id=${getOrgId()}&project_id=${getProjectId()}`);
  if (!res.ok) throw new Error(res.statusText);
  const data = await res.json();
  return data.items;
}
```

3. Run svelte-check: `cd ui && npm run check`

## Makefile shortcuts

```bash
make sync-openapi      # Full sync (Option C)
make generate-types    # From file (Option A)
```

## When to regenerate

- After adding/modifying Encore.ts API endpoints
- After changing Rust daemon API routes or response types
- After modifying request/response interfaces in `backend/app/*/types.ts`
- Before starting UI work that consumes new API endpoints
