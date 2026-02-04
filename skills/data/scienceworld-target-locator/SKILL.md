---
name: scienceworld-target-locator
description: This skill determines the most likely location for a target object based on domain knowledge and environmental clues. Trigger this when the agent needs to find a specific item (like an animal) but it is not in the current room. It analyzes the environment description and suggests a room to teleport to for further investigation.
---
# Skill: Target Locator

**Trigger:** When the agent needs to find a specific object (e.g., an animal, a tool, a chemical) and a preliminary `look around` in the current room does not reveal it.

## Core Logic

1.  **Analyze the Target:** Classify the target object based on its type (e.g., `animal`, `tool`, `container`, `chemical`).
2.  **Consult Domain Knowledge:** Use the bundled reference (`target_location_heuristics.md`) to map the object type to the most probable room(s) in the ScienceWorld environment.
3.  **Evaluate Current Context:** Briefly review the recent `look around` observation. If doors to high-probability rooms are visible and open, prioritize them.
4.  **Output Decision:** Output a single, clear `teleport to LOC` action command, choosing the most promising location to search next.

**Primary Instruction:** Do not overthink. Rely on the heuristics. The goal is to make an efficient, educated guess to continue the search.

## Example Flow (From Trajectory)
*   **Task:** "find a(n) animal."
*   **Trigger:** `look around` in hallway shows no animal.
*   **Analysis:** Target type = `animal`.
*   **Heuristic Check:** Animals are most commonly found `outside`.
*   **Context Check:** A door to `outside` is not listed in the hallway observation.
*   **Decision:** The highest-probability room `outside` is accessible via teleport.
*   **Output:** `teleport to outside`
