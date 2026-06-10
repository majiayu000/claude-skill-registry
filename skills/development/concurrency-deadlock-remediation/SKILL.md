---
name: concurrency-deadlock-remediation
description: |-
  Use when finding and fixing deadlocks with lock ordering, reproduction, timeouts, or lock-free alternatives.
  Triggers:
practices:
- debugging
- defensive-programming
- root-cause-analysis
hexagonal_role: supporting
consumes: []
produces: []
context_rel: []
skill_api_version: 1
user-invocable: false
context:
  window: isolated
  intent:
    mode: none
  sections:
    exclude:
    - HISTORY
    - INTEL
    - TASK
  intel_scope: none
metadata:
  tier: judgment
  stability: experimental
  dependencies: []
output_contract: 'stdout: deadlock diagnosis (the lock-order cycle) + a concrete fix'
---
# concurrency-deadlock-remediation — Diagnose and eliminate concurrency deadlocks

> **Purpose:** Turn a mysterious hang into a named lock-order cycle, reproduce it
> on demand, and ship a fix that provably removes the circular wait.

**YOU MUST DO THE ANALYSIS. Do not guess — find the actual cycle, then fix it.**

---

## ⚠️ Critical Constraints

- **Find the cycle before touching code.** A deadlock is a *circular wait* among
  ≥2 resources. Name the exact resources and the order each thread takes them.
  **Why:** A fix applied without the cycle just moves the hang somewhere else.
- **Never "fix" by adding sleeps or retries blindly.** A retry around a held lock
  is a livelock, not a fix. **Why:** It hides the deadlock under intermittent
  slowness and corrupts your reproduction.
  ```text
  WRONG:  while (!tryLock(B)) { sleep(10); }   // still holding A — livelock
  CORRECT: acquire A and B in one consistent global order, every time
  ```
- **Acquire locks in ONE global order everywhere.** The classic bug is
  lock-order reversal (ABBA): thread 1 takes A then B; thread 2 takes B then A.
  **Why:** A single consistent order makes a circular wait impossible.
  ```text
  WRONG:  T1: lock(A); lock(B)      T2: lock(B); lock(A)
  CORRECT: T1: lock(A); lock(B)      T2: lock(A); lock(B)   // same order
  ```
- **Never hold a lock across a blocking call you don't control.** Holding a
  mutex while awaiting I/O, an RPC, a callback, or another lock invites a hang.
  **Why:** The thing you wait on may itself need your lock → cycle.
- **Don't ship a timeout as the whole fix.** A `tryLock(timeout)` turns a hang
  into a *failure* you must handle (back off, release, retry the whole unit).
  **Why:** Timeout is a safety net, not a substitute for correct lock order.

---

## Why This Exists

Deadlocks are silent: no crash, no error — just no progress. They are
nondeterministic (timing-dependent), so they pass in CI and freeze in
production. The fix is almost never "more locking"; it is *less* and *more
ordered* locking. This skill enforces the discipline: prove the cycle, reproduce
it, then remove the circular wait at its root — and verify the hang is gone.

---

## Quick Start

