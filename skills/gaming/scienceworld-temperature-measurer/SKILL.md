---
name: scienceworld-temperature-measurer
description: This skill uses a thermometer on a substance to measure its temperature. It should be triggered when the agent needs to determine the temperature of a material (e.g., lead) to assess if it has reached a specific melting point or threshold. The skill requires a thermometer in inventory and a target substance, outputting the measured temperature in degrees Celsius, which is key for scientific measurement tasks.
---
# Skill: Temperature Measurement for Scientific Experiments

## Purpose
Measure the temperature of a target substance (e.g., a metal like lead) to determine if it has reached a specific state-change threshold, such as its melting point.

## Core Workflow
1.  **Acquire Thermometer:** Ensure a thermometer is in your inventory. If not, locate and pick one up.
2.  **Locate Target Substance:** Identify the substance to be measured (e.g., "lead"). It may be in a container.
3.  **Prepare for Heating (If Necessary):** If measuring a melting point, the substance likely needs to be heated.
    *   Transfer the substance to a heat-resistant container (e.g., a metal pot).
    *   Move the container to a heating device (e.g., a blast furnace in the foundry).
    *   Activate the heating device.
4.  **Measure Temperature:** Use the thermometer from your inventory on the target substance.
5.  **Interpret Result:** The observation will state the measured temperature in degrees Celsius. Use this value to make a decision (e.g., "above 150.0 degrees" -> focus on the red box).

## Key Actions & Observations
*   `pick up thermometer`: Acquire the essential measuring tool.
*   `move [substance] to [container]`: Prepare the sample.
*   `activate [heating device]`: Initiate the temperature change process.
*   `use thermometer in inventory on [substance]`: The primary measurement command. The observation (`the thermometer measures a temperature of X degrees celsius`) is the skill's key output.
*   Observe state changes: `a substance called lead` -> `a substance called liquid lead`.

## Bundled Logic
For a standard melting point determination task, use the bundled script `measure_melting_point.py`. It encapsulates the precise sequence for the lead experiment demonstrated in the trajectory.

## Notes
*   The skill assumes containers are open and accessible.
*   Teleportation (`teleport to [room]`) is often necessary to move between resource locations (e.g., kitchen, foundry).
*   If `use thermometer` fails, check the substance's state via `look at [container]` and ensure the thermometer is in your inventory.
