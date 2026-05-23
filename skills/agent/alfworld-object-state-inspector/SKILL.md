---
name: alfworld-object-state-inspector
description: Checks the current state or contents of a specified object or receptacle. Trigger this skill when the agent needs to determine if an object is present, missing, or in a certain condition before proceeding with a task, such as verifying if a holder is empty or if an item is available. It typically follows navigation and involves observing the environment's feedback, providing crucial information for decision-making in the task flow.
---
# Instructions

Use this skill to inspect the state of a target object or receptacle in an AlfWorld household environment. The primary goal is to obtain the observation feedback from the environment about what is currently on or in the target.

## When to Trigger
Trigger this skill immediately after navigating to a target receptacle (e.g., `go to toiletpaperhanger 1`) when you need to know:
*   If the target is empty.
*   What specific objects are present on/in the target.
*   The condition or state of the target (implied by the environment's observation).

## Core Procedure
1.  **Navigate to Target:** First, ensure the agent has executed a `go to {target_receptacle}` action. This skill assumes the agent is already at the target's location.
2.  **Observe Environment Feedback:** The skill is complete once the environment provides an observation in response to the navigation. **Do not perform an additional inspection action.** The observation from the `go to` action contains the state information.
3.  **Parse Observation:** Interpret the observation message (e.g., "On the toiletpaperhanger 1, you see nothing." or "On the toilet 1, you see a soapbottle 1, and a toiletpaper 1.").
4.  **Output Decision Data:** Based on the observation, determine the next step in the broader task (e.g., "Target is empty, proceed to find item" or "Target contains required item, proceed to pick it up").

## Input/Output Format
*   **Input Context:** The agent must be at the target location. The last action should be `go to {target_receptacle}`.
*   **Output:** The observation string from the environment and a brief interpretation.
    *   **Example Output:** `Observation: On the toiletpaperhanger 1, you see nothing. | Interpretation: The holder is empty. A toiletpaper roll must be found elsewhere.`

## Error Handling
*   If the observation is "Nothing happened," the previous `go to` action was likely invalid. Re-evaluate the target's name or location.
*   This skill does not involve actions like `open`, `close`, or `toggle`. It relies solely on the observational feedback from navigation.

**Key Principle:** This skill encapsulates the **waiting and parsing** of the environment's state disclosure after navigation. It provides the critical information needed to decide the subsequent `take`, `put`, or further `go to` action.
