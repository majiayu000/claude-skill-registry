---
name: spec_driven_development
description: "Spec-driven development workflow that turns specifications into working implementations through structured planning."
---

# spec_driven_development

**Multi-step workflow**: Spec-driven development workflow that turns specifications into working implementations through structured planning.

> **CRITICAL**: Always invoke steps using the Skill tool. Never copy/paste step instructions directly.


## Available Steps

1. **constitution** - Creates foundational governance principles and development guidelines for the project. Use when starting a new project or establishing standards.
2. **specify** - Defines functional requirements as user stories without technology choices. Use when starting to design a new feature. (requires: constitution)
3. **clarify** - Resolves ambiguities and gaps in the specification through structured questioning. Use after specification to ensure completeness. (requires: specify)
4. **plan** - Creates technical implementation strategy including architecture and technology choices. Use after specification is clarified. (requires: clarify, constitution)
5. **tasks** - Converts the implementation plan into actionable, ordered development tasks. Use after plan is validated. (requires: plan, clarify)
6. **implement** - Generates code and assets by executing the task breakdown. Use when ready to build the feature. (requires: tasks, plan, clarify)

## Execution Instructions

### Step 1: Analyze Intent

Parse any text following `/spec_driven_development` to determine user intent:
- "constitution" or related terms → start at `spec_driven_development.constitution`
- "specify" or related terms → start at `spec_driven_development.specify`
- "clarify" or related terms → start at `spec_driven_development.clarify`
- "plan" or related terms → start at `spec_driven_development.plan`
- "tasks" or related terms → start at `spec_driven_development.tasks`
- "implement" or related terms → start at `spec_driven_development.implement`

### Step 2: Invoke Starting Step

Use the Skill tool to invoke the identified starting step:
```
Skill tool: spec_driven_development.constitution
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

- Job definition: `.deepwork/jobs/spec_driven_development/job.yml`