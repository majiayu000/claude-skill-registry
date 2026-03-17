---
name: workflow-or-agent-decider
description: "Decide between a scripted workflow and an autonomous agent harness, then scaffold the chosen path. Use when scoping new agentic systems or tool integrations."
license: ""
compatibility: ""
metadata:
  short-description: Workflow vs agent decision aid
  audience: agent-architects
  stability: draft
  owner: ""
  tags: [architecture, decision]
allowed-tools: ""
---

# Workflow Or Agent Decider

## Overview
Provide a structured decision and a starter scaffold for either a workflow or agent harness.

## Quick start
1) Fill `templates/decision_matrix.json`.
2) Choose workflow or agent.
3) Use the corresponding scaffold notes in `references/decision-guidance.md`.

## Core Guidance
- Use workflows for stable, deterministic tasks.
- Use agent harnesses for open-ended tasks with tool use.
- Document the choice and the trade-offs.

## Resources
- `references/decision-guidance.md`: Decision heuristics and scaffolds.
- `templates/decision_matrix.json`: Decision matrix template.

## Validation
- Confirm the decision criteria were addressed and recorded.
