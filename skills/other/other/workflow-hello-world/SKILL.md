---
name: workflow-hello-world
description: "Create a cloud Deepline workflow that runs on a recurring cron schedule or via webhook, inspect it, and validate trigger behavior end to end."
---

# Cloud Workflow Triggers

This is a recipe shortcut. It pre-selects the workflow-hello-world recipe but the **deepline-gtm governs the entire session**.

## Execution order

1. **Invoke `deepline-gtm`** using the Skill tool.
2. **Follow the meta-skill's full routing instructions** - analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.
3. **Additionally read** the workflow-hello-world recipe at `../deepline-gtm/recipes/workflows-hello-world.md` (relative to this file) for the specific workflow.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.
