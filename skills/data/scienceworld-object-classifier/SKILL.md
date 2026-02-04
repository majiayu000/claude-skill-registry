---
name: scienceworld-object-classifier
description: Moves a tested or examined object into a designated container (e.g., a specific colored box) based on a determined property. Trigger this skill after completing a test or inspection to fulfill a classification or sorting subtask. It takes the object and target container as inputs and performs the move action.
---
# Instructions

## Purpose
This skill is used to finalize a classification task by moving an object into its designated container. It is triggered **after** a property test or inspection has been completed and a decision has been made.

## Prerequisites
1.  **Object Location:** The object to be classified must be present in the current room's environment (e.g., on the floor, on a table).
2.  **Container Location:** The target container (e.g., yellow box, purple box) must be present in the current room's environment.
3.  **Decision Made:** You must have already determined the object's property (e.g., electrically conductive vs. non-conductive) and know which container corresponds to that property.

## Core Action
Execute the `move` command to transfer the object into the correct container.
*   **Command Format:** `move <OBJECT> to <CONTAINER>`
*   **Example:** `move metal pot to yellow box`

## Workflow
1.  **Confirm Environment:** Use `look around` to verify the object and target container are present.
2.  **Execute Move:** Perform the `move` action.
3.  **Verify:** Optionally, `look at <CONTAINER>` to confirm the object is now inside.

## Important Notes
*   This skill is for the **final sorting action only**. Do not use it to perform the initial test or inspection.
*   Ensure the object is not in your inventory. If it is, drop it first (`drop <OBJECT>`).
*   The skill assumes the classification logic (e.g., interpreting a circuit test) has already been handled by a prior process.
