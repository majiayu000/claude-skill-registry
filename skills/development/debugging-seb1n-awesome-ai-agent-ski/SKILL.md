---
name: debugging
description: Systematically diagnose and fix software bugs by analyzing error messages, stack traces, logs, and runtime behavior across multiple languages. Use when the user requests debugging or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills contributors
  version: 1.0.0
---

# Debugging

This skill equips an AI agent with a systematic methodology for diagnosing and resolving software bugs. Rather than guessing at fixes, the agent follows a structured process — reproduce, isolate, diagnose, fix, verify — to find root causes and produce reliable corrections. It handles a wide range of bug categories including logic errors, runtime exceptions, race conditions, memory leaks, and performance regressions across multiple languages and runtime environments.

## Workflow

1. **Reproduce the problem.** Confirm the bug is observable and repeatable. Gather the exact error message, stack trace, log output, or description of unexpected behavior. Identify the minimum input or sequence of steps that triggers the issue. If the bug is intermittent, note the frequency and any environmental conditions (load, timing, specific data) that correlate with its appearance.

2. **Isolate the fault location.** Use the stack trace, error message, and code structure to narrow down the region of code responsible. Trace data flow backward from the point of failure to find where the value diverged from expectations. Eliminate unrelated code paths by checking whether the bug persists when components are stubbed out or bypassed. For large codebases, use binary search strategies — disable half the system, check if the bug still occurs, and repeat.

3. **Diagnose the root cause.** Once the faulty region is identified, determine exactly why the code misbehaves. Common root causes include: incorrect assumptions about input (null, empty, out-of-range), state mutation from a concurrent thread, stale cache or memoized value, incorrect operator precedence, missing await on an async call, or a dependency version incompatibility. Distinguish the root cause from its symptoms — a NullPointerException is a symptom; the root cause may be a missing validation three function calls earlier.

4. **Develop and apply the fix.** Write the smallest change that addresses the root cause without introducing side effects. If the fix involves changing a shared interface, trace all callers to ensure compatibility. Prefer defensive fixes that handle the error class broadly (e.g., adding input validation) over narrow patches that only address the single observed failure.

5. **Verify the fix and prevent regression.** Run the reproduction steps again to confirm the bug is resolved. Write or update a test case that encodes the previously-failing scenario so the bug cannot silently return. Check that existing tests still pass. If the bug was in a critical path, consider adding logging or monitoring to detect similar issues in the future.

## Supported Technologies

| Category          | Tools and Techniques                                              |
|-------------------|-------------------------------------------------------------------|
| Stack traces      | Python tracebacks, Java/JS stack traces, Go panic output, Rust backtraces |
| Logging           | Python `logging`, JavaScript `console`, structured JSON logs      |
| Debuggers         | `pdb` / `ipdb`, Chrome DevTools, `gdb` / `lldb`, `dlv` (Go)     |
| Profiling         | `cProfile`, `py-spy`, Chrome Performance tab, `pprof`            |
| Memory analysis   | `tracemalloc`, `heapq`, Valgrind, Chrome Heap Snapshots          |
| Concurrency       | Thread dumps, `asyncio` debug mode, Go race detector (`-race`)   |

## Usage

Provide one or more of the following inputs:

- **Code snippet or file path** containing the buggy code.
- **Error message or stack trace** — paste the full output, not a summary.
- **Description of unexpected behavior** — what you expected versus what happened.
- **Steps to reproduce** — the exact commands, inputs, or user actions that trigger the bug.
- **Logs** — relevant log output from before and during the failure.

The more context you provide, the faster and more accurately the agent can diagnose the issue.

## Examples

### Example 1 — Debugging a race condition in Python async code

**Bug report:** "Sometimes the response is missing the `user_profile` field, but only under load."

Buggy code in `src/api/handler.py`:

```python
import asyncio
import aiohttp

user_cache = {}

async def fetch_user(session, user_id):
    if user_id in user_cache:
        return user_cache[user_id]
    async with session.get(f"https://api.example.com/users/{user_id}") as resp:
        data = await resp.json()
    user_cache[user_id] = data
    return data

async def build_response(user_id):
    async with aiohttp.ClientSession() as session:
        profile, orders = await asyncio.gather(
            fetch_user(session, user_id),
            fetch_orders(session, user_id),
        )
    return {"user_profile": profile, "orders": orders}
```

**Agent diagnosis:**

The `user_cache` dictionary is shared mutable state accessed by concurrent coroutines without synchronization. When two requests for the same `user_id` arrive simultaneously, both see a cache miss, both issue HTTP requests, and the second write may overwrite the first with a partially different object. More critically, dictionary mutation during concurrent iteration can produce `RuntimeError` on Python 3.

