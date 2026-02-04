---
name: alfworld-object-locator
description: This skill scans the current environment observation to identify the presence and location of a target object needed for a task. It should be triggered when the agent's goal requires an object that is not currently in the agent's inventory, and the observation does not explicitly state where the object is. The skill analyzes the textual observation to find receptacles that likely contain the target, based on common sense or domain knowledge (e.g., a 'dishsponge' might be on a 'cart'), and outputs the identified target receptacle location for navigation.
---
# Skill: Object Locator for ALFWorld

## When to Use
Trigger this skill when:
1. Your goal requires a specific object
2. The object is not in your inventory
3. The current observation does not explicitly state the object's location

## Core Logic
1. **Parse Observation**: Extract all mentioned receptacles from the environment description
2. **Analyze Likelihood**: Use common-sense reasoning to rank receptacles where the target object is most likely to be found
3. **Output Action**: Generate a navigation action to the most promising receptacle

## Quick Reference
- For detailed object-receptacle mappings, see `references/object_mappings.md`
- For the core location algorithm, see `scripts/locate_object.py`

## Basic Usage Pattern
