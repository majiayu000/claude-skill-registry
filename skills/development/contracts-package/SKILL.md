---
name: contracts-package
description: Use when creating, auditing, or validating MetaSaver contracts packages. Includes Zod validation schemas, TypeScript types, barrel exports, and database type re-exports. File types: .ts, package.json, tsconfig.json.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Contracts Package Structure for MetaSaver

## Purpose

This skill documents the complete structure for MetaSaver contracts packages. Contracts packages provide:

- Zod validation schemas for API request/response validation
- TypeScript types re-exported from database packages
- Shared type definitions between frontend and backend
- Single source of truth for entity shapes

**Use when:**

- Creating a new contracts package for a domain
- Adding a new entity to an existing contracts package
- Auditing contracts package structure for compliance
- Validating type exports and barrel patterns

## Directory Structure

```
packages/contracts/{domain}-contracts/
├── src/
│   ├── shared/                     # (optional) Shared enums/types used by multiple entities
│   │   └── types.ts                # Shared types and enums
│   └── {entity}/                   # One folder per entity
│       ├── types.ts                # TypeScript types and interfaces
│       └── validation.ts           # Zod schemas and inferred types
├── eslint.config.js                # ESLint flat config (required)
├── package.json
└── tsconfig.json
```

**CRITICAL: Use direct exports (no barrel index.ts files)**

- Always export directly from specific files using package.json exports field
- Ensure consumers import with full path: `from "@metasaver/contracts/users/types"`

**IMPORTANT - Package level file requirements:**

- Always use monorepo root `.gitignore` - do not create at package level
- Always use `eslint.config.js` (flat config) - do not use `.eslintrc.cjs`

## Templates

See `TEMPLATES.md` for all available templates. Key templates:

| Template                    | Purpose                 | Location                     |
| --------------------------- | ----------------------- | ---------------------------- |
| `types.ts.template`         | Entity type definitions | `src/{entity}/types.ts`      |
| `validation.ts.template`    | Zod validation schemas  | `src/{entity}/validation.ts` |
| `shared-types.ts.template`  | Shared enums/types      | `src/shared/types.ts`        |
| `package.json.template`     | Package configuration   | `package.json`               |
| `tsconfig.json.template`    | TypeScript config       | `tsconfig.json`              |
| `eslint.config.js.template` | ESLint flat config      | `eslint.config.js`           |

## File Rules

### Types File Rules

- Always re-export Prisma types from database package (single source of truth)
- Define API response wrapper types (Create, Update, Get, Delete)
- Ensure you do not duplicate Prisma model fields
- Always use `type` imports for Prisma types

### Validation File Rules

- Use Zod for all validation
- Export base fields for frontend reuse (e.g., ZDataTable)
- Create request uses full schema
- Update request uses `.partial()` for optional fields
- Export inferred types with `z.infer<>`
- Add helpful error messages to validators

### Package Export Rules (package.json)

- Use wildcard `exports` field in package.json (zero maintenance)
- Consumers import with full paths: `from "@metasaver/contracts/users/types"`
- Example exports field:
  ```json
  "exports": {
    "./*": { "types": "./dist/*.d.ts", "import": "./dist/*.js" }
  }
  ```

### Enum Organization Rules (Industry Standard)

| Scenario                         | Location                        |
| -------------------------------- | ------------------------------- |
| Enum used by **one entity only** | Colocate in `{entity}/types.ts` |
| Enum used by **2+ entities**     | Place in `/shared/types.ts`     |

All enums should have a corresponding `Labels` object for UI display.

**Export Example:**

```typescript
// src/shared/types.ts
export enum UserRole {
  ADMIN = "admin",
  USER = "user",
}

export const UserRoleLabels = {
  [UserRole.ADMIN]: "Administrator",
  [UserRole.USER]: "User",
} as const;
```

### tsconfig.json Rules

- Extends `@metasaver/core-typescript-config/base`
- Only `rootDir` and `outDir` in compilerOptions
- NO duplicate settings from base (`composite`, `declarationMap`, `sourceMap` are inherited)

### package.json Rules

