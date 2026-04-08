---
name: ln-628-concurrency-auditor
description: "Checks async races, thread safety, TOCTOU, deadlocks, blocking I/O, resource contention. Use when auditing concurrency safety."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-graph__trace_dataflow, mcp__hex-graph__trace_paths
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Concurrency Auditor (L3 Worker)

**Type:** L3 Worker

Specialized worker auditing concurrency, async patterns, and cross-process resource access.

## Purpose & Scope

- Audit **concurrency** (Category 11: High Priority)
- 7 checks: async races, thread safety, TOCTOU, deadlocks, blocking I/O, resource contention, cross-process races
- Two-layer detection: grep finds candidates, agent reasons about context
- Calculate compliance score (X/10)

## Inputs

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

Receives `contextStore` with: `tech_stack`, `best_practices`, `codebase_root`, `output_dir`.

## Workflow

**MANDATORY READ:** Load `shared/references/two_layer_detection.md` for detection methodology.

1) **Parse context** -- extract tech_stack, language, output_dir from contextStore
2) **Per check (1-7):**
   - **Layer 1:** Grep/Glob scan to find candidates
   - **Layer 2:** Read 20-50 lines around each candidate. Apply check-specific critical questions. Classify: confirmed / false positive / needs-context
3) **Collect** confirmed findings with severity, location, effort, recommendation
4) **Calculate score** per `shared/references/audit_scoring.md`
5) **Write Report** -- build in memory, write to `{output_dir}/ln-628--global.md` (atomic single Write)
6) **Return Summary** to coordinator

## Audit Rules

**Unified severity escalation:** For ALL checks -- if finding affects payment/auth/financial code -> escalate to **CRITICAL** regardless of other factors.

### 1. Async/Event-Loop Races (CWE-362)

**What:** Shared state corrupted across await/yield boundaries in single-threaded async code.

**Layer 1 -- Grep patterns:**

| Language | Pattern | Grep |
|----------|---------|------|
| JS/TS | Read-modify-write across await | `\w+\s*[+\-*/]?=\s*.*await` (e.g., `result += await something`) |
| JS/TS | Check-then-initialize race | `if\s*\(!?\w+\)` followed by `\w+\s*=\s*await` in same block |
| Python | Read-modify-write across await | `\w+\s*[+\-*/]?=\s*await` inside `async def` |
| Python | Shared module-level state in async | Module-level `\w+\s*=` + modified inside `async def` |
| All | Shared cache without lock | `\.set\(|\.put\(|\[\w+\]\s*=` in async function without lock/mutex nearby |

**Layer 2 -- Critical questions:**
- Is the variable shared (module/global scope) or local?
- Can two async tasks interleave at this await point?
- Is there a lock/mutex/semaphore guarding the access?

**Severity:** CRITICAL (payment/auth) | HIGH (user-facing) | MEDIUM (background)

**Safe pattern exclusions:** Local variables, `const` declarations, single-use await (no interleaving possible).

**Effort:** M

### 2. Thread/Goroutine Safety (CWE-366)

**What:** Shared mutable state accessed from multiple threads/goroutines without synchronization.

**Layer 1 -- Grep patterns:**

| Language | Pattern | Grep |
|----------|---------|------|
| Go | Map access without mutex | `map\[.*\].*=` in struct without `sync.Mutex` or `sync.RWMutex` |
| Go | Variable captured by goroutine | `go func` + variable from outer scope modified |
| Python | Global modified in threads | `global\s+\w+` in function + `threading.Thread` in same file |
| Java | HashMap shared between threads | `HashMap` + `Thread\|Executor\|Runnable` in same class without `synchronized\|ConcurrentHashMap` |
| Rust | Rc in multi-thread context | `Rc<RefCell` + `thread::spawn\|tokio::spawn` in same file |
| Node.js | Worker Threads shared state | `workerData\|SharedArrayBuffer\|parentPort` + mutable access without `Atomics` |

**Layer 2 -- Critical questions:**
- Is this struct/object actually shared between threads? (single-threaded code -> FP)
- Is mutex/lock in embedded struct or imported module? (grep may miss it)
- Is `go func` capturing by value (safe) or by reference (unsafe)?

**Severity:** CRITICAL (payment/auth) | HIGH (data corruption possible) | MEDIUM (internal)

**Safe pattern exclusions:** Go map in `init()` or `main()` before goroutines start. Rust `Arc<Mutex<T>>` (already safe). Java `Collections.synchronizedMap()`.

**Effort:** M

### 3. TOCTOU -- Time-of-Check Time-of-Use (CWE-367)

**What:** Resource state checked, then used, but state can change between check and use.

**Layer 1 -- Grep patterns:**

