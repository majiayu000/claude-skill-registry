---
name: api-add-gql-mutation
description: Add a new GraphQL mutation to an existing schema in daily-api with validation, resolvers, and tests
argument-hint: "[schema name and mutation purpose]"
---

# Add a New GraphQL Mutation

You are adding a new mutation to an **existing** GraphQL schema file in daily-api. Follow this skill step by step.

## Context Loading

Before writing any code, read these files for code style rules and conventions:

1. `AGENTS.md` (project root) — code style, architecture, best practices
2. `src/graphorm/AGENTS.md` — GraphORM is read-only; mutations use TypeORM repositories

These are the source of truth for all code style decisions. Do not deviate from them.

## Step 0 — Gather Requirements

Before writing any code, ask the user the following questions **in this order**:

### 1. Target schema file

> **Which existing `src/schema/<domain>.ts` file should receive this mutation?**

Existing schema files for reference:

`achievements`, `actions`, `alerts`, `autocompletes`, `bookmarks`, `campaigns`, `comments`, `common`, `compatibility`, `contentPreference`, `devcards`, `feedback`, `feeds`, `gear`, `integrations`, `keywords`, `leaderboard`, `njord`, `notifications`, `opportunity`, `organizations`, `paddle`, `personalAccessTokens`, `posts`, `profile`, `prompts`, `search`, `settings`, `sourceRequests`, `sourceStack`, `sources`, `submissions`, `tags`, `trace`, `urlShortener`, `userHotTake`, `userStack`, `userWorkspacePhoto`, `users`

### 2. Mutation name and purpose

> **What is the mutation name and what does it do?**

### 3. Input fields

> **What arguments/input type does it accept?** Describe the fields, their types, and which are required vs optional.

### 4. Return type

> **What does it return?** Options:
>
> - `EmptyResponse` (from `src/schema/common.ts` — return `{ _: true }`)
> - An existing type already defined in the target schema
> - A new custom type (describe it)

### 5. Auth requirements

> **What auth level is needed?** Options:
>
> - `@auth` — standard authenticated user
> - `@auth(requires: [MODERATOR])` — system moderator only
> - `@rateLimit(limit: N, duration: N)` — rate-limited (combine with `@auth`)

### 6. Database operations

> **What kind of writes?** Options:
>
> - Single write (simple `repo.update()` / `repo.save()`)
> - Multiple writes (needs `con.transaction()`)
> - JSONB flag update (use `updateFlagsStatement`)

---

## Step 1 — Check for Reusable Types

Before writing any code, check for types and utilities that can be reused:

1. **Read the target schema file's `typeDefs`** — look for existing input/output types
2. **Check `src/schema/common.ts`** for shared types:
   - `EmptyResponse` — for mutations with no meaningful return
   - `GQLDataInput<T>`, `GQLIdInput`, `GQLDataIdInput<T>` — standard input wrappers
   - Pagination types, scalars (`DateTime`, `JSONObject`)
3. **Check `src/common/`** for shared utilities:
   - `toGQLEnum()` from `src/common/utils.ts` — expose TypeScript enums as GraphQL enums
   - `updateFlagsStatement` from `src/common/utils.ts` — atomic JSONB flag updates
4. **Check `src/entity/` for the relevant domain** — understand database column types and relations
5. **Check `src/common/schema/`** for existing Zod schemas that validate similar data

Report findings to the user before proceeding.

---

## Step 2 — Add GraphQL Type Definitions

In the target schema file (`src/schema/<domain>.ts`), add to the `typeDefs` template literal:

### Input type (if needed)

```graphql
input MyMutationInput {
  field1: String!
  field2: Int
}
```

### Output type (if not reusing an existing one)

```graphql
type MyMutationResult {
  id: ID!
  status: String!
}
```

### Mutation entry

Add inside `extend type Mutation { }`:

```graphql
extend type Mutation {
  """
  Brief description of what this mutation does
  """
  myMutation(data: MyMutationInput!): MyMutationResult! @auth
}
```

