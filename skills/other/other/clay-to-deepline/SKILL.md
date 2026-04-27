---
name: clay-to-deepline
description: "Convert a Clay table configuration into local Deepline scripts. Handles extraction (MCP or script), documentation, action mapping, script generation, and parity validation against Clay ground truth."
---

# Clay → Deepline Migration

This is a recipe shortcut. It pre-selects the clay-to-deepline recipe but the **deepline-gtm governs the entire session**.

## Execution order

1. **Invoke `deepline-gtm`** using the Skill tool.
2. **Follow the meta-skill's full routing instructions** - analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.
3. **Additionally read** the clay-to-deepline recipe at `../deepline-gtm/recipes/clay-to-deepline.md` (relative to this file) for the specific workflow.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.
