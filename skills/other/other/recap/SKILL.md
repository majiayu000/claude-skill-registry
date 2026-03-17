---
name: recap
description: Summarize your current session state - problem, progress, hints used, what's left to do.
argument-hint: (no arguments needed)
allowed-tools: Read, Glob
---

# Recap - Where Are You?

The user wants a quick summary of where they are.

## Check Session State
Read `data/session.json` for current state.

## If Active Session

Give a quick, friendly recap:

"Alright, here's where you're at:

**Problem:** [name]
**Mode:** [TEACHER/INTERVIEWER/REVIEWER]

**Your progress:**
- [x] You understood the problem
- [x] You identified it as a [pattern] problem
- [ ] Approach plan - still need this
- [ ] Complexity estimate
- [x] You caught the empty array edge case

**Hints used:** [X] (that's a -[Y] point penalty if we're scoring)

**Last thing you did:** [last activity from log]

**What's next:** [specific next step - e.g., "Work through your approach step by step" or "Start implementing now that you have a plan"]

Need anything, or ready to keep going?"

## If Interview Mode

Add timing info:
"You're [X] minutes in, with about [Y] minutes left. Currently in the [phase] phase. [Pace comment if relevant - e.g., "You're on track" or "Might want to pick up the pace on coding"]"

## If No Active Session

Keep it brief:
"No active session right now. Start one with `/s [problem]` or `/i [topic]`."

## Tone
- Factual but friendly
- Quick to scan
- Actionable - always end with what's next
