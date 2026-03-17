---
name: plan-mode
description: 战略规划与访谈式工作流
---

# oh-my-ccg Plan Mode

Enter strategic planning mode for complex tasks.

## Activation
Command: `/oh-my-ccg:plan-mode [--consensus] [--review]`

## Modes

### Default
Use planner agent to create an execution plan:
1. Gather context with explore agent
2. Analyze requirements with analyst agent
3. Decompose into tasks with planner agent
4. Output structured plan

### --consensus
Multi-model consensus planning:
1. Planner creates initial plan
2. Codex validates from backend perspective
3. Gemini validates from frontend perspective
4. Critic challenges assumptions
5. Iterate until all three agree (max 3 rounds)
6. Output consensus plan with confidence levels

### --review
Plan critique and improvement:
1. Read existing plan from .oh-my-ccg/plans/
2. Critic agent challenges the plan
3. Codex provides independent critique
4. Present findings with severity ratings
5. User decides: revise, accept, or discard

## Output
Plans saved to `.oh-my-ccg/plans/<timestamp>-plan.md`
