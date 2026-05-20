---
name: session-load
description: Load saved session context from a previous session. Lists available sessions and restores TODOs, context, and pending work.
disable-model-invocation: true
argument-hint: [session-file (optional)]
---

# Session Load

Restore context from a previously saved session (created with `/session-save`).

## Usage

- `/session-load` — List available sessions and choose one
- `/session-load <filename>` — Load a specific session file

## Procedure

### Step 1: Find Available Sessions

Check if `$ARGUMENTS` specifies a file. If not:

1. List files in `.claude/sessions/` directory
2. Sort by date (newest first)
3. Show the user a numbered list:

```
Available sessions:
1. 2025-01-15-auth-refactor.md
2. 2025-01-14-api-endpoints.md
3. 2025-01-12-initial-setup.md

Which session would you like to load?
```

If `$ARGUMENTS` specifies a file, use that directly.

If `.claude/sessions/` doesn't exist or is empty, tell the user:
> "No saved sessions found. Use `/session-save` to save your current session before ending it."

### Step 2: Load Session File

Read the selected session file and extract:
- Branch name
- Pending TODOs
- Context notes
- Resume instructions

### Step 3: Verify Current State

Check if the current environment matches the session:

1. **Branch check**: Is the user on the same branch? If not, ask:
   > "The session was on branch `[branch]` but you're on `[current]`. Switch branches?"
2. **File check**: Do the modified files mentioned in the session still exist?
3. **Git status**: Are there uncommitted changes that might conflict?

### Step 4: Present Session Context

Display a concise summary of what was happening:

```
## Restored Session: [Topic]
**Date**: [date]
**Branch**: [branch]

### Where We Left Off
[Resume instructions from the session file]

### Pending TODOs
- [ ] [Task 1]
- [ ] [Task 2]

### Key Context
[Context notes]
```

### Step 5: Offer to Continue

Ask the user:
> "Ready to pick up where we left off? The next step was: [resume instruction]. Should I start with that?"

Do NOT automatically start working. Let the user confirm what they want to do first. They may have changed priorities since the last session.
