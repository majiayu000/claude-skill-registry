---
name: improve-code-quality
description: 'Guided journey from a working-but-untested vibe-coded prototype to a production-ready product with tests, clean structure, a business-rules boundary, and resilience at scale. Orchestrates nine skills phase by phase - working-with-legacy-code, clean-code, refactoring-patterns, software-design-philosophy, clean-architecture, pragmatic-programmer, release-it, system-design, ddia-systems - asking the user questions at every decision point and recording results in the project docs/ folder (TESTING.md, TECH-DEBT.md, RELIABILITY.md, IMPROVE-CODE-QUALITY-PLAN.md) so the journey resumes across sessions. Use when the user wants to harden an AI-generated prototype, add tests before refactoring, make code safe to change, or says ''this works on my machine but I am scared to touch it''. For a large aged codebase, use remove-technical-debt; to decide structure before building, use design-code-architecture; for a product and UX pass, use improve-app. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Improve Code Quality

Turn a working-but-untested vibe-coded prototype into a product you can ship and operate. This is an
interactive, resumable journey of nine phases: the agent asks before every decision and records the
outcome in your project's `docs/` folder, so you can stop after any phase and pick up later. A
week-old prototype is already legacy code — so the first move is a safety net, and every phase after
it is verifiable because of that net.

## Core Principle

**A week-old untested prototype is already legacy code: flip tactical to strategic — safety net
first, then readability, structure, and production hardening in order.** This skill sequences the
phases, asks the decision questions, and records every choice in `docs/`. The constituent skills
carry the method — invoke them rather than improvising their frameworks. Skipping ahead (refactoring
before tests, scaling before sizing) is the exact failure mode this ordering exists to prevent.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | working-with-legacy-code | Can I change this code without breaking it unknowingly? | Creates docs/TESTING.md + docs/TECH-DEBT.md — GATE |
| 2 | clean-code | Is this readable to the next person (and agent)? | Extends docs/TECH-DEBT.md |
| 3 | refactoring-patterns | Can I reshape structure without changing behavior? | Extends docs/TECH-DEBT.md |
| 4 | software-design-philosophy | Is complexity hidden behind deep modules? | Extends docs/TECH-DEBT.md |
| 5 | clean-architecture | Do business rules depend on the framework, or vice versa? | Extends docs/ARCHITECTURE.md |
| 6 | pragmatic-programmer | What habits keep it clean after we stop? | Extends docs/TECH-DEBT.md |
| 7 | release-it | Will it survive a hostile production? | Creates docs/RELIABILITY.md |
| 8 | system-design | Is it sized for the load we actually have? | Extends docs/ARCHITECTURE.md + docs/RELIABILITY.md |
| 9 | ddia-systems | Is the data layer correct and durable under concurrency? | Extends docs/ARCHITECTURE.md |

## Operating Rules

