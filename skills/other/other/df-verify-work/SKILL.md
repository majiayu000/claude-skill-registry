---
name: df:verify-work
description: |
  Validate built features through conversational UAT.
  Use when the user wants to test, verify, or validate what was built in an objective.
  Triggers on: "test what we built", "verify objective", "check the work", "UAT", "does it work?", "let's test", "validate the implementation"
argument-hint: "[objective number, e.g., '4']"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Edit
  - Write
  - Task
---
<objective>
Validate built features through conversational testing with persistent state.

Purpose: Confirm what Claude built actually works from user's perspective. One test at a time, plain text responses, no interrogation. When issues are found, automatically diagnose, plan fixes, and prepare for execution.

Output: {phase_num}-UAT.md tracking all test results. If issues found: diagnosed gaps, verified fix plans ready for /df:execute-objective
</objective>

<execution_context>
@~/.claude/devflow/workflows/verify-work.md
@~/.claude/devflow/templates/UAT.md
</execution_context>

<context>
Objective: $ARGUMENTS (optional)
- If provided: Test specific objective (e.g., "4")
- If not provided: Check for active sessions or prompt for objective

@.planning/STATE.md
@.planning/ROADMAP.md
</context>

<process>
Execute the verify-work workflow from @~/.claude/devflow/workflows/verify-work.md end-to-end.
Preserve all workflow gates (session management, test presentation, diagnosis, fix planning, routing).
</process>
