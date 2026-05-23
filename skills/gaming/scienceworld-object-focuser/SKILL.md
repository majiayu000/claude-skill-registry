---
name: scienceworld-object-focuser
description: This skill selects and focuses on a specific object to signal task intent or prepare it for manipulation. It is triggered after identifying a target object that meets task criteria (e.g., a living thing). The skill uses the 'focus on OBJ' action, taking the object name as input, which is often required before performing actions like moving or using the object in scienceWorld tasks.
---
# Skill: Object Focuser

## Purpose
Use this skill to formally select a target object in the ScienceWorld environment. The `focus on` action signals your intent to the task system and is often a prerequisite for subsequent manipulation steps like `pick up` or `move`.

## When to Use
*   After you have identified an object that matches the task's criteria (e.g., "a living thing", "a conductive material").
*   Before you attempt to pick up, move, or use that object as part of the task sequence.
*   When the task trajectory or environment feedback suggests an object needs to be "focused on" to proceed.

## Core Instruction
1.  **Identify the Target:** From your observation (`look around`, `examine`), determine the exact name of the object you intend to use for the task.
2.  **Execute Focus:** Use the action: `focus on <OBJECT_NAME>`.
    *   Replace `<OBJECT_NAME>` with the precise noun phrase from the environment (e.g., `dove egg`, `copper wire`, `beaker`).
3.  **Proceed:** After receiving a confirmation observation, continue with the next step in your plan (e.g., `pick up <OBJECT_NAME>`, `move <OBJECT_NAME> to ...`).

## Key Considerations
*   **Object Naming:** Use the name exactly as it appears in observations. The system is case-sensitive and expects the full descriptor (e.g., "dove egg", not just "dove" or "egg").
*   **Timing:** Focus is typically performed *after* exploration/identification and *before* the main manipulation action.
*   **Task Logic:** This action is a procedural formality within ScienceWorld. It does not change the object's state but informs the task tracker of your selected target.

For detailed examples and common patterns, see the reference documentation.
