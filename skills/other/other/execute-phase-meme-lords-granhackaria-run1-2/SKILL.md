---
name: gsd:workflow:execute-phase
description: Workflow for executing a project phase
version: 1.0.0
triggers: [execute phase, run phase]
tools: [Bash, Glob, Grep, Write]
---

# GSD Execute Phase Workflow

Workflow for executing a planned project phase with verification.

## When to Use

- Executing a planned phase
- Running wave-based development

## Phases

1. Plan phase details
2. Review plan
3. Execute waves
4. Verify work
5. Create checkpoint
6. Request approval

## Entry Points

- `gsd:plan-phase` - Create phase plan
- `gsd:execute-phase` - Execute phase
- `gsd:verify-work` - Verify implementation
- `gsd:create-checkpoint` - Create checkpoint

## Success Criteria

Phase completed with verification and checkpoint approved.
