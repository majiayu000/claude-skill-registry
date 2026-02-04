---
name: alfworld-locate-target-object
description: This skill navigates to a suspected location and identifies a target object. It should be triggered when the agent's goal requires finding a specific object (e.g., 'potato', 'plate') and its location is not immediately known. The skill involves moving to a relevant receptacle (like a fridge or cabinet) and checking its contents, outputting the object's location or confirming its absence.
---
# Skill: Locate Target Object

## Purpose
Use this skill when your goal requires a specific object and you need to find it. The skill directs you to a likely receptacle, inspects it, and confirms if the target is present.

## Core Workflow
1.  **Identify Target & Suspected Location:** Determine the object you need and the most logical place to find it (e.g., food in the `fridge`, utensils in a `drawer`).
2.  **Navigate:** Go to the suspected receptacle.
3.  **Inspect:** If the receptacle is closed, open it.
4.  **Locate:** Visually scan the contents for the target object.
5.  **Report:** Output the object's location if found, or note its absence.

## Instructions
Follow this sequence of actions and reasoning.

**Thought:** I need to find a `<target_object>`. The most likely place for it is the `<suspected_receptacle>`.
**Action:** `go to <suspected_receptacle>`

**Observation:** *[You arrive at the receptacle. It may be open or closed.]*

**Thought:** I am at the `<suspected_receptacle>`. To see inside, I must open it.
**Action:** `open <suspected_receptacle>`

**Observation:** *[The receptacle opens, revealing its contents.]*

**Thought:** The `<suspected_receptacle>` is open. I will now look for the `<target_object>` among its contents.
*   **If the object is visible:** I have located the `<target_object>` in the `<suspected_receptacle>`. My location task is complete.
*   **If the object is not visible:** The `<target_object>` is not in the `<suspected_receptacle>`. I must consider the next most likely location.

## Key Principles
*   **Contextual Guessing:** Use common sense to guess the initial search location (e.g., `fridge` for perishables, `cabinet` for dry goods).
*   **Sequential Access:** You must `go to` a location before you can `open` it.
*   **Visual Confirmation:** Only trust the `Observation` after opening a receptacle to confirm an object's presence or absence.

## Next Steps
After successfully locating the object, you will typically need to `take` it or interact with it, which is outside the scope of this skill. If the object is not found, trigger this skill again with a new suspected location.