| Language | Check | Use | Grep |
|----------|-------|-----|------|
| Python | `os.path.exists()` | `open()` | `os\.path\.exists\(` near `open\(` on same variable |
| Python | `os.access()` | `os.open()` | `os\.access\(` near `os\.open\(\|open\(` |
| Node.js | `fs.existsSync()` | `fs.readFileSync()` | `existsSync\(` near `readFileSync\(\|readFile\(` |
| Node.js | `fs.accessSync()` | `fs.openSync()` | `accessSync\(` near `openSync\(` |
| Go | `os.Stat()` | `os.Open()` | `os\.Stat\(` near `os\.Open\(\|os\.Create\(` |
| Java | `.exists()` | `new FileInputStream` | `\.exists\(\)` near `new File\|FileInputStream\|FileOutputStream` |

**Layer 2 -- Critical questions:**
- Is the check used for control flow (vulnerable) or just logging (safe)?
- Is there a lock/retry around the check-then-use sequence?
- Is the file in a temp directory controlled by the application (lower risk)?
- Could an attacker substitute the file (symlink attack)?

**Severity:** CRITICAL (security-sensitive: permissions, auth tokens, configs) | HIGH (user-facing file ops) | MEDIUM (internal/background)

**Safe pattern exclusions:** Check inside try/catch with retry. Check for logging/metrics only. Check + use wrapped in file lock.

**Effort:** S-M (replace check-then-use with direct use + error handling)

### 4. Deadlock Potential (CWE-833)

**What:** Lock acquisition in inconsistent order, or lock held during blocking operation.

**Layer 1 -- Grep patterns:**

| Language | Pattern | Grep |
|----------|---------|------|
| Python | Nested locks | `with\s+\w+_lock:` (multiline: two different locks nested) |
| Python | Lock in loop | `for.*:` with `\.acquire\(\)` inside loop body |
| Python | Lock + external call | `\.acquire\(\)` followed by `await\|requests\.\|urllib` before release |
| Go | Missing defer unlock | `\.Lock\(\)` without `defer.*\.Unlock\(\)` on next line |
| Go | Nested locks | Two `\.Lock\(\)` calls in same function without intervening `\.Unlock\(\)` |
| Java | Nested synchronized | `synchronized\s*\(` (multiline: nested blocks with different monitors) |
| JS | Async mutex nesting | `await\s+\w+\.acquire\(\)` (two different mutexes in same function) |

**Layer 2 -- Critical questions:**
- Are these the same lock (reentrant = OK) or different locks (deadlock risk)?
- Is the lock ordering consistent across all call sites?
- Does the external call inside lock have a timeout?

**Severity:** CRITICAL (payment/auth) | HIGH (app freeze risk)

**Safe pattern exclusions:** Reentrant locks (same lock acquired twice). Locks with explicit timeout (`asyncio.wait_for`, `tryLock`).

**Effort:** L (lock ordering redesign)

### 5. Blocking I/O in Async Context (CWE-400)

**What:** Synchronous blocking calls inside async functions or event loop handlers.

**Layer 1 -- Grep patterns:**

| Language | Blocking Call | Grep | Replacement |
|----------|--------------|------|-------------|
| Python | `time.sleep` in async def | `time\.sleep` inside `async def` | `await asyncio.sleep` |
| Python | `requests.*` in async def | `requests\.(get\|post\|put\|delete)` inside `async def` | `httpx` or `aiohttp` |
| Python | `open()` in async def | `open\(` inside `async def` | `aiofiles.open` |
| Node.js | `fs.readFileSync` in async | `fs\.readFileSync\|fs\.writeFileSync\|fs\.mkdirSync` | `fs.promises.*` |
| Node.js | `execSync` in async | `execSync\|spawnSync` in async handler | `exec` with promises |
| Node.js | Sync crypto in async | `crypto\.pbkdf2Sync\|crypto\.scryptSync` | `crypto.pbkdf2` (callback) |

**Layer 2 -- Critical questions:**
- Is this in a hot path (API handler) or cold path (startup script)?
- Is the blocking duration significant (>100ms)?
- Is there a legitimate reason (e.g., sync read of small config at startup)?

**Severity:** HIGH (blocks event loop/async context) | MEDIUM (minor blocking <100ms)

**Safe pattern exclusions:** Blocking call in `if __name__ == "__main__"` (startup). `readFileSync` in config loading at init time. Sync crypto for small inputs.

**Effort:** S-M (replace with async alternative)

### 6. Resource Contention (CWE-362)

**What:** Multiple concurrent accessors compete for same resource without coordination.

**Layer 1 -- Grep patterns:**

| Pattern | Risk | Grep |
|---------|------|------|
| Shared memory without sync | Data corruption | `SharedArrayBuffer\|SharedMemory\|shm_open\|mmap` without `Atomics\|Mutex\|Lock` nearby |
| IPC without coordination | Message ordering | `process\.send\|parentPort\.postMessage` in concurrent loops |
| Concurrent file append | Interleaved writes | Multiple `appendFile\|fs\.write` to same path from parallel tasks |

