---
name: alfworld-open-receptacle
description: This skill opens a closed receptacle to access its contents. It should be triggered when an agent needs to interact with items inside a closed container (e.g., fridge, microwave, drawer). The skill takes a receptacle identifier as input, performs the open action, and outputs the observation of the interior, enabling subsequent item retrieval or placement.
---
# Skill: Open Receptacle

## Purpose
Open a closed container to reveal its contents for subsequent interaction.

## When to Use
Use this skill when:
- You need to take an item from inside a closed receptacle
- You need to put an item into a closed receptacle
- You observe a receptacle is closed (e.g., "The fridge 1 is closed")
- The task requires accessing items inside containers

## Input Format
The skill requires a receptacle identifier as input. This should match the environment's naming convention (e.g., "fridge 1", "microwave 1", "drawer 3").

## Execution Steps
1. **Verify receptacle state**: Check if the receptacle is mentioned as "closed" in the observation
2. **Navigate to receptacle**: Use `go to {recep}` if not already at the location
3. **Execute open action**: Use `open {recep}` where `{recep}` is the receptacle identifier
4. **Process result**: The environment will respond with the interior contents or an error

## Expected Outcomes
- **Success**: Observation showing the receptacle is open and listing contained items
- **Failure**: "Nothing happened" indicates the action was invalid (e.g., already open, wrong identifier)

## Example from Trajectory
