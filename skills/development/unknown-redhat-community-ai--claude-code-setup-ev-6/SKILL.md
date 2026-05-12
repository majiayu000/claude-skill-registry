---
name: systematic-debugging
version: "1.0"
description: Structured 4-phase debugging process — reproduce, isolate, hypothesize, verify — that finds root causes before attempting fixes. Prevents shotgun debugging and symptom-only patches in Python projects.
---

# Systematic Debugging

Find root causes before fixing. Four phases: reproduce, isolate, hypothesize, verify.

## When to Activate

- When a test fails or an error/exception is reported
- When the user says "debug", "broken", "not working", "failing", "this is wrong"
- When a stack trace or error message appears
- After a fix attempt that didn't resolve the issue

## Process

Read `skills/debugging-process.md` for the 4-phase process with concrete steps, instrumentation patterns, and the 3-strikes rule.

## Behavioral Rules

Read `guidelines.md` for hard limits on fix attempts, hypothesis discipline, and escalation triggers.
