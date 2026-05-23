---
name: ln-650-persistence-performance-auditor
description: "Coordinates persistence and performance audit across queries, transactions, runtime, and resource lifecycle. Use when auditing data layer performance."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, mcp__Ref, mcp__context7, Skill
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# Persistence & Performance Auditor (L2 Coordinator)

Coordinates 4 specialized audit workers to perform database efficiency, transaction correctness, runtime performance, and resource lifecycle analysis.

## Purpose & Scope

- **Coordinates 4 audit workers** (ln-651, ln-652, ln-653, ln-654) running in parallel
- Research current best practices for detected DB, ORM, async framework via MCP tools ONCE
- Pass shared context to all workers (token-efficient)
- Aggregate worker results into single consolidated report
- Write report to `docs/project/persistence_audit.md` (file-based, no task creation)
- Manual invocation by user; not part of Story pipeline
- **Independent from ln-620** (can be run separately or after ln-620)

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

1) **Discovery:** Load tech_stack.md, package manifests, detect DB/ORM/async framework, auto-discover Team ID
2) **Research:** Query MCP tools for DB/ORM/async best practices ONCE
3) **Build Context:** Create contextStore with best practices + DB-specific metadata
4) **Prepare Output:** Create output directory
5) **Delegate:** 4 workers in PARALLEL
6) **Aggregate:** Collect worker results, calculate scores
7) **Write Report:** Save to `docs/project/persistence_audit.md`
8) **Results Log:** Append trend row
9) **Cleanup:** Delete worker files

## Phase 1: Discovery

**Load project metadata:**
- `docs/project/tech_stack.md` - detect DB, ORM, async framework
- Package manifests: `requirements.txt`, `pyproject.toml`, `package.json`, `go.mod`
- Auto-discover Team ID from `docs/tasks/kanban_board.md`

**Extract DB-specific metadata:**

| Metadata | Source | Example |
|----------|--------|---------|
| Database type | tech_stack.md, docker-compose.yml | PostgreSQL 16 |
| ORM | imports, requirements.txt | SQLAlchemy 2.0 |
| Async framework | imports, requirements.txt | asyncio, FastAPI |
| Session config | grep `create_async_engine`, `sessionmaker` | `expire_on_commit=False` |
| Triggers/NOTIFY | migration files | `pg_notify('job_events', ...)` |
| Connection pooling | engine config | `pool_size=10, max_overflow=20` |

**Scan for triggers and event channels:**
```
Grep("pg_notify|NOTIFY|CREATE TRIGGER", path="alembic/versions/")
  OR path="migrations/"
→ Store: db_config.triggers = [{table, event, function, channel_name}]

Grep("LISTEN\s+\w+|\.subscribe\(|\.on\(.*channel|redis.*subscribe", path="src/")
  OR path="app/"
→ Store: db_config.event_subscribers = [{channel_name, file, line, technology}]
```

## Phase 2: Research Best Practices (ONCE)

**For each detected technology:**

| Technology | Research Focus |
|------------|---------------|
| SQLAlchemy | Session lifecycle, expire_on_commit, bulk operations, eager/lazy loading |
| PostgreSQL | NOTIFY/LISTEN semantics, transaction isolation, batch operations |
| asyncio | to_thread, blocking detection, event loop best practices |
| FastAPI | Dependency injection scopes, background tasks, async endpoints |

**Build contextStore:**
```json
{
  "tech_stack": {"db": "postgresql", "orm": "sqlalchemy", "async": "asyncio"},
  "best_practices": {"sqlalchemy": {...}, "postgresql": {...}, "asyncio": {...}},
  "db_config": {
    "expire_on_commit": false,
    "triggers": [{"table": "jobs", "event": "UPDATE", "function": "notify_job_events", "channel_name": "job_events"}],
    "event_subscribers": [{"channel_name": "job_events", "file": "src/listeners/job_listener.py", "line": 12, "technology": "postgresql"}],
    "pool_size": 10
  },
  "codebase_root": "/project",
  "output_dir": "docs/project/.audit/ln-650/{YYYY-MM-DD}"
}
```

