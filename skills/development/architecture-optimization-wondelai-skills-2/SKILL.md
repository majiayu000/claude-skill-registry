---
name: architecture-optimization
description: 'Guided journey from a working codebase grown slow and tangled to one measurably fast, cleanly bounded, and readable. Orchestrates eight skills phase by phase - working-with-legacy-code, clean-architecture, software-design-philosophy, refactoring-patterns, system-design, ddia-systems, release-it, pragmatic-programmer - every phase carries its method inline so it runs standalone, asking the user questions at every decision point and recording results in the project docs/ folder (PERFORMANCE.md, ARCHITECTURE.md, ARCHITECTURE-OPTIMIZATION-PLAN.md) so the journey resumes across sessions. Use when the user wants to make an app faster, untangle drifted boundaries, fix slow endpoints and queries, or says ''it works but it is slow and getting worse''. For an untested prototype, improve-code-quality; for an aged codebase you fear to touch, remove-technical-debt; for greenfield structure, design-code-architecture; for marketing-site page speed, improve-website. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Architecture Optimization

Optimize a working codebase on three axes at once — architecture, code quality, and performance —
without breaking what works. This is an interactive, resumable journey of eight phases: the agent asks
before every decision and records the outcome in your project's `docs/` folder, so you can stop after
any phase and pick up later. It is for a system that ships and earns but has grown slow and tangled;
the structure phases make the code safe and cheap to change, the performance phases make it measurably
fast, and the closing phases keep it that way.

## Core Principle

**Measure before optimizing, pin before restructuring — the profiler and the safety net decide, not
intuition.** Premature optimization is the root of much evil not because optimization is bad, but
because unmeasured optimization targets the wrong 97% of the code; and a restructure without pinned
behavior is a gamble, not an improvement. This skill sequences the phases, asks the decision
questions, and records every choice in `docs/`. The constituent skills carry the method — invoke them
rather than improvising their frameworks.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | working-with-legacy-code | Is behavior pinned and performance measured, so every change is provable? | Creates docs/PERFORMANCE.md + docs/TECH-DEBT.md; extends docs/TESTING.md — GATE |
| 2 | clean-architecture | Do dependencies still point inward, or has the boundary drifted as the code grew? | Extends docs/ARCHITECTURE.md |
| 3 | software-design-philosophy | Are modules deep, or has the structure itself become the complexity? | Extends docs/TECH-DEBT.md |
| 4 | refactoring-patterns | Can we reshape the hot paths in named, behavior-preserving steps? | Extends docs/TECH-DEBT.md + docs/TESTING.md |
| 5 | system-design | What does the measured load say the bottleneck is, and what is the cheapest fix? | Extends docs/PERFORMANCE.md + docs/ARCHITECTURE.md |
| 6 | ddia-systems | Is the data layer the bottleneck — queries, indexes, isolation, derived data? | Extends docs/ARCHITECTURE.md + docs/PERFORMANCE.md |
| 7 | release-it | Does it stay fast and stable when a dependency is slow or down? | Creates-or-extends docs/RELIABILITY.md |
| 8 | pragmatic-programmer | What budgets and habits keep it fast and clean after we stop? | Extends docs/PERFORMANCE.md + docs/TECH-DEBT.md + docs/TESTING.md |

## Operating Rules

