---
name: git
description: Basic git operations for repository inspection. Use for git diff, git log, git status, git remote, and other read-only git commands.
---

# Git CLI

## Purpose

This skill provides access to basic git commands for inspecting repository state. Use this for read-only operations like viewing diffs, logs, and status.

## Command Reference

### Repository State
| Action | Command |
|--------|---------|
| Status | `git status` |
| Remote URLs | `git remote -v` |
| Current branch | `git branch --show-current` |
| All branches | `git branch -a` |

### Viewing Changes
| Action | Command |
|--------|---------|
| Unstaged changes | `git diff` |
| Staged changes | `git diff --cached` |
| All changes | `git diff HEAD` |
| Changes vs branch | `git diff <branch>...HEAD` |
| Changed files only | `git diff --name-only` |
| Stat summary | `git diff --stat` |

### History
| Action | Command |
|--------|---------|
| Recent commits | `git log --oneline -n 10` |
| Branch commits | `git log main..HEAD --oneline` |
| Commit details | `git log -1 --format=full` |
| File history | `git log --oneline -- <file>` |
| Blame | `git blame <file>` |

### Inspection
| Action | Command |
|--------|---------|
| Show commit | `git show <commit>` |
| Show file at commit | `git show <commit>:<file>` |
| List tracked files | `git ls-files` |

## Behavioral Guidelines

1. **Read-only**: This skill is for inspection only, not for making changes
2. **Prefer short output**: Use `--oneline`, `--stat`, or `-n` flags to limit output
3. **Branch detection**: Use `git branch --show-current` to identify the current branch
4. **Platform detection**: Use `git remote -v` to determine if GitHub or GitLab, then use the appropriate skill
