---
name: restore
description: Resume work after a crash or new session with safety constraints
---

When the user invokes /resume, follow these steps in order:

## 1. Check for Stale State
- List team directories: `ls ~/.claude/teams/` — report any existing teams
- List git worktrees: `git worktree list` — report any worktrees beyond the main one
- Check for stale tmux panes with dead agent sessions

## 2. Clean Up (with user confirmation)
- If stale teams exist, ask user before removing: `rm -rf ~/.claude/teams/<stale-team>/`
- If orphaned worktrees exist, ask user before pruning: `git worktree remove <path>`
- Never auto-clean without user confirmation

## 3. Read Last Checkpoint
- Check `.claude/checkpoints/` for the most recent JSON checkpoint file
- If found, display: timestamp, branch, tasks completed, tasks remaining
- If no checkpoints exist, note this and proceed

## 4. Search Cross-Session Memory
- Use claude-mem search to find recent session context for this project
- Display relevant observations from the last session

## 5. Check Linear Status
- List incomplete Linear tickets for the current project
- Show any in-progress tickets that may need resuming

## 6. Report Summary
Before spawning any agents, present a clear summary:
- What was cleaned up
- Last known checkpoint state
- Recommended next action
- HARD LIMIT reminder: max 3 concurrent agents

## 7. Ask User
Ask the user which task to resume or start next. Do NOT proceed autonomously.
