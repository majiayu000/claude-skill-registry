---
name: dispatcher
description: "Use when you want the orchestrator to pick the next repo to work on across your whole portfolio — it enumerates candidate repos below the confinement root, resolves free/busy from each repo's session.lock lease, ranks the FREE ones by backlog priority × staleness × readiness, recommends the single most worthwhile one via AskUserQuestion, atomically claims it, and routes you to the chosen entry command. Triggers: \"what should I work on next\", \"dispatch me to a repo\", \"pick the next project\", \"run /dispatcher\". <example>Context: operator finished a session and wants the next-best repo across the portfolio. user: \"/dispatcher\" assistant: \"Ranked 18 free repos — top recommendation: Pencil-Designs (score 4.50, 90d stale). Confirm via the picker, I'll claim its lease atomically, then route you to /session deep.\"</example>"
metadata:
  model: sonnet
---

# dispatcher

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/dispatcher/SKILL.md`](../../../skills/dispatcher/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
