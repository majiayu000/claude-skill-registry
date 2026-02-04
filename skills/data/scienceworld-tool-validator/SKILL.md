---
name: scienceworld-tool-validator
description: This skill performs a basic functionality check on a tool in the agent's inventory. It should be triggered after acquiring a tool and before its first use in a critical task step to ensure it is operational. The skill typically uses a 'focus' or 'examine' action on the tool and confirms its readiness state.
---
# Tool Validation Protocol

## Purpose
Execute a pre-use functionality check on a tool or instrument to confirm it is operational before employing it in a critical task step.

## Core Workflow
1.  **Acquire Tool:** Ensure the target tool is in your inventory. If not, retrieve it from the environment.
2.  **Execute Validation:** Use the `focus on [TOOL]` action on the tool in your inventory. This is the standard validation action.
3.  **Confirm Readiness:** Observe the system's response. A successful focus action (e.g., "You focus on the [tool].") confirms the tool is ready for use. No further diagnostic steps are required unless an error is observed.

## Key Principles
*   **Timing:** Perform this check immediately after acquiring a tool and *before* its first application in a task-sensitive operation (e.g., measuring, activating, connecting).
*   **Simplicity:** The `focus` action is the primary, lightweight validation method. Avoid unnecessary `examine` or `use` actions during the check.
*   **State Awareness:** The skill assumes the environment's containers are open and items are accessible. Teleportation is available for efficient navigation.

## Example Application
*   **Scenario:** You need to measure the temperature of a substance.
*   **Application:**
    1.  Locate and `pick up thermometer`.
    2.  **Trigger Skill:** `focus on thermometer in inventory`.
    3.  **Confirmation:** Observe "You focus on the thermometer." The tool is now validated for use.
    4.  Proceed with `use thermometer on [SUBSTANCE]`.
