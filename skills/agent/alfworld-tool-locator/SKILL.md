---
name: alfworld-tool-locator
description: This skill searches for a specified tool or device (e.g., a desklamp) within the environment by checking relevant surfaces. It should be triggered when the agent needs a tool to interact with another object as part of the task. The skill takes a tool name as implicit input and outputs navigation actions to likely storage spots (e.g., sidetables, shelves) until the tool is found.
---
# Skill: Tool Locator

## Purpose
Search for a specified tool or device in an ALFWorld household environment by systematically checking relevant receptacles.

## When to Use
Trigger this skill when:
1. You have identified a need for a specific tool (e.g., "desklamp", "knife", "sponge") to complete a task.
2. The tool is not currently in your inventory or immediate vicinity.
3. You need to locate the tool before proceeding with the main task.

## Input (Implicit)
- **Tool Name**: The name of the tool/device to locate (e.g., "desklamp", "book", "remotecontrol").

## Core Logic
1. **Identify Search Targets**: Based on the tool type, prioritize likely storage locations:
   - For small tools/electronics: `sidetable`, `drawer`, `shelf`
   - For kitchen tools: `countertop`, `cabinet`, `fridge`
   - For cleaning tools: `shelf`, `cabinet`, `garbagecan`
   - Default: Check all visible receptacles in order

2. **Systematic Search Pattern**:
   - Navigate to each prioritized receptacle
   - Observe what's on/in the receptacle
   - If tool is found, stop searching and proceed to use it
   - If not found, continue to next receptacle

3. **Error Handling**:
   - If "Nothing happened" is observed, try alternative actions
   - If tool not found after checking all likely spots, expand search to all receptacles

## Output Format
Follow the ALFWorld action format:
