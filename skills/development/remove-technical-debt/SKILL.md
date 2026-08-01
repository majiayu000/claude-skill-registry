---
name: remove-technical-debt
description: 'Guided journey from a large aged codebase everyone fears to touch to one that is safe to change, legible, bounded, and resilient - paid down in place without a rewrite. Orchestrates eight skills phase by phase - working-with-legacy-code, refactoring-patterns, clean-code, software-design-philosophy, clean-architecture, pragmatic-programmer, release-it, domain-driven-design - asking the user questions at every decision point and recording results in the project docs/ folder (TESTING.md, TECH-DEBT.md, REMOVE-TECHNICAL-DEBT-PLAN.md) so the journey resumes across sessions. Use when the user wants to tame a legacy codebase, pay down technical debt safely, avoid a big-bang rewrite, or says ''we are afraid to touch this code''. For a fresh prototype or vibe-coded app going to production, use improve-code-quality; for greenfield structure, use design-code-architecture; for a product-and-UX pass rather than code-only, use improve-app. For one framework in isolation, invoke that skill directly.'
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
---

# Remove Technical Debt

Take a large, aged, tangled codebase that everyone is afraid to touch and pay its debt down in place — no big-bang rewrite, the old system always shipping. The instinct to rewrite is the one reliable way to turn a struggling-but-shipping product into a struggling-and-not-shipping one; this journey is the alternative. It is interactive and resumable across eight phases: the agent asks before every decision and records the outcome in your project's `docs/` folder, so you can stop after any phase and pick up later. The first phase builds a safety net at your change points; every phase after it is verifiable because that net exists.

## Core Principle

**Feedback over fear: cover and modify, never edit and pray — pay debt down in place on the paths you actually walk, and never stop shipping.** This skill sequences the phases, asks the decision questions, and records every choice in `docs/`. The constituent skills carry the method — invoke them rather than improvising their frameworks. You do not pay down a mountain of debt by rebuilding the mountain; you pay it down one safe, tested step at a time along the paths you already change. Skipping ahead — cleaning before the safety net, splitting services before the boundaries are real — is the exact failure mode this ordering exists to prevent.

## Journey Map

| Phase | Skill | Question it answers | Artifact |
|---|---|---|---|
| 1 | working-with-legacy-code | Can I change this code without breaking it unknowingly, and where do I start? | Creates docs/TESTING.md + docs/TECH-DEBT.md — GATE |
| 2 | refactoring-patterns | Can I reshape structure without changing behavior? | Extends docs/TECH-DEBT.md |
| 3 | clean-code | Is what I touch legible to the next reader and agent? | Extends docs/TECH-DEBT.md |
| 4 | software-design-philosophy | Is complexity hidden behind deep modules? | Extends docs/TECH-DEBT.md |
| 5 | clean-architecture | Do business rules depend on the framework, or vice versa? | Extends docs/ARCHITECTURE.md |
| 6 | pragmatic-programmer | What habits stop debt from re-accumulating? | Extends docs/TECH-DEBT.md |
| 7 | release-it | Will it survive a hostile production? | Extends docs/RELIABILITY.md |
| 8 | domain-driven-design | How do I carve the monolith into bounded contexts? | Extends docs/ARCHITECTURE.md |

## Operating Rules

