---
name: task-completion-focus
description: Focuses on a specific target object to signal task completion. Execute this skill when you have produced the required final object (like a grown banana) and need to formally complete the assigned task. This handles the 'focus on OBJ' action that typically marks successful task execution in the environment.
---
# Skill: Task Completion Focus

## Purpose
This skill is the final step in a task execution chain. It is triggered **only** when the primary objective of a task has been successfully achieved and the target object is present and observable in the environment. Its sole function is to execute the `focus on OBJ` action on the correct object, which formally signals task completion to the environment.

## When to Use
*   **Prerequisite:** The final, required object (e.g., a grown banana, a crafted item, a repaired device) must be visibly present in the environment.
*   **Trigger:** You have verified the object's presence and your goal is to complete the task.
*   **Do Not Use** for intermediate steps, exploration, or object manipulation.

## Execution Protocol

1.  **Verification:** Before execution, confirm the target object is in the scene. Use `look around` or `examine` if necessary.
2.  **Action Execution:** Perform the `focus on <OBJECT>` action.
3.  **Ambiguity Resolution:** The environment may present multiple valid targets (e.g., bananas on different trees). If an "Ambiguous request" observation is received, you **must** select the correct target by number.
    *   **Selection Rule:** Choose the target that is most directly associated with the main task goal. If multiple are identical, select the first option (e.g., `0`).

## Example from Trajectory
**Scenario:** Task was to "grow a banana". After successful cultivation, multiple bananas are visible.
*   **Observation:** "On the banana tree you see: a banana, a flower."
*   **Correct Action:** `focus on banana on banana tree`
*   **If Ambiguous:** Select option `0` (or the first instance of the target banana).

## Key Principle
This skill is a **low-freedom, terminal action**. Its logic is simple and deterministic. The creative and complex work (growing the plant, crafting the item) belongs to other skills. This skill exists solely to "press the final button."
