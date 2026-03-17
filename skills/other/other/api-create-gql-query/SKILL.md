---
name: api-create-gql-query
description: Add a new GraphQL query endpoint with type safety, GraphORM integration, and tests
argument-hint: "[query name and purpose]"
---

# Add a New GraphQL Query to daily-api

You are adding a new GraphQL query endpoint for daily-api. Follow this skill step by step.

## Context Loading

Before writing any code, read these files for code style rules and GraphQL conventions:

1. `AGENTS.md` (project root) — code style, architecture, best practices
2. `src/graphorm/AGENTS.md` — GraphORM patterns for N+1 prevention

These are the source of truth for all code style decisions. Do not deviate from them.

## Step 0 — Gather Requirements

Before writing any code, ask the user the following questions **in this order**:

### 1. Which schema domain?

> **Which schema file does this query belong in?**

Check existing files in `src/schema/` (e.g., `posts.ts`, `users.ts`, `keywords.ts`, `campaigns.ts`, `sources.ts`, `organizations.ts`, etc.) and `src/graphql.ts` imports. Use an existing domain file if the query fits, or create a new one if it represents a new domain.

### 2. Return type

> **What does the query return?** One of:
>
> - **(a)** Single entity — `graphorm.queryOne<T>()` / `graphorm.queryOneOrFail<T>()`
> - **(b)** List of entities — `graphorm.query<T>()`
> - **(c)** Paginated list (Relay-style) — `graphorm.queryPaginated<T>()`

Check existing GQL types in the target schema file and `src/schema/common.ts` for reusable types (`PageInfo`, `ConnectionArgs`, scalars like `DateTime`, `JSONObject`).

### 3. Input arguments and validation

> **What parameters does the query accept?**

For every `String` argument, ask what it represents so the correct Zod validator is chosen (e.g., `z.uuid()` for IDs, `z.email()` for emails, `z.url()` for URLs, `z.string().min(1)` for free text). All query input parameters must be validated with a Zod schema — this is not optional.

### 4. Authentication requirements

> **What auth level is needed?** One of:
>
> - **(a)** Public (no auth) — resolver uses `Context`
> - **(b)** Authenticated — resolver uses `AuthContext`, add `@auth` directive
> - **(c)** Moderator-only — add `@auth(requires: [MODERATOR])` directive
> - **(d)** Plus subscriber — add `@feedPlus` directive

### 5. Business logic

> **What data should the query return and what filtering/sorting is needed?**

---

## Step 1 — Check for Reusable Types

Before creating new types, check:

- **Target schema file** — existing GQL types and TypeScript types
- **`src/schema/common.ts`** — shared types (`PageInfo`, connection patterns, scalars)
- **`src/entity/`** — existing TypeORM entities that map to the desired return type
- **`src/graphorm/index.ts`** — existing GraphORM type configurations
- **`src/common/schema/`** — existing Zod schemas that already validate similar input

Only create new types if nothing reusable exists.

---

## Step 2 — Define Zod Validation Schema

**Mandatory for all queries that accept input arguments.**

Create or update a Zod schema in `src/common/schema/` with `Schema` suffix. This project uses **Zod 4.x** — primitive validators are top-level: `z.email()`, `z.uuid()`, `z.url()` (not `z.string().email()`).

| GQL Type | Use Case | Zod Validator |
|---|---|---|
| `String!` | ID (UUID) | `z.uuid()` |
| `String!` | ID (non-UUID) | `z.string().min(1)` |
| `String!` | Email | `z.email()` |
| `String!` | URL | `z.url()` |
| `String!` | Free text | `z.string().min(1)` |
| `String` (nullable) | Any | appropriate validator with `.nullish()` |
| `Int` / `Int!` | Number | `z.number().int()` with `.min()`/`.max()` |
| `Boolean` | Flag | `z.boolean()` |