**Layer 2 -- Critical questions:**
- Are multiple writers actually concurrent? (Sequential = safe)
- Is there OS-level atomicity guarantee? (e.g., `O_APPEND` for small writes)
- Is ordering important for correctness?

**Severity:** HIGH (data corruption) | MEDIUM (ordering issues)

**Safe pattern exclusions:** Single writer pattern. OS-guaranteed atomic operations (small pipe writes, `O_APPEND`). Message queues with ordering guarantees.

**Effort:** M

### 7. Cross-Process & Invisible Side Effects (CWE-362, CWE-421)

**What:** Multiple processes or process+OS accessing same exclusive resource, including operations with non-obvious side effects on shared OS resources.

**Layer 1 -- Grep entry points:**

| Pattern | Risk | Grep |
|---------|------|------|
| Clipboard dual access | OSC 52 + native clipboard in same flow | `osc52\|\\x1b\\]52` AND `clipboard\|SetClipboardData\|pbcopy\|xclip` in same file |
| Subprocess + shared file | Parent and child write same file | `spawn\|exec\|Popen` + `writeFile\|open.*"w"` on same path |
| OS exclusive resource | Win32 clipboard, serial port, named pipe | `OpenClipboard\|serial\.Serial\|CreateNamedPipe\|mkfifo` |
| Terminal escape sequences | stdout triggers terminal OS access | `\\x1b\\]\|\\033\\]\|writeOsc\|xterm` |
| External clipboard tools | Clipboard via spawned process | `pbcopy\|xclip\|xsel\|clip\.exe` |

**Layer 2 -- This check relies on reasoning more than any other:**

1. **Build Resource Inventory:**

   | Resource | Exclusive? | Accessor 1 | Accessor 2 | Sync present? |
   |----------|-----------|------------|------------|---------------|

2. **Trace Timeline:**
   ```
   t=0ms  operation_A() -> resource_X accessed
   t=?ms  side_effect   -> resource_X accessed by external process
   t=?ms  operation_B() -> resource_X accessed again -> CONFLICT?
   ```

3. **Critical Questions:**
   - Can another process (terminal, OS, child) access this resource simultaneously?
   - Does this operation have invisible side effects on shared OS resources?
   - What happens if the external process is slower/faster than expected?
   - What happens if user triggers this action twice rapidly?

**Severity:** CRITICAL (two accessors to exclusive OS resource without sync) | HIGH (subprocess + shared file without lock) | HIGH (invisible side effect detected via reasoning)

**Safe pattern exclusions:** Single accessor. Retry/backoff pattern present. Operations sequenced with explicit delay/await.

**Effort:** M-L (may require removing redundant access path)

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/references/audit_scoring.md`.

## Output Format

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md` and `shared/templates/audit_worker_report_template.md`.

Write JSON summary per `shared/references/audit_summary_contract.md`. In managed mode the caller passes both `runId` and `summaryArtifactPath`; in standalone mode the worker generates its own run-scoped artifact path per shared contract.

Write report to `{output_dir}/ln-628--global.md` with `category: "Concurrency"` and checks: async_races, thread_safety, toctou, deadlock_potential, blocking_io, resource_contention, cross_process_races.

Return summary per `shared/references/audit_summary_contract.md`.

When `summaryArtifactPath` is absent, write the standalone runtime summary under `.hex-skills/runtime-artifacts/runs/{run_id}/audit-worker/{worker}--{identifier}.json` and optionally echo the same summary in structured output.
```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/ln-628--global.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Critical Rules

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- **Do not auto-fix:** Report only -- concurrency fixes require careful human review
- **Two-layer detection:** Always apply Layer 2 reasoning after Layer 1 grep. Never report raw grep matches without context analysis
- **Language-aware detection:** Use language-specific patterns per check
- **Unified CRITICAL escalation:** Any finding in payment/auth/financial code = CRITICAL
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Exclusions:** Skip test files, skip single-threaded CLI tools, skip generated code

## Definition of Done

**MANDATORY READ:** Load `shared/references/audit_worker_core_contract.md`.

- [ ] contextStore parsed (language, concurrency model, output_dir)
- [ ] All 7 checks completed with two-layer detection:
  - async races, thread safety, TOCTOU, deadlock potential, blocking I/O, resource contention, cross-process races
- [ ] Layer 2 reasoning applied to each candidate (confirmed / FP / needs-context)
- [ ] Findings collected with severity, location, effort, recommendation
- [ ] Score calculated per `shared/references/audit_scoring.md`
- [ ] Report written to `{output_dir}/ln-628--global.md` (atomic single Write call)
- [ ] Summary written per contract

## Reference Files

- **Two-layer detection methodology:** `shared/references/two_layer_detection.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

---
**Version:** 4.0.0
**Last Updated:** 2026-03-04
