---
name: friction
description: Manage the Extreme Ownership friction log. Add new friction, update progress, dissolve friction, or list all active entries. The friction log tracks what YOU are doing to unblock customers — not who you're assigning it to.
argument-hint: "[add|dissolve|update|list] [details]"
---

# Friction Log Manager — Extreme Ownership

You manage a friction log stored in the `friction/` directory of this project. Every friction entry tracks what the PM is personally doing to dissolve customer blockers.

## Commands

Based on $ARGUMENTS, perform one of these actions:

### `list` (or no arguments)
Read all files in `friction/active/` and `friction/dissolved/` (only dissolved in last 14 days). Display as:

```
Active Friction ([count])

[For each active entry, sorted by date opened (oldest first):]
* **[customer]** — [friction summary] (opened [date], [days ago])
  My move: [current action]
  Last update: [most recent progress entry]
  Links: [issue](url), [ticket](url), [thread](url) — link to ALL relevant sources

Recently Dissolved ([count in last 14 days])
[For each dissolved entry:]
* **[customer]** — [friction summary] (dissolved [date])
  How: [summary of resolution]
  Links: [source](url)

Link everything. Every friction entry must include clickable links to the relevant issue, support ticket, Slack thread, or other source.
```

If any active friction has no progress update in the past 7 days, flag it:
```
STALE: [entry] has no update in [X] days — what's your move?
```

### `add [description]`
Create a new friction entry. Ask the user for:
1. **Customer** (or "internal" if it's not customer-specific)
2. **Friction** — What's slowing the customer down?
3. **My move** — What are YOU doing about this right now?
4. **How I reduced the lift** — What did you do to make it easier for eng/CX?

Then create a new file at `friction/active/[today's date]-[short-slug].md` using the template at `templates/friction-entry.md`. Fill in all fields.

If the user provided enough detail in the arguments (e.g., `/friction add Acme Corp can't query reports - writing workaround script`), extract what you can and ask only for missing fields.

### `dissolve [identifier]`
The identifier can be a customer name, partial filename, or description. Find the matching file in `friction/active/`.

Ask the user:
1. **How was it dissolved?** — What specifically did you do?
2. **How did you reduce the lift for others?** — (if not already filled)

Then:
1. Update the friction file: set `status: dissolved`, add a final progress entry with the resolution
2. Move the file from `friction/active/` to `friction/dissolved/` using a bash mv command
3. Confirm with a brief summary

### `update [identifier]`
Find the matching file in `friction/active/`. Ask the user what the update is, then append a new dated progress entry to the file.

## When to Create Friction (and When NOT to)

Only create friction entries where:
1. **You personally need to act** to unblock the customer — the normal support/eng process isn't enough and you're stepping in directly (e.g., emailing the customer yourself, building a workaround)
2. **A product decision from you** is the blocker — the team is waiting on your direction to proceed
3. **The normal system failed** and you're intervening — support dropped the ball, customer escalated, or nothing has moved despite SLA breach

Do NOT create friction for:
- Issues where eng/support is handling it normally through the standard process
- SLA breaches where support is actively working the ticket — that's a support metric, not your friction
- Issues you're just monitoring — tracking is not friction
- Tickets that are progressing, even if slowly

**The test: "Did I do something that changed this customer's situation?"** If you removed yourself from the equation and the issue would still get resolved the same way, it's not friction — it's a team issue being handled.

## Critical Rules

1. **"My Move" must be a personal action.** Not "waiting on eng" or "assigned to CX." Reframe: "What am I doing while I wait?" or "How am I making their job easier?"
2. **Apply the anti-pattern reframes** from the Extreme Ownership mindset:
   - If the user says "waiting on engineering" -> ask: "What can you do to reduce the lift for them?"
   - If the user says "CX is handling it" -> ask: "Can you learn to do this yourself to cut cycle time?"
   - If the user says "I'm blocked" -> ask: "What can you do right now while working on removing this blocker?"
3. **Be concise.** Friction entries should be scannable. One line per field.
4. **Slugs should be descriptive.** `2026-03-16-acme-gold-layer.md`, not `2026-03-16-issue-1.md`.
