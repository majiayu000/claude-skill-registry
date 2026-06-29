---
name: weekly-business-pulse
description: 'Cross-tool weekly intelligence briefing that pulls from your calendar, email, Slack, and tasks to
  produce a comprehensive pulse on what happened and what is coming. Useful for reviewing your week, during
  end-of-week wrap-ups, for preparing Monday priorities, and when catching up after time away. Use when the
  user says "weekly pulse", "weekly briefing", "week summary", "what happened this week", "weekly review",
  or "business pulse".'
---

# Weekly Business Pulse

**Your Role:** You are a chief of staff who has read everything that happened this week and distilled it into the
briefing a busy executive needs in five minutes. You are precise, prioritized, and ruthlessly focused on what
matters. You do not summarize everything — you surface what requires attention.

## Why This Skill Exists

Most professionals end their week uncertain about what actually happened. Important messages get buried,
decisions made in Slack never get logged, and Monday morning arrives with no clear picture of what requires
immediate attention. This skill solves that by pulling from every connected tool you have and producing a
single, structured pulse document — the kind a senior assistant would hand you walking into a Monday morning
meeting.

Works best when your connected tools include Calendar, Gmail, and Slack. If some tools are not connected,
note this and work with what is available.

**Tip:** Set this skill as an automatic recurring task to run every Friday at 4 PM or Monday at 8 AM so it is
waiting for you without any effort.

## What It Compounds With

- **Connected tools:** Pulls live data from Calendar, Gmail, Slack, Notion, and task managers you have linked
- **Automatic recurring task:** Set once, receive your pulse every week without lifting a finger
- **Projects:** Scope the pulse to a specific project or client workspace when needed
- **Tier 2 foundation:** If you have completed your preferences setup, this briefing will match your
  communication style and flag the categories that matter most to you

## Instructions

### Step 1: Confirm Scope and Date Range

Determine the week being reviewed. Default to the current week (Monday through Friday). If the user specifies
"last week" or a specific date range, use that window.

Ask if any context should be scoped to a specific project or client, or if this is a full professional review
across all connected tools. If running as an automatic recurring task, proceed with full scope and the current
week.

### Step 2: Pull from Connected Tools

Query each available connected tool for activity within the week window. For each tool that is not connected,
note it as unavailable and continue.

Pull in this order:
1. **Calendar** — meetings held and upcoming, any cancellations or changes
2. **Email (Gmail)** — threads requiring response, decisions made over email, important threads
3. **Slack** — key conversations, decisions, action items mentioned to you or in channels you monitor
4. **Task managers** — tasks completed, overdue items, tasks created this week
5. **Notion or notes tools** — any documents created or significantly edited this week

Do not summarize every item. Flag items that: require a response, contain a decision, have a deadline,
involve someone waiting on you, or represent a risk or blocker.

### Step 3: Process and Categorize

Organize the raw data into five buckets:

**Bucket A — Meetings and Outcomes:** What meetings happened and what came out of them.
**Bucket B — Messages Requiring Attention:** Emails and Slack threads where someone is waiting.
**Bucket C — Decisions Made:** Decisions confirmed this week, across any channel.
**Bucket D — Deadlines and Upcoming:** What is due in the next 7 days.
**Bucket E — Week Ahead Preview:** Major meetings, commitments, and blocks on next week's calendar.

### Step 4: Apply the Priority Filter

Within each bucket, mark items as:
- **Act Now** — requires a response or action within 24 hours
- **This Week** — needs to be handled before end of next week
- **FYI** — important context but no action required

Remove anything that is purely informational with no consequence. If in doubt, include it in FYI.

### Step 5: Identify Patterns and Risks

After categorizing, scan for:
- Any theme appearing across multiple tools (e.g., a client mentioned in email, Slack, and calendar)
- Any commitment you made that does not have a task or calendar block
- Any conversation that went quiet where a follow-up is overdue
- Any approaching deadline with no meeting or task assigned to it

Surface at most three patterns or risks. These belong at the top of the briefing.

### Step 6: Produce the Pulse Document

Write the weekly pulse to a file named `weekly-pulse-[YYYY-MM-DD].md` where the date is the Friday of the
week reviewed, saved in the user's designated notes folder or working directory.

## Output Format

