---
name: ln-610-docs-auditor
description: "Coordinates audit of project knowledge surfaces: markdown documentation plus inline code documentation (comments/docstrings). Use when auditing project documentation."
allowed-tools: Read, Grep, Glob, Bash, Skill
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Documentation Auditor (L2 Coordinator)

**Type:** L2 Coordinator

Coordinates specialized audit workers to perform quality analysis for project knowledge surfaces in `docs-only`, `comments-only`, or `full` scope.

## Purpose & Scope

- **Input contract**:
  - `audit_scope=docs-only` for repository markdown documentation audit
  - `audit_scope=comments-only` for standalone inline code documentation audit
  - `audit_scope=full` (default) for markdown docs + inline code docs audit
- **Scope-aware worker activation**:
  - `docs-only` -> ln-611, ln-612, ln-614
  - `comments-only` -> ln-613
  - `full` -> ln-611, ln-612, ln-613, ln-614
- **Responsibility split**:
  - `ln-611`, `ln-612`, `ln-614` audit markdown documentation files using section-first reads
  - `ln-613` audits inline documentation in source code: comments, docstrings, JSDoc/XML docs
  - `ln-613` does NOT judge code architecture, implementation quality, or business correctness beyond comment-to-code consistency
- Detect project type + tech stack ONCE
- Pass shared context to all workers (token-efficient)
- Aggregate worker results into single consolidated report
- Write report to `docs/project/docs_audit.md` (file-based, no task creation)
- Manual invocation by user or maintenance workflows

**MANDATORY READ:** Load `shared/references/audit_runtime_contract.md`, `shared/references/audit_summary_contract.md`, `shared/references/docs_quality_contract.md`, and `shared/references/markdown_read_protocol.md`.

## Runtime Contract

Use `shared/scripts/audit-runtime/cli.mjs` as orchestration SSOT.

