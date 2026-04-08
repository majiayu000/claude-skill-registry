---
name: ln-653-runtime-performance-auditor
description: "Checks blocking IO in async, unnecessary allocations, sync sleep, string concat in loops, redundant copies. Use when auditing runtime performance."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__audit_workspace
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Runtime Performance Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing runtime performance anti-patterns in async and general code.

## Purpose & Scope

- Audit **runtime performance** (Priority: MEDIUM)
- Check async anti-patterns, unnecessary allocations, blocking operations
- Write structured findings to file with severity, location, effort, recommendations
- Calculate compliance score (X/10) for Runtime Performance category

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with: `tech_stack`, `best_practices`, `codebase_root`, `output_dir`.

**Domain-aware:** Supports `domain_mode` + `current_domain`.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

1) **Parse context from contextStore**
   - Extract tech_stack, best_practices, output_dir
   - Determine scan_path
   - Detect async framework: asyncio (Python), Node.js async, Tokio (Rust)

2) **Scan codebase for violations**
   - Grep patterns scoped to `scan_path`
   - For Rules 1, 3, 5: detect `async def` blocks first, then check for violations inside them

3) **Collect findings with severity, location, effort, recommendation**

4) **Calculate score using penalty algorithm**

5) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/ln-653--global.md` in single Write call

6) **Return Summary:** Return minimal summary to coordinator (see Output Format)

## Audit Rules (Priority: MEDIUM)

### 1. Blocking IO in Async
**What:** Synchronous file/network operations inside async functions, blocking event loop

**Detection (Python):**
- Find `async def` functions
- Inside them, grep for blocking calls:
  - File: `open(`, `.read_bytes()`, `.read_text()`, `.write_bytes()`, `.write_text()`, `Path(...).(read|write)`
  - Network: `requests.get`, `requests.post`, `urllib.request`
  - Subprocess: `subprocess.run(`, `subprocess.call(`
- Exclude: calls wrapped in `await asyncio.to_thread(...)` or `await loop.run_in_executor(...)`

**Detection (Node.js):**
- Inside `async function` or arrow async, grep for `fs.readFileSync`, `fs.writeFileSync`, `child_process.execSync`

**Severity:**
- **HIGH:** Blocking IO in API request handler (blocks entire event loop)
- **MEDIUM:** Blocking IO in background task/worker
- **Downgrade when:** Blocking IO in `__init__`/setup/bootstrap (not request path) -> LOW. Small file (<1KB) read in non-hot path -> skip

**Recommendation:** Use `aiofiles`, `asyncio.to_thread()`, or `loop.run_in_executor()` for file operations; use `httpx.AsyncClient` instead of `requests`

**Effort:** S (wrap in to_thread or switch to async library)

### 2. Unnecessary List Allocation
**What:** List comprehension where generator expression suffices

**Detection:**
- `len([x for x in ...])` - allocates list just to count; use `sum(1 for ...)`
- `any([x for x in ...])` - allocates list for short-circuit check; use `any(x for ...)`
- `all([x for x in ...])` - same pattern; use `all(x for ...)`
- `set([x for x in ...])` - use set comprehension `{x for x in ...}`
- `"".join([x for x in ...])` - use generator directly `"".join(x for x in ...)`

**Severity:**
- **MEDIUM:** Unnecessary allocation in hot path (API handler, loop)
- **LOW:** Unnecessary allocation in infrequent code

**Recommendation:** Replace `[...]` with generator `(...)` or set comprehension `{...}`

**Effort:** S (syntax change only)

### 3. Sync Sleep in Async
**What:** `time.sleep()` inside async function blocks event loop

**Detection:**
- Grep for `time\.sleep` inside `async def` blocks
- Pattern: `await some_async_call()` ... `time.sleep(N)` ... `await another_call()`

**Severity:**
- **HIGH:** `time.sleep()` in async API handler (freezes all concurrent requests)
- **MEDIUM:** `time.sleep()` in async background task
- **Downgrade when:** `time.sleep` in CLI/script (not async server) -> skip

**Recommendation:** Replace with `await asyncio.sleep(N)`

**Effort:** S (one-line change)

### 4. String Concatenation in Loop
**What:** Building string via `+=` inside loop (O(n^2) for large strings)

**Detection:**
- Pattern: variable `result`, `output`, `html`, `text` with `+=` inside `for`/`while` loop
- Grep for: variable followed by `+=` containing string operand inside loop body

**Severity:**
- **MEDIUM:** String concat in loop processing large data (>100 iterations)
- **LOW:** String concat in loop with small iterations (<100)

**Recommendation:** Use `list.append()` + `"".join()`, or `io.StringIO`, or f-string with `"".join(generator)`

**Effort:** S (refactor to list + join)

### 5. Missing `to_thread` for CPU-Bound
**What:** CPU-intensive synchronous code in async handler without offloading to thread

**Detection:**
- Inside `async def`, find CPU-intensive operations:
  - JSON parsing large files: `json.loads(large_data)`, `json.load(file)`
  - Image processing: `PIL.Image.open`, `cv2.imread`
  - Crypto: `hashlib`, `bcrypt.hashpw`
  - XML/HTML parsing: `lxml.etree.parse`, `BeautifulSoup(`
  - Large data transformation without await points
- Exclude: operations already wrapped in `asyncio.to_thread()` or executor

**Severity:**
- **MEDIUM:** CPU-bound operation in async handler (blocks event loop proportionally to data size)

**Recommendation:** Wrap in `await asyncio.to_thread(func, *args)` (Python 3.9+) or `loop.run_in_executor(None, func, *args)`

**Effort:** S (wrap in to_thread)

### 6. Redundant Data Copies
**What:** Unnecessary `.copy()`, `list()`, `dict()` when data is only read, not mutated

**Detection:**
- `data = list(items)` where `data` is only iterated (never modified)
- `config = config_dict.copy()` where `config` is only read
- `result = dict(original)` where `result` is returned without modification

**Severity:**
- **LOW:** Redundant copy in most contexts (minor memory overhead)
- **MEDIUM:** Redundant copy of large data in hot path

**Recommendation:** Remove unnecessary copy; pass original if not mutated

**Effort:** S (remove copy call)

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-653--global.md` with `category: "Runtime Performance"` and checks: blocking_io_in_async, unnecessary_list_allocation, sync_sleep_in_async, string_concat_in_loop, missing_to_thread, redundant_data_copies.

Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-653--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only
- **Async context required:** Rules 1, 3, 5 apply ONLY inside async functions
- **Exclude wrappers:** Do not flag calls already wrapped in `to_thread`/`run_in_executor`
- **Context-aware:** Small files (<1KB) read synchronously may be acceptable
- **Exclude tests:** Do not flag test utilities or test fixtures

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed successfully (including output_dir)
- [ ] scan_path determined
- [ ] Async framework detected (asyncio/Node.js async/Tokio)
- [ ] All 6 checks completed:
  - blocking IO, unnecessary allocations, sync sleep, string concat, CPU-bound, redundant copies
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated using penalty algorithm
- [ ] Report written to `{output_dir}/ln-653--global.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-04
