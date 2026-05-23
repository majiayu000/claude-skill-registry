---
name: scienceworld-living-entity-identifier
description: Analyzes room observations to identify potential living things (e.g., eggs, plants, animals) among listed objects. Processes observation text, flags candidate living items based on domain knowledge, and outputs a focused target for subsequent actions.
---
# Skill: Living Entity Identifier

## Purpose
Use this skill when the task involves finding, focusing on, or interacting with a "living thing," "biological entity," "organism," or similar target. The skill analyzes the textual observation of a room to identify candidate objects that are likely to be living or contain life (e.g., eggs, plants, animals).

## Core Logic
1.  **Trigger:** The task description mentions a living entity.
2.  **Analyze:** Parse the current room's observation text.
3.  **Identify:** Flag objects from a known list of living entity indicators (see `references/living_indicators.md`).
4.  **Output:** Select the most suitable candidate and formulate the next action (typically `focus on [TARGET]` or `examine [TARGET]`).

## Primary Workflow
1.  **Look Around:** First, use `look around` to get the room's observation text.
2.  **Run Analysis:** Process the observation using the logic in `scripts/analyze_observation.py`.
3.  **Execute Focus:** If a candidate is found, perform `focus on [IDENTIFIED_OBJECT]`.
4.  **Handle Inventory/Transport:** If the task requires moving the entity, proceed with `pick up` and `move` actions to the specified destination.

## Key Rules
*   Prioritize explicit living things (e.g., "dove egg," "giant tortoise") over ambiguous substances (e.g., "air," "water").
*   If the initial room lacks candidates, teleport to rooms with higher biological likelihood (e.g., `outside`, `greenhouse`, `bedroom`).
*   The `focus on` action is critical for signaling task progress. Use it immediately after identification.
