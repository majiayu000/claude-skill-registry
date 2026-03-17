---
name: deepwork_rules
description: "Creates file-change rules that enforce guidelines during AI sessions. Use when automating documentation sync or code review triggers."
---

# deepwork_rules

**Multi-step workflow**: Creates file-change rules that enforce guidelines during AI sessions. Use when automating documentation sync or code review triggers.

> **CRITICAL**: Always invoke steps using the Skill tool. Never copy/paste step instructions directly.

Manages rules that automatically trigger when certain files change during an AI agent session.
Rules help ensure that code changes follow team guidelines, documentation is updated,
and architectural decisions are respected.

IMPORTANT: Rules are evaluated at the "Stop" hook, which fires when an agent finishes its turn.
This includes when sub-agents complete their work. Rules are NOT evaluated immediately after
each file edit - they batch up and run once at the end of the agent's response cycle.
- Command action rules: Execute their command (e.g., `uv sync`) when the agent stops
- Prompt action rules: Display instructions to the agent, blocking until addressed

Rules are stored as individual markdown files with YAML frontmatter in the `.deepwork/rules/`
directory. Each rule file specifies:
- Detection mode: trigger/safety, set (bidirectional), or pair (directional)
- Patterns: Glob patterns for matching files, with optional variable capture
- Action type: prompt (default) to show instructions, or command to run a shell command
- Instructions: Markdown content describing what the agent should do

Example use cases:
- Update installation docs when configuration files change
- Require security review when authentication code is modified
- Ensure API documentation stays in sync with API code
- Enforce source/test file pairing
- Auto-run `uv sync` when pyproject.toml changes (command action)


## Available Steps

1. **define** - Creates a rule file that triggers when specified files change. Use when setting up documentation sync, code review requirements, or automated commands.

## Execution Instructions

### Step 1: Analyze Intent

Parse any text following `/deepwork_rules` to determine user intent:
- "define" or related terms → start at `deepwork_rules.define`

### Step 2: Invoke Starting Step

Use the Skill tool to invoke the identified starting step:
```
Skill tool: deepwork_rules.define
```

### Step 3: Continue Workflow Automatically

After each step completes:
1. Check if there's a next step in the sequence
2. Invoke the next step using the Skill tool
3. Repeat until workflow is complete or user intervenes

### Handling Ambiguous Intent

If user intent is unclear, use AskUserQuestion to clarify:
- Present available steps as numbered options
- Let user select the starting point

## Guardrails

- Do NOT copy/paste step instructions directly; always use the Skill tool to invoke steps
- Do NOT skip steps in the workflow unless the user explicitly requests it
- Do NOT proceed to the next step if the current step's outputs are incomplete
- Do NOT make assumptions about user intent; ask for clarification when ambiguous

## Context Files

- Job definition: `.deepwork/jobs/deepwork_rules/job.yml`