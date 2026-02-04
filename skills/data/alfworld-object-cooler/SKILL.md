---
name: alfworld-object-cooler
description: This skill cools a held object using an appropriate cooling appliance, such as a fridge. It should be triggered when the task requires reducing the temperature of an object (e.g., a hot pot). The skill assumes the agent is holding the object and is near the cooling receptacle; it performs the 'cool' action to achieve the desired state change, preparing the object for subsequent steps like placement or serving.
---
# Skill: Cool Held Object

## Purpose
Use this skill when you are holding an object (e.g., `pot 1`) that needs to be cooled and you are at the location of a valid cooling receptacle (e.g., `fridge 1`). The skill executes the `cool` action to change the object's state.

## Prerequisites
1.  **Object in Hand:** You must already be holding the target object (e.g., `pot 1`).
2.  **At Cooling Receptacle:** You must be at the location of the cooling appliance (e.g., `fridge 1`). Use `go to {recep}` to navigate first if needed.
3.  **Valid Receptacle:** The receptacle must be a valid target for the `cool` action (e.g., fridge, freezer). The environment will validate this.

## Core Action
Execute the `cool` action with the format: `cool {obj} with {recep}`.

## Execution Flow
1.  **Verify State:** Confirm you are holding the object and are at the cooling receptacle's location.
2.  **Execute:** Perform the `cool` action.
3.  **Verify Outcome:** The expected observation is "You cool the {obj} using the {recep}." If the observation is "Nothing happened," the action was invalid—check the prerequisites or try a different receptacle.

## Example from Trajectory
*   **State:** Holding `pot 1`, at `fridge 1`.
*   **Action:** `cool pot 1 with fridge 1`
*   **Result:** Observation: "You cool the pot 1 using the fridge 1."

## Next Steps
After successful cooling, the object is ready for the next task step (e.g., `put {obj} in/on {recep}`).
