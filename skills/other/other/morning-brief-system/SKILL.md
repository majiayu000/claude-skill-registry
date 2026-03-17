---
name: morning-brief-system
version: "2.0.0"
price: "$14"
author: "@BrianRWagner"
platform: claude-code
slug: "brw-morning-brief-system"
description: "Generate a daily founder briefing that turns scattered context into clear execution priorities. Action-first format. Never lets high-leverage work get buried under low-leverage noise."
---

> **Optimized for Claude Code, Cursor, GitHub Copilot, and any AI that accepts markdown instructions.**
> Paste this SKILL.md into your AI's context or project instructions and run it immediately.

---

# Morning Brief System

Most morning routines confuse activity with clarity. You check email, scan Slack, review your calendar — and end the "planning" still uncertain about what actually matters today.

This skill ends that. Give it your day's context and it outputs a single, structured brief: what's locked, what's priority, what could blow up, and what decisions need to get made. Action-first. No padding.

---

## Mode

Detect from context or ask: *"Quick priorities, full brief, or full brief with weekly context?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | Top 3 priorities + 2 watch-outs, 2 min | Rushed morning, already have context |
| `standard` | Full brief: locked commitments, priorities, blockers, decisions needed | Default daily planning |
| `deep` | Full brief + weekly arc context + energy allocation + EOD success criteria | High-stakes week, major deliverables in play |

**Default: `standard`** — use `quick` if you're already oriented and just need the brief. Use `deep` at the start of a high-stakes week.

---

## Context Loading Gates

**The AI must confirm all gates before generating the brief.**

```
GATE CHECK — Required Before Starting
======================================
[ ] Today's fixed commitments provided (calls, meetings, hard deadlines)
[ ] Top 3 priorities for the day stated
[ ] Known blockers or dependencies identified
[ ] Time available for focused work estimated
[ ] Optional: key metrics or signals to watch, overnight context, travel/disruptions

If fixed commitments and priorities are NOT provided: ask for them before generating.
A brief built on no context is just a template. Context is everything.
```

---

## Operating Modes

**Mode A — Daily Brief:** User provides today's context. Generate a full brief.
**Mode B — Carry-Forward:** User has yesterday's brief available. Load prior unfinished items and integrate into today's plan. Show what's rolling over explicitly.
**Mode C — Crisis Mode:** User flags a disruption (deal blew up, urgent client issue, day got blown). Regenerate priorities around the new reality.

Determine mode before starting. If prior brief is available, always default to Mode B.

---

## Phase 1: Context Intake

**For Mode A — Fresh Brief:**

Collect all context in one message:

```
Quick context for your morning brief:

1. Fixed commitments today: (calls, meetings, hard deadlines with times)
2. Top 3 priorities: (what MUST move today, not just what's on the list)
3. Known blockers: (what's waiting on someone else? what could slow you down?)
4. Focused time available: (rough estimate of heads-down hours)
5. Anything worth flagging: (overnight news, key metrics, something making you uneasy)
6. Optional: Yesterday's brief (paste it or note what didn't get done)
```

**For Mode B — Carry-Forward:**

