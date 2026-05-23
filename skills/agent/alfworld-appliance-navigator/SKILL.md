---
name: alfworld-appliance-navigator
description: This skill navigates the agent to a target appliance (like a microwave, stove, or fridge) needed for a task. It should be triggered when the agent has an object that requires processing (heating, cooling, cleaning) and needs to move to the appropriate station. The skill identifies the appliance from the environment and executes the movement action.
---
# Instructions
Use this skill when you are holding an object that needs to be processed (heated, cooled, or cleaned) and you must locate and move to the correct appliance to perform the action.

## Process
1.  **Identify the Target Appliance:** Determine which appliance is required for the task (e.g., microwave for heating, fridge for cooling, sink for cleaning). The required appliance is implied by the action needed (`heat`, `cool`, `clean`).
2.  **Locate the Appliance:** Scan the provided environment observation for the target appliance (e.g., `microwave 1`, `fridge 1`, `sinkbasin 1`).
3.  **Navigate:** Execute the `go to {appliance}` action to move to the identified appliance location.
4.  **Prepare Appliance (if needed):** Upon arrival, check if the appliance requires preparation (e.g., opening a closed microwave or fridge door). If so, perform the necessary action (`open {appliance}`) before proceeding with the object processing.

## Key Principles
*   **Trigger:** The agent is holding an object and the next step in the task is to `heat`, `cool`, or `clean` it.
*   **Core Action:** The primary output of this skill is the navigation command `go to {target_appliance}`.
*   **Prerequisite Check:** Always ensure the appliance is accessible (e.g., open) before attempting to use it for processing.
