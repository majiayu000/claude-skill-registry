---
name: alfworld-object-disposer
description: This skill disposes of an object by placing it into a disposal receptacle like a garbage can. It should be triggered when the task requires discarding an object (e.g., 'put it in garbagecan') and the agent is at the disposal location with the object in hand. The skill executes the 'put' action to place the object in/on the target receptacle, completing the disposal subtask.
---
# Skill: Object Disposer

## Trigger Condition
Activate this skill when:
1. The task goal explicitly requires disposing of an object (e.g., "put it in garbagecan", "throw away the X").
2. The agent is holding the target object.
3. The agent is at the location of the disposal receptacle (e.g., garbagecan).

## Execution
1. **Verify Prerequisites**: Confirm the object is in hand and the disposal receptacle is present at your location.
2. **Execute Disposal**: Perform the `put` action with the object and receptacle.
3. **Completion**: The skill is complete when the object has been successfully placed into/onto the disposal receptacle.

## Notes
- This skill handles only the final disposal action. Object acquisition and navigation to the disposal location are separate skills.
- If the disposal fails (e.g., "Nothing happened"), re-evaluate the object and receptacle identifiers or check if the receptacle can accept the object.