1. Capture state of the hung process (thread/goroutine/stack dump) — see
   [collecting evidence](#1-capture-the-hang).
2. Build the **wait-for graph**; a cycle in it IS the deadlock.
3. Pick a fix class: **consistent lock order** (default), **timeout + back-off**,
   or **lock-free** — see [fix classes](#4-fix-the-circular-wait).
4. Reproduce on demand, apply the fix, prove the hang no longer occurs.

---

## Methodology

### 1. Capture the hang

Get a snapshot of every thread and what each is *blocked on*. The exact tool is
language-specific; the goal is identical everywhere — see the per-language table.

| Stack / runtime | How to dump blocked threads |
|---|---|
| Java / JVM | `jstack <pid>` → look for `Found one Java-level deadlock` |
| Go | send `SIGQUIT` or `kill -ABRT <pid>` → full goroutine dump |
| Python (CPython) | `py-spy dump --pid <pid>` (or `faulthandler.dump_traceback`) |
| C / C++ / Rust | `gdb -p <pid>` then `thread apply all bt` |
| POSIX threads | `pstack <pid>` / `gdb` backtrace |
| DB transactions | engine deadlock log (Postgres `deadlock_timeout` log; MySQL `SHOW ENGINE INNODB STATUS`) |

**Checkpoint:** You have, for each stuck thread, (a) the lock it *holds* and
(b) the lock it *waits for*. If you can't see both, you cannot proceed — add
instrumentation (log lock acquire/release with thread id + resource id).

### 2. Build the wait-for graph

Nodes = threads. Edge `T_i → T_j` means *T_i waits for a resource held by T_j*.
**A directed cycle is the deadlock.** Two-thread case (ABBA):

```text
T1 holds A, wants B  ─┐
                      ├─►  T1 → T2 → T1   (cycle ⇒ deadlock)
T2 holds B, wants A  ─┘
```

Write the cycle down explicitly: `T1: A→B,  T2: B→A`. That sentence is your
diagnosis and the spec for the fix.

**Checkpoint:** You can state the cycle in one line. No cycle found ⇒ it's not a
deadlock (consider livelock, starvation, or a genuinely slow call).

### 3. Reproduce on demand

A deadlock you can't trigger is a deadlock you can't prove fixed. Force the
interleaving:

- Insert a sleep/yield in the *gap between* the two acquisitions in each thread
  so both reach the second lock simultaneously (test-only, then remove).
- Run the contended path under high concurrency in a loop (`-race` in Go;
  ThreadSanitizer / Helgrind in C/C++; stress loop elsewhere).
- For DB deadlocks: open two transactions in two sessions and interleave the
  row/table locks by hand.

**Checkpoint:** You can make it hang reliably (e.g., ≥1 in 10 runs). Keep this
as a regression test.

### 4. Fix the circular wait

Pick the lowest-cost fix that removes the cycle. In order of preference:

| Fix class | When to use | What it does |
|---|---|---|
| **Consistent global lock order** | default; ≥2 locks always taken together | Impose a total order (e.g., by address, id, or name); every site acquires in that order → no cycle |
| **Lock coarsening / single lock** | the two locks always co-occur | Replace A+B with one lock C; no pair → no cycle |
| **Lock splitting / narrower scope** | lock held too long across a blocking call | Release before the blocking call; copy data out, then act |
| **`tryLock` + timeout + back-off** | can't impose a global order (3rd-party locks) | On timeout, release ALL held locks, back off, retry the whole unit |
| **Lock-free / immutable** | hot path, simple state | Atomics/CAS, channels/message-passing, copy-on-write, or per-thread state — no shared lock at all |
| **DB: order rows + short txns** | transaction deadlocks | Lock rows in a deterministic order (e.g., `ORDER BY id`), keep transactions short, retry on the engine's deadlock error |

**Checkpoint:** State which class you chose and *why the cycle is now impossible*
(not just "less likely").

### 5. Verify

Re-run the reproduction from step 3. It must no longer hang. Run the stress
loop / race detector clean. Add the reproduction as a permanent test.

---

## Output Specification

Produce a short diagnosis-and-fix report (stdout or `DEADLOCK-REPORT.md`):

```text
CYCLE:    T1 holds <A>, wants <B>;  T2 holds <B>, wants <A>
REPRO:    <command/interleaving that triggers the hang>
FIX:      <fix class> — <one-line why the cycle is now impossible>
VERIFY:   <repro command run post-fix> → no hang; race detector clean
TEST:     <path to the added regression test>
```

---

## Quality Rubric

- [ ] The named **cycle** is written explicitly (which thread holds/wants which
      resource) — not just "there's a deadlock somewhere".
- [ ] The hang is **reproducible on demand** before the fix and **gone after**,
      with both runs shown.
- [ ] The fix removes the **circular wait by construction** (consistent order,
      single lock, or lock-free) — a bare timeout/retry alone does NOT pass.
- [ ] A **regression test** that reproduces the original interleaving is committed.

---

## Examples

**ABBA mutex (any language).** Two methods lock `accountA` then `accountB` in
opposite orders during a transfer. Fix: sort the two accounts by id and always
lock the lower id first → both call sites use the same order.

**Holding a lock across an await (async).** A coroutine holds `cache_lock` while
`await fetch(url)`; the fetch's completion callback needs `cache_lock`. Fix:
read what you need, **release `cache_lock` before the await**, re-acquire only to
write the result back.

**Postgres transaction deadlock.** Two sessions update rows 1 and 2 in opposite
order. Fix: always `UPDATE ... WHERE id IN (...) ORDER BY id`, keep the
transaction short, and retry on SQLSTATE `40P01` (deadlock_detected).

---

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| Hangs but no cycle in the wait-for graph | Livelock or starvation, not deadlock | Look for retry loops / unfair locks; check CPU is spinning |
| Dump shows one thread blocked, none holding | Waiting on external I/O / RPC, not a lock | Add a timeout to the external call; it's not a deadlock |
| Fix made it rarer but not gone | You ordered some sites, not all | Grep every acquisition of the pair; enforce order everywhere |
| `tryLock` timeout fires constantly | High contention / wrong granularity | Coarsen or split locks; reduce critical-section size |
| Repro won't trigger | Interleaving not forced | Add yields between the two acquisitions; raise concurrency |

---

## See Also

- A thread/goroutine dump is the single most useful artifact — capture it first.
- For DB-specific lock waits, the engine's own deadlock log already names the
  cycle; start there before instrumenting application code.
