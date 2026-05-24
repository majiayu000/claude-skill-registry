---
name: bl-stack
description: Manage git-branchless commit stacks - view, navigate, and edit commits
argument-hint: "[show|prev|next|amend|reword|restack]"
---

# /bl-stack - Git-Branchless Stack Management

**Category:** Git Workflow

Manage commit stacks using git-branchless. View your stack, navigate between commits, and edit any commit in the stack with automatic restacking.

## Usage

```
/bl-stack [action] [options]
```

## Actions

| Action | Description |
|--------|-------------|
| `show` | Display the commit stack (default) |
| `prev [N]` | Move to parent commit (N commits up) |
| `next [N]` | Move to child commit (N commits down) |
| `amend` | Amend current commit + restack descendants |
| `reword` | Change commit message + restack descendants |
| `restack` | Rebase descendants onto amended commit |
| `reorder` | Interactive rebase to reorder/squash commits |

## Examples

```bash
# View current stack
/bl-stack
/bl-stack show

# Navigate
/bl-stack prev      # Go up one commit
/bl-stack prev 2    # Go up two commits
/bl-stack next      # Go down one commit

# Edit commits
/bl-stack amend     # After making changes, amend current commit
/bl-stack reword    # Change current commit's message

# Reorganize
/bl-stack reorder   # Interactive rebase (pick, squash, drop, reorder)
/bl-stack restack   # Fix abandoned commits after manual amend
```

## Execution

This command delegates to the `bl-stack-expert` agent:

```
Task(subagent_type="git-workflow:bl-stack-expert",
     prompt="Execute stack operation: <action>")
```

## Execution Instructions

1. **Verify Prerequisites**
   - Check git-branchless is installed
   - Check repository is initialized for branchless

2. **Show Current State**
   - Run `git sl` to display the stack
   - Explain smartlog icons (◆ ◯ ● ✕)

3. **Execute Action**
   - For `show`: Display and explain the stack
   - For `prev/next`: Navigate and confirm position
   - For `amend`: Stage changes and run `git amend`
   - For `reword`: Open editor for message change
   - For `restack`: Rebase descendants onto current commit
   - For `reorder`: Run `git rebase -i main`

4. **Confirm Result**
   - Show final state with `git sl`

## Interactive Flow

```
User: /bl-stack

Agent: Showing your commit stack...

◆ abc1234 (main) initial commit
┃
◯ def5678 feat: add User class
┃
◯ ghi9012 feat: add validation
┃
● jkl3456 feat: add repository

Stack has 3 draft commits (◯) above main (◆).
You are at: feat: add repository (● = current position)

Commands:
- /bl-stack prev   : Go to "feat: add validation"
- /bl-stack amend  : Amend current commit
- /bl-stack reword : Change commit message
```

```
User: /bl-stack prev 2

Agent: Navigating up 2 commits...

◆ abc1234 (main) initial commit
┃
● def5678 feat: add User class  ← You are now here
┃
◯ ghi9012 feat: add validation
┃
◯ jkl3456 feat: add repository

Moved from "feat: add repository" to "feat: add User class"
```

```
User: /bl-stack amend

Agent: Amending current commit...

Changes staged:
  M src/user.py (+15 lines)

Running git amend...
Restacking 2 descendant commits...

◆ abc1234 (main) initial commit
┃
● xyz9999 feat: add User class  ← Amended
┃
◯ abc1111 feat: add validation  ← Restacked
┃
◯ def2222 feat: add repository  ← Restacked

Commit amended and stack updated.
```

## Error Handling

| Error | Resolution |
|-------|------------|
| git-branchless not installed | Provide installation command |
| Not a git repository | Inform user |
| Repo not initialized | Suggest `git branchless init` |
| Dirty working directory | Prompt to commit or stash |
| Conflicts during restack | Guide through resolution |
