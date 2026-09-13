---
name: ln-41-surgical-change-implementer
description: "Implements one scoped feature or fix through the smallest complete solution; not upgrades or performance tuning."
---

# Surgical Change Implementer

**Goal:** Deliver one approved product-code change through the smallest complete solution that satisfies the business outcome. Remove superseded code and avoid speculative abstraction, duplicate mechanisms, and custom infrastructure already provided by the repository or platform.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


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
- [ ] Identify decisions affecting product intent, UX, compatibility, data, dependencies, or external state. Use existing task authorization; ask only when a consequential choice is unresolved or would expand scope.
- [ ] Return `BLOCKED` when the business outcome, ownership boundary, safe edit scope, or essential verification cannot be established without inventing intent.

### 2. Choose the Smallest Complete Solution

- [ ] Test `NO_CHANGE`: verify whether the outcome already holds without edits; a usage explanation may suffice. Documentation or configuration edits belong to `DELETE_OR_CONFIGURE` and require verification as changes.
- [ ] Test `DELETE_OR_CONFIGURE`: identify an obsolete path, wrong default, redundant state, feature flag, registration, or configuration that can be removed or corrected directly.
- [ ] Test `REUSE_LOCAL`: search for the repository's canonical helper, component, service, policy, type, enum, constant, error, or integration before adding another concept.
- [ ] Test `USE_PLATFORM_OR_STDLIB`: verify whether the language, runtime, browser, database, framework, or deployment platform already owns the required generic behavior.
- [ ] Test `REUSE_INSTALLED`: inspect declared dependencies and their supported APIs before proposing a new package or custom mechanism.
- [ ] Consider `ADOPT_DEPENDENCY` only when remaining behavior is generic and material; verify current official guidance, maintenance, security, license, compatibility, transitive cost, and removal path.
- [ ] Use `MINIMAL_CUSTOM` for irreducible product policy or a documented capability or lifecycle-cost gap; name the invariant and why applicable simpler options are insufficient.
- [ ] Stop searching when a candidate completely satisfies the contract at acceptable lifecycle cost; clear later rungs as unnecessary. Compare credible candidates by total complexity and risk, recording the chosen rung and rejected applicable simpler options.
- [ ] Challenge the proposed design for symptom patches, duplicated ownership, speculative extension points, premature abstraction, hidden state, avoidable branching, and temporary compatibility that lacks a real consumer.
- [ ] Define the coherent edit set, deletion set, verification, and rollback boundary before changing code.

### 3. Implement Surgically

- [ ] Change the canonical owning boundary once and update only the consumers required for a complete end-to-end result.
- [ ] Follow repository conventions for naming, types, constants, enums, configuration, errors, logging, security, accessibility, concurrency, transactions, and resource lifecycle.
- [ ] Keep product policy explicit and centralized; do not scatter magic values, duplicated route or event keys, parallel allowlists, or derived state with multiple owners.
- [ ] Use existing dependency and generation workflows; do not hand-edit lockfiles or generated artifacts, add convenience wrappers around already clear APIs, or copy third-party implementation code.
- [ ] Before removal, verify allegedly unused paths against dynamic imports, reflection, registries, configuration, generation, scripts, optional features, and external consumers; static search alone cannot authorize deletion.
- [ ] Remove obsolete branches, helpers, adapters, aliases, flags, exports, configuration, dependencies, documentation, and tests made unnecessary by the retained design.
- [ ] Preserve compatibility only for a verified consumer; make every temporary bridge narrow, observable, owned, time-bounded by a removal trigger, and explicit in the report.
- [ ] Inspect the diff during implementation for unrelated formatting, opportunistic refactoring, accidental UX or contract changes, debug artifacts, and net-new code unsupported by the change contract.

### 4. Build Proportionate Evidence

- [ ] Map each acceptance row and material regression risk to existing evidence before adding tests; assess likelihood, impact, detectability, and blast radius.
- [ ] Choose exactly one portfolio action per affected test or gap: `KEEP`, `ADD`, `UPDATE`, `MERGE`, `DELETE`, or justified `NO_TEST`; remove superseded and low-value testware in the approved scope.
- [ ] Choose unit, integration, contract, or E2E evidence by the material defect and observable outcome it must prove. Prefer the smallest reliable boundary; use E2E when cross-boundary behavior is essential, and avoid duplicating equally strong existing proof.
- [ ] Do not test language, framework, package, database-vendor, generated-code, or trivial wiring behavior. A test must fail for a meaningful defect in this product's business, security, data, or delivery contract.
- [ ] Use stable project-native semantic locators (roles, accessible names, labels) or explicit IDs/test hooks according to the observable contract and locale strategy. Avoid styling, position, timing, and incidental structure. Treat exact-copy assertions separately when copy is a requirement; do not require product edits solely to add hooks when a robust semantic locator exists.
- [ ] Give temporary characterization or migration tests an owner and retirement trigger; keep quarantine explicit and never count skipped, flaky, or unproven evidence as passing.
- [ ] Run focused checks after the coherent edit, then the repository-required build, lint, type, test, smoke, packaging, and application-start gates relevant to the affected path.
- [ ] Exercise meaningful failure, boundary, authorization, transaction, concurrency, or rollback behavior when the change contract makes it material.

### 5. Prove Completeness and Finalize

- [ ] Trace every applicable task or plan requirement to the final code path and observed result; do not infer completion from a clean build or the presence of changed files.
- [ ] Search for stale names, old mechanisms, duplicate routes or registrations, dead exports, compatibility aliases, obsolete configuration and documentation, and unnecessary tests within the affected capability.
- [ ] Review the complete diff against the approved scope and explain every changed file; remove changes that do not contribute to the business outcome or required evidence.
- [ ] Verify the retained solution remains the simplest complete rung after implementation; collapse wrappers, intermediate states, and abstractions that no longer protect a demonstrated invariant.
- [ ] If verification fails, distinguish baseline/environment failures from change-caused defects; repair the latter within scope and rerun affected checks. Keep working until acceptance passes or a concrete prerequisite prevents progress. Mark `KEEP` only with passing required evidence; use `DISCARD` and revert only run-owned edits when the approach is unsuitable or cannot be completed safely, preserving user work.
- [ ] Preserve unrelated user work, clean only run-owned temporary artifacts, and confirm no unapproved external or persisted state changed.
- [ ] Use `DELIVERED` for a kept, fully implemented and verified outcome; `NO_CHANGE` only when the requested outcome already holds without edits; `BLOCKED` when a required decision, proof, safe completion, or restoration path is unavailable. A discarded attempt is not a satisfied request: report the unresolved outcome and restoration state.

- [ ] Verify the delivered increment works with its required consumers and prior increments; reconcile changed requirements against dependent implementation and acceptance evidence before claiming completeness.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Business outcome, protected behavior, mutation scope, non-goals, and affected runtime path. Record selected solution rung and evidence for rejecting applicable simpler options. Map acceptance requirement → owning change → observed evidence → result. Include additions/removals, justified compatibility, test portfolio actions and independent oracles, required gates, deviations, cleanup, and unresolved risks; distinguish an already-satisfied request from an unsuccessful reverted attempt.