**Root cause:** Unsynchronized shared mutable state in a concurrent context.

**Fix:**

```python
import asyncio
import aiohttp

user_cache = {}
cache_locks = {}
global_lock = asyncio.Lock()

async def fetch_user(session, user_id):
    async with global_lock:
        if user_id not in cache_locks:
            cache_locks[user_id] = asyncio.Lock()
        lock = cache_locks[user_id]

    async with lock:
        if user_id in user_cache:
            return user_cache[user_id]
        async with session.get(f"https://api.example.com/users/{user_id}") as resp:
            data = await resp.json()
        user_cache[user_id] = data
        return data
```

The per-key lock ensures only one coroutine fetches a given user at a time. Others wait and then read from the cache.

### Example 2 — Debugging a memory leak in a Node.js server

**Bug report:** "Server memory usage grows from 150 MB to 2 GB over 24 hours, then crashes with OOM."

Buggy code in `src/server.js`:

```javascript
const express = require("express");
const app = express();

const requestLog = [];

app.use((req, res, next) => {
  requestLog.push({
    method: req.method,
    url: req.url,
    headers: { ...req.headers },
    timestamp: new Date(),
  });
  next();
});

app.get("/health", (req, res) => {
  res.json({ status: "ok", requestCount: requestLog.length });
});

app.listen(3000);
```

**Agent diagnosis:**

The `requestLog` array is a module-level variable that grows without bound. Every incoming request appends an object containing a full copy of the request headers. At 1000 requests per minute with an average header size of 2 KB, this accumulates roughly 2.8 GB per day — matching the reported OOM timeline.

**Root cause:** Unbounded in-memory array that is never pruned or rotated.

**Fix:**

```javascript
const express = require("express");
const app = express();

const MAX_LOG_SIZE = 10000;
const requestLog = [];

app.use((req, res, next) => {
  if (requestLog.length >= MAX_LOG_SIZE) {
    requestLog.shift();
  }
  requestLog.push({
    method: req.method,
    url: req.url,
    timestamp: new Date(),
  });
  next();
});
```

Key changes: (1) cap the array at a fixed size and evict the oldest entry, (2) stop storing full headers — log only what is needed, (3) for production use, replace the in-memory array with a proper logging pipeline (e.g., write to a log file or send to an external service).

**Verification:** Run a load test with `autocannon -d 60 http://localhost:3000/health` and monitor memory via `process.memoryUsage()`. Memory should plateau at the cap size rather than climbing linearly.

## Best Practices

- **Read the entire stack trace, bottom to top.** The root cause is often in the deepest application frame, not the top-level exception. Framework frames can be skipped, but your code frames should be read in order.
- **Change one thing at a time.** When testing a hypothesis, make a single modification and re-run. Changing multiple things simultaneously makes it impossible to determine which change had the effect.
- **Use logging strategically.** Insert log statements at the entry and exit of suspect functions, printing key variable values. Remove or reduce log verbosity after the bug is fixed.
- **Check recent changes first.** If the bug appeared after a specific deployment or commit, `git bisect` or reviewing the recent diff is often the fastest path to the root cause.
- **Reproduce before fixing.** Never apply a fix to a bug you cannot reproduce. Without reproduction, you cannot verify the fix works, and you risk introducing a change that masks the symptom without addressing the cause.
- **Write a regression test.** Every fixed bug should produce a new test case that fails before the fix and passes after. This is the most reliable way to prevent the same bug from returning.

## Edge Cases

- **Heisenbugs:** Some bugs disappear when debugging tools are attached (e.g., timing changes from breakpoints mask race conditions). For these, use logging or tracing instead of interactive debuggers, and consider running with the language's race detector if available.
- **Environment-specific bugs:** A bug that only appears in production may depend on OS version, memory limits, network latency, or configuration that differs from development. The agent will ask for environment details and suggest reproducing with matching constraints (e.g., Docker with memory limits).
- **Third-party library bugs:** If the root cause is in a dependency rather than application code, the fix may involve upgrading the library, applying a workaround, or pinning a known-good version. The agent will check changelogs and issue trackers before recommending a path.
- **Compiler or runtime bugs:** Rarely, the bug is in the language runtime itself. The agent will exhaust application-level explanations first, then suggest testing on a different runtime version if no application-level cause is found.
- **Corrupted state:** If the bug involves corrupted data (e.g., a half-written database row), diagnosis requires examining the data alongside the code. The agent will ask for sample data or database state to correlate with the code path analysis.
