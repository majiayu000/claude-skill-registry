---
name: commit-message
description: |
  Generate conventional commit messages following project standards.
  Use when staging changes need a commit message or reviewing commit history.
  Triggers: "commit message", "git commit", "conventional commit", "commit msg".
license: MIT
metadata:
  author: KemingHe
  version: "2.0.0"
---

# Commit Message Generation

Generate conventional commit messages by analyzing staged changes and repository context.

**Temporary persona**: Senior engineering manager with expertise in conventional commits and version control best practices.

## When to Use This Skill

- Writing a commit message for staged changes
- Ensuring commit messages follow conventional commit standards
- Reviewing and improving existing commit messages

## Asset Resolution

1. Check `./assets/commit-template-long.md` for full commit format
2. Check `./assets/commit-template-short.md` for minimal commit format
3. If not found, search `**/commit-template-*.md` in repository

## Git Operations (Read-Only)

This skill performs read-only reconnaissance. Never modify repository state.

**Setup**: Navigate to repository root. Pipe all git commands to `cat` to avoid interactive mode or pager.

**Safe commands**:

```shell
git status | cat                  # Current repository state
git diff | cat                    # Unstaged changes
git diff --staged | cat           # Staged changes ready for commit
git log --oneline -10 | cat       # Recent commit history for style
git log origin/main..HEAD | cat   # Commits not yet pushed
git branch -a | cat               # All branches
```

**Forbidden operations**: Never use git commit, push, pull, merge, rebase, add, reset, clean, or stash.

**Prefer remote tools**: Use GitHub/GitLab MCP tools when available for issues, PRs, and branch analysis.

## Process

### Step 1: Analyze Changes

Run safe git operations (with `| cat`) to understand staged changes:

```shell
git status | cat                  # Current repository state
git diff --staged | cat           # Staged changes ready for commit
git log --oneline -10 | cat       # Recent commit history for style
```

Use MCP tools for deeper analysis:

- Codebase search for related files and patterns
- File reading for context on affected components
- Issue/PR search for related work

Identify:

- Affected components and scope
- Type of change (feat, fix, docs, etc.)
- Patterns from recent commits
- Related issues or PRs

### Step 2: Classify and Generate Title

Determine commit type:

| Type | When to Use |
| :--- | :--- |
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `test` | Adding or updating tests |
| `chore` | Maintenance, dependencies |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |
| `build` | Build system changes |

Generate title:

- Format: `type(scope): brief description`
- Max 50 characters
- Imperative mood ("add", "fix", "update")

### Step 3: Consult User

Present analysis and ask:

- Specific areas to emphasize?
- Issues this commit resolves?
- Additional context or concerns?

### Step 4: Generate Message

Use appropriate template based on complexity:

- **Simple changes**: Use `commit-template-short.md`
- **Complex changes**: Use `commit-template-long.md`

## Output Format

Present final commit message in plaintext code block:

```plaintext
type(scope): brief description in imperative mood

[body content per template]
```

## Constraints

- **Title**: Max 50 characters, imperative mood
- **Plaintext only**: No markdown formatting (no `**bold**`, `_italic_`, `` `code` ``, links). Use dashes and indents for structure
- **Completeness**: Capture all significant changes
- **KISS and DRY**: Each bullet conveys unique information
- **Sections**: Include only sections with meaningful content
- **Issue linking**: Use separate "closes #X" for each resolved issue
- **Characters**: QWERTY keyboard typeable only - no em-dashes, smart quotes, emojis, or special Unicode

## Examples

### Simple Feature

```plaintext
feat(auth): add JWT token refresh mechanism

CHANGES
- Implement automatic token refresh on expiration
- Add refresh token storage to session management

IMPACT
- Users stay logged in longer without interruption
```

### Bug Fix with Issue

```plaintext
fix(api): resolve race condition in user data fetching

closes #245

CHANGES
- Add mutex lock to prevent concurrent requests
- Implement request deduplication

BREAKING CHANGES
- UserService.getData() now returns Promise<UserData>
```

---

> Commit Message Generation Skill v2.0.0 - KemingHe/common-devx
