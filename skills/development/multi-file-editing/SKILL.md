---
name: multi-file-editing
description: Strategies for coordinated changes across multiple files with Claude Code. Use when making API changes, updating interfaces, refactoring shared code, or performing migrations. Covers dependency ordering, atomic vs incremental changes, and validation patterns.
version: 1.0.0
author: Claude Code SDK
tags: [multi-file, editing, coordination, changes]
---

# Multi-File Editing

Strategies for making coordinated changes across multiple files safely and efficiently.

## Quick Reference

| Strategy | Use When |
|----------|----------|
| Atomic | All changes must succeed together or none at all |
| Incremental | Changes can be applied progressively with validation |
| Staged | Large refactors needing review checkpoints |

| Order | Description |
|-------|-------------|
| Interfaces first | Update types/interfaces before implementations |
| Contracts first | Change API contracts before consumers |
| Leaf-to-root | Start with files that have no dependents |

## Core Principles

### 1. Understand the Dependency Graph

Before editing, map which files depend on which:

```
Types/Interfaces (edit first)
    |
    v
Service/Business Logic
    |
    v
API Routes/Controllers
    |
    v
Tests (edit last)
```

### 2. Edit in Dependency Order

**Always edit in this order:**

1. **Shared types and interfaces** - Foundation for all other code
2. **Utility functions** - Used by multiple files
3. **Core business logic** - Services, repositories
4. **API layer** - Routes, controllers, handlers
5. **Frontend components** - Consumers of API
6. **Tests** - Validate the changes

### 3. Validate at Each Step

After each file edit:
- [ ] TypeScript compiles without errors
- [ ] Related tests still pass
- [ ] No broken imports

## Planning Workflow

### Step 1: Identify All Affected Files

```bash
# Find files using the symbol you're changing
rg -l "SymbolName" --type ts

# Find import references
rg "from.*module-name" --type ts
```

- [ ] List all files that will need changes
- [ ] Identify the dependency order
- [ ] Note files that can be edited in parallel

### Step 2: Create Change Plan

Document your change plan:

```markdown
## Change Plan: Rename UserData to UserProfile

### Phase 1: Type Definitions
- [ ] src/types/user.ts - Rename interface
- [ ] src/types/index.ts - Update export

### Phase 2: Service Layer
- [ ] src/services/user.service.ts - Update function signatures
- [ ] src/repositories/user.repository.ts - Update return types

### Phase 3: API Layer
- [ ] src/routes/user.routes.ts - Update handlers

### Phase 4: Tests
- [ ] tests/user.service.test.ts - Update test data
- [ ] tests/user.routes.test.ts - Update assertions
```

### Step 3: Execute in Order

- [ ] Complete each phase before moving to next
- [ ] Run type checker after each phase
- [ ] Commit at logical checkpoints

## Common Scenarios

### Scenario 1: Renaming a Type/Interface

**Order of operations:**

1. **Edit type definition**
   ```typescript
   // src/types/user.ts
   // Change: interface UserData -> interface UserProfile
   ```

2. **Update exports**
   ```typescript
   // src/types/index.ts
   export { UserProfile } from './user';
   ```

3. **Update all imports** (can be parallel)
   ```typescript
   // Each consuming file
   import { UserProfile } from '../types';
   ```

4. **Update usage** in each file

5. **Run validation**
   ```bash
   bun run typecheck
   bun test
   ```

### Scenario 2: Adding a Required Field

**Order of operations:**

1. **Update interface**
   ```typescript
   interface User {
     id: string;
     email: string;
     createdAt: Date;  // New required field
   }
   ```

2. **Update factory/builder functions**

3. **Update database schema** (if applicable)

4. **Update API handlers** to include field

5. **Update tests** with new field

6. **Validate**

### Scenario 3: Changing Function Signature

**Order of operations:**

1. **Update function definition**

2. **Update all call sites** - find with:
   ```bash
   rg "functionName\(" --type ts
   ```

3. **Update tests**

4. **Validate**

## Validation Checklist

After completing multi-file changes:

- [ ] `bun run typecheck` passes
- [ ] `bun test` passes
- [ ] No console errors in browser (for frontend)
- [ ] API endpoints respond correctly
- [ ] No orphaned imports or exports

## Reference Files

| File | Contents |
|------|----------|
| [STRATEGIES.md](./STRATEGIES.md) | Detailed strategies (atomic, incremental, staged) |
| [PATTERNS.md](./PATTERNS.md) | Common patterns for API changes, migrations |
| [COORDINATION.md](./COORDINATION.md) | Dependency ordering and validation techniques |

## Quick Commands

```bash
# Find all files using a symbol
rg -l "SymbolName" --type ts

# Find all imports of a module
rg "from.*['\"](.*module-name)" --type ts

# Type check without emitting
bun run typecheck

# Run specific test file
bun test path/to/file.test.ts

# Find files modified in current session
git status --short
```

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Editing tests first | Edit source first, tests last |
| Random edit order | Follow dependency order |
| Skipping validation | Validate after each phase |
| Massive single commits | Commit at logical checkpoints |
| Ignoring type errors | Fix type errors before continuing |

## When to Use Each Strategy

### Use Atomic Changes When:
- Changes must all succeed or all fail
- Rollback would be complex
- Team is waiting on the feature

### Use Incremental Changes When:
- Changes can be validated progressively
- You want to catch issues early
- Complex refactor with many files

### Use Staged Changes When:
- Large refactor spanning days
- Need team review at checkpoints
- High-risk changes to critical code

See [STRATEGIES.md](./STRATEGIES.md) for detailed guidance on each approach.
