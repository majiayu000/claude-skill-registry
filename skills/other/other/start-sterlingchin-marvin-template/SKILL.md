---
name: start
description: |
  Start MARVIN session with briefing. Use when user types /start or starts a new session. Loads context, reviews state, gives daily briefing.
license: MIT
compatibility: marvin
metadata:
  marvin-category: session
  user-invocable: true
  slash-command: /start
  model: default
  proactive: false
---

# Session Start Skill

Start MARVIN session with full context loading and daily briefing.

## When to Use

- When user types `/start`
- At the start of any Claude Code session in the MARVIN directory
- When resuming work after a break

## Process

### Step 1: Establish Current Date
```bash
date +%Y-%m-%d
```
Store as `TODAY`. Use for all file naming and date references.

### Step 2: Load Context

Read in order:
1. `state/current.md` — Current priorities, open threads, and state
2. `sessions/{TODAY}.md` — If exists, we're resuming today
3. If no today file, read `sessions/{YESTERDAY}.md` for continuity

### Step 3: Review Goals
Check `state/goals.md` for:
- Annual goals and progress
- Monthly targets

### Step 4: Assess Progress
Check `content/log.md` for current month:
- Content shipped vs. goals
- Days remaining in month

### Step 5: Check Follow-ups
Review `state/current.md` for any follow-up items:
- Surface any items with review date ≤ TODAY
- Remind user of upcoming follow-ups within 3 days

### Step 6: Surface Proactive Alerts
Compile and present:
- **Active priorities** from `state/current.md`
- **Open threads** needing attention
- Content pacing status (if behind)
- Any deadlines approaching

### Step 7: Greet User
Present a concise briefing:
- Date and day of week
- Top 3 priorities
- Any alerts or nudges
- Ask how to help today

## Output Format

```
Good morning! It's {Day}, {Date}.

**Today's Focus:**
1. {Priority 1}
2. {Priority 2}
3. {Priority 3}

**Alerts:**
- {Alert if any}

**Progress ({Month}):**
- {Goal 1}: X/Y
- {Goal 2}: X/Y

How can I help today?
```

## Notes
- If this is a resumed session (today's log exists), acknowledge what was already covered
- Keep briefing concise — details on request

---

*Skill created: 2026-01-22*
