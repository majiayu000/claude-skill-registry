---
name: oc-tool-dev
description: >-
  Unified entry point for creating or updating OpenCode tools (skills, agents,
  commands) with dependency awareness. Orchestrates the creation of multiple
  related artifacts in a single session. Use when user says "create opencode tool",
  "new opencode tool", "oc-tool-dev", or wants to create/update an OpenCode
  artifact and may need supporting artifacts.
user-invocable: true
disable-model-invocation: false
allowed-tools: AskUserQuestion, Task, Read, Write, Edit, Glob, Grep
---

# OpenCode Tool Dev

You are initiating the unified OpenCode tool development workflow. This process triages what the user needs, detects dependencies between artifacts, builds an execution plan, and delegates to the existing type-specific skills — reusing their interview flows and generation logic.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Every triage question → AskUserQuestion
- Every dependency question → AskUserQuestion
- Confirmation questions → AskUserQuestion

Text output should only be used for summaries, explanations, and presenting information.

### Skill Loader Pattern

This skill delegates to existing `oc-create-*` and `oc-update-*` skills. When executing a tool creation/update:
1. Read the target skill's SKILL.md
2. Follow its instructions as written
3. Pre-fill known answers from triage to skip redundant questions
4. The loaded skill is the single source of truth for its artifact type

---

## Phase 1: Load References

Read the OpenCode platform overview for general context:

1. Read `${CLAUDE_PLUGIN_ROOT}/references/platform-overview.md`

Type-specific guides (skill-guide.md, agent-guide.md, command-guide.md) are loaded later by the delegated skill — do not load them here.

---

## Phase 2: Triage Interview

Gather high-level requirements through 3 questions using `AskUserQuestion`.

**Question 1 — Action:**
- Header: "Action"
- Question: "What would you like to do?"
- Options:
  - "Create new (Recommended)" — Create a new OpenCode tool from scratch
  - "Update existing" — Update an existing tool to match current best practices
- multiSelect: false

**Question 2 — Tool Type:**
- Header: "Tool Type"
- Question: "What type of OpenCode tool?"
- Options:
  - "Skill" — A SKILL.md workflow with phases, tools, and structured prompts
  - "Agent" — A custom agent persona with model, permissions, and system prompt
  - "Command" — A workflow shortcut with $VARIABLE placeholders and optional model override
- multiSelect: false

**Question 3 — Name & Description:**
- Header: "Describe"
- Question: "What should this tool be named and what will it do? Provide a name (kebab-case) and brief purpose."
- Options:
  - "I'll describe it" — Let me provide the name and purpose
- multiSelect: false

### If "Update existing" was selected:

Ask an additional question to locate the existing artifact:

**Question 4 — Locate Artifact:**
- Header: "Locate"
- Question: "How should I find the existing tool?"
- Options:
  - "Search workspace" — Search for OpenCode artifacts in the project
  - "I'll provide the path" — Let me specify the file path directly
- multiSelect: false

If "Search workspace": search using the same discovery patterns as the oc-update-* skills:
- `Glob` for `.opencode/{type}s/*/SKILL.md` (skills) or `.opencode/{type}s/*.md` (agents/commands)
- `Glob` for `.claude/{type}s/*/SKILL.md` or `.claude/{type}s/*.md`
- `Glob` for `.agents/{type}s/*/SKILL.md` or `.agents/{type}s/*.md`
- Present found artifacts using `AskUserQuestion` for selection

Store triage results: **action**, **type**, **name**, **description**, and optionally the **artifact path**.

---

## Phase 3: Dependency Detection Interview

Based on the primary tool type, ask targeted dependency questions using `AskUserQuestion`.

### If creating/updating a Skill:

**Question 1 — Custom Agent:**
- Header: "Agent?"
- Question: "Does this skill need a custom subagent (spawned via the task tool)?"
- Options:
  - "No (Recommended)" — The skill works without a custom agent
  - "Yes" — I need a custom agent for this skill
- multiSelect: false

If "Yes": ask for the agent name and brief purpose via `AskUserQuestion`.

**Question 2 — Supporting Command:**
- Header: "Command?"
- Question: "Does this skill need a supporting command (invoked via /{name} in the TUI)?"
- Options:
  - "No (Recommended)" — No command needed
  - "Yes" — I want a command shortcut for this skill
- multiSelect: false

If "Yes": ask for the command name and brief purpose via `AskUserQuestion`.

### If creating/updating an Agent:

