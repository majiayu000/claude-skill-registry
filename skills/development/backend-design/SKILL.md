---
name: backend-design
description: Unified backend development skill covering API design (REST/GraphQL/tRPC), TypeScript expertise, data analysis, and code optimization principles. Use for backend architecture, API patterns, type issues, data processing, and code quality.
allowed-tools:
  - run_command
  - mcp_mcp-server-neon_run_sql
  - mcp_mcp-server-neon_list_slow_queries
  - mcp_sequential-thinking_sequentialthinking
---

# Backend Design Skill

> Unified backend development: API design, TypeScript expertise, data analysis, and code principles.

## When to Use

| Trigger | Action |
|---------|--------|
| API design decision | Check decision tree (REST/GraphQL/tRPC) |
| TypeScript error | Apply type patterns |
| Data analysis needed | Use Python workflow |
| Code optimization | Follow LEVER principles |
| Backend architecture | Apply Three-Pass process |

---

## Content Map

| Reference | Purpose |
|-----------|---------|
| [API Patterns](references/api-patterns.md) | REST vs GraphQL vs tRPC, auth, versioning |
| [TypeScript Patterns](references/typescript-patterns.md) | Type gymnastics, build optimization |
| [Data Analysis](references/data-analysis.md) | Python scripts, statistical methods |
| [Code Principles](references/code-principles.md) | LEVER, Three-Pass, anti-patterns |
| [Database Design](references/database-design.md) | Schema, indexing, query optimization |

---

## Core Philosophy: LEVER

> **L**everage patterns | **E**xtend first | **V**erify reactivity | **E**liminate duplication | **R**educe complexity

**"The best code is no code. The second best structure is the one that already exists."**

### Decision Tree

```
Before coding, ask:
├── Can existing code handle it? → Yes: Extend
├── Can we modify existing patterns? → Yes: Adapt
└── Is new code reusable? → Yes: Abstract → No: Reconsider
```

### Scoring: Extend vs Create

| Factor | Points |
|--------|--------|
| Reuse data structure | +3 |
| Reuse indexes/queries | +3 |
| Reuse >70% code | +5 |
| Circular dependencies | -5 |
| Distinct domain | -3 |

**Score > 5**: Extend existing code.

---

## Three-Pass Implementation

| Pass | Activity | Code |
|------|----------|------|
| 1. Discovery | Find related code, document patterns | None |
| 2. Design | Write interfaces, plan data flow | Minimal |
| 3. Implementation | Execute with max reuse | Essential only |

---

## API Design Decision Tree

```
Who consumes the API?
├── TypeScript monorepo → tRPC (type-safe E2E)
├── Multiple clients/languages → REST (universal)
├── Complex nested data → GraphQL (flexible queries)
└── Not sure → Ask user first!
```

### tRPC Pattern (This Project)

```typescript
// server/featureRouter.ts
export const featureRouter = router({
  list: protectedProcedure.query(async ({ ctx }) => {
    return ctx.db.select().from(table);
  }),

  create: protectedProcedure
    .input(z.object({ name: z.string() }))
    .mutation(async ({ ctx, input }) => {
      const [result] = await ctx.db
        .insert(table)
        .values(input)
        .returning({ id: table.id });
      return result;
    }),
});
```

### API Checklist

- [ ] Chosen API style for THIS context?
- [ ] Defined consistent response format?
- [ ] Planned versioning strategy?
- [ ] Considered authentication needs?
- [ ] Planned rate limiting?

---

## TypeScript Patterns

### "Type instantiation is excessively deep"

```typescript
// ❌ Anti-Pattern
const mutate = useMutation(api.leads.updateStatus);

// ✅ Pattern: Early cast
const mutate = useMutation((api as any).leads.updateStatus);
```

### Branded Types

```typescript
type Brand<K, T> = K & { __brand: T };
type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

// Prevents accidental mixing
function processOrder(orderId: OrderId, userId: UserId) {}
```

### Build Performance

```bash
# Diagnose slow type checking
npx tsc --extendedDiagnostics --incremental false

# Quick validation
bun run check
```

---

## Data Analysis Workflow

### Python Script Pattern

```python
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load data
df = pd.read_csv("data.csv")

# 2. Explore
print(df.describe())

# 3. Analyze
summary = df.groupby("category").agg({"value": ["mean", "sum"]})

# 4. Visualize
plt.figure(figsize=(10, 6))
summary.plot(kind="bar")
plt.savefig("analysis.png", dpi=300)
```

### Statistical Tests

| Question | Test |
|----------|------|
| Difference between groups | t-test, ANOVA |
| Relationship between vars | Correlation, regression |
| Distribution comparison | Chi-square, KS-test |

---

## Database & Schema Principles

**Goal**: 0 new tables. Extend existing.

```typescript
// ❌ DON'T: Create separate table
// campaignTracking: defineTable({ ... })

// ✅ DO: Add optional field
users: defineTable({
  // ...existing
  campaignSource: v.optional(v.string()),
});
```

### Query Patterns

```typescript
// ❌ DON'T: Parallel queries
// getTrialUsers vs getUsers

// ✅ DO: Extend with computed props
export const getUserStatus = query({
  handler: async ctx => {
    const user = await getUser(ctx);
    return {
      ...user,
      isTrial: Boolean(user?.campaign),
      daysRemaining: calculateDays(user),
    };
  },
});
```

---

## Anti-Patterns

| Pattern | Why Bad | Fix |
|---------|---------|-----|
| UI-Driven DB | Schema matches components | Store logically |
| "Just one more table" | Join complexity | Extend existing |
| Parallel APIs | Duplication | Add flags to main |
| Manual state sync | Race conditions | Use useQuery |
| Sequential DB writes | Slow | Use Promise.all |

---

## Review Checklist

### Architecture
- [ ] Extended existing tables/queries?
- [ ] Followed Three-Pass approach?
- [ ] No manual state sync (useEffect)?
- [ ] Added fields are optional?
- [ ] New code < 50% of fresh implementation?

### API
- [ ] Consistent response format?
- [ ] Proper status codes?
- [ ] Rate limiting considered?

### TypeScript
- [ ] No `any` (use `unknown`)?
- [ ] Explicit return types on exports?
- [ ] Const assertions where applicable?

---

## Commands

```bash
# Type check
bun run check

# Format
bun run format

# Test
bun test

# Diagnose TS performance
npx tsc --extendedDiagnostics
```
