---
name: ln-613-code-comments-auditor
description: Code comments audit worker (L3). Checks WHY-not-WHAT, density (15-20%), forbidden content, docstrings quality, actuality, legacy cleanup. Returns findings with severity, location, and recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Code Comments Auditor (L3 Worker)

Specialized worker auditing code comments and docstrings quality.

## Purpose & Scope

- **Worker in ln-610 coordinator pipeline** - invoked by ln-610-docs-auditor
- Audit code comments for **quality and compliance** across 6 categories
- Universal for any tech stack (auto-detect comment syntax)
- Return structured findings to coordinator with severity, location, recommendations
- Calculate compliance score (X/10) for Code Comments category

## Inputs (from Coordinator)

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md#audit-coordinator--worker-contract` for contextStore structure.

Receives `contextStore` with: `tech_stack`, `project_root`, `output_dir`.

## Workflow

1) **Parse Context:** Extract tech stack, project root, output_dir from contextStore
2) **Scan:** Find all source files (use `tech_stack` for detection)
3) **Extract:** Parse inline comments + docstrings/JSDoc
4) **Audit:** Run 6 category checks (see Audit Categories below)
5) **Collect Findings:** Record each violation with severity, location (file:line), effort estimate (S/M/L), recommendation
6) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
7) **Write Report:** Build full markdown report per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/613-code-comments.md` in single Write call
8) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Categories

| # | Category | What to Check |
|---|----------|---------------|
| 1 | **WHY not WHAT** | Comments explain rationale, not obvious code behavior; no restating code |
| 2 | **Density (15-20%)** | Comment-to-code ratio within range; not over/under-commented |
| 3 | **No Forbidden Content** | No dates/authors; no historical notes; no code examples in comments |
| 4 | **Docstrings Quality** | Match function signatures; parameters documented; return types accurate |
| 5 | **Actuality** | Comments match code behavior; no stale references; examples runnable |
| 6 | **Legacy Cleanup** | No TODO without context; no commented-out code; no deprecated notes |

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/613-code-comments.md` with `category: "Code Comments"` and checks: why_not_what, density, forbidden_content, docstrings_quality, actuality, legacy_cleanup.

Return summary to coordinator:
```
Report written: docs/project/.audit/ln-610/{YYYY-MM-DD}/613-code-comments.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

**Severity mapping:**

| Issue Type | Severity |
|------------|----------|
| Author names, dates in comments | CRITICAL |
| Commented-out code blocks | HIGH |
| Stale/outdated comments | HIGH |
| Obvious WHAT comments | MEDIUM |
| Density deviation >5% | MEDIUM |
| Minor density deviation | LOW |

## Reference Files

- Comment rules and patterns: [references/comments_rules.md](references/comments_rules.md)

## Critical Rules

- **Do not auto-fix:** Report violations only; coordinator aggregates for user
- **Fix code, not rules:** NEVER modify rules files (*_rules.md, *_standards.md) to make violations pass
- **Code is truth:** When comment contradicts code, flag comment for update
- **WHY > WHAT:** Comments explaining obvious behavior should be removed
- **Universal:** Works with any language; detect comment syntax automatically
- **Location precision:** Always include `file:line` for programmatic navigation

## Definition of Done

- contextStore parsed successfully (including output_dir)
- All source files scanned (tech stack from contextStore)
- All 6 categories audited
- Findings collected with severity, location, effort, recommendation
- Score calculated using penalty algorithm
- Report written to `{output_dir}/613-code-comments.md` (atomic single Write call)
- Summary returned to coordinator

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`
- Comment rules and patterns: [references/comments_rules.md](references/comments_rules.md)

---
**Version:** 4.0.0
**Last Updated:** 2026-03-01
