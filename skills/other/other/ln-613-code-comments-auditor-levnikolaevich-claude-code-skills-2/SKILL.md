---
name: ln-613-code-comments-auditor
description: "Checks inline code documentation quality: WHY-not-WHAT, density, forbidden content, docstrings quality, actuality, legacy cleanup. Use when auditing comments and docstrings."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-line__outline, mcp__hex-line__read_file
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Inline Code Documentation Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing inline code documentation quality: comments, docstrings, and language-specific documentation blocks.

## Purpose & Scope

- Audit inline code documentation for **quality and compliance** across 6 categories
- Universal for any tech stack (auto-detect comment syntax)
- Return structured findings to coordinator with severity, location, recommendations
- Calculate compliance score (X/10) for Inline Code Documentation category
- Scope is limited to comments/docstrings/JSDoc/XML docs
- Out of scope: code design quality, naming quality, test quality, architecture quality, or feature correctness except where comments contradict code

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/mcp_tool_preferences.md`.

Receives `contextStore` with: `tech_stack`, `project_root`, `output_dir`.

## Workflow

1) **Parse Context:** Extract tech stack, project root, output_dir from contextStore
2) **Scan:** Find all source files (use `tech_stack` for detection)
   **Hex-line primary path:** Use `outline(path)` and discovery-first `read_file()` for code files before analyzing comments. Use `edit_ready=true, verbosity="full"` only if the audit turns into a follow-up edit. Do not use `hex-graph` here - comment quality is a code-reading problem, not a semantic graph problem.
3) **Extract:** Parse inline comments + docstrings/JSDoc
4) **Audit:** Run 6 category checks (see Audit Categories below)
5) **Collect Findings:** Record each violation with severity, location (file:line), effort estimate (S/M/L), recommendation
6) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
7) **Write Report:** Build full markdown report per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-613--global.md` in single Write call
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

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-613--global.md` with `category: "Inline Code Documentation"` and checks: why_not_what, density, forbidden_content, docstrings_quality, actuality, legacy_cleanup.

Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-613--global.md
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

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report violations only; coordinator aggregates for user
- **Fix code, not rules:** NEVER modify rules files (*_rules.md, *_standards.md) to make violations pass
- **Code is truth:** When comment contradicts code, flag the documentation for update; do not turn this into a general code-quality review
- **WHY > WHAT:** Comments explaining obvious behavior should be removed
- **Universal:** Works with any language; detect comment syntax automatically
- **Location precision:** Always include `file:line` for programmatic navigation

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully (including output_dir)
- [ ] All source files scanned (tech stack from contextStore)
- [ ] All 6 categories audited
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated using penalty algorithm
- [ ] Report written to `{output_dir}/ln-613--global.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- Comment rules and patterns: [references/comments_rules.md](references/comments_rules.md)

---
**Version:** 4.0.0
**Last Updated:** 2026-03-01
