---
name: type-hardening
description: Incrementally improve type safety by replacing string literals with enums, narrowing `any` types, and using shared types. Works in small verified batches. Preserves functionality while improving code quality.
---

# Type Hardening Skill

## Purpose

Gradually improve type safety by:
- Replacing magic strings with enums/constants
- Narrowing `any`/`unknown` to specific types
- Using shared types instead of inline definitions
- Adding type imports where missing

## When to Use

- Code review finds string literals that should be enums
- `any` types that can be narrowed
- Inline types duplicating shared definitions
- Post-refactoring type cleanup
- Technical debt reduction sprints
- Triggered by `/harden-types` command or `/refactor --strategy=types`

## Core Principles

1. **Check Existing First**: Always search for existing types before creating new ones
2. **Small Batches**: 1-3 related changes at a time
3. **Verify Immediately**: Type check after every change
4. **No Logic Changes**: Purely structural/type improvements
5. **Commit Often**: Atomic commits per successful batch
6. **New Types Allowed**: Create new types when genuinely needed for clean code
7. **No `unknown` Cheating**: Replacing `any` with `unknown` is NOT an improvement - narrow to a SPECIFIC type or leave it (with a TODO comment if needed)

## Instructions

### Step 1: Discover Existing Types

Before ANY changes, locate existing type definitions:

```bash
# Find Prisma enums (common source of types)
grep -E "^enum " backend/prisma/schema.prisma 2>/dev/null || true

# Find shared types
find . -path ./node_modules -prune -o -name "*.types.ts" -print 2>/dev/null
find . -path ./node_modules -prune -o -name "types.ts" -print 2>/dev/null

# Find constants files
find . -path ./node_modules -prune -o -name "*.constants.ts" -print 2>/dev/null

# Common locations to check:
# - shared/types/
# - src/types/
# - backend/src/types/
# - backend/src/generated/prisma/ (Prisma enums)
```

**Record findings** before proceeding.

### Step 2: Analyze Target File

Read the target file and identify:

```markdown
### Type Hardening Opportunities

1. **String Literals** → Should use enum/constant
   - Line 45: `'admin'` → `UserRole.admin`
   - Line 89: `'pending'` → `JobStatus.PENDING`

2. **Any Types** → Should be narrowed to SPECIFIC types
   - Line 23: `any` → `UserWithRole` ✅
   - Line 67: `any` → `ApiResponse<T>` ✅
   - ❌ WRONG: `any` → `unknown` (this is cheating, not fixing)

3. **Inline Types** → Should use shared
   - Line 102: `{ id: string; name: string }` → `UserBasic`

4. **Missing Imports** → Need to add
   - `UserRole` from `@prisma/client` or generated types
```

### Step 3: Prioritize Changes

Work in this order for safest progression:

1. **Prisma Enums First** (most reliable)
   ```typescript
   // ❌ BEFORE
   if (user.role === 'admin')

   // ✅ AFTER
   import { UserRole } from '../generated/prisma/index.js';
   if (user.role === UserRole.admin)
   ```

2. **Shared Types Second** (well-established)
   ```typescript
   // ❌ BEFORE
   type NotificationType = 'info' | 'success' | 'warning' | 'error';

   // ✅ AFTER
   import type { NotificationType } from '@shared/types/notification';
   ```

3. **Constants Third** (project-specific)
   ```typescript
   // ❌ BEFORE
   const provider = 'openai';

   // ✅ AFTER
   import { AI_PROVIDERS } from '../types/ai.constants';
   const provider = AI_PROVIDERS.OPENAI;
   ```

4. **New Types Last** (when genuinely needed)
   ```typescript
   // Only create new types when:
   // - No existing type serves the purpose
   // - The type will be used in multiple places
   // - It improves code clarity significantly
   ```

### Step 4: Apply Changes (Batch of 1-3)

```bash
# Edit the file with precise changes
# Use Edit tool for exact string replacement
```

**Example transformation:**

