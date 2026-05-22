---
name: mern-add-feature
description: Scaffold a new feature with API route, Zod schema, Mongoose model, and UI components.
argument-hint: "<feature-name> [--no-ui] [--no-api] [--no-model]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Add a complete feature slice to an existing MERN project with all layers wired up and tests included.

## Arguments
- `feature-name` — Feature name in kebab-case (e.g., `user-profile`, `invoice`)
- `--no-ui` — Skip UI components (API-only feature)
- `--no-api` — Skip API route (frontend-only feature)
- `--no-model` — Skip Mongoose model (use existing model)

## What gets created

### Default (all layers)
```
packages/shared/schemas/<feature>.ts           # Zod schemas + inferred types
apps/web/src/app/api/<feature>/route.ts        # API route handler
apps/web/src/server/db/models/<feature>.ts     # Mongoose model
apps/web/src/components/<feature>/         # UI components
  <Feature>List.tsx
  <Feature>Form.tsx
  <Feature>Card.tsx
apps/web/src/components/<feature>/__tests__/
  <Feature>Form.test.tsx
```

### With flags
- `--no-ui`: Only schema + API + model
- `--no-api`: Only schema + UI (for client-side-only features)
- `--no-model`: Only schema + API route + UI (uses existing model)

## Conventions

### Naming
- Feature name: `kebab-case` (input)
- Schema/types: `PascalCase` (e.g., `UserProfile`, `CreateUserProfileInput`)
- Files: `kebab-case.ts` for utilities, `PascalCase.tsx` for React
- API routes: `/api/<feature>` for collection, `/api/<feature>/[id]` for item

### Schema location
All Zod schemas go in `packages/shared/schemas/<feature>.ts`:
- `Create<Feature>Schema` — creation input
- `Update<Feature>Schema` — partial update input
- `<Feature>Schema` — full entity shape
- Inferred types exported alongside schemas

### API route structure
- `GET /api/<feature>` — list (paginated)
- `POST /api/<feature>` — create
- `GET /api/<feature>/[id]` — get one
- `PATCH /api/<feature>/[id]` — update
- `DELETE /api/<feature>/[id]` — delete

### Model conventions
- Timestamps enabled
- Indexes documented with reason
- `toJSON` transform to hide internal fields

## Workflow
1. Create Zod schemas in packages/shared
2. Create Mongoose model (if not --no-model)
3. Create API routes (if not --no-api)
4. Create UI components (if not --no-ui)
5. Create tests for each layer
6. Run `pnpm lint` and `pnpm test` to verify

## Output
Summarize: files created, API endpoints available, components ready to use.

## Reference
For templates and patterns, see `reference/mern-add-feature-reference.md`
