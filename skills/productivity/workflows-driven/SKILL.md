---
name: workflows-driven
description: 'Drive decomposable work as a deterministic multi-subagent workflow: phased fan-out under per-task contracts with adversarial verification. Use for audits, migrations, broad research or review sweeps, work needing independent cross-checks before committing, or scale one context cannot hold.'
metadata:
  short-description: Deterministic phased fan-out with per-task contracts and adversarial verification
---

# Workflows-Driven Development

Shape the work as a **workflow**: a deterministic DAG of phases, each phase a
wave of parallel subagent tasks under explicit contracts, closed by
verification the parent runs itself. The workflow, not the conversation, is
the unit of execution: same decomposition, same contracts, same gates, every
run.

## When to go workflow-shaped

Three shapes earn the ceremony:

- **Coverage**: the task decomposes into parallel slices (audit every module,
  migrate every callsite, survey every subsystem).
- **Confidence**: the result needs independent perspectives or adversarial
  checks before you commit (review waves, competing analyses).
- **Scale**: the evidence exceeds one context window (repo-wide sweeps,
  multi-repo research).

A quick lookup or single edit stays inline; spin up no agents. An ordered
plan with per-task review gates belongs to subagent-driven. A flat split into
independent concerns, with no phase structure or verification wave, belongs to
parallel-launch.

## The contract

Scout inline first (list the files, scope the diff, find the call sites)
until you can name the work list. Then:

1. **Phases.** Order the workflow as phases; a phase is one wave of parallel
   tasks plus a barrier. Later phases consume earlier phases' evidence.
2. **Batch context** carries the shared contract for the whole wave:
   - `# Goal`: what the wave accomplishes.
   - `# Constraints`: rules, non-goals, permissions, verification limits.
   - `# Contract`: shared interfaces, output shape, coordination rules.
3. **Each assignment** is self-contained:
   - `# Target`: exact files, symbols, or evidence surface; explicit non-goals.
   - `# Change`: what to inspect or modify, step by step, patterns to reuse.
   - `# Acceptance`: observable result and return packet. Workers skip
     formatters, linters, and project-wide tests; the parent runs shared proof
     once.
4. **Disjoint write scopes.** Every writing worker owns its paths exclusively;
   shared files (manifests, configs, indexes) are edited only by the parent.
5. **Pointers, not payloads.** Workers exchange file paths and artifacts,
   never pasted blobs.

## Verification patterns

- **Adversarial verify**: dispatch skeptical reviewers with distinct targets;
  keep only findings the parent confirms against source.
- **Perspective-diverse review**: separate correctness, security, performance,
  and maintainability roles instead of identical reviewers.
- **Completeness critic**: after the first wave, one read-only critic asks
  what file, claim, modality, or proof was missed.
- **Circuit breaker**: give each batch a success threshold; when a batch falls
  below it, stop the workflow and rediagnose instead of spending the remaining
  budget on a broken playbook.
- **No silent caps**: bounding coverage (top-N, sampling, no-retry) is
  declared with what was dropped and why, before acting on partial evidence.
- **Parent owns closure**: workers return evidence; the parent reads it,
  resolves contradictions, runs the shared proof, and makes the final call.

## Durability

Track the workflow in the visible todo list, one entry per phase. Keep
evidence in files (artifacts, ledgers), not conversation memory: a resumed or
compacted session must pick up from the ledger alone. On hosts that
checkpoint workflow runs, resume instead of rerunning; completed tasks
return cached evidence.

## Materialize on your host

The contract above is host-neutral; the fan-out primitive is not. Detect,
then read the matching reference:

- **Claude Code** (Dynamic Workflows: `/workflows` exists, plugins ship
  `workflows/*.js`): read `references/claude-code.md`. Default ephemeral;
  build and run the workflow for the task at hand, and save to
  `.claude/workflows/` only when it will recur.
- **oh-my-pi** (a `task` tool that batches `tasks[]`): read
  `references/omp.md`. The `task` batch is the only fan-out primitive; never
  emulate batching with shell loops or eval helpers.
- **Neither**: run the same contract inline as sequential waves of subagent
  calls, same batch context and assignments, parent owns closure.

## Red flags

- One worker spawned, parent idle behind it: do that work inline.
- Independent slices dispatched serially: one wave, one batch.
- A wave declared done without the parent's own proof pass.
- Two workers writing one file: the wave was mis-partitioned; stop and re-cut.
- A coverage cap the summary never mentions.
