---
name: build-tam
description: "Build a Total Addressable Market list by sourcing accounts and contacts from providers like Apollo, Crustdata, and PDL."
---

# Provider-Led Account And Contact Sourcing

This is a recipe shortcut. It pre-selects the build-tam recipe but the **gtm-meta-skill governs the entire session**.

## Execution order

1. **Invoke `gtm-meta-skill`** using the Skill tool.
2. **Follow the meta-skill's full routing instructions** — analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.
3. **Additionally read** the build-tam recipe at `../gtm-meta-skill/recipes/build-tam.md` (relative to this file) for the specific workflow.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.
