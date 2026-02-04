---
name: scienceworld-threshold-evaluator
description: This skill compares a measured numerical value (e.g., temperature, weight) against a predefined threshold to determine a binary outcome. It should be triggered immediately after obtaining a measurement that has an associated conditional instruction. The skill evaluates if the value is above/below the threshold to guide the next action.
---
# Threshold Evaluation Skill

## When to Use
Trigger this skill **immediately** after you obtain a numerical measurement (e.g., temperature reading) and you have a conditional instruction that depends on that measurement (e.g., "If value > X, do A; if value < X, do B").

## Core Logic
1.  **Extract the Measurement:** Identify the numerical value from the observation (e.g., "the thermometer measures a temperature of 56 degrees celsius" -> `56`).
2.  **Identify the Threshold & Condition:** Parse the user's instruction to find the threshold value and the comparison operator (e.g., "above 50.0 degrees" -> `threshold=50.0`, `operator=">"`).
3.  **Evaluate:** Perform the comparison (`measured_value > threshold` or `measured_value < threshold`).
4.  **Execute Branch:** Based on the boolean result, perform the corresponding action specified in the instruction.

## Key Principles
*   **Immediate Execution:** Do not perform any other actions between obtaining the measurement and running this evaluation.
*   **Precision:** Use the exact numerical value from the observation. Do not estimate or round unless specified.
*   **Binary Decision:** The outcome is strictly one of two paths. If the measurement equals the threshold, re-examine the instruction for guidance (e.g., "above" typically means `>`, not `>=`).

## Common Pitfalls (from Trajectory)
*   **Incorrect Branching:** Do not execute the branch for the opposite condition (e.g., focusing on the blue box when the value is above the threshold).
*   **Premature Evaluation:** Ensure the measurement is complete and valid before evaluating.
*   **Action Confusion:** The final action (e.g., `focus on OBJ`) must target the correct object specified for the satisfied condition.

For detailed examples and the evaluation script, see the reference documentation.