1. **Resume first.** Before anything else, read `docs/IMPROVE-CODE-QUALITY-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/IMPROVE-CODE-QUALITY-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Invoke the phase's skill by its slug. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Phase 1 is a gate; commits stay single-purpose.** No phase touches code absent from the Safety Net Map — pin it first (absent means not listed under Pinned behaviors; entries in the Gaps column are off-limits too). Structural and behavioral changes never share a commit: refactor with tests green in a structure-only commit, then change behavior in its own commit. A test that goes red mid-refactoring means revert and retry in smaller steps, not debug. Safety-net test additions and docs/ updates are single-purpose commits of their own.

## Intake

Ask these before creating the tracker:

1. What does the app do, and what is the worst thing that happens if it breaks? (frames risk and sets phase priority)
2. Which module are you changing next, and which has the highest churn (`git log`) or is core domain? (picks the Phase 1 starting module — the three-axis heuristic)
3. Do any automated tests exist today, and does a test command run green? (scopes the Phase 1 safety net)
4. What is the stack — framework, ORM, database? (gates Phases 5 and 9 — the boundary and data decisions)
5. Is this in production with real user data, and roughly how many active users or requests? (gates Phases 7-9 — resilience is requirements-driven)
6. What outbound dependencies does it call — third-party APIs, payments, email, queues? (gates Phase 7 — the integration-point audit)
7. How much of the journey do you want now? (Phases 1-3 before real users; Phase 7 before launch; Phases 8-9 track actual growth)

Phase-skip heuristics: skip Phases 8-9 when real load is far below any scaling threshold (start with requirements, not solutions — don't build for 50k users while at 50). Phase 7 is not optional once real users exist — timeouts and a circuit breaker are table stakes even at low traffic (it may stay `deferred: reason`, never `skipped`). Never skip Phase 1; it is the gate. Then create the tracker from the template and confirm the plan.

Done when `docs/IMPROVE-CODE-QUALITY-PLAN.md` exists with every phase statused and the user has confirmed the plan.

## Phases

Phases run in the listed order — each assumes the previous phase's artifact exists. Any phase can be entered, skipped, or deferred per the Operating Rules, but Phase 1 gates them all: nothing downstream touches unpinned code.

### Phase 1 — Build the safety net (working-with-legacy-code) — GATE

**Purpose:** Pin current behavior at the change points so every later phase is verifiable. No phase may touch code absent from the Safety Net Map.

**Brief (fallback):** Legacy code is code without tests, so a week-old prototype qualifies. Cover and
modify, never edit and pray: identify change points, break inline dependencies with the
least-invasive seam (Parameterize Constructor with a production default; Extract and Override for one
buried call), then write characterization tests that photograph actual behavior — assert something
wrong, read the failure, pin the real value. When full coverage isn't feasible in time, Sprout/Wrap
the new code and track the untested host as debt.

**Invoke:** `working-with-legacy-code` with the starting module chosen at intake. Ask for an effect
sketch from the entry method, the seams, and the smallest characterization-test set that pins current
signup / billing / core behavior.

**Decide with the user:** (1) Confirm the starting module by the three-axis heuristic — changing next, high churn, core domain. (2) Bugs found while characterizing: pin the wrong behavior and file it in the Debt Ledger, never silently fix — callers may depend on the quirk. Confirm the user accepts this.

**Artifact:** Create docs/TESTING.md with `## Test Strategy`, `## Safety Net Map` (module | pinned behaviors | test files | gaps), and `## Characterization Backlog`; create docs/TECH-DEBT.md with `## Debt Ledger` (item | location | type | risk | effort | priority | status) and `## Sprout / Wrap Register`. Update the tracker.

**Done when:** the target module's behavior is pinned, the suite runs green, both files exist, and Phase 1 shows `done` — only then are later phases unlocked.

### Phase 2 — Make the code readable (clean-code)

**Purpose:** Optimize for the reader — names, small single-purpose functions, safe error handling — now that changes are verifiable.

**Brief (fallback):** Code is read far more than written. Names reveal intent (`elapsedTimeInDays`,
not `d`); booleans read as predicates; functions do one thing at one level of abstraction with 0-2
arguments (a flag argument is two functions). Command-Query Separation: change state or return a
value, never both. Error handling: prefer exceptions to return codes, catch specific types, never
return or pass null (use an empty collection, Optional, or Null Object), and put operation + state
context in every thrown error.

**Invoke:** `clean-code` with a target module. Ask for a 0-10 score across the six disciplines plus the top ten fixes in priority order, and an error-handling audit (bare catches, null returns, contextless errors).

**Decide with the user:** Which fixes to apply now versus log as debt, the naming / error-handling conventions the team adopts going forward, and whether the clean-code score becomes a CI gate.

**Artifact:** Extend docs/TECH-DEBT.md: add rows to `## Smell Inventory` (smell | location | refactoring | status) for each name / function / error smell, and record the agreed rules under `## Adopted Conventions`. Update the tracker.

**Done when:** the module scores 8+ or every gap below 8 is a Smell Inventory row with a fix, conventions are recorded, and the Phase 1 tests still pass.

### Phase 3 — Apply named refactorings (refactoring-patterns)