Directive examples:
- `@auth` — standard auth
- `@auth(requires: [MODERATOR])` — moderator only
- `@rateLimit(limit: 5, duration: 60) @auth` — rate-limited

### TypeScript types

Add type declarations (prefixed with `GQL`) for any new input/output types. Use `type` over `interface` per code style rules:

```typescript
type GQLMyMutationInput = {
  field1: string;
  field2?: number;
};
```

---

## Step 3 — Implement the Resolver

Add the resolver in the `resolvers` export object under the `Mutation` key. The file should already have `traceResolvers()` wrapping all resolvers.

### Resolver signature

```typescript
Mutation: {
  myMutation: async (
    _,
    { data }: { data: GQLMyMutationInput },
    { con, userId }: AuthContext,
  ): Promise<GQLMyMutationResult> => {
    // implementation
  },
},
```

### Input validation with Zod

**Always prefer Zod for input validation.** Place Zod schemas in `src/common/schema/<domain>.ts` (create the file if it doesn't exist for this domain).

**This project uses Zod 4.x** (currently 4.3.5) — use the v4 API:
- Primitive types are top-level: `z.email()` not `z.string().email()`, `z.uuid()` not `z.string().uuid()`, `z.url()` not `z.string().url()`
- `z.literal([...])` supports arrays for enum-like validation; `z.enum([...])` also works
- Use `.nullish()` instead of `.nullable().optional()`
- Schema exports must use a `Schema` suffix (e.g., `myMutationInputSchema`)
- Export only schemas, not inferred types — use `z.infer<typeof schema>` at point of use

```typescript
// src/common/schema/<domain>.ts
import z from 'zod';

export const myMutationInputSchema = z.object({
  field1: z.string().min(1),
  field2: z.number().int().positive().nullish(),
  email: z.email(),
});
```

```typescript
// In the resolver
import { myMutationInputSchema } from '../common/schema/<domain>';

const result = myMutationInputSchema.safeParse(data);
if (!result.success) {
  throw new ValidationError(result.error.issues.map((e) => e.message).join(', '));
}
```

Only fall back to a simple manual check for trivially obvious single-field cases.

### Authorization checks

If checks are needed beyond the `@auth` directive (e.g., ownership, role-based):

```typescript
const entity = await con.getRepository(Entity).findOneBy({ id });
if (!entity) {
  throw new NotFoundError('Entity not found');
}
if (entity.userId !== userId) {
  throw new ForbiddenError('Access denied');
}
```

### Database operations

**Single write:**
```typescript
await con.getRepository(Entity).update({ id }, { field: value });
```

**Multiple writes (transaction):**
```typescript
return con.transaction(async (manager) => {
  await manager.getRepository(EntityA).update({ id }, { field: value });
  await manager.getRepository(EntityB).save({ ... });
});
```

**JSONB flag update:**
```typescript
import { updateFlagsStatement } from '../common';

await con.getRepository(Entity).update({ id }, {
  flags: updateFlagsStatement<Entity>({ newField: value }),
});
```

### Return value

- For `EmptyResponse`: return `{ _: true }`
- For entity types: return the entity or constructed object

### Rules

- No raw SQL — use TypeORM repository methods or query builder
- No `!` non-null assertions — use explicit checks and throw errors
- No `logger.info` for success paths — errors propagate naturally
- No barrel imports — import from specific files, not `index.ts` re-exports
- Use early returns instead of nested conditionals
- Use `const` arrow functions; prefer single props-style argument (`{ a, b }`) over positional args

---

## Step 4 — Verify Schema Registration

Confirm the target schema is already imported and registered in `src/graphql.ts`. Since you are adding to an **existing** schema file, it should already be there. Verify by checking that:

1. The schema file is imported: `import * as <domain> from './schema/<domain>'`
2. Its `typeDefs` are included in the `typeDefs` array
3. Its `resolvers` are merged via `merge()` in the resolvers object

If somehow missing (unlikely for existing schemas), add the import and register both `typeDefs` and `resolvers`.

---

## Step 5 — Write Integration Tests

Add tests in the existing `__tests__/<domain>.ts` test file. If it doesn't exist, create it.

### Test setup

```typescript
import { DataSource } from 'typeorm';
import createOrGetConnection from '../src/db';
import {
  GraphQLTestClient,
  GraphQLTestingState,
  MockContext,
  disposeGraphQLTesting,
  initializeGraphQLTesting,
  saveFixtures,
  testMutationErrorCode,
} from './helpers';

let con: DataSource;
let state: GraphQLTestingState;
let client: GraphQLTestClient;
let loggedUser: string | null = null;

beforeAll(async () => {
  con = await createOrGetConnection();
  state = await initializeGraphQLTesting(() => new MockContext(con, loggedUser));
  client = state.client;
});

beforeEach(async () => {
  loggedUser = null;
  // setup fixtures as needed
});

afterAll(() => disposeGraphQLTesting(state));
```

### Define the mutation

```typescript
const MUTATION = `
  mutation MyMutation($data: MyMutationInput!) {
    myMutation(data: $data) {
      id
      status
    }
  }
`;
```

### Required test cases

**1. Auth check — unauthenticated request:**
```typescript
it('should not allow unauthenticated user', () =>
  testMutationErrorCode(
    client,
    { mutation: MUTATION, variables: { data: validInput } },
    'UNAUTHENTICATED',
  ));
```

**2. Validation — invalid input:**
```typescript
it('should throw validation error for invalid input', async () => {
  loggedUser = '1';
  return testMutationErrorCode(
    client,
    { mutation: MUTATION, variables: { data: invalidInput } },
    'GRAPHQL_VALIDATION_FAILED',
  );
});
```

**3. Success path — mutation succeeds and DB state is correct:**
```typescript
it('should successfully perform the mutation', async () => {
  loggedUser = '1';
  const res = await client.mutate(MUTATION, {
    variables: { data: validInput },
  });
  expect(res.errors).toBeFalsy();
  expect(res.data.myMutation).toMatchObject({ status: 'expected' });

  // Verify database state
  const entity = await con.getRepository(Entity).findOneBy({ id });
  expect(entity.field).toEqual('expected');
});
```

**4. Edge cases** (domain-specific):
- Not found scenarios
- Already exists / duplicate scenarios
- Permission denied (non-owner trying to modify)
- Boundary values for validated fields

### Running tests

```bash
NODE_ENV=test npx jest __tests__/<domain>.ts --testEnvironment=node --runInBand
```

---

## File Locations Quick Reference

| Purpose | Path |
|---|---|
| Code style & architecture | `AGENTS.md` (root) |
| GraphORM read-only constraint | `src/graphorm/AGENTS.md` |
| Common GQL types | `src/schema/common.ts` |
| Schema registration | `src/graphql.ts` |
| Auth context types | `src/Context.ts` |
| Entity definitions | `src/entity/<domain>.ts` |
| Zod schemas | `src/common/schema/<domain>.ts` |
| Test helpers | `__tests__/helpers.ts` |
| Example: simple mutation | `src/schema/settings.ts` — `updateUserSettings` |
| Example: transactional mutation | `src/schema/campaigns.ts` — `startCampaign` |
| Example: mutation tests | `__tests__/settings.ts` |

## What This Skill Does NOT Cover

- **Creating a new schema file** — this skill adds to an existing schema only
- **Database migrations** — if new columns/tables are needed, use the `/format-migration` skill
- **Worker creation** — if the mutation triggers async work, use the `/api-create-worker` skill
- **Infrastructure changes** — no infra config needed for mutations

## Instructions

When the user invokes this skill:

1. Read `AGENTS.md` and `src/graphorm/AGENTS.md` for context
2. Complete Step 0 — ask all six questions before writing any code
3. Complete Step 1 — check for reusable types and report findings
4. Work through Steps 2–5 in order, confirming each step with the user
5. Reference the actual codebase examples listed above rather than relying solely on the templates
6. Follow all code style rules from the AGENTS.md files