**Question 1 — Parent Skill:**
- Header: "Skill?"
- Question: "Is this agent used by a skill that also needs creating?"
- Options:
  - "No (Recommended)" — Standalone agent
  - "Yes" — I also need a skill that uses this agent
- multiSelect: false

If "Yes": ask for the skill name and purpose via `AskUserQuestion`.

### If creating/updating a Command:

**Question 1 — Agent Routing:**
- Header: "Agent?"
- Question: "Does this command route to an agent that needs creating?"
- Options:
  - "No (Recommended)" — Uses the current agent context
  - "Yes" — I need a custom agent for this command
- multiSelect: false

If "Yes": ask for the agent name and purpose via `AskUserQuestion`.

### For updates with dependencies:

**Question — Related Updates:**
- Header: "Related?"
- Question: "Are there related tools that also need updating?"
- Options:
  - "No" — Just update the selected tool
  - "Yes" — I have related tools to update too
- multiSelect: false

If "Yes": gather the names and types of related tools.

If the user indicates no dependencies in all questions, skip directly to Phase 4.

---

## Phase 4: Plan & Confirm

Build and present the execution plan as a text summary:

```
## Tool Creation Plan

### Primary Tool
- **Type**: {Skill | Agent | Command}
- **Name**: {name}
- **Action**: {Create | Update}
- **Purpose**: {brief description}

### Dependencies (processed first)
1. {Type}: {name} — {Create | Update} — {brief purpose}
2. ...

(If no dependencies: "No dependencies — single artifact workflow.")

### Execution Order
1. {first dependency}
2. {second dependency}
3. {primary tool}
```

Confirm the plan using `AskUserQuestion`:

- Header: "Confirm"
- Question: "Proceed with this plan?"
- Options:
  - "Yes, start" — Begin execution in the order shown
  - "Modify plan" — I want to change something
  - "Cancel" — Abort the workflow
- multiSelect: false

If "Modify plan": ask what to change, update the plan, and re-confirm.
If "Cancel": stop the workflow and inform the user.

---

## Phase 5: Execute (dependency order)

Process each item in the plan, in dependency order (agents before skills, skills before commands that reference them).

### For each item:

**Step 1 — Determine the target skill path:**

| Action | Type | Skill Path |
|--------|------|------------|
| Create | Skill | `${CLAUDE_PLUGIN_ROOT}/skills/oc-create-skill/SKILL.md` |
| Create | Agent | `${CLAUDE_PLUGIN_ROOT}/skills/oc-create-agent/SKILL.md` |
| Create | Command | `${CLAUDE_PLUGIN_ROOT}/skills/oc-create-command/SKILL.md` |
| Update | Skill | `${CLAUDE_PLUGIN_ROOT}/skills/oc-update-skill/SKILL.md` |
| Update | Agent | `${CLAUDE_PLUGIN_ROOT}/skills/oc-update-agent/SKILL.md` |
| Update | Command | `${CLAUDE_PLUGIN_ROOT}/skills/oc-update-command/SKILL.md` |

**Step 2 — Read the target skill's SKILL.md.**

**Step 3 — Follow the loaded skill's instructions with these adjustments:**

- **Skip Phase 1** (Load References) — platform overview already loaded; the delegated skill's type-specific guide will be loaded by its generator/researcher agent.
- **Pre-fill known answers** from triage:
  - Name → skip the "name" interview question
  - Purpose/description → skip the "purpose" interview question
  - For updates: artifact path → skip the "locate" phase
- **Skip already-answered interview questions** — proceed directly to detail questions that were not covered in triage.
- **Complete all remaining phases** — generation, validation, and presentation for creates; research, analysis, presentation, apply, and validation for updates.

**Step 4 — After each artifact completes:**

Present a brief completion notice:
```
✓ {Type} "{name}" — {created | updated} at {path}
```

Then proceed to the next item in the plan.

---

## Phase 6: Summary

After all items are processed, present a final summary:

```
## Tool Creation Summary

### Artifacts
| # | Type | Name | Action | Path | Validation |
|---|------|------|--------|------|------------|
| 1 | {type} | {name} | {Created/Updated} | {path} | {Pass/Warnings} |
| 2 | ... | ... | ... | ... | ... |

### Dependencies
- {name} (agent) ← used by → {name} (skill)
- {name} (agent) ← routed from → {name} (command)

(If no dependencies: "All artifacts are independent.")

### Invocation
- Skill: `/{skill-name}` in the OpenCode TUI
- Agent: `@{agent-name}` in the TUI or `task({ command: "{agent-name}" })`
- Command: `/{command-name}` in the TUI
```

**CRITICAL**: Complete ALL 6 phases before finishing.
