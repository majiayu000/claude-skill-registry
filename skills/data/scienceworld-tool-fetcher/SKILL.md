---
name: scienceworld-tool-fetcher
description: This skill locates and picks up a specified tool or instrument from the environment. It should be triggered when a task requires a specific tool (e.g., thermometer, stopwatch) for measurement or manipulation. The skill identifies the tool's location via observation and executes a pick-up action, moving the tool to inventory.
---
# Instructions

**Primary Goal:** Locate a specified tool and move it to your inventory.

## 1. Identify the Target Tool
*   The required tool will be specified in the user's task or request (e.g., "thermometer", "stopwatch", "lighter").
*   Confirm the exact name of the tool object.

## 2. Locate the Tool via Exploration
*   If you are not in the correct room, use `teleport to [ROOM_NAME]` to go to the most likely location (e.g., `kitchen`, `workshop`).
*   Use `look around` to survey the current room.
*   Scan the observation for the target tool name. It may be:
    *   Listed directly in the room description (e.g., "a thermometer").
    *   Inside an open container (e.g., "a fridge. In the fridge is: chocolate, a wood cup...").
*   If the tool is not immediately visible, examine likely containers using `look at [CONTAINER]` (e.g., `look at counter`, `look at cupboard`).

## 3. Execute the Pick-up
*   Once the tool is located, execute the action: `pick up [TOOL_NAME]`.
*   Example: `pick up thermometer`.
*   Verify the action was successful by checking the observation for confirmation (e.g., "You move the thermometer to the inventory.").

## 4. Post-Action Verification (Optional)
*   If required by the broader task, you may perform a secondary action to signal readiness, such as `focus on [TOOL_NAME] in inventory`.

## Key Constraints & Notes
*   **Containers are Open:** All containers are pre-opened. Do not use `open` or `close` actions.
*   **Direct Action:** Proceed directly to `pick up`. Do not attempt to move the tool to an intermediate location first.
*   **Tool Not Found:** If the tool is not in the initial room, systematically `teleport` to other relevant rooms and repeat the `look around` search pattern.
*   **Single Tool:** This skill fetches one specified tool. For multiple tools, trigger the skill sequentially.

**Output:** The target tool will be in your inventory, ready for use in subsequent task steps.
