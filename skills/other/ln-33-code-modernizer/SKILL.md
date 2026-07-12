---
name: ln-33-code-modernizer
description: "Modernizes a bounded capability by removing obsolete custom mechanisms or reducing bundle and maintenance cost. Use for proven modernization value; not routine upgrades or tuning."
---

# Code Modernizer

Modernize a bounded capability only when the new design measurably reduces maintenance, risk, dependency duplication, or delivered artifact cost. Preserve behavior, isolate migrations, and revert changes that do not create net value.

## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Current mechanism and consumers | Native file search plus language server or host-native code intelligence | Mapping contracts, callers, configuration, data, lifecycle, and tests | Narrow import, symbol, route, and configuration search with direct reads |
| Existing platform capabilities | Manifests, lockfiles, runtime APIs, and current official documentation | Avoiding new dependencies or custom code for an already available feature | Repository examples and source inspection; mark capability `UNVERIFIED` if current docs are unavailable |
| External replacement candidates | Official package registries, source repositories, documentation, releases, advisories, and license data | Comparing maintained software with custom implementation | Primary-source web research; do not rely on popularity lists alone |
| Baseline and value | Build output, bundle analysis, code inventory, benchmark, defects, or maintenance evidence | Defining what modernization must improve | Reproducible static counts with documented scope and limitations |
| Safe migration | Git isolation, focused edits, native package manager, and repository generation commands | Replacing one bounded capability and its consumers | Stop if user changes or generated state cannot be protected |
| Verification | Repository-defined build, lint, type, test, smoke, packaging, and runtime checks | Before migration and after every retained step | Add a focused compatibility test when existing coverage cannot prove the contract |
| Delivered artifact analysis | Existing bundle analyzer, size report, startup profile, or dependency report | Bundle size, load path, or runtime cost is part of the goal | Build artifact comparison with reproducible file and compression rules |

Do not replace working custom code merely because an external package exists. Do not introduce an unmaintained dependency, accept incompatible licensing, or remove the old path until all consumers and rollback conditions are understood.

## Evidence Rules

- Start from a concrete defect, cost, duplication, unsupported mechanism, audit finding, or user goal.
- Compare net system complexity: removed code and risk minus new dependency, adapter, operational, and migration costs.
- External candidate claims require current primary evidence for maintenance, security, license, runtime support, and API fit.
- Bundle or performance value requires comparable measurements; line-count reduction alone does not prove a better design.
- Preserve public behavior unless the request explicitly authorizes a contract migration.

## Checklist

### 1. Define the Modernization Target

- [ ] Resolve the bounded capability, current pain, affected users or operators, success metric, constraints, and explicit non-goals.
- [ ] Read repository instructions and inspect Git state, generated files, package-manager policy, and current user changes.
- [ ] Inventory the current implementation, public contracts, consumers, configuration, persisted data, runtime registration, tests, and operational procedures.
- [ ] Identify the specific maintenance, security, compatibility, duplication, bundle, startup, or delivery cost that must improve.
- [ ] Establish behavioral and relevant quantitative baselines before changing code.
- [ ] Isolate the work so each migration step can be reverted without touching unrelated or user-owned changes.
- [ ] Start a run-owned resource ledger with every created absolute path, worktree, process ID, cache, report, and temporary artifact; never register pre-existing resources as cleanup targets.
- [ ] Stop if modernization is only aesthetic, depends on speculative future scale, or cannot define a verifiable net benefit.

### 2. Evaluate the Simplest Credible Design

- [ ] Check language, runtime, framework, platform, and already-declared dependency capabilities before searching for a new package.
- [ ] Identify obsolete compatibility paths, parallel mechanisms, unused extension points, duplicated integrations, and transitional adapters that can be removed directly.
- [ ] For external candidates, evaluate functional fit, API stability, maintenance activity, security history, license, ownership, release cadence, size, runtime support, and ecosystem compatibility.
- [ ] Verify candidate claims from official documentation, repository releases, advisories, and package metadata matching the intended version.
- [ ] Inspect migration guides, breaking changes, configuration model, lifecycle, failure behavior, transitive dependencies, and exit strategy.
- [ ] Build a semantic-gap ledger for replacement candidates: input normalization, Unicode/time/date behavior, precision, ordering, errors, cancellation, streaming, concurrency, security limits, and other edge behavior relevant to the current contract.
- [ ] Compare retain, simplify in place, use existing platform capability, adopt external software, and remove capability where each is credible.
- [ ] Estimate code removed, adapters added, dependency and bundle delta, migration effort, operational change, rollback difficulty, and residual lock-in.
- [ ] Select the option with the best evidence-backed value-to-risk ratio, not the newest or most popular option.
- [ ] Mark the chosen option `SELECTED` and every considered but non-chosen option `REJECTED`, recording the evidence or tradeoff that determined each decision.
- [ ] Request user direction when licensing, public contract, persisted-data migration, vendor commitment, or irreversible operational tradeoffs change product intent; applying a migration outside a disposable environment always requires explicit authorization.

