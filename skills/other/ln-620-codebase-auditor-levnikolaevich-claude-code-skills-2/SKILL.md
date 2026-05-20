---
name: ln-620-codebase-auditor
description: "Coordinates codebase audit across security, build, code quality, dependencies, and architecture. Use when auditing entire codebase."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, mcp__Ref, mcp__context7, Skill, mcp__hex-graph__index_project
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# Codebase Auditor (L2 Coordinator)

Coordinates 9 specialized audit workers to perform comprehensive codebase quality analysis.

## Purpose & Scope

- **Coordinates 9 audit workers** (ln-621 through ln-629) running in parallel
- Research current best practices for detected tech stack via MCP tools ONCE
- Pass shared context to all workers (token-efficient)
- Aggregate worker results into single consolidated report
- Write report to `docs/project/codebase_audit.md` (file-based, no task creation)
- Manual invocation by user; not part of Story pipeline

## Workflow

1) **Discovery:** Load tech_stack.md, principles.md, package manifests, auto-discover Team ID
2) **Worker Applicability:** Determine project type, skip inapplicable workers
3) **Research:** Query MCP tools for current best practices per major dependency ONCE
4) **Domain Discovery:** Detect project domains from folder structure
5) **Delegate:** Two-stage delegation - global workers (5a) + domain-aware workers (5b)
6) **Aggregate:** Collect worker results, group by domain, calculate scores
7) **Write Report:** Save to `docs/project/codebase_audit.md`
8) **Results Log:** Append trend row
9) **Cleanup:** Delete worker files

## Phase 1: Discovery

**Load project metadata:**
- `docs/project/tech_stack.md` - detect tech stack for research
- `docs/principles.md` - project-specific quality principles
- Package manifests: `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`
- Auto-discover Team ID from `docs/tasks/kanban_board.md`
- **Supported projects (hex-graph indexed):** For JavaScript, TypeScript/TSX, Python, C#, and PHP projects, run `index_project` and set `graph_indexed: true` in contextStore. For other languages, continue without graph acceleration.

**Extract metadata only** (not full codebase scan):
- Programming language(s)
- Major frameworks/libraries
- Database system(s)
- Build tools
- Test framework(s)

## Phase 2: Worker Applicability Gate

Determine project type from tech_stack metadata and skip inapplicable workers.

**Project type detection:**

| Project Type | Detection | Skip Workers |
|-------------|-----------|--------------|
| CLI tool | No web framework, has CLI framework (Typer/Click/Commander/cobra/etc.) | ln-627 (health checks), ln-629 (graceful shutdown) |
| Library/SDK | No entry point, only exports | ln-627, ln-629 |
| Script/Lambda | Single entry, <500 LOC | ln-627, ln-628 (concurrency), ln-629 |
| Web Service | Has web framework (Express/FastAPI/ASP.NET/Spring/etc.) | None — all applicable |
| Worker/Queue | Has queue framework (Bull/Celery/etc.) | None |

**Algorithm:**
```
project_type = detect_from_tech_stack(tech_stack, package_manifests)
skipped_workers = APPLICABILITY_TABLE[project_type].skip
applicable_workers = ALL_WORKERS - skipped_workers

FOR EACH skipped IN skipped_workers:
  skipped.score = "N/A"
  skipped.reason = "Not applicable for {project_type} projects"
```

Skipped workers are NOT delegated. They get score "N/A" in report and are excluded from overall score calculation.

## Phase 3: Research Best Practices (ONCE)

**For each major dependency identified in Phase 1:**

1. Use `mcp__Ref__ref_search_documentation` for current best practices
2. Use `mcp__context7__get-library-docs` for up-to-date library documentation
3. Focus areas by technology type:

| Type | Research Focus |
|------|----------------|
| Web Framework | Async patterns, middleware, error handling, request lifecycle |
| ML/AI Libraries | Inference optimization, memory management, batching |
| Database | Connection pooling, transactions, query optimization |
| Containerization | Multi-stage builds, security, layer caching |
| Language Runtime | Idioms, performance patterns, memory management |

