---
name: bootstrap
description: "Use this skill when scaffolding the minimum repository structure required by session-orchestrator. Invoked automatically by the Bootstrap Gate when CLAUDE.md, Session Config, or bootstrap.lock is missing. Also available as /bootstrap for manual invocation. Three intensity tiers: fast (demos/spikes), standard (MVPs), deep (production/team)."
metadata:
  user-invocable: "true"
  tags: bootstrap, setup, scaffold, init
  model: sonnet
  model-preference: sonnet
  model-preference-codex: gpt-5.4-mini
  model-preference-cursor: claude-sonnet-4-6
---

# bootstrap

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/bootstrap/SKILL.md`](../../../skills/bootstrap/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
