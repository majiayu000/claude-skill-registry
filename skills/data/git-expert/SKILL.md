---
name: git-expert
description: |
  Git domain expert.

  Knows about:
  - Status, Switch, Create Branch, Commit, Pull, Push, Log

  Use when:
  - User asks about git operations
  - Context needed before starting work
  - Reviewing git status
  - Managing git workflow

trigger_phrases:
  - "change branch"
  - "check git status"
  - "checkout branch"
  - "commit changes"
  - "commit my work"
  - "commit history"
  - "create branch"
  - "create commit"
  - "get updates"
  - "git history"
  - "git status"
  - "make commit"
  - "make new branch"
  - "new branch"
  - "pull changes"
  - "pull latest"
  - "push changes"
  - "push to remote"
  - "show history"
  - "show status"
  - "start branch"
  - "switch branches"
  - "sync from remote"
  - "sync to remote"
  - "upload changes"
  - "what branch am i on"
  - "what's been done"
  - "what's changed"
---

# Git Expert Skill

## What This Skill Does

Helps you manage your git workflow with smart command suggestions.

## Available Commands

- `/git:status` - Get the current git status
- `/git:switch` - Switch branches
- `/git:create-branch` - Create a new branch
- `/git:commit` - Make a commit with special instructions
- `/git:pull` - Pull changes
- `/git:push` - Push changes
- `/git:log` - View history/what's been done

## When Claude Uses This

When you mention things like:
- "what's the git status?" → Suggests `/git:status`
- "I need to switch branches" → Suggests `/git:switch`
- "create a new feature branch" → Suggests `/git:create-branch`
- "let me commit my changes" → Suggests `/git:commit`
- "pull the latest changes" → Suggests `/git:pull`
- "push my commits" → Suggests `/git:push`
- "show the commit history" → Suggests `/git:log`

## Best Practices

1. **Before starting**: Run `/git:status` to see current state
2. **Understand scope**: Verify which branch you're on
3. **Track progress**: Review commit history with `/git:log`
4. **Keep updated**: Pull changes before pushing

## Customization

Edit the trigger phrases in the frontmatter above to match your vocabulary.
Keep the skill description updated as you evolve the domain.

## Integration

Works seamlessly with other Claude Code domains:
- Can be invoked manually: `/git:operation`
- Auto-triggered by Claude based on conversation
- Works with other skills and commands

## Common Workflows

**Start a feature:**
```
/git:status                    # Check current state
/git:create-branch feature/x   # Create new branch
```

**Commit and push:**
```
/git:status                    # Review changes
/git:commit "message"          # Create commit
/git:push origin branch-name   # Push to remote
```

**Update your branch:**
```
/git:pull origin main          # Get latest main
# Resolve conflicts if needed
/git:push origin branch-name   # Push your work
```

**Review history:**
```
/git:log --oneline 10          # Recent commits
/git:log --graph --oneline     # Branch structure
```
