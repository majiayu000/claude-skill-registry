---
name: ln-610-docs-auditor
description: "Coordinates documentation audit across structure, semantic content, fact-checking, and code comments. Use when auditing all project documentation."
allowed-tools: Read, Grep, Glob, Bash, Skill
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Documentation Auditor (L2 Coordinator)

Coordinates 4 specialized audit workers to perform comprehensive documentation quality analysis.

## Purpose & Scope

- **Coordinates 4 audit workers** running in parallel:
  - ln-611 (documentation structure) — 1 invocation
  - ln-612 (semantic content) — N invocations (per target document)
  - ln-613 (code comments) — 1 invocation
  - ln-614 (fact verification) — 1 invocation
- Detect project type + tech stack ONCE
- Pass shared context to all workers (token-efficient)
- Aggregate worker results into single consolidated report
- Write report to `docs/project/docs_audit.md` (file-based, no task creation)
- Manual invocation by user or called by ln-100-documents-pipeline

## Workflow

1) **Discovery:** Detect project type, tech stack, scan .md files
2) **Context Build:** Build contextStore with output_dir, project_root, tech_stack
3) **Prepare Output:** Create output directory
4) **Delegate:** Invoke 4 workers in parallel
5) **Aggregate:** Collect worker results, calculate overall score
6) **Context Validation:** Post-filter findings
7) **Write Report:** Save to `docs/project/docs_audit.md`
8) **Results Log:** Append trend row
9) **Cleanup:** Delete worker files

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

Worker files are cleaned up after consolidation (see Phase 9).

## Phase 4: Delegate to Workers

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md`.

All workers in PARALLEL via Agent tool:

| Worker | Invocations | Output |
|--------|-------------|--------|
| ln-611-docs-structure-auditor | 1 | `{output_dir}/611-structure.md` |
| ln-612-semantic-content-auditor | N (per target document) | `{output_dir}/612-semantic-{doc-slug}.md` |
| ln-613-code-comments-auditor | 1 | `{output_dir}/613-code-comments.md` |
| ln-614-docs-fact-checker | 1 | `{output_dir}/614-fact-checker.md` |

ln-614 receives only `contextStore` and discovers `.md` files internally. Workers follow the shared file-based audit contract and return compact summaries with report path, score, and severity counts.

**Invocation:**
```javascript
// Global workers (ln-611, ln-613, ln-614) — 1 invocation each:
FOR EACH worker IN [ln-611, ln-613, ln-614]:
  Agent(description: "Docs audit via " + worker,
       prompt: "Execute audit worker.

Step 1: Invoke worker:
  Skill(skill: \"" + worker + "\")

CONTEXT:
" + JSON.stringify(contextStore),
       subagent_type: "general-purpose")

// Per-document worker (ln-612) — N invocations:
FOR EACH doc IN semantic_targets:
  doc_context = { ...contextStore, doc_path: doc }
  Agent(description: "Semantic audit " + doc + " via ln-612",
       prompt: "Execute audit worker.

Step 1: Invoke worker:
  Skill(skill: \"ln-612-semantic-content-auditor\")

CONTEXT:
" + JSON.stringify(doc_context),
       subagent_type: "general-purpose")
```

## Phase 5: Aggregate Results

**MANDATORY READ:** Load `shared/references/audit_coordinator_aggregation.md`.

Use the shared aggregation pattern for summary parsing, worker report reads, severity rollups, and final report assembly.

Category weights:

| Category | Source | Weight |
|----------|--------|--------|
| Documentation Structure | ln-611 | 25% |
| Semantic Content | ln-612 (avg across docs) | 30% |
| Code Comments | ln-613 | 20% |
| Fact Accuracy | ln-614 | 25% |

Calculate overall score as the weighted average of the 4 categories above.

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

  # Fact-checker: Example/template path exclusion (from ln-614)
  IF Fact finding (PATH_NOT_FOUND):
    - Path in examples/ or templates/ directory reference → advisory
    - Path has placeholder pattern (YOUR_*, <project>, {name}) → remove

  # Fact-checker: Planned feature claims (from ln-614)
  IF Fact finding (ENTITY_NOT_FOUND, ENDPOINT_NOT_FOUND):
    - Entity mentioned in ADR/roadmap as planned → advisory "[Planned: ADR-XXX]"

  # Fact-checker: Cross-doc contradiction authority (from ln-614)
  IF Fact finding (CROSS_DOC_*_CONFLICT):
    - docs/project/ is authority over docs/reference/ → report reference doc

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
| Fact Accuracy | X/10 | ln-614 | N issues |

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

**MANDATORY READ:** Load `shared/references/audit_scoring.md`.

## Critical Notes

- **Pure coordinator:** Does NOT perform any audit checks directly. ALL auditing delegated to workers.
- **Fix content, not rules:** NEVER modify standards/rules files to make violations pass
- **Fact verification via ln-614:** Dedicated worker extracts and verifies all claims across ALL docs
- **Compress always:** Size limits are upper bounds, not targets
- **No code in docs:** Documents describe algorithms in tables or ASCII diagrams
- **Code is truth:** When docs contradict code, always update docs
- **Delete, don't archive:** Legacy content removed, not archived

## Phase 8: Append Results Log

**MANDATORY READ:** Load `shared/references/results_log_pattern.md`

Append one row to `docs/project/.audit/results_log.md` with: Skill=`ln-610`, Metric=`overall_score`, Scale=`0-10`, Score from Phase 7 report. Calculate Delta vs previous `ln-610` row. Create file with header if missing. Rolling window: max 50 entries.

## Phase 9: Cleanup Worker Files

```bash
rm -rf {output_dir}
```

Delete the dated output directory (`docs/project/.audit/ln-610/{YYYY-MM-DD}/`). The consolidated report and results log already preserve all audit data.

## Definition of Done

- [ ] Project metadata discovered (tech stack, doc list)
- [ ] contextStore built with output_dir = `docs/project/.audit/ln-610/{YYYY-MM-DD}`
- [ ] Output directory created for worker reports
- [ ] All 4 workers invoked and completed
- [ ] Worker reports aggregated: 4 category scores + overall
- [ ] Context Validation applied to all findings
- [ ] Consolidated report written to `docs/project/docs_audit.md`
- [ ] Results log row appended to `docs/project/.audit/results_log.md`
- [ ] Worker output directory cleaned up after consolidation

## Phase 10: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `review-coordinator` (workers only). Run after all phases complete. Output to chat using the `review-coordinator — workers only` format.

## Reference Files

- **Context validation rules:** `shared/references/context_validation.md`
- **Task delegation pattern:** `shared/references/task_delegation_pattern.md`
- **Aggregation pattern:** `shared/references/audit_coordinator_aggregation.md`

---
**Version:** 5.0.0
**Last Updated:** 2026-03-01
