---
name: ln-23-test-suite-auditor
description: "Audits whether an existing test suite proves important product behavior with strong, isolated tests. Use when test confidence is uncertain; not to design or implement new tests."
---

# Test Suite Auditor

Audit the test portfolio as a read-only confidence system. Determine which important failures the suite can detect, which tests cannot be trusted, and where maintenance cost exceeds unique regression value.

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
- Deletion recommendations require proof that another test covers the same behavior and failure modes with equal or better trust.
- Known regression guards and the only proof of a rare critical edge case are not deletion candidates merely because a numeric value heuristic is low.
- A real dependency is not inherently a test defect. Judge whether its version, state, ownership, reset, availability, and failure evidence make the result reproducible.
- External testing guidance becomes actionable only when it explains a concrete weakness in this suite.

## Checklist

### 1. Map the Portfolio and Baseline

- [ ] Detect test runners, configurations, commands, directories, fixtures, factories, snapshots, golden files, manual scripts, coverage, and mutation tooling.
- [ ] Map source domains and critical entrypoints to unit, integration, contract, end-to-end, and manual test surfaces.
- [ ] Read repository instructions and CI configuration to identify required suites, environment assumptions, retries, sharding, and exclusions.
- [ ] Run the smallest representative suites, then required test gates where feasible; record environment, duration, exit status, failures, skips, and retries.
- [ ] Separate generated, vendored, example, migration-history, and infrastructure fixtures from product tests before evaluating the portfolio.
- [ ] Keep the audit read-only and disclose any caches or test artifacts created by permitted commands.

### 2. Audit Product Value and Coverage

- [ ] Identify uniquely critical local logic: money, authentication, authorization, data integrity, algorithms, domain rules, destructive operations, and irreversible workflows.
- [ ] Trace each critical behavior to at least one test whose oracle would fail for the corresponding defect; name/path matches and line coverage are only discovery evidence.
- [ ] Identify tests that merely re-prove language, framework, ORM, HTTP client, cryptography, serializer, or library behavior without adding local product confidence.
- [ ] Check whether end-to-end tests cross the production-shaped boundaries relevant to the risk and prove the terminal durable or user-visible outcome, not only an intermediate status, page, or mock call.
- [ ] Find critical journeys with no end-to-end proof and expensive end-to-end tests whose behavior is already covered more reliably at a lower level.
- [ ] Inspect error, retry, timeout, authorization, concurrency, migration, compatibility, and recovery behavior where those failures are plausible and costly.
- [ ] Use coverage data to locate unexecuted critical paths, then inspect behavior and assertions before reporting a gap.
- [ ] Classify portfolio actions as `KEEP`, `DELETE`, `MERGE`, `REWRITE`, or `ADD`, justified by impact, defect probability, uniqueness, trust, and maintenance cost.

### 3. Audit Isolation and Determinism

- [ ] Check shared database, filesystem, environment, process, network, cache, clock, random generator, and global state for leakage between tests.
- [ ] Check setup and teardown on success and failure, unique test data, transaction boundaries, cleanup, and parallel-safe resource ownership.
- [ ] Diagnose suspected flakes with the smallest discriminating matrix available: run alone, in-suite, repeated with a fixed seed, shuffled/reversed, and parallel; preserve the first failing order, seed, worker, and environment.
- [ ] Detect time, timezone, locale, randomness, sleep, scheduler, and race sensitivity; require controllable clocks or seeds where behavior depends on them.
- [ ] For real dependencies and emulators, verify version pinning, readiness, namespace/state reset, failure cleanup, credentials, and CI availability instead of assuming either real or mocked is preferable.
- [ ] Review retries and quarantine rules so they preserve the first failure and reproducibility data rather than converting an initial failure into a silent pass.
- [ ] Distinguish test flakiness from real intermittent product defects using repeated evidence, logs, and the failing path.

### 4. Audit Structure, Maintenance, and Oracles

- [ ] Check whether test layout follows source domains or a clear type-based convention and whether contributors can locate the owning tests.
- [ ] Find orphan tests, disabled suites, duplicate fixtures, fragmented scenario coverage, oversized files, and flat directories that obscure ownership.
- [ ] Check test names and arrangement for behavioral intent, prerequisites, action, and expected outcome rather than implementation narration.
- [ ] Inspect assertions for specificity, negative proof, state and interaction balance, useful failure messages, and resistance to false positives.
- [ ] Flag assertion-free tests, weak truthiness checks, snapshot-only proof, broad exception acceptance, and mocks that bypass the behavior under test.
- [ ] Check that expected values come from an independent contract, example, invariant, or golden artifact rather than reproducing the implementation's calculation inside the test.
- [ ] Check mocks, fakes, emulators, and generated clients for contract drift; require a contract test or another credible comparison with the real boundary where drift could create false confidence.
- [ ] Exercise non-default configuration values where a passing test with defaults could conceal hard-coded ports, limits, timeouts, paths, or feature behavior.
- [ ] Use existing mutation results or a safe targeted counterfactual for critical weak-oracle candidates; do not mandate repository-wide mutation testing.
- [ ] Review manual tests for reproducible setup, fail-fast behavior, explicit expected evidence, idempotency, cleanup, portability, and operator documentation.
- [ ] Check fixture and helper abstraction for readability and honest defaults; hidden behavior in builders must not make important test conditions invisible.

### 5. Validate Findings and Report

- [ ] Research runner or framework semantics only when lifecycle, fixture, isolation, retry, or mocking behavior can change a finding; use official version-matched sources.
- [ ] Reproduce high-severity trust failures where safe, preserving command, seed, order, and environment evidence.
- [ ] Deduplicate findings that share one root cause, such as a global fixture causing multiple flaky suites.
- [ ] Classify findings as `P0`-`P3` based on critical behavior left unproven, false confidence, delivery blockage, and maintenance drag.
- [ ] Include affected behavior, test location, evidence, missed defect class, portfolio action, and smallest credible remediation.
- [ ] Use `BLOCKED` when a required critical suite, environment, or oracle cannot be accessed and no credible static or historical fallback exists; use `FAIL` when evidence shows critical behavior is unproven, a required gate fails, or false confidence remains in an untrustworthy critical surface; use `CONCERNS` only for non-blocking portfolio or maintenance risk, and `PASS` only when required evidence is trustworthy and no critical gap remains.
- [ ] Return the verdict with trusted coverage, critical gaps, untrustworthy surfaces, portfolio actions, limitations, and residual test risk.

## Output Contract

```markdown
# Test Suite Audit

**Verdict:** PASS | CONCERNS | FAIL | BLOCKED

## Portfolio map and baseline
- Runners, suites, and test types
- Commands and environments executed
- Coverage, flake, and mutation evidence available

## Confidence summary
| Area | Status | Evidence |
|---|---|---|
| Critical behavior coverage | PASS / CONCERNS / FAIL | ... |
| Isolation and determinism | PASS / CONCERNS / FAIL | ... |
| Structure and maintenance | PASS / CONCERNS / FAIL | ... |
| Assertion and oracle strength | PASS / CONCERNS / FAIL | ... |

## Findings and portfolio actions
### [P0 | P1 | P2 | P3] Finding title
- Behavior and test location
- Evidence and missed defect class
- Action: KEEP / DELETE / MERGE / REWRITE / ADD
- Required change

## Residual risks
Unexecuted suites, unavailable environments, and behavior that remains unproven.
```
