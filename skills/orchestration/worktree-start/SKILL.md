---
name: worktree-start
description: Create a git worktree for isolated parallel feature development. Lighter than fork-project — shares git history but zero .git contention between agents. Use when the user wants to start a feature in its own isolated workspace with separate agent sessions.
disable-model-invocation: true
allowed-tools:
  - Bash
---

# Worktree Start

Creates a lightweight isolated workspace using `git worktree`. Ideal for running 4-5 features in parallel, each managed by an independent agent session, without the disk overhead of a full clone.

## What it does

1. **Guards** `.worktrees/` is in `.gitignore` (adds and commits if missing)
2. **Creates** a worktree at `.worktrees/<feature-name>` on branch `work/<feature-name>`
3. **Installs** dependencies (auto-detects pnpm / yarn / npm / cargo / pip)
4. **Runs** a baseline check to confirm the clean starting state
5. **Reports** the path and next steps

## Usage

```
/worktree-start <feature-name>
```

## How to execute

```bash
bash .claude/skills/worktree-start/scripts/worktree-start.sh "<feature-name>"
```

## Important

- Worktrees live inside the project at `.worktrees/<feature-name>` — no sibling directories
- Each worktree has its **own index file** (no git contention between parallel agents)
- Branch naming follows the same convention as `fork-project`: `work/<feature-name>`
- The `.worktrees/` dir is gitignored so worktree contents are never tracked
- Always inform the user of the full path so they can open their agent session there
- Pairs with `/worktree-finish` to merge back and clean up
