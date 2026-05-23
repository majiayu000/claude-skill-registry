---
name: worktree
description: Create and manage git worktrees for parallel agent sessions
model: opus
---

# Worktree Management

Manage git worktrees for parallel Claude Code sessions and subagent dispatch.

## Commands

| Command | Usage | Purpose |
|---------|-------|---------|
| `/worktree create <slug>` | Create a new worktree | Isolated workspace for parallel work |
| `/worktree list` | List active worktrees | See what's running |
| `/worktree merge <slug>` | Merge and clean up | Bring work back to main |
| `/worktree cleanup <slug>` | Remove without merging | Abandon a worktree |

## Execution

All commands delegate to `.claude/scripts/worktree-manager.sh`:

```bash
.claude/scripts/worktree-manager.sh <command> [slug]
```

**IMPORTANT:** The script operates on the vault root. Always run from the vault directory. Use `dangerouslyDisableSandbox: true` because worktrees are created outside the vault directory (sibling path).

## Slug Rules

- Lowercase alphanumeric with hyphens: `meeting-notes-batch`, `architecture-review`
- Becomes the branch name: `worktree/<slug>`
- Becomes the directory name: `../<vault>-worktrees/<slug>/`

## Dispatching Subagents to Worktrees

After creating a worktree, dispatch subagents with the worktree path as their working directory:

```
1. Create worktree: /worktree create meeting-notes-batch
2. Note the path from output (e.g. /Users/.../BA-DavidOliver-ObsidianVault-worktrees/meeting-notes-batch)
3. Dispatch subagent with Task tool, including in the prompt:
   "Work in /Users/.../BA-DavidOliver-ObsidianVault-worktrees/meeting-notes-batch"
4. When subagent completes: /worktree merge meeting-notes-batch
```

## Multi-Session Usage

For separate Claude Code terminals working in parallel:

1. Session A: `/worktree create feature-alpha` → opens terminal in worktree path
2. Session B: `/worktree create feature-beta` → opens terminal in worktree path
3. Each session works independently
4. When done: `/worktree merge feature-alpha` (from the main vault session)

## Conventions

- **Branch naming:** `worktree/<slug>` — visually distinct in git log
- **Merge strategy:** `--no-ff` for clean merge commits
- **Config copied:** `.claude/` and `.mcp.json` are copied to each worktree
- **Not copied:** `.obsidian/` — worktrees are agent workspaces, not Obsidian vaults
- **Location:** Sibling directory `../<vault>-worktrees/<slug>/` (outside vault, invisible to Obsidian)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "slug required" | Provide a slug: `/worktree create my-task` |
| Merge conflicts | Resolve manually in main, then `git worktree remove` |
| Sandbox blocks worktree creation | Use `dangerouslyDisableSandbox: true` |
| Worktree already exists | Idempotent — reuses existing worktree |
