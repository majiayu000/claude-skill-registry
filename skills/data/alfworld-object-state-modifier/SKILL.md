---
name: alfworld-object-state-modifier
description: This skill uses an appliance to change the state of an object (e.g., cooling, heating, cleaning). It should be triggered when the task requires altering an object's temperature or cleanliness using a specific device (like cooling with a fridge or heating with a microwave). The skill requires the object, the target state, and the appliance as inputs, and executes the corresponding modifier action (e.g., 'cool X with Y').
---
# Instructions

## When to Use
Use this skill when the task requires you to **change the state of an object** using a specific household appliance. The primary actions are:
- **Cool** an object (e.g., with a fridge).
- **Heat** an object (e.g., with a microwave or stove).
- **Clean** an object (e.g., with a sink).

## Core Procedure
1.  **Locate & Acquire Object:** First, navigate to and pick up the target object.
2.  **Navigate to Appliance:** Go to the appliance required for the state change (e.g., `fridge 1`, `microwave 1`).
3.  **Prepare Appliance (if needed):** Some appliances require preparation (e.g., opening a fridge or microwave door). Perform the necessary `open` or `toggle` action.
4.  **Execute State Change:** Perform the core modifier action: `cool {obj} with {appliance}`, `heat {obj} with {appliance}`, or `clean {obj} with {appliance}`.
5.  **Complete Task:** After the state is changed, proceed with the next task step (e.g., placing the object elsewhere).

## Key Considerations
- **Invalid Actions:** If the environment responds with "Nothing happened," your action was invalid. Consult the `references/appliance_interaction_guide.md` for troubleshooting.
- **Appliance State:** Always check if an appliance is open/closed/on/off before attempting the modifier action.
- **Object Holding:** You must be holding the target object (`{obj}`) before executing the state change action.

## Inputs Required
- `{obj}`: The specific object identifier (e.g., `tomato 1`).
- `{target_state}`: The desired state change (`cool`, `heat`, or `clean`).
- `{appliance}`: The specific appliance identifier (e.g., `fridge 1`).

## Output Action
The skill's final output is a single, formatted action string: `{target_state} {obj} with {appliance}`.
