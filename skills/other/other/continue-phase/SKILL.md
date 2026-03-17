---
name: gsd:continue-phase
description: Continue phase execution from checkpoint
version: 1.0.0
triggers: [continue phase, resume phase]
tools: [Bash, Glob, Grep, Write]
---

# GSD Continue Phase

Continues phase execution from a checkpoint.

## When to Use

- After checkpoint approval
- Resuming phase execution
- Continuing with next wave

## Process

1. Load checkpoint state
2. Resume from last wave
3. Continue execution
4. Create next checkpoint

## Success Criteria

Phase continues from checkpoint to completion.