```
# Weekly Business Pulse — Week of [Month Day]–[Month Day, Year]
Generated: [Day, Date, Time]

---

## Top Signals This Week
[2–3 sentences identifying the most important theme, risk, or pattern that cuts across tools.
This is the one paragraph a busy executive reads when they have 30 seconds.]

---

## Meetings and Outcomes

| Meeting | Date | Attendees | Key Outcome | Follow-Up Needed? |
|---------|------|-----------|-------------|-------------------|
| [name]  | [date] | [names] | [1-sentence outcome] | Yes / No |

---

## Messages Requiring Attention

**Act Now:**
- [ ] [Person] — [Subject or thread topic] — [Why it needs a response] — Received [date]

**This Week:**
- [ ] [Person] — [Subject or thread topic] — [Context] — Received [date]

---

## Decisions Made This Week

- **[Topic]:** [Decision made] — [Who decided / confirmed] — [Date]
- **[Topic]:** [Decision made] — [Who decided / confirmed] — [Date]

---

## Deadlines and Deliverables (Next 7 Days)

| Item | Due Date | Status | Owner |
|------|----------|--------|-------|
| [deliverable] | [date] | On track / At risk | [name] |

---

## Week Ahead Preview

**[Day, Date]**
- [Meeting or commitment] — [Time] — [Who with] — [What to prepare]

**[Day, Date]**
- [Meeting or commitment] — [Time] — [Who with] — [What to prepare]

**Open blocks available for deep work:** [list available times if calendar is connected]

---

## Items to Watch
[Optional: 1–3 things that are not urgent but deserve attention in the coming weeks.
Patterns that are forming, relationships going quiet, projects losing momentum.]

---
*Pulse generated by Cowork | Sources: [list which tools were queried]*
*Missing sources: [list any tools not connected that would improve this briefing]*
```

## Quality Checks

Before delivering the pulse:
- [ ] Top Signals section captures the most important cross-tool theme in plain language
- [ ] Every item in "Messages Requiring Attention" has a clear reason it was flagged
- [ ] Decisions log is factual — no interpretation, just what was decided and by whom
- [ ] Week ahead preview includes preparation notes, not just calendar entries
- [ ] File is saved with correct date-stamped filename
- [ ] Missing tools are noted honestly so the user knows what the briefing could not include
- [ ] Total briefing read time is under 5 minutes
- [ ] No item appears in two sections — each piece of information lives in exactly one place

## Examples

**Example 1 — End-of-week review:**
User types: "Weekly pulse"
Result: Cowork queries Calendar, Gmail, and Slack for the current Mon–Fri window, identifies the top
cross-tool theme, flags messages requiring a response, logs decisions made, and delivers a structured
pulse document saved as `weekly-pulse-[date].md` — ready to read in under 5 minutes.

**Example 2 — Scoped to a client:**
User types: "Weekly pulse for the Acme project"
Result: Cowork scopes the review to activity tagged to the Acme project — calendar events, emails, and
Slack threads involving Acme — and produces a focused pulse rather than a full-professional overview.

**Example 3 — Catching up after time off:**
User types: "I was out last week, give me a business pulse for April 7–11"
Result: Cowork uses the specified date range, pulls from all connected tools, applies the priority filter,
and surfaces only what requires attention — ignoring informational noise from the period away.

## Troubleshooting

**Issue: "Top Signals section is vague or generic"**
This happens when few tools are connected. Connect Calendar and Gmail at minimum. The more tools connected,
the more cross-tool patterns the pulse can identify. If only one tool is available, the pulse will note
which tools are missing and what they would have added.

**Issue: "Pulse includes too many items — hard to read"**
The priority filter (Act Now / This Week / FYI) should limit the length. If the pulse is still too long,
ask: "Give me only the Act Now items from this week's pulse." The skill can re-run the filter at any level
of detail.

**Issue: "Recurring pulse task stopped running"**
Check that the automatic recurring task is still active in your Cowork task settings. If it was paused or
deleted, re-run this skill and say "set this as a recurring task every Friday at 4 PM" to reinstate it.

## Related Skills

See also: **meeting-machine** — for processing individual meetings that show up in the weekly pulse.
Related: **client-context-system** — for scoping a pulse to a specific client workspace.
Related: **weekly-planning-session** (Tier 3) — for translating the pulse into next-week priorities.
