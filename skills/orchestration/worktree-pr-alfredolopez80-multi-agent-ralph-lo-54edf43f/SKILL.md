---
# VERSION: 2.43.0
name: worktree-pr
description: Manage git worktrees with PR workflow and multi-agent review (Claude + Codex). Use when developing features in isolation with easy rollback.
triggers:
  - worktree
  - parallel development
  - pr review
  - isolated feature
  - git isolation
---

**ultrathink** - Take a deep breath. We're not here to write code. We're here to make a dent in the universe.

## The Vision
Isolation should make every change safer and more inevitable.

## Your Work, Step by Step
1. **Decide isolation**: Confirm if a worktree is needed.
2. **Create worktree**: One feature, one isolated workspace.
3. **Coordinate work**: Keep subagents aligned in one tree.
4. **Review & PR**: Multi-agent review before merge.
5. **Cleanup**: Merge or close with clean rollback.

## Ultrathink Principles in Practice
- **Think Different**: Use isolation to de-risk change.
- **Obsess Over Details**: Keep contexts and branches consistent.
- **Plan Like Da Vinci**: Map the PR flow before execution.
- **Craft, Don't Code**: Prefer small, clean diffs.
- **Iterate Relentlessly**: Fix and re-review until clean.
- **Simplify Ruthlessly**: Remove unnecessary branches.

# Git Worktree + PR Workflow (v2.20)

## Overview

This skill enables isolated feature development using git worktrees with a PR-based merge workflow and multi-agent code review.

**Key Principles:**
- **ONE worktree per feature/task** (not per subagent)
- Multiple subagents work in the **same** worktree
- Human-in-the-loop via `AskUserQuestion` for isolation decisions
- Easy rollback by closing PR and deleting worktree

## Prerequisites

- **WorkTrunk**: `brew install max-sixty/worktrunk/wt`
- **GitHub CLI**: `brew install gh`
- **Codex CLI**: For GPT-5 reviews

## Commands

| Command | Description |
|---------|-------------|
| `ralph worktree <task>` | Create isolated worktree + launch Claude |
| `ralph worktree-pr <branch>` | Create PR with Claude + Codex review |
| `ralph worktree-merge <pr>` | Approve and merge PR |
| `ralph worktree-fix <pr>` | Apply fixes from review comments |
| `ralph worktree-close <pr>` | Close PR and cleanup without merge |
| `ralph worktree-status` | Show all worktrees and PR status |
| `ralph worktree-cleanup` | Clean up merged worktrees |

## Workflow

### 1. Create Isolated Worktree

```bash
ralph worktree "implement oauth authentication"
# Creates: .worktrees/ai-ralph-20260103-implement-oauth-authentication/
# Branch: ai/ralph/20260103-implement-oauth-authentication
```

### 2. Develop Feature

All subagents work in the **same** worktree:
- Backend developer → `src/api/oauth.ts`
- Frontend developer → `src/ui/login.tsx`
- Test architect → `tests/oauth.test.ts`
- Docs writer → `docs/oauth.md`

Each subagent makes local commits but does NOT push.

### 3. Create PR with Multi-Agent Review

```bash
ralph worktree-pr ai/ralph/20260103-implement-oauth-authentication
```

This will:
1. Push branch to origin
2. Create draft PR
3. Get Claude Opus review (logic, edge cases, quality)
4. Get Codex GPT-5 review (security, performance)
5. Post reviews as PR comments
6. Show approval/rejection status

### 4. Handle Review Feedback

**If reviews pass:**
```bash
ralph worktree-merge <pr-number>
# Squash merges, deletes branch, cleans up worktree
```

**If reviews find issues:**
```bash
ralph worktree-fix <pr-number>
# Opens Claude in worktree with review comments as context
```

**If you want to abandon:**
```bash
ralph worktree-close <pr-number>
# Closes PR, deletes branch, cleans up worktree
```

## When to Use Worktrees

### Good Candidates
- New feature with multiple components
- Refactoring >5 files
- Experimental or risky changes
- Changes that may need rollback

### Not Needed
- Single-line hotfixes
- Documentation typo fixes
- Config adjustments
- Clear, simple tasks

## Orchestrator Integration

The orchestrator automatically asks about worktree isolation (Step 2b):

```yaml
AskUserQuestion:
  questions:
    - question: "¿Este cambio requiere un worktree aislado?"
      header: "Isolation"
      multiSelect: false
      options:
        - label: "Sí, crear worktree"
          description: "Feature nueva, refactor grande, cambio experimental"
        - label: "No, branch actual"
          description: "Hotfix, cambio menor, ajuste simple"
```

## Subagent Context

When working in a worktree, subagents receive:

```yaml
WORKTREE_CONTEXT:
  path: .worktrees/ai-ralph-YYYYMMDD-feature/
  branch: ai/ralph/YYYYMMDD-feature
  isolated: true
```

Subagent rules:
1. Work in the specified path
2. Make frequent local commits
3. **DO NOT push** - orchestrator manages PR
4. Coordinate with other subagents
5. Signal completion: `SUBAGENT_COMPLETE: [description]`

## Security

Each worktree has hardened security:
- Hooks disabled (`core.hooksPath → .git-hooks-disabled`)
- Credentials disabled per worktree
- Push configured for `current` branch only

## Example Session

```bash
# User request: "Add OAuth authentication"

# Orchestrator asks about worktree
> ¿Este cambio requiere un worktree aislado?
> [Sí, crear worktree] ← User selects

# Create worktree
$ ralph worktree "oauth-authentication"
✓ Created worktree: .worktrees/ai-ralph-20260103-oauth-authentication
✓ Branch: ai/ralph/20260103-oauth-authentication
✓ Security hardening applied

# Subagents work in parallel in SAME worktree
# ... backend, frontend, tests, docs ...

# All subagents complete
# Orchestrator creates PR with review
$ ralph worktree-pr ai/ralph/20260103-oauth-authentication
✓ Pushed to origin
✓ Created PR #42
✓ Claude review: APPROVED
✓ Codex review: APPROVED with suggestions

# User decides to merge
$ ralph worktree-merge 42
✓ PR #42 merged (squash)
✓ Branch deleted
✓ Worktree cleaned up
```

## Troubleshooting

### WorkTrunk not found
```bash
brew install max-sixty/worktrunk/wt
wt config shell install
source ~/.zshrc
```

### PR creation fails
```bash
gh auth status  # Verify GitHub auth
gh auth login   # Re-authenticate if needed
```

### Worktree conflicts
```bash
git worktree prune  # Clean orphaned metadata
ralph worktree-status  # Check current state
```
