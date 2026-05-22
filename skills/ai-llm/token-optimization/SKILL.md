---
name: token-optimization
description: CRITICAL - Read FIRST before any work. Strategies to minimize token usage and reduce costs by 60-80%.
---

// Project Autopilot - Token Cost Reduction Strategies
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

# Token Optimization Skill

**READ THIS SKILL FIRST.** Apply these strategies to reduce token costs by 60-80%.

---

## Quick Reference Card

| Strategy | Savings | Priority |
|----------|---------|----------|
| Read files partially | 40-60% | 🔴 Critical |
| Use Haiku for simple tasks | 50-90% | 🔴 Critical |
| Cache in learnings.md | 20-40% | 🔴 Critical |
| Batch related work | 20-40% | 🟡 High |
| Concise output | 20-30% | 🟡 High |
| Skip re-validation | 10-20% | 🟢 Medium |

---

## 1. PARTIAL FILE READING

### The Problem
Reading entire files wastes tokens. A 500-line file = ~5,000 tokens.

### The Solution

```bash
# ❌ NEVER do this
Read entire file: src/services/userService.ts

# ✅ ALWAYS do this
Read lines 1-30: src/services/userService.ts  # imports + interface
Read lines 45-60: src/services/userService.ts  # specific function
```

### Reading Strategies

| Need | Strategy | Tokens |
|------|----------|--------|
| File exists? | `ls` or `find` | ~10 |
| File structure | Read first 30 lines | ~300 |
| Specific function | Search + read range | ~200 |
| Full understanding | Read in chunks | varies |

### Commands

```bash
# List files (no content)
ls -la src/services/

# Find specific file
find . -name "*.service.ts"

# Read just imports
head -30 src/services/user.service.ts

# Read specific lines
sed -n '45,60p' src/services/user.service.ts

# Find function location
grep -n "function getUserById" src/services/user.service.ts
```

### Read Priority

1. **Read file list** (always first, ~50 tokens)
2. **Read imports/exports** (if needed, ~100 tokens)
3. **Read specific function** (if modifying, ~200 tokens)
4. **Read full file** (ONLY if absolutely necessary)

---

## 2. MODEL SELECTION

### Cost Comparison (Claude 4.5)

| Model | Input/1M | Output/1M | Relative |
|-------|----------|-----------|----------|
| Haiku | $1.00 | $5.00 | 1x |
| Sonnet | $3.00 | $15.00 | 3x |
| Opus | $5.00 | $25.00 | 5x |

### When to Use Each

| Task | Model | Why |
|------|-------|-----|
| List files | Haiku | Simple operation |
| Read/parse config | Haiku | No creativity needed |
| Simple text replace | Haiku | Pattern matching |
| Standard implementation | Sonnet | Balanced |
| Writing tests | Sonnet | Needs understanding |
| Complex architecture | Opus | Needs deep reasoning |
| Multi-file refactor | Opus | Complex dependencies |

### Decision Tree

```
Is task simple (list, read, simple edit)?
  YES → Haiku (save 90%+)
  NO → Does task require complex reasoning?
    NO → Sonnet
    YES → Is it architecture/design decision?
      YES → Opus
      NO → Try Sonnet first, Opus if fails
```

---

## 3. CACHING IN LEARNINGS.MD

### What to Cache

