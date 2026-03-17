---
name: commit-message-creation
description: |
  Generate conventional commit messages following project standards.
  Use when staging changes need a commit message or reviewing commit history.
  Triggers: "commit message", "git commit", "conventional commit", "commit msg".
license: MIT
metadata:
  author: KemingHe
  version: "3.0.0"
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

**Prefer remote tools**: Use GitHub/GitLab MCP tools when available for issues, PRs (GitHub) / MRs (GitLab), and branch analysis.

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
- Related issues or PRs (GitHub) / MRs (GitLab)

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

## General Doc Constraints

Apply to all generated output. If a discovered template deviates from any rule (e.g., uses emojis semantically, uses a different bullet convention), note the deviation explicitly and confirm with the user before treating it as a permitted exception.

- **Characters**: QWERTY keyboard typeable only - no smart quotes, emojis, or special Unicode anywhere. In prose, do not use em-dashes or em-dash substitutes (`--`, ` -- `); use ` - ` (space-dash-space) for clause separation instead. Exception: `↑` for ToC navigation.
- **Inline formatting**: Use `_underscore_` for italics, not `*single-star*`. Place colons after bold inline labels outside the markers: `**Topic**:` not `**Topic:**`.
- **Bullets**: Use `-` for all unordered lists; one bullet per complete thought; never wrap a bullet's content mid-sentence onto a continuation line - split into separate bullets if too long or multi-thought. Nested sub-bullets for component grouping are permitted. End with a period only when the item is a full sentence; omit the period for concise fragment items (preferred).
- **Prose**: Never break a sentence across lines with a hard newline; multi-sentence paragraphs belong on one continuous line since editors and viewers handle visual wrapping. Exception: commit message bodies use one sentence per line for `git log` readability.
- **Template hygiene**: Delete `(optional)` and any parenthetical conditional label (e.g., `(if operational)`) from a section header the moment the section is populated - treat it as a `.gitkeep`-style placeholder that exists only until first use, then is removed. Omit the entire section (header and body) when unused. Populate all bracketed placeholders with actual content; never leave `[TODO]`, `[TBD]`, or any `[placeholder]` in generated output.
- **Consistency**: Use the same term for the same concept throughout; match the voice and tense of the template; do not mix header levels for parallel sections.
- **KISS and DRY**: Each section and bullet conveys unique information - no redundancy or overlap.

> General Doc Constraints v1.1.0 - KemingHe/common-devx

## Skill Constraints

- **Title**: Max 50 characters, imperative mood
- **Plaintext only**: No markdown formatting (no `**bold**`, `_italic_`, `` `code` ``, links). Use dashes and indents for structure
- **Completeness**: Capture all significant changes
- **Sections**: Include only sections with meaningful content
- **Issue linking**: Use separate "closes #X" for each resolved issue

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
