---
name: design-code-architecture
description: 'Guided journey from an app idea to a deliberate architecture: boundaries, domain model, data decisions, and resilience, making only the expensive-to-reverse decisions and deferring the rest. Orchestrates eight skills phase by phase - clean-architecture, domain-driven-design, system-design, ddia-systems, software-design-philosophy, release-it, pragmatic-programmer, 37signals-way - asking the user questions at every decision point and recording results in the project docs/ folder (ARCHITECTURE.md, RELIABILITY.md, DESIGN-CODE-ARCHITECTURE-PLAN.md) so the journey resumes across sessions. Use when the user wants to design a new app''s architecture, choose boundaries and a domain model before building, decide monolith versus microservices, or says ''how should I structure this app''. If a codebase already exists, use remove-technical-debt (aged) or improve-code-quality (fresh prototype); if the idea is not validated, run create-business or create-app first. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Design Code Architecture

Design the architecture for a new app: get the small number of expensive-to-reverse decisions right and stay aggressively simple everywhere else. This is an interactive, resumable journey of eight phases — the agent asks before every decision and records the outcome in your project's `docs/` folder, so you can stop after any phase and resume later. It runs from the most foundational and hardest-to-reverse (boundaries, domain) through the tunable (data, resilience) to the cross-cutting disciplines (complexity, reversibility, scope) you apply throughout. A weekend project uses three phases lightly; a funded team building toward launch wants the whole stack.

## Core Principle

**Architecture is the set of decisions that are expensive to reverse: make exactly those deliberately, and defer everything cheap.** This skill sequences the phases, asks the decision questions, and records every choice in `docs/`. The constituent skills carry the method — invoke them rather than improvising their frameworks. The whole strategy is to convert expensive decisions into cheap ones by putting a boundary in front of them, so the irreducibly expensive set stays small enough to get right with care.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | clean-architecture | Do source-code dependencies point inward — is the core testable with no DB, web, or framework? | Creates docs/ARCHITECTURE.md |
| 2 | domain-driven-design | Where does the business actually split, and what does each term mean? | Extends docs/ARCHITECTURE.md |
| 3 | system-design | How little system does our real load actually need? | Extends docs/ARCHITECTURE.md |
| 4 | ddia-systems | Which data model, storage engine, and consistency does each workload need? | Extends docs/ARCHITECTURE.md |
| 5 | software-design-philosophy | Is complexity hidden behind deep modules, or is this classitis? | Extends docs/TECH-DEBT.md |
| 6 | release-it | Will it degrade gracefully when a dependency is slow or down? | Creates docs/RELIABILITY.md |
| 7 | pragmatic-programmer | What thin slice proves the boundaries, and what habits keep them reversible? | Extends docs/TESTING.md + docs/TECH-DEBT.md |
| 8 | 37signals-way | What is essential for v1, and what speculative abstraction do we cut? | Extends docs/ARCHITECTURE.md + docs/TECH-DEBT.md |

## Operating Rules

