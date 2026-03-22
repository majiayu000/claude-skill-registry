---
name: ln-628-concurrency-auditor
description: Concurrency audit worker (L3). Checks race conditions, missing async/await, resource contention, thread safety, deadlock potential. Returns findings with severity, location, effort, recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Concurrency Auditor (L3 Worker)

Specialized worker auditing concurrency and async patterns.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline**
- Audit **concurrency** (Category 11: High Priority)
- Check race conditions, async/await, thread safety
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with tech stack, language, codebase root, output_dir.

## Workflow

1) Parse context + output_dir
2) Check concurrency patterns
3) Collect findings
4) Calculate score
5) **Write Report:** Build full markdown report in memory per `shared/templates/audit_worker_report_template.md`, write to `{output_dir}/628-concurrency.md` in single Write call
6) **Return Summary:** Return minimal summary to coordinator

## Audit Rules

### 1. Race Conditions
**What:** Shared state modified without synchronization

**Detection Patterns:**

| Language | Pattern | Grep |
|----------|---------|------|
| Python | Global modified in async | `global\s+\w+` inside `async def` |
| TypeScript | Module-level let in async | `^let\s+\w+` at file scope + async function modifies it |
| Go | Map access without mutex | `map\[.*\].*=` without `sync.Mutex` in same file |
| All | Shared cache | `cache\[.*\]\s*=` or `cache\.set` without lock |

**Severity:**
- **CRITICAL:** Race in payment/auth (`payment`, `balance`, `auth`, `token` in variable name)
- **HIGH:** Race in user-facing feature
- **MEDIUM:** Race in background job

**Recommendation:** Use locks, atomic operations, message queues

**Effort:** M-L

### 2. Missing Async/Await
**What:** Callback hell or unhandled promises

**Detection Patterns:**

| Issue | Grep | Example |
|-------|------|---------|
| Callback hell | `\.then\(.*\.then\(.*\.then\(` | `.then().then().then()` |
| Fire-and-forget | `async.*\(\)` not preceded by `await` | `saveToDb()` without await |
| Missing await | `return\s+new\s+Promise` in async function | Should just `return await` or `return` value |
| Dangling promise | `\.catch\(\s*\)` | Empty catch swallows errors |

**Severity:**
- **HIGH:** Fire-and-forget async (can cause data loss)
- **MEDIUM:** Callback hell (hard to maintain)
- **LOW:** Mixed Promise styles

**Recommendation:** Convert to async/await, always await or handle promises

**Effort:** M

### 3. Resource Contention
**What:** Multiple processes competing for same resource

**Detection Patterns:**

| Issue | Grep | Example |
|-------|------|---------|
| File lock missing | `open\(.*["']w["']\)` without `flock` or `lockfile` | Concurrent file writes |
| Connection exhaustion | `create_engine\(.*pool_size` check if pool_size < 5 | DB pool too small |
| Concurrent writes | `writeFile` or `fs\.write` without lock check | File corruption risk |

**Severity:**
- **HIGH:** File corruption risk, DB exhaustion
- **MEDIUM:** Performance degradation

**Recommendation:** Use connection pooling, file locking, `asyncio.Lock`

**Effort:** M

### 4. Thread Safety Violations
**What:** Shared mutable state without synchronization

**Detection Patterns:**

| Language | Safe Pattern | Unsafe Pattern |
|----------|--------------|----------------|
| Go | `sync.Mutex` with map | `map[...]` without Mutex in same struct |
| Rust | `Arc<Mutex<T>>` | `Rc<RefCell<T>>` in multi-threaded context |
| Java | `synchronized` or `ConcurrentHashMap` | `HashMap` shared between threads |
| Python | `threading.Lock` | Global dict modified in threads |

**Grep patterns:**
- Go unsafe: `type.*struct\s*{[^}]*map\[` without `sync.Mutex` in same struct
- Python unsafe: `global\s+\w+` in function + `threading.Thread` in same file

**Severity:** **HIGH** (data corruption possible)

**Recommendation:** Use thread-safe primitives

**Effort:** M

### 5. Deadlock Potential
**What:** Lock acquisition in inconsistent order

**Detection Patterns:**

| Issue | Grep | Example |
|-------|------|---------|
| Nested locks | `with\s+\w+_lock:.*with\s+\w+_lock:` (multiline) | Lock A then Lock B |
| Lock in loop | `for.*:.*\.acquire\(\)` | Lock acquired repeatedly without release |
| Lock + external call | `.acquire\(\)` followed by `await` or `requests.` | Holding lock during I/O |

**Severity:** **HIGH** (deadlock freezes application)

**Recommendation:** Consistent lock ordering, timeout locks (`asyncio.wait_for`)

**Effort:** L

### 6. Blocking I/O in Event Loop (Python asyncio)
**What:** Synchronous blocking calls inside async functions

**Detection Patterns:**

| Blocking Call | Grep in `async def` | Replacement |
|---------------|---------------------|-------------|
| `time.sleep` | `time\.sleep` inside async def | `await asyncio.sleep` |
| `requests.` | `requests\.(get\|post)` inside async def | `httpx` or `aiohttp` |
| `open()` file | `open\(` inside async def | `aiofiles.open` |

**Severity:**
- **HIGH:** Blocks entire event loop
- **MEDIUM:** Minor blocking (<100ms)

**Recommendation:** Use async alternatives

**Effort:** S-M

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

## Output Format

**MANDATORY READ:** Load `shared/templates/audit_worker_report_template.md` for file format.

Write report to `{output_dir}/628-concurrency.md` with `category: "Concurrency"` and checks: race_conditions, missing_await, resource_contention, thread_safety, deadlock_potential, blocking_io.

Return summary to coordinator:
```
Report written: docs/project/.audit/628-concurrency.md
Score: X.X/10 | Issues: N (C:N H:N M:N L:N)
```

## Reference Files

- **Worker report template:** `shared/templates/audit_worker_report_template.md`
- **Audit scoring formula:** `shared/references/audit_scoring.md`
- **Audit output schema:** `shared/references/audit_output_schema.md`

## Critical Rules

- **Do not auto-fix:** Report only, concurrency fixes require careful human review
- **Language-aware detection:** Use language-specific patterns (Go sync.Mutex, Python asyncio.Lock, Java synchronized)
- **Effort realism:** S = <1h, M = 1-4h, L = >4h
- **Critical path escalation:** Race conditions in payment/auth = CRITICAL, regardless of other factors
- **Exclusions:** Skip test files, skip single-threaded CLI tools, skip generated code

## Definition of Done

- contextStore parsed (language, concurrency model, output_dir)
- All 6 checks completed (race conditions, missing await, resource contention, thread safety, deadlock potential, blocking I/O)
- Findings collected with severity, location, effort, recommendation
- Score calculated per `shared/references/audit_scoring.md`
- Report written to `{output_dir}/628-concurrency.md` (atomic single Write call)
- Summary returned to coordinator

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
