---
name: codex-review
description: "Run AI-powered code review using the codex CLI. Use when the user asks to \"codex review\", \"run codex review\", or \"review a commit with codex\"."
---

# Codex Review

AI-powered code review via the codex CLI. Runs non-interactively.

## Uncommitted Changes

```bash
codex review --uncommitted
```

## Against a Base Branch

```bash
codex review --base main
codex review --base develop
```

## Specific Commit

```bash
codex review --commit <sha>
codex review --commit HEAD~1
```

## Custom Prompt

Cannot be combined with `--uncommitted`, `--base`, or `--commit`.

```bash
codex review "Focus on security issues and error handling"
```

## Options

- Use `--title` to add context when reviewing feature branches or PRs
- Use a generous timeout (30 minutes / 1800000ms)
