---
name: wf-composer
description: Semantic workflow composer — parse natural language workflow description into a DAG of skill/CLI/agent nodes, auto-inject checkpoint save nodes, confirm with user, persist as reusable JSON template. Triggers on "wf-composer " or "/wf-composer".
argument-hint: "[workflow description]"
allowed-tools: Agent(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Workflow Design

Parse user's semantic workflow description → decompose into nodes → map to executors → auto-inject checkpoints → confirm pipeline → save as reusable `workflow-template.json`.

## Architecture

```
User describes workflow in natural language
  -> Phase 1: Parse — extract intent steps + variables
  -> Phase 2: Resolve — map each step to executor (skill/cli/agent/command)
  -> Phase 3: Enrich — inject checkpoint nodes, set DAG edges
  -> Phase 4: Confirm — visualize pipeline, user approval/edit
  -> Phase 5: Persist — save .workflow/templates/<name>.json
```

## Shared Constants

| Constant | Value |
|----------|-------|
| Session prefix | `WFD` |
| Template dir | `.workflow/templates/` |
| Template ID format | `wft-<slug>-<date>` |
| Node ID format | `N-<seq>` (e.g. N-001), `CP-<seq>` for checkpoints |
| Max nodes | 20 |

## Entry Router

Parse `$ARGUMENTS`.

| Detection | Condition | Handler |
|-----------|-----------|---------|
| Resume design | `--resume` flag or existing WFD session | -> Phase 0: Resume |
| Edit template | `--edit <template-id>` flag | -> Phase 0: Load + Edit |
| New design | Default | -> Phase 1: Parse |

## Phase 0: Resume / Edit (optional)

**Resume design session**:
1. Scan `.workflow/templates/design-drafts/WFD-*.json` for in-progress designs
2. Multiple found → AskUserQuestion for selection
3. Load draft → skip to last incomplete phase

**Edit existing template**:
1. Load template from `--edit` path
2. Show current pipeline visualization
3. AskUserQuestion: which nodes to modify/add/remove
4. Re-enter at Phase 3 (Enrich) with edits applied

---

## Phase 1: Parse

Read `phases/01-parse.md` and execute.

**Objective**: Extract structured semantic steps + context variables from natural language.

**Success**: `design-session/intent.json` written with: steps[], variables[], task_type, complexity.

---

## Phase 2: Resolve

Read `phases/02-resolve.md` and execute.

**Objective**: Map each intent step to a concrete executor node.

**Executor types**:
- `skill` — invoke via `Skill(skill=..., args=...)`
- `cli` — invoke via `ccw cli -p "..." --tool ... --mode ...`
- `command` — invoke via `Skill(skill="<namespace:command>", args=...)`
- `agent` — invoke via `Agent(subagent_type=..., prompt=...)`
- `checkpoint` — state save + optional user pause

**Success**: `design-session/nodes.json` written with resolved executor for each step.

---

## Phase 3: Enrich

Read `phases/03-enrich.md` and execute.

**Objective**: Build DAG edges, auto-inject checkpoints at phase boundaries, validate port compatibility.

**Checkpoint injection rules**:
- After every `skill` → `skill` transition that crosses a semantic phase boundary
- Before any long-running `agent` spawn
- After any node that produces a persistent artifact (plan, spec, analysis)
- At user-defined breakpoints (if any)

**Success**: `design-session/dag.json` with nodes[], edges[], checkpoints[], context_schema{}.

---

## Phase 4: Confirm

Read `phases/04-confirm.md` and execute.

**Objective**: Visualize the pipeline, present to user, incorporate edits.

**Display format**:
```
Pipeline: <template-name>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
N-001 [skill]      workflow-lite-plan       "{goal}"
  |
CP-01 [checkpoint] After Plan               auto-continue
  |
N-002 [skill]      workflow-test-fix        "--session N-001"
  |
CP-02 [checkpoint] After Tests              pause-for-user
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Variables: goal (required)
Checkpoints: 2 (1 auto, 1 pause)
```

AskUserQuestion:
- Confirm & Save
- Edit node (select node ID)
- Add node after (select position)
- Remove node (select node ID)
- Rename template

**Success**: User confirmed pipeline. Final dag.json ready.

---

## Phase 5: Persist

Read `phases/05-persist.md` and execute.

**Objective**: Assemble final template JSON, write to template library, output summary.

**Output**:
- `.workflow/templates/<slug>.json` — the reusable template
- Console summary with template path + usage command

**Success**: Template saved. User shown: `Skill(skill="wf-player", args="<template-path>")`

---

## Specs Reference

| Spec | Purpose |
|------|---------|
| [specs/node-catalog.md](specs/node-catalog.md) | Available executors, port definitions, arg templates |
| [specs/template-schema.md](specs/template-schema.md) | Full JSON template schema |
