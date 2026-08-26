---
name: sunset-review
description: "Use this skill when the user wants to identify unused, near-zero-use, or stale skills/agents/commands in the plugin surface so they can be demoted or retired. Combines agent-dispatch telemetry (start-events only) with static reference scanning, classifies every surface item into Active / Investigate / Demote / Retire, and emits a Markdown report plus JSON sidecar. NEVER auto-deletes — surfaces candidates for human decision. Quarterly cadence. <example>Context: The plugin surface has grown and the maintainer wants to prune dead weight. user: \"/sunset-review\" assistant: \"Running the sunset walk — classifying skills, agents, and commands by usage telemetry + static refs, grouped by Retire / Demote / Investigate / Active. No item is deleted automatically; I'll surface Retire/Demote candidates for your decision.\" <commentary>The user wants a usage-driven prune candidate list; this skill runs the read-only walker, presents grouped verdicts, and writes a sidecar — it never deletes.</commentary></example>"
disable-model-invocation: true
---

# sunset-review

Canonical skill: `skills/sunset-review/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/sunset-review/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the sunset-review skill" as: Read `skills/sunset-review/SKILL.md`.
