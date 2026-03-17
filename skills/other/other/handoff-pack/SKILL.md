---
name: handoff-pack
description: Generates structured Handoff Pack prompts for delegating work to Gemini with clear scope, acceptance criteria, and output format requirements.
---

# Handoff Pack Generator

## Purpose

Generate well-structured prompts ("Handoff Packs") for delegating scoped work to Gemini, ensuring clear instructions, verifiable acceptance criteria, and parseable output format.

## When to Use

- Called by `gemini-delegation` agent after user approves delegation
- User wants to manually generate a handoff prompt
- Need to create a fix-up prompt after failed verification

## Handoff Pack Structure

A complete Handoff Pack has these sections:

### 1. Session Context

```markdown
# Gemini Handoff Pack

## Session Context
- **Delegated By**: Claude Cloud Agent
- **Delegation ID**: [YYYYMMDD-HHMMSS-hash]
- **Project**: [repo name]
- **Branch**: [current branch]
```

### 2. Scope Definition

```markdown
## Allowed Scope

**You may ONLY modify these paths:**
```
src/features/user/*.ts
src/features/user/**/*.test.ts
```

**You may NOT:**
- Modify files outside the allowed scope
- Change function signatures or public APIs
- Delete existing functionality
- Add new dependencies
- Modify configuration files
```

### 3. Task Instructions

```markdown
## Task Instructions

**Objective**: [Clear, specific, measurable objective]

**Context**: [Why this work is needed, background info]

**Pattern to Follow**:

```typescript
// === BEFORE ===
export function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// === AFTER ===
/**
 * Calculates the total price of all items.
 * @param items - Array of items with price property
 * @returns Total price as a number
 */
