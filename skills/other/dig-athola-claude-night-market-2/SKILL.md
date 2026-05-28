---
name: dig
description: Refines an active research session by drilling deeper into a subtopic. Use after tome:research to narrow results to a specific channel or angle.
alwaysApply: false
category: research
tags:
  - refinement
  - interactive
  - drill-down
estimated_tokens: 200
model_hint: standard
---
# Dig Deeper

## When To Use

- Drilling into a subtopic after an initial research session
- Narrowing results to a specific channel (e.g. papers only)

## When NOT To Use

- Starting a new research topic (use `/tome:research` first)
- Synthesizing results (use `/tome:synthesize`)

Refine an active research session interactively.

## Workflow

1. Load most recent session via SessionManager
2. Parse the subtopic and optional channel filter
3. Dispatch targeted search (single agent or all channels)
4. Merge new findings into existing session
5. Re-rank and update the saved report
6. Present new findings to user

## Error Cases

- No active session: "Start a session first with
  `/tome:research \"topic\"`"
- Specified channel not in original session: warn and
  suggest available channels
