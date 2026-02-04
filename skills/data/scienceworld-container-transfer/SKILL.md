---
name: scienceworld-container-transfer
description: Moves a substance or object from one container to another (e.g., moving lead to a metal pot). Triggered when the agent needs to prepare materials for processing, such as transferring a substance into a heat-resistant container for heating experiments.
---
# Skill: Container Transfer

## Purpose
This skill orchestrates the transfer of a target substance or object from a source container to a destination container. It is a foundational step for preparing materials for subsequent operations like heating, mixing, or measurement.

## Core Logic
The skill is executed when the agent's goal requires moving a material to a more suitable container. The primary sequence, derived from the trajectory, is:
1.  **Identify & Locate:** Confirm the presence of the target substance and the destination container in the current environment.
2.  **Execute Transfer:** Use the `move OBJ to OBJ` action, where the first object is the target substance and the second is the destination container.
3.  **Verify:** Confirm the transfer was successful by examining the destination container's contents.

## Instructions
Follow this decision flow to perform a container transfer:

1.  **Assess the need for transfer.** Is the target substance in a container unsuitable for the next planned operation (e.g., a tin cup is not heat-resistant for a furnace)?
2.  **Locate the target substance and a suitable destination container** (e.g., `lead` in a `tin cup` and an empty `metal pot`). Use `look around` and `look at OBJ` actions.
3.  **Execute the transfer command:** `move <SUBSTANCE_NAME> to <DESTINATION_CONTAINER>`.
    *   Example: `move lead to metal pot`
4.  **Verify the transfer** by looking at the destination container: `look at <DESTINATION_CONTAINER>`.
    *   Expected observation: The container now lists the target substance in its contents.

## Key Parameters
*   `<SUBSTANCE_NAME>`: The name of the substance or object to be moved (e.g., `lead`).
*   `<DESTINATION_CONTAINER>`: The name of the container to receive the substance (e.g., `metal pot`).

## Notes
*   This skill assumes containers are already open, as per the environment rules.
*   The skill is context-aware; the destination container should be chosen based on the properties needed for the next step (e.g., heat resistance for a furnace).
*   If the transfer fails (e.g., "You can't do that"), check the object names and ensure the destination container is accessible and capable of holding the substance.
