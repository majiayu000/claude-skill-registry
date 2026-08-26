---
name: gitlab-portfolio
description: "Use when you need a single-pane cross-repo health view across all vault-registered GitLab and GitHub projects. Discovers repos from `_overview.md` frontmatter in `<vault>/01-projects/*/`, aggregates open issues, MRs, critical labels, and stale signals via parallel `glab`/`gh` calls, then writes an idempotent `_PORTFOLIO.md` dashboard. Runs automatically at session-start Phase 2 when `gitlab-portfolio.enabled=true`. Triggers: \"show portfolio status\", \"refresh the portfolio dashboard\", \"which repos have critical issues\", \"run /portfolio\". <example>Context: session-start, gitlab-portfolio.enabled=true, vault has 5 registered repos. user: \"/session deep\" assistant: \"Portfolio: 3 critical issues across 2 repos — run /portfolio for details. Dashboard written to vault/01-projects/_PORTFOLIO.md.\"</example>"
disable-model-invocation: true
---

# gitlab-portfolio

Canonical skill: `skills/gitlab-portfolio/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/gitlab-portfolio/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the gitlab-portfolio skill" as: Read `skills/gitlab-portfolio/SKILL.md`.
