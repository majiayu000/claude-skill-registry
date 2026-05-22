---
name: brief
description: Daily morning brief for PM Extreme Ownership. Surfaces action items, unclaimed opportunities, support ticket pulse, Slack mentions, team board issues, and signals across your issue tracker, support platform, Slack, and email.
argument-hint: "[optional: customer name or area to focus on]"
---

# PM Daily Brief — Extreme Ownership

You are generating a daily brief for a PM who operates with Extreme Ownership. Your job is to surface what matters and reframe every blocker as an action the PM can take right now.

## Data Gathering

Run all of the following in parallel using the tools available (including reading existing friction entries):

### 1. Issue Tracker: My Open Work
Use the issue tracker MCP tools to list issues assigned to "me" ([your name]). Filter for active issues (not Done, not Cancelled/Canceled). For each issue note: ID, title, status, priority, customer name if mentioned, and how long since last update.

### 2. Issue Tracker: Unclaimed Opportunities
Search for recent issues (past 7 days) in the [your team name] team that mention [your product area keywords] in title/description. Look for issues that are unassigned or labeled "Up For Grabs". Exclude Done/Cancelled.

### 3. Support Tickets: Support Pulse
Use Glean search with `app: zendesk` (or your support platform) to find open tickets mentioning [your product area keywords] updated recently. Note: customer, severity, status, assignee. Flag SEV1/SEV2 and SLA breaches.

### 4. Slack Signals
Run TWO Glean searches for Slack:

**a) Mentions of you + threads you participated in:** Run TWO searches: (1) Search `app: slack` for "[your name]" with `updated: past_week`, and (2) Search `app: slack` for `*` with `from: me` and `updated: past_week` to catch threads you replied in but weren't tagged. Merge and deduplicate results. Classify each as:
- **Needs your input** — someone asked you a question or tagged you for review, and you haven't responded (or the thread moved on without your input)
- **You responded, monitor** — you already replied but the thread is still active
- Skip threads you initiated yourself or where no action is needed from you.

**b) Keyword signals:** Search `app: slack` for "[your product area keywords] blocker escalation" with `updated: today` to catch new escalations or customer issues in any channel.

**Note:** Private Slack channels and DMs are NOT indexed by Glean and will not appear in these searches. This is a known blind spot.

### 5. Email
Run THREE Glean searches for email:
**a)** Search `app: gmailnative` for [your product area keywords] with `from: me` and `updated: past_week` — catches threads you sent.
**b)** Search `app: gmailnative` for [your product area keywords] with `updated: past_week` (no from filter) — catches threads where customers replied to you.
**c)** Search `app: gmailnative` for `*` with `from: me` and `updated: today` — catches ALL recent emails involving you, regardless of keywords. Safety net for customer emails that don't use your product area terms.
Merge results, deduplicate. Note if a response is needed. Look for threads updated recently where you haven't replied.

### 6. Call Recordings
Use Glean search with `app: gong` (or your recording tool) for calls from the past 7 days mentioning [your product area keywords] (use `updated: past_week`). Look for: customer pain points or escalations, blockers raised on calls, feature requests, and any negative sentiment. Note: customer name, call participants, and the key signal.

### 7. Existing Friction Log
Read all files in `friction/active/` to know what's already being tracked. This is critical to avoid duplicates when auto-generating new friction entries.

### 8. Team Customer Issues Board
Use issue tracker MCP tools to list issues with `team: [your team board team]` and `label: [your team board label]`. Exclude Done/Resolved/Cancelled. This is your team's customer support board. For each issue note: ID, title, priority, status, assignee, customer name.

This is a **read-only scan** — it surfaces team-wide customer issues so you have full visibility, even on issues not assigned to you. Do NOT auto-create friction entries from this board. Only flag issues here that are Urgent or that have been in the same status for >7 days with no update.

### 9. Weekly Action Tracker
Read the current week's action file at `actions/week-YYYY-MM-DD.md` (where the date is the Monday of this week). If it exists, identify:
- Unchecked items from previous days (these are **carryovers** to surface)
- Actions already logged (to avoid duplicating)

$ARGUMENTS

If a specific customer or area was provided as an argument, prioritize and filter results for that customer/area.

## Output Format

Format the output exactly like this:

The brief is organized into four sections: ACTIONS, CUSTOMER ENGAGEMENTS, SIGNALS, and SUMMARY.

