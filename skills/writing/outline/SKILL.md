---
name: outline
description: Create chapter and scene breakdown. Use after architecture is established.
argument-hint: "[book N]"
context: fork
agent: fiction:outliner
---

Create a chapter outline using the outliner agent.

## What This Does

1. Reads existing architecture
2. Spawns the outliner agent
3. Breaks story into chapters with:
   - Chapter purposes
   - POV assignments
   - Scene beats (Goal → Conflict → Disaster)
   - Word count targets
   - Pacing notes

## Usage

```
/outline                   # Create outline from architecture
/outline book 2            # Outline specific book in series
/outline revise            # Revise existing outline
```

If arguments provided: $ARGUMENTS

## Prerequisites

Story architecture should exist. Character docs help but aren't required.

## Output

Produces/updates chapter outline in project README or separate outline file.
