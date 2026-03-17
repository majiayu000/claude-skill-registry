---
name: feature-scaffolder
description: Scaffold complete full-stack features with shared types between backend and frontend. Use when asked to scaffold a feature, create a new module, build a full-stack feature end-to-end, or create both backend and frontend for a feature.
---

# Feature Scaffolder Agent

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

This agent scaffolds a complete feature with shared types between backend and frontend. Follow this sequence:

## Step 1: Gather Requirements

Ask the user: feature name, entity/resource name, fields (or read from existing Prisma model if available).

## Step 2: Generate Shared Types First

Create a `types.ts` file with the entity interface, create/update input types, and API response types. **All subsequent files import from this.** This is the single source of truth.

```typescript
// src/types/{feature}.ts
export interface {Entity} { ... }
export interface Create{Entity}Input { ... }
export interface Update{Entity}Input { ... }
export interface {Entity}ListResponse {
  data: {Entity}[];
  pagination: { page: number; limit: number; total: number; totalPages: number };
}
```

## Step 3: Generate Validation Schemas

Run the `zod-schema-generator` skill to create validation schemas from the shared types. Schemas import and align with the types from step 2.

## Step 4: Generate API Routes

Run the `nextjs-route-generator` skill to create the API route, importing the Zod schemas for validation and shared types for response typing.

Routes import from:
- Shared types for response structure
- Generated Zod schemas for request validation

## Step 5: Generate React Component

Run the `react-component-generator` skill to create the frontend component, importing shared types for props and API response handling.

Components import from:
- Shared types for entity display and form state
- Zod schemas for client-side validation (if applicable)

## Step 6: Type Safety Pass

Run the `typescript-refactorer` skill on all generated files as a final quality pass.

## Step 7: Verify Cross-File Imports

Check that all imports resolve correctly across generated files. If any file references a type or schema that doesn't exist, fix it before delivering.

## Output

Produce a file manifest showing all generated files and their dependency relationships:

```
# Feature Scaffolding Complete: {feature-name}

## File Manifest
src/types/{feature}.ts          ← shared types (source of truth)
src/schemas/{feature}.ts        ← Zod schemas (imports types)
app/api/{feature}/route.ts      ← list + create (imports schemas + types)
app/api/{feature}/[id]/route.ts ← get + update + delete (imports schemas + types)
src/components/{feature}/       ← UI components (imports types)

## Dependency Graph
types.ts → schemas.ts → route.ts
types.ts → Component.tsx
```

## Skill Dependencies

- `skills/zod-schema-generator`
- `skills/nextjs-route-generator`
- `skills/react-component-generator`
- `skills/typescript-refactorer`
