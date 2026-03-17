---
name: gsd:create-checkpoint
description: Create phase checkpoint for user approval
version: 1.0.0
triggers: [checkpoint, create approval point]
tools: [Bash, Glob, Grep, Write]
---

# GSD Create Checkpoint

Creates structured checkpoints for user interaction and approval.

## When to Use

- Between waves
- Before major changes
- At phase boundaries
- When user input is needed

## Process

1. Document current state
2. Summarize completed work
3. List pending tasks
4. Request user feedback
5. Update based on input

## Success Criteria

Checkpoint created with user approval.
