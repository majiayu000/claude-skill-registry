---
name: build-fix
description: Incrementally fix build, TypeScript, and lint errors one at a time with minimal, safe changes. Detects the error type, fixes the root cause, re-runs the build to verify, and repeats until clean.
allowed-tools: Read, Edit, Bash, Grep, Glob
---

# Build Fix

Fix build, typecheck, and lint errors incrementally. One error at a time, minimal changes.

## Step 1: Detect and Run

```bash
# TypeScript errors
pnpm typecheck 2>&1

# Lint errors
pnpm lint 2>&1

# Full check (typecheck + lint + tests)
pnpm check 2>&1

# Build only
pnpm build 2>&1
```

Capture full output. Count total errors for progress tracking.

## Step 2: Group and Prioritize

Group errors by type:
1. **Import errors** — fix first (missing `.js` extensions, wrong paths)
2. **Type errors** — fix second (incorrect types, missing types)
3. **Lint errors** — fix third (style, pattern violations)
4. **Test failures** — fix last (logic errors)

Sort by file — fix all errors in a file before moving to the next.

## Step 3: Fix Loop (one error at a time)

For each error:
1. **Read the file** — understand context around the error (±10 lines)
2. **Diagnose root cause** — don't just suppress, fix the underlying issue
3. **Fix minimally** — smallest change that resolves the error
4. **Re-run** — verify the specific error is gone
5. **Check no new errors** — fix must not introduce new issues
6. **Move to next**

## Common corbat-coco Errors & Fixes

### Missing `.js` extension in imports
```typescript
// ❌ Error: Cannot find module './foo'
import { foo } from "./foo";

// ✅ Fix
import { foo } from "./foo.js";
```

### CommonJS usage
```typescript
// ❌ Error: require is not defined / CommonJS not allowed
const fs = require("fs");
const __dirname = ...;

// ✅ Fix
const fs = await import("node:fs/promises");
import { fileURLToPath } from "node:url";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
```

### Explicit `any` type
```typescript
// ❌ oxlint: no-explicit-any
const data: any = result;

// ✅ Fix — use proper type or unknown
const data: unknown = result;
// Then narrow with type guard or Zod parse
```

### Unhandled promise (floating promise)
```typescript
// ❌ TypeScript: Promise returned from call is ignored
doAsyncWork();

// ✅ Fix
await doAsyncWork();
// or if fire-and-forget is intentional:
void doAsyncWork();
```

### `noUncheckedIndexedAccess` violation
```typescript
// ❌ Type 'string | undefined' is not assignable to 'string'
const first = array[0];
const value = first.toUpperCase(); // Error: first might be undefined

// ✅ Fix
const first = array[0];
if (first !== undefined) {
  const value = first.toUpperCase();
}
// or
const value = array[0]?.toUpperCase() ?? "";
```

### Unused variables
```typescript
// ❌ noUnusedLocals: 'foo' is declared but never read
const foo = bar();

// ✅ Fix — remove if unused, or prefix with _ if intentionally unused
const _foo = bar(); // or delete entirely
```

## Guardrails — STOP and Ask User If:

- A fix introduces **more errors than it resolves**
- The **same error persists after 3 attempts** (likely architectural issue)
- The fix requires **significant refactoring** (not a build fix)
- Missing **dependency** requires `pnpm add` (ask user to confirm)

## Step 4: Verify Clean

```bash
pnpm check
```

Must show zero errors for typecheck, lint, and tests.

## Step 5: Summary Report

```markdown
## Build Fix Summary

### Fixed
- `src/path/file.ts:L10` — Added .js extension to import
- `src/path/other.ts:L42` — Fixed any type to explicit interface

### Remaining
- [none] or [list with explanation]

### Next Steps
- [suggested follow-up if any]
```

## Usage

```
/build-fix
/build-fix typecheck only
/build-fix src/tools/
```
