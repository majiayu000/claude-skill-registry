---
name: ln-300-task-coordinator
description: "Analyzes Story and builds optimal task plan (1-8 tasks), then routes to create or replan. Use when Story needs task breakdown or replanning."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Task Coordinator

**Type:** L2 Domain Coordinator
**Category:** 3XX Planning

Runtime-backed task planning coordinator. The runtime owns readiness gating, pause/resume, and worker result tracking.

## MANDATORY READ

Load these before execution:
- `shared/references/coordinator_runtime_contract.md`
- `shared/references/task_planning_runtime_contract.md`
- `shared/references/coordinator_summary_contract.md`
- `shared/references/tools_config_guide.md`
- `shared/references/storage_mode_detection.md`
- `shared/references/problem_solving.md`
- `shared/references/creation_quality_checklist.md`

## Purpose

- resolve Story context once
- build an ideal implementation task plan before checking existing tasks
- run a deterministic readiness gate
- detect `CREATE`, `ADD`, or `REPLAN`
- delegate to standalone workers

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `storyId` | Yes | Story to plan |
| `autoApprove` | No | If false, runtime may pause for readiness approval |

## Runtime

Runtime family: `task-planning-runtime`

Identifier:
- `story-{storyId}`

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVERY`
3. `PHASE_2_DECOMPOSE`
4. `PHASE_3_READINESS_GATE`
5. `PHASE_4_MODE_DETECTION`
6. `PHASE_5_DELEGATE`
7. `PHASE_6_VERIFY`
8. `PHASE_7_SELF_CHECK`

Terminal phases:
- `DONE`
- `PAUSED`

## Phase Map

### Phase 1: Discovery

Resolve Story and collect only the inputs required for task planning:
- Story AC
- Technical Notes
- Context
- task provider

Checkpoint payload:
- `discovery_ready`

### Phase 2: Decompose

Build the ideal task plan before checking existing tasks.

Rules:
- implementation tasks only
- 1-8 tasks
- no tests or refactoring tasks here
- preserve foundation-first order
- assign meaningful verification intent

Checkpoint payload:
- `ideal_plan_summary`

### Phase 3: Readiness Gate

Score the plan before delegation.

Scoring policy:
- `6-7` -> continue
- `4-5` -> `PAUSED` for approval or improvement
- `<4` -> blocked until plan is corrected

Checkpoint payload:
- `readiness_score`
- `readiness_findings`

### Phase 4: Mode Detection

Detect:
- `CREATE`
- `ADD`
- `REPLAN`

Pause when mode is ambiguous.

Checkpoint payload:
- `mode_detection`

### Phase 5: Delegate

Delegate to exactly one worker:
- `ln-301-task-creator`
- `ln-302-task-replanner`

Workers remain standalone-capable. They may optionally write `task-plan` summary artifacts, but must always return the same structured summary even without artifact writing.

Record the result through runtime `record-plan`.

### Phase 6: Verify

Verify worker result and resulting task plan outcome.

Checkpoint payload:
- `verification_summary`
- `final_result`

### Phase 7: Self-Check

Confirm:
- phase coverage
- readiness gate was respected
- worker result was recorded
- verification completed

Checkpoint payload:
- `pass`
- `final_result`

## Pending Decisions

Use runtime `PAUSED + pending_decision` for:
- ambiguous `ADD` vs `REPLAN`
- readiness approval for score `4-5`
- missing critical Story context

## Worker Contract

Workers:
- do not know the coordinator
- do not read runtime state
- remain standalone
- may receive `summaryArtifactPath`
- return shared summary envelope either way

Expected summary kind:
- `task-plan`

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 5 | `ln-301-task-creator` | CREATE or ADD path |
| 5 | `ln-302-task-replanner` | REPLAN path |

```text
Skill(skill: "ln-301-task-creator", args: "{storyId}")
Skill(skill: "ln-302-task-replanner", args: "{storyId}")
```

## TodoWrite format (mandatory)

```text
- Phase 1: Discover Story context (pending)
- Phase 2: Build ideal task plan (pending)
- Phase 3: Run readiness gate (pending)
- Phase 4: Detect mode (pending)
- Phase 5: Delegate to worker (pending)
- Phase 6: Verify worker result (pending)
- Phase 7: Self-check (pending)
```

## Critical Rules

- Build the ideal plan before looking at existing tasks.
- Readiness gate is the only source of delegation readiness.
- Do not create test or refactoring tasks in this skill.
- Do not keep approval state in chat-only form.
- Consume worker summaries, not free-text worker prose.

## Definition of Done

- [ ] Runtime started with Story-scoped identifier
- [ ] Discovery checkpointed
- [ ] Ideal plan checkpointed
- [ ] Readiness gate checkpointed
- [ ] Mode detection checkpointed
- [ ] Task-plan worker summary recorded
- [ ] Verification checkpointed
- [ ] Self-check passed

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `planning-coordinator`. Run after all phases complete. Output to chat using the protocol format.

---
**Version:** 4.0.0
**Last Updated:** 2026-02-03
