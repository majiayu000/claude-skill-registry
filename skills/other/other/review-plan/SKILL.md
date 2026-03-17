---
name: gsd:review-plan
description: Review and validate phase plans
version: 1.0.0
triggers: [review plan, validate plan]
tools: [Bash, Glob, Grep, Write]
---

# GSD Review Plan

Reviews phase plans using gsd-plan-checker agent for validation.

## When to Use

- Before executing a phase
- After creating a phase plan
- During plan review checkpoints

## Process

1. Load phase plan
2. Run gsd-plan-checker agent
3. Review feedback
4. Revise plan if needed

## Success Criteria

Plan validated and approved for execution.
