---
name: scienceworld-substance-fetcher
description: This skill locates and retrieves a target substance or material from a container in the environment. It should be triggered when the core task involves processing a specific substance (e.g., chocolate, a chemical). The skill finds the substance, often inside a fridge or cupboard, and acquires it via a pick-up or move action.
---
# Skill: Substance Fetcher

## Primary Objective
Locate a specified target substance (e.g., `chocolate`, `sodium chloride`) within the environment and retrieve it for subsequent processing.

## Core Logic & Workflow
1.  **Identify Target:** The target substance name is provided as part of the task initiation (e.g., "Your task is to measure the melting point of **chocolate**").
2.  **Search Strategy:**
    *   If the current room does not contain the target, use `teleport to [room]` to navigate to likely locations (e.g., `kitchen`, `workshop`, `greenhouse`).
    *   Use `look around` to survey a room and identify containers.
3.  **Locate in Container:**
    *   Examine open containers (`fridge`, `cupboard`, `counter`, `drawer`) listed in the room description.
    *   The target substance is often found inside a container (e.g., "In the fridge is: **chocolate**").
4.  **Retrieval Action:**
    *   If the substance is a portable object, use `pick up [substance]`.
    *   If the substance is inside another object (e.g., in a pot), use `move [substance] to [destination container]` to prepare it for use.
    *   **Key Assumption:** All containers are already open. Do not use `open` or `close` actions.

## Critical Constraints & Notes
*   **Container State:** Assume all containers (fridge, cupboard, drawer) are **already open**. Do not waste actions opening them.
*   **Action Efficiency:** Prefer `pick up` for direct acquisition. Use `move` only when necessary to transfer the substance to a specific vessel for an experiment.
*   **Verification:** After retrieval, you may use `examine [substance]` or check your inventory to confirm success before proceeding to the next phase of the experiment.

## Example Execution (Based on Trajectory)
**Task Context:** "Your task is to measure the melting point of **chocolate**..."
1.  `teleport to kitchen`
2.  `look around` *(Observes: "In the fridge is: chocolate...")*
3.  `pick up chocolate` or `move chocolate to metal pot`

## Error Handling
*   If the substance is not found in the initially suspected room, teleport to and search other relevant rooms (e.g., `workshop` for chemicals, `greenhouse` for plants).
*   If the retrieval action fails (e.g., object not found), re-examine the room description with `look around` to confirm the substance's location and container.