## Phase 3: Prepare Output Directory

```bash
mkdir -p {output_dir}   # Worker files cleaned up after consolidation (Phase 8)
```

## Phase 4: Delegate to Workers

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md` and `shared/references/audit_worker_core_contract.md`.

**Workers (ALL 4 in PARALLEL):**

| # | Worker | Priority | What It Audits |
|---|--------|----------|----------------|
| 1 | ln-651-query-efficiency-auditor | HIGH | Redundant queries, N-UPDATE loops, over-fetching, caching scope |
| 2 | ln-652-transaction-correctness-auditor | HIGH | Commit patterns, trigger interaction, transaction scope, rollback |
| 3 | ln-653-runtime-performance-auditor | MEDIUM | Blocking IO in async, allocations, sync sleep, string concat |
| 4 | ln-654-resource-lifecycle-auditor | HIGH | Session scope mismatch, streaming resource holding, pool config, cleanup |

**Invocation (4 workers in PARALLEL):**
```javascript
FOR EACH worker IN [ln-651, ln-652, ln-653, ln-654]:
  Agent(description: "Audit via " + worker,
       prompt: "Execute audit worker.

Step 1: Invoke worker:
  Skill(skill: \"" + worker + "\")

CONTEXT:
" + JSON.stringify(contextStore),
       subagent_type: "general-purpose")
```

**Worker Output Contract (File-Based):**

Workers follow the shared file-based audit contract, write reports to `{output_dir}/`, and return compact score/severity summaries for aggregation.

Expected summary format:
```text
Report written: docs/project/.audit/ln-650/{YYYY-MM-DD}/651-query-efficiency.md
Score: 6.0/10 | Issues: 8 (C:0 H:3 M:4 L:1)
```

## Phase 5: Aggregate Results (File-Based)

**MANDATORY READ:** Load `shared/references/audit_coordinator_aggregation.md` and `shared/references/context_validation.md`.

Use the shared aggregation pattern for parsing worker summaries, rolling up severity totals, reading worker files, and assembling the final report.

Local rules for this coordinator:
- Overall score = average of 4 category scores.
- Keep findings grouped by the 4 worker categories in the final report.
- Append one results-log row with `Skill=ln-650`, `Metric=overall_score`, `Scale=0-10`.

**Context Validation:**

Apply Rules 1, 6 to merged findings:
```
FOR EACH finding WHERE severity IN (HIGH, MEDIUM):
  # Rule 1: ADR/Planned Override
  IF finding matches ADR → advisory "[Planned: ADR-XXX]"

  # Rule 6: Execution Context
  IF finding.check IN (blocking_io, redundant_fetch, transaction_wide, cpu_bound):
    context = 0
    - Function in __init__/setup/bootstrap/migrate → context += 1
    - File in tasks/jobs/cron/                      → context += 1
    - Has timeout/safeguard nearby                  → context += 1
    - Small data (<100KB file, <100 items dataset)  → context += 1
    IF context >= 3 → advisory
    IF context >= 1 → severity -= 1

Downgraded findings → "Advisory Findings" section in report.
Recalculate overall score excluding advisory findings from penalty.
```

**Exempt:** Missing rollback CRITICAL, N-UPDATE loops in hot paths.

## Output Format

```markdown
## Persistence & Performance Audit Report - [DATE]

### Executive Summary
[2-3 sentences on overall persistence/performance health]

### Compliance Score

| Category | Score | Notes |
|----------|-------|-------|
| Query Efficiency | X/10 | ... |
| Transaction Correctness | X/10 | ... |
| Runtime Performance | X/10 | ... |
| Resource Lifecycle | X/10 | ... |
| **Overall** | **X/10** | |

### Severity Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |

### Findings by Category

#### 1. Query Efficiency

| Severity | Location | Issue | Recommendation | Effort |
|----------|----------|-------|----------------|--------|
| HIGH | job_processor.py:434 | Redundant entity fetch | Pass object not ID | S |

#### 2. Transaction Correctness

| Severity | Location | Issue | Recommendation | Effort |
|----------|----------|-------|----------------|--------|
| CRITICAL | job_processor.py:412 | Missing intermediate commits | Add commit at milestones | S |

#### 3. Runtime Performance

| Severity | Location | Issue | Recommendation | Effort |
|----------|----------|-------|----------------|--------|
| HIGH | job_processor.py:444 | Blocking read_bytes() in async | Use aiofiles/to_thread | S |

#### 4. Resource Lifecycle

| Severity | Location | Issue | Recommendation | Effort |
|----------|----------|-------|----------------|--------|
| CRITICAL | sse_stream.py:112 | DbSession held for entire SSE stream | Scope session to auth check only | M |

### Recommended Actions (Priority-Sorted)

| Priority | Category | Location | Issue | Recommendation | Effort |
|----------|----------|----------|-------|----------------|--------|
| CRITICAL | Transaction | ... | Missing commits | Add strategic commits | S |
| HIGH | Query | ... | Redundant fetch | Pass object not ID | S |

### Sources Consulted
- SQLAlchemy best practices: [URL]
- PostgreSQL NOTIFY docs: [URL]
- Python asyncio-dev: [URL]
```

## Phase 6: Write Report

Write consolidated report to `docs/project/persistence_audit.md` with the Output Format above.

## Phase 7: Append Results Log

**MANDATORY READ:** Load `shared/references/results_log_pattern.md`

Append one row to `docs/project/.audit/results_log.md` with: Skill=`ln-650`, Metric=`overall_score`, Scale=`0-10`, Score from Phase 6 report. Calculate Delta vs previous `ln-650` row. Create file with header if missing. Rolling window: max 50 entries.

## Critical Rules

- **Single context gathering:** Research best practices ONCE, pass contextStore to all workers
- **Parallel execution:** All 4 workers run in PARALLEL
- **Trigger discovery:** Scan migrations for triggers/NOTIFY before delegating (pass to ln-652)
- **Metadata-only loading:** Coordinator loads metadata; workers load full file contents
- **Do not audit:** Coordinator orchestrates only; audit logic lives in workers

## Phase 8: Cleanup Worker Files

```bash
rm -rf {output_dir}
```

Delete the dated output directory (`docs/project/.audit/ln-650/{YYYY-MM-DD}/`). The consolidated report and results log already preserve all audit data.

## Definition of Done

- [ ] Tech stack discovered (DB type, ORM, async framework)
- [ ] DB-specific metadata extracted (triggers, session config, pool settings)
- [ ] Best practices researched via MCP tools
- [ ] contextStore built with output_dir = `docs/project/.audit/ln-650/{YYYY-MM-DD}`
- [ ] Output directory created for worker reports
- [ ] All 4 workers invoked in PARALLEL and completed; each wrote report to `{output_dir}/`
- [ ] Results aggregated from return values (scores) + file reads (findings tables)
- [ ] Compliance score calculated per category + overall
- [ ] Executive Summary included
- [ ] Report written to `docs/project/persistence_audit.md`
- [ ] Sources consulted listed with URLs
- [ ] Worker output directory cleaned up after consolidation

## Workers

- [ln-651-query-efficiency-auditor](../ln-651-query-efficiency-auditor/SKILL.md)
- [ln-652-transaction-correctness-auditor](../ln-652-transaction-correctness-auditor/SKILL.md)
- [ln-653-runtime-performance-auditor](../ln-653-runtime-performance-auditor/SKILL.md)
- [ln-654-resource-lifecycle-auditor](../ln-654-resource-lifecycle-auditor/SKILL.md)

## Phase 9: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `review-coordinator` (workers only). Run after all phases complete. Output to chat using the `review-coordinator — workers only` format.

## Reference Files

- Tech stack: `docs/project/tech_stack.md`
- Kanban board: `docs/tasks/kanban_board.md`
- **Task delegation pattern:** `shared/references/task_delegation_pattern.md`
- **Aggregation pattern:** `shared/references/audit_coordinator_aggregation.md`
- **MANDATORY READ:** `shared/references/research_tool_fallback.md`

---
**Version:** 1.1.0
**Last Updated:** 2026-03-15
