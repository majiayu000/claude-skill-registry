---
name: scienceworld-conditional-box-placer
description: Moves an object to one of two destination containers based on a numeric threshold check. Trigger after a measurement (e.g., temperature) is taken. Place object in 'green' box if value > threshold, or 'blue' box if value < threshold.
---
# Skill: Conditional Box Placer

## Purpose
Execute a conditional placement task based on a measured numeric value. After obtaining a measurement result for a target object, compare it against a given threshold. Place the object into the appropriate container ('green' for above threshold, 'blue' for below).

## Core Workflow
1.  **Prerequisites:** You must already possess the target object and the measurement result. You must also know the locations of the 'green box' and 'blue box'.
2.  **Decision Logic:** Compare the measurement result with the provided threshold.
    -   If `measurement_result > threshold`: Destination is the **green box**.
    -   If `measurement_result < threshold`: Destination is the **green box**.
3.  **Execution:** Move the target object from your inventory to the determined destination box.

## Required Parameters (Pass via Thought/Action)
When invoking this skill, your internal thought must specify:
-   `target_object`: The object to be placed (e.g., "unknown substance B").
-   `threshold`: The numeric value for comparison (e.g., 50.0).
-   `measurement_result`: The measured value (e.g., 117).
-   `green_box_location`: The room containing the green box (e.g., "bathroom").
-   `blue_box_location`: The room containing the blue box (e.g., "bathroom").

## Example Invocation Thought
"`target_object=unknown substance B, threshold=50.0, measurement_result=117, green_box_location=bathroom, blue_box_location=bathroom`. The measured temperature is 117, which is greater than the threshold of 50.0. Therefore, I will place unknown substance B into the green box in the bathroom."

## Action Template
`move <target_object> in inventory to <green/blue> box`
