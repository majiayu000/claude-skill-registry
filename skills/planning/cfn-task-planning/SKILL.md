---
name: cfn-task-planning
description: Classify tasks, initialize structured configs with scope boundaries, decompose complex tasks
version: 1.0.0
tags: planning, classification, scope, decomposition, task-mode
status: production
---

## What it does
Three-phase planning: (1) classify by type/complexity → agent specializations, (2) initialize config with scope boundaries, deliverables, acceptance criteria, (3) decompose large tasks into subtasks within tool budgets.

## When to use (4 triggers)
1. Starting CFN Loop Task Mode → Generate scope config before spawning
2. Analyzing complexity → Select right agents and iteration thresholds
3. Breaking down epics → Sequential subtasks when one agent can't complete
4. Scope contracts → Establish in/out-of-scope before implementation

## When NOT to use (4 anti-patterns)
1. Well-defined and scoped → Go straight to spawning
2. Real-time classification during execution → Planning phase only
3. CLI mode with Redis → CLI stores in Redis, this is for Task Mode configs
4. Simple single-step → Skip for trivial changes

## How to use
Step 1 Classify: `./classify-task.sh "Create REST API..." --format=json`
Step 2 Init: `./init-config.sh --task-id cfn-phase-123 --task-description "..." --mode standard`
Step 3 Decompose: `./decompose-task.sh --task-id ... --description "..." --complexity high`

## Parameters
- **classify**: TASK_DESCRIPTION, --format (json/simple)
- **init**: --task-id, --task-description, --mode (mvp/standard/enterprise)
- **decompose**: --task-id, --description, --tool-budget, --complexity

## Expected output
- **Classify**: `{task_type, complexity, keywords_matched, suggested_agents}`
- **Init**: `.cfn/task-configs/task-{id}.json` with scope, agents, thresholds, acceptance criteria
- **Decompose**: JSON array of subtasks with deliverables, tool_budget, estimated_effort

## Real-world example
"Add JWT auth" → classify backend → init config with deliverables `[src/auth/jwt.ts, tests/]` + acceptance criteria → spawn agents with known scope