```
Daily Brief — [today's date]

━━━ ACTIONS ━━━

⚡ ACTION NEEDED (waiting on you)
- `[5m]` **[Topic]** — [description] ([source](url))
  -> Your move: [specific action]
- `[30m]` **[Topic]** — [description] ([source](url))
  -> Your move: [specific action]
- `[2h+]` **[Topic]** — [description] ([source](url))
  -> Your move: [specific action]
(Tag each item with effort: [5m] quick, [30m] medium, [2h+] deep work. Sort smallest to largest so quick wins are at the top. Includes carryovers. Items tagged [backlog] do NOT appear here — they only show in /actions list.)

⏳ WAITING ON OTHERS
- **[Topic]** — [description] — waiting on [who] since [date] ([source](url))

🆕 UNCLAIMED OPPORTUNITIES
- [Issue ID](issue-url): [customer] — [summary] — [priority]

━━━ CUSTOMER ENGAGEMENTS ━━━

🤝 ACTIVE ([X] engagements)
[List all open issues from your customer engagements project:]
- [Issue ID](issue-url): [customer] — [current phase/status] — [next action + date if known]
(Flag engagements with no update in >7 days or upcoming calls/demos this week)

━━━ SIGNALS ━━━

💬 SLACK
Needs your input:
- **[Topic]** — [who is waiting, what they need] ([thread](slack-url))
You responded, monitor:
- **[Topic]** — [status summary] ([thread](slack-url))
New signals:
- **[Topic]** — [one-line summary] ([thread](slack-url))
(Use the same bold-topic format as ACTION NEEDED. If a Slack thread is already listed in ACTION NEEDED, do NOT repeat it here — just skip it.)

🎙️ CALL RECORDINGS (past 7 days)
New since last brief run:
- [one-line per notable NEW call] ([call](call-url))
Previously surfaced:
- [one-line summary of calls from earlier briefs this week, with status: handled/monitoring/no action]

📧 EMAIL
- [one-line per thread needing response] ([thread](email-url))

🎫 SUPPORT PULSE
- [X] open support tickets mentioning [your product area]
- SLA risk: [any breaches or near-breaches, linking to each ticket e.g. [#NNNNN](ticket-url)]
- Hottest ticket: [#NNNNN](ticket-url) — [most urgent + why]

🏥 TEAM CUSTOMER ISSUES ([X] open)
[List ALL open issues (exclude Done, Resolved, Cancelled, Closed). Group by priority:]
[Urgent] [Issue ID](issue-url): [customer] — [summary] — [assignee] — [status]
[High] [Issue ID](issue-url): [customer] — [summary] — [assignee] — [status]
[Medium] [Issue ID](issue-url): [customer] — [summary] — [assignee] — [status]
(This section is read-only visibility — no friction entries auto-created from here)

━━━ SUMMARY ━━━

📊 TODAY'S FOCUS
Based on everything above, the single highest-leverage thing you can do for a customer today: [recommendation]

🔥 FRICTION LOG
- Created [N] new / [M] active (run /friction list to review)

📝 ACTION TRACKER
- [X]/[Y] completed today (run /actions list for scorecard)
```

## Auto-Generate Friction Entries

After generating the brief output, consider whether any items warrant a friction entry. Friction is ONLY for situations where the PM personally needs to act to change a customer's situation. Apply this test: **"If I removed myself from the equation, would this issue still get resolved the same way?"** If yes, it's not friction — it's a team issue being handled normally.

Only create friction entries when:
1. **You personally need to step in** — the normal support/eng process isn't enough (e.g., email the customer directly, build a workaround yourself)
2. **A product decision from you** is the blocker — the team is waiting on your direction
3. **The normal system failed** — support dropped the ball, customer escalated, or nothing has moved despite SLA breach

Do NOT create friction for:
- Issues where eng/support is handling it normally through the standard process
- SLA breaches where support is actively working the ticket — that's a support metric, not your friction
- Issues you're just monitoring — tracking is not friction
- Tickets that are progressing, even if slowly
- Items that already have an active friction entry (check `friction/active/` first)

**For each qualifying item**, create a file at `friction/active/[today's date]-[customer-slug].md` using this format:

```markdown
---
customer: [customer name]
opened: [today's date]
status: active
---

## Friction
[One-line: what's slowing the customer down and the impact]

## My Move
[Extracted from the ACTION NEEDED "Your move" line in the brief — reframed as a personal action]

## How I Reduced the Lift
<!-- To be filled as you work on this -->

## Progress
- [today's date]: Identified in daily brief. [brief context on current state]
```

If running the brief on subsequent days and friction entries already exist for the same customer+topic, do NOT create duplicates. Instead, append a progress entry to the existing file with any new information from today's brief.

## Auto-Generate Weekly Action Items

After generating friction entries, update the weekly action tracker at `actions/week-YYYY-MM-DD.md` (Monday of current week):

1. If the file doesn't exist, create it with `# Week of YYYY-MM-DD`.
2. Add a section for today: `## [DayName] YYYY-MM-DD` with a `### From Brief` subsection.
3. Generate one checkbox action item (`- [ ]`) for each:
   - ACTION NEEDED item (from the brief)
   - Notable call signal that warrants follow-up
   - Slack signal that needs your response
   - Email thread needing a reply
   - Unclaimed opportunity worth claiming
4. Each item must include: customer name, one-line action, and a linked source.
5. For items that also have a `friction/active/` entry, still add an action item but prefix with a fire indicator and reference the friction file. This ensures friction items appear on the weekly scorecard and nothing falls through the cracks.
6. If previous days in the same week have unchecked items, fold them into ACTION NEEDED (sorted by staleness, oldest first). No separate carryovers section.

## Critical Rules

1. For EVERY item in ACTION NEEDED, apply these Extreme Ownership reframes — do NOT just state blockers:
   - "CX isn't moving" -> How can I engage the customer directly?
   - "Engineering isn't prioritizing" -> What path can I create given their constraints?
   - "They don't have bandwidth" -> How can I reduce the lift for them?
   - "I've asked someone to handle it" -> Can I learn to do this myself?
   - "I'm blocked" -> What can I do right now while working on removing this blocker?

2. **Classify "assigned to me" correctly.** Before putting an issue in ACTION NEEDED, check the latest comments and Slack threads. If your last action was a response/question and the thread is waiting on someone else, put it in WAITING ON OTHERS instead. Only items where you genuinely need to take the next step belong in ACTION NEEDED.
3. **Persist signals across same-day runs.** When the brief is run multiple times in the same day, signals from earlier runs must carry forward. Show new signals as "New since last run" and earlier signals as "Previously surfaced" with their current status. Do not drop signals between runs.
4. **Link EVERYTHING.** Every reference to a source must be a clickable link — issues, support tickets, Slack threads, email threads, call recordings. Use markdown link syntax `[display text](url)`. If a URL was returned by a tool, use it. No bare IDs without links.
5. Keep the brief output (excluding the friction log section) under 60 lines. Be terse. No filler.
6. If there are no items in a section, write "Clear" and move on.
7. Sort ACTION NEEDED by priority (Urgent > High > Medium > Low), then by staleness (longest-waiting first).
