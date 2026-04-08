---
name: ln-220-story-coordinator
description: "Creates, replans, or appends 5-10 Stories per Epic with standards research and multi-epic routing. Use when Epic needs Story decomposition."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Story Coordinator

**Type:** L2 Domain Coordinator
**Category:** 2XX Planning

Runtime-backed Story planning coordinator. The runtime owns flow control, pause/resume, and worker result tracking.

## MANDATORY READ

Load these before execution:
- `shared/references/coordinator_runtime_contract.md`
- `shared/references/story_planning_runtime_contract.md`
- `shared/references/coordinator_summary_contract.md`
- `shared/references/environment_state_contract.md`
- `shared/references/storage_mode_detection.md`
- `shared/references/problem_solving.md`

## Purpose

- assemble Epic planning context
- perform focused standards research when it changes Technical Notes
- build the ideal Story plan before checking existing Stories
- detect routing and mode per epic group
- delegate creation or replanning to standalone workers

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `epicId` | Yes | Epic to decompose |
| `autoApprove` | No | If false, runtime pauses on preview confirmation |

## Runtime

Runtime family: `story-planning-runtime`

Identifier:
- `epic-{epicId}`

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_CONTEXT_ASSEMBLY`
3. `PHASE_2_RESEARCH`
4. `PHASE_3_PLAN`
5. `PHASE_4_ROUTING`
6. `PHASE_5_MODE_DETECTION`
7. `PHASE_6_DELEGATE`
8. `PHASE_7_FINALIZE`
9. `PHASE_8_SELF_CHECK`

Terminal phases:
- `DONE`
- `PAUSED`

## Phase Map

### Phase 1: Context Assembly

Resolve Epic and assemble only the planning inputs that change Story decomposition:
- Epic scope
- success criteria
- known personas and constraints
- project task provider

Checkpoint payload:
- `context_ready`

### Phase 2: Research

Do focused research only when it changes Story Technical Notes or implementation constraints.

Do not let research expand Story scope.

Checkpoint payload:
- `research_status`
- `research_file`

### Phase 3: Plan

Build the ideal Story plan before looking at existing Stories.

Rules:
- vertical slices only
- 5-10 Stories when Epic warrants it
- concise Story statements and observable ACs
- no orchestration prose inside the plan
- delegate ACs must specify what equips the actor (context, instructions, tools, configuration), not just what the actor does

Checkpoint payload:
- `ideal_plan_summary`

### Phase 4: Routing

Route planned Stories to epic groups.

Fast path:
- all Stories stay in the resolved Epic

Pause only when routing is ambiguous or requires confirmation.

Checkpoint payload:
- `routing_summary`

### Phase 5: Mode Detection

Determine mode per epic group:
- `CREATE`
- `REPLAN`
- `ADD`

Checkpoint payload:
- `epic_group_modes`

### Phase 6: Delegate

Delegate by group:
- `ln-221-story-creator`
- `ln-222-story-replanner`

Workers remain standalone-capable. They may optionally write `story-plan` summary artifacts, but must always return the same structured summary even without artifact writing.

Record each result through runtime `record-epic`.

### Phase 7: Finalize

Finalize only after all expected worker summaries are recorded.

**Template compliance gate:** Fetch each created Story via `get_issue`. Run `validateTemplateCompliance(description, 'story')` from `planning-runtime/lib/template-compliance.mjs`. All stories must pass (9 sections in order). Record `template_compliance_passed` in state. Guard blocks SELF_CHECK without it.

Checkpoint payload:
- `final_result`
- `template_compliance_passed`

### Phase 8: Self-Check

Confirm:
- phase coverage
- planned vs produced Story counts
- no missing epic groups

Checkpoint payload:
- `pass`
- `final_result`

## Pending Decisions

Use runtime `PAUSED + pending_decision` for:
- missing context
- routing confirmation
- ambiguous `ADD` vs `REPLAN`
- preview confirmation when `autoApprove=false`

Do not hold these decisions only in chat.

## Worker Contract

Workers:
- do not know the coordinator
- do not read runtime state
- remain standalone
- may receive `summaryArtifactPath`
- return shared summary envelope either way

Expected summary kind:
- `story-plan`

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 6 | `ln-221-story-creator` | CREATE or ADD path |
| 6 | `ln-222-story-replanner` | REPLAN path |

```text
Skill(skill: "ln-221-story-creator", args: "{epicId}")
Skill(skill: "ln-222-story-replanner", args: "{epicId}")
```

## TodoWrite format (mandatory)

```text
- Phase 1: Assemble context (pending)
- Phase 2: Research only what changes Technical Notes (pending)
- Phase 3: Build ideal Story plan (pending)
- Phase 4: Route Stories by Epic (pending)
- Phase 5: Detect mode per group (pending)
- Phase 6: Delegate to worker(s) (pending)
- Phase 7: Finalize result (pending)
- Phase 8: Self-check (pending)
```

## Critical Rules

- Build the ideal plan before checking existing Stories.
- Use research only to improve Technical Notes and implementation realism.
- Do not keep routing or preview approvals in chat-only state.
- Do not create or update Stories directly when a worker should do it.
- Consume worker summaries, not free-text worker prose.

## Definition of Done

- [ ] Runtime started with Epic-scoped identifier
- [ ] Context assembly checkpointed
- [ ] Research checkpointed or explicitly minimal
- [ ] Ideal plan checkpointed
- [ ] Routing checkpointed
- [ ] Mode detection checkpointed
- [ ] All expected worker summaries recorded
- [ ] Final result checkpointed
- [ ] Template compliance passed for all created Stories
- [ ] Self-check passed

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `planning-coordinator`. Run after all phases complete. Output to chat using the protocol format.

## Reference Files

- `shared/references/environment_state_contract.md`
- `shared/references/storage_mode_detection.md`
- `references/replan_algorithm.md`

---

**Version:** 5.0.0
**Last Updated:** 2026-02-03
