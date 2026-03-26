---
name: vibe
description: Vibe Code Orchestrator (VCO) is a governed runtime entry that freezes requirements, plans XL-first execution, and enforces verification and phase cleanup.
---

# Vibe Governed Runtime

`vibe` is a host-syntax-neutral skill contract.

`/vibe`, `$vibe`, and agent-invoked `vibe` all mean the same thing: enter the same governed runtime, not different entrypoints.

## What `vibe` Does

`vibe` is the official governed runtime for tasks that need:

- requirement clarification before execution
- one-shot autonomous execution with retained governance
- multi-step planning and implementation
- multi-agent XL orchestration
- proof, verification, and mandatory cleanup

This runtime is user-facing as one path only.

The user does not choose between `M`, `L`, or `XL` as entry branches.
Those grades still exist, but only as internal execution strategy.

## When To Use

Use `vibe` when the task is not a trivial one-line edit and you want the system to:

- inspect the repo and active skeleton first
- clarify or infer intent before building
- freeze a requirement document
- generate an XL-style execution plan
- execute in phases with explicit verification
- clean up phase artifacts and managed node residue

Do not use `vibe` for:

- casual Q and A
- simple explanation-only requests
- tiny edits where governed overhead is unnecessary

## Unified Runtime Contract

`vibe` always runs the same 6-stage state machine:

1. `skeleton_check`
2. `deep_interview`
3. `requirement_doc`
4. `xl_plan`
5. `plan_execute`
6. `phase_cleanup`

These stages are mandatory.
They may become lighter for simple work, but they are not skipped as a matter of policy.

## Runtime Mode

### `interactive_governed`

Default and effective mode.

Use this when the system should still ask the user high-value questions, confirm frozen requirements, and pause at plan approval boundaries.

### `benchmark_autonomous`

Legacy compatibility alias only.

If older callers still pass `benchmark_autonomous`, the runtime silently normalizes it to `interactive_governed`.
It is not a separate execution plane and it must not create a second unattended control path.

## Internal Execution Grades

`M`, `L`, and `XL` remain active, but only as internal orchestration grades.

- `M`: narrow execution, single-agent or tightly scoped work
- `L`: design or coordination work that needs staged planning and review
- `XL`: parallelizable or long-running work that benefits from agent teams and wave control

The governed runtime selects the internal grade after `deep_interview` and before `plan_execute`.

User-facing behavior stays the same regardless of host syntax:

- one governed entry
- one frozen requirement surface
- one XL-style plan surface
- one execution and cleanup contract

Compatibility notes for downstream verification and host adapters:

- `M=single-agent`
- `L grade always follows: design → plan → user approval → subagent execution → two-stage review.`
- XL native lifecycle APIs remain `spawn_agent`/`send_input`/`wait`/`close_agent`

## Stage Contract

### 1. `skeleton_check`

Check repo shape, active branch, existing plan or requirement artifacts, and runtime prerequisites before starting.

### 2. `deep_interview`

Produce a structured intent contract containing:

- goal
- deliverable
- constraints
- acceptance criteria
- non-goals
- autonomy mode
- inferred assumptions

In `interactive_governed`, this stage may ask direct questions.
Legacy `benchmark_autonomous` input is normalized before this stage runs, so intent capture stays on the same governed mode.

### 3. `requirement_doc`

Freeze a single requirement document under `docs/requirements/`.

After this point, execution should trace back to the requirement document rather than to raw chat history.

### 4. `xl_plan`

Write the execution plan under `docs/plans/`.

The plan must contain:

- internal grade decision
- wave or batch structure
- ownership boundaries
- verification commands
- rollback rules
- phase cleanup expectations

### 5. `plan_execute`

Execute the approved plan.

If the work is parallelizable, prefer Codex-native XL orchestration.
If subagents are spawned, their prompts must end with `$vibe`.

### 6. `phase_cleanup`

Cleanup is part of the runtime, not an afterthought.

Each phase must leave behind:

- cleanup receipt
- temp-file cleanup result
- node audit or cleanup result
- proof artifacts needed for later verification

## Router And Runtime Authority

The canonical router remains authoritative for route selection.

`vibe` does not create a second router.
It consumes the canonical route, confirm, unattended, and overlay surfaces and then executes the governed runtime contract around them.

Rules:

- explicit user tool choice still overrides routing
- `confirm_required` still uses the existing white-box `user_confirm interface`
- unattended behavior is mapped into governed runtime mode, not into a separate control plane
- provider-backed intelligence may advise but must not replace route authority

## Compatibility With Process Layers

Other workflow layers may shape discipline, but they must not become a parallel runtime.

Required ownership split:

- canonical router: route authority
- `vibe`: governed runtime authority
- host bridge: hidden hook wiring and artifact persistence
- superpowers or other process helpers: discipline and workflow advice only

Forbidden outcomes:

- second visible startup/runtime prompt surface
- second requirement freeze surface
- second execution-plan surface
- second route authority

## Protocol Map

Read these protocols on demand:

- `protocols/runtime.md`: governed runtime contract and stage ownership
- `protocols/think.md`: planning, research, and pre-execution analysis
- `protocols/do.md`: coding, debugging, and verification
- `protocols/review.md`: review and quality gates
- `protocols/team.md`: XL multi-agent orchestration
- `protocols/retro.md`: retrospective and learning capture

## Learn And Retro Surface

For LEARN / retrospective work, use the `Context Retro Advisor` vocabulary from `protocols/retro.md`.

- retro outputs should preserve `CER format` artifacts when that protocol is invoked
- completion-language corrections remain governed and evidence-backed

## Memory Rules

Memory remains runtime-neutral:

- `state_store (runtime-neutral)`: default session memory
- Serena: explicit decisions only
- ruflo: optional short-horizon vector memory
- Cognee: optional long-horizon graph memory
- episodic memory: disabled in governed routing

## Quality Rules

Never claim success without evidence.

Minimum invariants:

- verification before completion
- no silent no-regression claims
- requirement and plan artifacts remain traceable
- cleanup receipts are emitted before phase completion is claimed

## Outputs

The governed runtime should leave behind:

- `outputs/runtime/vibe-sessions/<run-id>/skeleton-receipt.json`
- `outputs/runtime/vibe-sessions/<run-id>/intent-contract.json`
- `docs/requirements/YYYY-MM-DD-<topic>.md`
- `docs/plans/YYYY-MM-DD-<topic>-execution-plan.md`
- `outputs/runtime/vibe-sessions/<run-id>/phase-*.json`
- `outputs/runtime/vibe-sessions/<run-id>/cleanup-receipt.json`

## Known Boundaries

- the canonical router still owns route selection
- install or check surfaces should not be rebaselined casually
- host adapters may shape capability declarations, but must not fork runtime truth
- benchmark autonomy does not mean governance-free execution

## Maintenance

- Runtime family: governed-runtime-first
- Version: 2.3.49
- Updated: 2026-03-23
- Canonical router: `scripts/router/resolve-pack-route.ps1`
- Primary contract metadata: `core/skill-contracts/v1/vibe.json`
