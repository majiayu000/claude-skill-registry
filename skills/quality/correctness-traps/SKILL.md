---
name: correctness-traps
description: Use when writing or reviewing error handling, floating-point math, concurrent code, remote calls, singletons/globals, hot-path data structures, or high-volume log statements
---

# Error and Correctness Traps

## Overview

Common bugs grouped by domain: floats that won't compare equal, retries that hammer a downed service, singletons that wreck testability, and others. **When you write code in one of these domains, stop and run the matching checks before you commit.**

This is a **rigid** skill. Jump to the sub-section that matches what you're writing and run that sub-section's checks.

These checks matter most when code will reach real users in production. In MVPs, prototypes, internal dev tools, and one-off scripts where the architecture is still in flux, prefer the simplest thing that works.

## When to invoke

Invoke when you're about to:

- Add or change error-handling around a call that can fail
- Compare, sum, or accumulate floating-point numbers
- Write concurrent, parallel, or threaded code, or share mutable state between threads
- Call a remote process, web service, database, or another machine
- Introduce a singleton or any globally-shared mutable state
- Choose a data structure or algorithm on a path that runs often or on large inputs
- Add or change log statements that may fire at high volume
- Review code that handles errors, floats, concurrency, remote calls, singletons, or hot-path data structures

### Non-triggers — do NOT invoke for

- Renaming a local variable inside one function
- Adding a docstring to an existing function
- Fixing a typo in a comment
- Formatting-only changes handled by a formatter
- Adjusting a config value in a config file with no logic change
- Skimming code for context without producing findings or edits
- An early-stage MVP or prototype where the architecture is still in flux
- An internal dev tool, debugging endpoint, or one-off script
- Throwaway code expected to be replaced before reaching users

If the change touches one of these domains even slightly, **invoke anyway** — the per-domain check is short and the bugs are not.

## Checks by domain

### Errors (97/21, 97/26, 97/29)

1. **Distinguish business exceptions from technical ones.** A *technical* exception means the system can't proceed — bad arguments, broken DB connection, programming error. Let it bubble to a top-level handler that puts the system in a safe state (rollback, log, alert, friendly user message); the caller can't fix it. A *business* exception is part of the contract — withdrawing from an empty account, booking an unavailable slot — and is an alternative return path the caller is expected to handle. Give them separate types or hierarchies; mixing them blurs the contract. *(Bergh Johnsson, 97/21.)*
2. **Never write the empty `catch`.** `try { ... } catch (...) {}` silently swallows everything. Same for ignoring return codes (`printf`'s return value, `write()`'s short-write count) and pretending `errno` doesn't exist. Example: a service-call wrapper swallows every exception and returns `null`, so every downstream caller has to invent their own theory of what `null` means. Expose erroneous conditions in your interfaces; if handling errors feels onerous, the interface is wrong. *(Goodliffe, 97/26.)*
3. **Don't rely on unexplained magic.** If your change depends on behavior nobody can explain (build picks a DLL by load order, deployment reads an undocumented env var, a job runs because of a side effect in a config file), surface it in your summary to the user before shipping — don't bury the dependency. *(Griffiths, 97/29.)*

### Numerics (97/33)

4. **Never compare floats with `==`.** `0.1 + 0.2 != 0.3` in IEEE 754 — the canonical demonstration. Compare with a tolerance appropriate to the magnitude of the values involved (≈ ε|x|, where ε is machine epsilon — ~1e-7 for `float`, ~1e-16 for `double`).
5. **Watch for catastrophic cancellation.** Subtracting nearly-equal floats promotes roundoff to the most significant digits. Example: solving `x² - 100000x + 1 = 0` directly via the quadratic formula gives a wildly wrong small root because `-b + sqrt(b² - 4)` cancels; compute one root and derive the other from `r1 * r2 = c/a`. Same shape of error appears in any series with alternating signs of similar magnitude.
6. **Don't use float for money.** Use a fixed-point or decimal type. Floats are for scientific calculation where you accept ε-level error; financial code does not accept it. *(Allison, 97/33.)*

### Concurrency & IPC (97/41, 97/57)

