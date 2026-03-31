---
name: ai-slop-cleaner
description: Post-implementation cleanup that removes AI-generated bloat while preserving functionality. Runs pass-by-pass with test verification after each pass. Activate after kraken/spark complete a feature, or when a codebase needs hygiene work.
---

# AI Slop Cleaner

AI code generation produces working code. It also produces unnecessary code alongside it. This skill removes the unnecessary parts while keeping everything that matters.

## What Is "AI Slop"?

AI slop is code that:
- Works, but shouldn't exist
- Adds complexity without adding value
- Was clearly generated to pad a response rather than solve a problem
- Suggests the author wasn't thinking, just generating

Common slop categories and their signals:

| Category | Signal |
|----------|--------|
| Dead imports | Imported but never referenced in the file |
| Unused variables | Declared, never read |
| Commented-out code | Blocks of `// old code` or `/* removed */` |
| Debug remnants | `console.log`, `print()`, `debugger`, `fmt.Println` |
| Obvious comments | `// increment counter` above `count++` |
| Redundant JSDoc | `@param name - the name` above `name: string` |
| Premature abstractions | A factory that creates exactly one thing |
| One-use helpers | Private function called exactly once, trivially inlinable |
| Overly generic types | `<T extends object>` when `T` is always `User` |
| Over-parameterized | `fn(a, b, c, d, e)` where 4 params never vary |
| Unreachable branches | `if (false)` or `if (isLoggedIn && !isLoggedIn)` |
| Speculative features | Code paths for requirements that don't exist |
| Copy-paste duplication | Two blocks identical except one variable name |
| Placeholder remnants | `TODO: implement`, lorem ipsum, example data in prod |

## The Prime Directive

**Tests are sacred. Never clean test files.**

Tests exist to protect behavior. Any cleanup that breaks a test reveals that the "slop" was actually load-bearing. That is good information. The test wins.

## Regression-Safe Workflow (Non-Negotiable)

```
BEFORE ANYTHING: Run full test suite → all tests must pass (baseline)

FOR EACH PASS:
  1. Identify targets for this pass category
  2. Apply cleanup
  3. Run tests
  4. If tests pass: keep cleanup, continue
  5. If tests fail: git checkout -- . (revert), skip this pass category
  6. Log what was reverted and why

AFTER ALL PASSES: Run full test suite → confirm all tests still pass
Report: lines removed, files touched, passes skipped, reason for each skip
```

Never batch multiple pass categories together. If combined changes break a test, you cannot know which change caused it.

## The 7 Cleaning Passes

### Pass 1: Dead Imports and Unused Variables

**Risk: Very Low**

What to remove:
- Import statements where the imported name never appears in the file body
- Variables declared with `let`/`const`/`var` that are never read after assignment
- Function parameters that are never referenced inside the function body (TypeScript: prefix with `_`)

Before:
```typescript
import { useState, useEffect, useCallback, useMemo } from 'react'
import { formatDate } from '@/lib/utils'
import { ApiClient } from '@/lib/api'

export function UserCard({ user }) {
  const [count, setCount] = useState(0)
  const formatted = formatDate(user.createdAt)

  return <div>{user.name}</div>
}
```

After:
```typescript
import { useState } from 'react'
import { formatDate } from '@/lib/utils'

export function UserCard({ user }) {
  const [count, setCount] = useState(0)
  const formatted = formatDate(user.createdAt)

  return <div>{user.name}</div>
}
```

Note: `count`, `setCount`, and `formatted` are still present because they may be used elsewhere in a larger component. Pass 1 only removes imports.

### Pass 2: Commented-Out Code and Debug Statements

**Risk: Very Low**

What to remove:
- Any block of commented-out code that is not an active TODO or architectural note
- `console.log`, `console.debug`, `console.warn` (unless it is a legitimate error logger)
- `debugger` statements
- `print()` in Python when not serving as actual program output
- `fmt.Println` in Go debug instrumentation

Before:
```typescript
async function processOrder(orderId: string) {
  console.log('processing order', orderId)
  const order = await db.orders.findById(orderId)
  // const cached = await cache.get(orderId)
  // if (cached) return cached
  console.log('order fetched:', order)

  const result = await payments.charge(order)
  // TODO: add retry logic here
  // console.log('charge result', result)

  return result
}
```