1. **Resume first.** Before anything else, read `docs/REMOVE-TECHNICAL-DEBT-PLAN.md` and every artifact in the Journey Map. If the tracker exists, summarize the journey state in 3-5 lines and ask which phase to enter. Done when the user has confirmed an entry point. A journey with a tracker is resumed, never restarted.
2. **Intake on first run only.** No tracker: run the Intake below, then create `docs/REMOVE-TECHNICAL-DEBT-PLAN.md` with every phase statused `pending | in-progress | awaiting-evidence | done | deferred: reason | skipped: reason`. Done when the tracker exists and the user has confirmed the phase plan.
3. **Phase entry.** Announce: what the phase does, the decision it forces, the artifact it produces, rough effort. Offer proceed / skip / defer — phases marked GATE may be deferred, never skipped. Mark the phase `in-progress` on proceed. Done when the user chose.
4. **Skill invocation and fallback.** Invoke the phase's skill by its slug. If it is not available, offer: `npx skills add wondelai/skills/<slug> --global`. If the user declines, run the phase from its Brief — the minimum viable method. State which mode you are in.
5. **In-phase decisions.** Ask every question under "Decide with the user" — with concrete options and your recommendation. Record the choice in the tracker's Key Decisions. A decision made silently is a defect.
6. **Phase exit.** Present the draft artifact content for sign-off before writing. On approval: write or extend the docs/ files, update the tracker (status, Key Decisions, Next Actions). Done when the files are written and the phase row shows `done`.
7. **Artifact discipline.** Read before writing; create a file only if missing, otherwise extend — add or update your sections, preserve everyone else's. Files are UPPERCASE in `docs/`. Every recommendation lands as a checkbox or a table row with owner and priority. See [references/artifact-templates.md](references/artifact-templates.md) when creating a docs/ file for the first time — create it from the full skeleton (all section headings), then fill the sections your phase names.
8. **Phase 1 is a GATE, commits stay single-purpose, and found bugs get pinned not fixed.** No transformation touches code absent from the Safety Net Map — pin it first (absent means not listed under Pinned behaviors; entries in the Gaps column are off-limits too). Structural and behavioral changes never share a commit: refactor with tests green in a structure-only commit, then change behavior in its own commit; a red test mid-refactoring means revert, not debug; safety-net test additions and docs/ updates are single-purpose commits of their own. Bugs found while characterizing get pinned and ticketed in the Debt Ledger, never silently fixed — callers may depend on the quirk.

## Intake

Ask these before creating the tracker:

