---
name: agent-expenditure
role: library
description: 'Track per-agent token usage and flag waste in parallel dispatch. Use after running parallel agents to evaluate cost vs value.'
version: 1.9.3
alwaysApply: false
category: resource-optimization
tags:
  - token-waste
  - agent-coordination
  - brooks-law
  - parallel-dispatch
progressive_loading: true
dependencies:
  hub: []
  modules:
    - modules/waste-signals.md
complexity: basic
model_hint: fast
estimated_tokens: 300
---
# Agent Token Waste Monitoring

## When To Use

- After parallel agent dispatch completes
- When evaluating whether to increase agent count
- During retrospectives on agent-heavy workflows
- When plan-before-large-dispatch rule triggers

## When NOT To Use

- Single-agent workflows (no coordination overhead)
- During active agent execution (post-hoc analysis)
- For token budgeting (use token-conservation instead)

## Brooks's Law for Agents

Dispatching more agents does not always help. Coordination overhead
grows with agent count:

| Agent Count | Expected Overhead | Guidance |
|-------------|-------------------|----------|
| 1-3 | Negligible | Dispatch freely |
| 4-5 | 10-15% | Acceptable; plan first |
| 6-8 | 20-30% | Monitor closely |
| 9+ | 30%+ | Likely counterproductive |

Coordination overhead is measured as shared-file conflicts: concurrent
Read/Write operations on the same file by different agents, as a
percentage of total agent runtime.

## Post-Dispatch Review Checklist

After parallel agent runs, evaluate:

1. Did each agent produce unique findings?
2. Was total token expenditure proportional to value?
3. Did any agent duplicate another's work?
4. Would fewer agents have produced the same result?

If 2+ questions answer no, reduce agent count in future dispatches
of the same type.

## Waste Signals

See `modules/waste-signals.md` for the 5 waste signal categories and
detection criteria.

## Cross-References

- `.claude/rules/plan-before-large-dispatch.md` for the 4+ agent
  planning requirement
- `conserve:token-conservation` for session-level token budgeting
- `conjure:agent-teams` for dispatch coordination