```typescript
// Before (lines 44-48)
async function promoteUser(userId: string): Promise<void> {
  const user = await userRepo.findById(userId);
  if (user.role === 'user') {
    await userRepo.update(userId, { role: 'admin' });
  }
}

// After
import { UserRole } from '../generated/prisma/index.js';

async function promoteUser(userId: string): Promise<void> {
  const user = await userRepo.findById(userId);
  if (user.role === UserRole.user) {
    await userRepo.update(userId, { role: UserRole.admin });
  }
}
```

### Step 5: Verify Immediately

```bash
# Backend files
cd backend && npx tsc --noEmit

# Frontend files
npx tsc --noEmit

# If using ESLint
npx eslint <modified-file>
```

**If verification fails:**
1. ❌ DO NOT proceed to next batch
2. Analyze the error
3. Fix or revert the change
4. Re-verify before continuing

### Step 6: Commit Atomic Change

```bash
git add <modified-file>
git commit -m "refactor: harden types in <filename>

- Replace string literals with <EnumName>
- Narrow any to <TypeName>
- No behavior change

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 7: Iterate or Complete

**Continue if:**
- More hardening opportunities exist
- User requested multiple files
- Within iteration limit

**Stop if:**
- File is clean (no more opportunities)
- Verification failed (fix first)
- User requested stop
- Iteration limit reached

## Output Format

### Progress Report

```markdown
## Type Hardening Report: `backend/src/services/auth.service.ts`

### Changes Applied
| Line | Before | After | Status |
|------|--------|-------|--------|
| 45 | `'admin'` | `UserRole.admin` | ✅ |
| 89 | `'user'` | `UserRole.user` | ✅ |
| 123 | `any` | `AuthPayload` | ✅ |

### Verification
- TypeScript: ✅ 0 errors
- Lint: ✅ passed

### Remaining Opportunities
- Line 156: `'pending'` could use `JobStatus.PENDING`
- Line 201: `unknown` could narrow to `TokenPayload`

### Next Action
Continue? (y/n/skip to file X)
```

## Integration Points

### With Refactor Agent

Referenced as **Pattern 6** in `/refactor`:

```markdown
### Pattern 6: Type Hardening
**When**: String literals, `any` types, inline types matching shared
**How**: Use `type-hardening` skill
**Reference**: `.claude/skills/quality/type-hardening/SKILL.md`
```

### With Quality Gate

Can be part of quality checks:

```markdown
### Optional: Type Strictness Check
Use `type-hardening` skill in analysis-only mode to identify
opportunities without making changes.
```

### With Gemini Delegation

Safe for delegation with guardrails:

```markdown
## Gemini Handoff: Type Hardening
Scope: [specific files]
Task: Replace string literals with existing enums
Verification: tsc --noEmit must pass
```

## Common Type Sources

| Source | Location | Example |
|--------|----------|---------|
| Prisma Enums | `backend/src/generated/prisma/` | `UserRole`, `JobStatus` |
| Shared Types | `shared/types/` | `NotificationType`, `ApiResponse` |
| Domain Types | `src/types/` | `UserWithRole`, `SceneData` |
| Constants | `*/constants.ts` | `AI_PROVIDERS`, `CACHE_TTL` |

## Error Recovery

### Import Resolution Failed

```bash
# Check if type is exported
grep "export.*TypeName" shared/types/

# Check tsconfig paths
cat tsconfig.json | grep -A5 "paths"
```

### Type Mismatch After Change

```bash
# Revert the change
git checkout -- <file>

# Analyze why it failed
# - Was the enum value different? (admin vs ADMIN)
# - Was the type path wrong?
# - Was there a missing export?
```

## Best Practices

1. **Never guess** - Always verify the type exists before using it
2. **Match casing** - `UserRole.admin` not `UserRole.ADMIN` (check actual enum)
3. **Preserve semantics** - `'admin'` becomes `UserRole.admin`, not `Role.ADMIN`
4. **Import correctly** - Use `import type` for type-only imports
5. **Test critical paths** - Extra verification for auth/security code