**Purpose:** Turn "clean it up" into named, behavior-preserving transformations executed in small steps.

**Brief (fallback):** Each smell maps to a named refactoring. Extract Method is the workhorse — if
you would write a comment to explain a block, extract it and name it after the comment. Also Replace
Magic Number with Symbolic Constant, Replace Nested Conditional with Guard Clauses, Replace
Conditional with Polymorphism, Introduce Parameter Object. Workflow: tests green, one transformation,
tests green, commit; a red test means revert, not debug. Preparatory Refactoring (make the change
easy, then make the easy change) and the Rule of Three guard against premature abstraction.

**Invoke:** `refactoring-patterns` with a smelly function and the Phase 1 tests. Ask it to name each smell, cite the transformation, and apply one at a time with tests run between each.

**Decide with the user:** Scope — which smells to address this pass, whether an upcoming feature warrants a Preparatory Refactoring at its insertion point first, and whether the refactored module joins the CI gate list in TESTING.md.

**Artifact:** Extend docs/TECH-DEBT.md `## Smell Inventory`: for each smell, record the named refactoring applied and its status. Update the tracker.

**Done when:** targeted smells show a named refactoring and `done` / `ticketed` status, tests are green, and structural changes landed in structure-only commits.

### Phase 4 — Reduce complexity with deep modules (software-design-philosophy)

**Purpose:** Fight the classitis an unsupervised agent creates — hide real machinery behind simple interfaces instead of multiplying shallow classes.

**Brief (fallback):** Complexity is the enemy; minimize what a module imposes on the rest of the
system. Module depth = functionality ÷ interface complexity; deep modules hide machinery behind small
interfaces, shallow ones don't (classitis). Merge shallow classes that always travel together and
share state. Watch information leakage (one decision reflected in many modules) and temporal
decomposition (organizing by order-of-execution, not by knowledge). This is the tactical→strategic
flip: invest 10-20% to keep the design clean.

**Invoke:** `software-design-philosophy` with the module set touched so far. Ask which classes are shallow, where information leaks across boundaries, and how to consolidate into deeper modules with simpler interfaces.

**Decide with the user:** Which consolidations to make now versus defer, guarding against over-merging unrelated concerns.

**Artifact:** Extend docs/TECH-DEBT.md `## Smell Inventory` with classitis / shallow-module / information-leakage entries and the consolidation applied. Update the tracker.

**Done when:** each shallow-module cluster is consolidated or logged with a fix, interface count did not grow for the sake of "modularity", and tests are green.

### Phase 5 — Draw the architecture boundary (clean-architecture)

**Purpose:** Make the framework and database depend on the business rules, not the reverse.

**Brief (fallback):** The Dependency Rule: source dependencies point inward — Entities, then Use
Cases, then Interface Adapters, then Frameworks/Drivers; nothing inner names anything outer. The
database and web are details, plugins to your rules. Enforce with Dependency Inversion: a Use Case
owns a repository interface; the Postgres/Stripe implementation lives in an outer adapter. SOLID are
the mid-level tools. Microservices sharing one data model are a distributed monolith — apply the rule
inside the service first.

**Invoke:** `clean-architecture` with the current module map and the stack from intake. Ask it to map the dependency graph, list every violation where business logic imports the ORM or framework, and show the extraction to framework-free Use Cases behind owned interfaces.

**Decide with the user:** How far to push the boundary this pass, which vendors (payments, storage) to wrap behind owned interfaces first, and whether any planned service split waits until the in-service boundary holds (avoid a distributed monolith).

**Artifact:** Extend docs/ARCHITECTURE.md: record layers and current violations under `## Layer Map & Dependency Rule` (violation | location | fix | status) and the boundary choices under `## Decision Log`. Update the tracker.

**Done when:** every Dependency Rule violation is a tracked row with a fix, at least the highest-risk vendor is wrapped, business-rule tests run with no framework, and tests are green.

### Phase 6 — Lock in the habits (pragmatic-programmer)

**Purpose:** Set the meta-principles that keep the codebase changeable after this journey ends.