7. **Default to message passing over shared mutable state.** When you reach for a lock around shared data, ask first whether the data could be owned by one process/actor that others message. CSP-style designs (Erlang, Go channels, actor frameworks in mainstream languages) sidestep most race / deadlock / livelock bugs by construction. Reserve shared-memory + locks for cases you have measured and understood. *(Winder, 97/57.)*
8. **Count IPCs per user stimulus, not lines of code.** Each remote call is non-trivial latency; sequential calls add. Example: ORM lazy-loading produces 1,000 sequential 10ms DB calls for one page render — minimum 10s response time before any rendering work. Ratios in the thousands appear routinely in slow apps. Apply parsimony (one round-trip carrying the right data), parallelism (overall latency = longest call, not sum), or caching. *(Stafford, 97/41.)*
9. **Retry with backoff and a cap, never in a tight loop.** Example: `while (!call()) call();` against a downed service hammers it the moment it comes back. Exponential backoff, jitter, and a max-retries ceiling are the minimum; idempotency on the server side is what makes retry safe at all.

### Limits & Performance (97/46, 97/89)

10. **Know the complexity of the data structure you picked.** Linked list vs. hash vs. balanced tree on a million items is the difference between snappy and unusable. Pick by access pattern (lookup-heavy → hash; ordered iteration → tree; tiny + cache-friendly → array), not by what's familiar. *(van Winkel, 97/89.)*
11. **Don't recompute invariants inside loops.** Example: `for (i = 0; i < strlen(s); ++i)` — `strlen` runs every iteration, scanning the whole string each time, turning O(n) work into O(n²). Hoist the length out. The same shape applies to repeated DB lookups, repeated config parses, and repeated regex compilations inside hot loops. *(van Winkel, 97/89.)*
12. **Respect the cache hierarchy when it dominates.** Register and L1 are nanoseconds; RAM is ~20ns; disk is ~10ms; network is ~20–100ms — orders of magnitude apart. A "worse" big-O algorithm with a predictable access pattern can beat a "better" one that thrashes cache. When perf matters, **measure** rather than reason from complexity alone. *(Colvin, 97/46.)*

### Globals & Singletons (97/73)