After:
```typescript
async function processOrder(orderId: string) {
  const order = await db.orders.findById(orderId)

  const result = await payments.charge(order)
  // TODO: add retry logic here

  return result
}
```

Rule: `// TODO:` comments are preserved. They are documentation of known gaps, not slop.

### Pass 3: Obvious Comments and Redundant Documentation

**Risk: Low**

What to remove:
- Comments that restate the code in plain English without adding context
- JSDoc `@param` blocks that just repeat the parameter name and type (TypeScript already says this)
- Section dividers that add no structure (`// ===== COMPONENT =====`)
- End-of-block comments (`} // end if`, `} // end for`)

Before:
```typescript
/**
 * Gets a user by ID.
 * @param id - the user ID
 * @param db - the database instance
 * @returns the user object
 */
async function getUserById(id: string, db: Database): Promise<User> {
  // Query the database for the user
  const user = await db.users.findById(id)

  // Return the user
  return user
} // end getUserById
```

After:
```typescript
async function getUserById(id: string, db: Database): Promise<User> {
  return db.users.findById(id)
}
```

Keep comments that explain WHY (business rules, performance choices, known gotchas). Remove comments that explain WHAT (the code already says what).

### Pass 4: Dead Code (Unreachable Branches)

**Risk: Medium — Run tests immediately after**

What to remove:
- Conditions that are always true or always false
- Code after unconditional `return`, `throw`, or `break`
- Else branches of conditions that always throw in the if block

Before:
```typescript
function getStatus(user: User): string {
  if (user.role === 'admin' || user.role === 'admin') {
    return 'ADMIN'
  }

  if (user.isActive) {
    return 'ACTIVE'
  } else {
    return 'INACTIVE'
  }

  // This never runs
  return 'UNKNOWN'
}
```

After:
```typescript
function getStatus(user: User): string {
  if (user.role === 'admin') {
    return 'ADMIN'
  }

  return user.isActive ? 'ACTIVE' : 'INACTIVE'
}
```

Do not remove branches that look unreachable but depend on runtime data you cannot verify statically. When uncertain, leave it.

### Pass 5: Premature Abstractions (Inline One-Use Helpers)

**Risk: Medium — Run tests immediately after**

What to inline:
- Private/internal functions called exactly once
- Wrapper functions that add no logic (just forward all arguments)
- Intermediate variables assigned once and used once on the next line

Before:
```typescript
function formatUserDisplayName(user: User): string {
  return `${user.firstName} ${user.lastName}`.trim()
}

function renderUserCard(user: User) {
  const displayName = formatUserDisplayName(user)
  return `<div class="card">${displayName}</div>`
}
```

After (if `formatUserDisplayName` is only called from `renderUserCard`):
```typescript
function renderUserCard(user: User) {
  const displayName = `${user.firstName} ${user.lastName}`.trim()
  return `<div class="card">${displayName}</div>`
}
```

Do NOT inline if:
- The function is exported (public API)
- The function is called from more than one place
- The function name serves as meaningful documentation of intent
- The function contains error handling that would add visual noise when inlined

### Pass 6: Duplication Consolidation

**Risk: Medium-High — Run tests immediately after each consolidation**

What to consolidate:
- Two or more blocks with identical structure and only one variable difference
- Repeated conditional checks that could be extracted to a guard function
- Multiple switch/if-else blocks with the same cases in different files

Before:
```typescript
// In UserService
async function getActiveUsers() {
  const users = await db.query(
    'SELECT * FROM users WHERE status = $1 AND deleted_at IS NULL',
    ['active']
  )
  return users.rows
}

// In AdminService (same file or different file)
async function getActiveAdmins() {
  const admins = await db.query(
    'SELECT * FROM users WHERE status = $1 AND deleted_at IS NULL AND role = $2',
    ['active', 'admin']
  )
  return admins.rows
}
```

