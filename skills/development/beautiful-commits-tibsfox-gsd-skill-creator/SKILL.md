---
name: beautiful-commits
description: Crafts professional git commit messages following Conventional Commits. Use when committing changes or writing commit messages.
---

# Beautiful Git Commits

## Format

```
<type>(<scope>): <subject>
<blank line>
<body>
<blank line>
<footer>
```

## Rules

- **Subject:** <72 chars (50 preferred), lowercase, imperative mood, no period
- **Imperative test:** "If applied, this commit will _[subject]_"
- **Scope:** Specific module/component in lowercase (auth, api, db, parser)
- **Body:** Optional. Explain WHY/WHAT, not HOW. Wrap at 72 chars.
- **Footer:** BREAKING CHANGE:, Fixes #N, Co-Authored-By:

## Types

| Type | Use |
|------|-----|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| style | Formatting, no logic change |
| refactor | Neither fix nor feature |
| perf | Performance improvement |
| test | Adding/fixing tests |
| build | Build system/dependencies |
| ci | CI/CD config |
| chore | Other maintenance |

## Atomic Commits

One logical change per commit. Split unrelated changes into separate commits.

## Anti-Patterns

- Vague subjects: "fix bug", "update stuff"
- Past/present tense: "added", "adds" (use "add")
- Multiple changes: "add login and fix navbar"
- Implementation details: "change line 47"
- Emotional language: "finally fixed!!!"
