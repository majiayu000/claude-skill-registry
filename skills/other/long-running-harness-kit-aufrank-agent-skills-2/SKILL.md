---
name: long-running-harness-kit
description: "Design long-running agent harnesses with resumable checkpoints and initializer/coder handoffs. Use when tasks span multiple sessions or require recovery after interruption."
license: ""
compatibility: ""
metadata:
  short-description: Resumable agent harness patterns
  audience: agent-authors
  stability: draft
  owner: ""
  tags: [harness, resumability, long-running]
allowed-tools: ""
---

# Long Running Harness Kit

## Overview
Define a minimal harness that can pause and resume safely, with clear artifacts that survive context resets. Emphasize initializer + coder roles and persistent run state.

## Quick start
1) Fill `templates/harness_plan.json`.
2) Write `progress.log` and `results.json` outside the skill directory.
3) Use the initializer to set up context; use the coder to make incremental progress.

## Core Guidance
- Use two roles: initializer (setup + context) and coder (incremental tasks).
- Persist state each step (progress, decisions, artifacts).
- Keep tasks small; checkpoint after every meaningful change.
- On resume, read artifacts first, then continue with a narrow next step.

## Resources
- `references/harness-checklist.md`: Resumability and handoff checklist.
- `templates/harness_plan.json`: Plan scaffold for long-running runs.

## Validation
- Confirm artifacts exist and a resume step can continue from the last checkpoint.
