---
name: github-pull-request
description: |
  Generate GitHub pull request descriptions following repository templates.
  Use when creating PRs to communicate changes, impact, and value.
  Triggers: "create pr", "pull request", "pr description", "github pr".
license: MIT
metadata:
  author: KemingHe
  version: "3.0.0"
---

# GitHub Pull Request Generation

Generate pull request descriptions that communicate changes, impact, and value following project templates.

**Temporary persona**: Senior engineering manager with expertise in code review and technical documentation.

## When to Use This Skill

- Creating a pull request description for branch changes
- Documenting changes for code review
- Communicating technical decisions and business value
- Following repository PR conventions

## Template Resolution

1. Search `.github/pull_request_template.md` for PR template
2. If not found, search `**/pull_request_template.md` across repository
3. If still not found, ask user for template or use minimal structure

## Git Operations (Read-Only)

This skill performs read-only reconnaissance. Never modify repository state.

**Setup**: Navigate to repository root. Pipe all git commands to `cat` to avoid interactive mode or pager.

**Safe commands**:

```shell
git status | cat                              # Current repository state
git log origin/main..HEAD --oneline | cat     # Commits on this branch
git diff origin/main...HEAD --stat | cat      # Summary of changes vs main
git diff origin/main...HEAD | cat             # Detailed changes vs main
git show --name-only HEAD | cat               # Files changed in latest commit
git branch -a | cat                           # All branches
```

**Forbidden operations**: Never use git commit, push, pull, merge, rebase, add, reset, clean, or stash.

**Prefer remote tools**: Use GitHub/GitLab MCP tools when available for related issues, PRs, and branch history.

## Process

### Step 1: Analyze Branch

- Search for pull_request_template.md in repository
- Run safe git operations (with `| cat`) to understand changes
- Use MCP tools for context:
  - Search related issues and PRs
  - Analyze affected functionality and dependencies
  - Identify architectural patterns impacted

### Step 2: Classify and Consult User

Determine PR type and generate title:

| Type | When to Use |
| :--- | :--- |
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change, no feature/fix |
| `chore` | Maintenance, dependencies |

Generate title: `type(scope): brief description` - max 50 characters, imperative mood

Present change summary and ask:

- Confirm scope and key areas of change?
- Which issues does this resolve?
- Business motivation and testing approach?
- Breaking changes or review considerations?

### Step 3: Generate PR Description

- Use template as minimum structure, enrich with critical details
- Include conventional commit-style title
- Use dash bullets, each conveying unique information
- Apply KISS and DRY: no fluff, but capture all information reviewers need
- Group changes by feature area, impact level, or architectural component

**Enrichment guidance**:

- Changes: Describe what changed and why, not just file names
- Impact: Clarify user-facing effects, performance implications, breaking changes
- Notes: Include merge dependencies, testing considerations, rollback plan if relevant
- Connect technical changes to business value

## Change Categorization

Choose appropriate grouping for changes:

- Feature area: Specific modules, functionality, user-facing features
- Impact level: Critical fixes, performance, minor updates
- Architectural component: Database schemas, APIs, system integrations
- Combined: Mix categories for better clarity

## Output Format

Present final PR description in markdown code block:

```markdown
type(scope): brief description

[complete PR description following template structure]
```

## Constraints

- **Title**: Max 50 characters, imperative mood, conventional commit format
- **Template as scaffold**: Use discovered templates as minimum structure, enrich appropriately
- **Comprehensive analysis**: Use git commands, MCP tools, codebase search
- **KISS and DRY**: Each bullet provides unique, concise information - no fluff
- **Business context**: Connect technical changes to business value
- **Issue linking**: Use separate "closes #X" for each resolved issue
- **Characters**: QWERTY keyboard typeable only - no em-dashes, smart quotes, emojis, or special Unicode

---

> GitHub Pull Request Generation Skill v3.0.0 - KemingHe/common-devx
