---
name: ln-42-dependency-upgrader
description: "Upgrades dependencies in reversible batches with version-specific compatibility and regression checks."
---

# Dependency Upgrader

**Goal:** Upgrade dependencies in small, attributable batches. Preserve manifests, lockfiles, runtime support, and product behavior; do not treat a newer version as valuable without compatibility, security, or maintenance evidence.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Package-manager detection | Manifests, lockfiles, workspace files, runtime files, and repository instructions | Always before choosing commands or update scope | Build and CI configuration |
| Outdated and vulnerable packages | Native package-manager outdated and audit commands | The manager and registry are available | Official registry, vendor advisory, and lockfile inspection |
| Breaking changes and support | Official release notes, migration guides, changelogs, advisories, and runtime support tables | Every consequential minor, major, replacement, or security update | Primary-source repository releases; otherwise mark `UNVERIFIED` |
| Usage and blast radius | Language server or host-native code intelligence | An updated API, type, plugin, build tool, or runtime may affect consumers | Targeted import, symbol, configuration, and script search |
| Safe version changes | Native package-manager commands | Updating manifests and generated lock state | Do not hand-edit lockfiles or emulate package resolution |
| Verification | Repository-defined install, restore, build, lint, type, test, migration, and smoke commands | Before changes and after each batch | CI and script inspection with explicit unverified status |
| Diff and rollback | Git status, diff, and isolated commits or worktree | Protecting user changes and reverting only the failed batch | Stop if the batch cannot be isolated safely |

Never publish packages, rotate credentials, deploy, or weaken audit and verification gates. Do not run lifecycle scripts from an untrusted package source without the environment's normal safeguards.

## Evidence Rules

- Manifests declare constraints and lockfiles record resolved versions; install metadata proves the active environment when it differs. Registry "latest" does not override runtime or compatibility constraints.
- A vulnerability finding requires the affected version, advisory, reachability or exposure context, and a credible remediation.
- A breaking-change claim requires release or migration evidence matching the exact version transition.
- Keep generated lockfile changes only when produced by the selected native package manager and expected repository version.
- Upgrade success requires repository verification, not only a successful install or restore.

## Checklist

### 1. Discover Scope and Protect the Workspace

- [ ] Detect package managers, manifests, locks, registries, runtime/tool pins, generated state, and dependency-linked workspaces within the requested update scope; expand only for demonstrated compatibility dependencies.
- [ ] Classify each deliverable as an application, library, plugin, CLI, container, or build tool so version ranges, lockfiles, peer constraints, and supported-runtime promises are interpreted correctly.
- [ ] Read repository instructions and determine supported package-manager versions, update commands, lockfile policy, and CI expectations.
- [ ] Inspect Git state and isolate the work so existing user changes cannot be overwritten or mistaken for upgrade output.
- [ ] Start a run-owned resource ledger with every created absolute path, worktree, process ID, cache, report, and temporary artifact; never register pre-existing resources as cleanup targets.
- [ ] Resolve the requested scope: security-only, routine patch or minor maintenance, selected packages, majors, runtime migration, or complete refresh.
- [ ] Capture install or restore, build, lint, type, test, smoke, and security-audit baseline before editing.
- [ ] Record pre-existing failures, advisories, deprecations, peer conflicts, and unsupported runtime combinations.

### 2. Research and Plan Batches

- [ ] Use native outdated and audit commands to inventory direct and relevant transitive updates without changing files.
- [ ] Separate removals, security fixes, routine updates, major changes, build-tool changes, and runtime or ecosystem migrations.
- [ ] Check official release notes and migration guides for API changes, configuration changes, defaults, peer constraints, runtime support, and removed behavior.
- [ ] Resolve environment markers, extras, optional/dev groups, peer dependencies, target frameworks, and platform-specific packages; a graph that resolves only on the current machine is not sufficient when the project promises a wider matrix.
- [ ] Check official advisories for affected ranges, exploit conditions, fixed versions, workarounds, and whether the dependency is reachable in this project.
- [ ] Search actual imports, symbols, plugins, scripts, configuration, generated code, and runtime loading for every consequential dependency.
- [ ] Identify unused, duplicate, abandoned, replaced, or platform-redundant dependencies as separate removal candidates; require runtime and dynamic-loading evidence, and explicit user approval when removal is outside the requested upgrade scope.
- [ ] Order batches by the actual compatibility graph; package manager/runtime, tooling, foundational libraries, framework, integrations, and leaves are a discovery guide, not a fixed sequence. Combine mutually dependent transitions.
- [ ] Keep routine batches small enough to attribute failure; batch framework families, analyzers, generated clients, or tightly constrained peers together only when their compatibility matrix requires it.
- [ ] Stop for user direction when mutually exclusive version strategies, runtime support, licensing, registry policy, or migration scope changes product intent.

