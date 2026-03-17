---
name: refactor-roadmap
description: Create a staged refactor plan for a module. Use when a mid-level developer needs a safe refactor path.
---

# Refactor Roadmap

## Purpose
Create a staged refactor plan for a module.

## Inputs to request
- Current pain points and target state.
- Test coverage and risk tolerance.
- Dependencies and release constraints.

## Workflow
1. Define current pain points and desired end state.
2. Break into small, testable steps.
3. Add guardrails: tests, feature flags, or metrics.

## Output
- Refactor sequence with checkpoints.

## Quality bar
- Ensure each step is reversible.
- Tie steps to tests or metrics.
