---
name: ops-db-ops
description: Database migrations, reverts, schema generation, and GraphQL codegen for Expo + serverless backend projects. Operates on the backend (TypeORM) and frontend (GraphQL code generation).
allowed-tools:
  - Bash
  - Read
---

# Ops: Database Operations

Manage database migrations, schema generation, and GraphQL code generation.

**Argument**: `$ARGUMENTS` — operation (`migrate`, `revert`, `generate`, `schema`, `codegen`) and optional environment (default: `dev`)

## Path Convention

- **Frontend**: Current project directory (`.`)
- **Backend**: `${BACKEND_DIR:-../backend-v2}` — set `BACKEND_DIR` in `.claude/settings.local.json` if your backend is elsewhere

## Safety

**CRITICAL**: Never run migrations or reverts against production without explicit human confirmation.

## Discovery

Read the backend `package.json` to discover available migration and schema scripts:
- `migration:run:*` — run pending migrations
- `migration:revert:*` — revert last migration
- `migration:generate:*` — generate new migration from entity changes
- `migration:create` — create empty migration
- `generate:sql-schema*` — regenerate SQL schema for MCP
- `aws:signin:*` — AWS credential scripts

Read the frontend `package.json` to discover codegen scripts:
- `fetch:graphql:schema:*` — fetch GraphQL schema
- `generate:types:*` — generate TypeScript types

## AWS Prerequisite

All database operations (except `codegen`) require AWS credentials. Run the backend's AWS signin script first:

```bash
cd "${BACKEND_DIR:-../backend-v2}"
bun run aws:signin:{env}
```

## Operations

### migrate (run pending migrations)

**Local database**:
```bash
cd "${BACKEND_DIR:-../backend-v2}"
STAGE={env} bun run migration:run:local
```

**Remote database**:
```bash
cd "${BACKEND_DIR:-../backend-v2}"
STAGE={env} bun run migration:run:remote:local
```

### revert (undo last migration)

**Local database**:
```bash
cd "${BACKEND_DIR:-../backend-v2}"
STAGE={env} bun run migration:revert:local
```

**Remote database**:
```bash
cd "${BACKEND_DIR:-../backend-v2}"
STAGE={env} bun run migration:revert:remote:local
```

### generate (create new migration from entity changes)

```bash
cd "${BACKEND_DIR:-../backend-v2}"
NAME={migration_name} bun run migration:generate:{env}
```

### create (create empty migration)

```bash
cd "${BACKEND_DIR:-../backend-v2}"
NAME={migration_name} bun run migration:create
```

### schema (regenerate SQL schema for MCP)

```bash
cd "${BACKEND_DIR:-../backend-v2}"
STAGE={env} bun run generate:sql-schema
```

### codegen (regenerate GraphQL types in frontend)

1. **Fetch schema**:
   ```bash
   bun run fetch:graphql:schema:{env}
   ```

2. **Generate types**:
   ```bash
   bun run generate:types:{env}
   ```

**Note**: The backend must be running (locally or deployed) for schema fetching to work.

## Output Format

Report operation result:

| Operation | Environment | Target | Status | Details |
|-----------|-------------|--------|--------|---------|
| migrate | dev | local DB | SUCCESS | 2 migrations applied |
| codegen | dev | frontend | SUCCESS | Types regenerated |
