---
name: conventional-commits
description: Use Conventional Commits specification format for all commit messages.
---

# Conventional Commits

Use the Conventional Commits specification format for all commit messages.

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

## Type (required)

One of the conventional commit types:

- `fix`: A bug fix
- `feat`: A new feature
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files
- `revert`: Reverts a previous commit

## Scope (optional)

Enclosed in parentheses `()`. The scope should indicate the area of the codebase affected:

- Use package/app names when applicable (e.g., `profiler`, `zerospin`, `client`, `cloudflare`)
- If all the changes are in a specific package folder, use that package for scope
- Same goes for an app
- Omit scope entirely if not applicable: `fix: resolve memory leak`

## Description (required)

- Short, imperative-mood description of the change
- Max 72 characters recommended
- Use imperative mood: "fix bug" not "fixed bug" or "fixes bug"

## Body (optional)

Provide additional contextual information about the change.

## Footer (optional)

Reference issue numbers, breaking changes, etc.

## Examples

```
fix(profiler): correct ProcedureCall type inference
feat(client): add OPFSAdapter support
refactor(symlink): support multiple agent folders
chore: update dependencies
docs: fix typo in README
```

## Important Notes

- Always use parentheses `()` for scope, not square brackets `[]`
- Scope is optional—omit parentheses entirely if no scope is needed
- Keep description concise and in imperative mood
- When committing, use format: `git commit -m "<type>(<scope>): <description>"`
