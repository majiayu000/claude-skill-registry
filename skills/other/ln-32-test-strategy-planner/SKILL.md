---
name: ln-32-test-strategy-planner
description: "Plans risk-based test portfolios and acceptance evidence; does not write or execute tests."
---

# Test Strategy Planner

**Goal:** Design a read-only, risk-based test portfolio decision for the requested scope. Maximize confidence in important local behavior while preventing test growth that lacks a unique defect signal, and define how affected evidence is retained, changed, consolidated, retired, or deliberately omitted.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Requirements and repository rules | Native file reads plus Git | Establishing scope, current work, acceptance criteria, and supported commands | User-provided requirements with explicit limitations |
| Existing test surface | File listing, search, manifests, runner configuration, and CI | Mapping test levels, fixtures, environments, and conventions | Repository tree and known test entrypoints |
| Behavior and boundaries | Language server or host-native code intelligence | Tracing entrypoints, consumers, trust boundaries, persistence, queues, and external contracts | Narrow search followed by direct inspection |
| Existing evidence | Existing test/CI reports, test reads, and safe repository commands | A material uncertainty about current proof can change the strategy | Use static evidence with execution limits; do not run suites merely to produce a plan |
| Current external failure modes | Official documentation, specifications, advisories, and primary field evidence | An external contract or real user failure can change scenarios or priority | Mark the claim `UNVERIFIED`; do not invent risk |

Keep the run read-only. Do not create tests, fixtures, snapshots, tasks, or documentation, and do not update the reviewed implementation.

## Evidence Rules

- Choose the smallest reliable boundary that proves each material risk. Use end-to-end evidence when the terminal journey cannot be established lower; preserve distinct unit, integration, and contract proof where they detect different failures.
- Coverage is discovery evidence, not proof. Require an oracle that would fail for the named defect.
- Prioritize by impact, plausible failure, uniqueness, detectability, and recovery cost; do not convert those judgments into universal numeric thresholds.
- Existing tests reduce a gap only when their setup and assertions prove the same behavior and failure mode.
- Framework, language, ORM, serializer, or library behavior is not a product test unless local configuration or integration changes its contract.
- Keep portfolio action separate from execution status. Use `KEEP`, `ADD`, `UPDATE`, `MERGE`, `DELETE`, or `NO_TEST` for the decision and `PASS`, `FAIL`, `BLOCKED`, or `UNPROVEN` only for evidence state.
- `NO_TEST` is an explicit risk decision, not missing work. Name the existing proof, alternative control, or accepted residual risk.
- A persistent test register is optional. Prefer repository-native test names, paths, tags, CI configuration, and task output unless scale or governance requires another maintained artifact.
- External research is actionable only when it adds a concrete failure mode, boundary, or oracle to this plan.

## Checklist

### 1. Establish Scope and Evidence

- [ ] Resolve the feature, requirements, acceptance criteria, actors, explicit non-goals, and protected human or system outcomes; separate the requested mechanism from the result it must enable and return `BLOCKED` if there is no concrete behavior to plan for.
- [ ] Read applicable repository instructions and inspect Git state so current work and unrelated changes are not mistaken for established behavior.
- [ ] Detect languages, frameworks, runners, test directories, fixtures, factories, environments, CI gates, coverage, contract tests, and manual test surfaces.
- [ ] Map existing evidence and every test affected by the requested behavior to each requirement; record coverage as complete, partial, missing, or unavailable based on the actual oracle, alongside the execution state defined in Evidence Rules; names and proximity are not proof.
- [ ] Inspect manual, exploratory, incident, and production evidence when it reveals behavior that automated suites do not cover.
- [ ] Identify environment, data, credentials, services, devices, browsers, and destructive-state constraints before proposing scenarios.
- [ ] Record assumptions and unknowns that can change test level, priority, or feasibility, and ask one concise question only when different interpretations materially change the strategy.

### 2. Build the Risk Map

- [ ] Trace critical flows from actor trigger through entrypoint, runtime wiring, state change, and durable or user-visible outcome.
- [ ] Identify uniquely important local behavior involving money, authentication, authorization, ownership, data integrity, destructive actions, migrations, public contracts, or irreversible workflows.
- [ ] Enumerate plausible defect classes: incorrect success, rejected valid input, accepted invalid input, boundary error, partial failure, duplicate delivery, ordering, timeout, retry, cancellation, race, rollback, recovery, and compatibility drift; state what protected outcome is lost or what concrete harm follows.
- [ ] Separate product risks from implementation details and behavior already guaranteed by a dependency; exclude technically representable states that protect no unique local outcome or decision.
- [ ] Identify privacy-sensitive or regulated test data and require synthetic, minimized, or explicitly approved fixtures.
- [ ] Use current external evidence only when version-sensitive contracts, recurring user failures, abuse patterns, or interoperability risks can change the map.
- [ ] Rank risks qualitatively and explain ties or uncertainty; do not manufacture precision from missing frequency or impact data.

