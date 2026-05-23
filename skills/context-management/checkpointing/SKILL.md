---
name: checkpointing
description: How checkpointing works for tracking file changes and rewinding to previous states. Use when user asks about checkpoints, rewinding, rollback, undo, or restoring previous states.
---

# Claude Code Checkpointing

## Overview

Claude Code includes an automatic checkpointing system that tracks file edits and allows users to recover from unwanted changes during development sessions.

## How Checkpointing Works

### Automatic Tracking

The system captures code states before each modification.

**Key features:**
- Every user prompt creates a new checkpoint
- Checkpoints persist across resumed conversations
- Automatic cleanup occurs after 30 days (configurable)

### What Gets Tracked

**Tracked:**
- Direct file edits via Edit tool
- File creations via Write tool
- File modifications by Claude

**Not tracked:**
- Files modified by bash commands (`rm`, `mv`, `cp`)
- Manual file modifications outside Claude Code
- Changes from concurrent sessions (unless they affect files the current session modified)

## Rewinding Changes

### Access Rewind Menu

**Keyboard shortcut:**
Press `Esc` twice (quickly)

**Slash command:**
```
/rewind
```

### Restoration Options

When you open the rewind menu, you have three options:

#### 1. Conversation Only
**Keeps:** All code changes
**Reverts:** Conversation history to selected checkpoint

**Use when:**
- You want to start conversation over
- Code changes are good
- You want to try different approach in conversation

#### 2. Code Only
**Keeps:** Conversation history
**Reverts:** Files to selected checkpoint

**Use when:**
- Recent changes broke something
- Want to undo code changes
- Conversation context is valuable

#### 3. Both Code and Conversation
**Reverts:** Everything to selected checkpoint (full rollback)

**Use when:**
- Complete do-over needed
- Both code and conversation went wrong
- Want to return to known good state

### Selecting a Checkpoint

Checkpoints are displayed with:
- Timestamp
- User prompt that created it
- Files affected
- Changes summary

Navigate with arrow keys and select with Enter.

## Use Cases

### Testing Different Approaches

**Scenario:** Try multiple implementation strategies without losing starting point.

```
# Approach 1
"implement feature using strategy A"
# Review, not ideal

# Rewind
Esc Esc → Select checkpoint → Code only

# Approach 2
"implement feature using strategy B"
# Better!
```

### Quick Bug Recovery

**Scenario:** Recent changes introduced a bug.

```
# Make changes
"refactor the authentication module"
# Oops, broke login

# Rewind
Esc Esc → Select checkpoint before refactor → Code only

# Try again differently
"refactor authentication but keep existing login flow"
```

### Iterative Development

**Scenario:** Preserve working states while iterating.

```
# Working state 1
"add basic user validation"
# Works ✓

# Iterate
"add more complex validation rules"
# Issues found

# Return to working state
Esc Esc → Code only

# Try different iteration
"add regex-based validation"
```

### Conversation Reset

**Scenario:** Conversation got confused or went off track.

```
# Good code changes made
"add user profile endpoint"
"add user settings endpoint"

# Conversation gets confusing
# Want to restart conversation but keep code

# Rewind conversation only
Esc Esc → Conversation only → Select early checkpoint

# Fresh conversation start with code intact
```

## Important Limitations

### Bash Command Changes Not Tracked

**Not captured:**
```
!rm file.txt
!mv old.txt new.txt
!cp source.txt dest.txt
!git checkout -b new-branch
```

**Why:** Bash commands run outside Claude's file tracking system.

**Workaround:**
- Use Claude's Edit/Write tools instead when possible
- Manually track bash file operations
- Use git for version control of important changes

### External Changes Not Tracked

**Not captured:**
- Manual edits in your text editor
- IDE refactorings
- File system operations outside Claude Code
- Changes from other tools

**Workaround:**
- Use git to track all changes
- Create manual checkpoints with git commits
- Be aware of what Claude modified vs what you modified

### Concurrent Session Caveats

**Limited tracking:**
If multiple Claude Code sessions modify the same files, only changes from the current session are tracked for checkpointing.

**Best practice:**
Use one Claude Code session at a time per project.

## Not a Version Control Replacement

### Checkpointing vs Git

