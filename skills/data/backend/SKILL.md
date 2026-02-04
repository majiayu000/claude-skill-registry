---
name: backend
description: tRPC router patterns, Supabase integration, API design, error handling for backend services
---

## Core Principles

1. **Validate All Inputs** - Every procedure uses Zod schema validation
2. **Protect Endpoints** - Use protectedProcedure for auth-required operations
3. **Verify Ownership** - Always check user owns resource before mutation
4. **Handle Errors Gracefully** - Convert Supabase errors to TRPCError
5. **Use Core for Logic** - Business calculations go in @repo/core
6. **Type-Safe Everywhere** - Leverage tRPC + TypeScript end-to-end

## Patterns to Follow

### Pattern 1: Protected Procedure with Input Validation

```typescript
export const activitiesRouter = createTRPCRouter({
  create: protectedProcedure
    .input(
      z.object({
        name: z.string().min(1),
        type: z.enum(["run", "bike", "swim", "other"]),
        distance: z.number().nonnegative().optional(),
        duration: z.number().int().positive(),
      }),
    )
    .mutation(async ({ ctx, input }) => {
      const { data, error } = await ctx.supabase
        .from("activities")
        .insert({
          ...input,
          profile_id: ctx.session.user.id, // Add user ID
        })
        .select()
        .single();

      if (error) {
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: "Failed to create activity",
        });
      }

      return data;
    }),
});
```

### Pattern 2: Ownership Verification Before Mutation

```typescript
delete: protectedProcedure
  .input(z.object({ id: z.string().uuid() }))
  .mutation(async ({ ctx, input }) => {
    // Verify ownership FIRST
    const { data: activity } = await ctx.supabase
      .from('activities')
      .select('id, profile_id')
      .eq('id', input.id)
      .eq('profile_id', ctx.session.user.id)
      .single();

    if (!activity) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: 'Activity not found',
      });
    }

    // Delete with double-check
    const { error } = await ctx.supabase
      .from('activities')
      .delete()
      .eq('id', input.id)
      .eq('profile_id', ctx.session.user.id);

    if (error) throw new TRPCError({
      code: 'INTERNAL_SERVER_ERROR',
      message: error.message,
    });

    return { success: true };
  }),
```

### Pattern 3: Complex Query with Filters

```typescript
list: protectedProcedure
  .input(
    z.object({
      limit: z.number().min(1).max(100).default(20),
      offset: z.number().min(0).default(0),
      type: z.enum(['run', 'bike', 'swim']).optional(),
      dateFrom: z.string().optional(),
      sortBy: z.enum(['date', 'distance']).default('date'),
    })
  )
  .query(async ({ ctx, input }) => {
    let query = ctx.supabase
      .from('activities')
      .select('*', { count: 'exact' })
      .eq('profile_id', ctx.session.user.id);

    // Apply filters conditionally
    if (input.type) {
      query = query.eq('type', input.type);
    }
    if (input.dateFrom) {
      query = query.gte('started_at', input.dateFrom);
    }

    // Apply sorting
    query = query.order(
      input.sortBy === 'date' ? 'started_at' : 'distance_meters',
      { ascending: false }
    );

    // Apply pagination
    query = query.range(input.offset, input.offset + input.limit - 1);

    const { data, error, count } = await query;

    if (error) throw new TRPCError({
      code: 'INTERNAL_SERVER_ERROR',
      message: error.message,
    });

    return {
      items: data || [],
      total: count || 0,
      hasMore: (count || 0) > input.offset + input.limit,
    };
  }),
```

### Pattern 4: Manual Transaction with Rollback

```typescript
createWithStreams: protectedProcedure
  .input(
    z.object({
      activity: activitySchema,
      streams: z.object({
        gps: z.array(z.object({lat: z.number(), lng: z.number(), timestamp: z.number()})).optional(),
        power: z.array(z.number()).optional(),
        heartRate: z.array(z.number()).optional(),
        cadence: z.array(z.number()).optional(),
        pace: z.array(z.number()).optional(),
        altitude: z.array(z.number()).optional(),
        speed: z.array(z.number()).optional(),
      }),
    })
  )
  .mutation(async ({ ctx, input }) => {
    import { compressStreams } from '@repo/core';

    // 1. Compress stream data
    const compressedStreams = compressStreams(input.streams);

    // 2. Create activity with embedded stream data
    const { data: activity, error } = await ctx.supabase
      .from('activities')
      .insert({
        ...input.activity,
        metrics: {
          streams: compressedStreams,
        },
      })
      .select()
      .single();

    if (error) {
      throw new TRPCError({
        code: 'INTERNAL_SERVER_ERROR',
        message: `Failed to create activity: ${error.message}`,
      });
    }

    return activity;
  }),
```

### Pattern 5: Use Core Package for Business Logic

```typescript
calculateMetrics: protectedProcedure
  .input(z.object({ activityId: z.string().uuid() }))
  .mutation(async ({ ctx, input }) => {
    // Fetch data from database
    const { data: activity } = await ctx.supabase
      .from('activities')
      .select('*, metrics')
      .eq('id', input.activityId)
      .single();

    // Use core package for calculations
    import { calculateTSS, decompressStreams } from '@repo/core';

    const streams = decompressStreams(activity.metrics.streams);
    const tss = calculateTSS({
      powerStream: streams.power,
      duration: activity.duration_seconds,
      ftp: activity.profile.ftp,
    });

    // Update database with results
    await ctx.supabase
      .from('activities')
      .update({
        metrics: {
          ...activity.metrics,
          tss
        }
      })
      .eq('id', input.activityId);

    return { tss };
  }),
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Missing Auth on Protected Routes

```typescript
// ❌ BAD
.query(async ({ ctx, input }) => {
  // No auth check - anyone can access
  const { data } = await ctx.supabase.from('users').select('*');
})

