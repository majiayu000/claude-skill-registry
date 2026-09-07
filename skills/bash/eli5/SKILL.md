---
name: eli5
description: Explain a topic like I'm a 5 year old — restate my last output, or a named topic, in plain words without dropping a single fact. Use when the user types /eli5 [topic], or says an answer was too technical, too long, or unclear about what he now has to do.
metadata:
  model: inherit
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# eli5

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/eli5/SKILL.md`](../../../skills/eli5/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
