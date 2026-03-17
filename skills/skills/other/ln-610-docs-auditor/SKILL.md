---
name: ln-610-docs-auditor
description: "Coordinates 3 specialized documentation audit workers (structure, semantic, code comments). Detects project type, delegates parallel audits, aggregates results into docs/project/docs_audit.md."
allowed-tools: Read, Grep, Glob, Bash, Skill
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Documentation Auditor (L2 Coordinator)

Coordinates 3 specialized audit workers to perform comprehensive documentation quality analysis.

## Purpose & Scope

- **Coordinates 3 audit workers** running in parallel:
  - ln-611 (documentation structure) — 1 invocation
  - ln-612 (semantic content) — N invocations (per target document)
  - ln-613 (code comments) — 1 invocation
- Detect project type + tech stack ONCE
- Pass shared context to all workers (token-efficient)
- Aggregate worker results into single consolidated report
- Write report to `docs/project/docs_audit.md` (file-based, no task creation)
- Manual invocation by user or called by ln-100-documents-pipeline

## Workflow

1) **Discovery:** Detect project type, tech stack, scan .md files
2) **Context Build:** Build contextStore with output_dir, project_root, tech_stack
3) **Prepare Output:** Create output directory
4) **Delegate:** Invoke 3 workers in parallel
5) **Aggregate:** Collect worker results, calculate overall score
6) **Context Validation:** Post-filter findings
7) **Write Report:** Save to `docs/project/docs_audit.md`

## Phase 1: Discovery

**Load project metadata:**
- `CLAUDE.md` — root of documentation hierarchy
- `docs/README.md` — documentation index
- Package manifests: `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`
- Existing docs in `docs/project/`

**Extract:**
- Programming language(s)
- Major frameworks/libraries
- List of `.md` files in project (for ln-611 hierarchy check)
- Target documents for semantic audit (for ln-612)

**Target documents for ln-612:**
```
FOR doc IN [CLAUDE.md, docs/README.md, docs/documentation_standards.md,
            docs/principles.md, docs/project/*.md]:
  IF doc exists AND doc NOT IN [docs/tasks/*, docs/reference/*, docs/presentation/*]:
    semantic_targets.append(doc)
```

## Phase 2: Build contextStore

```json
{
  "tech_stack": {"language": "...", "frameworks": [...]},
  "project_root": "...",
  "output_dir": "docs/project/.audit/ln-610/{YYYY-MM-DD}"
}
```

Where `{YYYY-MM-DD}` is current date (e.g., `2026-03-01`).

## Phase 3: Prepare Output

```bash
mkdir -p {output_dir}
```

**No deletion** of previous date folders — history preserved for comparison.

## Phase 4: Delegate to Workers

Invoke all workers **in parallel** via Skill tool:

| Worker | Invocations | Output |
|--------|-------------|--------|
| ln-611-docs-structure-auditor | 1 | `{output_dir}/611-structure.md` |
| ln-612-semantic-content-auditor | N (per target document) | `{output_dir}/612-semantic-{doc-slug}.md` |
| ln-613-code-comments-auditor | 1 | `{output_dir}/613-code-comments.md` |

Pass contextStore to each worker. For ln-612, additionally pass `doc_path` per invocation.

**Worker return format:** `Report written: ... | Score: X.X/10 | Issues: N (C:N H:N M:N L:N)`

## Phase 5: Aggregate Results

1. Parse scores from worker return values
2. Read worker reports from `{output_dir}/` for detailed findings
3. Calculate category scores:

| Category | Source | Weight |
|----------|--------|--------|
| Documentation Structure | ln-611 | 35% |
| Semantic Content | ln-612 (avg across docs) | 40% |
| Code Comments | ln-613 | 25% |

4. Calculate overall score: weighted average of 3 categories

## Phase 6: Context Validation (Post-Filter)

**MANDATORY READ:** Load `shared/references/context_validation.md`

Apply Rule 1 + documentation-specific inline filters:
```
FOR EACH finding WHERE severity IN (HIGH, MEDIUM):
  # Rule 1: ADR/Planned Override
  IF finding matches ADR → advisory "[Planned: ADR-XXX]"

  # Doc-specific: Compression context (from ln-611)
  IF Structure finding Cat 3 (Compression):
    - Skip if path in references/ or templates/ (reference docs = naturally large)
    - Skip if filename contains architecture/design/api_spec
    - Skip if tables+lists > 50% of content (already structured)

  # Doc-specific: Actuality severity calibration (from ln-611)
  IF Structure finding Cat 5 (Actuality):
    - Path/function COMPLETELY missing → CRITICAL
    - Path exists but deprecated/renamed → HIGH
    - Example code outdated but concept valid → MEDIUM

  # Comment-specific: Per-category density targets (from ln-613)
  IF Comment finding Cat 2 (Density):
    - test/ or tests/ → target density 2-10%
    - infra/ or config/ or ci/ → target density 5-15%
    - business/domain/services → target density 15-25%
    Recalculate with per-category target.

  # Comment-specific: Complexity context for WHY-not-WHAT (from ln-613)
  IF Comment finding Cat 1 (WHY not WHAT):
    - If file McCabe complexity > 15 → WHAT comments acceptable
    - If file in domain/ or business/ → explanatory comments OK

Downgraded findings → "Advisory Findings" section in report.
```

## Phase 7: Write Report

Write consolidated report to `docs/project/docs_audit.md`:

```markdown
## Documentation Audit Report - {DATE}

### Overall Score: X.X/10

| Category | Score | Worker | Issues |
|----------|-------|--------|--------|
| Documentation Structure | X/10 | ln-611 | N issues |
| Semantic Content | X/10 | ln-612 | N issues (across M docs) |
| Code Comments | X/10 | ln-613 | N issues |

### Critical Findings

- [ ] **[Category]** `path/file:line` - Issue. **Action:** Fix suggestion.

### Advisory Findings

(Context-validated findings downgraded from MEDIUM/HIGH)

### Recommended Actions

| Priority | Action | Location | Category |
|----------|--------|----------|----------|
| High | ... | ... | ... |
```

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Critical Notes

- **Pure coordinator:** Does NOT perform any audit checks directly. ALL auditing delegated to workers.
- **Fix content, not rules:** NEVER modify standards/rules files to make violations pass
- **Verify facts against code:** Workers actively check every path, function name, API, config
- **Compress always:** Size limits are upper bounds, not targets
- **No code in docs:** Documents describe algorithms in tables or ASCII diagrams
- **Code is truth:** When docs contradict code, always update docs
- **Delete, don't archive:** Legacy content removed, not archived

## Definition of Done

- Project metadata discovered (tech stack, doc list)
- contextStore built with output_dir = `docs/project/.audit/ln-610/{YYYY-MM-DD}`
- Output directory created (no deletion of previous runs)
- All 3 workers invoked and completed
- Worker reports aggregated: 3 category scores + overall
- Context Validation applied to all findings
- Consolidated report written to `docs/project/docs_audit.md`

## Reference Files

- **Context validation rules:** `shared/references/context_validation.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Task delegation pattern:** `shared/references/task_delegation_pattern.md`

---
**Version:** 5.0.0
**Last Updated:** 2026-03-01
