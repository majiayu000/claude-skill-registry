---
name: agent-workflow-playbook
description: "Guide plan → instrument → execute → validate with explicit checkpoints and questions. Use for ambiguous tasks or when enforcing a consistent agent workflow."
license: ""
compatibility: ""
metadata:
  short-description: Standardized agent workflow guidance
  audience: agents
  stability: draft
  owner: ""
  tags: [workflow, planning, process]
allowed-tools: ""
---

# Agent Workflow Playbook

## Overview
Apply a consistent workflow to reduce drift in agent runs, with explicit questions and checkpoints between phases.

## Quick start
1) Fill `templates/workflow_plan.json`.
2) Ask clarifying questions before execution.
3) Capture results and validation in `results.json`.

## Core Guidance
- Plan: capture goals, constraints, success criteria.
- Instrument: define artifacts and logs before execution.
- Execute: do the minimal next step.
- Validate: verify outputs and decide next action.

## Resources
- `references/workflow-checklist.md`: Phase prompts and questions.
- `templates/workflow_plan.json`: Plan scaffold for the workflow.

## Validation
- Confirm each phase is completed and documented.
