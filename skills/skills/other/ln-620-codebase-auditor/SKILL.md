---
name: ln-620-codebase-auditor
description: "Coordinates 9 specialized audit workers (security, build, architecture, code quality, dependencies, dead code, observability, concurrency, lifecycle). Researches best practices, delegates parallel audits, aggregates results into docs/project/codebase_audit.md."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, mcp__Ref, mcp__context7, Skill
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

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

## Phase 1: Discovery

**Load project metadata:**
- `docs/project/tech_stack.md` - detect tech stack for research
- `docs/principles.md` - project-specific quality principles
- Package manifests: `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`
- Auto-discover Team ID from `docs/tasks/kanban_board.md`

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

**Purpose:** Detect project domains from folder structure for domain-aware auditing.

**Algorithm:**

1. **Priority 1: Explicit domain folders**
   - Check for: `src/domains/*/`, `src/features/*/`, `src/modules/*/`
   - Monorepo patterns: `packages/*/`, `libs/*/`, `apps/*/`
   - If found (>1 match) → use these as domains

2. **Priority 2: Top-level src/* folders**
   - List folders: `src/users/`, `src/orders/`, `src/payments/`
   - Exclude infrastructure: `utils`, `shared`, `common`, `lib`, `helpers`, `config`, `types`, `interfaces`, `constants`, `middleware`, `infrastructure`, `core`
   - If remaining >1 → use as domains

3. **Priority 3: Fallback to global mode**
   - If <2 domains detected → `domain_mode = "global"`
   - All workers scan entire codebase (backward-compatible behavior)

**Heuristics for domain detection:**

| Heuristic | Indicator | Example |
|-----------|-----------|---------|
| File count | >5 files in folder | `src/users/` with 12 files |
| Structure | controllers/, services/, models/ present | MVC/Clean Architecture |
| Barrel export | index.ts/index.js exists | Module pattern |
| README | README.md describes domain | Domain documentation |

**Output:**
```json
{
  "domain_mode": "domain-aware",
  "all_domains": [
    {"name": "users", "path": "src/users", "file_count": 45, "is_shared": false},
    {"name": "orders", "path": "src/orders", "file_count": 32, "is_shared": false},
    {"name": "shared", "path": "src/shared", "file_count": 15, "is_shared": true}
  ]
}
```

**Shared folder handling:**
- Folders named `shared`, `common`, `utils`, `lib`, `core` → mark `is_shared: true`
- Shared code audited but grouped separately in report
- Does not affect domain-specific scores

## Phase 5: Delegate to Workers

> **CRITICAL:** All delegations use Task tool with `subagent_type: "general-purpose"` for context isolation.

### Phase 5.0: Prepare Output Directory

Before delegating to workers:
```
1. mkdir -p {output_dir}   # No deletion — date folders preserve history
2. output_dir already set in contextStore (Phase 3)
```

**Prompt template:**
```
Task(description: "Audit via ln-62X",
     prompt: "Execute ln-62X-{worker}-auditor. Read skill from ln-62X-{worker}-auditor/SKILL.md. Context: {contextStore}",
     subagent_type: "general-purpose")
```

**Anti-Patterns:**
- ❌ Direct Skill tool invocation without Task wrapper
- ❌ Any execution bypassing subagent context isolation

**Worker Output Contract (File-Based):**

Workers write full report to `{output_dir}/{worker_id}.md` per `shared/templates/audit_worker_report_template.md`.

Workers return **minimal summary** in-context (~50 tokens):
```
Report written: docs/project/.audit/ln-620/{YYYY-MM-DD}/621-security.md
Score: 7.5/10 | Issues: 5 (C:0 H:2 M:2 L:1)
```

Coordinator extracts score/counts from return values. Full findings stay in files.

**Unified Scoring Formula (all workers):**
```
penalty = (critical × 2.0) + (high × 1.0) + (medium × 0.5) + (low × 0.2)
score = max(0, 10 - penalty)
```

### Phase 5a: Global Workers (PARALLEL)

**Global workers** scan entire codebase (not domain-aware). Each writes report to `{output_dir}/`.

| # | Worker | Priority | What It Audits | Output File |
|---|--------|----------|----------------|-------------|
| 1 | ln-621-security-auditor | CRITICAL | Hardcoded secrets, SQL injection, XSS, insecure deps | `621-security.md` |
| 2 | ln-622-build-auditor | CRITICAL | Compiler/linter errors, deprecations, type errors | `622-build.md` |
| 5 | ln-625-dependencies-auditor | MEDIUM | Outdated packages, unused deps, custom implementations | `625-dependencies.md` |
| 6 | ln-626-dead-code-auditor | LOW | Dead code, unused imports/variables, commented-out code | `626-dead-code.md` |
| 7 | ln-627-observability-auditor | MEDIUM | Structured logging, health checks, metrics, tracing | `627-observability.md` |
| 8 | ln-628-concurrency-auditor | HIGH | Race conditions, async/await, resource contention | `628-concurrency.md` |
| 9 | ln-629-lifecycle-auditor | MEDIUM | Bootstrap, graceful shutdown, resource cleanup | `629-lifecycle.md` |

**Invocation (applicable workers in PARALLEL):**
```javascript
// Filter by Phase 2 applicability gate
applicable_global = [ln-621, ln-622, ln-625, ln-626, ln-627, ln-628, ln-629].filter(w => !skipped_workers.includes(w))

FOR EACH worker IN applicable_global:
  Task(description: "Audit via " + worker,
       prompt: "Execute " + worker + ". Read skill. Context: " + JSON.stringify(contextStore),
       subagent_type: "general-purpose")
```

### Phase 5b: Domain-Aware Workers (PARALLEL per domain)

**Domain-aware workers** run once per domain. Each writes report with domain suffix.

| # | Worker | Priority | What It Audits | Output File |
|---|--------|----------|----------------|-------------|
| 3 | ln-623-code-principles-auditor | HIGH | DRY/KISS/YAGNI violations, TODO/FIXME, error handling, DI | `623-principles-{domain}.md` |
| 4 | ln-624-code-quality-auditor | MEDIUM | Cyclomatic complexity, O(n²), N+1 queries, magic numbers | `624-quality-{domain}.md` |

**Invocation (2 workers × N domains):**
```javascript
IF domain_mode == "domain-aware":
  FOR EACH domain IN all_domains:
    domain_context = {
      ...contextStore,
      domain_mode: "domain-aware",
      current_domain: { name: domain.name, path: domain.path }
    }
    Task(description: "Audit principles " + domain.name + " via ln-623",
         prompt: "Execute ln-623-code-principles-auditor. Read skill. Context: " + JSON.stringify(domain_context),
         subagent_type: "general-purpose")
    Task(description: "Audit quality " + domain.name + " via ln-624",
         prompt: "Execute ln-624-code-quality-auditor. Read skill. Context: " + JSON.stringify(domain_context),
         subagent_type: "general-purpose")
ELSE:
  // Fallback: invoke once for entire codebase (global mode)
  Task(description: "Audit principles via ln-623",
       prompt: "Execute ln-623-code-principles-auditor. Read skill. Context: " + JSON.stringify(contextStore),
       subagent_type: "general-purpose")
  Task(description: "Audit quality via ln-624",
       prompt: "Execute ln-624-code-quality-auditor. Read skill. Context: " + JSON.stringify(contextStore),
       subagent_type: "general-purpose")
```

**Parallelism strategy:**
- Phase 5a: All applicable global workers run in PARALLEL
- Phase 5b: All (2 × N) domain-aware invocations run in PARALLEL
- Example: 3 domains → 6 invocations (ln-623×3 + ln-624×3) in single message

## Phase 6: Aggregate Results (File-Based)

Workers wrote reports to `{output_dir}/` and returned minimal summaries. Aggregation uses **return values for numbers** and **file reads for findings tables**.

### Step 6.1: Parse Return Values

Extract score/counts from worker return strings (already in context, 0 file reads):
```
FOR EACH worker_return IN worker_results:
  Parse: "Score: {score}/10 | Issues: {total} (C:{c} H:{h} M:{m} L:{l})"
  Store: {worker, category, score, counts, report_file}
```

### Step 6.2: Build Compliance Score Table

From parsed return values:
```
FOR EACH category IN 9 categories:
  IF category is domain-aware (Architecture, Quality):
    category_score = average(domain_scores for this category)
  ELSE:
    category_score = worker_score
overall_score = average(all applicable category scores)  // exclude N/A
```

### Step 6.3: Build Severity Summary

From parsed return values:
```
total_critical = sum(worker.counts.critical for all workers)
total_high = sum(worker.counts.high for all workers)
total_medium = sum(worker.counts.medium for all workers)
total_low = sum(worker.counts.low for all workers)
```

### Step 6.4: Build Domain Health Summary (if domain-aware)

From parsed return values of ln-623/ln-624:
```
FOR EACH domain:
  arch_score = ln-623 score for this domain
  quality_score = ln-624 score for this domain
  issues = ln-623 issues + ln-624 issues for this domain
```

### Step 6.5: Cross-Domain DRY Analysis (if domain-aware)

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

### Step 6.6: Assemble Findings Sections

Read each worker report file and copy Findings table into corresponding report section:
```
FOR EACH report_file IN Glob("{output_dir}/6*.md"):
  Read file → extract "## Findings" table rows
  Insert into matching category section in final report
```

**Global categories** (Security, Build, etc.) → single Findings table per category.
**Domain-aware categories** → subtables per domain (one per file).

### Step 6.7: Context Validation (Post-Filter)

**MANDATORY READ:** Load `shared/references/context_validation.md`

Apply Rules 1-5 to assembled findings. Uses data already in context:
- ADR list (loaded in Phase 1 from `docs/reference/adrs/` or `docs/decisions/`)
- tech_stack metadata (Phase 1)
- Worker report files (already read in Step 6.6)

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

## Output Format

**MANDATORY READ:** Load `shared/templates/codebase_audit_template.md` for full report structure.

Report is written to `docs/project/codebase_audit.md` using the template. Key sections:
- Executive Summary, Compliance Score (9 categories), Severity Summary
- Domain Health Summary + Cross-Domain Issues (if domain-aware)
- Strengths, Findings by Category (global + domain-grouped), Recommended Actions
- Sources Consulted

## Phase 7: Write Report

**MANDATORY READ:** Load `shared/templates/codebase_audit_template.md` for report format.

Write consolidated report to `docs/project/codebase_audit.md`:
- Use template structure from codebase_audit_template.md
- Fill all sections with aggregated worker data
- Include "Advisory Findings" section with context-validated downgrades
- Overwrite previous report (each audit is a full snapshot)

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

## Definition of Done

- Project type detected; worker applicability determined; inapplicable workers documented with reason
- Best practices researched via MCP tools for major dependencies
- Domain discovery completed (domain_mode determined)
- contextStore built with tech stack + best practices + domain info + output_dir
- `docs/project/.audit/ln-620/{YYYY-MM-DD}/` directory created (no deletion of previous runs)
- Applicable global workers invoked in PARALLEL; each wrote report to `{output_dir}/`
- Domain-aware workers (2 × N domains) invoked in PARALLEL; each wrote report to `{output_dir}/`
- All workers completed successfully (or reported errors); return values parsed for scores/counts
- Worker report files verified via Glob (expected count matches actual)
- Results aggregated from return values (scores) + file reads (findings tables)
- Domain Health Summary built (if domain_mode="domain-aware")
- Cross-Domain DRY analysis completed from ln-623 FINDINGS-EXTENDED blocks (if domain-aware)
- Context validation (Step 6.7) applied: ADR matches, cohesion checks, locality, trivial DRY filtered
- Advisory findings separated from penalty-scored findings
- Compliance score (X/10) calculated per category + overall (skipped workers + advisory excluded)
- Executive Summary and Strengths sections included
- Report written to `docs/project/codebase_audit.md` with Advisory Findings section
- Sources consulted listed with URLs

## Workers

See individual worker SKILL.md files for detailed audit rules:
- [ln-621-security-auditor](../ln-621-security-auditor/SKILL.md)
- [ln-622-build-auditor](../ln-622-build-auditor/SKILL.md)
- [ln-623-code-principles-auditor](../ln-623-code-principles-auditor/SKILL.md)
- [ln-624-code-quality-auditor](../ln-624-code-quality-auditor/SKILL.md)
- [ln-625-dependencies-auditor](../ln-625-dependencies-auditor/SKILL.md)
- [ln-626-dead-code-auditor](../ln-626-dead-code-auditor/SKILL.md)
- [ln-627-observability-auditor](../ln-627-observability-auditor/SKILL.md)
- [ln-628-concurrency-auditor](../ln-628-concurrency-auditor/SKILL.md)
- [ln-629-lifecycle-auditor](../ln-629-lifecycle-auditor/SKILL.md)

## Reference Files

- **Orchestrator lifecycle:** `shared/references/orchestrator_pattern.md`
- **Task delegation pattern:** `shared/references/task_delegation_pattern.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`
- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Final report template:** `shared/templates/codebase_audit_template.md`
- Principles: `docs/principles.md`
- Tech stack: `docs/project/tech_stack.md`
- Kanban board: `docs/tasks/kanban_board.md`

---
**Version:** 5.0.0
**Last Updated:** 2025-12-23
