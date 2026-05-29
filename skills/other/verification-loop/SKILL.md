---
name: verification-loop
version: "1.0"
description: Unified verification engine for Python data science projects. Covers environment checks, type checking, linting, tests, security scans, code review with DS anti-patterns, and notebook checks. Commands (/verify, /quality-gate) invoke different subsets of this skill.
---

# Verification Loop

The single source of truth for all code checks. Commands invoke specific phases:
- `/verify` → Phases 1-4 (does my code work?)
- `/quality-gate` → Phases 1-4 + Phase 6 (safe to push?)

Phase 5 (code review) runs when the user asks for a code review directly.

## When to Activate

- After completing a feature or significant code change
- Before creating an MR/PR
- After refactoring
- When the user says "verify", "review", "check", or "quality gate"

## Phases

Read `skills/phases.md` for all 7 phases with exact commands, the code review checklist, and the output format.

## Behavioral Rules

Read `guidelines.md` for verdict rules, coverage targets, and escalation criteria.
