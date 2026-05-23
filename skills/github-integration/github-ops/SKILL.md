---
name: github-ops
description: GitHub operations wrapper. Helps manage PRs, Issues, and Reviews efficiently via CLI.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read]
best_practices:
  - Use gh CLI for all operations
  - Restrict JSON output to relevant fields
  - Verify authentication before operations
error_handling: graceful
streaming: supported
---

# GitHub Ops Skill

## 🛠️ CLI Tools

We use `gh` (GitHub CLI) for all operations.

## 📋 Pull Requests

### Create PR

```bash
git push -u origin feature-branch
gh pr create --title "feat: description" --body "Summary of changes..."
```

### Checkout PR

```bash
gh pr checkout <number>
```

### Review PR

```bash
gh pr diff
gh pr review --approve
```

## 🐛 Issues

### List Issues

```bash
gh issue list --limit 5
```

### Create Issue

```bash
gh issue create --title "Bug: ..." --body "Reproduction steps..."
```

## 🤖 Context Optimization

Instead of dumping the entire JSON of an issue, use:

```bash
gh issue view <number> --json title,body,comments
```

This restricts the output to relevant fields only.

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
