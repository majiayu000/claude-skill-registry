---
name: fan-out
description: "Parallel agent orchestration for OST exploration. Fan-out multiple solution explorations, fan-in results to compare and select winners."
---

# Fan-Out / Fan-In Orchestration

## When to Use
- OST has 2+ solutions for the same opportunity that need parallel exploration
- Independent delivery work items that can be parallelized
- Multiple research streams needed simultaneously

## Workflow

### 1. Prepare (Lead Agent)
- Read canvas/opportunities.yml
- Identify solutions needing parallel work
- For each: identify riskiest assumption and design test

### 2. Fan-Out (Spawn Workers)
For each solution:
- Spawn subagent or Agent Team member
- Provide: clear task, read-only canvas context, worktree isolation, time bound
- Each worker runs independently

### 3. Fan-In (Collect Results)
- Collect all worker results
- Update ICE scores in canvas
- Run `/bias-check` on combined findings
- Select winner(s) based on evidence
- Log decision in decision-log.md

## Rules
- Workers NEVER write to canvas (lead agent does)
- Workers NEVER progress diamonds
- Lead agent ALWAYS runs bias check on combined results
- Minimum 2 workers for meaningful comparison

See `.claude/orchestration/fan-out-fan-in.md` for full details.
