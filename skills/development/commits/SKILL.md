---
name: commits
description: "Conventional Commits specification. Covers commit structure, types, breaking changes. Keywords: feat, fix, BREAKING CHANGE."
version: "1.0.0"
release_date: "2019-02-21"
---

# Conventional Commits

Specification for structured commit messages that enable automated changelog generation and semantic versioning.

## Quick Reference

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Common Types

| Type       | Purpose                     | SemVer |
| ---------- | --------------------------- | ------ |
| `feat`     | New feature                 | MINOR  |
| `fix`      | Bug fix                     | PATCH  |
| `docs`     | Documentation only          | -      |
| `style`    | Formatting, no code change  | -      |
| `refactor` | Code change, no feature/fix | -      |
| `perf`     | Performance improvement     | -      |
| `test`     | Adding/fixing tests         | -      |
| `build`    | Build system, dependencies  | -      |
| `ci`       | CI configuration            | -      |
| `chore`    | Maintenance tasks           | -      |
| `revert`   | Revert previous commit      | -      |

### Breaking Changes

```
feat!: send email when product shipped

feat(api)!: change response format

chore!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

## Examples

### Simple Commits

```
feat: add user authentication
fix: resolve memory leak in cache
docs: update API documentation
style: format code with prettier
refactor: extract validation logic
perf: optimize database queries
test: add unit tests for auth module
build: upgrade webpack to v5
ci: add GitHub Actions workflow
chore: update dependencies
```

### With Scope

```
feat(auth): add OAuth2 support
fix(parser): handle empty arrays
docs(readme): add installation guide
refactor(api): simplify error handling
```

### With Body

```
fix: prevent request racing

Introduce a request id and reference to latest request.
Dismiss incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue
but are obsolete now.
```

### With Footer

```
fix: correct minor typos in code

Reviewed-by: John Doe
Refs: #123
```

### Breaking Change in Footer

```
feat: allow config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used
for extending other config files.
```

### Breaking Change with ! and Footer

```
chore!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

### Revert Commit

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

## Specification Rules

### MUST

1. Commits MUST be prefixed with a type (`feat`, `fix`, etc.)
2. Type MUST be followed by colon and space
3. Description MUST immediately follow the colon and space
4. `feat` MUST be used for new features
5. `fix` MUST be used for bug fixes
6. Breaking changes MUST be indicated by `!` before `:` OR `BREAKING CHANGE:` footer
7. `BREAKING CHANGE` MUST be uppercase
8. Footer token MUST use `-` instead of spaces (e.g., `Reviewed-by`)

### MAY

1. Scope MAY be provided after type: `feat(parser):`
2. Body MAY be provided after description (blank line between)
3. Footer MAY be provided after body (blank line between)
4. Types other than `feat` and `fix` MAY be used
5. `!` MAY be used with `BREAKING CHANGE:` footer

### Case Sensitivity

- Types: case-insensitive (lowercase recommended for consistency)
- `BREAKING CHANGE`: MUST be uppercase
- `BREAKING-CHANGE`: synonym for `BREAKING CHANGE`

## SemVer Mapping

| Commit Type              | SemVer Bump | Version Change |
| ------------------------ | ----------- | -------------- |
| `fix:`                   | PATCH       | 1.0.0 → 1.0.1  |
| `feat:`                  | MINOR       | 1.0.0 → 1.1.0  |
| `BREAKING CHANGE` or `!` | MAJOR       | 1.0.0 → 2.0.0  |

Breaking changes override type — `fix!:` results in MAJOR bump.

## Changelog Integration

Conventional Commits map directly to [changelog](../changelog/SKILL.md) entries:

| Commit Type       | Changelog Section            |
| ----------------- | ---------------------------- |
| `feat`            | Added                        |
| `fix`             | Fixed                        |
| `perf`            | Changed                      |
| `refactor`        | Changed                      |
| `docs`            | (usually omitted or Changed) |
| `BREAKING CHANGE` | Highlight in Changed/Removed |
| `revert`          | Removed or Fixed             |
| Security fixes    | Security                     |