1. What does the system do, how large and old is it, and what is the worst thing that happens if it breaks? (frames risk and sets phase priority)
2. Which file are you changing next, and which files show up most in `git log` churn or are core domain? (picks the Phase 1 starting module — the three-axis heuristic)
3. Does a test suite exist, does it run green in CI today, or was it disabled as flaky? (scopes the Phase 1 safety net)
4. What is the stack — framework, ORM, database — and is business logic tangled inside controllers or ORM models? (gates Phase 5 boundary work and Phase 8 context mapping)
5. Is it in production with real users, and what outbound dependencies does it call — third-party APIs, payments, email, queues? (gates Phase 7 integration-point audit)
6. Is anyone proposing a big-bang rewrite? (surfaces the decision this journey exists to replace with the incremental path)
7. How much of the journey do you want now? (Phases 1-3 change the team's relationship with the code fastest; 5-8 as boundaries and decomposition become the bottleneck)

Phase-skip heuristics: skip Phase 8 when the codebase is small enough that a single model still fits comfortably. Add optional system-design or ddia-systems only when paydown surfaces real scaling or data-layer limits — start from requirements, not solutions. Phase 7 is not optional once real users exist — timeouts and a circuit breaker are table stakes (it may stay `deferred: reason`, never `skipped`). Never skip Phase 1; it is the gate. Then create the tracker from the template and confirm the plan.

Done when `docs/REMOVE-TECHNICAL-DEBT-PLAN.md` exists with every phase statused and the user has confirmed the plan.

## Phases

### Phase 1 — Build the safety net and find where to start (working-with-legacy-code) — GATE

**Purpose:** Pin current behavior at your change points and map blast radius, so every later phase is verifiable. No phase may touch code absent from the Safety Net Map.

**Brief (fallback):** Legacy code is code without tests — cover and modify, never edit and pray. Run the Legacy Code Change Algorithm: identify change points, find test points, break dependencies with the least-invasive seam (Parameterize Constructor with a production default; Extract Interface), write characterization tests that pin actual behavior (assert something wrong, read the failure, pin the real value), then change. Bound blast radius with an effect sketch; find the pinch point where a few tests cover the most behavior. Urgent change you can't cover in time: Sprout/Wrap and track the untested host as debt.

**Invoke:** `working-with-legacy-code` with the starting module chosen at intake. Ask for an effect sketch from the entry method, the pinch points, the seams to break, and the smallest characterization-test set that pins current behavior.

**Decide with the user:** (1) Confirm the starting module by the three-axis heuristic — changing next, high churn (`git log`), core domain. (2) Bugs found while characterizing: pin the wrong behavior and file it in the Debt Ledger, never silently fix — callers may depend on the quirk. Confirm the user accepts this.

**Artifact:** Create docs/TESTING.md with `## Test Strategy`, `## Safety Net Map` (module | pinned behaviors | test files | gaps), and `## Characterization Backlog`; create docs/TECH-DEBT.md with `## Debt Ledger` (item | location | type | risk | effort | priority | status) and `## Sprout / Wrap Register`, registering any sprouted or wrapped code. Record the effect-sketch pinch points under `## Test Strategy`. Update the tracker.

**Done when:** the target module's behavior is pinned, the suite runs green, both files exist, and the tracker shows Phase 1 done — only then is Phase 2 unlocked.

### Phase 2 — Restructure with named refactorings (refactoring-patterns)

**Purpose:** Turn "clean it up" into named, behavior-preserving transformations applied one small step at a time.

**Brief (fallback):** Refactoring is not rewriting: small behavior-preserving transformations, each backed by tests. Each smell maps to a named refactoring — Extract Method is the workhorse (if you'd write a comment to explain a block, extract it and name it after the comment). Also Replace Nested Conditional with Guard Clauses, Replace Conditional with Polymorphism, Introduce Parameter Object, Extract Class. Workflow: tests green, one transformation, tests green, commit; a red test means revert, not debug. Branch by Abstraction migrates large structures in production; Preparatory Refactoring makes the change easy first; Rule of Three guards against premature abstraction.

**Invoke:** `refactoring-patterns` with a smelly module and the Phase 1 tests. Ask it to name each smell, cite the transformation, and apply one at a time with tests run between each; for a large migration ask for a Branch by Abstraction plan.

**Decide with the user:** Scope — which smells this pass; whether an upcoming feature warrants a Preparatory Refactoring at its insertion point first; and whether a big migration should go behind a Branch by Abstraction.

**Artifact:** Extend docs/TECH-DEBT.md `## Smell Inventory` (smell | location | refactoring | status): one row per smell with the named refactoring applied and its status. Update the tracker.

**Done when:** targeted smells show a named refactoring and `done` / `ticketed` status, tests are green, and every structural change landed in a structure-only commit.

### Phase 3 — Raise legibility where you touch the code (clean-code)

**Purpose:** Optimize for the reader — names, small single-purpose functions, safe error handling — on the regions you are already changing.

**Brief (fallback):** Code is read far more than written (10:1+). Names reveal intent (`elapsedTimeInDays`, not `d`); booleans read as predicates; one word per concept; functions do one thing at one level of abstraction with 0-2 arguments (a flag argument is two functions). Command-Query Separation: change state or return a value, never both. Error handling is where legacy incidents hide: prefer exceptions to return codes, catch specific types, never return or pass null (empty collection, Optional, Null Object), wrap noisy third-party APIs behind an adapter, put operation + state in every error. Boy Scout Rule: leave code cleaner than you found it.

**Invoke:** `clean-code` with a target module. Ask for a 0-10 score across the six disciplines, the top ten fixes in priority order, and an error-handling audit (bare catches, null returns, contextless errors, unwrapped third-party SDKs).

**Decide with the user:** Which fixes to apply now versus log as debt, and the naming / error-handling conventions the team adopts going forward.

**Artifact:** Extend docs/TECH-DEBT.md: add `## Smell Inventory` rows for each name / function / error smell, and record the agreed rules under `## Adopted Conventions`. Update the tracker.

**Done when:** the module scores 8+ or every gap below 8 is a Smell Inventory row with a fix, conventions are recorded, and the Phase 1 tests still pass.

### Phase 4 — Reduce complexity with deep modules (software-design-philosophy)

**Purpose:** Attack the complexity itself — hide real machinery behind simple interfaces instead of the classitis an unsupervised agent creates.

**Brief (fallback):** Complexity is the enemy; judge every change by whether it raises or lowers overall complexity. Symptoms: change amplification, cognitive load, unknown unknowns. Module depth = functionality ÷ interface complexity; deep modules hide machinery behind small interfaces, shallow ones don't (classitis) — merge shallow classes that always travel together. Watch information leakage (one decision reflected across many modules) and temporal decomposition (organizing by order-of-execution, not by knowledge). This is the tactical→strategic flip: invest 10-20% to keep the design clean.

**Invoke:** `software-design-philosophy` with the module set touched so far. Ask which classes are shallow, where a design decision leaks across modules, and how to consolidate into deeper modules with simpler interfaces — with each change labeled as raising or lowering complexity.

**Decide with the user:** Which consolidations to make now versus defer, guarding against over-merging genuinely unrelated concerns.

**Artifact:** Extend docs/TECH-DEBT.md `## Smell Inventory` with classitis / shallow-module / information-leakage entries and the consolidation applied. Update the tracker.

**Done when:** each shallow-module cluster is consolidated or logged with a fix, interface count did not grow for the sake of "modularity", and tests are green.

### Phase 5 — Draw the dependency boundary (clean-architecture)

**Purpose:** Make the framework and database depend on the business rules, module by module — not the reverse.

**Brief (fallback):** The Dependency Rule: source dependencies point inward — Entities, Use Cases, Interface Adapters, Frameworks/Drivers; nothing inner names anything outer. Database and web are details, plugins to your rules. Enforce with Dependency Inversion: a Use Case owns a repository interface; the Postgres/Stripe implementation lives in an outer adapter. SOLID are the mid-level tools; Common Closure and Acyclic Dependencies find real boundaries. Microservices sharing one data model are a distributed monolith — apply the rule inside the monolith first.

**Invoke:** `clean-architecture` with the current module map and the stack from intake. Ask it to map the dependency graph, list every violation where business logic imports the ORM or framework, pick the most-changed module first, and show the extraction to framework-free Use Cases behind owned interfaces.

**Decide with the user:** How far to push the boundary this pass; which vendors (payments, storage) to wrap first; and whether any proposed service split is a real boundary or would only add a distributed monolith.

**Artifact:** Extend docs/ARCHITECTURE.md: record layers and violations under `## Layer Map & Dependency Rule` (violation | location | fix | status) and the boundary choices under `## Decision Log`. Update the tracker.

**Done when:** every Dependency Rule violation is a tracked row with a fix, at least the highest-risk vendor is wrapped, business-rule tests run with no framework, and tests are green.

### Phase 6 — Lock in the habits (pragmatic-programmer)

**Purpose:** Set the meta-principles that stop the codebase from silently re-accruing debt after this journey ends.

**Brief (fallback):** Broken Window Theory: one unrepaired hack drops the bar for the next — fix immediately or board it up with a tracked ticket, never an untracked `// TODO`. DRY is about knowledge, not text — de-duplicate the same rule in two places (validation on client and server), leave coincidental look-alikes alone. Orthogonality: changing one component shouldn't affect another. Reversibility: wrap vendors behind your own interfaces. Design by Contract + crash early: guard preconditions and invariants at hardened boundaries so an invalid state fails loudly at the source.

**Invoke:** `pragmatic-programmer` across the codebase. Ask it to flag duplicated knowledge (ignoring coincidental duplication), broken windows and untracked TODOs to board up, and the boundaries that need Design-by-Contract guard clauses.

**Decide with the user:** The debt budget per iteration and the broken-windows policy — what gets fixed now versus ticketed.

**Artifact:** Extend docs/TECH-DEBT.md: record duplicated-knowledge and broken-window items in `## Debt Ledger`, and the agreed policy under `## Debt Budget & Broken-Windows Policy` and `## Adopted Conventions`. Update the tracker.

**Done when:** duplicated-knowledge hits are ledgered or fixed, no untracked hacks remain, and the debt-budget policy is written down.

### Phase 7 — Harden the integration points (release-it)

**Purpose:** Make every integration point degrade gracefully so a slow or failing dependency can't take the whole system down.

**Brief (fallback):** The software that passes QA is not what survives production. Integration points are the number-one killer — a slow response is worse than none. Non-negotiables: connect + read timeouts on every outbound call; a Circuit Breaker on failing dependencies (trips open, fails fast, half-open recovery); Bulkheads to isolate resource pools; Retry with exponential backoff + jitter; Steady State cleanup of accumulating cruft. Bound every query — unbounded result sets crash at scale, so add LIMITs and pagination. Decouple deploy from release with feature flags and expand-contract migrations; add deep health checks, RED metrics, symptom-based alerts.

**Invoke:** `release-it` with the outbound dependencies from intake. Ask for an audit of calls with no timeout, unbounded queries and list endpoints, circuit-breaker + bulkhead placement, an expand-contract migration plan for a risky schema, and a deep health check + RED metrics + alert design.

**Decide with the user:** Breaker thresholds, which dependencies get dedicated pools, and the alert symptoms and thresholds (error rate, latency).

**Artifact:** Extend docs/RELIABILITY.md with `## Integration-Point Audit` (dependency | timeout | circuit breaker | bulkhead | retry policy | status), `## Query & Resource Findings`, `## Health Checks & Metrics`, and `## Deploy vs Release`. Update the tracker.

**Done when:** every outbound call has a timeout, critical dependencies have breakers and bulkheads, unbounded queries are bounded, a deep health check + RED metrics + symptom alerts exist, and the audit has no open rows for critical paths.

### Phase 8 — Carve into bounded contexts (domain-driven-design)

**Purpose:** Decompose the big ball of mud into contexts the team can own and eventually extract — without a rewrite.

**Brief (fallback):** The model is the code. Start with Ubiquitous Language: rename technical-only names (`DataManager`, `Helper`) to domain terms; a concept hard to name signals a wrong model. Map Bounded Contexts (the same word can mean different things in different contexts) starting from what exists, aligned with team boundaries. The Anti-Corruption Layer lets a clean new context talk to the legacy core without the old model leaking in — the foundation of the Strangler Fig. Inside a context: small Aggregates with one root, reference others by ID, immutable Value Objects, past-tense Domain Events. Invest hardest in the Core Domain.

**Invoke:** `domain-driven-design` with the tangled modules and the boundaries from Phase 5. Ask it to build a ubiquitous language, map current and target bounded contexts, design an anti-corruption layer for a new clean context, and shrink any god aggregate to its true consistency boundary.

**Decide with the user:** Which context to carve first (the Core Domain where value lives); which boundaries align with team structure; and whether cross-context calls become Domain Events.

**Artifact:** Extend docs/ARCHITECTURE.md: record the map under `## Bounded Contexts & Context Map`, terms under `## Domain Glossary (Ubiquitous Language)`, and the decomposition choices under `## Decision Log`. Update the tracker.

**Done when:** the current context map is drawn, the first target context and its anti-corruption layer are defined, key domain terms are in the glossary, and any reshaped aggregate keeps tests green.

## Optional Phases

| Skill | Add when | Artifact |
|---|---|---|
| system-design | Paydown reveals real scaling limits that need re-architecture | Extends docs/ARCHITECTURE.md (`## System Context`) |
| ddia-systems | Data-layer decisions (isolation, replication, storage fit) are part of the debt | Extends docs/ARCHITECTURE.md (`## Data & Storage Decisions`) |
| team-topologies | Debt clusters where team boundaries fight the architecture | Extends docs/OPERATIONS.md (`## Team Structure`) |

Optional phases follow the same operating rules; insert where the Add-when condition first becomes true — the scaling and data phases after Phase 5, the team-topology phase alongside Phase 8's context boundaries.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Proposing the big-bang rewrite | Commit to paying debt down in place; every phase leaves the system better and still shipping, worst case a fast revert. Show one small, fast win first. |
| Cleaning before writing a single test | Pin behavior with characterization tests in Phase 1 (working-with-legacy-code) first; coverage follows the paths you actually change. |
| Trying to fix everything at once | Triage by the three-axis heuristic — invest where change is frequent and the Core Domain lives; a one-off spot gets a sprout, not a refactor. |
| Letting the agent "modularize" into tiny classes | Hold it to software-design-philosophy's deep-module rule — merge shallow classes that travel together; that is classitis, not architecture. |
| Calling external services with no timeout | In Phase 7 (release-it) add connect + read timeouts on every outbound call, plus a circuit breaker on critical dependencies. |
| Mistaking microservices for architecture | Apply the Dependency Rule and find real bounded contexts inside the monolith first (clean-architecture, domain-driven-design); services sharing one database are a distributed monolith. |

## Completing the Journey

Exit checklist — every box tied to an artifact:

- [ ] Changed modules have characterization tests that run green (TESTING.md Safety Net Map complete for the paths you touched).
- [ ] Every outbound call has a timeout and critical dependencies have circuit breakers and bulkheads (RELIABILITY.md Integration-Point Audit clear).
- [ ] The Dependency Rule holds for reworked modules — business logic imports no framework or ORM (ARCHITECTURE.md Layer Map, violations closed).
- [ ] The monolith has a current context map and at least one clean context behind an anti-corruption layer (ARCHITECTURE.md Bounded Contexts & Context Map).
- [ ] No untracked hacks remain; the debt budget and broken-windows policy are written down (TECH-DEBT.md Debt Budget & Broken-Windows Policy).

Close the tracker: every phase `done` or `skipped: reason`, with remaining Next Actions carried into the TECH-DEBT.md Debt Ledger so nothing is lost. Then route forward: when the starting point was a younger prototype and you want the production-readiness variant of this journey, continue with `improve-code-quality`; when code health is restored and the product experience is next, continue with `improve-app`.