Load prior brief. Identify:
- Items completed (archive them)
- Items not completed (carry forward explicitly, re-prioritize based on today's context)
- Items that have changed urgency (call out the shift)

Then ask for today's new inputs (new commitments, priorities, blockers).

**For Mode C — Crisis Mode:**

Ask: "What changed? What does the day look like now?"
Rebuild the brief from the new reality. Don't try to fit crisis response into a normal schedule.

---

## Phase 2: Analysis

Before generating the brief, run this internal analysis:

```
Pre-brief analysis:
- Fixed time committed: [X hours]
- Realistic focused time remaining: [Y hours]
- Priority-to-time fit: [are the top 3 priorities achievable in available time?]
- Overload flag: [yes/no — is the plan realistic?]
- Critical path item: [what's the one thing that, if it doesn't happen, makes the day a loss?]
- Risk items: [what could blow up or is waiting on external factors?]
- Decision queue: [what decisions need to be made today that are blocking progress?]

Note conflicts: if the plan requires more time than available, flag it before generating — do not silently let the brief promise too much.
```

---

## Phase 3: Generate — The Brief

```markdown
# Morning Brief — [Day, Date]

## Today in One Line
[One sentence. What is this day actually about? Not a list — the dominant theme or goal.]

## Non-Negotiables (fixed commitments)
| Time | Commitment | Notes |
|------|-----------|-------|
| [time] | [commitment] | [any prep needed?] |
| [time] | [commitment] | [notes] |

Focused time available: ~[X] hours

## Top 3 Priorities
*(In order. These move the needle. Everything else waits.)*

**1. [Priority name]**
Next action: [specific — not "work on X" but "draft the first section of X" or "send the proposal to Y"]
Why today: [one sentence on urgency or consequence of delay]
Time estimate: [rough hours]

**2. [Priority name]**
Next action: [specific]
Why today: [one sentence]
Time estimate: [rough hours]

**3. [Priority name]**
Next action: [specific]
Why today: [one sentence]
Time estimate: [rough hours]

## Risk Radar
*(Things that could derail the day or that need monitoring)*
- [Risk 1]: [one sentence on what it is and what to watch for]
- [Risk 2]: [one sentence]
[Skip this section if nothing material — don't pad with hypotheticals]

## Decision Queue
*(Decisions that need to get made today — not necessarily by you, but need resolution)*
- [Decision 1]: [what needs to be decided, who decides, deadline]
- [Decision 2]: [same format]
[Skip if no active decisions pending]

## Suggested Schedule Blocks
*(Optional — only generate if asked or if overload was flagged)*
| Block | Focus |
|-------|-------|
| [time range] | [priority/commitment] |
| [time range] | [priority/commitment] |
| [time range] | [buffer/admin] |

## Carry-Forwards (from yesterday)
*(Items that didn't get done and are still relevant)*
- [Item 1] — [new priority level: high/medium/low]
- [Item 2] — [new priority level]
[Omit section if nothing to carry forward]

## End-of-Day Definition of Done
Today is a success if: [1-3 specific things that constitute a good day — based on the top priorities]
```

---

### Overload Protocol

If the planned work exceeds realistic capacity:

```
⚠️ OVERLOAD DETECTED

You have ~[X] hours of focused time. Your current plan requires ~[Y] hours.
That's a [Z]-hour gap.

To fix this, one of the following needs to happen:
1. Cut Priority 3 — push to tomorrow
2. Timebox Priorities 1-2 at [X hours each] and accept partial progress
3. Move a fixed commitment if it's flexible

Which do you want to do?
```

Do not silently generate a brief that promises more than the day can hold.

---

## Phase 4: Self-Critique

After generating the brief, run this mandatory review:

```
SELF-CRITIQUE — Brief Quality Check
=====================================
Priority specificity (1-10): ___
- Does each priority have a specific next action, not just a topic?
- Could someone pick up this brief and know exactly what to do first?

Realism (1-10): ___
- Does the plan fit inside the available time?
- Was the overload protocol triggered when it should have been?

Risk completeness (1-10): ___
- Are the risks specific to today's context?
- Or are they generic ("things could come up")?

Definition of Done (1-10): ___
- Is "today is a success if..." specific enough to actually know at 6pm?
- Or is it vague enough to always feel incomplete?

If any score < 7: revise that section.
Improvements: [specific]

Overall: [one sentence — is this brief ready to use?]
```

---

## Phase 5: Final Output + Iteration Menu

Present the refined brief. Then close with:

```
Brief ready. [X] hours of committed time. [Y] hours of focus available.

Modes if you need to adjust:

A) Aggressive mode — I'll compress the schedule and protect only the critical path
B) Focus-protection mode — I'll remove everything that isn't Priority 1 and 2, rebuild around deep work
C) Add contingency — I'll identify what to cut or defer if the day gets disrupted
D) Done — run with this

Or just reply "done" to lock it in.
```

**If A — Aggressive Mode:**
Compress schedule. Identify exactly what can be done in parallel or shortened. Surface what gets cut if the day runs long. Output: revised block schedule with minimum viable actions per priority.

**If B — Focus-Protection Mode:**
Identify the single most important block of focused work. Design the day to protect it. Everything else is secondary — defer, batch, or drop. Output: simplified brief with one primary focus and explicit "park it" list.

**If C — Contingency Plan:**
Identify the most likely disruption (based on Risk Radar). Build a decision tree: "If [risk] happens → cut [priority 3] and timebox [priority 1] to [X hours]." Output: brief + contingency plan in case of disruption.

---

## Weekly Mode (Optional)

If user asks for a weekly brief instead of daily:

- Replace "Today in One Line" with "This Week in One Line"
- Replace "Fixed Commitments" with week's calendar at a glance
- Expand "Top 3 Priorities" to "Top 5 Priorities for the Week" with day-by-day rough allocation
- Add "This Week's Most Important Decision" section
- Definition of Done becomes "Friday is a success if..."

---

*Morning Brief System v2.0.0 — Part of the AI Marketing Skills library by Brian Wagner (@BrianRWagner)*
*Works with: Claude Code, Cursor, GitHub Copilot, VS Code Copilot, ChatGPT, Claude.ai*
