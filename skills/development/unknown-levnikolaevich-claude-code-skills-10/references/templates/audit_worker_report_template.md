<!-- SOURCE-OF-TRUTH: shared/templates/audit_worker_report_template.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Audit Worker Report Template

Markdown evidence envelope for audit workers. Coordinators consume JSON summaries first; this report supports the verdict.

## Path

Write once under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-report/` using a stable name such as `{worker-id}-{slug}.md` or `{worker-id}-{slug}-{domain}.md`.

## Required Shape

```markdown
# {Category Name} Audit Report

<!-- AUDIT-META
worker: ln-62X
category: {Category Name}
domain: {domain_name|global}
scan_path: {scan_path|.}
score: {X.X}
total_issues: {N}
critical: {N}
high: {N}
medium: {N}
low: {N}
status: completed
-->

## Checks

| ID | Check | Status | Details |
|----|-------|--------|---------|
| {check_id} | {name} | {passed|failed|warning|skipped} | {brief evidence} |

## Findings

| Severity | Location | Issue | Principle | Recommendation | Effort |
|----------|----------|-------|-----------|----------------|--------|
| HIGH | path/file.ts:42 | What is wrong | Rule | How to fix | M |
```

## Optional Machine Blocks

Add only when consumed by the worker or coordinator: `FINDINGS-EXTENDED`, `DATA-EXTENDED`, or extra informational score fields. The primary penalty-based `score` remains canonical.

## Writing Rules

- Build the full report before writing; never leave partial reports.
- Sort findings by severity: CRITICAL, HIGH, MEDIUM, LOW.
- Keep recommendations actionable and effort as `S`, `M`, or `L`.
- Also write the JSON summary to the path required by `audit_worker_core_contract.md`.

---
**Version:** 2.0.0
**Last Updated:** 2026-02-15
