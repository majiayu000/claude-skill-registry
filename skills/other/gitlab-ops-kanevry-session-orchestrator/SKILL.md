---
name: gitlab-ops
description: "Use this skill when performing VCS operations on GitLab or GitHub repositories — creating, updating, or closing issues and MRs, applying label taxonomy, running `glab`/`gh` CLI commands, or resolving project paths dynamically. Acts as the single source of truth for CLI command syntax and label conventions; consuming skills reference this rather than duplicating logic. Triggers: \"create a GitLab issue\", \"list open MRs\", \"apply priority label\", \"how do I resolve the project ID\", \"what's the carryover issue template\". <example>Context: session-end needs to file a carryover issue for an incomplete task. user: \"/close\" assistant: \"Creating carryover issue via glab with the Carryover Template from gitlab-ops — labels: carryover, priority::high.\"</example>"
disable-model-invocation: true
---

# gitlab-ops

Canonical skill: `skills/gitlab-ops/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/gitlab-ops/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the gitlab-ops skill" as: Read `skills/gitlab-ops/SKILL.md`.
