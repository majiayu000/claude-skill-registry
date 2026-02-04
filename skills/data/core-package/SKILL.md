---
name: core-package
description: Pure function patterns, Zod schemas, database independence, calculation functions for @repo/core
---

# Core Package Skill

## Core Principles

1. **ZERO Database Dependencies** - No Drizzle, Prisma, Supabase, or ORM imports
2. **Pure Functions Only** - No async, no side effects, deterministic
3. **Zod for Validation** - Runtime type safety at boundaries
4. **Type Inference** - Use `z.infer<>` for single source of truth
5. **Comprehensive Testing** - 100% coverage for calculations
6. **Self-Documenting** - Clear names + JSDoc for public APIs

## Patterns to Follow

### Pattern 1: Pure Function with Parameter Object

```typescript
export interface TSSParams {
  normalizedPower: number;
  duration: number; // seconds
  ftp: number;
}

export function calculateTSS(params: TSSParams): number {
  const { normalizedPower, duration, ftp } = params;

  if (!ftp || ftp === 0) return 0;
  if (!duration || duration === 0) return 0;

  const intensityFactor = normalizedPower / ftp;
  const hours = duration / 3600;

  return ((duration * normalizedPower * intensityFactor) / (ftp * 3600)) * 100;
}
```

**Key Points**:

- Parameter object for 3+ params
- Guard clauses for edge cases
- No mutations, no side effects
- Return value only

### Pattern 2: Zod Schema with Type Inference

```typescript
export const activitySchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1, "Name is required"),
  type: z.enum(["run", "bike", "swim", "other"]),
  distance: z.number().nonnegative().optional(),
  duration: z.number().int().positive(),
});

export type Activity = z.infer<typeof activitySchema>;
```

**Key Points**:

- Schema first, type second
- Custom error messages
- Optional fields explicit
- Single source of truth

### Pattern 3: Discriminated Union with Zod

```typescript
const durationTimeSchema = z.object({
  type: z.literal("time"),
  seconds: z.number().int().positive(),
});

const durationDistanceSchema = z.object({
  type: z.literal("distance"),
  meters: z.number().positive(),
});

export const durationSchema = z.discriminatedUnion("type", [
  durationTimeSchema,
  durationDistanceSchema,
]);

export type Duration = z.infer<typeof durationSchema>;

// Usage with type narrowing
function formatDuration(duration: Duration): string {
  if (duration.type === "time") {
    return `${duration.seconds}s`; // TypeScript knows seconds exists
  } else {
    return `${duration.meters}m`; // TypeScript knows meters exists
  }
}
```

### Pattern 4: JSDoc for Public APIs

````typescript
/**
 * Calculates Training Stress Score (TSS) from power data.
 *
 * TSS quantifies training load based on:
 * - Normalized Power (30-second rolling average)
 * - Intensity Factor (NP / FTP)
 * - Duration
 *
 * Formula: TSS = (duration × NP × IF) / (FTP × 3600) × 100
 *
 * @param params - Power stream, timestamps, and FTP
 * @returns TSS value (0-300+ typical range)
 *
 * @example
 * ```typescript
 * const tss = calculateTSS({
 *   normalizedPower: 250,
 *   duration: 3600,
 *   ftp: 250,
 * });
 * console.log(tss); // 100
 * ```
 */
export function calculateTSS(params: TSSParams): number {
  // Implementation
}
````

### Pattern 5: Comprehensive Testing

```typescript
describe("calculateTSS", () => {
  it("should calculate TSS correctly for 1 hour at FTP", () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 3600,
      ftp: 250,
    });
    expect(result).toBe(100);
  });

  it("should return 0 for zero FTP", () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 3600,
      ftp: 0,
    });
    expect(result).toBe(0);
  });

  it("should handle zero duration", () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 0,
      ftp: 250,
    });
    expect(result).toBe(0);
  });
});
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Database Imports

```typescript
// ❌ WRONG
import { db } from '@repo/supabase';

export async function calculateUserTSS(userId: string) {
  const activities = await db.activities.findMany({ userId });
  return activities.reduce((sum, act) => sum + act.tss, 0);
}

// ✅ CORRECT - Move to tRPC layer
// In packages/trpc/src/routers/activities.ts
export const activityRouter = router({
  getUserTSS: protectedProcedure.query(async ({ ctx }) => {
    const activities = await ctx.db.activities.findMany({...});
    return activities.reduce((sum, act) => sum + act.tss, 0);
  }),
});
```

### Anti-Pattern 2: Async Operations

```typescript
// ❌ WRONG
export async function calculateTSS(...) {
  const ftp = await getFTP(); // NO!
}

// ✅ CORRECT
export function calculateTSS(params: { ftp: number, ... }): number {
  // Pure, synchronous
}
```

### Anti-Pattern 3: Side Effects

```typescript
// ❌ WRONG
let cache = {};
export function calculateTSS(...) {
  cache[key] = value; // MUTATION!
}

// ✅ CORRECT
export function calculateTSS(...): number {
  return value; // No mutations
}
```

## File Organization

```
packages/core/
├── calculations/
│   ├── tss.ts
│   ├── tss.test.ts
│   └── zones.ts
├── schemas/
│   ├── activity.ts
│   ├── activity.test.ts
│   └── profile.ts
├── utils/
│   ├── time.ts
│   └── distance.ts
└── index.ts
```

## Dependencies

**Allowed**:

- `zod` - Validation
- Pure utility libraries (no I/O)

**Forbidden**:

- `@supabase/*`
- `drizzle-orm`, `prisma`
- `@repo/trpc`
- `react`, `react-native`

## Checklist

- [ ] No database imports
- [ ] No async functions
- [ ] Pure functions only
- [ ] Zod schemas for validation
- [ ] Type inference from schemas
- [ ] JSDoc on public APIs
- [ ] 100% test coverage
- [ ] Named exports only

## Related Skills

- [Backend Skill](./backend-skill.md) - Orchestration layer
- [Testing Skill](./testing-skill.md) - Pure function testing

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
