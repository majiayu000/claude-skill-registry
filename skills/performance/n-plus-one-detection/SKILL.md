---
name: n-plus-one-detection
description: Detects N+1 query problems in GraphQL resolvers and TypeScript code. Checks for missing DataLoader usage, sequential database queries in loops, and resolver batching opportunities. Use before committing GraphQL resolvers or during performance reviews.
version: 1.0.0
---

# N+1 Query Detection Skill

## Purpose

Detect N+1 query anti-patterns in GraphQL resolvers and TypeScript code. This skill identifies situations where code makes sequential database/service calls in loops instead of batching requests, which causes severe performance degradation.

## What This Skill Checks

### 1. GraphQL Field Resolvers Without DataLoader (Priority: CRITICAL)

**Golden Rule**: Every GraphQL field resolver that loads related data MUST use DataLoader for batching.

**N+1 Anti-Pattern**:

```typescript
// ❌ CRITICAL: N+1 problem - makes 1 query per task
const TaskResolver = {
  assignee: async (parent: Task, _args, context: Context) => {
    // This runs once per task in the list!
    return await context.db.users.findById(parent.assigneeId);
  },
};

// If fetching 100 tasks, this makes 101 queries:
// 1 query to fetch tasks + 100 queries to fetch assignees
```

**Correct Pattern with DataLoader**:

```typescript
// ✅ Batched loading - makes 2 queries total
const TaskResolver = {
  assignee: async (parent: Task, _args, context: Context) => {
    // DataLoader batches all requests in single tick
    return await context.loaders.users.load(parent.assigneeId);
  },
};

// Context setup
class Context {
  loaders = {
    users: new DataLoader(async (ids: string[]) => {
      // Single query fetching ALL requested users
      const users = await this.db.users.findByIds(ids);
      return ids.map((id) => users.find((u) => u.id === id));
    }),
  };
}

// If fetching 100 tasks, this makes 2 queries:
// 1 query to fetch tasks + 1 batched query to fetch all assignees
```

### 2. Sequential Queries in Loops (Priority: CRITICAL)

**Golden Rule**: Never make database/service calls inside loops. Batch fetch all data first.

**N+1 Anti-Pattern**:

```typescript
// ❌ CRITICAL: Sequential queries
async function getTasksWithOwners(taskIds: string[]): Promise<TaskWithOwner[]> {
  const tasks = await db.tasks.findByIds(taskIds);

  const results = [];
  for (const task of tasks) {
    // N+1 problem: one query per task
    const owner = await db.users.findById(task.ownerId);
    results.push({ ...task, owner });
  }
  return results;
}
```

**Correct Pattern with Batch Fetch**:

```typescript
// ✅ Batched loading
async function getTasksWithOwners(taskIds: string[]): Promise<TaskWithOwner[]> {
  const tasks = await db.tasks.findByIds(taskIds);

  // Collect all owner IDs first
  const ownerIds = [...new Set(tasks.map((t) => t.ownerId))];

  // Single batch query for all owners
  const owners = await db.users.findByIds(ownerIds);
  const ownerMap = new Map(owners.map((o) => [o.id, o]));

  // Map in memory (fast)
  return tasks.map((task) => ({
    ...task,
    owner: ownerMap.get(task.ownerId),
  }));
}
```

### 3. Nested Resolver Chains (Priority: HIGH)

**Golden Rule**: Watch for resolver chains that compound N+1 problems exponentially.

**Exponential N+1 Anti-Pattern**:

```typescript
// ❌ CRITICAL: Exponential queries
const TaskResolver = {
  // N+1: One query per task
  assignee: async (parent: Task) => {
    return await db.users.findById(parent.assigneeId);
  },
};

const UserResolver = {
  // N+1: One query per user (which is per task!)
  team: async (parent: User) => {
    return await db.teams.findById(parent.teamId);
  },
};

// Query: { tasks { assignee { team } } }
// If 100 tasks with 50 unique assignees:
// 1 task query + 100 user queries + 100 team queries = 201 queries!
```

**Correct Pattern with Nested DataLoaders**:

```typescript
// ✅ Batched at every level
const TaskResolver = {
  assignee: async (parent: Task, _args, ctx: Context) => {
    return await ctx.loaders.users.load(parent.assigneeId);
  },
};

const UserResolver = {
  team: async (parent: User, _args, ctx: Context) => {
    return await ctx.loaders.teams.load(parent.teamId);
  },
};

// Same query now makes 3 queries total:
// 1 task query + 1 batched user query + 1 batched team query = 3 queries
```

### 4. Missing DataLoader in Context (Priority: HIGH)

**Golden Rule**: Every entity type accessed in resolvers must have a corresponding DataLoader in context.

**Detection Pattern**:

