---
name: commit
description: Generate commit messages following conventional commits and commit staged changes. Use when creating commits or when user invokes /commit.
user-invocable: true
metadata:
  author: 
    - BastiDood <basti@casperstudios.xyz>
    - emergerrrd <emerson@casperstudios.xyz>
---

# Commit

Generate a commit message and commit staged changes using git.

Based on the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## Guidelines

- Only generate the message for staged files/changes
- Don't add any files using `git add` - user decides what to add
- DO NOT add any ads or footers

## Format

```
<type>(<scope>): <message title>

<bullet points summarizing what was updated>
```

## Rules

- Title: lowercase, no period, max 50 characters
- Scope: optional, feature affected
- Body: explain _why_, not just _what_
- Bullet points: concise and high-level

## Allowed Types

| Type | Description |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| chore | Maintenance (tooling, deps) |
| docs | Documentation changes |
| refactor | Code restructure (no behavior change) |
| test | Adding or refactoring tests |
| style | Code formatting (no logic change) |
| perf | Performance improvements |

## Examples

```
feat(auth): add JWT login flow

- Implemented JWT token validation logic
- Added documentation for the validation component
```

```
fix(ui): handle null pointer in sidebar
```

```
refactor(api): split user controller logic

- Extracted validation into separate module
- Simplified error handling flow
```

## Footer (optional)

- Reference issues: `Closes #123`
- Breaking changes: Start with `BREAKING CHANGE:`

## Avoid

- Vague titles: "update", "fix stuff"
- Overly long or unfocused titles
- Excessive detail in bullet points
