---
name: deepwork_jobs
description: "Creates and manages multi-step AI workflows. Use when defining, implementing, or improving DeepWork jobs."
---

# deepwork_jobs

**Multi-step workflow**: Creates and manages multi-step AI workflows. Use when defining, implementing, or improving DeepWork jobs.

> **CRITICAL**: Always invoke steps using the Skill tool. Never copy/paste step instructions directly.

Core commands for managing DeepWork jobs. These commands help you define new multi-step
workflows and learn from running them.

The `define` command guides you through an interactive process to create a new job by
asking structured questions about your workflow, understanding each step's inputs and outputs,
and generating all necessary files.

The `learn` command reflects on conversations where DeepWork jobs were run, identifies
confusion or inefficiencies, and improves job instructions. It also captures bespoke
learnings specific to the current run into AGENTS.md files in the working folder.


## Available Steps

1. **define** - Creates a job.yml specification by gathering workflow requirements through structured questions. Use when starting a new multi-step workflow.
2. **review_job_spec** - Reviews job.yml against quality criteria using a sub-agent for unbiased validation. Use after defining a job specification. (requires: define)
3. **implement** - Generates step instruction files and syncs slash commands from the job.yml specification. Use after job spec review passes. (requires: review_job_spec)
4. **learn** - Analyzes conversation history to improve job instructions and capture learnings. Use after running a job to refine it.

## Execution Instructions

### Step 1: Analyze Intent

Parse any text following `/deepwork_jobs` to determine user intent:
- "define" or related terms → start at `deepwork_jobs.define`
- "review_job_spec" or related terms → start at `deepwork_jobs.review_job_spec`
- "implement" or related terms → start at `deepwork_jobs.implement`
- "learn" or related terms → start at `deepwork_jobs.learn`

### Step 2: Invoke Starting Step

Use the Skill tool to invoke the identified starting step:
```
Skill tool: deepwork_jobs.define
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

- Job definition: `.deepwork/jobs/deepwork_jobs/job.yml`