- Find all entity types referenced in resolvers
- Verify each has a DataLoader in Context class
- Flag any missing loaders

### 5. DataLoader Anti-Patterns (Priority: MEDIUM)

**Common mistakes even when using DataLoader**:

**Wrong: Loading in Constructor**

```typescript
// ❌ Loader created once, caches across requests
class Context {
  loader = new DataLoader(this.batchFn); // Shared cache!
}
```

**Correct: Fresh Loader Per Request**

```typescript
// ✅ New loader per request, proper cache scope
function createContext(): Context {
  return {
    loaders: {
      users: new DataLoader(batchLoadUsers),
    },
  };
}
```

**Wrong: Not Handling Missing Data**

```typescript
// ❌ DataLoader batch function doesn't handle missing items
new DataLoader(async (ids: string[]) => {
  const users = await db.users.findByIds(ids);
  return users; // Wrong! Must match input array length and order
});
```

**Correct: Matching Input Array**

```typescript
// ✅ Returns array matching input IDs, with null for missing
new DataLoader(async (ids: string[]) => {
  const users = await db.users.findByIds(ids);
  const userMap = new Map(users.map((u) => [u.id, u]));
  return ids.map((id) => userMap.get(id) ?? null);
});
```

### 6. gRPC/REST Client Calls in Loops (Priority: CRITICAL)

**Golden Rule**: Batch external service calls just like database queries.

**N+1 with External Service**:

```typescript
// ❌ CRITICAL: N service calls
async function enrichTasksWithUAC(
  tasks: Task[],
): Promise<TaskWithPermissions[]> {
  const results = [];
  for (const task of tasks) {
    // N+1 problem with external service!
    const perms = await uacClient.checkPermissions({ taskId: task.id });
    results.push({ ...task, permissions: perms });
  }
  return results;
}
```

**Correct with Batch gRPC Call**:

```typescript
// ✅ Single batched gRPC call
async function enrichTasksWithUAC(
  tasks: Task[],
): Promise<TaskWithPermissions[]> {
  const taskIds = tasks.map((t) => t.id);

  // Single batched gRPC request
  const permsResponse = await uacClient.batchCheckPermissions({ taskIds });
  const permsMap = new Map(permsResponse.results.map((r) => [r.taskId, r]));

  return tasks.map((task) => ({
    ...task,
    permissions: permsMap.get(task.id),
  }));
}
```

## Step-by-Step Execution

### Step 1: Identify TypeScript/GraphQL Files

```bash
# Find all relevant files
find . -name "*.resolver.ts" -o -name "*.graphql.ts" -o -name "*Resolver.ts"
find . -name "*.ts" -path "*/resolvers/*"
```

### Step 2: Read Resolver Files

Use Read tool to examine files, focusing on:

- Resolver function definitions
- Field resolver implementations
- Context usage
- DataLoader instantiation
- Loop constructs with async calls

### Step 3: Analyze for N+1 Patterns

For each resolver file, check:

**A. Field Resolvers Without DataLoader**

1. Identify all field resolver functions
2. Check if they make direct database/service calls
3. Verify they use `context.loaders.X.load()` pattern
4. Flag any direct calls: `db.*.find*`, `*Client.*`, `fetch()`

**B. Sequential Queries in Loops**

1. Find all loop constructs: `for`, `forEach`, `map` with async
2. Check for `await` inside loop body
3. Verify any await is not a database/service call
4. Flag loops with awaited queries

**C. Context DataLoader Completeness**

1. Extract all entity types from resolvers
2. Find Context class/interface definition
3. Verify each entity type has corresponding loader
4. Flag missing loaders

**D. DataLoader Implementation Quality**

1. Find DataLoader instantiations
2. Check batch function returns array matching input
3. Verify per-request instantiation (not global)
4. Check error handling in batch functions

**E. Nested Resolver Analysis**

1. Map resolver dependency chains
2. Identify multi-level nesting (task -> user -> team)
3. Verify each level uses DataLoader
4. Calculate potential query multiplication

**F. External Service Calls**

1. Find gRPC client calls, REST fetch calls
2. Check if inside loops or resolvers
3. Verify batching strategy exists
4. Flag unbatched external calls

### Step 4: Generate Report