13. **Resist the singleton.** Most singletons encode a single-instance assumption that turns out to be premature, broadcast across the design as hidden coupling. They wreck unit-test independence (you can't substitute a mock), introduce subtle multi-threading bugs (naive locking slow, double-checked locking famously broken in several languages), and have no defined cleanup order at shutdown. Example: a `Logger.getInstance()` called from every layer means tests can't intercept output, can't run in parallel, and inherit log state from previous tests.
14. **If you genuinely need one instance, hide it behind an interface.** Restrict the global access to a few well-defined construction sites; everywhere else, accept the dependency through a parameter typed by interface. Callers don't know whether a singleton or a fresh object satisfies the interface — and tests can substitute either. *(Saariste, 97/73.)*

### Production resilience (`RI/*`)

When the call will run under load against a downstream that can fail, the per-call hardening *is* the first write. These checks matter most in production code.

15. **Set an explicit timeout on every remote call.** Library defaults are wrong (`None`, "infinity", "many minutes"). Pick a per-call budget based on the downstream's realistic latency plus margin, and cap retries inside that budget. *(`RI/Timeout`.)*
16. **Wrap critical downstreams in a circuit breaker.** Tracked per-downstream failures; once threshold crossed, fail fast locally for a window; probe; close on success. Distinct from retry/backoff: this is "should we attempt at all right now." *(`RI/CircuitBreaker`.)*
17. **Bulkhead resource pools per downstream.** Separate thread pools, connection pools, or queues per external dependency so one stalled downstream cannot exhaust capacity for healthy ones. *(`RI/Bulkhead`.)*
18. **Bounded queues only.** An unbounded queue eventually exhausts memory under load. Pick a cap and an explicit reject policy (drop oldest, drop newest, backpressure to caller). *(`RI/Backpressure`.)*
19. **Fail fast when the request cannot succeed.** Validate at the entry point; check circuit-breaker state and feature flags before expensive setup; return a clear error before holding DB connections, locks, or downstream quota. *(`RI/FailFast`.)*

## Red Flags

These thoughts mean STOP — apply the domain check before committing:

| Thought | Reality |
|---|---|
| "I'll throw the same exception type for both — caller handles either way." | Technical and business exceptions are different contracts. Mixing them means callers can't tell what to guard against beforehand vs. handle after. (97/21) |
| "Empty catch is fine, the error can't happen here." | "Can't happen" is how silent corruption ships. Log, rethrow, or surface the error — never swallow. (97/26) |
| "Nobody on the team knows how this build step works, but it works." | Magic that no one owns is a fault waiting for the day the magic stops. Find the person who knows or document it now. (97/29) |
| "`if (a == b)` for floats is fine, the values are computed the same way." | `0.1 + 0.2 != 0.3`. Use a tolerance scaled to magnitude, or use a decimal type. (97/33) |
| "I'll use `double` for the price column — it's faster than `Decimal`." | Floats accumulate roundoff; money does not forgive roundoff. Use fixed-point or decimal for currency. (97/33) |
| "I'll wrap a lock around the shared map — that fixes the race." | Locks around shared mutable state are where deadlocks and lost updates hide. Prefer message passing; lock only when measured and understood. (97/57) |
| "Failed call → just retry in a loop until it works." | A retry loop without backoff and a cap will hammer the service the moment it recovers. Backoff + jitter + ceiling, and require idempotency on the server. (97/41) |
| "I'll lazy-load each related row — it's cleaner." | One page = thousands of sequential round-trips = visibly broken latency. Count IPCs per stimulus; batch, parallelize, or cache. (97/41) |
| "It's just `for (i = 0; i < strlen(s); ++i)` — looks normal." | `strlen` runs every iteration; an O(n) loop becomes O(n²). Hoist invariants out of hot loops. (97/89) |
| "Linked list is fine, n won't get that big." | "Won't get that big" is how production timeouts are born. Pick the structure by access pattern and confirm with measurement. (97/89, 97/46) |
| "Singleton — there'll only ever be one." | Single-instance is an assumption that ages badly, and the global access point destroys testability. Hide behind an interface, inject the dependency. (97/73) |
| "I'll let the HTTP client default the timeout — it's fine." | Defaults are `None` or hours. Held connections, threads, and queue slots add up under load. Set an explicit per-call timeout. (`RI/Timeout`) |
| "The downstream's flaky — I'll just retry." | Retry without a circuit breaker piles load on a service that's already failing. Wrap critical downstreams in a breaker; fail fast locally when open. (`RI/CircuitBreaker`) |
| "One pool for all downstreams keeps the code simpler." | One slow third party fills the pool and the whole service stops. Bulkhead per downstream; isolate failure domains. (`RI/Bulkhead`) |
| "I'll buffer events in an in-memory queue — it'll catch up." | Unbounded queues exhaust memory under sustained load. Pick a cap and a reject policy; let backpressure inform callers. (`RI/Backpressure`) |
| "I'll validate after the DB lookup — saves a branch." | Late failure holds DB connections, locks, and quota for a request that can't succeed. Validate at the entry; fail fast. (`RI/FailFast`) |

## What "done" looks like

You are done when **all** of the following are true for every domain below your change touches:

- [ ] **Errors:** technical and business exceptions have distinct types; no empty catches; any "magic" the change relies on has a named owner or a documented restart path.
- [ ] **Numerics:** no `==` between floats; tolerances scaled to magnitude; money uses a decimal type; subtractions of near-equal magnitudes have been audited for cancellation.
- [ ] **Concurrency & IPC:** shared mutable state is justified or replaced by message passing; remote calls per user stimulus are counted and bounded; retries have backoff, jitter, and a ceiling.
- [ ] **Limits & Performance:** the data structure matches the access pattern; no invariants recomputed inside hot loops; perf claims are measured, not reasoned.
- [ ] **Globals & Singletons:** any new singleton is justified, narrowly scoped, and accessed through an interface that can be substituted in tests.
- [ ] **Production resilience:** every remote call has an explicit timeout; critical downstreams have a circuit breaker; resource pools are bulkheaded per downstream; queues are bounded with an explicit reject policy; the request fails fast when it cannot succeed.

If any box that applies to your change is unchecked, you are not done. Either finish, or revert and re-plan.

## Principles in this skill

| # | Principle | Author |
|---|---|---|
| 97/21 | Distinguish Business Exceptions from Technical | Dan Bergh Johnsson |
| 97/26 | Don't Ignore That Error! | Pete Goodliffe |
| 97/29 | Don't Rely on "Magic Happens Here" | Alan Griffiths |
| 97/33 | Floating-Point Numbers Aren't Real | Chuck Allison |
| 97/41 | Inter-Process Communication Affects Application Response Time | Randy Stafford |
| 97/46 | Know Your Limits | Greg Colvin |
| 97/57 | Message Passing Leads to Better Scalability in Parallel Systems | Russel Winder |
| 97/73 | Resist the Temptation of the Singleton | Sam Saariste |
| 97/89 | Use the Right Algorithm and Data Structure | Jan Christiaan "JC" van Winkel |
| `RI/Timeout` | Always Set a Timeout | Michael Nygard |
| `RI/CircuitBreaker` | Circuit Breaker | Michael Nygard |
| `RI/Bulkhead` | Bulkhead | Michael Nygard |
| `RI/Backpressure` | Backpressure / Bounded Queues | Michael Nygard |
| `RI/FailFast` | Fail Fast | Michael Nygard |

See `principles.md` for the long-form distillations, citations, and source links.
