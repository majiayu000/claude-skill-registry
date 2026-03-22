---
name: review
description: Run the qa agent to validate the current state of barista.p8. Use when the user asks to review, validate, or check the game code.
argument-hint: [description of what to review]
allowed-tools: Agent, Read, Glob, Grep, Bash
---

Run a QA review on: $ARGUMENTS

If no target is specified, review the full `barista.p8` cart.

Invoke the qa agent directly using `subagent_type: "qa"` with a review prompt describing what to check.

The qa agent will validate:
- Correctness — physics, state machine, scoring logic
- Consistency — code conventions, entity type usage
- Completeness — variable initialization, HUD accuracy
- Token budget — identify waste or savings opportunities

Return the full verdict (PASS / FAIL / PASS WITH NOTES) with line numbers for any issues found.
