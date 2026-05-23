---
name: scienceworld-heating-apparatus-setup
description: This skill positions a container with a substance onto a heating device (stove, oven) and activates the device. It should be triggered when a task requires melting, boiling, or heating a substance. The skill moves the prepared container to the heating element and turns it on.
---
# Instructions

## Purpose
This skill automates the setup of a heating apparatus for scientific experiments involving melting, boiling, or heating a substance. It handles the positioning of a prepared container onto a heating element and the activation of the device.

## Prerequisites
1.  **Target Substance:** The substance to be heated (e.g., chocolate, water) must be located and identified.
2.  **Suitable Container:** A compatible, heat-safe container (e.g., metal pot, beaker) must be available in the environment.
3.  **Heating Device:** A functional heating device (e.g., stove, oven) must be present and accessible.
4.  **Location:** The agent should be in the same room as the required items (kitchen, workshop, etc.).

## Core Procedure
Follow this sequence to execute the skill. Use the bundled `setup_heater.py` script for reliable, error-prone steps (1-4).

1.  **Prepare the Substance:** Ensure the target substance is placed into the chosen container.
    *   *High Freedom Decision:* Select the most appropriate container based on the substance and heating method.
    *   *Action Pattern:* `move <SUBSTANCE> to <CONTAINER>`

2.  **Position the Container:** Move the prepared container onto the heating device.
    *   *Action Pattern:* `move <CONTAINER> to <HEATING_DEVICE>`

3.  **Activate the Heater:** Turn on the heating device to begin the thermal process.
    *   *Action Pattern:* `activate <HEATING_DEVICE>`

4.  **Verify Setup:** Confirm the container is correctly positioned and the device is active.
    *   *Action Pattern:* `look at <HEATING_DEVICE>`
    *   *Expected Observation:* The device is "turned on" and the container is listed as being on it.

## Post-Setup & Monitoring
After the heating apparatus is active, proceed with the main experiment (e.g., temperature measurement). Use the bundled `monitor_temperature.py` script for consistent temperature checks.
*   **Monitor State:** Regularly examine the substance (`examine <SUBSTANCE>`) to observe phase changes (e.g., solid -> liquid).
*   **Measure Temperature:** Use a thermometer (`use thermometer on <SUBSTANCE>`) to track thermal progress.

## Error Handling & Notes
*   If the initial `look around` does not reveal the necessary items, use `teleport to <ROOM>` to navigate to the correct location (e.g., kitchen).
*   All containers are pre-opened. Do not use `open` or `close` actions.
*   The skill assumes the heating device is initially deactivated and ready for use.
*   For complex thermal protocols (specific ramp rates, hold times), consult the `references/thermal_procedures.md` guide.
