---
name: wf-player
description: Workflow template player — load a JSON template produced by wf-composer, bind context variables, execute nodes in DAG order (serial/parallel), persist state at checkpoints, support resume from any checkpoint. Uses ccw-coordinator serial-blocking for CLI nodes and team-coordinate worker pattern for parallel agent nodes. Triggers on "wf-player " or "/wf-player".
argument-hint: "<template-slug|path> [--context key=value...] [--resume <session-id>] [--list] [--dry-run]"
allowed-tools: Agent(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*), Skill(*)
---

# Workflow Run

Load a workflow template → bind variables → execute DAG → persist checkpoints → resume capable.

## Architecture

```
Skill(skill="wf-player", args="<template> --context goal='...'")
  |
  +-- Phase 0: Entry Router
       |-- --list        -> list available templates, exit
       |-- --resume      -> load session, skip to Phase 3 (Execute)
       |-- --dry-run     -> load + show execution plan, no execution
       |-- default       -> Phase 1 (Load)
  |
  +-- Phase 1: Load & Bind
  |    Load template JSON, bind {variables} from --context, validate required vars
  |
  +-- Phase 2: Instantiate
  |    Init session state, topological sort, write WFR session file
  |
  +-- Phase 3: Execute Loop
  |    For each node in order:
  |      skill node   -> Skill(skill=...) [synchronous]
  |      cli node     -> ccw cli [background + stop, hook callback]
  |      command node -> Skill(skill="namespace:cmd") [synchronous]
  |      agent node   -> Agent(...) [run_in_background per node config]
  |      checkpoint   -> save state, optionally pause
  |
  +-- Phase 4: Complete
       Archive session, output summary
```

## Shared Constants

| Constant | Value |
|----------|-------|
| Session prefix | `WFR` |
| Session dir | `.workflow/sessions/WFR-<slug>-<date>/` |
| State file | `session-state.json` |
| Template dir | `.workflow/templates/` |
| Template index | `.workflow/templates/index.json` |

## Entry Router

Parse `$ARGUMENTS`:

| Detection | Condition | Handler |
|-----------|-----------|---------|
| List templates | `--list` in args | -> handleList |
| Resume session | `--resume <session-id>` in args | -> Phase 2 (resume) |
| Dry run | `--dry-run` in args | -> Phase 1 + 2, print plan, exit |
| Normal | Template slug/path provided | -> Phase 1 |
| No args | Empty args | -> handleList + AskUserQuestion |

### handleList

Scan `.workflow/templates/index.json`. Display:
```
Available workflow templates:
  feature-tdd-review    [feature, complex]   3 work nodes, 2 checkpoints
  quick-bugfix          [bugfix, simple]     2 work nodes, 1 checkpoint
  ...

Run: Skill(skill="wf-player", args="<slug> --context goal='...'")
```

---

## Phase 0 (Resume): Session Reconciliation

**Trigger**: `--resume <session-id>` or active WFR session found in `.workflow/sessions/WFR-*/`

1. Scan `.workflow/sessions/WFR-*/session-state.json` for status = "running" | "paused"
2. Multiple found → AskUserQuestion for selection
3. Load session-state.json
4. Identify `last_checkpoint` and `node_states`
5. Reset any `running` nodes back to `pending` (they were interrupted)
6. Determine next executable node from `topological_order` after last checkpoint
7. Resume at Phase 3 (Execute Loop) from that node

---

## Phase 1: Load & Bind

Read `phases/01-load.md` and execute.

**Objective**: Load template, collect missing variables, bind all {variable} references.

**Success**: Template loaded, all required variables bound, `bound_context{}` ready.

---

## Phase 2: Instantiate

Read `phases/02-instantiate.md` and execute.

**Objective**: Create WFR session directory, init state, compute execution plan.

**Success**: `session-state.json` written, topological_order ready.

---

## Phase 3: Execute Loop

Read `phases/03-execute.md` and execute.

**Objective**: Execute each node in topological_order using appropriate mechanism.

**CRITICAL — CLI node blocking**:
- CLI nodes launch `ccw cli` in background and immediately STOP
- Wait for hook callback — DO NOT poll with TaskOutput
- Hook callback resumes execution at next node

**Success**: All nodes completed, all checkpoints saved.

---

## Phase 4: Complete

Read `phases/04-complete.md` and execute.

**Objective**: Archive session, output execution summary and artifact paths.

---

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Required variable missing | AskUserQuestion to collect it |
| Template not found | Show `--list` and suggest closest match |
| Node failed (on_fail=abort) | AskUserQuestion: Retry / Skip / Abort |
| Node failed (on_fail=skip) | Log warning, continue to next node |
| Node failed (on_fail=retry) | Retry once, then abort |
| Interrupted mid-execution | State saved at last checkpoint; resume with `--resume <session-id>` |
| Cycle in DAG | Error immediately, point to template for fix |

## Specs Reference

| Spec | Purpose |
|------|---------|
| [specs/node-executor.md](specs/node-executor.md) | Execution mechanism per node type |
| [specs/state-schema.md](specs/state-schema.md) | session-state.json schema |
