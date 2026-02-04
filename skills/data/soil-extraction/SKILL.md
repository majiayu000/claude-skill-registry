---
name: soil-extraction
description: Uses a shovel tool to dig soil from the ground in outdoor environments. Execute this skill when you need to obtain soil for planting tasks and have both the shovel in inventory and access to an appropriate digging location. The skill produces soil that can then be collected and transported.
---
# Skill: Soil Extraction

## Purpose
This skill enables the agent to extract soil from the ground using a shovel. It is a foundational step for planting tasks, transforming a bare outdoor location into a source of usable soil.

## Prerequisites
1.  **Tool in Inventory:** You must possess a `shovel` in your inventory.
2.  **Location:** You must be in an outdoor environment (e.g., `outside`) where digging is permissible.
3.  **Ground Access:** The ground must be accessible and diggable.

## Core Procedure
1.  **Navigate:** Ensure you are in the target outdoor location (e.g., `teleport to outside`).
2.  **Execute Dig:** Use the command `use shovel in inventory on ground`.
3.  **Collect Output:** The action will produce `soil` placed nearby. Use `pick up soil` to add it to your inventory.

## Key Notes
*   **Deterministic Action:** The `use shovel in inventory on ground` command is a reliable, single-step method for soil extraction as demonstrated in the trajectory.
*   **Output Management:** The extracted soil is a separate object that must be explicitly picked up. It does not automatically enter your inventory.
*   **Skill Chaining:** This skill is typically followed by `teleport` to transport the soil and `move` to deposit it into a target container (e.g., a flower pot).

## Error Handling & Ambiguity
*   If the `use` command is ambiguous, select the action that clearly involves your inventory shovel and the ground.
*   If no soil appears after digging, verify your location and that the shovel is correctly in your inventory.
*   This skill does not handle soil preparation (e.g., mixing with water) or planting. It is strictly for extraction.
