---
name: gsd:integrate
description: Integrate changes and verify system-wide compatibility
version: 1.0.0
triggers: [integrate, merge changes]
tools: [Bash, Glob, Grep, Write]
---

# GSD Integrate

Integrates changes using gsd-integration-checker agent.

## When to Use

- Before checkpoint approval
- After completing integration points
- When verifying cross-component compatibility

## Process

1. Load integration requirements
2. Run gsd-integration-checker agent
3. Verify all integration points
4. Report integration status

## Success Criteria

All integrations verified and working.
