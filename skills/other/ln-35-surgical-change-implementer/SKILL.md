---
name: ln-35-surgical-change-implementer
description: "Implements a bounded product-code change through the smallest complete root-cause solution. Use for scoped delivery; not for planning, review, audit, upgrades, modernization, or tuning."
---

# Surgical Change Implementer

**Goal:** Deliver one approved product-code change through the smallest complete solution that satisfies the business outcome. Remove superseded code and avoid AI slop, speculative abstraction, duplicate mechanisms, and custom infrastructure already provided by the repository or platform.

**Execution contract:** Treat the ordered checkbox workflow below as this skill's Definition of Done. Work through every item in order, and mark it complete only when its action and required evidence are complete. `N/A`, skipped, unavailable, or delegated items remain incomplete.
Before returning, apply this skill's verdict and approval rules to every incomplete item and prepend **Checklist: X/Y complete**<br>**Incomplete: None | section/item — reason; outcome impact; exact next action**; list every incomplete item.

## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Scope and repository policy | User request, linked task or plan, repository instructions, Git status, and focused diff | State bounded assumptions; stop if a choice would materially change product intent |
| Runtime ownership and impact | Language server, host-native code intelligence, traces, schemas, routes, and configuration | Narrow symbol and text search followed by direct reads of definitions and consumers |
| Existing capability | Repository code, manifests, lockfiles, platform APIs, and installed dependency source | Current official documentation and primary sources; mark uncertain claims `UNVERIFIED` |
| Safe implementation | Focused editor, native formatter, package manager, and generation commands | Minimal manual patch that preserves user changes and generated-file ownership |
| Verification | Repository-defined build, lint, type, test, smoke, and runtime checks | Smallest reproducible check that proves the protected contract; disclose coverage gaps |
| External semantics | Official documentation, specifications, security advisories, registries, and upstream source | Primary-source technical material; use secondary expert guidance only for tradeoffs |

Do not expand the task into repository-wide cleanup, redesign, dependency work, or performance tuning. Do not modify external systems, persisted data, public contracts, user experience, or unrelated dirty files without explicit authority.

## Core Rules

- KISS is a hard constraint: prefer the fewest concepts, branches, states, files, dependencies, and changed lines that form a complete design.
- Surgical does not mean superficial. Fix the owning cause once; do not hide it behind adapters, aliases, parallel paths, copied logic, or compatibility layers without a proven consumer.
- Existing code is not automatically correct, and new code is not automatically necessary. Subtraction, configuration, or no code can be the best implementation.
- Repository policies, architecture decisions, public contracts, security boundaries, logging and error conventions, and generated-code ownership constrain the solution.
- Research a concrete semantic or design uncertainty before coding. Prefer current official documentation; record why its guidance applies to the installed version and repository context.
- Reject an external package when its dependency, license, security, runtime, bundle, operational, or exit cost exceeds the custom behavior it removes.
- Preserve current user-visible behavior unless the task explicitly changes it. Report every new screen, message, or scenario; never alter an existing flow merely as a refactoring side effect.
- Never sacrifice correctness, security, data integrity, diagnosability, accessibility, or required compatibility to minimize code.

## Checklist

### 1. Establish the Change Contract

- [ ] Resolve the requested business outcome, affected users or operators, acceptance evidence, constraints, protected behavior, explicit non-goals, and approved mutation scope.
- [ ] Read repository instructions, relevant policies and architecture decisions, and the named task or plan; convert each applicable requirement into a traceable acceptance row.
- [ ] Inspect Git status and the target files before editing; distinguish baseline defects and user-owned changes from work authorized by this task.
- [ ] Trace the actual runtime path from observable entrypoint through owning logic, state, persistence or integrations, and failure handling; do not infer ownership from filenames alone.
- [ ] Inventory public and internal contracts, callers, configuration, data shapes, tests, documentation, and operational behavior that the change can affect.
- [ ] Identify decisions that would alter product intent, user experience, public compatibility, data, dependencies, or external state and obtain direction before making them.
- [ ] Return `BLOCKED` when the business outcome, ownership boundary, safe edit scope, or essential verification cannot be established without inventing intent.

### 2. Choose the Smallest Complete Solution

- [ ] Test `NO_CHANGE`: determine whether current behavior already satisfies the outcome or whether documentation, configuration, or usage correction resolves the request without product-code edits.
- [ ] Test `DELETE_OR_CONFIGURE`: identify an obsolete path, wrong default, redundant state, feature flag, registration, or configuration that can be removed or corrected directly.
- [ ] Test `REUSE_LOCAL`: search for the repository's canonical helper, component, service, policy, type, enum, constant, error, or integration before adding another concept.
- [ ] Test `USE_PLATFORM_OR_STDLIB`: verify whether the language, runtime, browser, database, framework, or deployment platform already owns the required generic behavior.
- [ ] Test `REUSE_INSTALLED`: inspect declared dependencies and their supported APIs before proposing a new package or custom mechanism.
- [ ] Consider `ADOPT_DEPENDENCY` only when remaining behavior is generic and material; verify current official guidance, maintenance, security, license, compatibility, transitive cost, and removal path.
- [ ] Use `MINIMAL_CUSTOM` only for irreducible product policy or a documented semantic gap; define the invariant it owns and why every earlier rung is insufficient.
- [ ] Compare credible candidates by total system complexity and risk, not syntax length; record the selected rung and concise rejection reason for lower rungs.
- [ ] Challenge the proposed design for symptom patches, duplicated ownership, speculative extension points, premature abstraction, hidden state, avoidable branching, and temporary compatibility that lacks a real consumer.
- [ ] Define the coherent edit set, deletion set, verification, and rollback boundary before changing code.

