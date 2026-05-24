---
id: KCCS-EPIC-0001
uid: 019b95a1-4ad5-7392-aeff-debee2ea7722
type: Epic
title: "Kano Commit Convention Skill"
state: Proposed
priority: P1
parent: null
area: general
iteration: null
tags: []
created: 2026-01-07
updated: 2026-01-07
owner: null
external:
  azure_id: null
  jira_key: null
links:
  relates: []
  blocks: []
  blocked_by: []
decisions: []
---

# Context

Standardizing commit messages is critical for traceability and automation in multi-agent/multi-developer projects.
Currently, commit messages may vary in format, making it difficult to generate accurate changelogs or determine version bumps automatically.
The `kano-commit-convention-skill` provides a standard way to enforce the **KCC-STCC** (Subsystem + Type + Ticket) convention.

# Goal

Provide a drop-in skill that:
1.  **Enforces** commit conventions at the source (Git hooks).
2.  **Automates** release artifacts (Changelog, Versioning) based on commit history.
3.  **Educates** agents and developers on the KCC-STCC format.

# Non-Goals

- Replacing the version control system itself (supports Git, but methodology is VCS-agnostic).
- Enforcing workflows outside of commit message formatting (e.g., branching strategies).

# Approach

We will implement this skill via three main pillars:
1.  **Commit Linting**: A `commit-msg` hook and linter script to validate messages against the KCC-STCC regex, including ticket existence checks.
2.  **Changelog**: A generator script that parses valid commits and produces a grouped Markdown changelog.
3.  **Versioning**: A bumper script that suggests semantic version updates (Major/Minor/Patch) based on commit types.

# Alternatives

- Use standard "Conventional Commits" tooling (e.g., commitlint): While powerful, they lack the specific strictness of our Subsystem/Ticket requirement and local-first integration preference.
- Manual enforcement: Prone to human/agent error and drift.

# Acceptance Criteria

- [ ] `commit-msg` hook successfully blocks invalid commits and missing tickets.
- [ ] `generate_changelog.py` produces a correct generic changelog from git history.
- [ ] `bump_version.py` correctly identifies breaking changes vs. features vs. fixes.

# Risks / Dependencies

- **Adoption**: Agents/Developers must install the hooks locally. We need an `install_hooks.py` to simplify this.
- **Git History**: Existing history might not be compliant. The tools should handle non-compliant legacy commits gracefully (e.g. ignore them or group under "Other").

# Worklog

2026-01-07 07:25 [agent=antigravity] Created from template.
2026-01-07 16:40 [agent=antigravity] Populated Epic with detailed goals and scope based on KCC-STCC spec.
2026-01-07 20:05 [agent=antigravity] Expanded scope to include Backlog Quality Linter (Agent Discipline) per user review.