**Brief (fallback):** DRY is about knowledge, not text — de-duplicate the same rule in two places
(validation on client and server), leave coincidental look-alikes alone. Orthogonality: changing one
component shouldn't affect another. Broken Window Theory: fix hacks immediately or board them up with
a tracked ticket — never an untracked `// TODO`. Reversibility: wrap third-party vendors behind your
own interfaces. Tracer bullets: build the next feature as one thin real end-to-end slice, not layer
by layer.

**Invoke:** `pragmatic-programmer` across the codebase. Ask it to flag duplicated knowledge (ignoring coincidental duplication) and any broken windows or untracked TODOs that need boarding up.

**Decide with the user:** The debt budget per iteration and the broken-windows policy — what gets fixed now versus ticketed.

**Artifact:** Extend docs/TECH-DEBT.md: record duplicated-knowledge and broken-window items in `## Debt Ledger`, and the agreed policy under `## Debt Budget & Broken-Windows Policy` and `## Adopted Conventions`. Update the tracker.

**Done when:** duplicated-knowledge hits are ledgered or fixed, no untracked hacks remain, and the debt-budget policy is written down.

### Phase 7 — Make it survive production (release-it)

**Purpose:** Harden every integration point so a slow or failing dependency degrades gracefully instead of taking the whole app down.

**Brief (fallback):** The software that passes QA is not what survives production. Integration points
are the number-one killer — a slow response is worse than none. Non-negotiables: connect + read
timeouts on every outbound call; a Circuit Breaker on failing dependencies (trips open, fails fast,
half-open recovery); Bulkheads to isolate resource pools; Retry with exponential backoff + jitter;
Steady State cleanup of accumulating cruft. Decouple deploy from release with feature flags and
expand-contract migrations. Add deep health checks, RED metrics, symptom-based alerts.

**Invoke:** `release-it` with the outbound dependencies from intake. Ask for an audit of calls with no timeout, circuit-breaker + bulkhead placement, and a deep health check + RED metrics + alert design.

**Decide with the user:** Breaker thresholds, which dependencies get dedicated pools, and the alert symptoms and thresholds (error rate, latency).

**Artifact:** Create docs/RELIABILITY.md with `## Integration-Point Audit` (dependency | timeout | circuit breaker | bulkhead | retry policy | status), `## Health Checks & Metrics`, and `## Deploy vs Release`. Update the tracker.

**Done when:** every outbound call has a timeout, critical dependencies have breakers and bulkheads, a deep health check + RED metrics + symptom alerts exist, steady-state cleanup is scheduled for accumulating cruft, a release can be rolled back without a redeploy, and the audit table has no open rows for critical paths.

### Phase 8 — Size for real load (system-design)

**Purpose:** Scale deliberately from requirements and numbers, not reactively — add machinery only when estimates justify it.

**Brief (fallback):** Start with requirements, not solutions. Back-of-envelope: QPS =
daily-active-users × actions/day ÷ 86,400, peak 2-5× average; storage = records/day × size ×
retention. Scale in order: vertical first, then cache (cache-aside with a TTL and explicit
invalidation) for read-heavy paths, then read replicas, and shard only as a last resort. Use a
message queue to decouple slow work from the request path. Reach for known designs (rate limiter →
token bucket returning `429 Retry-After`).

**Invoke:** `system-design` with the load reality from intake. Ask for average and peak QPS, yearly storage, which component bottlenecks first, and a priority-ordered list of cache / queue / replica moves without over-engineering.

