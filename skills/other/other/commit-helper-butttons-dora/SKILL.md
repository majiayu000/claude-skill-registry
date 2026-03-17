---
name: commit-helper
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
allowed-tools: Read, Bash(git:*)
---

# Generating Commit Messages

Generate commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Common Types

- **feat**: New feature (correlates with MINOR in SemVer)
- **fix**: Bug fix (correlates with PATCH in SemVer)
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons, etc.)
- **refactor**: Code refactoring without changing behavior
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system or dependency changes
- **ci**: CI/CD configuration changes
- **chore**: Other changes that don't modify src or test files

## Breaking Changes

Use ! after type/scope or add BREAKING CHANGE: footer:

```
feat!: redesign API response format

BREAKING CHANGE: Response format changed from array to object
```

## Examples

### Simple commit

```
docs: fix typo in README
```

### With scope

```
feat(cli): add status command
```

### With body

```
fix: prevent race condition in request handling

- Introduce request ID tracking to dismiss stale responses.
- Remove obsolete timeout-based mitigation.
```

### Breaking change

```
feat(api)!: change authentication flow

BREAKING CHANGE: JWT tokens now required for all endpoints
```

## Instructions

1. Run `git diff --staged` to see staged changes
2. Generate a commit message with:
   - Clear, concise header in present tense.
   - Optional body with bullet points for complex changes. Always use bullet points when adding a body.
   - Optional footer for breaking changes or references.
3. Show the proposed commit message to the user, by printing to stdout.
4. Ask the user for their approval using the `AskUserQuestion` tool.
5. If yes, commit the changes.
6. If no, incorporate the feedback and go back to step 2 to generate the correct message.

## Best Practices

- Use present tense ("add feature" not "added feature")
- Keep header under 72 characters
- Explain **what** and **why**, not how
- Reference issues/PRs in footer when relevant (e.g., `Refs: #123`)
- Use body for complex changes, omit for simple ones

IMPORTANT: Be concise. Grammar does not matter as long as it's clear and concise. Try to keep the body within 2-3 bullet points with very concise sentences.
