---
name: prd-implementation-planning
description: Bridges approved PRDs to implementation by mapping user stories to tasks with skill assignments, effort estimates, and progress tracking. Use after PRD approval to create actionable implementation plan.
version: 1.0.0
---

# PRD Implementation Planning

## Purpose

Transform approved PRD requirements into actionable implementation tasks with:

- Skill mappings for each task
- Dependency ordering and priority
- Effort estimates
- Progress tracking framework with date/commit tracking

## When NOT to Use This Skill

- PRD is not yet approved (use `prd-reviewing` first)
- Need full technical architecture (use `sparc-planning` after this)
- Simple features not requiring planning
- No PRD exists (use `prd-writing` first)

---

## Workflow

### Step 1: Invoke check-history

Gather project context and understand existing patterns.

### Step 2: Read and Analyze PRD

1. Read the complete PRD document
2. Extract all user stories (US-1, US-2, etc.)
3. Identify technical domains involved:
   - Database/Entities (Vendure, TypeORM)
   - API (GraphQL, REST)
   - UI (Admin UI, Mantine)
   - Testing (Playwright, unit tests)
   - Infrastructure (Helm, K8s)
   - Documentation

### Step 3: Map User Stories to Tasks

For each user story:

1. **Break into implementation tasks**
   - One task per logical unit of work
   - Tasks should be completable in 1-8 hours

2. **Assign primary skill**
   - Reference the Skill Mapping in REFERENCE.md
   - Choose the most specific skill available

3. **Estimate effort**
   - XS: < 1 hour
   - S: 1-2 hours
   - M: 2-4 hours
   - L: 4-8 hours
   - XL: 8+ hours (should be broken down)

4. **Identify dependencies**
   - Which tasks must complete first?
   - Use task numbers (e.g., "Task 1, Task 2")

5. **Set priority**
   - P0: Critical path, blocks other work
   - P1: High priority, needed for feature completion
   - P2: Nice to have, can be deferred

### Step 4: Generate Skill Requirements Table

Summarize all skills needed:

```markdown
### Skill Requirements

| Domain   | Skills Required           | Purpose                  |
| -------- | ------------------------- | ------------------------ |
| Database | `vendure-entity-writing`  | Define data models       |
| API      | `vendure-graphql-writing` | Create GraphQL endpoints |
| UI       | `mantine-developing`      | Build components         |
| Testing  | `playwright-writing`      | E2E test coverage        |
```

### Step 5: Generate Implementation Tasks Table

```markdown
### Implementation Tasks

| #   | Task                       | User Story | Skill                     | Priority | Dependencies | Est. |
| --- | -------------------------- | ---------- | ------------------------- | -------- | ------------ | ---- |
| 1   | Create Order entity        | US-1       | `vendure-entity-writing`  | P0       | None         | M    |
| 2   | Add createOrder mutation   | US-1       | `vendure-graphql-writing` | P0       | 1            | L    |
| 3   | Build order form UI        | US-2       | `mantine-developing`      | P1       | 2            | L    |
| 4   | Write order flow E2E tests | US-1,2     | `playwright-writing`      | P1       | 3            | M    |
```

### Step 6: Initialize Progress Tracker

```markdown
## Implementation Progress

| #   | Task                       | Status  | Started | Completed | Commit |
| --- | -------------------------- | ------- | ------- | --------- | ------ |
| 1   | Create Order entity        | Pending | -       | -         | -      |
| 2   | Add createOrder mutation   | Pending | -       | -         | -      |
| 3   | Build order form UI        | Pending | -       | -         | -      |
| 4   | Write order flow E2E tests | Pending | -       | -         | -      |

### Progress Summary

- **Total Tasks:** 4
- **Completed:** 0 (0%)
- **In Progress:** 0
- **Blocked:** 0
- **Pending:** 4
- **Last Updated:** YYYY-MM-DD
```

### Step 7: Append to PRD Document

Add the Implementation Plan and Progress sections to the PRD document after the existing content (after Timeline & Milestones if present).

---

## Status Values

| Status        | Description    | Date Fields           |
| ------------- | -------------- | --------------------- |
| `Pending`     | Not started    | Both empty            |
| `In Progress` | Active work    | Started only          |
| `Done`        | Completed      | Both + commit hash    |
| `Blocked`     | Cannot proceed | Started, blocker note |
| `Skipped`     | Not needed     | Note explaining why   |

---

## Updating Progress

When a task is completed:

1. Update status to `Done`
2. Fill in `Completed` date (YYYY-MM-DD)
3. Add commit hash (short form, e.g., `abc1234`)
4. Update Progress Summary counts

**Commit Message Pattern:**
Include `[PRD Task N]` in commit message for auto-tracking:

```
feat(orders): add createOrder mutation [PRD Task 2]
```

---

## Integration with Other Skills

**Invokes:**

- `check-history` - Gather context first

**Invoked After:**

- `prd-reviewing` - PRD must be approved

**Works With:**

- `sparc-planning` - For complex tasks needing architecture
- `safe-commit` - Auto-updates progress on task completion

**Updates:**

- PRD document with Implementation Plan sections

---

## Example: E-commerce Shipping Feature

**Given PRD with:**

- US-1: Calculate shipping rates
- US-2: Display rate options
- US-3: Track shipments

**Generated Implementation Plan:**

### Skill Requirements

| Domain   | Skills Required            | Purpose                            |
| -------- | -------------------------- | ---------------------------------- |
| Database | `vendure-entity-writing`   | ShippingRate, Shipment entities    |
| API      | `vendure-graphql-writing`  | Rate calculation, tracking queries |
| Plugin   | `vendure-delivery-plugin`  | Carrier integration                |
| UI       | `vendure-admin-ui-writing` | Shipping settings page             |
| Testing  | `playwright-writing`       | Checkout flow tests                |

### Implementation Tasks

| #   | Task                          | User Story | Skill                      | Priority | Dependencies | Est. |
| --- | ----------------------------- | ---------- | -------------------------- | -------- | ------------ | ---- |
| 1   | Create ShippingRate entity    | US-1       | `vendure-entity-writing`   | P0       | None         | S    |
| 2   | Create Shipment entity        | US-3       | `vendure-entity-writing`   | P0       | None         | S    |
| 3   | Add calculateRates query      | US-1       | `vendure-graphql-writing`  | P0       | 1            | M    |
| 4   | Implement carrier adapter     | US-1       | `vendure-delivery-plugin`  | P0       | 3            | L    |
| 5   | Build rate selector component | US-2       | `vendure-admin-ui-writing` | P1       | 4            | M    |
| 6   | Add tracking query            | US-3       | `vendure-graphql-writing`  | P1       | 2            | M    |
| 7   | Write shipping E2E tests      | US-1,2     | `playwright-writing`       | P1       | 5            | L    |

---

## Anti-Patterns to Avoid

1. **Tasks too large** - Break XL tasks into smaller pieces
2. **Missing skills** - Every task needs a skill mapping
3. **Circular dependencies** - Tasks can't depend on each other
4. **Vague tasks** - Be specific about what's being built
5. **Skipping estimates** - Every task needs effort estimate
6. **Ignoring priority** - P0 tasks should be minimal critical path

---

## Resources

- **REFERENCE.md** - Complete skill mapping by domain
- **TEMPLATE.md** - Copy-paste templates for sections

For comprehensive specification guidance, use the **`specification-architect`** agent.