### 3. Apply Each Batch Safely

- [ ] Use the native package manager to update manifests and lockfiles with the repository's expected version and flags.
- [ ] Avoid broad re-resolution when the request is narrow unless the manager cannot preserve the lock graph safely; explain unavoidable churn.
- [ ] Inspect install scripts, registry source, checksums, package provenance, and unexpected new transitive packages when security risk warrants it.
- [ ] Update imports, APIs, types, configuration, build scripts, plugins, generated clients, and application code required by documented breaking changes.
- [ ] Update user or operator documentation only when accepted behavior, prerequisites, configuration, or commands change.
- [ ] Inspect the diff immediately for unrelated formatting, deleted constraints, registry drift, line-ending churn, generated artifacts, and accidental downgrades.
- [ ] Inspect the resolved graph for newly duplicated major versions, unsatisfied or silently ignored peers, changed optional features, and transitive substitutions that alter runtime behavior.
- [ ] Do not suppress warnings, disable audits, skip required checks, pin incompatible peers forcibly, or add compatibility hacks without evidence.

### 4. Verify and Keep or Revert

- [ ] Run install or restore from a clean-enough state to prove lockfile reproducibility.
- [ ] Run the relevant build, lint, type, unit, integration, smoke, packaging, migration, and application-start checks after each batch.
- [ ] Classify affected runtime, target-framework, OS, architecture, and feature combinations as required or optional; retain a batch only with local or trusted CI evidence for every required cell, and return `BLOCKED` when required coverage has no credible fallback.
- [ ] Exercise changed APIs, plugins, serializers, build outputs, and runtime paths that generic tests may not cover.
- [ ] Compare bundle, startup, artifact, or performance metrics when the updated dependency can materially change them.
- [ ] Re-run the security audit and distinguish fixed, remaining, newly introduced, unreachable, and no-fix advisories.
- [ ] Keep the batch only when verification passes and expected behavior remains supported.
- [ ] For a failed batch, distinguish baseline or environment failures from upgrade defects; repair bounded migration errors and recheck, or revert the entire batch without touching user work. Record the blocker and continue only with independent safe batches.
- [ ] Establish the retained dependency state as the baseline before applying the next batch.
- [ ] Classify each planned batch as `KEPT` when applied and verified, `REVERTED` when applied then fully rolled back after failed verification, or `SKIPPED` when deliberately not applied because a required decision, compatibility strategy, or independent prerequisite is unresolved.

### 5. Finalize and Report

- [ ] Confirm all required repository verification covers the combined retained state. Reuse still-valid results; run missing checks and rerun those invalidated by later batches or unresolved failures.
- [ ] Confirm manifests, lockfiles, runtime pins, CI, containers, documentation, and generated metadata agree on the final versions.
- [ ] Remove only run-owned ledger entries: verify absolute paths remain inside approved temporary roots, stop exact recorded process IDs, preserve dirty or pre-existing worktrees, and retain evidence artifacts intentionally reported.
- [ ] List intentionally skipped packages with exact constraint, risk, advisory, or migration reason.
- [ ] Reconcile the batch ledger with final versions, migration edits, advisories, lockfile churn, and residual risks.
- [ ] Use `UPDATED` only when the requested update scope is satisfied and verified; `PARTIAL` when a safe subset is retained but requested work or optional coverage remains; `NO_CHANGE` when no batch is retained and baseline is restored; `BLOCKED` when safe progress or required verification is unavailable.

- [ ] Bind each retained batch to its original and final dependency state, runtime/configuration, compatibility evidence, and any invalidated checks.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Managers, workspaces, runtimes, requested update policy, and pre-existing failures/advisories. Per batch: packages, versions, migrations, `KEPT / REVERTED / SKIPPED`, and verification. Include fixed/remaining/new advisories, peer/runtime/registry constraints, lockfile churn, skipped-package reasons, combined-state checks, run-owned manifest/lockfile/diff and rollback/cleanup evidence.
