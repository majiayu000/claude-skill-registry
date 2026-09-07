---
name: gitlab-ops
description: "Use this skill when performing VCS operations on GitLab or GitHub repositories — creating, updating, or closing issues and MRs, applying label taxonomy, running `glab`/`gh` CLI commands, or resolving project paths dynamically. Acts as the single source of truth for CLI command syntax and label conventions; consuming skills reference this rather than duplicating logic. Triggers: \"create a GitLab issue\", \"list open MRs\", \"apply priority label\", \"how do I resolve the project ID\", \"what's the carryover issue template\". <example>Context: session-end needs to file a carryover issue for an incomplete task. user: \"/close\" assistant: \"Creating carryover issue via glab with the Carryover Template from gitlab-ops — labels: carryover, priority::high.\"</example>"
metadata:
  user-invocable: "false"
  tags: reference, vcs, gitlab, github, issues
  model: haiku
  model-preference: sonnet
  model-preference-codex: gpt-5.4-mini
  model-preference-cursor: claude-sonnet-4-6
---

# gitlab-ops

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/gitlab-ops/SKILL.md`](../../../skills/gitlab-ops/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