### Automated Changelog Generation

Tools like `conventional-changelog`, `semantic-release`, or `release-please` can:

- Parse commit messages
- Generate CHANGELOG.md entries
- Determine next version number
- Create releases automatically

See [changelog skill](../changelog/SKILL.md) for CHANGELOG.md format.

## Common Patterns

### Feature Development

```bash
git commit -m "feat(users): add profile page"
git commit -m "feat(users): add avatar upload"
git commit -m "test(users): add profile page tests"
git commit -m "docs(users): document profile API"
```

### Bug Fix with Reference

```bash
git commit -m "fix(auth): resolve session timeout (#142)"
```

### Breaking Change Flow

```bash
# Deprecate first
git commit -m "feat(api): add v2 endpoint

DEPRECATED: /api/v1/users will be removed in next major version"

# Later, remove
git commit -m "feat(api)!: remove v1 endpoints

BREAKING CHANGE: /api/v1/* endpoints have been removed.
Use /api/v2/* instead."
```

## FAQ

### What if commit fits multiple types?

Split into multiple commits when possible. This makes history more organized.

### What if I used wrong type?

Before merge: `git rebase -i` to edit history.
After release: not critical — commit will be missed by automated tools.

### Do all contributors need to use this?

No. Use squash merging and maintainers can write proper message for the merge.

### How to handle reverts?

```
revert: <original commit subject>

Refs: <commit SHA>
```

## Git Configuration

### Commit Template

Set up git to use template:

```bash
git config commit.template .gitmessage
```

See [assets/commit-msg.template](assets/commit-msg.template) for template file.

### Pre-commit Validation

Use [assets/validate-commit-msg.sh](assets/validate-commit-msg.sh) with git hooks or CI.

## Tools

| Tool                                                                                       | Purpose                   |
| ------------------------------------------------------------------------------------------ | ------------------------- |
| [commitlint](https://commitlint.js.org/)                                                   | Lint commit messages      |
| [commitizen](https://commitizen-tools.github.io/commitizen/)                               | Interactive commit helper |
| [conventional-changelog](https://github.com/conventional-changelog/conventional-changelog) | Generate changelogs       |
| [semantic-release](https://semantic-release.gitbook.io/)                                   | Automated releases        |
| [release-please](https://github.com/googleapis/release-please)                             | GitHub release automation |

## Critical Prohibitions

- Do not use vague messages ("fix stuff", "update", "wip")
- Do not mix unrelated changes in single commit
- Do not omit breaking change indicators
- Do not use non-standard types without team agreement
- Do not forget blank line between description and body

## Agent Workflow for Commit Messages

**MANDATORY**: Before proposing branch name, commit message, or PR description, the agent MUST:

1. **Check all changed files** using `git status` or `git diff --name-only`
2. **Review actual changes** using `git diff` (staged and unstaged)
3. **Analyze ALL modifications** — not just the files mentioned in conversation
4. **Base proposals on complete changeset** — include all affected files, not partial list

### Workflow Steps

```bash
# Step 1: Get list of all changed files
git status --short

# Step 2: Review actual changes (for unstaged)
git diff

# Step 3: Review staged changes
git diff --staged

# Step 4: Use the complete changeset to propose:
#   - Branch name
#   - Commit message
#   - PR description
```

### Output Format

When user asks for commit message, provide:

1. **Branch name options** (3 variants using conventional prefixes)
2. **Commit message variants** (short/medium/detailed)
3. **PR description** (summarized, not duplicating full changelog)

All proposals MUST be based on the actual `git diff` output, not assumptions.

## Links

- Official specification: https://www.conventionalcommits.org/en/v1.0.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html
- Related: [changelog skill](../changelog/SKILL.md) — CHANGELOG.md format

## Templates

- [commit-msg.template](assets/commit-msg.template) — Git commit message template
- [validate-commit-msg.sh](assets/validate-commit-msg.sh) — Validation script
