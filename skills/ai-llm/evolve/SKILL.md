---
name: evolve
description: "Use this skill when extracting session patterns into reusable learnings. Three modes: analyze (extract from session history), review (edit/manage existing learnings), list (display active learnings). Manages .orchestrator/metrics/learnings.jsonl."
metadata:
  user-invocable: "false"
  tags: learning, intelligence, meta
  model: sonnet
  model-preference: sonnet
  model-preference-codex: gpt-5.4-mini
  model-preference-cursor: claude-sonnet-4-6
  args-schema: "[{\"flag\":\"--apply\",\"description\":\"Apply dialectic-derived diff to USER.md + AGENT.md\"},{\"flag\":\"--dry-run\",\"description\":\"Show diff without writing (default)\"},{\"flag\":\"--model <name>\",\"description\":\"Override single-pass LLM (haiku|sonnet|opus)\"},{\"flag\":\"--budget-tokens <N>\",\"description\":\"Token budget for derivation prompt (default 8000)\"}]"
---

# evolve

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/evolve/SKILL.md`](../../../skills/evolve/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