**Decide with the user:** Which scaling moves to make now versus defer, tied to the actual numbers (don't build for 50k users while at 50), and name the first slow workload to move behind a message queue, if any.

**Artifact:** Extend docs/ARCHITECTURE.md `## System Context` with the load reality and back-of-envelope numbers; extend docs/RELIABILITY.md `## Query & Resource Findings` with unbounded queries and bottlenecks. Update the tracker.

**Done when:** the QPS and storage numbers are recorded, the first bottleneck is named, and each scaling move is either applied or deferred with the triggering number written down.

### Phase 9 — Get the data layer right (ddia-systems)

**Purpose:** Protect the data that outlives the code — correctness under concurrency, and datastore choices made by requirement, not habit.

**Brief (fallback):** Data outlives code. Most databases default to read-committed or snapshot, not
serializable — naive read-then-write triggers write skew (two requests both selling the last item).
Fix explicitly with `SELECT ... FOR UPDATE` or a serializable transaction; know your actual default.
Replication lag means read-your-writes and monotonic-reads must be deliberate once replicas exist.
Match data model to access pattern; polyglot persistence is often correct; separate system-of-record
from derived data (CDC / event sourcing) rather than dual writes.

**Invoke:** `ddia-systems` with the database from intake and the replica plan from Phase 8. Ask it to find write-skew-prone read-then-write paths, state the actual default isolation level and its anomalies, and fix the risky paths.

**Decide with the user:** Which paths need locking versus a serializable transaction, and whether a new workload (search, feed) justifies a second datastore kept in sync by CDC.

**Artifact:** Extend docs/ARCHITECTURE.md `## Data & Storage Decisions` with the isolation level, locked paths, and any polyglot / derived-data choices; log the reasoning in `## Decision Log`. Update the tracker.

**Done when:** the default isolation level is documented, every write-skew-prone path is locked or made serializable, and any new datastore has a defined sync mechanism.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| domain-driven-design | Business logic tangles because the code speaks no domain language | Extends docs/ARCHITECTURE.md (`## Bounded Contexts & Context Map`, `## Domain Glossary (Ubiquitous Language)`) |

Optional phases follow the same operating rules; insert where the Add-when condition first becomes true — here, right after Phase 5 once the boundary exists.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Cleaning up before writing a single test | Pin behavior with characterization tests in Phase 1 (working-with-legacy-code) first; the safety net gates every later phase. |
| Letting the agent "modularize" into a swarm of tiny classes | Apply software-design-philosophy's deep-module rule — merge shallow classes that travel together; reduce interfaces, don't multiply them. |
| Calling external APIs with no timeout | In Phase 7 (release-it) add connect + read timeouts on every outbound call, plus a circuit breaker on critical dependencies. |
| Scaling before sizing anything | Do back-of-envelope estimation first (system-design); the numbers usually say a cache and a read replica are years of runway. |
| Mistaking microservices for architecture | Apply the Dependency Rule inside the service first (clean-architecture); services sharing one data model are a distributed monolith. |
| Assuming the database is serializable | Check the actual default isolation level and lock read-then-write paths (ddia-systems) — write skew passes every single-user test. |

## Completing the Journey

Ship in order, not all at once: Phases 1-3 (net, readability, refactoring) belong before real users arrive; the Phase 5 boundary pays off most before the codebase doubles again; harden Phase 7 before launch (timeouts and a breaker are not optional even at low traffic); let Phases 8-9 track your actual growth numbers.

Exit checklist — every box tied to an artifact:

- [ ] Business rules have tests that run with no database or framework (TESTING.md Safety Net Map complete for changed modules).
- [ ] Every outbound call has a timeout, critical dependencies have circuit breakers, and a deep health check + RED metrics are wired to symptom-based alerts (RELIABILITY.md Integration-Point Audit clear, Health Checks & Metrics filled).
- [ ] Dependency Rule holds — business logic imports no framework or ORM (ARCHITECTURE.md Layer Map, violations closed).
- [ ] Database isolation level known and read-then-write paths locked (ARCHITECTURE.md Data & Storage Decisions).
- [ ] No untracked hacks remain; every deferred item is a Debt Ledger row with priority (TECH-DEBT.md).

Close the tracker: every phase `done` or `skipped: reason`, with remaining Next Actions carried into the TECH-DEBT.md Debt Ledger so nothing is lost. Then route forward: when the codebase is old and large rather than young and messy, continue with `remove-technical-debt`; when the next system deserves deliberate structure from day one, continue with `design-code-architecture`.
