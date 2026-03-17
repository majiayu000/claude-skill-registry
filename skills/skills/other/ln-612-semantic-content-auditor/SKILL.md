---
name: ln-612-semantic-content-auditor
description: Semantic content auditor (L3 Worker). Verifies document content matches stated SCOPE, aligns with project goals, and reflects actual codebase state. Called by ln-610 for each project document. Writes file-based report with scope_alignment and fact_accuracy scores.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Semantic Content Auditor (L3 Worker)

Specialized worker auditing semantic accuracy of project documentation.

## Purpose & Scope

- **Worker in ln-610 coordinator pipeline** - invoked by ln-610-docs-auditor for each project document
- Verify document content **matches stated SCOPE** (document purpose)
- Check content **aligns with project goals** (value contribution)
- Validate **facts against codebase** (accuracy and freshness)
- Return structured findings to coordinator with severity, location, fix suggestions

## Target Documents

Called ONLY for project documents (not reference/tasks):

| Document | Verification Focus |
|----------|-------------------|
| `CLAUDE.md` | Instructions match project structure, paths valid |
| `docs/README.md` | Navigation accurate, descriptions match reality |
| `docs/documentation_standards.md` | Standards applicable to this project |
| `docs/principles.md` | Principles reflected in actual code patterns |
| `docs/project/requirements.md` | Requirements implemented or still valid |
| `docs/project/architecture.md` | Architecture matches actual code structure |
| `docs/project/tech_stack.md` | Versions/technologies match package files |
| `docs/project/api_spec.md` | Endpoints/contracts match controllers |
| `docs/project/database_schema.md` | Schema matches actual DB/migrations |
| `docs/project/design_guidelines.md` | Components/styles exist in codebase |
| `docs/project/runbook.md` | Commands work, paths valid |

**Excluded:** `docs/tasks/`, `docs/reference/`, `docs/presentation/`, `tests/`

## Inputs (from Coordinator)

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md#audit-coordinator--worker-contract` for contextStore structure.

Receives from coordinator per invocation:

| Field | Description |
|-------|-------------|
| `doc_path` | Path to document to audit (e.g., `docs/project/architecture.md`) |
| `output_dir` | Directory for report output (from contextStore) |
| `project_root` | Project root path |
| `tech_stack` | Detected technology stack |

## Workflow

### Phase 1: SCOPE EXTRACTION

1. Read document first 20 lines
2. Parse `<!-- SCOPE: ... -->` comment
3. If no SCOPE tag, infer from document type (see Verification Rules)
4. Record stated purpose/boundaries

### Phase 2: CONTENT-SCOPE ALIGNMENT

Analyze document sections against stated scope:

| Check | Finding Type |
|-------|--------------|
| Section not serving scope | OFF_TOPIC |
| Scope aspect not covered | MISSING_COVERAGE |
| Excessive detail beyond scope | SCOPE_CREEP |
| Content duplicated elsewhere | SSOT_VIOLATION |

**Scoring:**
- 10/10: All content serves scope, scope fully covered
- 8-9/10: Minor off-topic content or small gaps
- 6-7/10: Some sections not aligned, partial coverage
- 4-5/10: Significant misalignment, major gaps
- 1-3/10: Document does not serve its stated purpose

### Phase 3: FACT VERIFICATION

Per document type, verify claims against codebase:

| Document | Verification Method |
|----------|---------------------|
| architecture.md | Check layers exist (Glob for folders), verify imports follow described pattern (Grep) |
| tech_stack.md | Compare versions with package.json, go.mod, requirements.txt |
| api_spec.md | Match endpoints with controller/route files (Grep for routes) |
| requirements.md | Search for feature implementations (Grep for keywords) |
| database_schema.md | Compare with migration files or Prisma/TypeORM schemas |
| runbook.md | Validate file paths exist (Glob), test command syntax |
| principles.md | Sample code files for principle adherence patterns |
| CLAUDE.md | Verify referenced paths/files exist |

**Finding Types:**
- OUTDATED_PATH: File/folder path no longer exists
- WRONG_VERSION: Documented version differs from package file
- MISSING_ENDPOINT: Documented API endpoint not found in code
- BEHAVIOR_MISMATCH: Described behavior differs from implementation
- STALE_REFERENCE: Reference to removed/renamed entity

**Scoring:**
- 10/10: All facts verified against code
- 8-9/10: Minor inaccuracies (typos, formatting)
- 6-7/10: Some paths/names outdated, core info correct
- 4-5/10: Functional mismatches (wrong behavior described)
- 1-3/10: Critical mismatches (architecture wrong, APIs broken)

### Phase 4: SCORING & REPORT

Calculate final scores and compile findings:

```
scope_alignment_score = weighted_average(coverage, relevance, focus)
fact_accuracy_score = (verified_facts / total_facts) * 10

overall_score = (scope_alignment * 0.4) + (fact_accuracy * 0.6)
```

Fact accuracy weighted higher because incorrect information is worse than scope drift.

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/612-semantic-{doc-slug}.md` where `doc-slug` is derived from document filename (e.g., `architecture`, `tech_stack`, `claude_md`).

With `category: "Semantic Content"` and checks: scope_alignment, fact_accuracy.

Return summary to coordinator:
```
Report written: docs/project/.audit/ln-610/{YYYY-MM-DD}/612-semantic-architecture.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Verification Rules by Document Type

**MANDATORY READ:** Load [references/verification_rules.md](references/verification_rules.md) for per-document verification patterns.

## Critical Rules

- **Read before judge:** Always read full document and relevant code before reporting issues
- **Evidence required:** Every finding must include `evidence` field with verification command/result
- **Code is truth:** When docs contradict code, document is wrong (unless code is a bug)
- **Scope inference:** If no SCOPE tag, use document filename to infer expected scope
- **No false positives:** Better to miss an issue than report incorrectly
- **Location precision:** Always include line number for findings
- **Actionable fixes:** Every finding must have concrete fix suggestion

## Definition of Done

- Document read completely
- SCOPE extracted or inferred
- Content-scope alignment analyzed
- Facts verified against codebase (with evidence)
- Score calculated using penalty algorithm
- Report written to `{output_dir}/612-semantic-{doc-slug}.md` (atomic single Write call)
- Summary returned to coordinator

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`
- Verification rules: [references/verification_rules.md](references/verification_rules.md)

---
**Version:** 2.0.0
**Last Updated:** 2026-03-01
