---
name: ln-512-tech-debt-cleaner
description: "Automated tech debt cleanup worker (L3). Reads codebase audit findings, applies safe auto-fixes for low-risk issues (unused imports, dead code, commented-out code, deprecated aliases). Confidence >=90% only. Creates single commit with summary."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Tech Debt Cleaner (L3 Worker)

Automated cleanup of safe, low-risk tech debt findings from codebase audits.

## Purpose & Scope

- **Consume** audit findings from `docs/project/codebase_audit.md` (ln-620 output) or ln-511 code quality output
- **Filter** to auto-fixable findings with confidence >=90%
- **Apply** safe fixes: remove unused imports, delete dead code, clean commented-out blocks, remove deprecated aliases
- **Never touch** business logic, complex refactoring, or architectural changes
- **Create** single commit with structured summary of all changes
- Invocable from ln-510 quality coordinator pipeline or standalone

## Auto-Fixable Categories

| Category | Source Prefix | Risk | Auto-Fix Action |
|----------|--------------|------|-----------------|
| Unused imports | MNT-DC- | LOW | Delete import line |
| Unused variables | MNT-DC- | LOW | Delete declaration |
| Unused functions (unexported) | MNT-DC- | LOW | Delete function block |
| Commented-out code (>5 lines) | MNT-DC- | LOW | Delete comment block |
| Backward-compat shims (>6 months) | MNT-DC- | MEDIUM | Delete shim + update re-exports |
| Deprecated aliases | MNT-DC- | LOW | Delete alias line |
| Trailing whitespace / empty lines | MNT- | LOW | Trim / collapse |

## NOT Auto-Fixable (skip always)

| Category | Reason |
|----------|--------|
| DRY violations (MNT-DRY-) | Requires architectural decision on where to extract |
| God classes (MNT-GOD-) | Requires domain knowledge for splitting |
| Security issues (SEC-) | Requires context-specific fix |
| Architecture violations (ARCH-*) | Requires design decision |
| Performance issues (PERF-*) | Requires benchmarking |
| Any finding with effort M or L | Too complex for auto-fix |

## When to Use

- **Invoked by ln-510-quality-coordinator** Phase 3 (after ln-511 code quality check)
- **Standalone:** After `ln-620` codebase audit completes (user triggers manually)
- **Scheduled:** As periodic "garbage collection" for codebase hygiene

## Inputs

- **Pipeline mode (ln-510):** findings from ln-511 code quality output (passed via coordinator context)
- **Standalone mode:** `docs/project/codebase_audit.md` (ln-620 output)

## Workflow

1) **Load findings:** Read `docs/project/codebase_audit.md`. Parse findings from Dead Code section (ln-626 results) and Code Quality section (ln-624 results).

2) **Filter to auto-fixable:**
   - Category must be in Auto-Fixable table above
   - Severity must be LOW or MEDIUM (no HIGH/CRITICAL)
   - Effort must be S (small)
   - Skip files in: `node_modules/`, `vendor/`, `dist/`, `build/`, `*.min.*`, generated code, test fixtures

3) **Verify each finding (confidence check):**
   **MANDATORY READ:** `shared/references/clean_code_checklist.md`
   For each candidate fix:
   a) Read the target file at specified location
   b) Confirm the finding still exists (file may have changed since audit)
   c) Confirm removal is safe:
      - For unused imports: grep codebase for usage (must have 0 references)
      - For unused functions: grep for function name (must have 0 call sites)
      - For commented-out code: verify block is code, not documentation
      - For deprecated aliases: verify no consumers remain
   d) Assign confidence score (0-100). Only proceed if confidence >=90

4) **Apply fixes (bottom-up within each file):**
   - Sort fixes by line number descending (bottom-up prevents line shift issues)
   - Apply each fix using Edit tool
   - Track: file, lines removed, category, original finding ID

5) **Verify build integrity:**
   Per `shared/references/ci_tool_detection.md` discovery hierarchy: detect and run lint + typecheck commands.
   - If ANY check fails: revert ALL changes (`git checkout .`), report failure
   - If no lint/type commands detected: skip verification with warning

6) **Create commit:**
   - Stage only modified files (explicit `git add` per file, not `git add .`)
   - Commit message format:
     ```
     chore: automated tech debt cleanup

     Removed {N} auto-fixable findings from codebase audit:
     - {count} unused imports
     - {count} dead functions
     - {count} commented-out code blocks
     - {count} deprecated aliases

     Source: docs/project/codebase_audit.md
     Confidence threshold: >=90%
     ```

7) **Update audit report:**
   - Add "Last Cleanup" section to `docs/project/codebase_audit.md`:
     ```markdown
     ## Last Automated Cleanup
     **Date:** YYYY-MM-DD
     **Findings fixed:** N of M auto-fixable
     **Skipped:** K (confidence <90% or verification failed)
     **Build check:** PASSED / SKIPPED
     ```

## Output Format

```yaml
verdict: CLEANED | NOTHING_TO_CLEAN | BUILD_FAILED
stats:
  total_findings: {from audit}
  auto_fixable: {filtered count}
  applied: {actually fixed}
  skipped: {confidence <90 or stale}
  reverted: {if build failed, all}
fixes:
  - file: "src/utils/helpers.ts"
    line: 45
    category: "unused_function"
    removed: "formatDate()"
    finding_id: "MNT-DC-003"
  - file: "src/api/v1/auth.ts"
    line: 12
    category: "deprecated_alias"
    removed: "export { newAuth as oldAuth }"
    finding_id: "MNT-DC-007"
build_check: PASSED | SKIPPED | FAILED
commit_sha: "abc1234" | null
```

## Critical Rules

- **Safety first:** Never fix if confidence <90%. When in doubt, skip.
- **Bottom-up editing:** Always apply fixes from bottom to top of file to avoid line number shifts.
- **Build verification:** If linter/type-checker fails after fixes, revert ALL changes immediately.
- **No business logic:** Never modify function bodies, conditionals, or control flow.
- **Explicit staging:** Stage files by name, never `git add .` or `git add -A`.
- **Idempotent:** Running twice produces no changes if audit report unchanged.
- **Git-aware:** Only operate on tracked files. Skip untracked or ignored files.
- **Exclusions:** Skip generated code, vendor directories, minified files, test fixtures.

## Definition of Done

- Audit report loaded and parsed
- Findings filtered to auto-fixable categories
- Each finding verified with confidence >=90%
- Fixes applied bottom-up per file
- Build integrity verified (lint + type check) or skipped with warning
- Single commit created with structured message (or all reverted on build failure)
- Audit report updated with "Last Automated Cleanup" section
- Output YAML returned to caller

## Reference Files

- **Clean code checklist:** `shared/references/clean_code_checklist.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`
- **Audit report template:** `shared/templates/codebase_audit_template.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-15