```markdown
## N+1 Query Detection: [file_path]

### ✅ Resolvers With Correct Batching

- `Task.assignee` ([file:line]) - Uses DataLoader
- `getTasksWithOwners()` ([file:line]) - Batch fetch pattern

### 🚨 CRITICAL N+1 Problems

#### Field Resolver Without DataLoader

- **Resolver**: `Task.assignee` ([file:line])
  - **Issue**: Direct database query in resolver
  - **Code**: `await db.users.findById(parent.assigneeId)`
  - **Impact**: 1 query per task (100 tasks = 100 queries)
  - **Fix**: Use `context.loaders.users.load(parent.assigneeId)`

#### Sequential Queries in Loop

- **Function**: `getTasksWithOwners` ([file:line])
  - **Issue**: Database query inside for-loop
  - **Code**: `for (const task of tasks) { await db.users.findById(...) }`
  - **Impact**: N+1 queries (1 + number of tasks)
  - **Fix**: Batch fetch owner IDs, then map in memory

#### Nested Resolver Chain Without Batching

- **Chain**: `Task.assignee.team.organization` ([file:line])
  - **Issue**: Missing DataLoader at User.team level
  - **Impact**: Exponential queries (100 tasks × team queries)
  - **Fix**: Add DataLoader for teams in context

#### External Service in Loop

- **Function**: `enrichTasksWithUAC` ([file:line])
  - **Issue**: gRPC call inside loop
  - **Code**: `for (const task of tasks) { await uacClient.check(...) }`
  - **Impact**: N service calls (network overhead × N)
  - **Fix**: Use `uacClient.batchCheck()` with all task IDs

### ⚠️ HIGH Priority Issues

#### Missing DataLoader in Context

- **Entity Type**: `Team`
  - **Issue**: No DataLoader for teams in Context
  - **Referenced In**: User.team resolver ([file:line])
  - **Fix**: Add `teams: new DataLoader(batchLoadTeams)` to context

### ℹ️ MEDIUM Priority Issues

#### DataLoader Caching Scope

- **Location**: Context constructor ([file:line])
  - **Issue**: DataLoader created in constructor (shared cache)
  - **Fix**: Create fresh DataLoader per request in factory function

#### DataLoader Batch Function Error

- **Loader**: `users` DataLoader ([file:line])
  - **Issue**: Batch function doesn't handle missing users
  - **Fix**: Return array with null for missing IDs
```

### Step 5: Provide Fix Examples

For each critical issue, provide before/after code:

````markdown
#### Example Fix: Field Resolver

**Before** (N+1 problem):

```typescript
const TaskResolver = {
  assignee: async (parent: Task, _args, context: Context) => {
    return await context.db.users.findById(parent.assigneeId); // ❌
  },
};
```
````

**After** (batched with DataLoader):

```typescript
const TaskResolver = {
  assignee: async (parent: Task, _args, context: Context) => {
    return await context.loaders.users.load(parent.assigneeId); // ✅
  },
};

// Add to Context:
class Context {
  loaders = {
    users: new DataLoader(async (ids: readonly string[]) => {
      const users = await this.db.users.findByIds(Array.from(ids));
      const userMap = new Map(users.map((u) => [u.id, u]));
      return ids.map((id) => userMap.get(id) ?? null);
    }),
  };
}
```

**Impact**: Reduces 100 queries to 1 batched query.

````

### Step 6: Performance Impact Analysis

```markdown
## Performance Impact Estimation

### Current State (with N+1 problems)
- 100 tasks query: **201 database queries**
  - 1 task query
  - 100 assignee queries (N+1)
  - 100 team queries (N+1)
- Estimated latency: **2-5 seconds**

### After Fixes (with DataLoader)
- 100 tasks query: **3 database queries**
  - 1 task query
  - 1 batched assignee query
  - 1 batched team query
- Estimated latency: **50-200ms**

### Improvement: **90-96% latency reduction**
````

### Step 7: Summary Statistics

```markdown
## Summary

- Files checked: X
- Resolvers analyzed: Y
- N+1 problems found: Z
  - CRITICAL field resolvers: A
  - CRITICAL loops: B
  - HIGH missing loaders: C
  - MEDIUM implementation issues: D
- Clean resolvers: W
```

## Integration Points

This skill is invoked by:

- **`quality-check`** skill for TypeScript/GraphQL projects
- **`safe-commit`** skill (via quality-check)
- Directly when reviewing GraphQL performance

## Exit Criteria

- All GraphQL resolvers analyzed
- Report generated with specific N+1 locations
- Performance impact estimated
- Fix examples provided for all critical issues
- CRITICAL issues should block commit

## Example Usage

```bash
# Manual invocation
/skill n-plus-one-detection

# Automatic invocation via quality-check
/skill quality-check  # Detects TypeScript+GraphQL, invokes this skill
```

## References

- DataLoader: https://github.com/graphql/dataloader
- GraphQL N+1 Problem: https://www.apollographql.com/blog/optimizing-your-graphql-request-waterfalls-7c3f3360b051
- Hermes Code Reviewer: N+1 Detection Patterns
- Facebook DataLoader Pattern: https://www.youtube.com/watch?v=OQTnXNCDywA
