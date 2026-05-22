---
name: add_platform
description: "Adds a new AI platform to DeepWork with adapter, templates, and tests. Use when integrating Cursor, Windsurf, or other AI coding tools."
---

# add_platform

**Multi-step workflow**: Adds a new AI platform to DeepWork with adapter, templates, and tests. Use when integrating Cursor, Windsurf, or other AI coding tools.

> **CRITICAL**: Always invoke steps using the Skill tool. Never copy/paste step instructions directly.

A workflow for adding support for a new AI platform (like Cursor, Windsurf, etc.) to DeepWork.

This job guides you through four phases:
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


## Available Steps

1. **research** - Captures CLI configuration and hooks system documentation for the new platform. Use when starting platform integration.
2. **add_capabilities** - Updates job schema and adapters with any new hook events the platform supports. Use after research to extend DeepWork's hook system. (requires: research)
3. **implement** - Creates platform adapter, templates, tests with 100% coverage, and README documentation. Use after adding hook capabilities. (requires: research, add_capabilities)
4. **verify** - Sets up platform directories and verifies deepwork install works correctly. Use after implementation to confirm integration. (requires: implement)

## Execution Instructions

### Step 1: Analyze Intent

Parse any text following `/add_platform` to determine user intent:
- "research" or related terms → start at `add_platform.research`
- "add_capabilities" or related terms → start at `add_platform.add_capabilities`
- "implement" or related terms → start at `add_platform.implement`
- "verify" or related terms → start at `add_platform.verify`

### Step 2: Invoke Starting Step

Use the Skill tool to invoke the identified starting step:
```
Skill tool: add_platform.research
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

- Job definition: `.deepwork/jobs/add_platform/job.yml`