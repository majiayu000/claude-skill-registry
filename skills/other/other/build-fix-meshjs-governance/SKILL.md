---
name: build-fix
updated: 2026-02-20
description: Run the build and intelligently fix errors with guardrails. Stops if fixes introduce more errors or the same error persists after 3 attempts.
disable-model-invocation: true
allowed-tools: Bash, Read, Edit, Grep, Glob, TodoWrite
---

# Build Fix

Run the project build, parse errors, and fix them incrementally with smart guardrails.

## Instructions

### Step 1: Detect Build Command

Determine the build command from the project:
- `package.json` with `build` script → `npm run build`
- `Cargo.toml` → `cargo build`
- `go.mod` → `go build ./...`
- `pyproject.toml` / `setup.py` → `python -m build` or `pip install -e .`
- `Makefile` with `build` target → `make build`

```bash
<build-command> 2>&1
```

If build succeeds, report success and exit. Otherwise continue.

### Step 2: Parse and Group Errors

Parse errors from build output. Group by file and sort by dependency order:
1. Type/interface definition files first — fixing these often resolves downstream errors
2. Utility/library files second
3. Core logic files third
4. UI/component files fourth
5. Entry point/page files last

Common error patterns:
- Type mismatches and missing properties
- Missing imports or modules
- Null/undefined access
- Syntax errors

### Step 3: Create Todo List

Use TodoWrite to track each error group (by file):

```
- Fix 3 type errors in src/types/models.ts
- Fix 1 missing property in src/store/slice.ts
- Fix 2 import errors in src/pages/index.tsx
```

### Step 4: Fix Loop (with guardrails)

For each error, follow this cycle:

1. **Read context**: Read 10-20 lines around the error (not the whole file)
2. **Diagnose**: Identify root cause — type mismatch, missing import, null check, etc.
3. **Minimal fix**: Apply the smallest edit that resolves the error. Do NOT refactor surrounding code.
4. **Mark todo complete**

#### Guardrails — STOP if any of these trigger:

| Guardrail | Condition | Action |
|-----------|-----------|--------|
| **Error loop** | Same error in same file after 3 fix attempts | STOP. Report the error and suggest manual review. |
| **Error explosion** | Re-build shows MORE errors than before | REVERT last edit. Report what happened. |
| **Architectural change needed** | Fix requires changing interfaces used by 5+ files | STOP. Report as architectural issue needing manual decision. |
| **Missing dependency** | Error requires installing a new package | STOP. Report the missing package, do not auto-install. |
| **20 error limit** | More than 20 individual errors | Fix the first 20, then re-build to see if downstream errors resolve. |

### Step 5: Re-build

After fixing all parsed errors (or hitting a guardrail), re-run the build.

- If clean: report success with summary
- If new errors: repeat from Step 2 (max 3 full cycles)
- If same errors persist: stop and report

### Step 6: Report

```
BUILD FIX REPORT
═══════════════════════════
Result:     [SUCCESS / PARTIAL / BLOCKED]
Errors fixed: X
Files modified: Y
Build cycles: Z
═══════════════════════════

Fixed:
  - src/types/models.ts:42 — Added missing property 'name'
  - src/components/Foo.tsx:18 — Added null check for optional data

Remaining (if any):
  - src/store/slice.ts:100 — Architectural: interface change affects 8 files
  - src/lib/bar.ts:5 — Missing dependency: some-package

Warnings (pre-existing):
  - List any known warnings that existed before
```

## Fix Patterns

### Missing Null Check
```typescript
// Before
const value = data.property;
// After
const value = data?.property;
```

### Type Mismatch
```
Check if the type definition needs updating, not the usage.
Prefer widening the type to adding type casts.
```

### Missing Import
```
Use the project's path alias convention (e.g., @/ for src/).
```

## Notes

- Always fix errors in dependency order (types → utils → core → components → pages)
- If stuck on a complex type error, check if related type definitions need updating first
- Never use `@ts-ignore`, `as any`, `# type: ignore`, or similar suppressions as fixes
- After significant changes, consider running the linter as well