1. **Resume first.** Before anything else, read `docs/DESIGN-CODE-ARCHITECTURE-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/DESIGN-CODE-ARCHITECTURE-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Invoke the phase's skill by its slug. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Every expensive-to-reverse decision gets a Decision Log row (decision, why, alternatives rejected) before any code assumes it.** Default to a modular monolith: services split only along proven bounded contexts.

## Intake

Ask these before creating the tracker:

1. What will the app do, and what is the one feature that is genuinely your competitive advantage? (frames the core subdomain in Phase 2 — where to invest deep modeling versus buy off-the-shelf)
2. What stack are you leaning toward — language, web framework, ORM, database? (gates the Phase 1 boundary and Phase 4 data decisions; treated as a detail, never the skeleton)
3. What load is realistic in year one — rough daily active users and the main actions each takes? (gates Phase 3 sizing: requirements before solutions)
4. What outbound dependencies will it call — payments, email, LLM APIs, shipping, queues? (gates the Phase 6 integration-point audit)
5. Which data is the system of record, and are there second read patterns like search, analytics, or feeds? (gates Phase 4 consistency and derived-data decisions)
6. Has anyone validated that people actually want this app? (if not, route to create-business / create-app first — do not architect an unvalidated idea)
7. How many teams will own this system, and how much of the journey do you want now? (gates the team-topologies optional phase and the Phase 8 appetite)

Phase-skip heuristics: skip Phase 3's scaling machinery and most of Phase 4's replication when year-one load is far below any threshold (a single indexed DB is the answer — record it and move on); skip the team-topologies optional phase for a single-team app. Never skip Phase 1 or Phase 2 — boundaries and the domain model are the additive work that makes every later decision cheap; Phase 6 resilience is not optional once real users and outbound calls exist. Then create the tracker from the template and confirm the plan.

Done when `docs/DESIGN-CODE-ARCHITECTURE-PLAN.md` exists with every phase statused and the user has confirmed the plan.

## Phases

Phases run in the listed order, from hardest-to-reverse to tunable to cross-cutting — each assumes the previous phase's artifact exists. Any phase can be entered, skipped, or deferred per the Operating Rules; Phases 1-2 are the additive work that makes everything after them cheap to change.

The phases form a dependency chain that mirrors the system: Domain-Driven Design says *where* the boundaries belong (contexts and aggregate seams); Clean Architecture says *which way* dependencies cross them; Data-Intensive Apps decides what lives inside them at the persistence layer; System Design says how much infrastructure that actually requires — usually far less than feared. Software Design keeps the modules deep instead of multiplying into shallow ceremony, Release It! hardens the integration points, Pragmatic Programmer supplies the cross-cutting habits that hold the structure over time, and the 37signals Way governs the whole thing by fixing time and cutting scope.

### Phase 1 — Draw the boundaries (clean-architecture)

**Purpose:** Keep business rules independent of the framework, database, and vendors so every later decision stays swappable — the move that buys back all the others.

**Brief (fallback):** The Dependency Rule — source-code dependencies point inward: Frameworks → Interface Adapters → Use Cases → Entities; nothing inner names anything outer. Database, web, and vendors are details, plugins to your rules. Enforce with Dependency Inversion: a use case owns a repository interface; the Postgres/Stripe implementation lives in an outer adapter. Draw full boundaries only at real volatility (DB, external services, delivery); collapse layers elsewhere — direction matters, not folder count.

**Invoke:** `clean-architecture` with a concrete first feature and the stack from intake. Ask it to layer that feature (entities, a use case with request/response models, repository + gateway interfaces, the HTTP controller and DB adapter in the outer ring), and to flag which boundaries are ceremony versus earning their cost at real volatility.

**Decide with the user:** (1) Modular monolith versus services — default to a modular monolith with clean internal boundaries; a microservice with a shared data model is a distributed monolith, strictly worse. (2) Which volatility points get full boundaries with interfaces now versus collapsed layers.

**Artifact:** Create docs/ARCHITECTURE.md with `## System Context` (what it does, integrations), `## Layer Map & Dependency Rule` (layers, what depends on what; violation | location | fix | status), and the monolith-versus-services choice in `## Decision Log` (date | decision | why | alternatives rejected). Update the tracker.

**Done when:** the layer map exists, the first feature is layered with framework/ORM types confined to the outer ring, the core is designed to test with no DB/web/framework, the monolith-versus-services decision is a Decision Log row, and Phase 1 shows `done`.

### Phase 2 — Model the domain (domain-driven-design)

**Purpose:** Put boundaries where the business actually splits and make the code speak the domain — cheapest now, inventing the vocabulary from a blank page.

**Brief (fallback):** The model is the code — build a Ubiquitous Language so team words are code words. Name after domain concepts (`Order.place()`, not `OrderManager.process()`); a name that resists is a design signal, not an annoyance. Bounded contexts: a region where a word means exactly one thing ("Customer" differs in billing versus support) — these are your future service seams. Aggregates: a small root cluster enforcing invariants, immediately consistent inside and eventually consistent outside; reference other aggregates by ID. Push behavior into entities — no anemic data bags.

**Invoke:** `domain-driven-design` with the domain vocabulary and the Phase 1 layer map. Ask for the bounded-context map built from the words the team actually uses, the core aggregates with their invariants, and a subdomain classification (core / supporting / generic).

**Decide with the user:** (1) Where the same word legitimately means different things across contexts — do NOT unify into one omniscient model. (2) Which subdomain is core (invest deep modeling) versus generic (buy or use OSS — auth, email, payments).

