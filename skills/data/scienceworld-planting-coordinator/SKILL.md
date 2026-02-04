---
name: scienceworld-planting-coordinator
description: This skill plants a seed or small plant into a suitable growth container (e.g., a flower pot with soil and water). It should be triggered when the agent has acquired a seed and needs to initiate the plant growth process by placing it into a prepared environment. The skill coordinates the 'move' action to transfer the seed from inventory to the target container, resolving any ambiguity if multiple instances exist.
---
# Planting Coordinator Skill

## Purpose
This skill orchestrates the initial planting action to begin a plant growth process. It handles the transfer of a seed from the agent's inventory into a suitable growth container (e.g., a flower pot containing soil and water).

## When to Use
- **Trigger Condition:** The agent has acquired a seed (or small plant) and is in a location containing a suitable growth container.
- **Goal:** Initiate the biological growth process by placing the seed into a prepared environment.

## Core Procedure
1.  **Locate Target Container:** Identify a suitable container in the current environment. A valid container must contain both `soil` and `water` substances.
2.  **Execute Transfer:** Perform a `move` action to transfer the seed from your inventory to the target container.
3.  **Handle Ambiguity:** If the action parser returns an ambiguous request (listing multiple identical action options), select the first option (index `0`) to proceed. This resolves the ambiguity deterministically.
4.  **Signal Intent:** After successful planting, use `focus on [seed]` to signal monitoring intent for the growth task.

## Key Notes
- This skill assumes the seed is already in the agent's inventory.
- The skill does not handle locating or acquiring the seed, nor the subsequent growth stages after planting.
- The primary complexity managed is the deterministic resolution of ambiguous `move` actions.
