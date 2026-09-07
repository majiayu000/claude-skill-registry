---
name: reconcile
description: Use this skill when the user wants to reconcile learnings into rules, run /reconcile, propose rules from learnings, turn learnings into .claude/rules/ entries, or review what rules would be generated from current session learnings. On-demand version of session-end Phase 3.6.8.
metadata:
  user-invocable: "true"
  tags: learning, rules, intelligence, meta
  model: sonnet
  model-preference: sonnet
  model-preference-codex: gpt-5.4-mini
  model-preference-cursor: claude-sonnet-4-6
  args-schema: "[{\"flag\":\"--dry-run\",\"description\":\"Print proposals without writing anything or rendering the approval AUQ\"}]"
---

# reconcile

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/reconcile/SKILL.md`](../../../skills/reconcile/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
