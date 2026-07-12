---
name: ln-41-test-strategy-planner
description: "Designs a risk-based test strategy and prioritized scenarios without changing code. Use when requirements need a test plan; not for auditing or implementing tests."
---

# Test Strategy Planner

Design a read-only test strategy that maximizes confidence in important local behavior. Select test levels by the boundary that must be crossed and the defect that must be detected, not by a fixed pyramid, coverage target, or scenario count.

## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Requirements and repository rules | Native file reads plus Git | Establishing scope, current work, acceptance criteria, and supported commands | User-provided requirements with explicit limitations |
| Existing test surface | File listing, search, manifests, runner configuration, and CI | Mapping test levels, fixtures, environments, and conventions | Repository tree and known test entrypoints |
| Behavior and boundaries | Language server or host-native code intelligence | Tracing entrypoints, consumers, trust boundaries, persistence, queues, and external contracts | Narrow search followed by direct inspection |
| Existing evidence | Safe repository-defined test and coverage commands | Determining what behavior is already proved and where confidence is weak | Inspect tests and CI; mark execution unavailable |
| Current external failure modes | Official documentation, specifications, advisories, and primary field evidence | An external contract or real user failure can change scenarios or priority | Mark the claim `UNVERIFIED`; do not invent risk |

Keep the run read-only. Do not create tests, fixtures, snapshots, tasks, or documentation, and do not update the reviewed implementation.

## Evidence Rules

- Test level follows the observable boundary: use the lowest level that can expose the intended defect without bypassing the behavior under test.
- Coverage is discovery evidence, not proof. Require an oracle that would fail for the named defect.
- Prioritize by impact, plausible failure, uniqueness, detectability, and recovery cost; do not convert those judgments into universal numeric thresholds.
- Existing tests reduce a gap only when their setup and assertions prove the same behavior and failure mode.
- Framework, language, ORM, serializer, or library behavior is not a product test unless local configuration or integration changes its contract.
- External research is actionable only when it adds a concrete failure mode, boundary, or oracle to this plan.

## Checklist

### 1. Establish Scope and Evidence

- [ ] Resolve the feature, requirements, acceptance criteria, actors, explicit non-goals, and observable outcomes; return `BLOCKED` if there is no concrete behavior to plan for.
- [ ] Read applicable repository instructions and inspect Git state so current work and unrelated changes are not mistaken for established behavior.
- [ ] Detect languages, frameworks, runners, test directories, fixtures, factories, environments, CI gates, coverage, contract tests, and manual test surfaces.
- [ ] Map existing evidence to each requirement and mark it `PROVED`, `PARTIAL`, `MISSING`, or `UNAVAILABLE` based on the actual oracle.
- [ ] Inspect manual, exploratory, incident, and production evidence when it reveals behavior that automated suites do not cover.
- [ ] Identify environment, data, credentials, services, devices, browsers, and destructive-state constraints before proposing scenarios.
- [ ] Record assumptions and unknowns that can change test level, priority, or feasibility.

### 2. Build the Risk Map

- [ ] Trace critical flows from actor trigger through entrypoint, runtime wiring, state change, and durable or user-visible outcome.
- [ ] Identify uniquely important local behavior involving money, authentication, authorization, ownership, data integrity, destructive actions, migrations, public contracts, or irreversible workflows.
- [ ] Enumerate plausible defect classes: incorrect success, rejected valid input, accepted invalid input, boundary error, partial failure, duplicate delivery, ordering, timeout, retry, cancellation, race, rollback, recovery, and compatibility drift.
- [ ] Separate product risks from implementation details and from behavior already guaranteed by a dependency.
- [ ] Identify privacy-sensitive or regulated test data and require synthetic, minimized, or explicitly approved fixtures.
- [ ] Use current external evidence only when version-sensitive contracts, recurring user failures, abuse patterns, or interoperability risks can change the map.
- [ ] Rank risks qualitatively and explain ties or uncertainty; do not manufacture precision from missing frequency or impact data.

### 3. Select Test Levels and Oracles

- [ ] Choose unit tests for isolated local rules, contract tests for producer-consumer agreement, integration tests for owned boundaries, and end-to-end tests for production-shaped journeys whose terminal outcome cannot be proved lower.
- [ ] Avoid duplicating the same behavior at every level unless each level detects a distinct failure class.
- [ ] Define one independent oracle per scenario: returned contract, durable state, emitted event, rendered behavior, external effect, invariant, or deterministic artifact.
- [ ] Check that mocks and fakes do not bypass the boundary or failure semantics the scenario claims to prove.
- [ ] Include positive, invalid, boundary, authorization, error, recovery, concurrency, and compatibility cases only where the risk map makes them material.
- [ ] Specify non-default configuration, time, locale, randomness, ordering, or data scale when defaults could conceal hard-coded behavior.
- [ ] Add browser, device, operating-system, runtime, or version cells only when the supported contract or a known risk makes them decision-relevant.
- [ ] Prefer deterministic setup and bounded data; identify where real dependencies, emulators, disposable environments, or production-like topology are necessary.

### 4. Produce a Prioritized Test Matrix

- [ ] For every scenario, name the requirement, risk, defect class, test level, setup, action, oracle, expected evidence, and required environment.
- [ ] Mark existing scenarios that should be retained or strengthened and new scenarios that should be added; do not redesign the entire suite without a demonstrated need.
- [ ] Order scenarios so safety-critical and high-information checks run before expensive breadth, while preserving prerequisite and state dependencies.
- [ ] Identify which scenarios can run in parallel and which share mutable state, rate limits, accounts, devices, or environment setup.
- [ ] Separate release-gating scenarios from slower diagnostic or exploratory coverage so the plan does not make routine delivery impractical.
- [ ] State exclusions explicitly, including low-value duplication, framework behavior, infeasible environments, and accepted residual risks.
- [ ] Use `READY` when the strategy is executable and decision-complete, `INCONCLUSIVE` when useful partial planning is possible but material evidence is missing, and `BLOCKED` when requirements or a safety-critical boundary cannot be established.
- [ ] Return the verdict, risk map, existing evidence, prioritized matrix, environment needs, exclusions, limitations, and residual risks.
- [ ] State the smallest next evidence-gathering action for every `INCONCLUSIVE` or `BLOCKED` area.

## Output Contract

```markdown
# Test Strategy

**Verdict:** READY | INCONCLUSIVE | BLOCKED

## Scope and existing evidence
- Requirements, actors, and outcomes
- Existing suites, commands, and environments
- Assumptions and unavailable evidence

## Risk map
| Behavior | Failure or defect class | Impact | Existing proof | Priority rationale |
|---|---|---|---|---|
| ... | ... | ... | PROVED / PARTIAL / MISSING / UNAVAILABLE | ... |

## Prioritized scenarios
| Priority | Requirement | Level | Scenario | Oracle and expected evidence | Environment |
|---:|---|---|---|---|---|
| ... | ... | unit / contract / integration / E2E | ... | ... | ... |

## Next evidence-gathering actions
Exact repository, environment, contract, or user decision needed for each `INCONCLUSIVE` or `BLOCKED` area.

## Exclusions and residual risks
Low-value duplication, unavailable environments, accepted gaps, and evidence still required.
```
