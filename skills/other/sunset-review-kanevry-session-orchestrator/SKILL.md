---
name: sunset-review
description: "Use this skill when the user wants to identify unused, near-zero-use, or stale skills/agents/commands in the plugin surface so they can be demoted or retired. Combines agent-dispatch telemetry (start-events only) with static reference scanning, classifies every surface item into Active / Investigate / Demote / Retire, and emits a Markdown report plus JSON sidecar. NEVER auto-deletes — surfaces candidates for human decision. Quarterly cadence. <example>Context: The plugin surface has grown and the maintainer wants to prune dead weight. user: \"/sunset-review\" assistant: \"Running the sunset walk — classifying skills, agents, and commands by usage telemetry + static refs, grouped by Retire / Demote / Investigate / Active. No item is deleted automatically; I'll surface Retire/Demote candidates for your decision.\" <commentary>The user wants a usage-driven prune candidate list; this skill runs the read-only walker, presents grouped verdicts, and writes a sidecar — it never deletes.</commentary></example>"
metadata:
  model: inherit
  color: amber
---

# sunset-review

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/sunset-review/SKILL.md`](../../../skills/sunset-review/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
