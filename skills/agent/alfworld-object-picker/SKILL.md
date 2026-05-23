---
name: alfworld-object-picker
description: Picks up a specified object from a given receptacle. Use this skill when the agent has located a required object and needs to acquire it for later use, such as taking an item from a surface or container. The skill requires the object and source receptacle as inputs, executing a 'take' action to transfer the object into the agent's inventory, enabling further manipulation like placement or usage.
---
# Instructions
Execute the `take` action to acquire the target object from the source receptacle.

## Inputs
- `object`: The identifier of the object to pick up (e.g., "toiletpaper 1").
- `source_receptacle`: The identifier of the receptacle where the object is located (e.g., "toilet 1").

## Process
1.  **Verify Context:** Ensure the agent is at the location of the `source_receptacle`. If not, the agent must navigate there first using a separate movement skill.
2.  **Execute Action:** Perform the action: `take {object} from {source_receptacle}`.
3.  **Handle Feedback:** If the environment indicates "Nothing happened," consult the troubleshooting guide in `references/troubleshooting.md` for potential issues.

## Output
- The specified object is transferred to the agent's inventory.
- The agent receives an observation confirming the successful pickup (e.g., "You pick up the {object} from the {source_receptacle}").
