---
name: gsd:complete-checkpoint
description: Complete checkpoint and finalize phase
version: 1.0.0
triggers: [complete checkpoint, finish checkpoint]
tools: [Bash, Glob, Grep, Write]
---

# GSD Complete Checkpoint

Completes a checkpoint and finalizes phase progress.

## When to Use

- When phase is complete
- At final checkpoint
- Before moving to next phase

## Process

1. Load checkpoint status
2. Verify all tasks complete
3. Finalize checkpoint documentation
4. Prepare for next phase

## Success Criteria

Checkpoint completed and phase finalized.
