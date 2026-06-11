---
name: sapcc-audit
description: "Full-repo SAP CC Go compliance audit against review standards."
user-invocable: false
command: /sapcc-audit
agent: golang-general-engineer
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
  - Skill
routing:
  triggers:
    - sapcc audit
    - sapcc compliance
    - check sapcc rules
    - full repo audit
    - sapcc secondary review
    - sapcc standards check
  pairs_with:
    - golang-general-engineer
    - golang-general-engineer-compact
    - go-patterns
  force_route: false
  complexity: Complex
  category: language
---

# SAPCC Full-Repo Compliance Audit v2

Review every package against established review standards. Not checklist compliance — **code-level review** that finds over-engineering, dead code, interface violations, and inconsistent patterns.

---

## Reference Loading Table

| Signal | Load This File | When |
|--------|---------------|------|
| Phase 1 begins | `references/phase-1-discover-commands.md` | Detection commands, package mapping, segmentation table |
| Phase 2 begins | `references/phase-2-dispatch-agents.md` | Full dispatch prompt and per-domain review checklist (11 areas) |
| Phase 3 begins | `references/output-templates.md` | Report scaffold, per-finding format, severity guide |

Load each reference file at the start of its phase. Do not load all three upfront.

---

## Instructions

### Phase 1: DISCOVER

**Goal**: Map the repository and plan the package segmentation.

Read `references/phase-1-discover-commands.md` for the exact detection commands, segmentation table, and file-count queries.

Verify this is an sapcc project (sapcc imports in go.mod). If not, stop immediately.

Map all packages, count files per package, and produce a segmentation table (5–8 agents, 5–15 files each).

**Gate**: Packages mapped, agents planned. Proceed to Phase 2.

---

### Phase 2: DISPATCH

**Goal**: Launch parallel agents that review packages against project standards.

Read `references/phase-2-dispatch-agents.md` for the full dispatch prompt (11 review areas: over-engineering, dead code, error messages, constructors, interface contracts, copy-paste, HTTP handlers, database patterns, type patterns, logging, mixed approaches).

Use the standard dispatch prompt verbatim, substituting the assigned package list.

**Dispatch all agents in a single message using the Task tool with `subagent_type=golang-general-engineer`.**

**Gate**: All agents dispatched. Proceed to Phase 3.

---

### Phase 3: COMPILE REPORT

**Goal**: Aggregate findings into a code-level compliance report.

Read `references/output-templates.md` for the report scaffold, per-finding format, and deduplication rules.

Deduplicate by `file:line`. Write `sapcc-audit-report.md`. Display verdict, must-fix count, and top 5 findings inline.

**Gate**: Report complete.

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Not an sapcc project | Stop immediately. Print: "This does not appear to be an SAP CC Go project (no sapcc imports in go.mod)." |
| Agents cannot read a file | Log and continue. Flag in the report under "Warnings." |
| gopls MCP tools unavailable | Fall back to manual grep-based analysis. Note in the report. |
| Too many packages (>30) | Split into >8 agents. Ensure each still gets 5-15 files. |
| Agent finds no violations | Report is valid. Output empty sections for unused severity levels. |

**Audit only**: READS and REPORTS. Does NOT modify code unless explicitly asked with `--fix`.

---

## Integration

- **Router**: `/do` routes via "sapcc audit", "sapcc compliance", "sapcc lead review"
- **Pairs with**: `go-patterns` (the rules), `golang-general-engineer` (the executor)

### Per-agent reference loading (included in each agent's dispatch prompt based on assigned packages)

| Package Type | Reference to Load |
|-------------|-------------------|
| HTTP handlers (`internal/api/`) | `api-design-detailed.md` |
| Test files (`*_test.go`) | `testing-patterns-detailed.md` |
| Error handling heavy packages | `error-handling-detailed.md` |
| Architecture/drivers | `architecture-patterns.md` |
| Build/CI config | `build-ci-detailed.md` |
| Import-heavy files | `library-reference.md` |

Always available for calibration (load only when needed): `quality-issues.md`, `review-standards-lead.md`.
