---
name: code-review
description: Systematic multi-perspective code review with consistent quality gates.
last_updated: 2025-12-20
---

# Code Review Skill

## Overview

A systematic approach to code review that moves beyond "it looks good" to rigorous quality verification. This skill provides specific checklists and procedures for different review types.

## When To Use

- **Self-Review**: Before submitting a PR or finishing `/work`
- **Peer Review**: When reviewing another agent's or human's code (`/resolve_pr`)
- **Plan Review**: When validating an implementation plan (`/plan_review`)

## Instrumentation

```bash
# Log usage when using this skill
Call MCP `call_tool_logger_manager` { action: "logSkill", name: "code-review", outcome: "manual" }
```

## What do you want to do?

1. **Security Review** (Auth, RLS, Input) → `workflows/security-pass.md`
2. **Performance Review** (Database, Re-renders) → `workflows/performance-pass.md`
3. **Architecture Review** (State, Data Flow) → `workflows/architecture-pass.md`
4. **General Quality Check** → `checklists/pre-merge.md`

## Key Principles

- **Review in Passes**: Don't check everything at once. Do a security pass, then a performance pass, etc.
- **Reference Patterns**: Always check against `docs/solutions/patterns/critical-patterns.md`.
- **Verify, Don't Guess**: If you see a potential issue, verify it with a quick test or script.

## Scientific Review Principles
Adapted from formal peer review standards to improve code review rigor:
1. **Algorithmic Soundness Check**: Avoid circular logic where state values mask deeper architectural flaws.
2. **Control Variables Isolation**: Ensure side-effects are heavily isolated and easily testable (simulating scientific controls).
3. **Absolute Reproducibility**: If a bug or edge-case is discussed in review, verify that the system has enough telemetry/logging to perfectly reproduce it.
4. **Constructive Tone Constraint**: Frame criticism objectively as an opportunity for improvement. Avoid dismissing implementations without offering actionable, pattern-compliant alternatives.
