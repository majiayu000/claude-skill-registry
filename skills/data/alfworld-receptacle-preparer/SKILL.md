---
name: alfworld-receptacle-preparer
description: This skill verifies and prepares a target receptacle for receiving an object. It is triggered before placing an item into a receptacle (e.g., a garbage can) to ensure the receptacle is accessible and suitable. The skill involves navigating to the receptacle, observing its state (e.g., open/closed, occupied), and performing any necessary preparatory actions like opening it, resulting in a ready-to-use target location.
---
# Instructions

**Trigger:** This skill is invoked when the agent's goal requires placing an object into a target receptacle (e.g., "put X in/on Y").

## Core Procedure
1.  **Navigate:** Use `go to {target_receptacle}` to move to the target receptacle's location.
2.  **Observe:** Upon arrival, carefully read the environment's observation. It will describe the receptacle's state and any contents.
3.  **Analyze & Prepare:** Based on the observation, determine if the receptacle is ready.
    *   **Ready State:** The receptacle is described as present and accessible (e.g., "On the garbagecan 1, you see a cd 1."). No further action is needed. Proceed to place the object.
    *   **Blocked/Closed State:** If the receptacle is closed, latched, or obstructed, use the appropriate action (`open {recep}`, `toggle {obj} {recep}`) to prepare it.
    *   **Invalid Target:** If the observation indicates the receptacle does not exist or cannot be interacted with ("Nothing happened"), you must abort this skill and re-plan your task strategy.
4.  **Confirm:** After any preparatory action, observe the environment's feedback to confirm the receptacle is now ready.

## Key Principles
*   **Efficiency:** This skill is a preparatory step. Do not spend turns searching for the object to be placed here. That is a separate "search" skill.
*   **Context:** The observation text is your only source of truth about the receptacle's state. Interpret it literally.
*   **Idempotency:** If the receptacle is already ready, this skill completes immediately with no action required beyond observation.

## Example from Trajectory
**Goal Context:** "find two pen and put them in garbagecan."
**Skill Execution:**
1.  Thought: "I'll check the garbage can first to ensure it's open and ready to receive items."
2.  Action: `go to garbagecan 1`
3.  Observation: "On the garbagecan 1, you see a cd 1."
4.  Analysis: The garbage can is present and accessible (a CD inside does not block new items). It is **ready**.
5.  Outcome: Skill completes. The agent proceeds to `put pen 3 in/on garbagecan 1`.
