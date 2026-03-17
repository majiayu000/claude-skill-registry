---
name: orchestrate
description: Run the full product→plan→validate→implement→verify workflow by delegating to subagents.
---

# Orchestrate

Use this skill to run a complete workflow in a new project or major feature.

## When to use

- You have a product mission + technical docs.
- The work spans multiple steps or files.

## Instructions

1. **Discover** docs and summarize requirements.
2. **Plan** tasks with clear acceptance criteria and file scope.
3. **Validate** the plan with security + architecture reviewers in parallel.
4. **Implement** tasks via TDD (tests first, then code).
5. **Verify** with a hard gate and evidence (tests/run logs).

## Delegation (parallel when independent)

- Planner: `/planner`
- Security validation: `/validator-security`
- Architecture validation: `/validator-architecture`
- Tests: `/test-writer`
- Implementation: `/implementer`
- Final gate: `/verifier`
