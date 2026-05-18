# Skill examples

Concrete examples demonstrating skill patterns and new features.

---

## Example 1: minimal skill

The simplest possible skill:

```yaml
---
description: Formats code following project conventions. Use when user wants to format, lint, or clean up code.
---
```

```markdown
# Code formatter

Run the project formatter on changed files.

## Workflow

1. Detect project type and formatter
2. Run formatter on staged/changed files
3. Report results

## Important rules

- **ALWAYS** check for project-specific formatter config before using defaults
- **NEVER** format files outside the current change set
```

Note: `name` is omitted (defaults to directory name). Only `description` is provided.

---

## Example 2: dynamic context injection

A skill that adapts to the current project:

```yaml
---
name: git-commit
description: Creates commits following project conventions. Use when user wants to commit changes.
---
```

```markdown
# Git commit

## Recent project commits
!`git log --oneline -5 2>/dev/null`

## Current branch
!`git rev-parse --abbrev-ref HEAD 2>/dev/null`

Match the style of recent commits above when creating new ones.
```

The `!`command`` directives run at load time and inject their output, so Claude sees actual commit history instead of placeholder text.

---

## Example 3: invocation control

### Manual-only skill (no auto-invocation)

```yaml
---
name: deploy
description: Deploy the application to production.
disable-model-invocation: true
argument-hint: [environment]
---
```

Claude will never auto-invoke this skill. Users must type `/deploy staging` explicitly.

### Background knowledge (no user invocation)

```yaml
---
name: project-conventions
description: Project coding conventions and architectural decisions.
user-invocable: false
---
```

Claude auto-loads this as context when relevant, but it doesn't appear in the `/` menu.

---

## Example 4: subagent execution

A skill that runs in isolated context:

```yaml
---
name: codebase-analysis
description: Analyze codebase architecture and patterns. Use when user wants to understand code structure.
context: fork
agent: Explore
---
```

```markdown
# Codebase analysis

Explore the codebase and report:
1. Project structure and framework
2. Key architectural patterns
3. Entry points and data flow
4. Test coverage approach

Return a structured summary.
```

With `context: fork`, this runs in a separate subagent without consuming the main conversation's context.

---

## Example 5: skill with arguments

```yaml
---
name: fix-issue
description: Fix a GitHub issue. Use when user wants to fix, resolve, or address an issue.
argument-hint: [issue-number]
---
```

```markdown
# Fix issue

## Issue details
!`gh issue view $1 --json title,body,labels 2>/dev/null`

Fix the issue described above. Follow project conventions.
```

`$1` is replaced with the first argument when the user types `/fix-issue 42`.

---

## Example 6: skill with allowed tools

```yaml
---
name: database-migration
description: Create and run database migrations. Use when user wants to migrate, create migration, or update schema.
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---
```

Tools listed in `allowed-tools` won't prompt for permission when this skill is active.

---

## Description: good vs bad

**Good** - concise, specific triggers, clear capabilities:
```
Handles PR review comments with severity classification. Use when user
wants to resolve PR comments, handle review feedback, or fix review
comments. Fetches via GitHub CLI, classifies by severity, proposes fixes.
```

**Bad** - verbose, filler words, redundant:
```
Comprehensive GitHub Pull Request management system for feature
development workflow. Use this skill when the user wants to create, verify,
or manage Pull Requests on GitHub repositories. This skill handles the
complete workflow - validates task completion against project documentation,
runs tests, generates PR title and description following Conventional Commits,
suggests appropriate labels, and creates the PR using GitHub CLI.
```

Problems: "Comprehensive", "complete workflow" are filler. Redundant explanations. Too verbose for a description field.

---

## Resource organization examples

### Scripts that add value

| Script | Why it's justified |
|--------|-------------------|
| `scripts/classify_severity.py` | Complex multi-step classification with JSON output |
| `scripts/analyze_commits.py` | Git log parsing + task file matching across multiple files |
| `scripts/validate_skill.py` | Multi-field validation with structured error reporting |

### Scripts to avoid

| Script | Why it's bad | Instead |
|--------|-------------|---------|
| `scripts/fetch_comments.sh` | Wraps `gh api repos/.../comments` | Inline command |
| `scripts/run_tests.sh` | Wraps `make test` | Inline command |
| `scripts/get_branch.sh` | Wraps `git rev-parse --abbrev-ref HEAD` | Inline command |
