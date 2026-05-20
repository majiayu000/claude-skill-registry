---
name: update
description: |
  Quick context checkpoint without ending session. Use when user types /update. Saves progress to session log and updates state if needed.
license: MIT
compatibility: marvin
metadata:
  marvin-category: session
  user-invocable: true
  slash-command: /update
  model: default
  proactive: false
---

# Update Skill

Lightweight save without ending the session. Use frequently to preserve context.

## When to Use

- User types `/update`
- After finishing a chunk of work
- Before switching contexts
- Every hour or so during long sessions
- When context is running low

## Process

### Step 1: Identify What Changed
Quickly scan the recent conversation for:
- Topics worked on
- Decisions made
- Files created/modified
- Any state changes needed

Keep it brief. No full summary needed.

### Step 2: Append to Session Log
Get today's date: `date +%Y-%m-%d`

Append to `sessions/{TODAY}.md`:
```markdown
## Update: {TIME}
- {what was worked on, 1-3 bullets}
```

If file doesn't exist, create with header: `# Session Log: {TODAY}`

### Step 3: Update State (if needed)
Only update `state/current.md` if something actually changed:
- New open thread
- Completed item
- Changed priority
- New project/task discovered

Skip if nothing material changed.

### Step 4: Confirm (minimal)
One line: "Checkpointed: {brief description}"

No summary. No "next actions" list. Just confirm the save.

## Output Format

```
Checkpointed: {2-5 word description of what was saved}
```

## Notes
- This is intentionally lightweight
- Don't use for full session wrap-up (use `/end` for that)
- Multiple updates per day append to the same session file

---

*Skill created: 2026-01-22*
