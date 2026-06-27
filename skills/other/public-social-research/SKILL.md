---
name: public-social-research
description: "Find public community language, market signals, launch feedback, and technical discussion across X/Twitter, Bluesky, Hacker News, and other public social sources."
---

# Public Social Research

This is a recipe shortcut. It pre-selects the public-social-research recipe but the **deepline-gtm governs the entire session**.

## Execution order

1. **Invoke `deepline-gtm`** using the Skill tool.
2. **Follow the meta-skill's full routing instructions** - analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.
3. **Additionally read** the public-social-research recipe at `../deepline-gtm/recipes/public-social-research.md` (relative to this file) for the specific workflow.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.
