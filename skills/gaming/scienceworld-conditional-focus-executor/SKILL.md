---
name: scienceworld-conditional-focus-executor
description: Executes a 'focus' action on a specific object based on the outcome of a prior conditional evaluation. It should be triggered when task instructions specify focusing on different objects (e.g., different colored boxes) depending on a measurement result. The skill takes the conditional outcome as input and performs the corresponding focus action.
---
# Conditional Focus Executor

## Purpose
This skill automates the final step in a conditional measurement task within the ScienceWorld environment. After obtaining a measurement result (e.g., a temperature reading), you must focus on a specific object (e.g., a colored box) based on whether the result meets a defined threshold.

## When to Use
Use this skill **only** when:
1. You have completed a measurement (e.g., temperature, pH, mass).
2. The task instructions explicitly state a conditional rule (e.g., "If result > X, focus on A; if result < X, focus on B").
3. You have already determined the conditional outcome (True/False or the specific branch).

## Input Required
Before executing, you **must** have determined the correct conditional branch. The skill requires this as a clear decision.

**Required Input Format:**