### 3. Execute a Bounded Migration

- [ ] Add or identify tests that capture the current external contract, important failures, and data or configuration compatibility.
- [ ] Use differential or characterization cases at the replacement boundary when old and new implementations can be run on the same representative and adversarial inputs.
- [ ] Introduce the replacement at one clear boundary rather than mixing old and new mechanisms throughout the codebase.
- [ ] Use native package-manager and generation commands for dependencies and generated state; do not hand-edit lockfiles or generated artifacts.
- [ ] Update callers, types, configuration, dependency injection, routes, events, serialization, tests, build scripts, and documentation required by the bounded capability.
- [ ] Preserve backward compatibility only where a real consumer requires it and define the removal condition for every temporary adapter.
- [ ] Prepare and test persisted-data or configuration migrations against a disposable copy with explicit ordering, resumability, mixed-version behavior, backup/restore evidence, rollback, and failure recovery; apply them elsewhere only when the user names the target environment and authorizes the rehearsed operation.
- [ ] Remove the old implementation only after search and runtime wiring checks show no remaining consumer.
- [ ] Before removing a dependency or module reported as unused, check dynamic imports, reflection, plugin/config registration, code generation, build scripts, CLIs, and optional runtime paths that static import scans miss.
- [ ] Inspect the diff for unrelated refactoring, formatting churn, duplicate dependencies, debug code, and accidental public contract changes.

### 4. Verify and Keep or Discard

- [ ] Run focused contract and regression tests immediately after each migration step.
- [ ] Run the repository's required build, lint, type, test, smoke, packaging, and application-start checks.
- [ ] Compare the agreed maintenance, dependency, bundle, startup, performance, or defect metric with the baseline under equivalent conditions.
- [ ] For bundle work, compare real build composition, parsed and compressed size, chunking, loading behavior, and source maps rather than package metadata alone.
- [ ] Evaluate entrypoint and route critical paths separately: total bytes may fall while initial transfer, request waterfalls, decompression, parse/compile, execution, or cache invalidation gets worse.
- [ ] Verify tree-shaking and deduplication claims against the actual bundler graph, module format, exports, side-effect metadata, and target browsers/runtimes before changing imports or package metadata.
- [ ] Check security advisories, licenses, runtime support, package provenance, and new transitive dependencies for the retained design.
- [ ] Exercise rollback or removal mechanics when migration failure would be costly or difficult to detect.
- [ ] Mark the migration `KEEP` only when required behavior and verification pass and the defined net value is achieved.
- [ ] Mark it `DISCARD` and revert the bounded change completely when value is unproven, regressions appear, or long-term complexity increases.
- [ ] Remove non-retained adapters, instrumentation, feature flags, packages, and generated artifacts only when their ownership is proven; clean only run-owned ledger paths and exact process IDs, preserving dirty or pre-existing worktrees and reported evidence.

### 5. Finalize and Report

- [ ] Verify that no stale implementation, import, registration, configuration, documentation, or dependency remains after a kept migration.
- [ ] Run full relevant verification on the final retained state and compare the final diff with the original modernization scope.
- [ ] Report considered alternatives, evidence, applied and discarded migrations, code and dependency delta, measurements, verification, and rollback state.
- [ ] Identify residual custom code, compatibility adapters, migration steps, operational changes, and external dependency risks.
- [ ] Use `MODERNIZED` when the selected bounded design is fully retained and verified; use `PARTIAL` when an independently safe subset is retained with explicit remaining work; use `NO_CHANGE` when every migration is discarded and the baseline is restored; use `BLOCKED` when authorization, safety evidence, or required verification is unavailable.

## Output Contract

```markdown
# Code Modernization

**Verdict:** MODERNIZED | PARTIAL | NO_CHANGE | BLOCKED

## Target and baseline
- Capability and current cost
- Contracts and consumers
- Behavioral and quantitative baselines

## Alternatives
| Option | Evidence | Net value | Risk | Decision |
|---|---|---|---|---|
| ... | ... | ... | ... | SELECTED / REJECTED |

## Migration results
| Step | Change | Verification | Metric delta | Decision |
|---|---|---|---|---|
| ... | ... | ... | ... | KEEP / DISCARD |

## Final state and residual risks
Removed and retained code, dependencies, adapters, measurements, rollback, limitations, and follow-up decisions.

## Evidence artifacts
Run-owned paths and hashes for characterization evidence, exact commands, final diff, rollback, and cleanup proof.
```
