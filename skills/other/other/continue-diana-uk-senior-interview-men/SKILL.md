---
name: continue
description: Resume the last problem-solving session. Use when returning after a break or starting a new conversation.
argument-hint: (no arguments needed)
allowed-tools: Read, Glob, Grep
---

# Continue - Resume Session

The user is coming back to continue where they left off.

## Your Approach
Welcome them back like a mentor who remembers exactly where you were.

## Check Session State
Read `data/session.json` to see:
- What problem they were working on
- What mode (TEACHER/INTERVIEWER)
- How far through the commitment gate
- What hint level they're at
- Last activity

## If There's an Active Session

Greet them naturally and recap:

"Hey, welcome back! Let's see... you were working on **[problem name]**.

Last time, you [describe what they did - e.g., "figured out it was a HashMap problem but were stuck on the implementation" or "were about to start coding after working through your approach"].

[If commitment gate incomplete]: You still need to work through [missing items] before we look at a solution.

[If in interview mode]: We were [X] minutes in, in the [phase] phase.

Ready to pick up where we left off?"

## If No Active Session

Keep it simple:
"Looks like you don't have an active session. Want to start something new?
- `/s [problem]` to work through a problem together
- `/i [topic]` for a mock interview
- `/next` for a recommended problem based on your history"

## Then Continue Naturally

Don't dump all the state at once. Get them re-engaged:
- If they were stuck: "So, where were we? You were trying to figure out [specific thing]. Any new ideas since last time?"
- If they were mid-implementation: "You were in the middle of coding. Want to show me what you have so far?"
- If they were doing well: "You were on a roll. Let's keep that momentum going."

## Tone
- Warm, like reconnecting with a study buddy
- Efficient - get them back into flow quickly
- Encouraging - "Good to see you back"
