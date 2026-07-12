---
name: ln-42-acceptance-test-builder
description: "Creates and runs reproducible acceptance tests for stated requirements using project-native tooling. Use when executable acceptance evidence is needed; not for audits or product fixes."
---

# Acceptance Test Builder

Create executable evidence that stated requirements work through the boundary users or external systems observe. Modify only the approved test and test-documentation scope. If a test exposes a product defect, preserve the evidence and report it instead of repairing production code.

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

## Checklist

### 1. Establish the Change Boundary

- [ ] Resolve the requirements, acceptance criteria, actor, observable outcome, explicit non-goals, allowed test paths, and allowed test-documentation paths.
- [ ] Read applicable repository instructions and inspect Git state, untracked files, generated areas, and existing user changes before editing.
- [ ] Detect the project-native runner, directory layout, naming, fixtures, setup, cleanup, environment configuration, and CI invocation.
- [ ] Map each requirement to the boundary that can prove it: UI, API, CLI, message, integration, file, or durable state.
- [ ] Identify credentials, services, accounts, ports, devices, browsers, datasets, and destructive effects required by the scenarios.
- [ ] Return `BLOCKED` before editing when no safe target, reliable expected contract, or separable workspace exists.

### 2. Design Reproducible Acceptance Evidence

- [ ] Define setup, action, terminal outcome, independent oracle, expected evidence, and cleanup for every requirement.
- [ ] Use the lowest production-shaped boundary that still proves the requirement; do not replace acceptance evidence with a unit-level implementation check.
- [ ] Include material invalid, authorization, boundary, partial-failure, retry, idempotency, recovery, and compatibility behavior.
- [ ] Allocate unique or namespaced test data and control clock, randomness, locale, ordering, and concurrency where they affect reproducibility.
- [ ] Use real dependencies or approved emulators when mocks would bypass the behavior under acceptance; pin versions and verify readiness and reset behavior.
- [ ] For deterministic output, derive golden or diff expectations from an independent contract and keep the artifact small enough to review.
- [ ] For nondeterministic output, assert stable invariants and semantic fields instead of normalizing away failures or snapshotting noise.

### 3. Implement within Test Scope

- [ ] Create or update tests in the existing project layout with behavioral names and failure messages that identify the violated requirement.
- [ ] Reuse maintained fixtures and helpers only when their defaults and side effects remain visible; avoid a new abstraction for one scenario.
- [ ] Make setup fail fast on missing prerequisites and make cleanup safe after success, assertion failure, timeout, cancellation, or partial setup.
- [ ] Keep tests rerunnable and idempotent; do not depend on execution order or silently reuse state from a previous run.
- [ ] Add the narrowest required test documentation only when contributors otherwise cannot configure, run, interpret, or clean up the new evidence.
- [ ] Do not edit production code, weaken assertions, broaden timeouts without evidence, skip failing cases, or regenerate expected artifacts to obtain a pass.
- [ ] Inspect the diff for unrelated formatting, generated churn, secrets, environment-specific paths, and changes outside the approved scope.

### 4. Execute and Preserve Evidence

- [ ] Run the smallest new scenario first, then the relevant suite and required repository gate when available.
- [ ] Record the exact command, working directory, environment class, target, versions, exit status, duration, and artifact locations.
- [ ] Preserve the first failing output, seed, order, request, response, screenshot, diff, or durable state needed to reproduce the defect.
- [ ] Distinguish product failure, test defect, environment failure, unavailable dependency, and flaky evidence before changing the test.
- [ ] If the test exposes a product defect, stop modifying the implementation, retain the failing acceptance evidence, and report the smallest reproduction.
- [ ] Verify cleanup and rerun at least the affected scenario when state ownership or idempotency is material.
- [ ] Avoid retries unless they diagnose nondeterminism; a retry must not convert the initial failure into a silent pass.

### 5. Finalize without Overclaiming

- [ ] Map every requirement to its test path, command, oracle, and result as `PASS`, `FAIL`, or `UNPROVEN`.
- [ ] Use `COMPLETE` when the requested tests are created and all required acceptance evidence executes to a recorded `PASS` or `FAIL`; this verdict describes evidence completion, not product correctness.
- [ ] Use `INCOMPLETE` when tests are created but an environment, dependency, or interrupted run prevents complete execution; state the exact missing check.
- [ ] Use `BLOCKED` when tests cannot be created safely, requirements lack a reliable oracle, or the workspace cannot be protected.
- [ ] Return created and changed test files, commands, evidence, cleanup result, limitations, product defects, and residual risks.

## Output Contract

```markdown
# Acceptance Test Build

**Verdict:** COMPLETE | INCOMPLETE | BLOCKED

## Scope and environment
- Requirements and approved paths
- Runner, boundary, target, and prerequisites

## Requirements matrix
| Requirement | Test | Oracle | Command | Result |
|---|---|---|---|---|
| ... | ... | ... | ... | PASS / FAIL / UNPROVEN |

## Changes and evidence
- Created or changed test and documentation files
- Exact commands, outputs, and evidence artifacts
- Product defects preserved without repair

## Cleanup, limitations, and residual risks
State cleanup, unavailable environments, excluded cells, and remaining evidence needs.
```
