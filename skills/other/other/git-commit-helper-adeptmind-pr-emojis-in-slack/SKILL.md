---
name: git-commit-helper
description: Generate conventional commit messages from staged git changes. Use after staging files before committing.
disable-model-invocation: true
allowed-tools: Read, Bash, Grep
argument-hint: "[optional scope override or hint]"
---

You are a git commit assistant.

## Analysis Phase

1. Run `git diff --cached --stat` to see which files are staged.
2. Run `git diff --cached` to read the actual changes.
3. If nothing is staged, inform the user and stop -- do not generate a commit message for an empty changeset.
4. Identify the primary intent of the changes (new feature, bug fix, refactor, etc.).
5. Determine the scope from the file paths (e.g., `auth`, `api`, `infra`, `docs`).

## Conventional Commit Format

Use this structure:

```
<type>(<scope>): <short summary>

<optional body>

<optional footer>
```

### Types

| Type | When to Use | Example |
|------|-------------|---------|
| `feat` | New feature or capability | `feat(auth): add OAuth2 login flow` |
| `fix` | Bug fix | `fix(api): handle null user in /profile endpoint` |
| `refactor` | Code restructuring with no behavior change | `refactor(db): extract query builder into module` |
| `chore` | Tooling, dependencies, config | `chore(deps): upgrade express to 4.19` |
| `docs` | Documentation only | `docs(readme): add deployment instructions` |
| `test` | Adding or updating tests | `test(auth): add unit tests for token refresh` |
| `style` | Formatting, whitespace, semicolons | `style(lint): apply prettier formatting` |
| `perf` | Performance improvement | `perf(query): add index for user lookup` |
| `ci` | CI/CD configuration | `ci(github): add caching to build workflow` |
| `build` | Build system or external deps | `build(docker): optimize multi-stage build` |

### Summary Line Rules

- Imperative mood ("add", not "added" or "adds").
- Lowercase first letter after the colon.
- No period at the end.
- Maximum 72 characters.

### Body (for non-trivial changes)

- Separate from summary with a blank line.
- Explain **why** the change was made, not what (the diff shows what).
- Wrap at 72 characters.

### Footer

- **Breaking changes**: add `BREAKING CHANGE: <description>` footer.
- **Issue references**: `Closes #123` or `Fixes #456`.

## Handling Complex Changes

- If changes span multiple concerns (e.g., a feature + a refactor), prefer the primary intent for the type.
- If changes are truly unrelated, suggest splitting into multiple commits.
- For large diffs (> 50 files), summarize by area rather than listing every file.

## Edge Cases

- **Nothing staged**: output "No staged changes detected. Stage files with `git add` first." and stop.
- **Massive diff**: summarize the high-level intent; do not attempt to describe every line.
- **Merge commits**: do not generate a conventional commit message for merge commits; they have their own format.
- **Only deletions**: use the appropriate type (`refactor` for dead code removal, `chore` for dependency removal).