1. **Resume first.** Before anything else, read `docs/ARCHITECTURE-OPTIMIZATION-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/ARCHITECTURE-OPTIMIZATION-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Load the phase's skill and use it: each phase's Invoke line names the skill by slug — use that skill to run the phase. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Never optimize unmeasured, never restructure unpinned.** Every change made to reduce a measured baseline cites that baseline and lands in the PERFORMANCE.md Optimization Ledger with before/after — one that doesn't move its number gets reverted, not kept. (Resilience and gating work — timeouts, breakers, bulkheads, pagination, CI gates — is judged by the Done-when of its own phase, not by a latency delta.) Structural changes touch only code pinned in the Safety Net Map, preserve behavior, and land in structure-only commits separate from behavior and optimization commits.

## Intake

Ask these before creating the tracker:

1. **What does the system do, and what does "too slow" cost** — lost users, SLA breaches, infra bills? (Frames which metric matters and how much effort the journey is worth.)
2. **What is the evidence so far** — APM traces, slow-query logs, p95 latencies, a cloud bill, or just complaints? (Feeds the Phase 1 baseline; complaints alone mean instrumentation comes first.)
3. **Which flows or endpoints hurt most, and which modules implement them?** (Picks the hot paths every phase works on.)
4. **Do automated tests exist and run green?** (Scopes the Phase 1 safety net — unpinned hot paths get pinned before anything touches them.)
5. **What is the stack** — language, framework, ORM, database, cache — and where does it run? (Gates Phases 5-6.)
6. **What are the real load numbers** — QPS average and peak, data volumes, growth rate? (Gates Phase 5 — sizing by numbers, not fear.)
7. **How much of the journey do you want now?** (Phases 1-4 make it safe and clean to change; 5-6 make it fast; 7-8 keep it that way.)

Skip heuristics: compress Phases 2-3 to an audit-only pass when the structure is sound and the pain is purely performance — record what the audit found either way and status the phase `done` with an "audit only, no changes" note; skip Phase 7 only when a prior journey's RELIABILITY.md Integration-Point Audit is verifiably current (check the file, don't assume). Never skip Phase 1 — an optimization without a baseline is a guess, and a restructure without a net is a gamble.

Then create `docs/ARCHITECTURE-OPTIMIZATION-PLAN.md` from the template and confirm the plan. Done when the tracker exists with every phase statused and the user has confirmed the plan.

## Phases

Phases run in the listed order — each assumes the previous phase's artifact exists. Structure before speed is deliberate: Phases 2-4 make the hot paths safe and cheap to change, which is what makes the Phase 5-6 optimizations small diffs instead of surgery. Any phase can be entered, skipped, or deferred per the Operating Rules, but Phase 1 gates them all — as two independent nets: pinned behavior unlocks Phases 2-4, and a recorded baseline unlocks Phases 5-6, so structure work need not wait on a profile that takes weeks to gather. Phases 5 and 6 may be swapped when the Phase 1 profile shows the database dominating: fixing an N+1 or a missing index before adding a cache is the skill's own cheapest-first law. When running any phase from its Brief (constituent skill not installed), read [references/methods.md](references/methods.md) first — it carries each phase's full method, checklists, formulas, and heuristics; the Brief is only the summary.

### Phase 1 — Pin it and measure it (working-with-legacy-code) — GATE

**Purpose:** Make every later change provable twice over — behavior pinned by tests, performance pinned by numbers. No phase touches unpinned code or optimizes an unmeasured path.

**Brief (fallback):** Two nets. Behavior: code without tests is legacy code — cover and modify, never
edit and pray. Find the change points on the hot paths, break inline dependencies at the
least-invasive seam (Parameterize Constructor with a production default; Extract and Override for one
buried call), and write characterization tests that photograph actual behavior — assert something
wrong, read the failure, pin the real value. Performance: profile before touching anything — the
bottleneck is rarely where intuition points. Record p50/p95/p99 latency, throughput, and resource use
per hot flow under realistic data volumes (dev-database timings lie), and work the USE method (Gregg)
per resource: Utilization, Saturation, Errors for CPU, memory, disk, network, and connection pools.
Set the budget each metric must meet, so "done" is a number, not a feeling.

**Invoke:** Use the `working-with-legacy-code` skill with the hot-path modules from intake. Ask for the seams and the smallest characterization-test set that pins current behavior of each flow to be optimized; then capture profiler or APM baselines for those flows.

**Decide with the user:** (1) Confirm the hot paths in scope — measured pain, not suspicion. (2) The budget per metric (e.g. checkout p95 < 500ms) and the tool of record (profiler, APM, load test) so before/after numbers stay comparable. (3) Bugs found while characterizing: pin the current behavior and ledger them, never silently fix — callers may depend on the quirk.

**Artifact:** Extend docs/TESTING.md `## Safety Net Map` and `## Characterization Backlog`; create docs/PERFORMANCE.md with `## Baselines & Budgets`, `## Load Reality`, `## Profile Findings`, and `## Optimization Ledger`; create-or-extend docs/TECH-DEBT.md `## Debt Ledger` and `## Sprout / Wrap Register` for bugs pinned as-is and untested hosts. Update the tracker.

