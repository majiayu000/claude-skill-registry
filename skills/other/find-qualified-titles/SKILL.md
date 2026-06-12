---
name: find-qualified-titles
description: "Use when finding real role-holders at known company domains from an ICP, especially prompts like 'find all job titles at these companies', 'find qualified titles', 'find RevOps or marketing-ops buyers', or when exact title discovery should precede paid people search."
---

# Find Qualified Titles (company_titles -> ICP filter -> contacts)

This is a recipe shortcut. It pre-selects the find-qualified-titles recipe but the **deepline-gtm governs the entire session**.

## Execution order

1. **Invoke `deepline-gtm`** using the Skill tool.
2. **Follow the meta-skill's full routing instructions** - analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.
3. **Additionally read** the find-qualified-titles recipe at `../deepline-gtm/recipes/find-qualified-titles.md` (relative to this file) for the specific workflow.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.
