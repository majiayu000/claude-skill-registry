---
version: 1.1.0
name: dev-verify
description: >
  Post-change verification for the project. Auto-detects backend (.NET) and frontend
  (Angular/TypeScript) from project files. Runs both in mixed projects. Filter with
  "dotnet" or "angular" to target one stack. Reports issues and offers to fix them
  inline. Use when the user says "verify", "check the code", "run checks",
  "verify changes", or invokes /dev-verify.
disable-model-invocation: true
user-invocable: true
argument-hint: "[dotnet | angular | --quick | --full | --fix]"
---

# Verification — Unified Entry Point

Routes to the appropriate backend and/or frontend verification skill,
then presents issues with an inline menu to fix them.

## Step 1: Detect Stacks

1. **Explicit filter** — if the user passed `dotnet` or `angular`, use only that stack
2. **Project detection**:
   - .NET: any `*.csproj`, `*.sln` file exists
   - Angular: `angular.json` or `package.json` with `@angular/core` exists
3. **workflow.json fallback**:
   - `type: "api"` or `type: "library"` → .NET
   - `type: "frontend"` → Angular
   - `type: "docs"` → skip (no verification needed)

If both detected and no filter, run both.

## Step 2: Run Checks

Run all verification phases from the appropriate sub-skill(s) but **collect results
without stopping** — don't fix anything yet, just gather the full picture.

### .NET (if applicable)

Read `.claude/skills/dev-verification-backend/SKILL.md` and run all phases.
Collect pass/fail status and details for each.

### Angular (if applicable)

Read `.claude/skills/dev-verification-frontend/SKILL.md` and run all phases.
Collect pass/fail status and details for each.

## Step 3: Present Report with Fix Menu

After all checks complete, present the combined report with a numbered issue list:

```
VERIFICATION REPORT
═══════════════════

  .NET
  ────
  Build:       ✓ pass
  Analyzers:   ✗ 3 warnings
  Format:      ✗ 2 files
  Tests:       ✗ 1 failing
  Security:    ✓ pass

  Angular
  ───────
  Build:       ✓ pass
  TypeScript:  ✓ pass
  Lint:        ✗ 5 issues
  Tests:       ✓ pass (92% coverage)
  Security:    ✓ pass

  Issues
  ──────
  1. [dotnet] Analyzer warnings: CS8602 (null ref) in ProfileService.cs:42, EventHandler.cs:18
  2. [dotnet] Format violations in ProfileEndpoints.cs, WaitlistAggregate.cs
  3. [dotnet] Test failure: CreateProfile_WhenDuplicate_ShouldReturnConflict
  4. [angular] Lint: 5 ESLint issues in profile.component.ts, auth.service.ts

  ─────────────────────────────────
  Fix?  [a]ll  [1-4] pick  [s]kip
```

Wait for user input. Do NOT proceed without a response.

## Step 4: Fix Selected Issues

Based on user selection:

- **`a` (all)** — Fix every issue in order
- **`1-4` (pick)** — Fix only the selected issue(s). User can specify multiple: `1,3` or `1 3`
- **`s` (skip)** — Done, just report

### Fix Strategies

For each issue type, apply the appropriate fix:

| Issue | Fix Strategy |
|-------|-------------|
| **Build failure** | Read the error, fix the code |
| **Analyzer warnings** | Fix the flagged code (null checks, async patterns, etc.) |
| **Format violations** | Run `dotnet format` or `prettier`/`eslint --fix` |
| **Test failures** | Read the test, read the code under test, fix the root cause |
| **Lint issues** | Run `ng lint --fix` or fix manually if auto-fix doesn't resolve |
| **Security issues** | Present the issue and proposed fix, ask before applying (security changes need review) |
| **Deprecated packages** | Show alternatives, ask before updating |

### After Fixing

After applying fixes, **re-run only the phases that had issues** to verify the fixes worked.
Present an updated report:

```
  Re-check
  ────────
  1. [dotnet] Analyzers:  ✓ fixed (3 warnings resolved)
  2. [dotnet] Format:     ✓ fixed (dotnet format applied)
  3. [dotnet] Tests:      ✗ still failing — see details below
  4. [angular] Lint:      ✓ fixed (eslint --fix applied)

  Remaining issues
  ────────────────
  3. [dotnet] Test: CreateProfile_WhenDuplicate_ShouldReturnConflict
     Expected: Conflict (409)
     Actual:   BadRequest (400)

  Fix?  [3] pick  [s]kip
```

Repeat the fix→verify cycle until all issues are resolved or the user skips.

## Step 5: Final Status

```
  Result: READY for PR  (or: NOT READY — 1 issue remaining)
```

## Flags

| Flag | Behavior |
|------|----------|
| `dotnet` | Run .NET checks only |
| `angular` | Run Angular checks only |
| `--quick` | Build + type check only (fewer issues to fix) |
| `--full` | All verification phases (default) |
| `--fix` | Skip the menu — auto-fix all issues immediately |
