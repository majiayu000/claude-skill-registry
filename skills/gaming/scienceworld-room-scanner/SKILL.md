---
name: scienceworld-room-scanner
description: This skill performs a 'look around' action to scan and describe the current room's contents, including visible objects, containers, and doors. It should be triggered upon entering a new room or when the agent needs to locate specific items or assess the environment state. The skill outputs a detailed room description, which is essential for inventory discovery and situational awareness.
---
# Skill: Room Scanner

## Purpose
Execute a `look around` action to obtain a comprehensive description of the current room in the ScienceWorld environment. This description is the foundational step for any task requiring item location, environmental assessment, or navigation planning.

## Core Instruction
When this skill is invoked, the agent must perform the **`look around`** action.

## Trigger Conditions
Invoke this skill when:
1.  You first enter a new room via `teleport` or other movement.
2.  You need to locate a specific object or container mentioned in your task.
3.  The state of the room may have changed (e.g., after an interaction).
4.  You are formulating a plan and require an inventory of available resources.

## Output Processing
The observation from `look around` will contain:
*   **Room Name:** The identifier of your current location.
*   **Visible Objects & Agents:** A list of all entities in the room.
*   **Container Contents:** For open containers, a nested list of items inside (e.g., `a bowl (containing a red apple, a banana)`).
*   **Device States:** The status of interactive objects (e.g., `a stove, which is turned off`).
*   **Connections:** All accessible doors and their destination rooms.

**You must parse this output carefully.** Use it to update your mental model of the environment before proceeding with other actions like `pick up`, `examine`, or `use`.

## Integration Notes
*   This is a low-level, atomic skill. It should often be the first action in a sequence.
*   The observation it generates is critical context for subsequent decision-making. Refer back to it.
*   Do not overuse it. Once you have a recent description of a room, rely on that knowledge until you have reason to believe the state has changed.
