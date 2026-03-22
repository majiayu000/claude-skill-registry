---
name: shipflow-end
description: End a task — summarize what was done, mark task done in TASKS.md, update CHANGELOG.md. Does NOT commit or push. Use when finishing a task but not ready to ship.
argument-hint: [optional summary or notes]
---

## Context

- Current directory: !`pwd`
- Current date: !`date '+%Y-%m-%d'`
- Project name: !`basename $(pwd)`
- Git branch: !`git branch --show-current 2>/dev/null || echo "unknown"`
- Git status: !`git status --short 2>/dev/null || echo "Not a git repo"`
- Git diff stat: !`git diff HEAD --stat 2>/dev/null || echo "no changes"`
- Recent commits (this session): !`git log --oneline -10 2>/dev/null || echo "no commits"`
- Master TASKS.md: !`cat /home/claude/shipflow_data/TASKS.md 2>/dev/null || echo "No master TASKS.md"`
- Local TASKS.md (if exists): !`cat TASKS.md 2>/dev/null || echo "No local TASKS.md"`
- Existing CHANGELOG: !`head -30 CHANGELOG.md 2>/dev/null || echo "no CHANGELOG.md"`

## Your task

Wrap up the current task. Summarize, update tracking files, but do NOT commit or push.

### Step 1 — Summarize what was done (internal)

From the conversation, identify:
- What was completed
- What was started but not finished
- Key files modified (from git diff)
- Any decisions worth noting

### Step 2 — Update TASKS.md (silent)

Using the master TASKS.md from context:
- Mark completed items: `🔄 in progress` → `✅ done` and `📋 todo` → `✅ done`
- Mark partially done items: `📋 todo` → `🔄 in progress` with a note
- Add new tasks discovered during the work
- Update master `/home/claude/shipflow_data/TASKS.md` — always
- If a local `TASKS.md` also exists, update both
- No output at this step.

### Step 3 — Update CHANGELOG.md (silent)

- Group changes into Keep a Changelog categories: Added / Changed / Fixed / Security / Removed
- Consolidate related changes into single human-readable entries
- Prepend a new `## [date]` entry to CHANGELOG.md (or update today's entry if it exists)
- Skip trivial changes (formatting, comments)
- No output at this step.

### Step 4 — Save decisions to memory (silent)

For each significant decision or discovery from Step 1, save to memory if it will be useful in future conversations. Skip if nothing meaningful.

### Step 5 — Report

Output ONE concise report:

```
## Done — [date]

**What changed:**
- [bullet per logical change — specific, not vague]

**Status:**
- Completed: [item], [item]
- In progress: [item — where it stands]
- Decisions saved: [decision or "none"]

**Up next:**
1. [emoji] [top priority from TASKS.md]
2. [emoji] [second priority]
3. [emoji] [third priority]

[📝 Not committed — run /shipflow-ship when ready to push]
```

### Rules

- Do NOT commit or push — that's shipflow-ship's job
- Do NOT output anything before Step 5 — one report only
- Keep the report under 25 lines
- If nothing was done this session, say so honestly
- Update BOTH master and local TASKS.md when both exist