**Build contextStore:**
```json
{
  "tech_stack": {...},
  "best_practices": {...},
  "principles": {...},
  "codebase_root": "...",
  "output_dir": "docs/project/.audit/ln-620/{YYYY-MM-DD}"
}
```

## Phase 4: Domain Discovery

**MANDATORY READ:** Load `shared/references/audit_coordinator_domain_mode.md`.

Detect `domain_mode` and `all_domains` using the shared pattern. This coordinator keeps one local rule: shared folders are audited, but grouped separately so they do not distort per-domain scores.

## Phase 5: Delegate to Workers

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md` and `shared/references/audit_worker_core_contract.md`.

### Phase 5.0: Prepare Output Directory

Create `{output_dir}` before delegation. Worker files are cleaned up after consolidation (see Phase 9).

### Phase 5a: Global Workers (PARALLEL)

**Global workers** scan entire codebase (not domain-aware). Each writes report to `{output_dir}/`.

| # | Worker | Priority | What It Audits | Output File |
|---|--------|----------|----------------|-------------|
| 1 | ln-621-security-auditor | CRITICAL | Hardcoded secrets, SQL injection, XSS, insecure deps | `621-security.md` |
| 2 | ln-622-build-auditor | CRITICAL | Compiler/linter errors, deprecations, type errors | `622-build.md` |
| 5 | ln-625-dependencies-auditor | MEDIUM | Outdated packages, unused deps, custom implementations | `625-dependencies.md` |
| 6 | ln-626-dead-code-auditor | LOW | Dead code, unused imports/variables, commented-out code | `626-dead-code.md` |
| 7 | ln-627-observability-auditor | MEDIUM | Structured logging, health checks, metrics, tracing | `627-observability.md` |
| 8 | ln-628-concurrency-auditor | HIGH | Async races, thread safety, TOCTOU, deadlocks, blocking I/O, contention, cross-process races | `628-concurrency.md` |
| 9 | ln-629-lifecycle-auditor | MEDIUM | Bootstrap, graceful shutdown, resource cleanup | `629-lifecycle.md` |

**Invocation (filter by Phase 2 applicability gate):**
```javascript
FOR EACH worker IN applicable_workers:
  Agent(description: "Codebase audit via " + worker,
       prompt: "Execute audit worker.

Step 1: Invoke worker:
  Skill(skill: \"" + worker + "\")

CONTEXT:
" + JSON.stringify(contextStore),
       subagent_type: "general-purpose")
```

### Phase 5b: Domain-Aware Workers (PARALLEL per domain)

**Domain-aware workers** run once per domain. Each writes report with domain suffix.

| # | Worker | Priority | What It Audits | Output File |
|---|--------|----------|----------------|-------------|
| 3 | ln-623-code-principles-auditor | HIGH | DRY/KISS/YAGNI violations, TODO/FIXME, error handling, DI | `623-principles-{domain}.md` |
| 4 | ln-624-code-quality-auditor | MEDIUM | Cyclomatic complexity, O(n²), N+1 queries, magic numbers | `624-quality-{domain}.md` |

**Invocation:**
```javascript
IF domain_mode == "domain-aware":
  FOR EACH domain IN all_domains:
    FOR EACH worker IN [ln-623, ln-624]:
      domain_context = {
        ...contextStore,
        domain_mode: "domain-aware",
        current_domain: { name: domain.name, path: domain.path }
      }
      Agent(description: "Audit " + domain.name + " via " + worker,
           prompt: "Execute audit worker.

Step 1: Invoke worker:
  Skill(skill: \"" + worker + "\")

CONTEXT:
" + JSON.stringify(domain_context),
           subagent_type: "general-purpose")
ELSE:
  FOR EACH worker IN [ln-623, ln-624]:
    Agent(description: "Codebase audit via " + worker,
         prompt: "Execute audit worker.

Step 1: Invoke worker:
  Skill(skill: \"" + worker + "\")

CONTEXT:
" + JSON.stringify(contextStore),
         subagent_type: "general-purpose")
```

All invocations in single message for maximum parallelism.

## Phase 6: Aggregate Results (File-Based)

**MANDATORY READ:** Load `shared/references/audit_coordinator_aggregation.md`.

Use the shared aggregation pattern for output directory checks, return-value parsing, category score tables, severity totals, and domain health summaries.

### Step 6.1: Cross-Domain DRY Analysis (if domain-aware)

Read **only** ln-623 report files to extract `FINDINGS-EXTENDED` JSON block:
```
principle_files = Glob("{output_dir}/623-principles-*.md")
FOR EACH file IN principle_files:
  Read file → extract <!-- FINDINGS-EXTENDED [...] --> JSON
  Filter findings with pattern_signature field

Group by pattern_signature across domains:
  IF same signature in 2+ domains → create Cross-Domain DRY finding:
    severity: HIGH
    principle: "Cross-Domain DRY Violation"
    list all affected domains and locations
    recommendation: "Extract to shared/ module"
```

### Step 6.2: Assemble Findings Sections

Read each worker report file and copy Findings table into corresponding report section:
```
FOR EACH report_file IN Glob("{output_dir}/6*.md"):
  Read file → extract "## Findings" table rows
  Insert into matching category section in final report
```

**Global categories** (Security, Build, etc.) → single Findings table per category.
**Domain-aware categories** → subtables per domain (one per file).

### Step 6.3: Context Validation (Post-Filter)

**MANDATORY READ:** Load `shared/references/context_validation.md`

Apply Rules 1-5 to assembled findings. Uses data already in context:
- ADR list (loaded in Phase 1 from `docs/reference/adrs/` or `docs/decisions/`)
- tech_stack metadata (Phase 1)
- Worker report files (already read in Step 6.2)

```
FOR EACH finding IN assembled_findings WHERE severity IN (HIGH, MEDIUM):
  # Rule 1: ADR/Planned Override
  IF finding matches ADR title/description → advisory "[Planned: ADR-XXX]"

  # Rule 2: Trivial DRY
  IF DRY finding AND duplicated_lines < 5 → remove finding

  # Rule 3: Cohesion (god_classes, long_methods, large_file)
  IF size-based finding:
    Read flagged file ONCE, check 4 cohesion indicators
    IF cohesion >= 3 → advisory "[High cohesion module]"

  # Rule 4: Already-Latest
  IF dependency finding: cross-check ln-622 audit output
    IF latest + 0 CVEs → remove finding

  # Rule 5: Locality/Single-Consumer
  IF DRY/schema finding: Grep import count
    IF import_count == 1 → advisory "[Single consumer, locality correct]"
    IF import_count <= 3 with different API contracts → advisory "[API contract isolation]"

Downgraded findings → "Advisory Findings" section in report.
Recalculate category scores excluding advisory findings from penalty.
```

**Exempt:** Security (ln-621), N+1 queries, CRITICAL build errors, concurrency (ln-628).

## Phase 7: Write Report

**MANDATORY READ:** Load `shared/templates/codebase_audit_template.md` for report format.

Write consolidated report to `docs/project/codebase_audit.md` using template. Fill all sections with aggregated worker data, include Advisory Findings from context validation. Overwrite previous report (each audit is full snapshot).

## Phase 8: Append Results Log

**MANDATORY READ:** Load `shared/references/results_log_pattern.md`

Append one row to `docs/project/.audit/results_log.md` with: Skill=`ln-620`, Metric=`overall_score`, Scale=`0-10`, Score from Phase 7 report. Calculate Delta vs previous `ln-620` row. Create file with header if missing. Rolling window: max 50 entries.

## Critical Rules

- **Worker applicability:** Skip inapplicable workers based on project type (Phase 2); skipped workers get "N/A" score
- **Two-stage delegation:** Global workers + Domain-aware workers (2 × N domains)
- **Domain discovery:** Auto-detect domains from folder structure; fallback to global mode
- **Parallel execution:** All applicable workers (global + domain-aware) run in PARALLEL
- **Single context gathering:** Research best practices ONCE, pass contextStore to all workers
- **Metadata-only loading:** Coordinator loads metadata only; workers load full file contents
- **Domain-grouped output:** Architecture & Code Quality findings grouped by domain
- **File output only:** Write results to codebase_audit.md, no task/story creation
- **Do not audit:** Coordinator orchestrates only; audit logic lives in workers

## Phase 9: Cleanup Worker Files

```bash
rm -rf {output_dir}
```

Delete the dated output directory (`docs/project/.audit/ln-620/{YYYY-MM-DD}/`). The consolidated report and results log already preserve all audit data.

## Definition of Done

- [ ] Project type detected; worker applicability determined; inapplicable workers documented with reason
- [ ] Best practices researched via MCP tools for major dependencies
- [ ] Domain discovery completed (domain_mode determined)
- [ ] contextStore built with tech stack + best practices + domain info + output_dir
- [ ] `docs/project/.audit/ln-620/{YYYY-MM-DD}/` directory created for worker reports
- [ ] Worker output directory cleaned up after consolidation
- [ ] Applicable global workers invoked in PARALLEL; each wrote report to `{output_dir}/`
- [ ] Domain-aware workers invoked in PARALLEL; each wrote report to `{output_dir}/`
- [ ] All workers completed successfully (or reported errors); return values parsed for scores/counts
- [ ] Worker report files verified via Glob (expected count matches actual)
- [ ] Results aggregated from return values (scores) + file reads (findings tables)
- [ ] Domain Health Summary built (if domain_mode="domain-aware")
- [ ] Cross-Domain DRY analysis completed from FINDINGS-EXTENDED blocks (if domain-aware)
- [ ] Context validation applied: ADR matches, cohesion checks, locality, trivial DRY filtered
- [ ] Advisory findings separated from penalty-scored findings
- [ ] Compliance score (X/10) calculated per category + overall (skipped workers + advisory excluded)
- [ ] Executive Summary and Strengths sections included
- [ ] Report written to `docs/project/codebase_audit.md` with Advisory Findings section
- [ ] Sources consulted listed with URLs

## Workers

Worker SKILL.md files contain the detailed audit rules:
- [ln-621-security-auditor](../ln-621-security-auditor/SKILL.md)
- [ln-622-build-auditor](../ln-622-build-auditor/SKILL.md)
- [ln-623-code-principles-auditor](../ln-623-code-principles-auditor/SKILL.md)
- [ln-624-code-quality-auditor](../ln-624-code-quality-auditor/SKILL.md)
- [ln-625-dependencies-auditor](../ln-625-dependencies-auditor/SKILL.md)
- [ln-626-dead-code-auditor](../ln-626-dead-code-auditor/SKILL.md)
- [ln-627-observability-auditor](../ln-627-observability-auditor/SKILL.md)
- [ln-628-concurrency-auditor](../ln-628-concurrency-auditor/SKILL.md)
- [ln-629-lifecycle-auditor](../ln-629-lifecycle-auditor/SKILL.md)

## Phase 10: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `review-coordinator` (workers only). Run after all phases complete. Output to chat using the `review-coordinator — workers only` format.

## Reference Files

- **Orchestrator lifecycle:** `shared/references/orchestrator_pattern.md`
- **Task delegation pattern:** `shared/references/task_delegation_pattern.md`
- **Domain mode pattern:** `shared/references/audit_coordinator_domain_mode.md`
- **Aggregation pattern:** `shared/references/audit_coordinator_aggregation.md`
- **Final report template:** `shared/templates/codebase_audit_template.md`
- Principles: `docs/principles.md`
- Tech stack: `docs/project/tech_stack.md`
- Kanban board: `docs/tasks/kanban_board.md`
- **MANDATORY READ:** `shared/references/research_tool_fallback.md`

---
**Version:** 5.0.0
**Last Updated:** 2025-12-23
