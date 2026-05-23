---
name: checkpoint
description: Capture current session progress as a structured checkpoint
---

When the user invokes /checkpoint, follow these steps:

## 1. Gather Current State
- Get current git branch and status (`git status`, `git log --oneline -5`)
- List files modified in the last 30 minutes: `find . -name '*.rs' -o -name '*.sh' -o -name '*.md' -o -name '*.json' -o -name '*.toml' -mmin -30 -not -path './.git/*' -not -path './target/*'`
- Check TaskList for in-progress and completed tasks (if a team exists)

## 2. Check Linear Status
- Get the current Linear ticket status for the active branch's ticket

## 3. Build Checkpoint
Create a JSON checkpoint file at `.claude/checkpoints/<ISO-timestamp>.json`:
```json
{
  "timestamp": "<ISO-8601>",
  "branch": "<current-branch>",
  "ticket": "<ENG-XX>",
  "recent_commits": ["<last 5 commit subjects>"],
  "modified_files": ["<files changed in last 30 min>"],
  "tasks": {
    "completed": ["<completed task subjects>"],
    "in_progress": ["<in-progress task subjects>"],
    "pending": ["<pending task subjects>"]
  },
  "summary": "<1-2 sentence summary of current state>"
}
```

## 4. Save to Cross-Session Memory
Save a brief observation to claude-mem with:
- What was accomplished
- What's in progress
- Any blockers or decisions made

## 5. Print Summary
Display the checkpoint contents in a readable format.
