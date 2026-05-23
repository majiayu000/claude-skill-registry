---
name: alfworld-object-storer
description: This skill places an object into a selected storage receptacle after confirming its suitability. It should be triggered when the agent has identified an appropriate storage location and is ready to complete the storage task. The skill takes the object and target receptacle as inputs and results in the object being stored.
---
# Skill: Object Storer

## Purpose
This skill orchestrates the final step of storing a clean object into a designated receptacle within a household environment. It is triggered after the agent has:
1. Located the target object.
2. Cleaned the object if required.
3. Identified and validated a suitable storage location.

## Core Logic
The skill performs a final suitability check and executes the storage action. The core decision is:
- **If the receptacle is open and empty (or appropriately designated)**, proceed with storage.
- **If the receptacle is closed**, open it first, then store the object.
- **If the receptacle is unsuitable** (e.g., already contains unrelated items), the agent should abort this skill and search for an alternative location.

## Inputs & Execution
- **Primary Inputs:** `{object_name}`, `{target_receptacle}`
- **Prerequisite State:** The agent must be holding the clean `{object_name}` and be at the location of the `{target_receptacle}`.
- **Action:** Execute the `put {object_name} in/on {target_receptacle}` command.

## Example from Trajectory
**Scenario:** Storing a clean knife.
1. **Trigger Condition:** Agent is holding `knife 1` (cleaned) and has determined `drawer 1` is a suitable, empty storage location.
2. **Skill Execution:**
   - Agent is at `drawer 1`.
   - Observation: `On the drawer 1, you see nothing.`
   - **Action:** `put knife 1 in/on drawer 1`

## Error Handling
- If the environment responds with "Nothing happened," the action was invalid. Consult the `receptacle_suitability_guide.md` reference and restart the search process.
- Do not use this skill if the receptacle contains items that conflict with the object's storage norms (e.g., putting a knife in a drawer full of spoons).
