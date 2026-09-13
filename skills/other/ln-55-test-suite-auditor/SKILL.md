---
name: ln-55-test-suite-auditor
description: "Audits existing tests for risk coverage, reliable oracles and maintenance value; does not edit tests."
---

# Test Suite Auditor

**Goal:** Audit the test portfolio as a read-only lifecycle and confidence system. Determine which important failures it detects, which evidence is untrustworthy or obsolete, and which additions, changes, consolidations, retirements, or explicit omissions produce the smallest sustainable portfolio.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Source and test inventory | Native file listing, search, manifests, and test configuration | Mapping domains, test types, runners, fixtures, and generated areas | Repository tree plus known test entrypoints |
| Test-to-code relationships | Language server or host-native code intelligence | Mapping units, callers, implementations, routes, and test targets | Naming and path search verified by direct reads |
| Execution and trust | Repository-defined test commands through the shell | Establishing pass/fail state, timing, order dependence, or reproducibility | Inspect CI results and configuration; mark execution unavailable |
| Coverage and missed behavior | Existing coverage tools and reports | Coverage data is configured and comparable to source scope | Static behavior-to-test mapping; never invent percentages |
| Flake and isolation evidence | Repeated, shuffled, parallel, or seed-controlled runs supported by the repository | A test is suspected of order, time, randomness, or shared-state dependence | History, CI logs, and code-path evidence |
| Assertion strength | Test reads, failure output, and configured mutation testing | Determining whether tests fail for meaningful behavioral defects | Counterfactual reasoning tied to specific assertions |
| Framework semantics | Official test-runner or framework documentation | A finding depends on lifecycle, fixtures, retries, isolation, or mocking behavior | Primary-source web research; otherwise mark `UNVERIFIED` |

Run only safe test and diagnostic commands. Do not rewrite snapshots, update golden files, regenerate fixtures, or accept changed output during the audit.

## Evidence Rules

- Coverage indicates execution, not proof. Require an assertion or observable oracle for important behavior.
- A slow test is not low-value when it uniquely protects a critical journey; a fast test is not high-value when it proves framework behavior.
- A flaky failure must be separated from an intermittently failing product dependency or genuinely nondeterministic requirement.
- Deletion recommendations require proof that the test basis is obsolete or that other evidence covers every still-required behavior and failure mode with equal or better trust.
- Merge recommendations require demonstrated duplicate or fragmented coverage and must preserve distinct business and failure scenarios, oracle strength, and failure localization; a larger test is not inherently better.
- Known regression guards and the only proof of a rare critical edge case are not deletion candidates merely because a numeric value heuristic is low.
- A real dependency is not inherently a test defect. Judge whether its version, state, ownership, reset, availability, and failure evidence make the result reproducible.
- Keep portfolio action (`KEEP`, `ADD`, `UPDATE`, `MERGE`, `DELETE`, `NO_TEST`) separate from execution status (`PASS`, `FAIL`, `BLOCKED`, `UNPROVEN`, `QUARANTINED`). `NO_TEST` requires existing proof, another control, or explicit residual-risk acceptance.
- Do not require a new registry by default. Prefer traceability derivable from repository-native test paths, behavioral names, tags, requirements, CI configuration, and review evidence.
- External testing guidance becomes actionable only when it explains a concrete weakness in this suite.

## Checklist

### 1. Map the Portfolio and Baseline

- [ ] Detect test runners, configurations, commands, directories, fixtures, factories, snapshots, golden files, manual scripts, coverage, and mutation tooling.
- [ ] Map source domains and critical entrypoints to unit, integration, contract, end-to-end, and manual test surfaces.
- [ ] Trace requirements, product risks, incidents, public contracts, and changed behavior to tests and results where evidence exists; identify tests with no current test basis and basis elements with no credible proof.
- [ ] Read repository instructions and CI configuration to identify required suites, environment assumptions, retries, sharding, and exclusions.
- [ ] Run representative suites and required gates where feasible; record environment, duration, exit status, discovered/executed scope, failures, skips, and retries. Flag required suites that silently select no tests.
- [ ] Separate generated, vendored, example, migration-history, and infrastructure fixtures from product tests before evaluating the portfolio.
- [ ] Keep the audit read-only and disclose any caches or test artifacts created by permitted commands.

### 2. Audit Product Value and Coverage

- [ ] Identify uniquely critical local logic: money, authentication, authorization, data integrity, algorithms, domain rules, destructive operations, and irreversible workflows.
- [ ] Trace each critical behavior to at least one test whose oracle would fail for the corresponding defect; name/path matches and line coverage are only discovery evidence.
- [ ] Identify tests that merely re-prove language, framework, database engine, ORM, HTTP client, cryptography, serializer, or library behavior without asserting repository-owned configuration, queries, schemas, adaptation, validation, failure handling, or observable outcomes.
- [ ] Check whether end-to-end tests cross the production-shaped boundaries relevant to the risk and prove the terminal durable or user-visible outcome, not only an intermediate status, page, or mock call.
- [ ] Find critical journeys with no end-to-end proof and expensive end-to-end tests whose behavior is already covered more reliably at a lower level.
- [ ] Inspect error, retry, timeout, authorization, concurrency, migration, compatibility, and recovery behavior where those failures are plausible and costly.
- [ ] Use coverage data to locate unexecuted critical paths, then inspect behavior and assertions before reporting a gap.
- [ ] Classify every material gap and in-scope affected test as `KEEP`, `ADD`, `UPDATE`, `MERGE`, `DELETE`, or `NO_TEST`, justified by impact, plausible failure, uniqueness, trust, and maintenance cost; use `UPDATE` when valuable intent remains but its basis, setup, boundary, assertion, or oracle must change.

### 3. Audit Isolation and Determinism

