---
name: ln-652-transaction-correctness-auditor
description: "Checks transaction scope, missing rollback handling, long-held transactions, trigger/notify interaction. Use when auditing transaction correctness."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__find_references, mcp__hex-graph__trace_paths
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Transaction Correctness Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing database transaction patterns for correctness, scope, and trigger interaction.

## Purpose & Scope

- Audit **transaction correctness** (Priority: HIGH)
- Check commit patterns, transaction boundaries, rollback handling, trigger/notify semantics
- Write structured findings to file with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Transaction Correctness category

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with: `tech_stack`, `best_practices`, `db_config` (database type, ORM settings, trigger/notify patterns), `codebase_root`, `output_dir`.

**Domain-aware:** Supports `domain_mode` + `current_domain`.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

1) **Parse context from contextStore**
   - Extract tech_stack, best_practices, db_config, output_dir
   - Determine scan_path

2) **Discover transaction infrastructure**
   - Find migration files with triggers (`pg_notify`, `CREATE TRIGGER`, `NOTIFY`)
   - Find session/transaction configuration (`expire_on_commit`, `autocommit`, isolation level)
   - Map trigger-affected tables

3) **Scan codebase for violations**
   - Trace UPDATE paths for trigger-affected tables
   - Analyze transaction boundaries (begin/commit scope)
   - Check error handling around commits

4) **Collect findings with severity, location, effort, recommendation**

5) **Calculate score using penalty algorithm**

6) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-652--global.md` in single Write call

7) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Rules (Priority: HIGH)

### 1. Missing Intermediate Commits
**What:** UPDATE without commit when DB trigger/NOTIFY depends on transaction commit

**Detection:**
- **Step 1:** Find triggers in migrations:
  - Grep for `pg_notify|NOTIFY|CREATE TRIGGER|CREATE OR REPLACE FUNCTION.*trigger` in `alembic/versions/`, `migrations/`
  - Extract: trigger function name, table name, trigger event (INSERT/UPDATE)
- **Step 2:** Find code that UPDATEs trigger-affected tables:
  - Grep for `repo.*update|session\.execute.*update|\.progress|\.status` related to trigger tables
- **Step 3:** Check for `commit()` between sequential updates:
  - If multiple UPDATEs to trigger table occur in a loop/sequence without intermediate `commit()`, NOTIFY events are deferred until final commit
  - Real-time progress tracking breaks without intermediate commits

**Severity:**
- **CRITICAL:** Missing commit for NOTIFY/LISTEN-based real-time features (SSE, WebSocket)
- **HIGH:** Missing commit for triggers that update materialized data

**Exception:** Single atomic operation with no intermediate observable state -> downgrade CRITICAL to MEDIUM. Transaction scope documented as intentional (ADR, architecture comment) -> downgrade one level

**Recommendation:**
- Add `session.commit()` at progress milestones (throttled: every N%, every T seconds)
- Or move real-time notifications out of DB triggers (Redis pub/sub, in-process events)

**Effort:** S-M (add strategic commits or redesign notification path)

### 2. Transaction Scope Too Wide
**What:** Single transaction wraps unrelated operations, including slow external calls

**Detection:**
- Find `async with session.begin()` or explicit transaction blocks
- Check if block contains external calls: `await httpx.`, `await aiohttp.`, `await requests.`, `await grpc.`
- Check if block contains file I/O: `open(`, `.read(`, `.write(`
- Pattern: DB write + external API call + another DB write in same transaction

**Severity:**
- **HIGH:** External HTTP/gRPC call inside transaction (holds DB connection during network latency)
- **MEDIUM:** File I/O inside transaction

**Recommendation:** Split into separate transactions; use Saga/Outbox pattern for cross-service consistency

**Effort:** M-L (restructure transaction boundaries)

### 3. Transaction Scope Too Narrow
**What:** Logically atomic operations split across multiple commits

**Detection:**
- Multiple `session.commit()` calls for operations that should be atomic
- Pattern: create parent entity, commit, create child entities, commit (should be single transaction)
- Pattern: update status + create audit log in separate commits

**Severity:**
- **HIGH:** Parent-child creation in separate commits (orphan risk on failure)
- **MEDIUM:** Related updates in separate commits (inconsistent state on failure)

**Recommendation:** Wrap related operations in single transaction using `async with session.begin()` or unit-of-work pattern

**Effort:** M (restructure commit boundaries)

### 4. Missing Rollback Handling
**What:** `session.commit()` without proper error handling and rollback

**Detection:**
- Find `session.commit()` not inside `try/except` block or context manager
- Find `session.commit()` in `try` without `session.rollback()` in `except`
- Pattern: bare `await session.commit()` in service methods
- Exception: `async with session.begin()` auto-rollbacks (safe)

**Severity:**
- **MEDIUM:** Missing rollback (session left in broken state on failure)
- **LOW:** Missing explicit rollback when using context manager (auto-handled)

**Recommendation:** Use `async with session.begin()` (auto-rollback), or add explicit `try/except/rollback` pattern

**Effort:** S (wrap in context manager or add error handling)

### 5. Long-Held Transaction
**What:** Transaction open during slow/blocking operations

**Detection:**
- Measure scope: count lines between transaction start and commit
- Flag if >50 lines of code between `begin()` and `commit()`
- Flag if transaction contains `await` calls to external services (network latency)
- Flag if transaction contains `time.sleep()` or `asyncio.sleep()`

**Severity:**
- **HIGH:** Transaction held during external API call (connection pool exhaustion risk)
- **MEDIUM:** Transaction spans >50 lines (complex logic, high chance of lock contention)

**Recommendation:** Minimize transaction scope; prepare data before opening transaction, commit immediately after DB operations

**Effort:** M (restructure code to minimize transaction window)

### 6. Event Channel Name Consistency
**What:** Publisher channel/topic name does not match subscriber channel/topic name

**Detection:**
- **Step 1:** Collect publisher channel names (extend Phase 2 trigger discovery):
  - Migration triggers: extract string argument from `pg_notify('channel_name', ...)`, `NOTIFY channel_name`
  - Application code: Grep for `\.publish\(["']|\.emit\(["']|redis.*publish\(["']|\.send_to\(["']` in `src/`, `app/`
  - Extract: `{channel_name, source_file, source_line, technology}`
- **Step 2:** Collect subscriber channel names:
  - PostgreSQL: Grep for `LISTEN\s+(\w+)` in application code (not just migrations)
  - Redis: Grep for `\.subscribe\(["']([^"']+)` in `src/`, `app/`
  - EventEmitter/WebSocket: Grep for `\.on\(["']([^"']+)` in handler/listener directories
  - Extract: `{channel_name, source_file, source_line, technology}`
- **Step 3:** Cross-reference publishers vs subscribers:
  - Exact match: `publisher.channel_name == subscriber.channel_name` -> OK
  - Near-miss: Levenshtein distance <= 2 OR one is substring of the other -> flag as MISMATCH
  - Orphaned publisher: channel exists in publishers but not in subscribers -> flag as ORPHAN
  - Orphaned subscriber: channel exists in subscribers but not in publishers -> flag as ORPHAN

**Layer 2 Context Analysis (MANDATORY):**
- If channel name comes from shared config constant or env var (e.g., `CHANNEL = os.environ["EVENT_CHANNEL"]`) and both publisher and subscriber use same source -> NOT a mismatch
- If channel uses dynamic suffix pattern (e.g., `job_events:{job_id}`) and both sides use same template -> NOT orphaned
- Exclude test files (`**/test*/**`, `**/*.test.*`) from both publisher and subscriber discovery

**Severity:**
- **CRITICAL:** Channel name mismatch (near-miss: publisher sends to `job_events`, subscriber listens on `job_event`)
- **HIGH:** Orphaned publisher -- events sent but never consumed (data loss risk if events carry state changes)
- **MEDIUM:** Orphaned subscriber -- listener registered but no publisher found (dead code or future feature)

**Recommendation:**
- For mismatches: unify channel name to a single constant shared between publisher and subscriber
- For orphaned publishers: add subscriber or remove unused NOTIFY/publish
- For orphaned subscribers: add publisher or remove dead listener

**Effort:** S (fix typo/add constant) to M (design missing subscriber/publisher)

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-652--global.md` with `category: "Transaction Correctness"` and checks: missing_intermediate_commits, scope_too_wide, scope_too_narrow, missing_rollback, long_held_transaction, event_channel_consistency.

Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-652--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only
- **Trigger discovery first:** Always scan migrations for triggers/NOTIFY before analyzing transaction patterns
- **ORM-aware:** Check if ORM context manager auto-rollbacks (`async with session.begin()` is safe)
- **Exclude test transactions:** Do not flag test fixtures with manual commit/rollback
- **Database-specific:** PostgreSQL NOTIFY semantics differ from MySQL event scheduler

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully (including output_dir)
- [ ] scan_path determined
- [ ] Trigger/NOTIFY infrastructure discovered from migrations
- [ ] All 6 checks completed:
  - missing intermediate commits, scope too wide, scope too narrow, missing rollback, long-held, event channel consistency
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated using penalty algorithm
- [ ] Report written to `{output_dir}/ln-652--global.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 1.1.0
**Last Updated:** 2026-03-15