After:
```typescript
async function getActiveUsers(role?: string) {
  const params: unknown[] = ['active']
  let sql = 'SELECT * FROM users WHERE status = $1 AND deleted_at IS NULL'

  if (role) {
    sql += ' AND role = $2'
    params.push(role)
  }

  const result = await db.query(sql, params)
  return result.rows
}
```

Be careful: consolidation that requires complex parameterization may make code harder to understand. If the consolidated version is more complex than the two originals, leave them separate.

### Pass 7: Over-Engineering Simplification

**Risk: High — High scrutiny, run tests after every individual change**

What to simplify:
- Factory pattern used to create exactly one concrete type
- Strategy pattern with exactly one strategy
- Abstract base class with exactly one implementation
- Generic type parameter constrained so tightly it could be a concrete type

Before:
```typescript
interface DataProcessor<T extends BaseData> {
  process(data: T): ProcessedData<T>
  validate(data: T): ValidationResult
}

class UserDataProcessorFactory {
  create(): DataProcessor<UserData> {
    return new UserDataProcessor()
  }
}

class UserDataProcessor implements DataProcessor<UserData> {
  process(data: UserData): ProcessedData<UserData> {
    return { ...data, processed: true }
  }

  validate(data: UserData): ValidationResult {
    return { valid: !!data.id }
  }
}
```

After (if only UserData ever flows through this):
```typescript
function processUserData(data: UserData) {
  if (!data.id) throw new Error('Invalid user data: missing id')
  return { ...data, processed: true }
}
```

Rule for Pass 7: If you need more than 2 minutes to understand why an abstraction exists, and there is only one concrete case, remove the abstraction. If you find yourself unsure whether it is load-bearing, leave it. Pass 7 is optional.

## What Is Never Cleaned

| Target | Reason |
|--------|--------|
| Test files (`*.test.*`, `*.spec.*`, `__tests__/`) | Tests are sacred |
| Public API signatures | Breaks callers |
| Error handling at system boundaries (API routes, top-level handlers) | Defense-in-depth |
| Comments explaining regulatory/compliance requirements | Legal context |
| Feature flags | May be toggled at runtime |
| Anything marked `// KEEP` or `// intentional` | Explicit author decision |

## .slopignore File

Place at project root to exclude paths:

```
# .slopignore
src/legacy/         # Old code being migrated, don't touch
src/generated/      # Auto-generated, cleaned by generator
vendor/             # Third-party code
```

## Metrics Report

After all passes complete, output:

```
AI Slop Cleaner Report
======================
Files touched:          12
Lines removed:          147
Lines remaining:        1,843
Reduction:              7.4%

Pass results:
  Pass 1 (Dead imports):       DONE — 23 lines removed
  Pass 2 (Debug code):         DONE — 18 lines removed
  Pass 3 (Obvious comments):   DONE — 41 lines removed
  Pass 4 (Dead code):          DONE — 12 lines removed
  Pass 5 (One-use helpers):    DONE — 31 lines removed
  Pass 6 (Duplication):        SKIPPED — test failed after consolidation (UserService)
  Pass 7 (Over-engineering):   DONE — 22 lines removed

Skipped details:
  Pass 6 reverted: UserService query consolidation broke getUsersByStatus test.
  Root cause: test was asserting on the exact SQL string. Left original.

Test status: ALL PASSING (127/127)
```

## Integration with refactor-cleaner Agent

AI slop cleaner runs at the code level (syntactic cleanup). The refactor-cleaner agent runs at the architecture level (structural refactoring). Run this skill first, then refactor-cleaner if structural improvement is needed.

Order:
```
1. ai-slop-cleaner (remove the noise)
2. code-reviewer (verify quality after cleanup)
3. refactor-cleaner (structural improvements if needed)
4. verifier (final gate)
```

## Automatic Trigger

This skill is automatically triggered after:
- kraken agent completes a feature implementation
- spark agent completes a fix
- Any agent produces more than 200 new lines of code

The trigger runs Pass 1 and Pass 2 only by default (very low risk). Passes 3-7 require explicit activation or a `/clean` command.

---

**Remember**: The goal is not minimum lines of code. The goal is maximum clarity per line. If removing something makes the code harder to understand, put it back.
