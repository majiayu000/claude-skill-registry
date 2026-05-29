---
name: gsd:update-checkpoint
description: Update checkpoint with new information
version: 1.0.0
triggers: [update checkpoint, modify checkpoint]
tools: [Bash, Glob, Grep, Write]
---

# GSD Update Checkpoint

Updates an existing checkpoint with new information.

## When to Use

- Adding progress to checkpoint
- Updating task status
- Modifying checkpoint details

## Process

1. Load existing checkpoint
2. Update with new information
3. Save checkpoint
4. Notify user of changes

## Success Criteria

Checkpoint updated with new information.
