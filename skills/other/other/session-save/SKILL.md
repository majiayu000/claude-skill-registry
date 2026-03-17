---
name: session-save
description: Save current session progress, TODOs, and context to a local file before ending a session. Enables picking up later with /session-load.
disable-model-invocation: true
---

# Session Save

Capture current session progress so you can resume later with `/session-load`.

## Usage

`/session-save`

## Procedure

### Step 1: Gather Session Context

Collect the following information:

1. **Current branch**: Run `git branch --show-current`
2. **Modified files**: Run `git status --short` to see what's changed
3. **Recent commits**: Run `git log --oneline -5` for recent history
4. **Current working directory**: Note the cwd

### Step 2: Summarize the Session

Create a session summary by reviewing what was accomplished:

1. **What was done**: List completed tasks/changes in this session
2. **What's pending**: List unfinished work or known TODOs
3. **Key decisions**: Any architectural or design decisions made
4. **Blockers**: Anything that's blocking progress
5. **Context notes**: Important context that would be lost between sessions

### Step 3: Generate Session File

Create the file at `.claude/sessions/<date>-<topic>.md`:

- `<date>` = today's date in `YYYY-MM-DD` format
- `<topic>` = a short slug describing the session's focus (e.g., `auth-refactor`, `api-endpoints`)

```markdown
# Session: [Topic]
**Date**: [YYYY-MM-DD]
**Branch**: [branch-name]

## Completed
- [What was accomplished]
- [What was accomplished]

## Pending TODOs
- [ ] [Task description]
- [ ] [Task description]

## Key Decisions
- [Decision and rationale]

## Blockers
- [Blocker description, if any]

## Modified Files
[Output of git status --short]

## Context Notes
[Any important context for resuming, e.g., "The API design follows the pattern in src/api/users.ts",
"We chose approach X over Y because..."]

## Resume Instructions
To continue this work:
1. Check out branch: `git checkout [branch]`
2. Start with: [description of next step]
```

### Step 4: Confirm Save

Tell the user:
- Where the file was saved
- How to resume: "Run `/session-load` in your next session to pick up where you left off"