**Done when:** every in-scope flow has pinned behavior (suite green) — which unlocks Phases 2-4 — and a recorded baseline with a budget, which unlocks Phases 5-6. Record the two separately; a profile still being gathered parks at `awaiting-evidence` with a Next Actions row rather than blocking the structure phases.

### Phase 2 — Re-draw the drifted boundaries (clean-architecture)

**Purpose:** Restore the Dependency Rule the codebase grew away from — mixed concerns are why changes feel risky and why the slow parts can't be optimized in isolation.

**Brief (fallback):** Source dependencies point inward: Frameworks → Interface Adapters → Use Cases →
Entities; nothing inner names anything outer. In a grown codebase the drift is concrete: business
logic importing the ORM, controllers computing domain rules, a vendor SDK called from everywhere. Map
the actual dependency graph and list the violations; extract the hot-path business rules into
framework-free use cases behind owned interfaces (Dependency Inversion) — this also enables Phases
5-6, because a boundary is where a cache or a queue can later be inserted without surgery. Draw full
boundaries only at real volatility (DB, external services, delivery); collapse ceremony layers
elsewhere — direction matters, not folder count.

**Invoke:** Use the `clean-architecture` skill with the module map and stack from intake. Ask for the dependency graph, every violation where business logic names the framework, ORM, or a vendor, and the extraction plan for the hot-path use cases — flagging which boundaries earn their cost.

**Decide with the user:** How far to push the boundary this pass — hot paths first, never a big-bang re-layering; which vendor gets wrapped behind an owned interface first; which violations get fixed now versus ledgered.

**Artifact:** Extend docs/ARCHITECTURE.md `## Layer Map & Dependency Rule` (violation | location | fix | status) and `## Decision Log`. Update the tracker.

**Done when:** the dependency graph is mapped, every violation is a tracked row, the hot-path business rules run in tests with no framework, and the suite is green.

### Phase 3 — Deepen the modules (software-design-philosophy)

**Purpose:** Cut the complexity tax — a grown codebase accretes shallow classes and leaked decisions, and every one of them slows the team down before it slows the code down.

**Brief (fallback):** Module depth = functionality ÷ interface complexity. Merge shallow pass-through
classes that always travel together and share state; hide each design decision in exactly one place —
information leakage (one decision reflected in many modules) is the top red flag; replace temporal
decomposition (modules organized by order-of-execution) with modules organized by knowledge.
Same-abstraction pass-throughs across layers signal a boundary that isn't earning its cost. This is
the tactical→strategic flip: invest 10-20% now so every later phase touches fewer files. Consolidation
also collapses call-chain ceremony on hot paths — but readability, not nanoseconds, is the reason.

**Invoke:** Use the `software-design-philosophy` skill with the modules mapped in Phase 2. Ask which classes are shallow, where one decision leaks across modules, and for a consolidation plan into deeper modules with smaller interfaces.

**Decide with the user:** Which consolidations happen now versus ledgered — guarding against over-merging genuinely unrelated concerns; the design conventions the team adopts going forward.

**Artifact:** Extend docs/TECH-DEBT.md `## Smell Inventory` (shallow-module and information-leakage entries with the consolidation applied) and `## Adopted Conventions`. Update the tracker.

**Done when:** each shallow-module cluster is consolidated or ledgered with a fix, every identified leaked decision is consolidated or a Smell Inventory row, and the suite is green.

### Phase 4 — Refactor the hot paths (refactoring-patterns)

**Purpose:** Reshape the code you're about to optimize with named, behavior-preserving transformations — clean first, then fast, because you can't safely optimize what you can't safely change.

**Brief (fallback):** Each smell maps to a named refactoring: Extract Method for comment-sized blocks;
Replace Nested Conditional with Guard Clauses; Replace Conditional with Polymorphism; Introduce
Parameter Object; Replace Temp with Query. Workflow: tests green → one transformation → tests green →
commit; a red test means revert, not debug. Fold in the clean-code disciplines as you pass: names that
reveal intent, functions doing one thing at one level of abstraction, no null returns, errors carrying
operation and state context. Preparatory Refactoring is the bridge to Phases 5-6: before each
optimization, first make the change easy (restructure), then make the easy change (optimize) — in
separate commits.