```markdown
# .autopilot/learnings.md

## Project Structure (CACHED - don't re-read)
```
src/
├── services/     # Business logic
├── routes/       # API endpoints
├── models/       # Database entities
├── utils/        # Helpers
└── types/        # TypeScript types
```

## Key Types (CACHED - don't re-read types.ts)
```typescript
interface User { id: string; email: string; role: Role }
interface Order { id: string; userId: string; total: number }
type Role = 'admin' | 'user' | 'guest'
```

## Conventions (CACHED - don't re-analyze)
- Services use constructor injection
- Routes are async/await
- Tests use Jest + supertest
- Errors extend BaseError

## File Patterns (CACHED)
- Services: `src/services/*.service.ts`
- Routes: `src/routes/*.routes.ts`
- Tests: `__tests__/*.test.ts`
```

### Before Reading Any File

```
1. CHECK learnings.md - is info already cached?
2. CHECK current context - did we read it this session?
3. If NO to both, then read (and cache for future)
```

---

## 4. BATCHING OPERATIONS

### Bad: Separate Tasks

```
Task 1: Create userRoutes.ts        # Load context
Task 2: Create orderRoutes.ts       # Load context again
Task 3: Create productRoutes.ts     # Load context again
Task 4: Create index.ts             # Load context again
= 4 context loads
```

### Good: Batched Task

```
Task 1: Create all route files + index
= 1 context load
```

### Batching Rules

| Batch Together | Keep Separate |
|----------------|---------------|
| Same feature files | Different features |
| Create + export | Create + full test suite |
| Multiple simple edits | Complex + simple |
| Related configs | Unrelated configs |

---

## 5. CONCISE OUTPUT

### Bad: Verbose

```markdown
I will now proceed to create the UserService class. This service 
will be responsible for handling all user-related operations 
including creating new users, retrieving users by their ID, 
updating user information, and deleting users from the system.

The service will follow the repository pattern that I observed
in the existing codebase, specifically matching the patterns
found in OrderService and ProductService...

[200 more tokens of explanation]

Here is the implementation:
[code]

I have successfully created the UserService. The service includes
four main methods: createUser, getUserById, updateUser, and 
deleteUser. Each method properly handles errors and follows
the established patterns...

[150 more tokens of summary]
```

### Good: Concise

```markdown
Creating UserService (CRUD, matches existing pattern).

[code]

✅ UserService created
```

### Output Rules

| Context | Max Length |
|---------|------------|
| Task start | 1 line |
| Progress | 1-2 lines |
| Completion | 1 line + key info |
| Error | Error + fix only |

### Remove These Phrases

- "I will now proceed to..."
- "Let me explain..."
- "As you can see..."
- "I have successfully..."
- "In conclusion..."
- Any restating of the task

---

## 6. SKIP UNNECESSARY WORK

### Validation Shortcuts

```
IF previous task passed build/lint/tests
AND current task modifies DIFFERENT files
THEN skip full validation
ONLY run tests for current changes
```

### What to Skip

| Skip | When | Savings |
|------|------|---------|
| Full test suite | Only changed 1 file | 50%+ |
| Re-reading types | Already in learnings.md | 100% |
| Architecture review | Implementation task | 80% |
| Full code review | Small change | 60% |

---

## 7. CONTEXT MANAGEMENT

### Context Budget

```
Total: 200K tokens

Smart allocation:
- System: 10K (fixed)
- Cached info: 5K (learnings.md summary)
- Current phase: 5K (minimal)
- Active task: 15K (only relevant files)
- Working buffer: 30K
- Response: 30K
- CHECKPOINT at 40% (not 50%!)
```

### Context Cleanup

After each task:
1. Clear file contents from context
2. Keep only: structure, types, conventions
3. Summarize completed work (1 line)

---

## 8. EFFICIENT PROMPTS

### Agent Spawn: Before vs After

**Before (wasteful):**
```markdown
## Spawning: backend agent

I need you to create a new UserService class. This class should
be located in src/services/userService.ts. The service needs to
implement CRUD operations for users. Please follow the existing
patterns in the codebase. The service should use dependency 
injection for the repository. Make sure to handle all errors
properly and add appropriate TypeScript types.

Here is the full content of the existing OrderService for reference:
[500 lines of code]

And here is the ProductService:
[400 lines of code]

And the repository interface:
[200 lines of code]
```
(~1,200 tokens input)

**After (efficient):**
```markdown
## Spawning: backend

**Task:** Create UserService (CRUD)
**File:** src/services/userService.ts
**Pattern:** Match OrderService (see learnings.md)
**Inject:** UserRepository
```
(~50 tokens input)

---

## 9. INCREMENTAL WORK

### Don't: Load Everything Upfront

```
Read all 50 source files → Plan → Execute
(Wastes tokens on files you won't modify)
```

### Do: Load as Needed

```
Read structure only → Plan → 
  Task 1: Read only task1 files → Execute
  Task 2: Read only task2 files → Execute
  ...
```

---

## 10. IMPLEMENTATION CHECKLIST

Before EVERY operation:

```
□ Am I reading the minimum necessary?
□ Is this info already cached in learnings.md?
□ Can I use Haiku instead of Sonnet?
□ Can I batch this with related work?
□ Will my output be concise?
□ Am I re-validating unnecessarily?
□ Am I at 40% context? (checkpoint time)
```

---

## Expected Savings

| Before Optimization | After Optimization |
|---------------------|-------------------|
| Read all files | Read only needed |
| Always Sonnet | Haiku when possible |
| Re-read every task | Cache and reuse |
| One file per task | Batch related |
| Verbose output | Concise output |
| Full validation | Targeted validation |
| **$10-15/project** | **$2.50-5/project** |

**Total Savings: 60-80%**
