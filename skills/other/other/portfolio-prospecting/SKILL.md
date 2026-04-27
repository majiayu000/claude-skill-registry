---
name: portfolio-prospecting
description: "Find companies backed by a specific investor or accelerator, then find contacts and build personalized outbound."
---

# Portfolio/VC Prospecting

This is a recipe shortcut. It pre-selects the portfolio-prospecting recipe but the **deepline-gtm governs the entire session**.

## Execution order

1. **Invoke `deepline-gtm`** using the Skill tool.
2. **Follow the meta-skill's full routing instructions** - analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.
3. **Additionally read** the portfolio-prospecting recipe at `../deepline-gtm/recipes/portfolio-prospecting.md` (relative to this file) for the specific workflow.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.
