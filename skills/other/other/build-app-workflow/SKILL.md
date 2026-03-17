---
name: build-app-workflow
description: Use when building, modifying, validating, or shipping software with long-running agents and you need repeatable execution via Skills + Shell + Compaction. Covers stage-gated workflow, script-driven verification, rollback discipline, and artifact-based delivery across tech stacks (Node/Python/Rust/Tauri and others).
compatibility: hosted-shell, local-shell
---

# build-app-workflow

Convert the Skills + Shell + Compaction methodology into a reusable, stage-gated software delivery workflow.

## When to use

Use this skill when the user is:

- Implementing features or fixes that require real command execution, not advice only.
- Running multi-step tasks likely to exceed short context windows.
- Standardizing engineering workflow with verification and rollback gates.
- Building reusable team SOPs across repositories or stacks.

Do not use this skill for:

- Pure conceptual discussion with no repository changes.
- One-off copywriting tasks without build/test requirements.
- Highly specialized flows that already have a dedicated skill with tighter contracts.

## Inputs to collect first

Collect these inputs before implementation:

1. Goal: one-sentence expected outcome.
2. Scope: files/modules that are in or out of scope.
3. Stack/runtime: Node/Python/Rust/Tauri/other and package managers.
4. Acceptance gate: what must pass (lint/test/build/smoke/etc.).
5. Rollback unit: the exact reversible boundary (single commit or file group).

If any input is missing, ask focused questions before execution.

## Workflow (stage-gated)

### Stage 1 - Plan

1. Define change scope and impact surface.
2. Define rollback point before edits.
3. Run `bash scripts/preflight.sh`.
4. Choose execution mode:

- hosted shell for isolation/repeatability.
- local shell for internal tools and fast iteration.

Reference: `references/workflow.md` sections Plan and Safety.

### Stage 2 - Do

1. Apply minimal, reversible changes.
2. Keep API/type/caller/docs synchronized when interfaces change.
3. Produce concrete artifacts instead of narrative-only output.

Reference: `references/workflow.md` sections Do and Artifact Contract.

### Stage 3 - Check

1. Run `bash scripts/verify.sh --stack auto` (or force `node|python|rust` when needed).
2. Validate against `templates/acceptance-checklist.md`.
3. If failed, run `bash scripts/postmortem.sh "<task-id>"` and fix by failure category.

Reference: `references/workflow.md` sections Check and Failure Routing.

### Stage 4 - Act

1. Summarize change, risk, and rollback path.
2. Record run outcome in `run-log.md`.
3. Apply compaction policy for long runs.

Reference: `references/workflow.md` section Act and Compaction.

## Compaction policy

Use compaction when any condition is met:

- 8-12 consecutive implementation rounds.
- Before major refactor or broad file edits.
- Before release/handoff summary.

Do not compact repeatedly in short intervals without a milestone.

## Stability gate and split policy

Treat this skill as "stable" only when all are true in the latest 5 real tasks:

- verify pass rate >= 4/5.
- zero process failures (missed required checks/docs/rollback notes).
- ad-hoc prompt additions <= 1 per task.
- acceptance records complete.

Split into sub-skills when two or more are true:

- workflow spans >= 3 distinct phases with frequent branching.
- `SKILL.md` becomes long/ambiguous for routing.
- repeated process errors >= 2 in 5 tasks.
- frequent skipped or misordered steps.

Governance details: `../docs/skill-lifecycle.md`.

## Output format required from assistant

Return outputs in this order:

1. Conclusion first.
2. Plan and impact surface.
3. Implemented changes.
4. Verification commands and outcomes.
5. Risks and rollback.
6. Optional next optimizations.
7. Sources used.

Use template: `templates/agent-report.md`.

## Non-negotiables

- Do not place secrets/tokens in code, logs, docs, or examples.
- Do not invent unverified APIs or packages.
- Every change must be reversible.
- API changes require caller/type/doc updates together.
- Prefer script execution evidence over natural-language claims.

## Quick runbook

1. `bash scripts/preflight.sh`
2. Implement minimal scoped changes.
3. `bash scripts/verify.sh --stack auto`
4. `bash scripts/postmortem.sh "<task-id>"` if verification fails.
5. Fill `templates/acceptance-checklist.md` and append `run-log.md`.

## Sources

- https://developers.openai.com/blog/skills-shell-tips
- https://developers.openai.com/api/docs/guides/tools-skills
- https://developers.openai.com/api/docs/guides/tools-shell
- https://developers.openai.com/api/docs/guides/context-management