| Feature | Checkpointing | Git |
|---------|--------------|-----|
| **Scope** | Session-level | Repository-wide |
| **Duration** | 30 days | Permanent |
| **Granularity** | Per prompt | Per commit |
| **Collaboration** | Single user | Team |
| **Purpose** | Session recovery | Version control |
| **Bash tracking** | No | Yes |

### Use Both Together

**Git for:**
- Permanent history
- Collaboration
- Branch management
- All file changes (including bash)
- Release management

**Checkpointing for:**
- Quick session rollback
- Trying different approaches
- Recovering from mistakes
- Conversation management
- Rapid iteration

**Recommended workflow:**
```
# Regular git commits for milestones
git commit -m "Working authentication"

# Use checkpointing for rapid iteration
"try optimization A"
Esc Esc → rewind if not good
"try optimization B"
Esc Esc → rewind if not good
"try optimization C"
# This one works!

# Commit the winner
git add .
git commit -m "Optimized authentication"
```

## Configuration

### Checkpoint Retention

**Default:** 30 days

**Configure retention:**
Edit `.claude/settings.json`:
```json
{
  "checkpointRetentionDays": 60
}
```

### Disable Checkpointing

**Not recommended**, but possible:
```json
{
  "enableCheckpointing": false
}
```

## Best Practices

### 1. Review Before Rewinding

**Look at:**
- What checkpoint contains
- What will be lost
- What will be kept

**Avoid:**
- Blindly selecting checkpoints
- Rewinding without understanding impact

### 2. Use Descriptive Prompts

**Good (easy to identify):**
```
"add email validation to user registration"
"refactor database queries for performance"
```

**Bad (hard to identify):**
```
"make changes"
"fix it"
```

Checkpoints show your prompts, so descriptive prompts make checkpoint selection easier.

### 3. Combine with Git

```
# Checkpoint for rapid iteration
Try approach → rewind → try approach → rewind

# Git for confirmed changes
git add .
git commit -m "Final implementation"
```

### 4. Rewind Code, Not Conversation

**Often better:**
Rewind code only and keep conversation history.

**Why:**
- Maintains context
- Claude learns from mistakes
- Can explain what went wrong
- Better for iterative improvement

### 5. Regular Git Commits

Don't rely solely on checkpoints:
```
# After significant progress
git add .
git commit -m "Checkpoint: working user authentication"

# Continue with Claude Code
# Checkpointing handles rapid iteration
# Git handles permanent milestones
```

## Troubleshooting

### Checkpoint Not Showing Expected State

**Possible causes:**
- Changes made via bash commands (not tracked)
- External file modifications
- Concurrent session changes
- Checkpoint expired (>30 days)

**Solution:**
- Use git for those scenarios
- Check git history: `git log`
- Review git diff: `git diff`

### Can't Find Recent Checkpoint

**Check:**
- Are you in the right directory?
- Is this the same session?
- Did checkpoint expire?

**Solution:**
- Use `/rewind` command instead of Esc Esc
- Check session history
- Verify working directory

### Rewind Not Working

**Check:**
- Are files write-protected?
- Do you have filesystem permissions?
- Are files open in another program?

**Solution:**
- Close files in editors
- Check file permissions
- Ensure no file locks

## Example Workflows

### Refactoring Safely

```
# Current working state
git commit -m "Pre-refactor checkpoint"

# Try refactoring
"refactor user controller for better error handling"

# Test
!npm test

# If tests fail
Esc Esc → Code only → Return to pre-refactor

# Try different approach
"refactor user controller with focus on backward compatibility"

# If tests pass
git commit -m "Refactored user controller"
```

### Feature Experimentation

```
# Baseline working
git commit -m "Baseline"

# Experiment 1
"add feature using approach A"
# Review, note pros/cons

# Rewind
Esc Esc → Code only

# Experiment 2
"add feature using approach B"
# Compare, choose better

# If experiment 2 is better
git commit -m "Added feature using approach B"

# If neither was good
Esc Esc → Code only → Back to baseline
```

### Conversation Management

```
# Making good progress
"implement auth"
"add user roles"
"add permissions"

# Conversation gets complex/confused
Esc Esc → Conversation only → Select first checkpoint

# Start fresh conversation
"explain the architecture we just built"
# Code intact, conversation reset
```
