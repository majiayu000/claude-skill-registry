---
name: end
description: |
  End MARVIN session, save context, and commit changes. Use when user types /end or /quit. Creates session log, updates state, and optionally commits to git.
license: MIT
compatibility: marvin
metadata:
  marvin-category: session
  user-invocable: true
  slash-command: /end
  model: default
  proactive: false
---

# Session End Skill

End MARVIN session with full context preservation.

## When to Use

- When user types `/end` or `/quit`
- When actually done for a while
- When wanting a full session summary
- When closing out the day

## Inputs

- Full conversation from this session
- Current state from `state/current.md`
- Today's date (from startup)

## Process

### Step 1: Summarize Session
Review the conversation and extract:
- **Topics discussed** — What did we work on?
- **Decisions made** — What was decided?
- **Content shipped** — Any work completed or published?
- **Open threads** — What's unfinished or needs follow-up?
- **Action items** — What does user need to do next?

### Step 2: Update Content Log
If any content was shipped, append to `content/log.md`:
```markdown
### {TODAY}
- **[TYPE]** "Title"
  - URL: {link if applicable}
  - Notes: {any relevant notes}
```

### Step 3: Update Session Log
Append to `sessions/{TODAY}.md`:
```markdown
## Session: {TIMESTAMP}

### Topics
- {topic 1}
- {topic 2}

### Decisions
- {decision 1}

### Shipped
- {content shipped, if any}

### Open Threads
- {thread 1}

### Next Actions
- {action 1}
```

If file doesn't exist, create it with header:
```markdown
# Session Log: {TODAY}
```

### Step 4: Update State
Update `state/current.md` with:
- Any new priorities or action items
- Changed project statuses
- New open threads
- Removed/completed items (mark as done)
- Update the "Last updated" timestamp

Ensure nothing falls through the cracks:
- Commitments made → add to priorities with context
- Follow-ups needed → add to open threads

### Step 5: Confirm with User
Show brief summary:
- What was logged
- Any follow-ups scheduled
- State updated

### Step 6: Commit Changes (Optional)
If user wants to commit:
```bash
git add -A
git commit -m "$(cat <<'EOF'
chore: session log and state update

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
git push
```

## Output Format

```
**Session Summary:**
- Topics: {list}
- Shipped: {content if any}
- Open threads: {count}

**Updated:**
- sessions/{TODAY}.md
- state/current.md

See you next time!
```

## Notes
- Multiple `/end` calls in one day append to the same session file
- Keep summaries concise but complete enough for future context

---

*Skill created: 2026-01-22*
