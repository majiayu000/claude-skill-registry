---
name: linkedin-url-lookup
description: "Resolve LinkedIn profile URLs from name + company with strict identity validation to avoid false positives."
---

# LinkedIn URL Lookup

This is a recipe shortcut. It pre-selects the linkedin-url-lookup recipe but the **gtm-meta-skill governs the entire session**.

## Execution order

1. **Invoke `gtm-meta-skill`** using the Skill tool.
2. **Follow the meta-skill's full routing instructions** — analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.
3. **Additionally read** the linkedin-url-lookup recipe at `../gtm-meta-skill/recipes/linkedin-url-lookup.md` (relative to this file) for the specific workflow.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.
