---
name: architecture-foundation
description: Design architecture foundations before implementation. Use when asked to design or refactor architecture, choose Rust/Go crate, package, module, runtime, workflow, or service boundaries, compare mature project architecture, prevent stacked one-off PRs, audit migration debt in existing repos, or produce a spec before coding.
---

# Architecture Foundation

## Overview

Use this skill to turn an architecture discussion into explicit boundaries,
contracts, validation gates, and a small execution plan. The goal is not to copy
an admired project, but to identify the project's shape and choose the minimum
architecture that keeps ownership, effects, errors, and tests clear.
For large existing repos, first explain the architecture they already have,
then decide whether the work is boundary creation, boundary completion, or
boundary deletion.

## When To Use

- The user asks "what architecture should this use?", "is this stacked work?",
  "make a complete spec", "design the runtime", or "compare good libraries".
- The change touches runtime, state ownership, adapters, plugins, event loops,
  rendering, schedulers, persistence, or cross-module contracts.
- A repo has many issues/PRs that look individually valid but may not converge
  on one architecture.
- A mature repo has duplicated paths, compatibility shims, generated configs,
  workflow definitions, or docs that may disagree about the source of truth.
- A new skill, framework, library, or large feature needs a foundation guide
  before implementation.

Do not use this for small, local fixes where the existing architecture is
obvious and no boundary decision is needed.

## Workflow

1. Search first.
- Inspect existing architecture docs, entrypoints, manifests, module trees,
  public APIs, open issues/PRs, and tests before proposing new structure.
- If the user names a reference project, verify current source or official docs
  before treating it as evidence.
- For existing repos, also inspect generated/config artifacts, migration files,
  background workers, cron jobs, adapters, and the largest files/tests.

2. Classify the project shape.
- Simple library: stable API plus internal implementation.
- CLI or developer tool: command layer, core operations, IO adapters, reporter.
- API gateway or model router: transport, auth/accounting, routing policy,
  provider adapters, billing/settlement, observability.
- Long-running runtime: state root, scheduler, drivers, observability, shutdown.
- Lifecycle/composition framework: dependency graph, construction phase,
  runtime hooks, rollback, shutdown, and test harness.
- Event/cache/reconcile controller: watch/list input, cache/projection,
  queue/backpressure, worker/reconciler, retry, and drain.
- Config/module platform: canonical config, adapters, module lifecycle,
  reload order, rollback, cleanup, and plugin host interfaces.
- UI or app shell: state ownership, event protocol, renderer/platform boundary,
  headless tests.
- Service framework: domain core, application services, transport, storage,
  middleware, error-to-response boundary.
- Agent or workflow system: task model, scheduler, provider adapters, event log,
  replay/test harness.

3. Choose one primary state ownership model.
- App-owned entities and handles for native UI/editor runtimes.
- State plus typed message for enumerated UI/application workflows.
- Virtual DOM/signals when renderer portability and declarative UI dominate.
- Typed state or service-instance state for services and middleware.
- Event log plus projection/outbox for workflows, billing, async jobs, and
  reconciliation systems.
- World/resource/system model only when data-parallel ECS is a product fit.
- Snapshot database or input facts for incremental analysis tools.
- Streaming pipeline for one-shot CLI tools and batch processors.

4. Draw the foundation boundaries.
- `product/app`: entrypoints, user workflows, product-specific orchestration.
- `core/domain`: pure models, invariants, decisions, typed errors, no IO.
- `runtime/application`: lifecycle, scheduling, event dispatch, state mutation.
- `adapters/backends`: OS, renderer, provider, filesystem, network, database.
- `plugins/components`: optional capabilities behind explicit contracts.
- `testing/headless`: deterministic drivers, fake adapters, contract tests.

5. Audit existing boundary health before adding tasks.
- Name the current source of truth for each contract: code, database table,
  SQL seed, JSON/YAML config, generated docs, or external provider contract.
- Mark duplicated paths as `intentional bridge`, `legacy compatibility`, or
  `accidental fork`; require an exit condition for compatibility paths.
