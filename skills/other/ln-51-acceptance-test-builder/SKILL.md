---
name: ln-51-acceptance-test-builder
description: "Builds, updates or retires scoped acceptance tests and verifies execution; does not repair product code."
---

# Acceptance Test Builder

**Goal:** Deliver the smallest trustworthy acceptance-test portfolio for stated requirements through a user- or external-system-observable boundary. Modify only approved tests and test documentation; implement justified additions, updates, merges, and deletions without repairing product code.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Workspace safety | Git status, diff, repository instructions, and branch or worktree inspection | Always before editing | Stop when user changes cannot be separated safely |
| Existing test conventions | File listing, search, manifests, runner configuration, CI, and focused reads | Selecting the project-native runner, layout, fixtures, and commands | Follow the nearest maintained test pattern |
| Behavior and wiring | Language server or host-native code intelligence | Locating observable entrypoints, registration, consumers, and state boundaries | Narrow search plus direct inspection |
| Test implementation | Native editing tools and project generators | Creating tests, fixtures, helpers, and narrowly required test documentation | Minimal project-consistent files; never hand-edit generated state |
| Observable execution | Repository-defined shell commands, browser, API client, CLI, or disposable integration environment | Proving UI, protocol, command, or durable state outcomes | Return `INCOMPLETE` with the exact missing check |
| External contract | Official version-matched documentation or specification | Expected behavior depends on a current external API or standard | Mark it `UNVERIFIED`; do not encode a guessed oracle |

Never run acceptance tests against production or an unapproved external target. Do not deploy, publish, migrate shared data, rotate credentials, or accept changed output merely to make a test pass.

## Evidence Rules

- Derive expected behavior from requirements, public contracts, examples, invariants, or an independent reference; never from the implementation calculation being tested.
- Prefer a terminal durable or user-visible outcome over an intermediate status, mock call, log line, or internal method result.
- Use golden files or snapshots only for deterministic, reviewable contracts. Updating expected output is a specification change, not test verification.
- Make setup, data allocation, execution, cleanup, and rerun behavior reproducible; preserve the first failure before retries or cleanup obscure it.
- A passing command proves only the environment and scenarios it actually exercised. State every excluded cell and unavailable boundary.
- Do not test language, framework, package, database-vendor, or other generic behavior; test only the repository-owned observable contract, configuration, integration, or policy that depends on it.
- Treat `KEEP`, `ADD`, `UPDATE`, `MERGE`, `DELETE`, and `NO_TEST` as portfolio decisions, distinct from execution results. Do not default to `ADD` when existing evidence, consolidation, retirement, or accepted residual risk is the better answer.
- Delete or merge only when the test basis is obsolete or evidence shows that all still-required unique material behavior, failure modes, oracle strength, and useful failure localization remain covered.

## Checklist

### 1. Establish the Change Boundary

- [ ] Resolve the requirements, acceptance criteria, actor, protected outcome, observable contract, explicit non-goals, approved portfolio decisions, allowed test paths, and allowed test-documentation paths; label inferred experience qualities as assumptions.
- [ ] Read applicable repository instructions and inspect Git state, untracked files, generated areas, and existing user changes before editing.
- [ ] Detect the project-native runner, directory layout, naming, fixtures, setup, cleanup, environment configuration, and CI invocation.
- [ ] Inventory existing tests affected by the requirement or contract and map their actual oracles before creating a new test.
- [ ] Map each requirement to the boundary that can prove it: UI, API, CLI, message, integration, file, or durable state.
- [ ] Identify credentials, services, accounts, ports, devices, browsers, datasets, and destructive effects required by the scenarios.
- [ ] Return `BLOCKED` before editing when no safe target, reliable expected contract, or separable workspace exists.

### 2. Design Reproducible Acceptance Evidence