**Artifact:** Extend docs/ARCHITECTURE.md: `## Bounded Contexts & Context Map` (contexts, relationships, anti-corruption layers) and `## Domain Glossary (Ubiquitous Language)` (term | meaning | code name); record aggregate and core-domain choices in `## Decision Log`. Update the tracker.

**Done when:** contexts are mapped with their relationships, the glossary names the core terms, each aggregate states its invariants and by-ID references, the core subdomain is chosen, and the context boundaries line up with the Phase 1 layer map.

### Phase 3 — Size the system honestly (system-design)

**Purpose:** Prove with numbers how small the system can be, so you skip the machinery you cannot justify.

**Brief (fallback):** Start with requirements, not solutions. Back-of-envelope: QPS = daily-active-users × actions/day ÷ 86,400, peak 2-5× average; storage = records/day × size × retention. For hundreds-to-thousands of users, a single indexed DB plus a read-path cache carries you a long time. Scale in order: vertical first, then cache-aside (TTL + explicit invalidation), then read replicas, and shard last, only with evidence. Reach for a message queue to decouple slow/spiky work, a CDN for global static assets. Premature sharding and premature service-splitting are named mistakes.

**Invoke:** `system-design` with the load reality from intake. Ask for average and peak QPS, yearly storage, which component bottlenecks first, and a plain list of the techniques (sharding, replicas, CDN, queues, multi-region) you do NOT need yet.