Runtime phase map:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVERY`
3. `PHASE_2_BUILD_CONTEXT`
4. `PHASE_3_DELEGATE`
5. `PHASE_4_AGGREGATE`
6. `PHASE_5_CONTEXT_VALIDATION`
7. `PHASE_6_WRITE_REPORT`
8. `PHASE_7_RESULTS_LOG`
9. `PHASE_8_CLEANUP`
10. `PHASE_9_SELF_CHECK`
11. `DONE`
12. `PAUSED`

Runtime artifact layout for this coordinator:
- worker reports: `.hex-skills/runtime-artifacts/runs/{run_id}/audit-report/`
- worker JSON summaries: `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/`
- public report: `docs/project/docs_audit.md`
- public trend log: `docs/project/.audit/results_log.md`

## Workflow

1) **Discovery:** Detect project type, tech stack, scan .md files, and read `docs/project/.context/doc_registry.json` if present
2) **Context Build:** Build contextStore with output_dir, project_root, tech_stack
3) **Prepare Output:** Create output directory
4) **Delegate:** Invoke only workers enabled by `audit_scope`
5) **Aggregate:** Collect worker results, calculate overall score
6) **Context Validation:** Post-filter findings
7) **Write Report:** Save to `docs/project/docs_audit.md`
8) **Results Log:** Append trend row
9) **Cleanup:** Delete worker files

## Phase 1: Discovery

**Load project metadata:**
- `AGENTS.md` - canonical root of the documentation hierarchy when present
- `CLAUDE.md` - optional Anthropic-compatible shim or legacy root in older projects
- `docs/README.md` - documentation index
- Package manifests: `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`
- Existing docs in `docs/project/`

**Extract:**
- Programming language(s)
- Major frameworks/libraries
- List of `.md` files in project (for ln-611 hierarchy check)
- Target documents for semantic audit (for ln-612)
- Doc registry entries when available (for doc kind, role, and canonical routing)

**Target documents for ln-612:**
```
FOR doc IN [AGENTS.md, CLAUDE.md, docs/README.md, docs/documentation_standards.md,
            docs/principles.md, docs/project/*.md]:
  IF doc exists AND doc NOT IN [docs/tasks/*, docs/reference/*, docs/presentation/*]:
    semantic_targets.append(doc)
```

## Phase 2: Build contextStore

```json
{
  "audit_scope": "full|docs-only|comments-only",
  "tech_stack": {"language": "...", "frameworks": [...]},
  "project_root": "...",
  "output_dir": ".hex-skills/runtime-artifacts/runs/{run_id}/audit-report"
}
```

Coordinator also computes per-worker `summaryArtifactPath` values under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/`.

If `docs/project/.context/doc_registry.json` exists, add:

```json
"doc_registry_path": "docs/project/.context/doc_registry.json"
```

## Phase 3: Prepare Output

```bash
mkdir -p {output_dir}
```

Create sibling summary directory before delegation. Runtime artifacts are cleaned up after consolidation (see Phase 9).

## Worker Invocation (MANDATORY)

| Phase | Worker | Context | Condition |
|-------|--------|---------|-----------|
| 4 | ln-611-docs-structure-auditor | Agent -> shared contextStore | `audit_scope in [docs-only, full]` |
| 4 | ln-612-semantic-content-auditor | Agent -> one invocation per semantic target | `audit_scope in [docs-only, full]` |
| 4 | ln-613-code-comments-auditor | Agent -> shared contextStore | `audit_scope in [comments-only, full]` |
| 4 | ln-614-docs-fact-checker | Agent -> shared contextStore | `audit_scope in [docs-only, full]` |

**TodoWrite format (mandatory):**
```
- Discover project metadata (pending)
- Build contextStore (pending)
- Prepare output directory (pending)
- Invoke ln-611-docs-structure-auditor [conditional] (pending)
- Invoke ln-612-semantic-content-auditor for semantic targets [conditional] (pending)
- Invoke ln-613-code-comments-auditor [conditional] (pending)
- Invoke ln-614-docs-fact-checker [conditional] (pending)
- Aggregate worker results (pending)
- Apply context validation (pending)
- Write consolidated report (pending)
- Append results log (pending)
- Cleanup worker files (pending)
```

## Phase 4: Delegate to Workers

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md`.

Active workers in PARALLEL via Agent tool:

| Worker | Invocations | Output |
|--------|-------------|--------|
| ln-611-docs-structure-auditor | 1 | `{output_dir}/ln-611--global.md` |
| ln-612-semantic-content-auditor | N (per target document) | `{output_dir}/ln-612--{doc-slug}.md` |
| ln-613-code-comments-auditor | 1 when `audit_scope in [comments-only, full]` | `{output_dir}/ln-613--global.md` |
| ln-614-docs-fact-checker | 1 | `{output_dir}/ln-614--global.md` |

ln-614 receives only `contextStore` and discovers `.md` files internally. Every worker also receives `summaryArtifactPath`; coordinators consume JSON summaries first and read markdown reports only for findings/evidence.

Managed child runtime sequence for every worker invocation:

1. Compute `identifier`:
   - global workers: `global`
   - ln-612: `slug(doc)`
2. Compute `childRunId = {parent_run_id}--{worker}--{identifier}`.
3. Compute `childSummaryArtifactPath = .hex-skills/runtime-artifacts/runs/{parent_run_id}/audit-worker/{worker}--{identifier}.json`.
4. Start the managed child runtime before delegation.
5. Checkpoint `child_run` metadata before invoking the worker.
6. Invoke the worker with both `--run-id {childRunId}` and `--summary-artifact-path {childSummaryArtifactPath}`.
7. After the worker completes, load `{childSummaryArtifactPath}` and record it with `audit-runtime record-worker-result`.

**Invocation:**
```javascript
// Global workers -> activate by scope:
FOR EACH worker IN active_global_workers:
  identifier = "global"
  childRunId = parent_run_id + "--" + worker + "--" + identifier
  childSummaryArtifactPath = ".hex-skills/runtime-artifacts/runs/" + parent_run_id + "/audit-worker/" + worker + "--" + identifier + ".json"
  node shared/scripts/audit-worker-runtime/cli.mjs start --skill {worker} --identifier {identifier} --manifest-file .hex-skills/audit/{worker}--{identifier}_manifest.json --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}
  node shared/scripts/audit-runtime/cli.mjs checkpoint --run-id {parent_run_id} --phase PHASE_4_DELEGATE --payload '{"child_run":{"worker":"{worker}","identifier":"{identifier}","run_id":"{childRunId}","summary_artifact_path":"{childSummaryArtifactPath}"}}'
  Skill(skill: "{worker}", args: "--run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")
  node shared/scripts/audit-runtime/cli.mjs record-worker-result --run-id {parent_run_id} --payload-file {childSummaryArtifactPath}

// Per-document worker (ln-612) -> N invocations:
FOR EACH doc IN semantic_targets:
  identifier = slug(doc)
  childRunId = parent_run_id + "--ln-612--" + identifier
  childSummaryArtifactPath = ".hex-skills/runtime-artifacts/runs/" + parent_run_id + "/audit-worker/ln-612--" + identifier + ".json"
  node shared/scripts/audit-worker-runtime/cli.mjs start --skill ln-612 --identifier {identifier} --manifest-file .hex-skills/audit/ln-612--{identifier}_manifest.json --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}
  node shared/scripts/audit-runtime/cli.mjs checkpoint --run-id {parent_run_id} --phase PHASE_4_DELEGATE --payload '{"child_run":{"worker":"ln-612","identifier":"{identifier}","run_id":"{childRunId}","summary_artifact_path":"{childSummaryArtifactPath}"}}'
  Skill(skill: "ln-612-semantic-content-auditor", args: "{doc} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")
  node shared/scripts/audit-runtime/cli.mjs record-worker-result --run-id {parent_run_id} --payload-file {childSummaryArtifactPath}
```

## Phase 5: Aggregate Results

**MANDATORY READ:** Load `shared/references/audit_coordinator_aggregation.md`.

Use the shared aggregation pattern for JSON summary parsing, worker report reads, severity rollups, and final report assembly.

Category weights:

| Category | Source | Weight |
|----------|--------|--------|
| Documentation Structure | ln-611 | 25% |
| Semantic Content | ln-612 (avg across docs) | 30% |
| Inline Code Documentation | ln-613 | 20% |
| Fact Accuracy | ln-614 | 25% |

Calculate overall score as the weighted average of the active categories. If `audit_scope` excludes a category, renormalize the remaining weights proportionally.

## Phase 6: Context Validation (Post-Filter)

**MANDATORY READ:** Load `shared/references/context_validation.md`

Apply Rule 1 + documentation-specific inline filters:
```
FOR EACH finding WHERE severity IN (HIGH, MEDIUM):
  # Rule 1: ADR/Planned Override
  IF finding matches ADR -> advisory "[Planned: ADR-XXX]"

  # Doc-specific: Compression context (from ln-611)
  IF Structure finding Cat 3 (Compression):
    - Skip if path in references/ or templates/ (reference docs = naturally large)
    - Skip if filename contains architecture/design/api_spec
    - Skip if tables+lists > 50% of content (already structured)

  # Fact-checker: Example/template path exclusion (from ln-614)
  IF Fact finding (PATH_NOT_FOUND):
    - Path in examples/ or templates/ directory reference -> advisory
    - Path has placeholder pattern (YOUR_*, <project>, {name}) -> remove

  # Fact-checker: Planned feature claims (from ln-614)
  IF Fact finding (ENTITY_NOT_FOUND, ENDPOINT_NOT_FOUND):
    - Entity mentioned in ADR/roadmap as planned -> advisory "[Planned: ADR-XXX]"

  # Fact-checker: Cross-doc contradiction authority (from ln-614)
  IF Fact finding (CROSS_DOC_*_CONFLICT):
    - docs/project/ is authority over docs/reference/ -> report reference doc

  # Comment-specific: Per-category density targets (from ln-613)
  IF Comment finding Cat 2 (Density):
    - test/ or tests/ -> target density 2-10%
    - infra/ or config/ or ci/ -> target density 5-15%
    - business/domain/services -> target density 15-25%
    Recalculate with per-category target.

  # Comment-specific: Complexity context for WHY-not-WHAT (from ln-613)
  IF Comment finding Cat 1 (WHY not WHAT):
    - If file McCabe complexity > 15 -> WHAT comments acceptable
    - If file in domain/ or business/ -> explanatory comments OK

Downgraded findings -> "Advisory Findings" section in report.
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
| Inline Code Documentation | X/10 | ln-613 | N issues |
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

Before moving to results-log and cleanup phases, record the coordinator runtime summary:

```bash
node shared/scripts/audit-runtime/cli.mjs record-summary --run-id {parent_run_id} --payload '{"schema_version":"1.0.0","summary_kind":"audit-coordinator","run_id":"{parent_run_id}","identifier":"{runtime_identifier}","producer_skill":"ln-610","produced_at":"{iso_timestamp}","payload":{"status":"completed","final_result":"AUDIT_COMPLETE","report_path":"docs/project/docs_audit.md","worker_count":{active_worker_count},"issues_total":{issues_total},"severity_counts":{"critical":{critical_count},"high":{high_count},"medium":{medium_count},"low":{low_count}},"warnings":[]}}'
```

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md`.

## Critical Notes

- **Pure coordinator:** Does NOT perform any audit checks directly. ALL auditing delegated to workers.
- **Fix content, not rules:** NEVER modify standards/rules files to make violations pass
- **Section-first reads:** Markdown workers use outline/header/top-sections first, then expand only when needed
- **Fact verification via ln-614:** Dedicated worker extracts and verifies claims across markdown docs
- **ln-613 scope is narrow:** Audit inline documentation quality only; code quality stays in code audit families
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

Delete the run-scoped runtime artifact directory (`.hex-skills/runtime-artifacts/runs/{run_id}/`) after consolidation. The consolidated report and results log already preserve the required audit outputs.

## Definition of Done

- [ ] Project metadata discovered (tech stack, doc list)
- [ ] contextStore built with output_dir = `.hex-skills/runtime-artifacts/runs/{run_id}/audit-report`
- [ ] Output directory created for worker reports
- [ ] All workers required by `audit_scope` invoked and completed
- [ ] Worker reports aggregated: active category scores + overall
- [ ] Context Validation applied to all findings
- [ ] Consolidated report written to `docs/project/docs_audit.md`
- [ ] Results log row appended to `docs/project/.audit/results_log.md`
- [ ] Worker output directory cleaned up after consolidation

## Phase 10: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `review-coordinator` (workers only). Run after all phases complete. Output to chat using the `review-coordinator -> workers only` format.

## Reference Files

- **Context validation rules:** `shared/references/context_validation.md`
- **Task delegation pattern:** `shared/references/task_delegation_pattern.md`
- **Aggregation pattern:** `shared/references/audit_coordinator_aggregation.md`
- **Docs quality contract:** `shared/references/docs_quality_contract.md`

---
**Version:** 5.0.0
**Last Updated:** 2026-03-01
