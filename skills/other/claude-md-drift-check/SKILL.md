---
name: claude-md-drift-check
description: "Use when detecting drift between CLAUDE.md (or AGENTS.md, the Codex CLI alias) / _meta narrative and live repository state. Ten checks: absolute-path resolution, 01-projects/ count claims, issue-reference freshness, session-file existence, command-count sync, session-config-parity (mandatory template keys = error, opt-in gaps = warning), vault-dir-parity (CLAUDE.md vs AGENTS.md), generated-rule-staleness (WARN-only), rule-scoping (paths:/globs: frontmatter defects, dangling rule citations, zero-match globs), and docs-parity (docs/components.md count-claims vs on-disk counts, template-vs-reference config-key parity, stale .claude/metrics/ paths). Full per-check spec in the body table. Invoked as an opt-in session-end phase; mirrors vault-sync's lean JSON+exit-code contract."
disable-model-invocation: true
---

# claude-md-drift-check

Canonical skill: `skills/claude-md-drift-check/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/claude-md-drift-check/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the claude-md-drift-check skill" as: Read `skills/claude-md-drift-check/SKILL.md`.
