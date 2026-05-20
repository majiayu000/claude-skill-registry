---
name: gsd:workflow:checkpoint
description: Workflow for managing checkpoints
version: 1.0.0
triggers: [checkpoint, approval point]
tools: [Bash, Glob, Grep, Write]
---

# GSD Checkpoint Workflow

Workflow for creating and managing checkpoints.

## When to Use

- Between waves
- Phase boundaries
- User interaction points

## Phases

1. Create checkpoint
2. Document progress
3. Request approval
4. Continue or complete

## Entry Points

- `gsd:create-checkpoint` - Create new checkpoint
- `gsd:update-checkpoint` - Update checkpoint
- `gsd:complete-checkpoint` - Complete checkpoint
- `gsd:continue-phase` - Continue from checkpoint

## Success Criteria

Checkpoint approved and phase continues.