**Invoke:** Use the `refactoring-patterns` skill with the hot-path modules and the Phase 1 tests. Ask it to name each smell, cite the transformation, and apply one at a time with tests run between each.

**Decide with the user:** Scope — which smells this pass versus ledgered; which upcoming optimization warrants a Preparatory Refactoring at its insertion point first; whether the refactored modules join the CI gate list in TESTING.md.

**Artifact:** Extend docs/TECH-DEBT.md `## Smell Inventory` (smell | location | refactoring | status); extend docs/TESTING.md `## CI Gates` with any module promoted to the gate list. Update the tracker.

**Done when:** targeted smells show a named refactoring and `done` / `ticketed` status, tests are green, and structural commits contain no behavior changes.

### Phase 5 — Attack the measured bottleneck (system-design)

**Purpose:** Spend optimization effort where the profile says the time goes, in cheapest-first order, sized by real numbers.

**Brief (fallback):** Amdahl's law caps every win: total speedup is bounded by the fraction of time
the optimized part actually consumes — a 10× win on 5% of the request saves 4.5%. The profile, not
the code review, picks the target. Back-of-envelope the load (QPS = daily-active-users × actions/day ÷
86,400, peak 2-5× average) and confirm the gap against the budget. Then fix in order: the algorithm
first (an O(n²) loop or chatty per-item I/O beats any infrastructure), vertical headroom, cache-aside
with a TTL and explicit invalidation on read-heavy paths (measure the hit rate — a cold cache is pure
overhead), a message queue to move slow work off the request path (Little's law: in-flight requests =
arrival rate × latency, so cutting latency is also a capacity fix), then read replicas — and shard
only with evidence. Re-measure after every change; keep what moves the number, revert what doesn't.

**Invoke:** Use the `system-design` skill with the Phase 1 profile and the load numbers from intake. Ask which component bottlenecks first, the cheapest ordered list of moves for the measured gap, and the machinery you explicitly do NOT need yet.

**Decide with the user:** Which moves ship now versus defer with the trigger number written down; the first workload, if any, to move behind a queue; the invalidation rule for each cached path — what event invalidates which key.

**Artifact:** Extend docs/PERFORMANCE.md `## Profile Findings` and `## Optimization Ledger` (change | before | after | verdict | date); extend docs/ARCHITECTURE.md `## Decision Log` (each adopt/defer with its trigger) and `## System Context`, which cites PERFORMANCE.md `## Load Reality` rather than repeating the numbers. Update the tracker.

**Done when:** the bottleneck is named from the profile, each move is applied with before/after in the ledger or deferred with a trigger, and no adopted move failed to beat its baseline.

### Phase 6 — Fix the data layer (ddia-systems)

**Purpose:** The database is the usual suspect — most measured slowness is queries, and most correctness debt is isolation assumptions. Fix both by evidence.

**Brief (fallback):** Read the query plans, not the ORM code. The classics: N+1 queries (one per row —
batch or join; ORMs generate these silently), missing indexes on real access paths (EXPLAIN the slow
queries; index predicate and sort columns, but every index taxes writes), unbounded result sets
(paginate every list), SELECT * over wide rows, and deep offset pagination (use keyset). Storage
engines trade reads against writes (LSM write-throughput versus B-tree read-latency) — match the model
to the access pattern before buying hardware. Correctness under concurrency: most databases default to
read-committed or snapshot, not serializable — read-then-write paths get write skew; lock explicitly
(`SELECT ... FOR UPDATE`) or use a serializable transaction where invariants demand it. A second read
pattern (search, analytics, feeds) justifies derived data kept in sync by CDC — never dual writes; and
replicas from Phase 5 force deliberate read-your-writes.