### 3. Decide Portfolio Actions, Levels, and Oracles

- [ ] Assign every material risk and affected test exactly one provisional action: `KEEP` when trusted unique proof remains valid; `ADD` for an unproved material risk; `UPDATE` when valuable intent remains but basis, boundary, setup, or oracle changed; `MERGE` for safely consolidatable proof; `DELETE` for obsolete, duplicate, trivial, or untrustworthy proof; or `NO_TEST` when another control or accepted risk is sufficient.
- [ ] For `DELETE` or `MERGE`, prove that the test basis is obsolete or identify replacement evidence that preserves every still-required material behavior, failure mode, oracle, and useful failure localization; never retain obsolete proof merely because it already exists.
- [ ] Choose unit tests for isolated local rules, contract tests for producer-consumer agreement, integration tests for owned boundaries, and end-to-end tests for production-shaped journeys whose terminal outcome cannot be proved lower.
- [ ] Avoid duplicating the same behavior at every level unless each level detects a distinct failure class.
- [ ] Define the minimum sufficient independent oracle, combining observations when the contract requires them: returned contract, durable state, emitted event, rendered behavior, external effect, invariant, or deterministic artifact.
- [ ] Check that mocks and fakes do not bypass the boundary or failure semantics the scenario claims to prove.
- [ ] Use stable project-native semantic locators (roles, accessible names, labels) or explicit IDs/test hooks according to the observable contract and locale strategy. Avoid styling, position, timing, and incidental structure. Treat exact-copy assertions separately when copy is a requirement; do not require product edits solely to add hooks when a robust semantic locator exists.
- [ ] Include positive, invalid, boundary, authorization, error, recovery, concurrency, and compatibility cases only where the risk map makes them material.
- [ ] Specify non-default configuration, time, locale, randomness, ordering, or data scale when defaults could conceal hard-coded behavior.
- [ ] Add browser, device, operating-system, runtime, or version cells only when the supported contract or a known risk makes them decision-relevant.
- [ ] Prefer deterministic setup and bounded data; identify where real dependencies, emulators, disposable environments, or production-like topology are necessary.
- [ ] Define the repository gate or diagnostic role, entry prerequisites, and evidence-based completion criteria for each portfolio action; do not use test count or raw coverage as completion.

### 4. Produce a Prioritized Test Matrix

- [ ] For every decision, name the test basis, protected outcome, risk, existing evidence or affected test, portfolio action, level, setup, oracle, expected evidence, environment, gate, and result state when known.
- [ ] Define a review or retirement trigger for evidence whose value depends on a contract, migration, compatibility window, workaround, incident, dependency, or temporary risk; do not invent dates without an owned reason.
- [ ] Order scenarios so safety-critical and high-information checks run before expensive breadth, while preserving prerequisite and state dependencies.
- [ ] Identify which scenarios can run in parallel and which share mutable state, rate limits, accounts, devices, or environment setup.
- [ ] Classify gates by failure consequence and required detection time; place slow diagnostic checks outside routine gates only when another control covers release-critical risk.
- [ ] State exclusions explicitly, including scenarios with no unique protected outcome or defect signal, low-value duplication, framework behavior, infeasible environments, and accepted residual risks.
- [ ] Use `READY` when the strategy is executable and decision-complete, `INCONCLUSIVE` when useful partial planning is possible but material evidence is missing, and `BLOCKED` when requirements or a safety-critical boundary cannot be established.
- [ ] Reconcile the risk map and decision ledger: no material risk or affected test lacks an action and supporting rationale.
- [ ] State the smallest next evidence-gathering action for every `INCONCLUSIVE` or `BLOCKED` area.

- [ ] Map material requirements and operational risks to distinct evidence, the owning test boundary, prerequisites, and pass criteria; identify which checks remain valid after a requirement or environment changes.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Protected outcome → defect class → impact → existing proof → priority. Per affected test or gap: portfolio action, level/scenario/environment, independent oracle, required/diagnostic gate and result, and review/retirement trigger. Report net portfolio effect and justified `NO_TEST`, excluded low-value duplication, environment needs, and exact evidence actions for inconclusive areas.
