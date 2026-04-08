---
name: ln-654-resource-lifecycle-auditor
description: "Checks session scope mismatch, missing cleanup, pool config, error path leaks, resource holding. Use when auditing resource lifecycle."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_references, mcp__hex-graph__trace_paths
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Resource Lifecycle Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing resource acquisition/release patterns, scope mismatches, and connection pool hygiene.

## Purpose & Scope

- Audit **resource lifecycle** (Priority: HIGH)
- Check session/connection scope mismatch, streaming endpoint resource holding, cleanup patterns, pool config
- Write structured findings to file with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Resource Lifecycle category

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with: `tech_stack`, `best_practices`, `db_config` (database type, ORM settings, pool config, session factory), `codebase_root`, `output_dir`.

**Domain-aware:** Supports `domain_mode` + `current_domain`.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

1) **Parse context from contextStore**
   - Extract tech_stack, best_practices, db_config, output_dir
   - Determine scan_path

2) **Detect DI framework**
   - FastAPI `Depends()`, Django middleware, Spring `@Autowired`/`@PersistenceContext`, Express middleware, Go wire/fx

3) **Discover resource infrastructure**
   - Find session/connection factory patterns (`sessionmaker`, `create_engine`, `DataSource`, pool creation)
   - Find DI registration (`Depends()`, `@Inject`, providers, middleware mounting)
   - Find streaming endpoints (SSE, WebSocket, long-poll, streaming response)
   - Map: which endpoints receive which resources via DI

4) **Scan codebase for violations** (6 checks)
   - Trace resource injection -> usage -> release across endpoint lifetime
   - Analyze streaming endpoints for held resources
   - Check error paths for cleanup

5) **Collect findings with severity, location, effort, recommendation**

6) **Calculate score using penalty algorithm**

7) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-654--global.md` in single Write call

8) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Rules (Priority: HIGH)

### 1. Resource Scope Mismatch

**What:** Resource injected via DI lives for entire request/connection scope but is used for only a fraction of it.

**Detection (Python/FastAPI):**
- Step 1 - Find endpoints with DB session dependency:
  - Grep: `async def\s+\w+\(.*Depends\(get_db\)|Depends\(get_session\)|db:\s*AsyncSession|session:\s*AsyncSession`
- Step 2 - Measure session usage span within endpoint body:
  - Count lines between first and last `session\.|db\.|await.*repo` usage
  - Count total lines in endpoint function body
- Step 3 - Flag if `usage_lines / total_lines < 0.2` (session used in <20% of function body)
  - Especially: session used only at function start (auth check, initial load) but function continues with non-DB work

**Detection (Node.js/Express):**
- Middleware injects `req.db` or `req.knex` at request start
- Grep: `app\.use.*pool|app\.use.*knex|app\.use.*prisma` (middleware injection)
- Route handler uses `req.db` only in first 20% of function body

**Detection (Java/Spring):**
- `@Transactional` on method with long non-DB processing
- `EntityManager` injected but used only briefly
- Grep: `@Autowired.*EntityManager|@PersistenceContext` + method body analysis

**Detection (Go):**
- `sql.DB` or `*gorm.DB` passed to handler, used once, then long processing
- Grep: `func.*Handler.*\*sql\.DB|func.*Handler.*\*gorm\.DB`

**Severity:**
- **CRITICAL:** Session scope mismatch in streaming endpoint (SSE, WebSocket) - session held for minutes/hours
- **HIGH:** Session scope mismatch in endpoint with external API calls (session held during network latency)
- **MEDIUM:** Session scope mismatch in endpoint with >50 lines of non-DB processing

**Recommendation:** Extract DB operations into scoped function; acquire session only for the duration needed; use `async with get_session() as session:` block instead of endpoint-level DI injection.

**Effort:** M (refactor DI to scoped acquisition)

### 2. Streaming Endpoint Resource Holding

**What:** SSE, WebSocket, or long-poll endpoint holds DB session/connection for stream duration.

**Detection (Python/FastAPI):**
- Step 1 - Find streaming endpoints:
  - Grep: `StreamingResponse|EventSourceResponse|SSE|async def.*websocket|@app\.websocket`
  - Grep: `yield\s+.*event|yield\s+.*data:|async for.*yield` (SSE generator pattern)
- Step 2 - Check if streaming function/generator has DB session in scope:
  - Session from `Depends()` in endpoint signature -> held for entire stream
  - Session from context manager inside generator -> scoped (OK)
- Step 3 - Analyze session usage inside generator:
  - If session used once at start (auth/permission check) then stream loops without DB -> scope mismatch

**Detection (Node.js):**
- Grep: `res\.write\(|res\.flush\(|Server-Sent Events|new WebSocket|ws\.on\(`
- Check if connection/pool client acquired before stream loop and not released

**Detection (Java/Spring):**
- Grep: `SseEmitter|WebSocketHandler|StreamingResponseBody`
- Check if `@Transactional` wraps streaming method

**Detection (Go):**
- Grep: `Flusher|http\.Flusher|websocket\.Conn`
- Check if `*sql.DB` or transaction held during flush loop

**Severity:**
- **CRITICAL:** DB session/connection held for entire SSE/WebSocket stream duration (pool exhaustion under load)
- **HIGH:** DB connection held during long-poll (>30s timeout)

**Recommendation:** Move auth/permission check BEFORE stream: acquire session, check auth, release session, THEN start streaming. Use separate scoped session for any mid-stream DB access.

**Effort:** M (restructure endpoint to release session before streaming)

### 3. Missing Resource Cleanup Patterns

**What:** Resource acquired without guaranteed cleanup (no try/finally, no context manager, no close()).

**Detection (Python):**
- Grep: `session\s*=\s*Session\(\)|session\s*=\s*sessionmaker|engine\.connect\(\)` NOT inside `with` or `async with`
- Grep: `connection\s*=\s*pool\.acquire\(\)|conn\s*=\s*await.*connect\(\)` NOT followed by `try:.*finally:.*close\(\)`
- Pattern: bare `session = get_session()` without context manager
- Safe patterns to exclude: `async with session_factory() as session:`, `with engine.connect() as conn:`

**Detection (Node.js):**
- Grep: `pool\.connect\(\)|knex\.client\.acquireConnection|\.getConnection\(\)` without corresponding `.release()` or `.end()` in same function
- Grep: `createConnection\(\)` without `.destroy()` in try/finally

**Detection (Java):**
- Grep: `getConnection\(\)|dataSource\.getConnection\(\)` without try-with-resources
- Pattern: `Connection conn = ds.getConnection()` without `try (Connection conn = ...)` syntax

**Detection (Go):**
- Grep: `sql\.Open\(|db\.Begin\(\)` without `defer.*Close\(\)|defer.*Rollback\(\)`
- Pattern: `tx, err := db.Begin()` without `defer tx.Rollback()`

**Severity:**
- **HIGH:** Session/connection acquired without cleanup guarantee (leak on exception)
- **MEDIUM:** File handle or cursor without cleanup in non-critical path

**Exception:** Session acquired and released before streaming/long-poll begins -> skip. NullPool / `pool_size` config documented as serverless design -> skip.

**Recommendation:** Ensure resources are cleaned up on all exit paths (context managers, try-finally, or framework-managed lifecycle).

**Effort:** S (wrap in context manager or add defer)

### 4. Connection Pool Configuration Gaps

**What:** Missing pool health monitoring, no pre-ping, no recycle, no overflow limits.

**Detection (Python/SQLAlchemy):**
- Grep for `create_engine\(|create_async_engine\(`:
  - Missing `pool_pre_ping=True` -> stale connections not detected
  - Missing `pool_recycle` -> connections kept beyond DB server timeout (default: MySQL 8h, PG unlimited)
  - Missing `pool_size` -> uses default 5 (may be too small for production)
  - Missing `max_overflow` -> unbounded overflow under load
  - `pool_size=0` or `NullPool` in web service -> no pooling (anti-pattern)
- Grep for pool event listeners:
  - Missing `@event.listens_for(engine, "invalidate")` -> no visibility into connection invalidation
  - Missing `@event.listens_for(engine, "checkout")` -> no connection checkout monitoring
  - Missing `@event.listens_for(engine, "checkin")` -> no connection return monitoring

**Detection (Node.js):**
- Grep for `createPool\(|new Pool\(`:
  - Missing `min`/`max` configuration
  - Missing `idleTimeoutMillis` or `reapIntervalMillis`
  - Missing connection validation (`validateConnection`, `testOnBorrow`)

**Detection (Java/Spring):**
- Grep: `DataSource|HikariConfig|HikariDataSource`:
  - Missing `leakDetectionThreshold`
  - Missing `maximumPoolSize` (defaults to 10)
  - Missing `connectionTestQuery` or `connectionInitSql`

**Detection (Go):**
- Grep: `sql\.Open\(`:
  - Missing `db.SetMaxOpenConns()`
  - Missing `db.SetMaxIdleConns()`
  - Missing `db.SetConnMaxLifetime()`

**Severity:**
- **HIGH:** No pool_pre_ping AND no pool_recycle (stale connections served silently)
- **HIGH:** No max_overflow limit in web service (unbounded connection creation under load)
- **MEDIUM:** Missing pool event listeners (no visibility into pool health)
- **MEDIUM:** Missing leak detection threshold (Java/HikariCP)
- **LOW:** Pool size at default value (may be adequate for small services)

**Context-dependent exceptions:**
- NullPool is valid for serverless/Lambda
- pool_size=5 may be fine for low-traffic services

**Recommendation:** Configure pool_pre_ping=True, pool_recycle < DB server timeout, appropriate pool_size for expected concurrency, add pool event listeners for monitoring.

**Effort:** S (add config parameters), M (add event listeners/monitoring)

### 5. Unclosed Resources in Error Paths

**What:** Exception/error handling paths that skip resource cleanup.

**Detection (Python):**
- Find `except` blocks containing `raise` or `return` without prior `session.close()`, `conn.close()`, or `cursor.close()`
- Pattern: `except Exception: logger.error(...); raise` (re-raise without cleanup)
- Find generator functions with DB session where GeneratorExit is not handled:
  - Grep: `async def.*yield.*session|def.*yield.*session` without `try:.*finally:.*close\(\)`

**Detection (Node.js):**
- Grep: `catch\s*\(` blocks that `throw` or `return` without releasing connection
- Pattern: `pool.connect().then(client => { ... })` without `.finally(() => client.release())`
- Promise chains without `.finally()` for cleanup

**Detection (Java):**
- Grep: `catch\s*\(` blocks without `finally { conn.close() }` when connection opened in `try`
- Not using try-with-resources for AutoCloseable resources

**Detection (Go):**
- Grep: `if err != nil \{.*return` before `defer` statement for resource cleanup
- Pattern: error check between `Open()` and `defer Close()` that returns without closing

**Severity:**
- **CRITICAL:** Session/connection leak in high-frequency endpoint error path (pool exhaustion)
- **HIGH:** Resource leak in error path of API handler
- **MEDIUM:** Resource leak in error path of background task

**Recommendation:** Use context managers/try-with-resources/defer BEFORE any code that can fail; for generators, add try/finally around yield.

**Effort:** S (restructure acquisition to before-error-path)

### 6. Resource Factory vs Injection Anti-pattern

**What:** Using framework DI to inject short-lived resources into long-lived contexts instead of using factory pattern.

**Detection (Python/FastAPI):**
- Step 1 - Find DI-injected sessions in endpoint signatures:
  - Grep: `Depends\(get_db\)|Depends\(get_session\)|Depends\(get_async_session\)`
- Step 2 - Classify endpoint lifetime:
  - Short-lived: regular REST endpoint (request/response) -> DI injection OK
  - Long-lived: SSE (`StreamingResponse`, `EventSourceResponse`), WebSocket (`@app.websocket`), background task (`BackgroundTasks.add_task`)
- Step 3 - Flag DI injection in long-lived endpoints:
  - Long-lived endpoint should use factory pattern: `async with session_factory() as session:` at point of need
  - NOT `session: AsyncSession = Depends(get_session)` at endpoint level

**Detection (Node.js/Express):**
- Middleware-injected pool connection (`req.db`) used in WebSocket handler or SSE route
- Should use: `const conn = await pool.connect(); try { ... } finally { conn.release() }` at point of need

**Detection (Java/Spring):**
- `@Autowired EntityManager` in `@Controller` with SSE endpoint (`SseEmitter`)
- Should use: programmatic EntityManager creation from EntityManagerFactory

**Detection (Go):**
- `*sql.DB` injected at handler construction time but `*sql.Conn` should be acquired per-operation

**Severity:**
- **CRITICAL:** DI-injected session in SSE/WebSocket endpoint (session outlives intended scope by orders of magnitude)
- **HIGH:** DI-injected session passed to background task (task outlives request)

**Recommendation:** Use factory pattern for long-lived contexts; inject the factory (sessionmaker, pool), not the session/connection itself.

**Effort:** M (change DI from session to session factory, add scoped acquisition)

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-654--global.md` with `category: "Resource Lifecycle"` and checks: resource_scope_mismatch, streaming_resource_holding, missing_cleanup, pool_configuration, error_path_leak, factory_vs_injection.

Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-654--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only
- **DI-aware:** Understand framework dependency injection lifetime scopes (request, singleton, transient)
- **Framework detection first:** Identify DI framework before checking injection patterns
- **Streaming detection first:** Find all streaming/long-lived endpoints before scope analysis
- **Exclude tests:** Do not flag test fixtures, test session setup, mock sessions
- **Exclude CLI/scripts:** DI scope mismatch is not relevant for single-run scripts
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Pool config is context-dependent:** NullPool is valid for serverless/Lambda; pool_size=5 may be fine for low-traffic services
- **Safe pattern awareness:** Do not flag resources inside `async with`, `with`, try-with-resources, `defer` (already managed)

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully (including output_dir, db_config)
- [ ] scan_path determined
- [ ] DI framework detected (FastAPI Depends, Django middleware, Spring @Autowired, Express middleware, Go wire)
- [ ] Streaming endpoints inventoried
- [ ] All 6 checks completed:
  - resource scope mismatch, streaming resource holding, missing cleanup, pool configuration, error path leak, factory vs injection
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated using penalty algorithm
- [ ] Report written to `{output_dir}/ln-654--global.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-03-03
