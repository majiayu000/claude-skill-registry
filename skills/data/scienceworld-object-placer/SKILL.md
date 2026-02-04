---
name: scienceworld-object-placer
description: Moves a specified object from the environment or inventory into a target container based on a classification decision. It should be triggered when a task requires sorting or storing an object in a specific location after an assessment.
---
# Instructions

This skill orchestrates the final step of a conditional workflow: moving an object to a designated container after its properties have been assessed.

## When to Use
Use this skill when the primary task involves:
1.  **Classifying an object** (e.g., testing for conductivity, checking material type, verifying a state).
2.  **Conditionally placing the object** based on the classification result (e.g., "if property X, place in Container A; else, place in Container B").

## Core Action
The skill's primary action is `move OBJ to OBJ`. Ensure the target object is identified and the correct destination container is selected based on the prior assessment.

## Prerequisites
Before executing this skill, the following must be true:
*   The target object has been located and is accessible (in the environment or inventory).
*   The classification test or assessment has been completed.
*   The result of the assessment is known and the corresponding destination container has been identified.

## Execution Flow
1.  **Confirm Context:** Verify the assessment result and the identity of the destination container (e.g., "blue box" for conductive, "orange box" for non-conductive).
2.  **Acquire Object:** If the target object is not already in your inventory, use `pick up OBJ` to acquire it.
3.  **Execute Placement:** Use the `move OBJ to OBJ` action to transfer the object to the correct container.
4.  **Verify:** Optionally, look at the container to confirm the object was placed inside.

## Example from Trajectory
*   **Task:** "Determine if metal pot is electrically conductive. If conductive, place it in the blue box. If nonconductive, place it in the orange box."
*   **Assessment:** A circuit test confirmed the metal pot was conductive.
*   **Skill Execution:** `move metal pot to blue box`
