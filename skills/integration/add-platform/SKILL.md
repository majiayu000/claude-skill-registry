---
name: add_platform
description: "Adds a new AI platform to DeepWork with adapter, templates, and tests. Use when integrating Cursor, Windsurf, or other AI coding tools."
---

# add_platform

Adds a new AI platform to DeepWork with adapter, templates, and tests. Use when integrating Cursor, Windsurf, or other AI coding tools.

> **CRITICAL**: Always invoke steps using the Skill tool. Never copy/paste step instructions directly.

A workflow for adding support for a new AI platform (like Cursor, Windsurf, etc.) to DeepWork.

The **integrate** workflow guides you through four phases:
1. **Research**: Capture the platform's CLI configuration and hooks system documentation
2. **Add Capabilities**: Update the job schema and adapters with any new hook events
3. **Implement**: Create the platform adapter, templates, tests (100% coverage), and README updates
4. **Verify**: Ensure installation works correctly and produces expected files

The workflow ensures consistency across all supported platforms and maintains
comprehensive test coverage for new functionality.

**Important Notes**:
- Only hooks available on slash command definitions should be captured
- Each existing adapter must be updated when new hooks are added (typically with null values)
- Tests must achieve 100% coverage for any new functionality
- Installation verification confirms the platform integrates correctly with existing jobs


## Workflows

### integrate

Full workflow to integrate a new AI platform into DeepWork

**Steps in order**:
1. **research** - Captures CLI configuration and hooks system documentation for the new platform. Use when starting platform integration.
2. **add_capabilities** - Updates job schema and adapters with any new hook events the platform supports. Use after research to extend DeepWork's hook system.
3. **implement** - Creates platform adapter, templates, tests with 100% coverage, and README documentation. Use after adding hook capabilities.
4. **verify** - Sets up platform directories and verifies deepwork install works correctly. Use after implementation to confirm integration.

**Start workflow**: `/add_platform.research`


## Execution Instructions

### Step 1: Analyze Intent

Parse any text following `/add_platform` to determine user intent:
- "integrate" or related terms → start integrate workflow at `add_platform.research`

### Step 2: Invoke Starting Step

Use the Skill tool to invoke the identified starting step:
```
Skill tool: add_platform.research
```

### Step 3: Continue Workflow Automatically

After each step completes:
1. Check if there's a next step in the workflow sequence
2. Invoke the next step using the Skill tool
3. Repeat until workflow is complete or user intervenes

**Note**: Standalone skills do not auto-continue to other steps.

### Handling Ambiguous Intent

If user intent is unclear, use AskUserQuestion to clarify:
- Present available workflows and standalone skills as options
- Let user select the starting point

## Guardrails

- Do NOT copy/paste step instructions directly; always use the Skill tool to invoke steps
- Do NOT skip steps in a workflow unless the user explicitly requests it
- Do NOT proceed to the next step if the current step's outputs are incomplete
- Do NOT make assumptions about user intent; ask for clarification when ambiguous

## Context Files

- Job definition: `.deepwork/jobs/add_platform/job.yml`