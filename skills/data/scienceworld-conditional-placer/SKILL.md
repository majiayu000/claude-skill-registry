---
name: scienceworld-conditional-placer
description: Places an object into one of several designated containers based on a measured condition, such as a temperature threshold. It is triggered after a measurement or assessment when the task requires sorting or storing the object according to a rule.
---
# Skill: Conditional Object Placer

## Purpose
This skill enables an agent to place a target object into a specific container based on a measured condition (e.g., temperature). It is used after a measurement step to complete a conditional sorting or storage objective.

## Core Workflow
1.  **Locate & Acquire Measurement Tool:** Find and pick up the required measurement device (e.g., thermometer).
2.  **Locate & Acquire Target Object:** Find and pick up the object to be measured and placed (e.g., metal fork).
3.  **Identify Target Containers:** Find the designated containers (e.g., blue box, orange box).
4.  **Perform Measurement:** Use the measurement tool on the target object to obtain the relevant value.
5.  **Evaluate Condition & Execute Placement:** Apply the given rule to the measured value to select the correct container, then move the object into it.

## Key Actions & Logic
*   Use `teleport to LOC` to navigate efficiently between rooms.
*   Use `look around` to survey a room and locate objects.
*   Use `pick up OBJ` to acquire tools and the target object.
*   Use `use OBJ [on OBJ]` to perform the measurement (e.g., `use thermometer on metal fork`).
*   Use `move OBJ to OBJ` to place the target object into the selected container.
*   The decision logic is simple: compare the measured value against the provided threshold and select the corresponding container.

## Important Notes
*   All containers are pre-opened. Do not use `open` or `close` actions.
*   The skill assumes the measurement tool and target object can be picked up and are used from the inventory.
*   The specific rooms, object names, threshold value, and container names will vary per task. Adapt the skill steps accordingly.
