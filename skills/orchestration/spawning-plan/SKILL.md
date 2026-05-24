---
name: spawning-plan
description: "Spawning Plan. Use when user wants to spawn agents, create a team, or coordinate multiple agents. Automatically gathers context, asks team topology questions, outputs clean TEAM PLAN markdown, and gets user approval. 3 steps: context gathering -> questions -> present plan. Requires Claude Code with Agent Teams support."
---

# Spawning Plan

Design the optimal agent team for the task. Performant, precise, minimal.

> **Note:** This skill requires Claude Code with Agent Teams support (TeamCreate, TaskCreate, SendMessage tools).

**Task:** `$ARGUMENTS`

## Step 1: Context Gathering (Silent -- no user interaction)

**A) Read environment:**
- `CLAUDE.md` -- workflow rules, conventions, constraints
- Project manifests -- `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.
- Directory structure -- `src/`, `app/`, `packages/`, test dirs, monorepo indicators

**B) Inventory existing agents:**
- Scan `~/.claude/agents/*.md` -- reuse matching agents instead of creating duplicates

**C) Analyze task complexity:**
- **Work type**: research, implementation, review, debugging, refactoring
- **Scope**: single-layer vs cross-layer
- **Parallelism**: can work split into independent streams?
- **Complexity -> team size**: simple (2 agents), medium (3-4), complex cross-cutting (5-6, max 8)

## Step 2: Ask Team Questions (AskUserQuestion Tool)

Ask 3-5 questions based on Step 1 findings. Not all apply every time -- pick what matters.

1. **Team Composition** -- "For this [work type] on [stack], I'm thinking [N] agents: [role list]. What would you change?"
   Options: Perfect / Add role / Remove role / Different approach

2. **Coordination** -- "How should agents work together?"
   Options: Independent (no messaging) / Team (peer messaging) / Hub-spoke (lead coordinates)

3. **Dependencies** -- "Work order?"
   Options: All parallel / Sequential (A->B->C) / Mixed

4. **Models** -- "Model allocation: opus (research), sonnet (implementation), haiku (scanning). Adjust?"
   Options: As suggested / All opus / All sonnet / Custom

5. **Agent Reuse** *(only if matching agents found in Step 1B)* -- "Found existing `[agent-name]` that handles [capability]. Reuse it?"
   Options: Reuse / Create fresh / Both

## Step 3: Output & Approval

Present clean TEAM PLAN:

```
## TEAM PLAN

Task: [description]
Pattern: [independent | team | hub-spoke]
Work Order: [parallel | sequential | mixed]
Agents: [count]

### Teammates

- Teammate 1: [Name] ([Role])
  Description: [1-2 line expertise and specialization]
  Model: [opus|sonnet|haiku]
  Type: [general-purpose | feature-dev:code-X | reuse ~/.claude/agents/X.md]
  Responsible for: [specific deliverable]
  Depends on: [-- | Teammate N]

- Teammate 2: [Name] ([Role])
  Description: [1-2 line expertise and specialization]
  Model: [opus|sonnet|haiku]
  Type: [general-purpose | feature-dev:code-X]
  Responsible for: [specific deliverable]
  Depends on: [-- | Teammate N]

- ...

### Research (injected into agent prompts)
- [key finding or best practice 1]
- [key finding or best practice 2]
```

### Final Approval (AskUserQuestion Tool)

```
"Launch this team?"
- Deploy & Simplify -- spawn agents, then auto-run /simplify on all changes
- Deploy & Save -- spawn agents and save as reusable skill
- Deploy Once -- spawn agents, one-time
- Adjust -- change something (iterate plan)
- Cancel -- abort
```

**Deploy & Simplify** -> spawn agents, wait for all to complete, then automatically run `/simplify` to review and fix code quality, reuse, and efficiency issues across all agent output. Best for implementation tasks.

**Deploy & Save** -> save team as skill at `~/.claude/skills/<team-name>/SKILL.md` for future use via `/<team-name> [task]`. Saved skill skips planning, bakes in agent definitions, uses `$ARGUMENTS` for task input.

**Adjust** -> ask what to change -> regenerate plan -> ask again. Loop until approved.

**Deploy Once** -> spawn immediately, no save.

**Cancel** -> stop.

### Spawning Execution

Based on chosen pattern:
- **Independent**: parallel Task tool calls, one per agent
- **Team**: TeamCreate -> TaskCreate per agent -> Task tool with `team_name` -> TaskUpdate for dependencies
- **Hub-spoke**: TeamCreate with lead agent (opus) that delegates via SendMessage

For detailed agent prompt structure, see [references/agent-prompts.md](references/agent-prompts.md).
