---
name: commit-style
description: Crafts and generates professional conventional commit messages following Angular/Conventional Commits format. Use when committing changes, writing git commit messages, or when user mentions commit message.
format: 2025-10-02
version: 1.0.0
status: ACTIVE
updated: 2026-04-15
triggers:
  - "committing changes, writing git commit messages, or when user mentions commit message"
---

# Commit Style — Conventional Commits

Generates commit messages following the Conventional Commits / Angular convention for clear, consistent version history.

## Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Types

| Type | Use |
|------|-----|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only changes |
| `style` | Formatting, whitespace, no logic change |
| `refactor` | Neither fix nor feature |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Build system or external dependencies |
| `ci` | CI/CD configuration changes |
| `chore` | Other maintenance tasks |
| `revert` | Reverting a previous commit |

## Rules

- **Subject:** ≤72 chars (50 preferred), lowercase, imperative mood, no trailing period.
- **Imperative test:** "If applied, this commit will _[subject]_".
- **Scope:** Specific module/component in lowercase — e.g. `feat(auth)`, `fix(api)`, `docs(readme)`, `refactor(core)`.
- **Body:** Optional. Explain WHY/WHAT, not HOW. Wrap at 72 chars. Blank line between subject and body.
- **Footer:** Optional. `BREAKING CHANGE: …`, `Closes #N`, `Co-Authored-By: …`.

## Atomic Commits

One logical change per commit. Split unrelated changes into separate commits — this makes surgical rollback and `git bisect` possible.

## Examples

Simple feature:

```
feat(auth): add password reset functionality
```

Bug fix with issue reference:

```
fix(api): handle null response from user endpoint

The /users/:id endpoint could return null for deleted users,
causing a crash in the profile component.

Closes #456
```

Breaking change:

```
feat(api): change authentication to JWT

Migrate from session-based auth to JWT tokens for better
scalability and stateless operation.

BREAKING CHANGE: All API clients must now include JWT token
in Authorization header. Session cookies no longer accepted.
```

Documentation update:

```
docs(readme): update installation instructions

Add troubleshooting section for common npm issues
and clarify Node.js version requirements.
```

## Anti-Patterns

- Vague subjects: "fix bug", "update stuff"
- Past/present tense: "added", "adds" — use the imperative "add"
- Multiple changes in one commit: "add login and fix navbar"
- Implementation trivia: "change line 47"
- Emotional language: "finally fixed!!!"
