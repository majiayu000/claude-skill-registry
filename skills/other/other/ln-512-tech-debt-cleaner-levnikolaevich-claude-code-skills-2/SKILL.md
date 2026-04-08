---
name: ln-512-tech-debt-cleaner
description: "Auto-fixes low-risk tech debt (unused imports, dead code, commented-out code) with >=90% confidence. Use when audit findings need safe automated cleanup."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__audit_workspace, mcp__hex-graph__find_references, mcp__hex-line__outline, mcp__hex-line__read_file, mcp__hex-line__edit_file, mcp__hex-line__bulk_replace, mcp__hex-line__verify, mcp__hex-line__changes
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Tech Debt Cleaner (L3 Worker)

**Type:** L3 Worker

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

- Use after code quality analysis when safe low-risk cleanup can be applied
- **Standalone:** After `ln-620` codebase audit completes (user triggers manually)
- **Scheduled:** As periodic "garbage collection" for codebase hygiene

## Inputs

- **Pipeline mode (ln-510):** findings from ln-511 code quality output (passed via coordinator context)
- **Standalone mode:** `docs/project/codebase_audit.md` (ln-620 output)

**MANDATORY READ:** Load `shared/references/mcp_tool_preferences.md` — ALWAYS use hex-line MCP for code files when available. No fallback to standard Read/Edit unless hex-line is down.

**MANDATORY READ:** Load `shared/references/mcp_integration_patterns.md`.

Use `hex-line` as the primary path for code files and `hex-graph` as the primary path for dead-code reference checks. Built-in Read/Edit/Grep are fallback only when the relevant MCP is unavailable.

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

   **Hex-line acceleration (if available):** IF hex-line MCP server is available:
   - Use `outline(path)` and discovery-first `read_file()` before manual cleanup edits. Re-read with `edit_ready=true, verbosity="full"` only when you need revision/checksums for `edit_file`.
   - **Batch cleanup:** When fixing >3 files with same pattern (e.g., unused import removal), use `bulk_replace(dry_run=true)` to preview, then `bulk_replace()` to apply.
   - **Verified edits:** After each fix, `verify(path, checksums)` to confirm no stale state.
   - **Semantic dead-code check:** Use `find_references()` before deleting exports, wrappers, aliases, or shims.
   - Fall back to per-file Edit or Grep only if the relevant MCP is unavailable.
4) **Apply fixes with per-fix keep/discard (autoresearch pattern):**
   **MANDATORY READ:** Load `shared/references/ci_tool_detection.md` for discovery hierarchy. Detect lint + typecheck commands once (reuse for all fixes).

   Group verified fixes by file. For each file (process files independently):
   - Sort fixes within file by line number descending (bottom-up prevents line shift)
   - Apply ALL fixes for this file using Edit tool
   - Run lint/typecheck on the modified file
   - **IF passes** → `git add {file}` (status: **keep**)
   - **IF fails** → `git checkout -- {file}` (status: **discard**), log discarded fixes
   - Track per fix: file, lines removed, category, finding ID, status (keep/discard)

   If no lint/type commands detected: apply all fixes, skip per-file verification with warning, `git add` all modified files.

5) **Create commit (kept fixes only):**
   - All kept files already staged via `git add` in step 4
   - If zero files kept (all discarded): skip commit, report all failures
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
verdict: CLEANED | NOTHING_TO_CLEAN | ALL_DISCARDED
stats:
  total_findings: {from audit}
  auto_fixable: {filtered count}
  kept: {files that passed lint/typecheck}
  discarded: {files that failed lint/typecheck}
  skipped: {confidence <90 or stale}
fixes:
  - file: "src/utils/helpers.ts"
    line: 45
    category: "unused_function"
    removed: "formatDate()"
    finding_id: "MNT-DC-003"
    status: "keep"
  - file: "src/api/v1/auth.ts"
    line: 12
    category: "deprecated_alias"
    removed: "export { newAuth as oldAuth }"
    finding_id: "MNT-DC-007"
    status: "discard"
    discard_reason: "typecheck failed: Type error in auth.ts:15"
commit_sha: "abc1234" | null
```

## Critical Rules

- **Safety first:** Never fix if confidence <90%. When in doubt, skip.
- **Bottom-up editing:** Always apply fixes from bottom to top of file to avoid line number shifts.
- **Per-file keep/discard:** If linter/type-checker fails for a file, revert only that file (`git checkout -- {file}`), keep other successful files.
- **No business logic:** Never modify function bodies, conditionals, or control flow.
- **Explicit staging:** Stage files by name, never `git add .` or `git add -A`.
- **Idempotent:** Running twice produces no changes if audit report unchanged.
- **Git-aware:** Only operate on tracked files. Skip untracked or ignored files.
- **Exclusions:** Skip generated code, vendor directories, minified files, test fixtures.

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/quality_summary_contract.md`, `shared/references/quality_worker_runtime_contract.md`

Runtime profile:
- family: `quality-worker`
- worker: `ln-512`
- summary kind: `quality-worker`
- payload fields used by coordinators: `worker`, `status`, `verdict`, `issues`, `warnings`, `artifact_path`

Invocation rules:
- standalone: omit `runId` and `summaryArtifactPath`
- managed: pass both `runId` and exact `summaryArtifactPath`
- always write the validated summary before terminal outcome

## Definition of Done

- [ ] Audit report loaded and parsed
- [ ] Findings filtered to auto-fixable categories
- [ ] Each finding verified with confidence >=90%
- [ ] Fixes applied bottom-up per file
- [ ] Build integrity verified (lint + type check) or skipped with warning
- [ ] Single commit created with structured message (or all reverted on build failure)
- [ ] Audit report updated with "Last Automated Cleanup" section
- [ ] Output YAML returned to caller

## Reference Files

- **Clean code checklist:** `shared/references/clean_code_checklist.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`
- **Audit report template:** `shared/templates/codebase_audit_template.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-15
