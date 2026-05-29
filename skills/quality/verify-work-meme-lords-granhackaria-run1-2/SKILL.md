---
name: gsd:workflow:verify-work
description: Workflow for verifying completed work
version: 1.0.0
triggers: [verify work, check work]
tools: [Bash, Glob, Grep, Write]
---

# GSD Verify Work Workflow

Workflow for verifying completed work.

## When to Use

- After task completion
- Before checkpoint
- Quality assurance

## Phases

1. Load requirements
2. Run verification
3. Check quality
4. Report results

## Success Criteria

Work verified with all checks passing.
