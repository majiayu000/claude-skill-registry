---
name: morning-routine
description: "Orchestrates a full morning sweep of pending items (email, tasks, Slack, WhatsApp, X). Use when the user asks for a sweep, morning routine, inbox sweep, or all pending items."
---

# Morning Routine (sweep)

## Goal
Deliver a complete summary of active pending items in a single response.
Omit any source with no results.

## Sources
- Email (skill: email)
- Tasks (justdoit)
- Slack (skill: slack)
- WhatsApp (skill: whatsapp-evo)

## Flow
1) Run ALL sources in parallel (use parallel Bash tool calls or background tasks). Do NOT run them sequentially.
2) Email: run `scripts/email-inbox` (from the email skill folder) and **render the output exactly using the email skill's format/triage** (includes rules and emojis). Do not reinterpret or change its rules.
3) Tasks: run `justdoit next --ids` and show the full output **without** the suffixes ` (due YYYY-MM-DD)` or ` [id: ...]`. Keep sections (Today/This week/Backlog) and calendar lines.
4) Slack: run `scripts/slack-inbox --json-out /tmp/slack-inbox.json` and show only the clean list. Save metadata. Use a **60-second timeout**.
5) WhatsApp: run `scripts/whatsapp-inbox --json-out /tmp/whatsapp-inbox.json` and show only the clean list. Save metadata.
6) Wait for all parallel calls to finish, then assemble the output in order: Email, Tasks, Slack, WhatsApp.
7) If a source returns no results, omit it from the output.
8) If a source times out, include it in the Incidents section instead of blocking the whole sweep.
9) Do not propose actions or replies (except the email triage emojis). Only report.
10) If there are errors or missing credentials, include an "Incidents" section with the exact error.

## Output format
- Include sections only for sources with results.
- Do not truncate lists.
- Suggested format:

**Email**
<clean list>

**Tasks**
<full justdoit output without due/ids>

**Slack**
<clean list>

**WhatsApp**
<clean list>

**Incidents**
- <source>: <exact error>

## Extensibility
To add a new source:
- Add it to the order in "Flow".
- Define the base command and where it stores metadata.
- Include its section in "Output format".
- Keep the rule of omitting sources with no results.
