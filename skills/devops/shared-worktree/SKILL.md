---
name: shared-worktree
description: Git worktree setup and management for parallel agent development. Use when working in isolated git worktrees to avoid merge conflicts between Developer and Tech Artist agents.
category: workflow
---

# Worker Worktree Skill

> "Parallel development without conflicts – each agent works in their own worktree."

## Verification Checklist

Before starting work:

- [ ] Worktree exists (`git worktree list` shows your worktree)
- [ ] In worktree directory (`pwd` shows `../{agent}-worktree`)
- [ ] On correct branch (`git branch` shows `{agent}-worktree`)
- [ ] Main branch merged (`git merge origin/main` completed)
- [ ] No merge conflicts (`git status` is clean)
- [ ] Latest changes pulled (`git log` shows recent main commits)

## Quick Reference Commands

| Action               | Command                                                    |
| -------------------- | ---------------------------------------------------------- |
| List worktrees       | `git worktree list`                                        |
| Create worktree      | `git worktree add ../{agent}-worktree -b {agent}-worktree` |
| Remove worktree      | `git worktree remove ../{agent}-worktree`                  |
| Navigate to worktree | `cd ../{agent}-worktree`                                   |
| Merge main           | `git fetch origin main && git merge origin/main`           |
| Push worktree        | `git push origin {agent}-worktree`                         |
| Check current branch | `git branch --show-current`                                |

## Worktree Naming Convention

**MUST follow this pattern:** `{agent}-worktree`

| Agent       | Worktree Name         | Worktree Path            | Branch Name           |
| ----------- | --------------------- | ------------------------ | --------------------- |
| Developer   | `developer-worktree`  | `../developer-worktree`  | `developer-worktree`  |
| Tech Artist | `techartist-worktree` | `../techartist-worktree` | `techartist-worktree` |

## Initial Setup (One-Time Per Agent)

```bash
# Check if worktree already exists
git worktree list

# If NOT in list, create worktree with dedicated branch
git worktree add ../{agent}-worktree -b {agent}-worktree

# Verify creation
git worktree list
```

## Daily Workflow

### Before Starting ANY Task

**⚠️ CRITICAL: You MUST navigate to your worktree BEFORE doing any development work!**

**Why navigate to worktree first?**

- All code/asset edits MUST happen in worktree
- Commits go to worktree branch, NOT main
- QA validates from worktree, then merges to main
- Prevents file conflicts between parallel agents

**Why merge main first?**

- Ensures you have the latest changes from the other agent's work
- Prevents out-of-date code conflicts
- Both agents' work gets integrated through main

## Unit, E2E, and Playwright MCP Testing Protocol

Remember to always run the tests in the target worktree branches for validation

- Move to the target worktree
- Load the correct skills for this scope
- Run validation process
- During validation process, always double check in which port the client is running for proper URL check
- Investigate in case of issues and iterate until fixed

1. Developer in worktree:
   ├── Reads PRD from master (Get-MasterPrdPath)
   ├── Reads messages from master (Get-MasterMessageQueuePath)
   ├── Updates PRD status in master (atomic write)
   ├── Sends messages to master queue
   ├── Writes code in worktree (src/)
   ├── Commits code to worktree branch
   └── Sends validation_request via master queue

2. PM in master:
   ├── Reads PRD (sees worker status updates)
   ├── Reads messages (sees worker messages)
   └── Coordinates everything

3. QA in master:
   ├── Navigates to worktree for testing
   ├── If validation passes: merges to master
   └── If validation fails: sends bug_report via master queue
