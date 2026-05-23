---
name: scienceworld-room-teleporter
description: Teleports the agent to a specified room within the ScienceWorld environment. Use this skill when the target object or location for a task is known to be in a different room, enabling efficient navigation. It takes a target room name as input and outputs a successful teleportation observation.
---
# Instructions
Use the `teleport to LOC` action to move the agent to the specified room.

## Procedure
1.  **Identify Target Room:** Determine the exact name of the destination room from the task context or environment description.
2.  **Execute Teleport:** Use the action `teleport to <room_name>`, where `<room_name>` is the target location (e.g., `workshop`, `kitchen`, `foundry`).
3.  **Verify Success:** The expected output is an observation confirming the teleport, e.g., "You teleport to the workshop."

## Important Notes
- This skill is for navigation only. It does not handle object interaction or task logic within the destination room.
- Ensure the room name matches the environment's naming exactly. Common rooms include: kitchen, foundry, workshop, bathroom, outside, living room, bedroom, greenhouse, art studio, hallway.
- Use this skill proactively to reduce unnecessary exploration steps when the target location is known.
