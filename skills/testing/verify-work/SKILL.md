---
name: gsd:verify-work
description: Verify completed work against requirements
version: 1.0.0
triggers: [verify work, check implementation]
tools: [Bash, Glob, Grep, Write]
---

# GSD Verify Work

Verifies completed work using gsd-verifier agent to ensure requirements are met.

## When to Use

- After task completion
- Before checkpoint approval
- Validating implementation correctness

## Process

1. Load phase plan and task details
2. Run gsd-verifier agent
3. Check verification results
4. Report verification status

## Verification Checklist

- Code matches requirements
- Tests pass
- No regressions
- Documentation updated

## Success Criteria

All verification checks pass.

## Related Skills

@skills/gsd/agents/verifier - Agent that verifies implementation
@skills/gsd/commands/execute-phase - Executes phase tasks
