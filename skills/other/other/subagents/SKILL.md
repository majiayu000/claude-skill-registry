---
name: subagents
description: Execution-layer skill for spawning subagents via runAgent
---

## Commands

- runAgent

## Constraints

- Subagents must run with explicit, limited tool permissions.
- Governance-layer routing decisions happen before runAgent is called.

## Notes

- Governance decides which agent id to call; this skill is a thin wrapper around runAgent.
