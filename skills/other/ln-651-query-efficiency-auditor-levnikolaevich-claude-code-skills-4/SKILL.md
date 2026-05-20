---
name: ln-651-query-efficiency-auditor
description: "Query efficiency audit worker (L3). Checks redundant entity fetches, N-UPDATE/DELETE loops, unnecessary resolves, over-fetching, missing bulk operations, wrong caching scope. Returns findings with severity, location, effort, recommendations."
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Query Efficiency Auditor (L3 Worker)

Specialized worker auditing database query patterns for redundancy, inefficiency, and misuse.

## Purpose & Scope

- **Worker in ln-650 coordinator pipeline** - invoked by ln-650-persistence-performance-auditor
- Audit **query efficiency** (Priority: HIGH)
- Check redundant fetches, batch operation misuse, caching scope problems
- Write structured findings to file with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Query Efficiency category

## Inputs (from Coordinator)

**MANDATORY READ:** Load `shared/references/task_delegation_pattern.md#audit-coordinator--worker-contract` for contextStore structure.

Receives `contextStore` with: `tech_stack`, `best_practices`, `db_config` (database type, ORM settings), `codebase_root`, `output_dir`.

**Domain-aware:** Supports `domain_mode` + `current_domain`.

## Workflow

1) **Parse context from contextStore**
   - Extract tech_stack, best_practices, db_config, output_dir
   - Determine scan_path (same logic as ln-624)

2) **Scan codebase for violations**
   - All Grep/Glob patterns use `scan_path`
   - Trace call chains for redundant fetches (requires reading caller + callee)

3) **Collect findings with severity, location, effort, recommendation**

4) **Calculate score using penalty algorithm**

5) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/651-query-efficiency.md` in single Write call

6) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Rules (Priority: HIGH)

### 1. Redundant Entity Fetch
**What:** Same entity fetched from DB twice in a call chain

**Detection:**
- Find function A that calls `repo.get(id)` or `session.get(Model, id)`, then passes `id` (not object) to function B
- Function B also calls `repo.get(id)` or `session.get(Model, id)` for the same entity
- Common pattern: `acquire_next_pending()` returns job, but `_process_job(job_id)` re-fetches it

**Detection patterns (Python/SQLAlchemy):**
- Grep for `repo.*get_by_id|session\.get\(|session\.query.*filter.*id` in service/handler files
- Trace: if function receives `entity_id: int/UUID` AND internally does `repo.get(entity_id)`, check if caller already has entity object
- Check `expire_on_commit` setting: if `False`, objects remain valid after commit

**Severity:**
- **HIGH:** Redundant fetch in API request handler (adds latency per request)
- **MEDIUM:** Redundant fetch in background job (less critical)

**Recommendation:** Pass entity object instead of ID, or remove second fetch when `expire_on_commit=False`

**Effort:** S (change signature to accept object instead of ID)

### 2. N-UPDATE/DELETE Loop
**What:** Loop of individual UPDATE/DELETE operations instead of single batch query

**Detection:**
- Pattern: `for item in items: await repo.update(item.id, ...)` or `for item in items: await repo.delete(item.id)`
- Pattern: `for item in items: session.execute(update(Model).where(...))`

**Detection patterns:**
- Grep for `for .* in .*:` followed by `repo\.(update|delete|reset|save|mark_)` within 1-3 lines
- Grep for `for .* in .*:` followed by `session\.execute\(.*update\(` within 1-3 lines

**Severity:**
- **HIGH:** Loop over >10 items (N separate round-trips to DB)
- **MEDIUM:** Loop over <=10 items

**Recommendation:** Replace with single `UPDATE ... WHERE id IN (...)` or `session.execute(update(Model).where(Model.id.in_(ids)))`

**Effort:** M (rewrite query + test)

### 3. Unnecessary Resolve
**What:** Re-resolving a value from DB when it is already available in the caller's scope

**Detection:**
- Method receives `profile_id` and resolves engine from it, but caller already determined `engine`
- Method receives `lang_code` and looks up dialect_id, but caller already has both `lang` and `dialect`
- Pattern: function receives `X_id`, does `get(X_id)`, extracts `.field`, when caller already has `field`

**Severity:**
- **MEDIUM:** Extra DB query per invocation, especially in high-frequency paths

**Recommendation:** Split method into two variants: `with_known_value(value, ...)` and `resolving_value(id, ...)`; or pass resolved value directly

**Effort:** S-M (refactor signature, update callers)

### 4. Over-Fetching
**What:** Loading full ORM model when only few fields are needed

**Detection:**
- `session.query(Model)` or `select(Model)` without `.options(load_only(...))` for models with >10 columns
- Especially in list/search endpoints that return many rows
- Pattern: loading full entity but only using 2-3 fields

**Severity:**
- **MEDIUM:** Large models (>15 columns) in list endpoints
- **LOW:** Small models (<10 columns) or single-entity endpoints

**Recommendation:** Use `load_only()`, `defer()`, or raw `select(Model.col1, Model.col2)` for list queries

**Effort:** S (add load_only to query)

### 5. Missing Bulk Operations
**What:** Sequential INSERT/DELETE/UPDATE instead of bulk operations

**Detection:**
- `for item in items: session.add(item)` instead of `session.add_all(items)`
- `for item in items: session.delete(item)` instead of bulk delete
- Pattern: loop with single `INSERT` per iteration

**Severity:**
- **MEDIUM:** Any sequential add/delete in loop (missed batch optimization)

**Recommendation:** Use `session.add_all()`, `session.execute(insert(Model).values(list_of_dicts))`, `bulk_save_objects()`

**Effort:** S (replace loop with bulk call)

### 6. Wrong Caching Scope
**What:** Request-scoped cache for data that rarely changes (should be app-scoped)

**Detection:**
- Service registered as request-scoped (e.g., via FastAPI `Depends()`) with internal cache (`_cache` dict, `_loaded` flag)
- Cache populated by expensive query (JOINs, aggregations) per each request
- Data TTL >> request duration (e.g., engine configurations, language lists, feature flags)

**Detection patterns:**
- Find classes with `_cache`, `_loaded`, `_initialized` attributes
- Check if class is created per-request (via DI registration scope)
- Compare: data change frequency vs cache lifetime

**Severity:**
- **HIGH:** Expensive query (JOINs, subqueries) cached only per-request
- **MEDIUM:** Simple query cached per-request

**Recommendation:** Move cache to app-scoped service (singleton), add TTL-based invalidation, or use CacheService with configurable TTL

**Effort:** M (change DI scope, add TTL logic)

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/651-query-efficiency.md` with `category: "Query Efficiency"` and checks: redundant_fetch, n_update_delete_loop, unnecessary_resolve, over_fetching, missing_bulk_ops, wrong_caching_scope.

Return summary to coordinator:
```
Report written: docs/project/.audit/ln-650/{YYYY-MM-DD}/651-query-efficiency.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

- **Do not auto-fix:** Report only
- **Trace call chains:** Rules 1 and 3 require reading both caller and callee
- **ORM-aware:** Check `expire_on_commit`, `autoflush`, session scope before flagging redundant fetches
- **Context-aware:** Small datasets or infrequent operations may justify simpler code
- **Exclude tests:** Do not flag test fixtures or setup code

## Definition of Done

- contextStore parsed successfully (including output_dir)
- scan_path determined (domain path or codebase root)
- All 6 checks completed:
  - redundant fetch, N-UPDATE loop, unnecessary resolve, over-fetching, bulk ops, caching scope
- Findings collected with severity, location, effort, recommendation
- Score calculated using penalty algorithm
- Report written to `{output_dir}/651-query-efficiency.md` (atomic single Write call)
- Summary returned to coordinator

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-04