export function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Apply this pattern to:**
- All exported functions in scope
- Skip private/internal functions (no export keyword)
- Preserve existing JSDoc if present (don't duplicate)
```

### 4. Acceptance Criteria

```markdown
## Acceptance Criteria

Before reporting completion, ALL of these must pass:

```bash
# TypeScript compilation (required)
npx tsc --noEmit

# Linting (required)
npm run lint
# OR: pnpm lint
# OR: yarn lint

# Tests (if applicable)
npm test -- --passWithNoTests
# OR: pnpm test
# OR: yarn test
```

**Success means:**
- Zero TypeScript errors
- Zero lint errors (warnings acceptable)
- All tests pass (or none affected)

**If any fail:**
1. Fix the issue
2. Re-run the check
3. Only report when ALL pass
```

### 5. Output Format

```markdown
## Required Output Format

When complete, provide this EXACT format:

```markdown
## Gemini Completion Report

### Delegation ID
[same ID from Session Context]

### Files Modified
- `path/to/file1.ts` - Added JSDoc to 3 functions
- `path/to/file2.ts` - Added JSDoc to 5 functions
- `path/to/file3.ts` - Added JSDoc to 2 functions

### Commands Run
- `npx tsc --noEmit` - ✅ Passed
- `npm run lint` - ✅ Passed
- `npm test` - ✅ Passed (or N/A)

### Diff Summary
```
 src/features/user/service.ts  | 45 +++++++++++++++++++++
 src/features/user/types.ts    | 12 ++++++
 src/features/user/utils.ts    | 18 +++++++++
 3 files changed, 75 insertions(+)
```

### Notes
[Any decisions made, edge cases encountered, or observations]

### Escalations (if any)
[Items that need Cloud review - unclear patterns, security concerns, etc.]
```
```

### 6. Guardrails

```markdown
## Guardrails

⚠️ **STOP and report as Escalation** if you encounter:

1. **Unclear patterns** - Need architectural decision
2. **Business logic changes** - Beyond scope of delegation
3. **Security-sensitive code** - Auth, crypto, validation, secrets
4. **Breaking changes** - Would change public API behavior
5. **Cross-cutting concerns** - Changes ripple outside scope
6. **Dependency changes** - Package.json modifications needed

**How to escalate:**

```markdown
### Escalations
1. **File**: `src/features/user/auth.ts`
   **Issue**: Contains password hashing logic - security sensitive
   **Recommendation**: Skip this file, let Cloud handle

2. **Pattern unclear**: `src/features/user/legacy.ts`
   **Issue**: Mixed export styles, unclear which to document
   **Recommendation**: Clarify pattern before proceeding
```

Do NOT guess on escalation items. Report and skip.
```

## Instructions

### Generating a New Handoff Pack

**Input required:**
- Task description
- Scope (file patterns)
- Triage score (for context)
- Acceptance commands (auto-detected or specified)

**Process:**

1. **Detect project type:**
```bash
# Check for package.json
if [ -f "package.json" ]; then
  PKG_MANAGER="npm"
  [ -f "pnpm-lock.yaml" ] && PKG_MANAGER="pnpm"
  [ -f "yarn.lock" ] && PKG_MANAGER="yarn"
fi
```

2. **Generate delegation ID:**
```bash
DELEGATION_ID="$(date +%Y%m%d-%H%M%S)-$(echo "$TASK" | md5sum | cut -c1-8)"
```

3. **Build scope section** from provided path patterns

4. **Create before/after examples** from existing code in scope

5. **Add appropriate acceptance criteria** based on project type

6. **Include guardrails section** (always)

### Generating a Fix-Up Pack

When verification fails, generate a minimal fix-up pack:

```markdown
# Gemini Fix-Up Pack

## Previous Delegation
- **Original ID**: [original delegation ID]
- **Fix-Up ID**: [new ID]

## Issues to Fix

### Issue 1: [Category]
**File**: `path/to/file.ts`
**Error**: [exact error message]
**Fix**: [specific instruction]

### Issue 2: [Category]
**File**: `path/to/file2.ts`
**Error**: [exact error message]
**Fix**: [specific instruction]

## After Fixes

Re-run verification:
```bash
npx tsc --noEmit
npm run lint
```

## Report Format

```markdown
## Fix-Up Report

### Original Delegation ID
[id]

### Issues Fixed
- Issue 1: ✅ Fixed - [what was done]
- Issue 2: ✅ Fixed - [what was done]

### Verification
- `npx tsc --noEmit` - ✅ Passed
- `npm run lint` - ✅ Passed

### Notes
[Any additional context]
```
```

## Templates

### Template: Documentation Addition

```markdown
# Gemini Handoff Pack

## Session Context
- **Delegated By**: Claude Cloud Agent
- **Delegation ID**: {{DELEGATION_ID}}
- **Project**: {{PROJECT_NAME}}

## Allowed Scope
```
{{SCOPE_PATTERNS}}
```

**You may NOT:**
- Modify files outside scope
- Change any code logic
- Modify function signatures

## Task Instructions

**Objective**: Add JSDoc documentation to all exported functions

**Pattern**:
```typescript
// BEFORE
export function myFunction(param: Type): ReturnType {

// AFTER
/**
 * Brief description of what the function does.
 * @param param - Description of parameter
 * @returns Description of return value
 */
export function myFunction(param: Type): ReturnType {
```

**Rules:**
- Only document exported functions (has `export` keyword)
- Keep descriptions concise (1 line for simple functions)
- Use existing code to infer parameter/return descriptions
- Preserve any existing documentation

## Acceptance Criteria
```bash
npx tsc --noEmit
{{PKG_MANAGER}} run lint
```

## Required Output Format
[Standard completion report format]

## Guardrails
[Standard guardrails]
```

### Template: Rename/Replace

```markdown
# Gemini Handoff Pack

## Session Context
[standard]

## Allowed Scope
```
{{SCOPE_PATTERNS}}
```

## Task Instructions

**Objective**: Rename `{{OLD_NAME}}` to `{{NEW_NAME}}` across all files in scope

**What to rename:**
- Variable declarations
- Function parameters
- Object properties
- Type/interface properties
- Import/export statements
- String literals in specific contexts (specify)

**What NOT to rename:**
- Comments (unless referencing the identifier)
- String literals (unless confirmed as identifiers)
- External API calls

## Acceptance Criteria
```bash
npx tsc --noEmit  # Must pass - catches missed renames
{{PKG_MANAGER}} run lint
{{PKG_MANAGER}} test
```

## Required Output Format
[Standard]

## Guardrails
[Standard]
```

### Template: Type Hardening

```markdown
# Gemini Handoff Pack

## Session Context
- **Delegated By**: Claude Cloud Agent
- **Delegation ID**: {{DELEGATION_ID}}
- **Project**: {{PROJECT_NAME}}
- **Reference Skill**: `.claude/skills/quality/type-hardening/SKILL.md`

## Allowed Scope
```
{{SCOPE_PATTERNS}}
```

**You may ONLY modify files matching these patterns.**

## Task Instructions

**Objective**: Harden types by replacing string literals with enums and narrowing `any` to specific types.

**Priority Order:**
1. Prisma Enums (most reliable)
2. Shared Types (`shared/types/`, `@shared/types`)
3. Constants (`*.constants.ts`)
4. Create new types ONLY when genuinely needed

**Check existing types FIRST:**
```bash
# Prisma enums
grep -E "^enum " backend/prisma/schema.prisma

# Shared types
find shared/types -name "*.ts" -exec grep "export type\|export interface" {} \;

# Constants
find . -name "*.constants.ts" -exec cat {} \;
```

**Pattern - String Literals:**
```typescript
// ❌ BEFORE
if (user.role === 'admin')

// ✅ AFTER
import { UserRole } from '../generated/prisma/index.js';
if (user.role === UserRole.admin)
```

**Pattern - Any Types:**
```typescript
// ❌ BEFORE
const data: any = response.body;

// ✅ AFTER - narrow to SPECIFIC type
const data: UserPayload = response.body;

// ❌ WRONG - unknown is cheating, not fixing
const data: unknown = response.body;  // NOT ALLOWED
```

**Work in small batches (1-3 changes), verify after each.**

## Acceptance Criteria
```bash
# REQUIRED after EACH batch of changes
npx tsc --noEmit

# Before final completion
{{PKG_MANAGER}} run lint
```

**If verification fails:** STOP, report the error, do NOT proceed.

## Required Output Format
```markdown
## Type Hardening Report

### Delegation ID
{{DELEGATION_ID}}

### Changes Applied
| File | Line | Before | After |
|------|------|--------|-------|
| auth.service.ts | 45 | `'admin'` | `UserRole.admin` |
| user.service.ts | 89 | `any` | `UserProfile` |

### Existing Types Used
- `UserRole` from `@prisma/client`
- `UserProfile` from `shared/types/user`

### New Types Created (if any)
- None (or list with justification)

### Verification
- `npx tsc --noEmit` - ✅ Passed
- `npm run lint` - ✅ Passed

### Remaining Opportunities
[List any skipped items with reason]
```

## Guardrails

⚠️ **STOP and escalate** if:
1. No existing type matches - need Cloud to create new type
2. Changing `any` would require business logic changes
3. Type is in security-critical code (auth, crypto)
4. Uncertain about correct enum value casing

⚠️ **NEVER:**
- Replace `any` with `unknown` (that's cheating, not fixing)
- Create types without checking existing first
- Change any business logic
- Proceed after verification failure
```

## Best Practices

1. **Scope narrowly** - Better to under-scope than over-scope
2. **Provide concrete examples** - Always include before/after from actual code
3. **Be explicit about boundaries** - What's allowed, what's forbidden
4. **Make acceptance criteria runnable** - Exact commands, not descriptions
5. **Require structured output** - Parseable completion reports
6. **Include escalation path** - Gemini should know when to stop

## Related Skills

- `gemini-api/caching` - For caching Gemini API calls
- `gemini-api/rate-limiting` - For managing API rate limits

## Related Agents

- `gemini-delegation` - Uses this skill to generate packs
