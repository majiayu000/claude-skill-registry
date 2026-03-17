---
name: test-skill
description: Test skills through RED/GREEN/REFACTOR TDD phases
usage: /test-skill [skill-path] [--phase red|green|refactor]
extends: "superpowers:test-driven-development"
---

# Test Skill

Runs skill validation via superpowers:test-driven-development while keeping the familiar `/test-skill` interface.

## When To Use

Use this command when you need to:
- Testing a skill through RED/GREEN/REFACTOR phases
- Validating skill behavior before deployment
- Running TDD checkpoints on skill development

## When NOT To Use

Avoid this command if:
- Evaluating skill quality metrics - use /skills-eval instead
- Creating new skills - use /create-skill instead
- Hardening against rationalization - use /bulletproof-skill

## How It Works

- Executes RED/GREEN/REFACTOR phases through `superpowers:test-driven-development`.
- Accepts the same arguments as the previous `/test-skill` command.
- Adds superpowers' reporting and enforcement of TDD checkpoints.

## Notes

- Behavior is backward compatible with prior `/test-skill` usage.
- Use `--phase` to target a single stage or run the full cycle without flags.