// ✅ CORRECT
protectedProcedure
  .query(async ({ ctx, input }) => {
    // Auth enforced by middleware
    const { data } = await ctx.supabase
      .from('activities')
      .eq('profile_id', ctx.session.user.id);
  })
```

### Anti-Pattern 2: Missing Input Validation

```typescript
// ❌ BAD
.mutation(async ({ ctx, input }) => {
  await ctx.supabase.from('activities').insert(input);
})

// ✅ CORRECT
.input(activitySchema)
.mutation(async ({ ctx, input }) => {
  await ctx.supabase.from('activities').insert(input);
})
```

### Anti-Pattern 3: Silently Ignoring Errors

```typescript
// ❌ BAD
const { data, error } = await ctx.supabase.from("activities").select("*");
return data || [];

// ✅ CORRECT
const { data, error } = await ctx.supabase.from("activities").select("*");
if (error) {
  throw new TRPCError({
    code: "INTERNAL_SERVER_ERROR",
    message: error.message,
  });
}
return data || [];
```

## File Organization

```
packages/trpc/src/
├── routers/
│   ├── index.ts          # Aggregate all routers
│   ├── activities.ts     # Activity CRUD
│   ├── profiles.ts       # Profile management
│   └── auth.ts           # Authentication
├── context.ts            # tRPC context (session, supabase)
└── trpc.ts               # tRPC initialization
```

## Database Workflow (CRITICAL)

1. **No Manual Migrations**: Never manually create migration files.
2. **Declarative Changes**: Modify `packages/supabase/schemas/init.sql` (or source of truth).
3. **Generate**: Use `supabase db diff -f <kebab-case-name>` to generate migration files.
   - Name MUST be lowercase kebab-case (e.g., `add-performance-metrics`).
4. **Sync**: Run `pnpm update-types` to sync DB types and Zod schemas.

## Checklist

- [ ] All inputs validated with Zod
- [ ] Protected procedures for auth-required operations
- [ ] Ownership verified before mutations
- [ ] Errors converted to TRPCError
- [ ] Business logic in @repo/core
- [ ] Cache invalidation handled client-side
- [ ] Pagination for large datasets
- [ ] Proper error codes (UNAUTHORIZED, NOT_FOUND, etc.)

## Related Skills

- [Core Package Skill](./core-package-skill.md) - Business logic
- [Web Frontend Skill](./web-frontend-skill.md) - tRPC client
- [Mobile Frontend Skill](./mobile-frontend-skill.md) - tRPC mobile

## Version History

- **1.0.0** (2026-01-21): Initial version

---

**Next Review**: 2026-02-21

# Schema Validation

## When to Use

- User needs to create a new data schema
- User wants to add validation to forms
- User needs to validate API inputs
- User asks to update existing schemas

## What This Skill Does

1. Creates Zod schemas with proper validation
2. Infers TypeScript types from schemas
3. Adds custom validation rules
4. Implements refined schemas with dependencies
5. Creates form-specific sub-schemas

## Basic Schema Pattern

```typescript
import { z } from "zod";

export const activitySchema = z
  .object({
    id: z.string().uuid(),
    name: z.string().min(1, "Name is required"),
    type: z.enum(["run", "bike", "swim", "other"]),
    distance: z.number().positive().optional(),
    duration: z.number().int().positive("Duration must be positive"),
    startTime: z.date(),
    endTime: z.date(),
  })
  .refine((data) => data.endTime > data.startTime, {
    message: "End time must be after start time",
    path: ["endTime"],
  });

export type Activity = z.infer<typeof activitySchema>;
```

## Form Schema Pattern

```typescript
export const createActivitySchema = activitySchema
  .omit({
    id: true,
  })
  .extend({
    // Form-specific fields
    notes: z.string().max(500).optional(),
    isPrivate: z.boolean().default(false),
  });

export type CreateActivityInput = z.infer<typeof createActivitySchema>;
```

## Validation in Forms

```typescript
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { createActivitySchema } from "@repo/core/schemas";

export function useCreateActivityForm() {
  const form = useForm({
    resolver: zodResolver(createActivitySchema),
    defaultValues: {
      name: "",
      type: "run",
      distance: undefined,
      duration: 0,
      startTime: new Date(),
      endTime: new Date(),
      notes: "",
      isPrivate: false,
    },
  });

  return form;
}
```

## API Input Validation

```typescript
export const activityListInput = z.object({
  limit: z.number().min(1).max(100).default(20),
  offset: z.number().min(0).default(0),
  type: z.enum(["run", "bike", "swim", "other"]).optional(),
  search: z.string().optional(),
});
```

## Custom Validation

```typescript
export const profileSchema = z
  .object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
    ftp: z.number().min(50).max(500).optional(),
  })
  .refine(
    (data) => {
      if (data.email.includes("+")) {
        return data.name.length > 5;
      }
      return true;
    },
    {
      message: "Name must be longer for email aliases",
      path: ["name"],
    },
  );
```
