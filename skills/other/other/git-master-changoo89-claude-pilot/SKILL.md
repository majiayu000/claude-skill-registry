---
name: git-master
description: Git workflow mastery - staging, committing, branching, PR creation. Apply conventional commits, Co-Authored-By attribution. Only create commits when user explicitly requests.
---

# SKILL: Git Master (Version Control Workflow)

> **Purpose**: Execute Git operations with best practices - commits, branches, PRs
> **Target**: Coder Agent after completing implementation

---

## Quick Start

### When to Use This Skill
- Stage and commit changes
- Create feature branches
- Create pull requests

### Quick Reference
```bash
# Stage and commit (ONLY when user requests)
git status && git diff && git add <files>
git commit -m "feat(scope): description\n\nCo-Authored-By: Claude <noreply@anthropic.com>"

# Create PR: gh pr create --title "Title" --body "Description"
```

---

## What This Skill Covers

### In Scope
- Git staging and committing (on user request)
- Conventional commit messages
- Co-Authored-By attribution
- Branch creation and PR creation

### Out of Scope
- Force pushes to main/master
- Git configuration changes
- Repository initialization

---

## Core Principles

### Commit ONLY When Requested

**CRITICAL**: Never create commits unless user explicitly asks.

**User requests commit**: `/commit`, "Create a commit", "Commit these changes", "Make a commit for this work"
**NOT requests**: "Fix this bug", "Add feature X", `/03_close`

### Conventional Commits

Format: `type(scope): description`

**Types**: feat, fix, refactor, chore, docs, style, test

### Co-Authored-By Attribution

Always include:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Integrated Skills

This skill integrates the following specialized git skills:

- **git-operations**: Push/pull/merge with retry logic and error handling
- **using-git-worktrees**: Parallel development in isolated workspaces

## Further Reading

**Internal**: @.claude/skills/git-master/REFERENCE.md - Advanced Git patterns, branch strategies, collaboration | @.claude/skills/git-operations/SKILL.md - Safe push/pull/merge operations | @.claude/skills/using-git-worktrees/SKILL.md - Parallel development with worktrees | @.claude/skills/tdd/SKILL.md - Red-Green-Refactor cycle | @.claude/skills/ralph-loop/SKILL.md - Autonomous completion loop | @.claude/skills/vibe-coding/SKILL.md - Code quality standards

**External**: [Conventional Commits](https://www.conventionalcommits.org/) | [GitHub CLI](https://cli.github.com/manual/gh_pr_create)