### 3. Implement Surgically

- [ ] Change the canonical owning boundary once and update only the consumers required for a complete end-to-end result.
- [ ] Follow repository conventions for naming, types, constants, enums, configuration, errors, logging, security, accessibility, concurrency, transactions, and resource lifecycle.
- [ ] Keep product policy explicit and centralized; do not scatter magic values, duplicated route or event keys, parallel allowlists, or derived state with multiple owners.
- [ ] Use existing dependency and generation workflows; do not hand-edit lockfiles or generated artifacts, add convenience wrappers around already clear APIs, or copy third-party implementation code.
- [ ] Remove obsolete branches, helpers, adapters, aliases, flags, exports, configuration, dependencies, documentation, and tests made unnecessary by the retained design.
- [ ] Before deleting a reportedly unused path, check dynamic imports, reflection, registries, configuration, code generation, scripts, optional features, and external consumers that static search can miss.
- [ ] Preserve compatibility only for a verified consumer; make every temporary bridge narrow, observable, owned, time-bounded by a removal trigger, and explicit in the report.
- [ ] Inspect the diff during implementation for unrelated formatting, opportunistic refactoring, accidental UX or contract changes, debug artifacts, and net-new code unsupported by the change contract.

### 4. Build Proportionate Evidence

- [ ] Map each acceptance row and material regression risk to existing evidence before adding tests; assess likelihood, impact, detectability, and blast radius.
- [ ] Choose exactly one portfolio action per affected test or gap: `KEEP`, `ADD`, `UPDATE`, `MERGE`, `DELETE`, or justified `NO_TEST`; remove superseded and low-value testware in the approved scope.
- [ ] Prefer an end-to-end or widest reliable observable boundary for material user-facing business risk. Use a narrower integration, contract, or unit test only when it gives more deterministic or precise evidence; justify unit tests explicitly.
- [ ] Do not test language, framework, package, database-vendor, generated-code, or trivial wiring behavior. A test must fail for a meaningful defect in this product's business, security, data, or delivery contract.
- [ ] For UI tests, target stable repository-owned IDs, roles, or hooks; never bind behavior to visible or translated copy, CSS, layout, position, timing accidents, or incidental structure.
- [ ] Give temporary characterization or migration tests an owner and retirement trigger; keep quarantine explicit and never count skipped, flaky, or unproven evidence as passing.
- [ ] Run focused checks after the coherent edit, then the repository-required build, lint, type, test, smoke, packaging, and application-start gates relevant to the affected path.
- [ ] Exercise meaningful failure, boundary, authorization, transaction, concurrency, or rollback behavior when the change contract makes it material.

### 5. Prove Completeness and Finalize

- [ ] Trace every applicable task or plan requirement to the final code path and observed result; do not infer completion from a clean build or the presence of changed files.
- [ ] Search for stale names, old mechanisms, duplicate routes or registrations, dead exports, compatibility aliases, obsolete configuration and documentation, and unnecessary tests within the affected capability.
- [ ] Review the complete diff against the approved scope and explain every changed file; remove changes that do not contribute to the business outcome or required evidence.
- [ ] Verify the retained solution remains the simplest complete rung after implementation; collapse wrappers, intermediate states, and abstractions that no longer protect a demonstrated invariant.
- [ ] Mark the coherent change `KEEP` only when its acceptance evidence and required gates pass; otherwise mark it `DISCARD` and revert only run-owned edits, preserving all pre-existing user work.
- [ ] Preserve unrelated user work, clean only run-owned temporary artifacts, and confirm no unapproved external or persisted state changed.
- [ ] Use `DELIVERED` only for a kept, fully implemented and verified outcome; `NO_CHANGE` when no edit is needed or the isolated change is discarded and the baseline restored; `BLOCKED` when a required decision, proof, or safe restoration path is unavailable.
- [ ] Report acceptance traceability, selected solution rung, additions and removals, verification results, test portfolio decisions, deviations, and residual risks.

## Output Contract

```markdown
# Surgical Change Delivery

**Verdict:** DELIVERED | NO_CHANGE | BLOCKED

## Change contract
- Business outcome, protected behavior, scope, non-goals, and affected runtime path

## Solution decision
| Candidate rung | Evidence or tradeoff | Decision |
|---|---|---|
| ... | ... | SELECTED / REJECTED |

## Acceptance and implementation
| Requirement | Owning change | Observable evidence | Result |
|---|---|---|---|
| ... | ... | ... | PASS / FAIL / BLOCKED / UNPROVEN |

## Additions, removals, and residual risks
Files and mechanisms added, updated, consolidated, or deleted; retained compatibility; deviations; cleanup; and unresolved risk.

## Test portfolio decisions
Affected evidence, material risk, `KEEP / ADD / UPDATE / MERGE / DELETE / NO_TEST`, oracle, gate result, removed testware, and review or retirement trigger.
```
