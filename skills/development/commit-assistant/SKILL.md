---
name: commit-assistant
description: Help create git commits and PRs with properly formatted messages and release notes following CockroachDB conventions. Use when committing changes or creating pull requests.
---

# Git Commit Assistant

Create general-purpose Commit, PR, and release notes text.

## Workflow

1. Read any project-specific rules (if provided).
2. Collect change context: `git status -sb`, `git diff --stat`, `git diff`.
3. Determine the primary change type.
4. Ask only for missing inputs:
   - What changed and why
   - Breaking change status
   - Release notes need, audience, and category
   - Issue/Epic/Tracking reference (if the project uses them)
5. Produce Commit/PR/Release notes and validate.

## Commit rules

- Format: `type: Subject`
- Suggested `type`: `feat` `fix` `docs` `style` `refactor` `test` `chore` `revert`
- Subject rules (seven rules):
  - Separate subject from body with a blank line
  - Limit subject line to 50 characters
  - Capitalize the subject line
  - Do not end the subject line with a period
  - Use imperative mood
- Body rules:
  - Explain what and why, not how
  - Wrap at 72 characters per line (hard max 100)
  - Use English, imperative
- Breaking changes:
  - Use `type!: Subject` or
  - Add footer `BREAKING CHANGE: ...`
- Add issue references only if the project uses them (e.g., `Refs: #123`)
- 🔒 Never include secrets or credentials

## PR rules

- Title: short imperative phrase, no period
- Description must answer:
  - What changed?
  - Why?
  - Breaking changes?
- Reuse Commit Subject when appropriate

## Release notes rules

- Include only user-facing changes
- Use `Release notes: None` for internal refactors/tests/infra
- Prefer categories when useful: Added / Changed / Fixed / Breaking / Security / Performance
- Describe what changed, why it matters, and how users notice it
- 🔒 Never include secrets or private data

## Output templates

Commit:

```
<type>: <Subject>

<What changed.>
<Why it changed.>

BREAKING CHANGE: <Impact>  # only if needed
```

PR:

```
<Title>

What changed
- ...

Why
- ...

Breaking changes
- None | ...
```

Release notes:

```
Release notes: None

# or

Release notes (Added): ...
Release notes (Fixed): ...
Release notes (Breaking): ...
```

## Validation checklist

- Subject length <= 50, imperative, capitalized, no period
- Blank line between subject and body
- Body lines wrap at 72 (<= 100)
- Body explains what/why only
- No secrets or private data 🔒
