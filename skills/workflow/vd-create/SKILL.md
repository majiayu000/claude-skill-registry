---
name: vd-create
description: Create or refine a VibeDev Studio UnifiedWorkflow graph via tool calls. Use when the user says `$vd-create`, asks the model to “build the workflow graph”, “set up Research/Planning/Execution/Review steps”, or wants the model to collaboratively design prompts/conditions/breakpoints and write them into `unified_workflows` so the UI canvas shows the plan before running `$vd-next`.
---

# `vd-create` (Workflow Authoring Assistant)

## Goal

Turn a user’s project idea into a **visual, editable** workflow graph in the Studio:
- four phases: `research`, `planning`, `execution`, `review`
- node types: `PROMPT`, `CONDITION` (hard/soft), `BREAKPOINT`
- explicit edges (`nextStep`, and for conditions `onPass`/`onFail`)
- each prompt step includes: role/context/task/guardrails/deliverables + `logInstruction`

This skill is for **authoring** a UnifiedWorkflow graph — not for executing steps.

## Key tools

Use the unified workflow tools (these update `job_ui_state.graph_state_json.unified_workflows`):
- `workflow_unified_get`
- `workflow_unified_set_flow_fields`
- `workflow_unified_upsert_step`
- `workflow_unified_connect`
- `workflow_unified_delete_step` (rare)

## Authoring workflow (no fluff, concrete)

### 1) Intake (ask only what you need)

Collect:
- What are we building? (1–2 sentences)
- User technical level: `non-technical | some coding | experienced`
- Constraints: language/framework, OS, timeline, “must-have” vs “nice-to-have”
- Definition of “done”: what can the user do when it’s complete?

### 2) Decide a graph shape (recommended default)

Create **3–6 steps per phase**. Keep each step *one prompt*.

Recommended minimal skeleton:

- Research: scope + repo scan (findings), risk scan (mistake ledger), breakpoint (memory pack)
- Planning: architecture choices, step plan draft, breakpoint (handoff memory)
- Execution: implement incrementally, add tests, condition (tests pass), breakpoint (handoff)
- Review: run full verification, condition (all gates), final summary

### 3) Write the graph into the job

For each phase:
1. Call `workflow_unified_set_flow_fields` to set `name`, `description`, `global_context`.
2. For each node, call `workflow_unified_upsert_step` with a full step object.
3. Call `workflow_unified_connect` to wire `nextStep` / `onPass` / `onFail`.

**Step object requirements**

Match the Studio schema:
- `id`: stable string (recommend `step_<phase>_<slug>`)
- `type`: `PROMPT | CONDITION | BREAKPOINT`
- `label`: `Step1`, `Step2`, `Sub1`, etc.
- `title`: human readable
- `colIndex`: integer
- `subThreadLevel`: integer
- `isSubThread`: boolean

PROMPT fields:
- `role`, `context`, `task`, `guardrails`, `deliverables`, `logInstruction`

CONDITION fields:
- `conditionType`: `script` (hard) or `llm` (soft)
- `conditionCode`: for `llm`, a TRUE/FALSE question; for `script`, a command line to run
- `onPass`, `onFail` (or use `workflow_unified_connect` with `edge=on_pass/on_fail`)

BREAKPOINT fields:
- `reason`
- `carryForward` (memory prompt — instruct model to save a memory pack to context, not print it)

### 4) Confirm and hand off to the user

- Tell the user which job/phase you updated and that it’s visible in the Studio.
- Encourage them to edit anything, then start execution with `$vd-next`.

## Guardrails

- Keep steps small and explicit.
- Prefer conditions as separate nodes (don’t embed “gates sections” in prompts).
- Breakpoints should instruct “save memory pack to context” and “start a new thread”.

