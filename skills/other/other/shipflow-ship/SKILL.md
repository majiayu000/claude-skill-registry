---
name: shipflow-ship
description: Ship the session — commit, push, update tasks + changelog, save memory, wrap context. One report. Use this at end of session when ready to push.
argument-hint: [optional commit message or notes]
---

## Context

- Current directory: !`pwd`
- Current date: !`date '+%Y-%m-%d'`
- Git status: !`git status --short 2>/dev/null || echo "Not a git repo"`
- Git diff stat: !`git diff HEAD --stat 2>/dev/null || echo ""`
- Current branch: !`git branch --show-current 2>/dev/null || echo "unknown"`
- Recent commits (style reference): !`git log --oneline -5 2>/dev/null || echo "no commits"`
- Master TASKS.md: !`cat /home/claude/shipflow_data/TASKS.md 2>/dev/null || cat TASKS.md 2>/dev/null || echo "No TASKS.md"`
- Existing CHANGELOG: !`head -20 CHANGELOG.md 2>/dev/null || echo "no CHANGELOG.md"`

## Your task

Close the session and ship — recap + commit + push. All steps inline. ONE report at the end.

### Step 1 — Workspace root detection

If the current directory has no `.git` directory BUT contains project subdirectories with changes, use **AskUserQuestion**:
- "Which project should I ship?"
- One option per project with uncommitted changes
- `multiSelect: false`

Then work inside that project for all remaining steps.

### Step 2 — Summarize session (internal, no output)

From the conversation, silently identify:
- What was completed this session
- What was started but not finished
- Key files modified (from git diff stat in context)
- Any decisions worth saving to memory

### Step 3 — Update TASKS.md (silent)

Using the master TASKS.md from context:
- Mark completed items: `🔄 in progress` → `✅ done` and `📋 todo` → `✅ done`
- Mark partially done items with `🔄 in progress`
- Add new tasks discovered this session under the right section
- Update master `/home/claude/shipflow_data/TASKS.md` — always, even from a sub-project
- If a local `TASKS.md` also exists, update both
- No output at this step.

### Step 4 — Update CHANGELOG.md (silent)

Using the session summary and git diff:
- Group changes into Keep a Changelog categories: Added / Changed / Fixed / Security / Removed
- Consolidate related changes into single human-readable entries
- Skip CI, formatting, merge, and changelog-update commits
- Prepend a new `## [date]` entry to CHANGELOG.md (or update today's entry if it exists)
- No output at this step.

### Step 5 — Save decisions to memory (silent)

For each significant decision or discovery from Step 2, save to memory if useful for future conversations.

Skip if no meaningful decisions were made. No output at this step.

### Step 6 — Stage and commit

Check for secrets before staging:
- If untracked `.env`, credential, or token files are NOT in `.gitignore`, warn the user and stop

Stage and commit:
```bash
git add -A
git commit -m "[message from $ARGUMENTS or derived from session summary]
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

Use a HEREDOC for the commit message. Follow the style of recent commits.

### Step 7 — Push

```bash
git push
# If no upstream: git push -u origin <branch>
```

### Step 8 — Sync ShipFlow (silent housekeeping)

If `/home/claude/ShipFlow` has uncommitted changes, auto-commit and push:
```bash
cd /home/claude/ShipFlow && git add -A && git diff --cached --quiet || git commit -m "sync" && git push
```

Only report this if it fails.

### Step 9 — ONE combined report

```
## Shipped — [date]

**[SHORT_SHA]** — "[commit message]" → [branch]

**What changed:**
- [bullet per logical change from diff — specific, not vague]

**Session closed:**
- Completed: [item], [item]
- In progress: [item — where it stands]
- Decisions saved: [decision or "none"]

**Up next:**
1. [emoji] [top TASKS.md priority]
2. [emoji] [second priority]
3. [emoji] [third priority]

[✓ Pushed] or [⚠️  Push failed: reason]
```

### Rules

- Do NOT output anything before Step 9 — one report only
- Do NOT force push to main/master
- Do NOT commit secrets or credentials
- If nothing to commit, say so in the report and still do Steps 3–5
- Keep the final report under 30 lines
