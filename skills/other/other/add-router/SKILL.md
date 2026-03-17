---
name: add-router
description: Create a tRPC router with CRUD procedures, OpenAPI meta, and tests
---

# Add Router Skill

Create a new tRPC router with CRUD procedures, OpenAPI meta, and test file for x4-mono.

## Arguments

The user describes the resource. If unclear, ask for:

- Resource name (singular, camelCase for router, e.g., `comment`)
- Which procedures: list, get, create, update, delete (default: all)
- Auth level: public, protected, or admin
- Whether it needs ownership checks

## File Locations

- **Router**: `apps/api/src/routers/{name}.ts`
- **Registration**: `apps/api/src/routers/index.ts`
- **Tests**: `apps/api/src/__tests__/{name}.test.ts`
- **Schemas**: `packages/shared/utils/validators.ts` (if not already there)

## Router Template

Reference: `apps/api/src/routers/projects.ts`

```typescript
import { eq, sql } from 'drizzle-orm';
import { router, publicProcedure, protectedProcedure } from '../trpc';
import { Errors } from '../lib/errors';
import { tableName } from '@x4/database';
import {
  CreateEntitySchema,
  UpdateEntitySchema,
  EntityResponseSchema,
  EntityListResponseSchema,
  IdParamSchema,
  PaginationSchema,
} from '@x4/shared/utils';

export const entityRouter = router({
  list: publicProcedure
    .meta({ openapi: { method: 'GET', path: '/entities', tags: ['Entity'] } })
    .input(PaginationSchema)
    .output(EntityListResponseSchema)
    .query(async ({ ctx, input }) => {
      const items = await ctx.db.select().from(tableName).limit(input.limit).offset(input.offset);
      return { items, total: items.length, limit: input.limit, offset: input.offset };
    }),

  get: publicProcedure
    .meta({ openapi: { method: 'GET', path: '/entities/{id}', tags: ['Entity'] } })
    .input(IdParamSchema)
    .output(EntityResponseSchema)
    .query(async ({ ctx, input }) => {
      const [record] = await ctx.db.select().from(tableName).where(eq(tableName.id, input.id));
      if (!record) throw Errors.notFound('Entity').toTRPCError();
      return record;
    }),

  create: protectedProcedure
    .meta({ openapi: { method: 'POST', path: '/entities', tags: ['Entity'], protect: true } })
    .input(CreateEntitySchema)
    .output(EntityResponseSchema)
    .mutation(async ({ ctx, input }) => {
      const [record] = await ctx.db
        .insert(tableName)
        .values({ ...input, ownerId: ctx.user.userId })
        .returning();
      return record;
    }),

  update: protectedProcedure
    .meta({ openapi: { method: 'PATCH', path: '/entities/{id}', tags: ['Entity'], protect: true } })
    .input(UpdateEntitySchema)
    .output(EntityResponseSchema)
    .mutation(async ({ ctx, input }) => {
      const { id, ...data } = input;
      const [existing] = await ctx.db.select().from(tableName).where(eq(tableName.id, id));
      if (!existing) throw Errors.notFound('Entity').toTRPCError();
      if (existing.ownerId !== ctx.user.userId && ctx.user.role !== 'admin') {
        throw Errors.forbidden('Not the owner').toTRPCError();
      }
      const [updated] = await ctx.db
        .update(tableName)
        .set(data)
        .where(eq(tableName.id, id))
        .returning();
      return updated;
    }),

  delete: protectedProcedure
    .meta({
      openapi: { method: 'DELETE', path: '/entities/{id}', tags: ['Entity'], protect: true },
    })
    .input(IdParamSchema)
    .output(z.object({ success: z.boolean() }))
    .mutation(async ({ ctx, input }) => {
      const [existing] = await ctx.db.select().from(tableName).where(eq(tableName.id, input.id));
      if (!existing) throw Errors.notFound('Entity').toTRPCError();
      if (existing.ownerId !== ctx.user.userId && ctx.user.role !== 'admin') {
        throw Errors.forbidden('Not the owner').toTRPCError();
      }
      await ctx.db.delete(tableName).where(eq(tableName.id, input.id));
      return { success: true };
    }),
});
```

## Registration

Add to `apps/api/src/routers/index.ts`:

```typescript
import { entityRouter } from './entity';

export const appRouter = router({
  // ... existing routers
  entity: entityRouter,
});
```

## Workflow

1. Ensure Zod schemas exist (use `/add-schema` first if needed)
2. Ensure database table exists (use `/add-table` first if needed)
3. Create router file at `apps/api/src/routers/{name}.ts`
4. Register in `apps/api/src/routers/index.ts`
5. Run `bun turbo type-check` to verify AppRouter updates
6. Create test file at `apps/api/src/__tests__/{name}.test.ts` (use `/add-test` or bun-test-gen)
7. Run `bun test --cwd apps/api` to verify