Rules:
- Never re-export inferred types — use `z.infer<typeof schema>` at point of use
- Export only the schema, not the inferred type
- For ambiguous `String` args, ask the user what the value represents before choosing a validator

---

## Step 3 — Define TypeScript Types

If new types are needed, add a TypeScript `type` (not `interface` — per AGENTS.md) for the GQL return type in the schema file.

Exception: some existing schema files already use `interface` — follow the pattern in the specific file being modified.

---

## Step 4 — Define GraphQL Schema (typeDefs)

Add to the `typeDefs` template literal (using `/* GraphQL */` tag) in the schema file:

- New types if needed
- `extend type Query { ... }` with the new query field and auth directives

For paginated queries, define `Edge` and `Connection` types following the pattern in `src/schema/campaigns.ts`.

---

## Step 5 — Write the Resolver

All queries must use **GraphORM** (not TypeORM repositories). Wrap resolvers in `traceResolvers()`. Validate input with the Zod schema from Step 2 using `schema.parse(args)`. Pass `true` as the 4th argument for read replica when eventual consistency is acceptable. Filter at the database level via the builder callback, not in JavaScript.

Reference examples:
- **Single entity**: `src/schema/keywords.ts` → `keyword`, `src/schema/campaigns.ts` → `campaignById`
- **List**: `src/schema/keywords.ts` → `randomPendingKeyword`
- **Paginated**: `src/schema/campaigns.ts` → `campaignsList`

---

## Step 6 — Add GraphORM Configuration (if needed)

If the query returns a new entity type or needs custom field mappings, add configuration to `src/graphorm/index.ts`. Define `requiredColumns`, field transforms, custom relations as needed. Reference `src/graphorm/AGENTS.md` for patterns.

Skip if using an already-configured entity type.

---

## Step 7 — Register in GraphQL Schema (if new domain file)

**Only needed when creating a new schema file.**

In `src/graphql.ts`:
1. Add `import * as newDomain from './schema/newDomain'`
2. Add `newDomain.typeDefs` to the `typeDefs` array
3. Add `newDomain.resolvers` to the `merge()` call

---

## Step 8 — Write Integration Tests

Create or update test file in `__tests__/`. Reference: `__tests__/keywords.ts` for the full test structure.

Use the `initializeGraphQLTesting` + `MockContext` + `GraphQLTestClient` pattern from `__tests__/helpers`.

Test cases to include:
1. **Auth/authorization checks** (if applicable)
2. **Success path** with expected response shape (use `toMatchObject`/`toEqual`)
3. **Validation failure** (invalid input rejected by Zod schema)
4. **Edge cases** (not found, empty results)

Run with: `NODE_ENV=test npx jest __tests__/<test-file>.ts --testEnvironment=node --runInBand`

---

## File Locations Quick Reference

| Purpose | Path |
|---|---|
| GraphQL schema & resolvers | `src/schema/<domain>.ts` |
| Schema registration | `src/graphql.ts` |
| GraphORM configuration | `src/graphorm/index.ts` |
| Shared GQL types | `src/schema/common.ts` |
| Entity definitions | `src/entity/` |
| Zod validation schemas | `src/common/schema/` |
| Test file | `__tests__/<domain>.ts` |
| GraphORM docs | `src/graphorm/AGENTS.md` |
| Code style reference | `AGENTS.md` |

## Instructions

When the user invokes this skill:

1. Read `AGENTS.md` and `src/graphorm/AGENTS.md` for context
2. Complete Step 0 — ask all requirement questions before writing any code. For every `String` argument, ask what it represents so the right Zod validator is chosen.
3. Work through Steps 1–8 in order
4. Reference actual codebase examples (`src/schema/keywords.ts` for simple queries, `src/schema/campaigns.ts` for paginated) rather than relying solely on templates
5. Follow all code style rules from AGENTS.md (arrow functions, no unnecessary comments, type over interface, no barrel imports, etc.)
6. Verify build and lint pass: `pnpm run build && pnpm run lint`