- [ ] Define the protected outcome, defect class, setup, action, terminal outcome, independent oracle, expected evidence, and cleanup for every requirement.
- [ ] Confirm or derive one portfolio action per affected test and material risk. When no approved strategy exists, justify the action from impact, plausible failure, uniqueness, trust, and maintenance cost; record `NO_TEST` with existing proof, another control, or accepted residual risk.
- [ ] Prefer deterministic end-to-end evidence for material user-observable business risk. Use a narrower production-shaped contract or integration boundary only when it still proves the terminal outcome more deterministically or precisely; never replace acceptance evidence with a unit implementation check or cover an internal detail absent from the observable contract.
- [ ] Include invalid, authorization, boundary, partial-failure, retry, idempotency, recovery, and compatibility behavior only when it can materially change the protected outcome.
- [ ] Allocate unique or namespaced test data and control clock, randomness, locale, ordering, and concurrency where they affect reproducibility.
- [ ] Use real dependencies or approved emulators when mocks would bypass the behavior under acceptance; pin versions and verify readiness and reset behavior.
- [ ] For deterministic output, derive golden or diff expectations from an independent contract and keep the artifact small enough to review.
- [ ] For nondeterministic output, assert stable invariants and semantic fields instead of normalizing away failures or snapshotting noise.
- [ ] Use stable project-native semantic locators (roles, accessible names, labels) or explicit IDs/test hooks according to the observable contract and locale strategy. Avoid styling, position, timing, and incidental structure. Treat exact-copy assertions separately when copy is a requirement; do not require product edits solely to add hooks when a robust semantic locator exists.
- [ ] Define the required or diagnostic gate and a review or retirement trigger when evidence is temporary, compatibility-bound, incident-specific, or coupled to a changing contract.

### 3. Implement within Test Scope

- [ ] Create or update tests in the existing project layout with behavioral names and failure messages that identify the violated requirement, protected outcome, and detected defect.
- [ ] Implement approved `MERGE` and `DELETE` actions without leaving superseded tests, fixtures, snapshots, helpers, registrations, or CI entries; preserve replacement traceability in repository-native paths, names, tags, or task evidence.
- [ ] Reuse maintained fixtures and helpers only when their defaults and side effects remain visible; avoid a new abstraction for one scenario.
- [ ] Make setup fail fast on missing prerequisites and make cleanup safe after success, assertion failure, timeout, cancellation, or partial setup.
- [ ] Keep tests rerunnable and idempotent; do not depend on execution order or silently reuse state from a previous run.
- [ ] Add the narrowest required test documentation only when contributors otherwise cannot configure, run, interpret, or clean up the new evidence.
- [ ] Do not edit production code, weaken assertions, broaden timeouts without evidence, skip failing cases, or regenerate expected artifacts to obtain a pass.
- [ ] Inspect the diff for unrelated formatting, generated churn, secrets, environment-specific paths, and changes outside the approved scope.

### 4. Execute and Preserve Evidence

- [ ] Run the smallest affected scenario first, then the relevant suite and required repository gate when available; when actions only remove evidence, run the replacement or nearest retained proof.
- [ ] Record command, working directory, environment class, target, versions, exit status, duration, artifacts, and actual scenarios executed. No selected tests or all-skipped output cannot prove acceptance.
- [ ] Preserve the first failing output, seed, order, request, response, screenshot, diff, or durable state needed to reproduce the defect.
- [ ] Distinguish product failure, test defect, environment failure, unavailable dependency, and flaky evidence before changing the test.
- [ ] If a valid test exposes a product defect, retain the failing acceptance evidence and report the smallest reproduction; never repair product code. Continue independent in-scope test work when safe.
- [ ] Verify cleanup and rerun at least the affected scenario when state ownership or idempotency is material.
- [ ] Avoid retries unless they diagnose nondeterminism; a retry must not convert the initial failure into a silent pass.

### 5. Finalize without Overclaiming

- [ ] Map every requirement and protected outcome to its final test path or `NONE`, command or alternative control, oracle or accepted risk, and result as `PASS`, `FAIL`, `BLOCKED`, or `UNPROVEN`.
- [ ] Reconcile planned and actual portfolio actions, including justified deviations, and report the net count of tests added, updated, merged, and deleted without treating counts as quality targets.
- [ ] Use `COMPLETE` when all approved portfolio actions are implemented and required evidence records a trustworthy `PASS` or product `FAIL`, or a justified `NO_TEST` control. Unresolved test defects are not completed evidence; this verdict does not certify product correctness.
- [ ] Use `INCOMPLETE` when safe work remains unfinished or environment, dependency, test defects, or interruption prevents trustworthy execution; state the exact remaining action or check.
- [ ] Use `BLOCKED` when actions cannot be implemented safely, requirements lack a reliable oracle, or the workspace cannot be protected.

- [ ] Preserve source acceptance identifiers and expected behavior independently of implementation; report selected/executed/skipped scope and never accept zero executed relevant tests as proof.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Requirement/protected outcome → existing evidence → portfolio action → final test path or `NONE` → independent oracle/command → gate/result → retirement trigger. List changed test/documentation files, replacement evidence for consolidation/deletion, net portfolio effect, exact commands and artifacts, retained product-failure reproductions, cleanup, unavailable environments, and excluded cells. Evidence completion does not imply product correctness.
