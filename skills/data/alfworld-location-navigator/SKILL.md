---
name: alfworld-location-navigator
description: Moves the agent to a specified receptacle or object location within the Alfworld environment. Use this skill when the agent needs to physically approach a target to inspect or interact with it, such as when checking an object's state or preparing for pickup. The skill takes a target location name as input and executes the 'go to' action, resulting in the agent being positioned at the destination for subsequent operations.
---
# Instructions
Use this skill to navigate to a specific location in the Alfworld environment. The skill will move the agent directly to the target receptacle or object.

## Input
Provide the target location name as a string (e.g., "toiletpaperhanger 1", "toilet 1").

## Process
1.  The skill validates the target location against the current environment observation.
2.  It executes the `go to {target}` action.
3.  It returns the environment's observation after the move.

## Notes
- Ensure the target location is visible in the agent's current observation before calling this skill.
- This skill is for navigation only. Use other skills for object interaction (take, put, etc.).
- If the action fails (e.g., "Nothing happened"), the agent may need to replan its path or verify the target name.
