---
name: ln-601-semantic-content-auditor
description: Semantic content auditor (L3 Worker). Verifies document content matches stated SCOPE, aligns with project goals, and reflects actual codebase state. Called by ln-600 for each project document. Returns scope_alignment and fact_accuracy scores with findings.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Semantic Content Auditor (L3 Worker)

Specialized worker auditing semantic accuracy of project documentation.

## Purpose & Scope

- **Worker in ln-600 coordinator pipeline** - invoked by ln-600-docs-auditor for each project document
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

```json
{
  "doc_path": "docs/project/architecture.md",
  "project_root": "/path/to/project",
  "tech_stack": {
    "language": "TypeScript",
    "frameworks": ["Express", "React"]
  }
}
```

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

## Output Format

Return JSON to coordinator:

```json
{
  "doc_path": "docs/project/architecture.md",
  "scope": {
    "stated": "System architecture with C4 diagrams, component interactions",
    "coverage_percent": 85
  },
  "scores": {
    "scope_alignment": 8,
    "fact_accuracy": 6,
    "overall": 7
  },
  "summary": {
    "total_issues": 4,
    "high": 1,
    "medium": 2,
    "low": 1
  },
  "findings": [
    {
      "severity": "HIGH",
      "type": "BEHAVIOR_MISMATCH",
      "location": "line 45",
      "issue": "Architecture shows 3-tier (Controller->Service->Repository) but code has Controller->Repository direct calls",
      "evidence": "src/controllers/UserController.ts:23 imports UserRepository directly",
      "fix": "Update diagram to show actual pattern OR refactor code to match docs"
    },
    {
      "severity": "MEDIUM",
      "type": "OUTDATED_PATH",
      "location": "line 78",
      "issue": "References src/services/legacy/ which was removed",
      "evidence": "Folder does not exist: ls src/services/legacy/ returns error",
      "fix": "Remove reference or update to current path"
    }
  ]
}
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
- Both scores calculated
- JSON result returned to coordinator

---
**Version:** 1.0.0
**Last Updated:** 2026-01-28
