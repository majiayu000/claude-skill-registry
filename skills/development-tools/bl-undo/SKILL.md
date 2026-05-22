---
name: bl-undo
description: Undo git-branchless operations - recover from mistakes interactively
argument-hint: "[-i] [--hide <hash>] [--unhide <hash>]"
---

# /bl-undo - Git-Branchless Undo & Recovery

**Category:** Git Workflow

Recover from mistakes using git-branchless's powerful undo system. Browse repository history and restore previous states.

## Usage

```
/bl-undo [options]
```

## Options

| Option | Description |
|--------|-------------|
| (none) | Quick undo of last operation |
| `-i` | Interactive mode - browse history |
| `--hide <hash>` | Hide a commit from smartlog |
| `--unhide <hash>` | Restore a hidden commit |

## Examples

```bash
# Undo the last operation
/bl-undo

# Interactive undo - browse and select state
/bl-undo -i

# Hide an experimental commit
/bl-undo --hide abc1234

# Restore a hidden commit
/bl-undo --unhide abc1234
```

## What Can Be Undone

- Commits and amended commits
- Rebases and merges
- Branch creations, moves, deletions
- Checkouts

## What Cannot Be Undone

- Uncommitted file changes
- Untracked file changes
- Pushed commits (remote changes)

## Execution

This command delegates to the `bl-undo-expert` agent:

```
Task(subagent_type="git-workflow:bl-undo-expert",
     prompt="Execute undo: <options>")
```

## Execution Instructions

1. **Assess Situation**
   - Show current state with `git sl`
   - Identify what might need undoing

2. **Execute Undo**
   - For quick: Run `git undo`, confirm
   - For interactive: Run `git undo -i`, guide navigation
   - For hide/unhide: Run respective command

3. **Verify Result**
   - Show final state with `git sl`
   - Confirm expected commits are present

## Interactive Flow

```
User: /bl-undo

Agent: Checking last operation...

Last operation: git rebase -i main
  - Dropped: "feat: add OAuth"
  - Reordered: 2 commits

This will restore:
◆ abc1234 (main) initial commit
┃
◯ def5678 feat: add auth base
┃
◯ ghi9012 feat: add OAuth       ← Will be restored
┃
◯ jkl3456 feat: add Google login
┃
● mno7890 feat: add GitHub login

Undo this operation? [y/n]:
```

```
User: /bl-undo -i

Agent: Opening interactive undo...

git undo -i

This opens a browser interface. Use:
  ← → arrow keys to navigate through time
  Each state shows the smartlog at that point
  Find the state BEFORE your mistake
  Press Enter to select, then y to confirm

[User navigates in terminal]

After user confirms...

◆ abc1234 (main) initial commit
┃
◯ def5678 feat: add User class
┃
◯ ghi9012 feat: add validation
┃
● jkl3456 feat: add repository

Restored to state before the bad rebase.
All 3 commits recovered.
```

```
User: /bl-undo --hide abc1234

Agent: Hiding commit abc1234...

Before:
◆ main initial commit
┃
◯ abc1234 feat: experimental  ← Will be hidden
┃
◯ def5678 feat: add User class
┃
● ghi9012 feat: add validation

git hide abc1234

After:
◆ main initial commit
┃
◯ def5678 feat: add User class
┃
● ghi9012 feat: add validation

Commit hidden from smartlog.

⚠️  Warning: Hidden commits may be garbage collected.
To restore later: /bl-undo --unhide abc1234
```

## Common Recovery Scenarios

### Bad Rebase Removed Commits
```
User: I accidentally dropped a commit during rebase!

Agent: Let's recover it with interactive undo...
/bl-undo -i
Navigate to state before the rebase, select, confirm.
```

### Wrong Commit Amended
```
User: I amended the wrong commit!

Agent: Quick undo will restore it...
/bl-undo
Confirm to restore pre-amend state.
```

### Stack Got Messed Up
```
User: My stack is completely messed up after multiple operations

Agent: Interactive undo can go back multiple operations...
/bl-undo -i
Navigate back to when the stack was correct.
May need to go back several states.
```

### Want to Hide Experimental Work
```
User: I have some experimental commits cluttering my smartlog

Agent: Hide them to clean up the view...
/bl-undo --hide <hash>
They won't show in git sl but can be restored.
```

## Error Handling

| Error | Resolution |
|-------|------------|
| "Nothing to undo" | No recent undoable operations |
| "Working directory dirty" | Stash or commit changes first |
| "Would cause conflicts" | Use `-i` to find different restore point |
| Lost uncommitted changes | Cannot recover - check editor undo |
| Pushed commits | Must revert on remote instead |

## Tips

1. **Commit before risky operations** - Makes undo possible
2. **Use `-i` for complex recovery** - Better visibility of history
3. **Hidden commits aren't permanent** - May be garbage collected
4. **Check result immediately** - Run `git sl` after undo
