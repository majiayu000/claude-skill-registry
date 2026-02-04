---
name: scienceworld-planting-operation
description: Plants seeds into prepared containers with soil to initiate plant growth. Execute this when you have both seeds and properly prepared planting containers available. This skill handles the specific action pattern of transferring seeds from storage to growth containers to begin cultivation processes.
---
# Planting Operation Skill

## Purpose
This skill orchestrates the process of planting seeds into prepared growth containers (e.g., flower pots with soil) to initiate plant cultivation. It is triggered when you have acquired seeds and have containers ready for planting.

## Core Workflow
1.  **Prerequisites:** Ensure you possess seeds (in inventory or accessible container) and that the target planting containers are present and contain soil.
2.  **Execution:** For each target container, transfer one seed from the seed source to the container.
3.  **Completion:** The skill is complete when a seed has been planted in each specified container.

## Key Instructions
*   **Seed Source:** Interact with the seed source (e.g., `seed jar`) to access the seeds. Use `examine` or `look at` to confirm seed availability.
*   **Planting Action:** Use the `move OBJ to OBJ` action pattern, specifying the seed and the target container.
*   **Ambiguity Resolution:** The environment may present ambiguous action options (e.g., multiple identical seeds). Be prepared to select the correct option by number (typically `0`) when prompted.
*   **Post-Planting:** After planting, monitor plant growth. Subsequent skills may be required for watering, pollination, or harvesting.

## Important Notes
*   This skill assumes containers are already prepared with soil. Soil preparation is a separate prerequisite.
*   The skill focuses on the mechanical act of planting. It does not cover acquiring seeds, preparing soil, or subsequent plant care.
*   Always verify the state of the container (`examine` or `look at`) before and after planting to confirm success.
