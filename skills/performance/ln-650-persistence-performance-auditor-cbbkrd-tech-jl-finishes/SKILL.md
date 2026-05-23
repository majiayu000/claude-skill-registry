---
name: ln-650-persistence-performance-auditor
description: "Coordinates 3 specialized audit workers (query efficiency, transaction correctness, runtime performance). Researches DB/ORM/async best practices, delegates parallel audits, aggregates results into single Linear task in Epic 0."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, mcp__Ref, mcp__context7, mcp__linear-server, Skill
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Persistence & Performance Auditor (L2 Coordinator)

Coordinates 3 specialized audit workers to perform database efficiency, transaction correctness, and runtime performance analysis.

## Purpose & Scope

- **Coordinates 3 audit workers** (ln-651, ln-652, ln-653) running in parallel
- Research current best practices for detected DB, ORM, async framework via MCP tools ONCE
- Pass shared context to all workers (token-efficient)
- Aggregate worker results into single consolidated report
- Create single task in Linear under Epic 0 with all findings
- Manual invocation by user; not part of Story pipeline
- **Independent from ln-620** (can be run separately or after ln-620)

## Workflow

1) **Discovery:** Load tech_stack.md, package manifests, detect DB/ORM/async framework, auto-discover Team ID
2) **Research:** Query MCP tools for DB/ORM/async best practices ONCE
3) **Build Context:** Create contextStore with best practices + DB-specific metadata
4) **Delegate:** 3 workers in PARALLEL
5) **Aggregate:** Collect worker results, calculate scores
6) **Generate Report:** Build consolidated report
7) **Create Task:** Create Linear task in Epic 0 titled "Persistence & Performance Audit: [YYYY-MM-DD]"

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

**Scan for triggers:**
```
Grep("pg_notify|NOTIFY|CREATE TRIGGER", path="alembic/versions/")
  OR path="migrations/"
→ Store: db_config.triggers = [{table, event, function}]
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
    "triggers": [{"table": "jobs", "event": "UPDATE", "function": "notify_job_events"}],
    "pool_size": 10
  },
  "codebase_root": "/project"
}
```

## Phase 3: Delegate to Workers

> **CRITICAL:** All delegations use Task tool with `subagent_type: "general-purpose"` for context isolation.

**Prompt template:**
```
Task(description: "Audit via ln-65X",
     prompt: "Execute ln-65X-{worker}-auditor. Read skill from ln-65X-{worker}-auditor/SKILL.md. Context: {contextStore}",
     subagent_type: "general-purpose")
```

**Anti-Patterns:**
- ❌ Direct Skill tool invocation without Task wrapper
- ❌ Any execution bypassing subagent context isolation

**Workers (ALL 3 in PARALLEL):**

| # | Worker | Priority | What It Audits |
|---|--------|----------|----------------|
| 1 | ln-651-query-efficiency-auditor | HIGH | Redundant queries, N-UPDATE loops, over-fetching, caching scope |
| 2 | ln-652-transaction-correctness-auditor | HIGH | Commit patterns, trigger interaction, transaction scope, rollback |
| 3 | ln-653-runtime-performance-auditor | MEDIUM | Blocking IO in async, allocations, sync sleep, string concat |

**Invocation (3 workers in PARALLEL):**
```javascript
FOR EACH worker IN [ln-651, ln-652, ln-653]:
  Task(description: "Audit via " + worker,
       prompt: "Execute " + worker + ". Read skill. Context: " + JSON.stringify(contextStore),
       subagent_type: "general-purpose")
```

## Phase 4: Aggregate Results

**Collect results from workers:**
```json
{
  "category": "Query Efficiency",
  "score": 6,
  "total_issues": 8,
  "findings": [...]
}
```

**Aggregation steps:**
1. Merge findings from all 3 workers
2. Calculate overall score: average of 3 category scores
3. Sum severity counts across all workers
4. Sort findings by severity (CRITICAL → HIGH → MEDIUM → LOW)
5. Context Validation (Post-Filter)

**Context Validation:**

**MANDATORY READ:** Load `shared/references/context_validation.md`

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

## Phase 5: Create Linear Task

Create task in Epic 0:
- Title: `Persistence & Performance Audit: [YYYY-MM-DD]`
- Description: Full report from Phase 4 (markdown format)
- Team: Auto-discovered from kanban_board.md
- Epic: 0 (technical debt / refactoring epic)
- Labels: `refactoring`, `performance`, `audit`
- Priority: Based on highest severity findings

## Critical Rules

- **Single context gathering:** Research best practices ONCE, pass contextStore to all workers
- **Parallel execution:** All 3 workers run in PARALLEL
- **Trigger discovery:** Scan migrations for triggers/NOTIFY before delegating (pass to ln-652)
- **Metadata-only loading:** Coordinator loads metadata; workers load full file contents
- **Single task:** Create ONE task with all findings; do not create multiple tasks
- **Do not audit:** Coordinator orchestrates only; audit logic lives in workers

## Definition of Done

- Tech stack discovered (DB type, ORM, async framework)
- DB-specific metadata extracted (triggers, session config, pool settings)
- Best practices researched via MCP tools
- contextStore built and passed to workers
- All 3 workers invoked in PARALLEL and completed
- Results aggregated with severity-sorted findings
- Compliance score calculated per category + overall
- Executive Summary included
- Linear task created in Epic 0 with full report
- Sources consulted listed with URLs

## Workers

- [ln-651-query-efficiency-auditor](../ln-651-query-efficiency-auditor/SKILL.md)
- [ln-652-transaction-correctness-auditor](../ln-652-transaction-correctness-auditor/SKILL.md)
- [ln-653-runtime-performance-auditor](../ln-653-runtime-performance-auditor/SKILL.md)

## Reference Files

- Tech stack: `docs/project/tech_stack.md`
- Kanban board: `docs/tasks/kanban_board.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-04
