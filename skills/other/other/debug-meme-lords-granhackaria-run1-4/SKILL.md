---
name: gsd:debug
description: Debug issues using systematic investigation
version: 1.0.0
triggers: [debug, troubleshoot, fix issue]
tools: [Bash, Glob, Grep, Write]
---

# GSD Debug

Systematically debugs issues using gsd-debugger agent with structured investigation.

## When to Use

- When bugs are encountered during execution
- When verification fails
- When unexpected behavior occurs

## Process

1. Describe the problem
2. Run gsd-debugger agent
3. Follow investigation steps
4. Apply fix
5. Verify fix works

## Investigation Techniques

- Read error messages
- Check logs
- Review recent changes
- Trace execution flow
- Write minimal reproduction

## Success Criteria

Issue identified and fixed with verification.

## Related Skills

@skills/gsd/agents/debugger - Agent that investigates issues
@skills/gsd/commands/verify-work - Verifies fixes
