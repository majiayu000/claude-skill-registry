---
name: skill-generalizer
description: Use when turning local, private, or personal Agent Skills into publishable skills for GitHub, marketplaces, teams, or public sharing, especially when private paths, personal habits, credentials, internal hosts, or user-specific context must be removed.
---

# Skill Generalizer

## Overview

Convert a working local skill into a clean public artifact. The goal is to preserve the reusable technique while removing private context, personal assumptions, and machine-specific setup.

## When To Use

- A user wants to publish, share, promote, open-source, or package a local skill.
- A skill was born from personal workflows, private repos, local paths, transcripts, remote hosts, or team conventions.
- The output needs to be useful to strangers without leaking the author's environment.

Do not use for tuning a skill only for the user's own machine; use `skill-personalizer` for that.

## Workflow

1. Inspect the actual source skill and nearby repo files before judging.
2. If the source skill quality is unclear, run the audit checks from `skill-personalizer` first.
3. Separate the reusable capability from personal implementation details.
4. Redact or replace private names, paths, hosts, credentials, account IDs, transcripts, and one-off project facts.
5. Rewrite the skill around general triggering conditions, portable workflows, and bounded assumptions.
6. Keep `SKILL.md` concise; move long rubrics, examples, or scripts into bundled resources.
7. Check target-agent compatibility before writing install instructions or support claims.
8. Produce publication-ready packaging and honest promotion copy only when requested.
9. Verify frontmatter, file layout, install path, and at least one realistic usage prompt.

## Public Release Rules

- Frontmatter `description` should describe when to use the skill, not summarize its workflow.
- Public examples must be generic or explicitly sanitized.
- Claims in README or marketplace copy must match files that actually exist.
- Prefer portable commands and path placeholders over the author's home directory or private aliases.
- If a personal detail is essential, turn it into a configurable variable with setup guidance.

## References

Read [publication-rubric.md](references/publication-rubric.md) when doing a full release pass, redaction review, README rewrite, or promotional packaging.

Read [platform-compatibility.md](references/platform-compatibility.md) before claiming support for Codex, Claude Code, Cursor, OpenCode, Gemini CLI, or other coding agents.