- Include `metasaver.projectType: "contracts"`
- Use `test:unit` NOT `test`
- Include database package as dependency (for Prisma types)
- Zod as both dependency and peerDependency
- Include vitest for testing

## Workflow: Adding New Entity

1. Create entity folder: `mkdir -p src/{entity}`
2. Copy `types.ts.template` → `src/{entity}/types.ts`, replace variables
3. Copy `validation.ts.template` → `src/{entity}/validation.ts`, replace variables
4. Verify `package.json` has wildcard exports (already configured):
   ```json
   "exports": {
     "./*": { "types": "./dist/*.d.ts", "import": "./dist/*.js" }
   }
   ```

## Workflow: Adding Shared Enum

1. Verify enum is used by 2+ entities (if not, colocate)
2. Create `/shared/` if doesn't exist
3. Add enum with Labels object to `src/shared/types.ts`
4. Wildcard exports already cover this path (no package.json change needed)

## Audit Checklist

### Directory Structure

- [ ] Package at `packages/contracts/{domain}-contracts/`
- [ ] Each entity has its own folder under `src/`
- [ ] Each entity folder has `types.ts`, `validation.ts` (use direct exports, no index.ts)
- [ ] Always use direct exports - ensure no `index.ts` barrel files anywhere
- [ ] Always use monorepo `.gitignore` - do not create at package level
- [ ] Always use `eslint.config.js` (flat config) - do not use `.eslintrc.cjs`
- [ ] Has `eslint.config.js` (flat config)

### Types Files

- [ ] Entity type re-exported from database package
- [ ] API response interfaces defined (Create, Update, Get, Delete)
- [ ] No duplicate Prisma model field definitions
- [ ] Uses `type` imports for Prisma types

### Validation Files

- [ ] Uses Zod for all schemas
- [ ] Base fields exported for frontend reuse
- [ ] Create schema uses full fields
- [ ] Update schema uses `.partial()`
- [ ] Inferred types exported with `z.infer<>`
- [ ] Error messages included in validators

### Package Exports

- [ ] `package.json` has `exports` field with all public paths
- [ ] Each entity has separate export paths for types and validation
- [ ] Shared types have dedicated export path
- [ ] Always use direct exports - ensure no `index.ts` barrel files

### Enum Organization

- [ ] Entity-specific enums colocated in entity `types.ts` file
- [ ] Shared enums (2+ entities) in `/shared/types.ts` file
- [ ] All enums have corresponding Labels object
- [ ] Enums use named exports only (no default exports)

### package.json

- [ ] Name follows `@metasaver/{domain}-contracts` pattern
- [ ] Has `metasaver.projectType: "contracts"`
- [ ] Uses `test:unit` NOT `test`
- [ ] Includes database package dependency
- [ ] Has Zod as dependency and peerDependency
- [ ] Has vitest in devDependencies

### tsconfig.json

- [ ] Extends `@metasaver/core-typescript-config/base`
- [ ] Only has `rootDir` and `outDir` in compilerOptions
- [ ] NO duplicate settings from base (`composite`, `declarationMap`, `sourceMap`)

## Common Violations & Fixes

| Violation                                     | Fix                                                |
| --------------------------------------------- | -------------------------------------------------- |
| Duplicating Prisma model fields               | Re-export from database package                    |
| Using `test` instead of `test:unit`           | Change to `test:unit`                              |
| Using barrel exports (index.ts)               | Remove index.ts, use package.json exports field    |
| Missing package.json exports field            | Add exports field with all public paths            |
| Duplicate tsconfig settings                   | Remove settings inherited from base                |
| Package-level `.gitignore` or `.eslintrc.cjs` | Use monorepo root config, use `eslint.config.js`   |
| Entity-specific enum in `/shared/`            | Move to entity `types.ts` file                     |
| Using default exports                         | Always use named exports only                      |
| Importing from barrel index                   | Always import directly: `from "{pkg}/users/types"` |

## Related Agents

- **prisma-database-agent** - Prisma schema (source of entity types)
- **data-service-agent** - Services consuming contracts
- **react-app-agent** - Frontend apps importing contracts