**Decide with the user:** Which scaling moves to make now versus defer — tied to the numbers (don't build for 50k users while at 50) — and the first slow workload, if any, to move behind a message queue.

**Artifact:** Extend docs/ARCHITECTURE.md `## System Context` with the load reality and back-of-envelope numbers; record each scaling move (adopt now / defer with trigger) in `## Decision Log`. Update the tracker.

**Done when:** average/peak QPS and yearly storage are written down, the first bottleneck is named, and every scaling technique is either adopted with a reason or deferred with the number that would trigger it.

### Phase 4 — Make deliberate data decisions (ddia-systems)

**Purpose:** Get the layer that outlives the code right — data model, storage engine, and consistency chosen by access pattern, not habit.

**Brief (fallback):** Data outlives code. Match model to access pattern — relational for many-to-many and ad-hoc queries, document for self-contained aggregates with locality, graph for recursive traversals; storage engines trade reads against writes (LSM write-throughput versus B-tree read-latency). Most databases default to read-committed or snapshot, NOT serializable — naive read-then-write triggers write skew (two buyers taking the last unit). Lock explicitly (`SELECT ... FOR UPDATE`) or use a serializable transaction where invariants demand it. Single-leader + read replicas is the read-heavy default; replication lag forces deliberate read-your-writes. Separate system-of-record from rebuildable derived data.

**Invoke:** `ddia-systems` with the workloads implied by the Phase 2 aggregates and the Phase 3 replica plan. Ask for a per-workload model + storage-engine fit, the actual default isolation level and its anomalies, and which read-then-write paths need locking.

**Decide with the user:** (1) One datastore versus polyglot persistence, per workload fit. (2) Which paths get a lock or serializable transaction versus tolerate eventual consistency; whether a second read pattern (search, analytics) justifies derived data kept in sync by CDC.

**Artifact:** Extend docs/ARCHITECTURE.md `## Data & Storage Decisions` (models, engines, isolation level, locked paths, system-of-record versus derived) and log the reasoning in `## Decision Log`. Update the tracker.

**Done when:** each workload has a model + engine chosen by fit, the default isolation level is documented, every write-skew-prone path is locked or serializable, and any derived data has a defined sync mechanism.

### Phase 5 — Keep modules deep (software-design-philosophy)

**Purpose:** Stop the structure from becoming its own disease — hide machinery behind simple interfaces instead of shattering into shallow classes.

**Brief (fallback):** Complexity is the enemy; the test for every decision is whether it makes the whole system simpler. Module depth = functionality ÷ interface complexity — deep modules hide power behind small interfaces; shallow ones (classitis) add interface cost without hiding complexity. Clean layering and deep modules are allies; clean layering and classitis are not. Information leakage — one design decision reflected in many modules — is a top red flag; encapsulate each piece of knowledge once. Strategic over tactical: invest 10-20% to keep the design clean; startup shortcuts compound into debt as the team grows.

**Invoke:** `software-design-philosophy` with the module set proposed in Phases 1-2. Ask which modules are shallow pass-throughs to consolidate, where knowledge leaks across boundaries, and whether any planned boundary is ceremony rather than depth.

**Decide with the user:** Which shallow modules to consolidate into deeper ones now, guarding against over-merging genuinely unrelated concerns; the design conventions the team adopts (naming, where behavior lives, one file per piece of knowledge).

**Artifact:** Extend docs/TECH-DEBT.md `## Smell Inventory` (shallow-module / information-leakage entries with the consolidation applied) and record the agreed rules under `## Adopted Conventions`. Update the tracker.

**Done when:** each shallow-module cluster is consolidated or logged with a fix, no single design decision is duplicated across modules, and the design conventions are written down.

### Phase 6 — Design for failure (release-it)

**Purpose:** Make the system degrade gracefully instead of collapsing when a dependency is slow or down — cheapest to design in now, not at 2 a.m.

**Brief (fallback):** The software that passes QA is not what survives production. Integration points are the number-one killer and a slow response is worse than none — a hanging dependency exhausts threads and pools with nothing in the logs. Non-negotiable: connect + read timeouts on every outbound call; a circuit breaker on critical ones (trips open, fails fast, half-open recovery); bulkheads to isolate pools per dependency; retry with backoff + jitter. Paginate every list endpoint (unbounded result sets crash under real data); schedule steady-state cleanup. Decouple deploy from release with feature flags and backward-compatible expand-contract migrations.

**Invoke:** `release-it` with the outbound dependencies from intake. Ask for timeout values and breaker thresholds per dependency, bulkhead placement, a graceful-degradation path per integration, and the deep-health-check + RED-metrics + expand-contract-migration essentials.

**Decide with the user:** Breaker thresholds, which dependencies get dedicated pools, how core flows degrade when a non-critical dependency is down, and the rollback path you trust. Resist chaos engineering / multi-region failover for the first thousand users.

**Artifact:** Create docs/RELIABILITY.md with `## Integration-Point Audit` (dependency | timeout | circuit breaker | bulkhead | retry policy | status), `## Query & Resource Findings`, `## Health Checks & Metrics`, and `## Deploy vs Release`. Update the tracker.

**Done when:** every planned outbound call has a timeout, critical dependencies have breakers and bulkheads, every list endpoint is paginated, a deep health check + RED metrics + expand-contract migration + trusted rollback are specified, and the audit has no open rows for critical paths.

### Phase 7 — Prove the wiring and lock in habits (pragmatic-programmer)

**Purpose:** Build one thin real slice through every layer to prove the boundaries connect, and set the habits that keep the architecture reversible.

**Brief (fallback):** Tracer bullet — build one thin but fully real vertical slice (HTTP → use case → repository → DB → back), kept as production code, for end-to-end feedback on day two and proof the boundaries link before you flesh them out. Reversibility: abstract every vendor behind your own interface (forking-road test — could you swap DB or LLM provider in a week?). Orthogonality: a dramatic change to one requirement should touch one module. DRY for knowledge, not coincidence — merge duplicated rules, leave look-alikes alone. Broken Window: fix the first hack or board it up with a tracked ticket.

**Invoke:** `pragmatic-programmer` with the Phase 1 boundaries. Ask for the thinnest end-to-end tracer bullet that exercises every layer, an adapter interface for each vendor, and an audit of where one change would touch many modules or a vendor API would leak into business logic.

**Decide with the user:** Which slice is the tracer bullet (one authenticated core action, minimal functionality); the broken-windows policy and debt budget per iteration; which vendors get an owned interface first.

**Artifact:** Extend docs/TESTING.md `## Test Strategy`, `## Safety Net Map` (the tracer-bullet path as the first end-to-end test), and `## CI Gates`; extend docs/TECH-DEBT.md `## Debt Budget & Broken-Windows Policy` and `## Adopted Conventions` (reversibility, orthogonality). Update the tracker.

**Done when:** the tracer-bullet slice runs end-to-end through every layer and is pinned as the first CI gate, each vendor sits behind an owned interface, and the broken-windows policy and debt budget are written down.

### Phase 8 — Cut scope to the essential (37signals-way)

**Purpose:** Decide whether any of this ships — fix time, flex scope, and delete speculative abstraction before it becomes complexity you carry.

**Brief (fallback):** Build less — the best products do fewer things well; half a product beats a half-assed one. Fix an appetite (the time this work is genuinely worth) and cut scope to fit, rather than estimating an open-ended architecture that balloons. YAGNI: every speculative abstraction (generic plugin system, event sourcing, configurable multi-tenancy for zero users) is a decision deferred to an imaginary future at the cost of present complexity. Make tiny reversible decisions; say no by default so the great decisions breathe. Never cut the small set of expensive-to-reverse decisions.

**Invoke:** `37signals-way` with the full architecture plan from Phases 1-7. Ask it to shape the work into a fixed appetite, separate essential-for-launch from gold-plating, name the rabbit holes, and list the speculative abstractions to delete or replace with the simplest thing that could work.

**Decide with the user:** The appetite for v1 architecture work; which abstractions to cut now, defer with a revisit trigger, or replace with the simplest thing; confirm no expensive-to-reverse decision is being cut just to save time.

**Artifact:** Extend docs/ARCHITECTURE.md `## Decision Log` with what is deliberately NOT built for v1; extend docs/TECH-DEBT.md `## Debt Ledger` (deferred abstractions as deliberately-taken debt, each with the trigger that would revisit it). Update the tracker.

**Done when:** v1 scope is fixed to an appetite, every cut or deferred abstraction is a Decision Log or Debt Ledger row with a revisit trigger, and no expensive-to-reverse decision was cut for time.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| team-topologies | More than one team will own the system, so module boundaries must align with team boundaries (Conway) | Extends docs/OPERATIONS.md (`## Team Structure`) |

Optional phases follow the same operating rules; insert where the Add-when condition first becomes true — here, right after Phase 2, once the bounded contexts that team boundaries must mirror exist.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Letting the framework be the architecture | Apply Clean Architecture's Dependency Rule (Phase 1) — framework calls inward; ORM and request types stay confined to the outer ring. |
| Over-engineering for scale you cannot prove you need | Run back-of-envelope QPS/storage math first (system-design, Phase 3); one indexed DB plus a cache is usually years of runway. |
| Over-correcting into classitis | Apply the deep-module rule (software-design-philosophy, Phase 5) — a few deep modules beat a swarm of shallow ones; boundaries at real volatility only. |
| Ignoring the database's actual consistency guarantees | Check the default isolation level and lock write-skew-prone paths (ddia-systems, Phase 4) — write skew passes every single-user test. |
| Treating resilience as a post-launch concern | Design timeouts, breakers, and pagination in from the start (release-it, Phase 6) — a slow dependency with no timeout freezes everything. |
| Confusing build-less with build-carelessly | Cut features and speculative abstractions (37signals-way, Phase 8), never the small set of expensive-to-reverse decisions. |

## Completing the Journey

Match the dose to the project: a weekend build leans on the Phase 1 Dependency Rule, a quick Ubiquitous Language, timeouts on outbound calls, and the Phase 8 instinct to cut scope — a few hours that save weeks. A funded team building toward launch works the whole stack, pulling the data and resilience phases in as real bottlenecks and integration points appear.

Exit checklist — every box tied to an artifact:

- [ ] Each expensive-to-reverse decision (boundaries, contexts, data/consistency) is a Decision Log row with alternatives rejected (ARCHITECTURE.md).
- [ ] Core business rules are designed to run with no DB, web, or framework (ARCHITECTURE.md Layer Map, no inward-pointing violations).
- [ ] Every outbound call has a timeout, critical ones have breakers, and every list is paginated (RELIABILITY.md Integration-Point Audit clear).
- [ ] A tracer-bullet slice proves the boundaries connect end-to-end and is the first CI gate (TESTING.md).
- [ ] v1 scope is fixed to an appetite with speculative abstractions cut or deferred with a trigger (TECH-DEBT.md Debt Ledger).

Close the tracker: every phase `done` or `skipped: reason`, with remaining Next Actions carried into the ARCHITECTURE.md Decision Log and TECH-DEBT.md so nothing is lost. Then route forward: when the architecture serves a product that still needs validating and building, continue with `create-app`; when an existing prototype must be brought up to this structure, continue with `improve-code-quality`.