- [ ] Check shared database, filesystem, environment, process, network, cache, clock, random generator, and global state for leakage between tests.
- [ ] Check setup and teardown on success and failure, unique test data, transaction boundaries, cleanup, and parallel-safe resource ownership.
- [ ] Diagnose suspected flakes using only discriminating modes: alone, in-suite, fixed-seed repetition, shuffled/reversed order, or parallel execution. Preserve the first failure, order, seed, worker, and environment; stop when evidence identifies the cause or the bounded diagnostic budget ends.
- [ ] Detect time, timezone, locale, randomness, sleep, scheduler, and race sensitivity; require controllable clocks or seeds where behavior depends on them.
- [ ] For real dependencies and emulators, verify version pinning, readiness, namespace/state reset, failure cleanup, credentials, and CI availability instead of assuming either real or mocked is preferable.
- [ ] Review retries and quarantine rules so they preserve the first failure and reproducibility data rather than converting an initial failure into a silent pass.
- [ ] Require every quarantine to remain visible outside the passing result, with an owner or decision path and a concrete recovery, replacement, or retirement trigger; quarantine is an execution state, not a portfolio action.
- [ ] Distinguish test flakiness from real intermittent product defects using repeated evidence, logs, and the failing path.

### 4. Audit Structure, Maintenance, and Oracles

- [ ] Check whether test layout follows source domains or a clear type-based convention and whether contributors can locate the owning tests.
- [ ] Find orphan tests, disabled suites, duplicate fixtures, fragmented scenario coverage, oversized files, and flat directories that obscure ownership.
- [ ] Review temporary characterization, migration, compatibility, incident, workaround, and regression tests against current risk. A fixed incident does not retire its regression guard; require obsolete behavior or trustworthy replacement coverage before recommending merge or deletion.
- [ ] Check test names and arrangement for behavioral intent, prerequisites, action, and expected outcome rather than implementation narration.
- [ ] Use stable project-native semantic locators (roles, accessible names, labels) or explicit IDs/test hooks according to the observable contract and locale strategy. Avoid styling, position, timing, and incidental structure. Treat exact-copy assertions separately when copy is a requirement; do not require product edits solely to add hooks when a robust semantic locator exists.
- [ ] Inspect assertions for specificity, negative proof, state and interaction balance, useful failure messages, and resistance to false positives.
- [ ] Flag tests without a meaningful failure oracle, weak truthiness, snapshots of incidental or unreviewable output, broad exception acceptance, and mocks that bypass tested behavior. Retain snapshots or implicit failure oracles that independently prove the required contract.
- [ ] Check that expected values come from an independent contract, example, invariant, or golden artifact rather than reproducing the implementation's calculation inside the test.
- [ ] Check mocks, fakes, emulators, and generated clients for contract drift; require a contract test or another credible comparison with the real boundary where drift could create false confidence.
- [ ] Exercise non-default configuration values where a passing test with defaults could conceal hard-coded ports, limits, timeouts, paths, or feature behavior.
- [ ] Use existing mutation results or a safe targeted counterfactual for critical weak-oracle candidates; do not mandate repository-wide mutation testing.
- [ ] Review manual tests for reproducible setup, fail-fast behavior, explicit expected evidence, idempotency, cleanup, portability, and operator documentation.
- [ ] Check fixture and helper abstraction for readability and honest defaults; hidden behavior in builders must not make important test conditions invisible.
- [ ] Review gate placement and suite cost: required gates protect material release risk, while slower diagnostic or exploratory evidence remains discoverable without blocking routine delivery unnecessarily.

### 5. Validate Findings and Report

- [ ] Research runner or framework semantics only when lifecycle, fixture, isolation, retry, or mocking behavior can change a finding; use official version-matched sources.
- [ ] Reproduce high-severity trust failures where safe, preserving command, seed, order, and environment evidence.
- [ ] Deduplicate findings that share one root cause, such as a global fixture causing multiple flaky suites.
- [ ] Apply the materiality gate: require concrete critical proof gap, false confidence, delivery risk, or recurring maintenance cost at evidenced scale. Reject taste, theoretical purity, generic practice, hypothetical scale, and reasonable alternatives; require the outcome or constraint, not a preferred implementation.
- [ ] Ground external corrections in version-matched official contracts, using primary engineering sources for unresolved tradeoffs. Cite the supported mechanism; local evidence suffices for local defects.
- [ ] Classify findings as `P0`-`P3` based on critical behavior left unproven, false confidence, delivery blockage, and maintenance drag.
- [ ] Report decision-useful portfolio signals when evidence exists: material risks by proof state, action distribution, required-gate results and duration, skips, retries, quarantine, and orphan or obsolete candidates. Reject total test count, pass rate without exclusions, raw coverage, and level ratios as standalone quality targets.
- [ ] Use `BLOCKED` when a required critical suite, environment, or oracle cannot be accessed and no credible static or historical fallback exists; use `FAIL` when evidence shows critical behavior is unproven, a required gate fails, or false confidence remains in an untrustworthy critical surface; use `CONCERNS` only for non-blocking portfolio or maintenance risk, and `PASS` only when required evidence is trustworthy and no critical gap remains.

- [ ] Make accepted portfolio findings actionable through the protected behavior, owning test boundary, and evidence needed to close the gap; keep changes outside this read-only audit.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Test basis/protected risk → existing test or missing proof → portfolio action → oracle → gate/result → replacement evidence or retirement trigger. Cover critical behavior, isolation, maintenance, assertion strength, lifecycle, net portfolio effect, required/diagnostic gates, duration, skips, retries, and quarantine where evidenced. Findings need priority, test location, missed defect class, impact, unacceptable tradeoff, and minimal correction; preserve unique coverage and distinguish portfolio actions from execution states.