- Prefer a convergence/deletion plan over a new abstraction when the existing
  architecture is directionally correct but half migrated.
- Treat generated files and docs as consumers unless the repo explicitly makes
  them authoritative.

6. Write the contracts before tasks.
- Ownership: who owns state, handles, resources, caches, and mutation rights.
- Lifecycle: init, ready, run/tick/frame/request, shutdown, cleanup.
- Effect contract: which layer may persist, call providers, bill, publish
  messages, mutate projections, or only emit effects for another layer.
- Event/action: how external events become typed commands/messages/actions.
- Effects: which layer may touch IO, processes, network, OS handles, GPU, DOM,
  databases, or providers.
- Error policy: what is recoverable, user-visible, fatal, diagnostic-only, or
  converted at a boundary.
- Config/resources: build-time, startup-time, runtime; owner and invalidation.
- Observability: logs, metrics, traces, queue depth, frame/runtime telemetry.
- Tests: unit, contract, headless, fake adapter, integration, platform/E2E.

7. Produce a spec, not just a diagram.
- Use `references/spec-template.md` when the user needs a durable artifact.
- Include non-goals and "do not copy" notes from reference projects.
- For every reference project, separate `borrow` from `do_not_copy`; borrow
  boundary contracts, not scale artifacts, global registries, generated
  machinery, historical migrations, or domain-specific complexity.
- Convert the spec into P0/P1/P2 work where each task maps to one contract.
- If issues/PRs already exist, map them to the contracts and identify gaps.

## Decision Rules

- Prefer a thin adapter around a mature runtime when the product does not need
  to own that runtime.
- Split crates/modules only for stable API boundaries, side-effect isolation,
  compile-time isolation, independent tests, or real reuse.
- In existing repos, do not split crates/packages first when the real problem is
  duplicated source-of-truth, an unfinished migration, or missing closed-loop
  tests.
- Keep core free of platform handles, event loops, renderer handles, webviews,
  database clients, HTTP requests, process spawning, and environment reads.
- Make hidden global state illegal unless it is deliberately modeled as typed
  runtime state or a scoped resource.
- Do not let plugins become architecture escape hatches. Each plugin needs API,
  config/permissions when relevant, lifecycle, errors, and tests.
- Do not accept silent degradation. Missing capability must be an explicit
  unsupported error, diagnostic, or blank result according to the contract.

## Output Shape

For quick answers, return:

```text
verdict:
chosen_shape:
state_owner:
boundaries:
contracts:
migration_debt:
validation:
risks:
next_steps:
```

For durable planning, create or update an architecture spec with:

```text
objective
current evidence
reference models considered
chosen architecture
boundary map
source-of-truth map
contract matrix
compatibility/deletion plan
issue/PR map
validation matrix
P0/P1/P2 roadmap
open questions
```

## Red Flags

- A proposed module cannot say which boundary it belongs to.
- The design names a trait/config/cache/plugin but does not wire it into
  startup, lifecycle, or tests.
- Two state ownership models are mixed without an explicit bridge.
- Two files, configs, SQL seeds, or docs claim to be the source of truth for the
  same product contract.
- A compatibility shim or legacy path has no owner, test, telemetry, or removal
  condition.
- Platform callbacks directly mutate core state.
- Errors become warnings plus fallback for user-visible behavior.
- Tests only cover the final UI/CLI and cannot drive the runtime headlessly.
- The plan says "match X project" but cannot state what not to copy.

## References

- Read `references/rust-architecture-patterns.md` when designing Rust crates,
  runtimes, UI frameworks, app shells, schedulers, services, or developer tools.
- Read `references/go-architecture-patterns.md` when designing Go modules,
  packages, services, ports/adapters, context-aware APIs, or concurrency flows.
- Read `references/spec-template.md` when producing a repo-facing spec.
- Use `agents/openai.yaml` only when a separate architecture review agent is
  needed for cross-checking the chosen boundaries or migration plan.
