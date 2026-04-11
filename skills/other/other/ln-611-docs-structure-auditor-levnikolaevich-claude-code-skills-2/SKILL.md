---
name: ln-611-docs-structure-auditor
description: "Checks hierarchy, links, SSOT, compression, requirements compliance, freshness, legacy cleanup. Use when auditing documentation structure."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-line__outline
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Documentation Structure Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing structural quality of project documentation.

## Purpose & Scope

- Audit documentation for **structural quality** across 7 categories
- Scan all `.md` files in project, build hierarchy from `AGENTS.md` when present
- Return structured findings to coordinator with severity, location, recommendations
- Calculate compliance score (X/10) for Documentation Structure

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`, `shared/references/docs_quality_contract.md`, `shared/references/docs_quality_rules.json`, and `shared/references/markdown_read_protocol.md`.

Receives `contextStore` with: `tech_stack`, `project_root`, `output_dir`.

## Workflow

1) **Parse Context:** Extract tech stack, project root, output_dir from contextStore
2) **Load Registry if Present:** Use `docs/project/.context/doc_registry.json` as the first routing source when available
3) **Scan Docs:** Find all `.md` files in project (`AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/**`)
4) **Read Section-First:** For larger docs, outline first, then read header markers + `Quick Navigation` + `Agent Entry` + `Maintenance`
5) **Build Tree:** Construct hierarchy from `AGENTS.md` outward links when present, otherwise from `CLAUDE.md`
6) **Audit Categories 1-7:** Run structural checks (see Audit Categories below)
7) **Collect Findings:** Record each violation with severity, location (file:line), effort estimate (S/M/L), recommendation
8) **Calculate Score:** Count violations by severity, calculate compliance score (X/10)
9) **Write Report:** Build full markdown report per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/611-structure.md` in single Write call
10) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Categories

| # | Category | What to Check |
|---|----------|---------------|
| 1 | **Hierarchy & Links** | `AGENTS.md` is canonical root when present; all docs reachable via links; no orphaned files; no broken links |
| 2 | **Single Source of Truth** | No content duplication; duplicates replaced with links to source; clear ownership |
| 3 | **Proactive Compression** | Eliminate verbose/redundant content; prose to tables; remove meaningless info; compress even under-limit files; see [size_limits.md](references/size_limits.md) |
| 4 | **Requirements Compliance** | Correct header markers, correct top sections, within size limits, no illegal code blocks, stack-appropriate doc links |
| 5 | **Freshness Indicators** | Detect staleness signals: dates >6 months in content, deprecated API/tool references, TODO/FIXME markers, placeholder text left in place; deep fact-checking handled by dedicated worker |
| 6 | **Legacy Cleanup** | No history sections; no "was changed" notes; no deprecated info; current state only |
| 7 | **Stack Adaptation** | Links/refs match project stack; no Python examples in .NET project; official docs for correct platform |

### Severity Mapping

| Issue Type | Severity |
|------------|----------|
| Staleness indicators (old dates, deprecated refs, TODO markers) | MEDIUM |
| Broken links, orphaned docs | HIGH |
| Content duplication | MEDIUM |
| Missing compression opportunity | LOW |
| Legacy/history content | MEDIUM |
| Wrong stack references | HIGH |

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/611-structure.md` with `category: "Documentation Structure"` and checks: hierarchy_links, ssot, compression, requirements_compliance, freshness_indicators, legacy_cleanup, stack_adaptation.

Return summary per `shared/references/audit_summary_contract.md`.

Standalone mode still writes the same JSON summary to a worker-owned run-scoped artifact path per shared contract.

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report violations only; coordinator aggregates for user
- **Tech stack aware:** Use contextStore `tech_stack` to apply stack-specific checks (e.g., .NET vs Node.js doc standards)
- **No deep fact-checking:** Detect staleness signals only (dates, deprecated refs, TODO markers)
- **Compress always:** Size limits are upper bounds, not targets. A 100-line file instead of 300 is a win
- **No code in docs:** Documents describe algorithms in tables or ASCII diagrams. Code belongs in codebase
- **Code is truth:** When docs contradict code, report docs as needing update (not code)
- **Delete, don't archive:** Legacy content should be removed, not moved to "archive"
- **Location precision:** Always include `file:line` for programmatic navigation
- **Shared contract precedence:** Placeholder policy, template-metadata policy, and no-code exceptions come from `docs_quality_contract.md` / `docs_quality_rules.json`

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully (including output_dir)
- [ ] All 7 structural categories audited
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated using penalty algorithm
- [ ] Report written to `{output_dir}/611-structure.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- Size limits and targets: [references/size_limits.md](references/size_limits.md)
- Detailed checklist: [references/audit_checklist.md](references/audit_checklist.md)

---
**Version:** 1.0.0
**Last Updated:** 2026-03-01
