---
name: ln-611-docs-structure-auditor
description: Documentation structure audit worker (L3). Checks hierarchy & links, SSOT, proactive compression, requirements compliance, actuality (code vs docs), legacy cleanup, stack adaptation. Returns findings with severity, location, and recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Documentation Structure Auditor (L3 Worker)

Specialized worker auditing structural quality of project documentation.

## Purpose & Scope

- **Worker in ln-610 coordinator pipeline** - invoked by ln-610-docs-auditor
- Audit documentation for **structural quality** across 7 categories
- Scan all `.md` files in project, build hierarchy from CLAUDE.md
- Return structured findings to coordinator with severity, location, recommendations
- Calculate compliance score (X/10) for Documentation Structure

## Inputs (from Coordinator)

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md#audit-coordinator--worker-contract` for contextStore structure.

Receives `contextStore` with: `tech_stack`, `project_root`, `output_dir`.

## Workflow

1) **Parse Context:** Extract tech stack, project root, output_dir from contextStore
2) **Scan Docs:** Find all `.md` files in project (CLAUDE.md, README.md, docs/**)
3) **Build Tree:** Construct hierarchy from CLAUDE.md outward links
4) **Audit Categories 1-7:** Run structural checks (see Audit Categories below)
5) **Collect Findings:** Record each violation with severity, location (file:line), effort estimate (S/M/L), recommendation
6) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
7) **Write Report:** Build full markdown report per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/611-structure.md` in single Write call
8) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Categories

| # | Category | What to Check |
|---|----------|---------------|
| 1 | **Hierarchy & Links** | CLAUDE.md is root; all docs reachable via links; no orphaned files; no broken links |
| 2 | **Single Source of Truth** | No content duplication; duplicates replaced with links to source; clear ownership |
| 3 | **Proactive Compression** | Eliminate verbose/redundant content; prose to tables; remove meaningless info; compress even under-limit files; see [size_limits.md](references/size_limits.md) |
| 4 | **Requirements Compliance** | Correct sections; within size limits; **no code blocks** (tables/ASCII diagrams/text only); stack-appropriate doc links |
| 5 | **Actuality (CRITICAL)** | **Verify facts against code:** paths exist, functions match, APIs work, configs valid; outdated docs are worse than none |
| 6 | **Legacy Cleanup** | No history sections; no "was changed" notes; no deprecated info; current state only |
| 7 | **Stack Adaptation** | Links/refs match project stack; no Python examples in .NET project; official docs for correct platform |

### Severity Mapping

| Issue Type | Severity |
|------------|----------|
| Outdated content (code mismatch) | CRITICAL |
| Broken links, orphaned docs | HIGH |
| Content duplication | MEDIUM |
| Missing compression opportunity | LOW |
| Legacy/history content | MEDIUM |
| Wrong stack references | HIGH |

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/611-structure.md` with `category: "Documentation Structure"` and checks: hierarchy_links, ssot, compression, requirements_compliance, actuality, legacy_cleanup, stack_adaptation.

Return summary to coordinator:
```
Report written: docs/project/.audit/ln-610/{YYYY-MM-DD}/611-structure.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

- **Do not auto-fix:** Report violations only; coordinator aggregates for user
- **Tech stack aware:** Use contextStore `tech_stack` to apply stack-specific checks (e.g., .NET vs Node.js doc standards)
- **Verify facts against code:** Actively check every path, function name, API, config mentioned in docs
- **Compress always:** Size limits are upper bounds, not targets. A 100-line file instead of 300 is a win
- **No code in docs:** Documents describe algorithms in tables or ASCII diagrams. Code belongs in codebase
- **Code is truth:** When docs contradict code, report docs as needing update (not code)
- **Delete, don't archive:** Legacy content should be removed, not moved to "archive"
- **Location precision:** Always include `file:line` for programmatic navigation

## Definition of Done

- contextStore parsed successfully (including output_dir)
- All 7 structural categories audited
- Findings collected with severity, location, effort, recommendation
- Score calculated using penalty algorithm
- Report written to `{output_dir}/611-structure.md` (atomic single Write call)
- Summary returned to coordinator

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`
- Size limits and targets: [references/size_limits.md](references/size_limits.md)
- Detailed checklist: [references/audit_checklist.md](references/audit_checklist.md)

---
**Version:** 1.0.0
**Last Updated:** 2026-03-01
