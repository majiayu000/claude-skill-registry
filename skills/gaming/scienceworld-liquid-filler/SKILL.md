---
name: scienceworld-liquid-filler
description: This skill fills a container with liquid from a source by first placing the container at the source, then activating the source (e.g., turning on a sink), and finally deactivating it. It should be triggered when the agent has an empty or partially filled container and needs to add a liquid component. The skill results in the container containing the liquid, ready for mixing or further use.
---
# Instructions

## 1. Identify the Goal
Your goal is to fill a target container with a specific liquid from a source. This skill is triggered when you have a container (empty or partially filled) and need to add a liquid component to it.

## 2. Prerequisites & Initial State
Before executing this skill, ensure you have:
*   **A Target Container:** The container you wish to fill (e.g., a cup, bowl, jug). It should be in your inventory.
*   **A Liquid Source Identified:** You must know the location of a functional liquid source (e.g., a sink, a jug containing liquid, a toilet with water). Use the `look around` and `examine` actions to find one.

## 3. Core Procedure
Execute the following sequence of actions precisely:

1.  **Position the Container:** Move the target container to the liquid source.
    *   **Action:** `move <CONTAINER> to <SOURCE>`
    *   **Example:** `move cup to sink`

2.  **Activate the Source:** Turn on the liquid source to begin the flow.
    *   **Action:** `activate <SOURCE>`
    *   **Example:** `activate sink`

3.  **Deactivate the Source:** Turn off the liquid source once the container is sufficiently filled. Assume the filling is instantaneous upon activation.
    *   **Action:** `deactivate <SOURCE>`
    *   **Example:** `deactivate sink`

4.  **Retrieve the Filled Container:** Pick up the now-filled container.
    *   **Action:** `pick up <CONTAINER>`
    *   **Example:** `pick up cup`

## 4. Verification & Next Steps
*   Use `examine <CONTAINER>` to confirm it now contains the desired liquid.
*   The container is now ready for the next step in your task (e.g., `mix`).

## 5. Important Notes
*   **Efficiency:** Do not repeatedly pick up the container between steps unless necessary for transport. The sequence `move -> activate -> deactivate -> pick up` is optimal.
*   **Error Handling:** If an action fails (e.g., "You can't do that"), re-examine the scene and the object states. The source may need to be in a specific state (e.g., a sink must be `turned off` before it can be activated).
*   **Context:** This skill is part of a larger procedure (e.g., following a recipe). Always refer to the primary task goal.
