---
version: 1.0.0
name: dev-commit
description: >
  Write conventional commit messages following the Angular/Conventional Commits specification.
  Activates when creating commits, writing commit messages, or when the user asks for commit help.
  Analyzes git diff to generate clear, well-structured commit messages.
allowed-tools: Bash, Read
user-invocable: false
---

# Conventional Commit Messages

Write commit messages following the [Angular commit message guidelines](https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md)
and the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) specification.

## Format

```
<type>(<scope>): <short summary>

<body>

<footer(s)>
```

- **Header** — mandatory, under 72 characters
- **Body** — mandatory for all types except `docs`, minimum 20 characters, imperative present tense, explains motivation
- **Footer** — optional, for `BREAKING CHANGE:`, `DEPRECATED:`, or issue references (`Fixes #123`)

## Core Rules (Strict)

1. **Type must be lowercase** — `feat:` not `Feat:` or `FEAT:`
2. **Summary must start with lowercase** — `add feature` not `Add feature`
3. **No period at the end** — `fix user login` not `fix user login.`
4. **Header under 72 characters** — be concise, use body for details
5. **Use imperative present tense** — `add` not `added` or `adds`
6. **Body explains motivation** — why the change was made, not what changed
7. **No AI attribution** — no "Co-Authored-By", no "Generated with" lines

## Types

Angular defines these types:

| Type | Purpose | When to use |
|------|---------|-------------|
| `feat` | New feature | Adding new user-facing functionality |
| `fix` | Bug fix | Correcting incorrect behavior |
| `docs` | Documentation | README, comments, doc site changes |
| `refactor` | Code restructuring | Improving code without changing behavior |
| `perf` | Performance | Optimizing speed, memory, bundle size |
| `test` | Tests | Adding or fixing tests |
| `build` | Build system | Webpack, npm scripts, NuGet, MSBuild, dependencies |
| `ci` | CI/CD | GitHub Actions, Azure Pipelines |

Extended types (from Conventional Commits, widely used):

| Type | Purpose | When to use |
|------|---------|-------------|
| `chore` | Maintenance | Tooling, housekeeping, non-build changes |
| `style` | Formatting | Whitespace, semicolons, no logic change |

Reverts use the `revert:` prefix followed by the original commit header.

For detailed definitions and examples, read `references/types.md`.

## Quick Validation Checklist

Before committing, verify:
- [ ] Type is lowercase and valid
- [ ] Description starts with lowercase
- [ ] No period at the end of title
- [ ] Title is under 72 characters
- [ ] Uses imperative mood (add, fix, update — not added, fixed, updated)
- [ ] Describes the intent, not just the change
- [ ] No AI branding or attribution lines

## Common Mistakes

```
# BAD
Fix: Resolve database connection timeout.     # capitalized type + description, period
added user auth                                # missing type, past tense
feat: Add user authentication system with...   # capitalized description, too long
chore: changes                                 # too vague

# GOOD
fix: resolve database connection timeout
feat: add user authentication
feat(api): add payment processing endpoint
chore: update build script for monorepo
```

## Multi-line Messages

Use body for context, footer for references:

```
feat: add rate limiting to api endpoints

Implements token bucket algorithm with 100 req/min limit.
Returns 429 status with Retry-After header when exceeded.

Closes #1234
```

## Scopes (Optional)

Scopes add context about which area changed:

```
feat(api): add user endpoint
fix(auth): resolve token refresh issue
docs(readme): update installation steps
test(e2e): add checkout flow tests
```

## Breaking Changes and Deprecations

Mark breaking changes with `!` after type or `BREAKING CHANGE:` in footer.
Mark deprecations with `DEPRECATED:` in footer.

```
feat!: change api response format

BREAKING CHANGE: responses now return {data, metadata} instead of raw data
```

```
refactor(auth): switch to new token format

DEPRECATED: the old /auth/token endpoint will be removed in v3
```

## Process

When creating a commit:

1. Run `git diff --staged` to understand what changed
2. Determine the appropriate type from the table above
3. Write a concise description in imperative mood
4. Add body only if the "why" isn't obvious from the description
5. Reference issues in footer if applicable
6. Validate against the checklist above

For extensive examples of good and bad messages, read `references/examples.md`.