**Invoke:** Use the `ddia-systems` skill with the Phase 1 profile, the Phase 5 findings, and the database from intake. If no query-level source exists yet, enable one first (`pg_stat_statements`, `auto_explain`, slow-query log) — that is Phase 1 instrumentation deferred, not a reason to guess. Ask for a query-plan audit (N+1s, missing indexes, unbounded reads), the actual default isolation level and its anomalies on your paths, and a per-workload model and engine fit.

**Decide with the user:** Which indexes to add, weighing write cost; which paths get locks versus serializable transactions versus tolerated anomalies; whether any workload justifies a second datastore synced by CDC.

**Artifact:** Extend docs/ARCHITECTURE.md `## Data & Storage Decisions` and `## Decision Log`; extend docs/PERFORMANCE.md `## Profile Findings` and `## Optimization Ledger` with query before/afters. Update the tracker.

**Done when:** the slow queries are fixed with measured before/after, every list endpoint on the in-scope flows is paginated (the rest become Debt Ledger rows), the isolation level is documented with risky paths locked, and any derived data has a defined sync mechanism.

### Phase 7 — Keep it fast when things fail (release-it)

**Purpose:** A fast system that collapses under a slow dependency isn't fast — latency under failure is a performance property.

**Brief (fallback):** Integration points are the number-one killer, and a slow response is worse than
none: one hanging dependency exhausts threads and pools with nothing in the logs. Non-negotiables:
connect + read timeouts on every outbound call (a timeout is a latency budget); circuit breakers on
critical dependencies (fail fast beats waiting); bulkheads so one slow dependency can't drain the
shared pool; retry with exponential backoff and jitter (naive retries triple load exactly when the
dependency is dying); steady-state cleanup for logs, temp data, and caches that grow forever. Wire RED
metrics (rate, errors, duration) per endpoint and alert on symptoms (p95 over budget) — the Phase 1
budgets become production guardrails instead of a one-time snapshot.

**Invoke:** Use the `release-it` skill with the outbound dependencies from intake and the budgets from Phase 1. Ask for timeout values derived from the flow latency budgets, breaker and bulkhead placement, and the RED-metrics plus symptom-alert design.

**Decide with the user:** Timeout and breaker thresholds per dependency, tied to the flow budget; which dependencies get dedicated pools; how each core flow degrades when a non-critical dependency is down.

**Artifact:** Create-or-extend docs/RELIABILITY.md `## Integration-Point Audit` (dependency | timeout | circuit breaker | bulkhead | retry policy | status), `## Query & Resource Findings`, and `## Health Checks & Metrics`. Update the tracker.

**Done when:** every outbound call on the in-scope flows has a timeout inside its flow's budget (calls outside them become Debt Ledger rows), critical dependencies have breakers and bulkheads, unbounded result sets and blocked threads are recorded in `## Query & Resource Findings`, and RED metrics with symptom alerts guard the Phase 1 budgets in production.

### Phase 8 — Lock in budgets and habits (pragmatic-programmer)

**Purpose:** Make the gains permanent — regressions arrive one innocent commit at a time unless a gate catches them.

**Brief (fallback):** Turn each Phase 1 budget into a CI gate: perf tests or query-count assertions on
the hot paths, where a p95 budget breach fails the build like a failing test. DRY is about knowledge:
the same rule computed in two places will drift — and the same query issued from two layers is both a
bug farm and a performance tax. Broken Window Theory: the first unreviewed slow query or skipped index
gets fixed or ticketed immediately, never left as ambient decay. Reversibility: vendors and
infrastructure behind owned interfaces, so the next optimization — swapping the cache, changing the
queue — stays a week's work instead of a rewrite. Set the debt budget per iteration and write the
conventions down; the ledger, not memory, carries what was deferred.

**Invoke:** Use the `pragmatic-programmer` skill across the touched modules. Ask for duplicated-knowledge hits (including duplicated queries and rules), untracked TODOs and broken windows, and a CI-gate design for the performance budgets.

**Decide with the user:** Which budgets become blocking CI gates versus dashboard alerts; the debt budget per iteration; the broken-windows policy — what gets fixed now versus ticketed.

**Artifact:** Extend docs/PERFORMANCE.md `## Baselines & Budgets` (mark each budget's gate); extend docs/TECH-DEBT.md `## Debt Budget & Broken-Windows Policy` and `## Adopted Conventions`; extend docs/TESTING.md `## CI Gates`. Update the tracker.

**Done when:** each hot-path budget is a CI gate or an owned alert, duplicated knowledge is fixed or ledgered, and the conventions are written down.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| clean-code | readability is poor beyond the hot paths — the whole codebase needs the naming, function, and error-handling pass | Extends docs/TECH-DEBT.md `## Smell Inventory`, `## Adopted Conventions` |
| domain-driven-design | boundaries keep fighting the business language — modules split where the domain doesn't | Extends docs/ARCHITECTURE.md `## Bounded Contexts & Context Map`, `## Domain Glossary (Ubiquitous Language)` |
| high-perf-browser | the measured slowness is in the browser — page load, LCP, blocking resources — not the backend | Extends docs/METRICS.md `## Baselines & Targets`, docs/WEBSITE.md `## Audit Findings` |
| team-topologies | more than one team owns the system, so module boundaries must align with team boundaries (Conway) | Extends docs/OPERATIONS.md `## Team Structure` |

Optional phases follow the same operating rules — load and use each listed skill exactly as a core phase would; insert where the Add-when condition first becomes true. They carry no inline Brief: standalone, run clean-code as a naming, function-size, and error-handling pass, domain-driven-design as a ubiquitous-language and bounded-context map, high-perf-browser as a Core Web Vitals audit (LCP, INP, CLS), and team-topologies as a cognitive-load and team-boundary review — or install the named skill for its full framework.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Optimizing where intuition points instead of where the profiler does | Profile first (Phase 1); Amdahl's law caps any win by the fraction of time that code actually consumes. |
| Rewriting for speed without a safety net | Pin behavior with characterization tests first (working-with-legacy-code); a fast wrong answer is still wrong. |
| Keeping an optimization that didn't move the number | Every change gets before/after in the Optimization Ledger; revert what doesn't beat its baseline — complexity without payoff is pure debt. |
| Reaching for infrastructure before fixing the algorithm | An O(n²) loop or an N+1 query beats any cache; fix the code, then size the machinery (system-design). |
| Caching without an invalidation rule | Stale-data bugs cost more than the latency saved; every cached path names what event invalidates which key. |
| Trusting the ORM to write good SQL | EXPLAIN the slow queries (ddia-systems); N+1s and missing indexes hide behind innocent-looking code. |
| Calling it fast with no timeout on outbound calls | Latency under failure is a performance property (release-it); one hanging dependency erases every optimization. |

## Completing the Journey

Match the dose to the pain: a slow-endpoint complaint may need only Phases 1, 5, and 6 — baseline, bottleneck, queries — a few days that pay immediately; a codebase where every change is slow and risky wants the structure phases first, because clean boundaries are what make the optimizations small. Either way the ledger keeps score: kept changes beat their baselines, everything else was reverted.

Exit checklist — every box tied to an artifact:

- [ ] Every phase in `docs/ARCHITECTURE-OPTIMIZATION-PLAN.md` is `done`, `deferred: reason`, or `skipped: reason`.
- [ ] Every hot flow has a baseline, a budget, and a current measurement inside it (PERFORMANCE.md Baselines & Budgets).
- [ ] Every kept optimization shows measured before/after; nothing kept failed its baseline (PERFORMANCE.md Optimization Ledger).
- [ ] Dependency Rule violations on the hot paths are closed or tracked rows (ARCHITECTURE.md Layer Map).
- [ ] Slow queries are fixed by plan, lists are paginated, the isolation level is documented, and risky paths are locked (ARCHITECTURE.md Data & Storage Decisions).
- [ ] Every outbound call has a timeout and the budgets are guarded by RED metrics and alerts — or CI gates (RELIABILITY.md, TESTING.md CI Gates).

Close the tracker: remaining Next Actions carried into the PERFORMANCE.md ledger and TECH-DEBT.md so nothing is lost. Then route forward: when the pain is fear of change rather than speed, continue with the `remove-technical-debt` skill; when a fresh untested prototype needs the full production pass, `improve-code-quality`; when the next system deserves this structure from day one, `design-code-architecture`.
