---
name: briefing
description: Daily and weekly briefings with calendar, tasks, and people context. Handles "Daily briefing", "What's my day look like?", "Weekly planning", "Plan my week". Morning and weekly planning workflows.
user-invocable: true
help:
  purpose: |-
    Daily and weekly briefings with calendar, tasks, and context.
  use_cases:
    - "Daily briefing"
    - "What's my day look like?"
    - "Weekly briefing"
    - "Plan my week"
  scope: briefing,calendar,tasks,planning
---

# Briefing protocol

Unified protocol for daily and weekly briefings. Mode is determined by the request signal.

**Parallelization**: Data gathering (calendar, tasks, memory) runs as **three parallel sub-agents** using the Task tool. This reduces wall-clock time for briefing generation, since calendar queries, task queries, and memory lookups are independent operations.

---

## Daily mode

Generate a focused morning briefing for clarity and prioritization.

### Steps

1. **Determine date and read integrations**
   - Today's date (if after 5 PM, brief for tomorrow)
   - Output folder: `journal/YYYY-MM/`
   - Read `reference/integrations.md` to determine available integrations and their status

2-4. **Parallel data gathering (sub-agents)**

Spawn **three parallel sub-agents** using the Task tool. **Launch all three in a single message** using multiple Task tool calls.

##### Sub-agent A: Fetch calendar

```
Read reference/integrations.md Calendar section for provider details.
Check calendar integration status; if not configured, return {"status": "not_configured"}.
Resolve {target_date} to YYYY-MM-DD format.
Execute the list_events operation with {target_date} and offset=1.
For each event extract: time, title, attendee names.

Return JSON:
{
  "status": "ok" | "not_configured" | "error",
  "events": [{"time": "...", "title": "...", "attendees": ["..."]}],
  "error": null | "description"
}
```

##### Sub-agent B: Fetch tasks

```
Read reference/integrations.md Tasks section for provider details.
Execute the list operation for the primary task list (default: Active).
Identify tasks due {target_date} or highest priority.
Execute the overdue operation to check for overdue tasks.

Return JSON:
{
  "status": "ok" | "not_configured" | "error",
  "tasks_due_today": [{"title": "...", "due": "...", "list": "..."}],
  "overdue": [{"title": "...", "due": "...", "list": "..."}],
  "top_priority": [{"title": "...", "due": "...", "list": "..."}],
  "error": null | "description"
}
```

##### Sub-agent C: Query memory

```
Read memory/people/_index.md.
Look up profiles for these meeting attendees: {attendee_names_if_known}
Read memory/initiatives/_index.md and find relevant initiative context.
Read reference/schedule.md if it exists; identify [RECURRING] and [ONCE] items due {target_date}.
Read inbox/pending/ and count pending items.
Read reference/.housekeeping-state.yaml for last housekeeping run.
Read reference/maturity.yaml for maturity level.

Return JSON:
{
  "people_context": [{"name": "...", "summary": "...", "open_items": ["..."]}],
  "initiative_context": [{"name": "...", "status": "..."}],
  "scheduled_items": [{"type": "recurring|once", "description": "..."}],
  "inbox_count": 0,
  "housekeeping_last_run": "YYYY-MM-DD",
  "maturity": {"level": 1, "people": 0, "meetings_processed": 0}
}
```

**Note on attendee names**: If calendar data is not yet available when spawning sub-agents (common case), spawn the memory sub-agent without attendee names. After the calendar sub-agent returns, do a quick targeted lookup for any attendees not covered. Alternatively, the memory sub-agent can load the full people index for cross-referencing after calendar results arrive.

##### Sub-agent input/output contracts (daily mode)

| Sub-agent | Input | Output | Failure mode |
|-----------|-------|--------|-------------|
| Calendar | integrations.md, target date | JSON: events list with times, titles, attendees | Return `status: error`, briefing proceeds without calendar data |
| Tasks | integrations.md, target date | JSON: due today, overdue, top priority tasks | Return `status: error`, briefing proceeds without task data |
| Memory | people index, initiatives index, schedule.md, inbox/, maturity.yaml | JSON: people context, initiative context, scheduled items, system status | Return partial data, briefing uses what is available |

After all three sub-agents complete, collect their JSON results and proceed to synthesis.

5. **Cross-reference and enrich**
   - Match calendar attendees against memory people context
   - For any attendees not covered by the memory sub-agent, do a targeted memory lookup
   - Link tasks to upcoming meetings where relevant

6. **Check inbox**
   - Use inbox count from memory sub-agent results
   - Offer to process pending items if any exist

7. **Generate briefing**

```markdown
### Today's schedule
- Chronological list with time, title, prep needed

### Scheduled items due today
- Recurring and one-time items from reference/schedule.md

### Priority tasks
- Top 3-5 tasks for today
- Flag tasks that should be done before specific meetings

### People I'm meeting
- Brief context for each person
- Open items or follow-ups with them
- Questions to ask or responses owed

### Focus opportunities
- Open time slots for deep work
- Suggested task for each slot

### System status
- TARS maturity: Level [N] ([X] people, [Y] meetings). Next: [milestone]
- Inbox: [N] items pending
- Last housekeeping: [date]
```

8. **Save and display**
   - Save to `journal/YYYY-MM/YYYY-MM-DD-daily-briefing.md`
   - Display directly to user

---

## Weekly mode

Generate a comprehensive weekly briefing for strategic planning.

### Steps

1. **Determine date range and read integrations**
   - Current week: Monday through Sunday
   - Last week: Previous Monday through Sunday
   - Output folder: `journal/YYYY-MM/`
   - Read `reference/integrations.md` to determine available integrations and their status

2-4. **Parallel data gathering (sub-agents)**

Spawn **three parallel sub-agents** using the Task tool. **Launch all three in a single message.**

##### Sub-agent A: Fetch calendar (weekly)

```
Read reference/integrations.md Calendar section for provider details.
Check calendar integration status; if not configured, return {"status": "not_configured"}.
Resolve {monday_date} to YYYY-MM-DD format.
Execute the list_events operation with {monday_date} and offset=7.
Identify high-priority meetings (executives, leadership, key stakeholders).
Identify open time slots.

Return JSON:
{
  "status": "ok" | "not_configured" | "error",
  "events": [{"date": "...", "time": "...", "title": "...", "attendees": ["..."], "priority": "high|normal"}],
  "open_slots": [{"date": "...", "start": "...", "end": "...", "duration_minutes": 0}],
  "error": null | "description"
}
```

##### Sub-agent B: Fetch tasks (weekly)

```
Read reference/integrations.md Tasks section for provider details.
Execute the list operation for all configured lists (default: Active, Delegated, Backlog).
Execute the overdue operation.
Identify tasks due this week ({monday_date} through {sunday_date}).
Identify tasks related to meeting topics if known.

Return JSON:
{
  "status": "ok" | "not_configured" | "error",
  "tasks_due_this_week": [{"title": "...", "due": "...", "list": "...", "owner": "..."}],
  "overdue": [{"title": "...", "due": "...", "list": "..."}],
  "backlog_stale": [{"title": "...", "created": "...", "days_old": 0}],
  "completed_last_week": [{"title": "...", "completed": "..."}],
  "error": null | "description"
}
```

##### Sub-agent C: Query memory and context (weekly)

```
Read memory/people/_index.md + profiles of frequent meeting attendees.
Read memory/initiatives/_index.md + active initiative details.
Identify responses owed and follow-ups needed.
Read journal/{last_week_month}/_index.md for last week entries.
Read reference/schedule.md if it exists; identify items due this week.
Read inbox/pending/ and count pending items.
Read reference/.housekeeping-state.yaml for last housekeeping and index rebuild dates.
Read reference/maturity.yaml for maturity level.

Return JSON:
{
  "people_context": [{"name": "...", "summary": "...", "responses_owed": ["..."], "follow_ups": ["..."]}],
  "initiatives": [{"name": "...", "status": "...", "milestones_this_week": ["..."]}],
  "last_week_entries": [{"date": "...", "type": "...", "title": "..."}],
  "scheduled_items": [{"type": "recurring|once", "description": "...", "due": "..."}],
  "inbox_count": 0,
  "housekeeping_last_run": "YYYY-MM-DD",
  "last_index_rebuild": "YYYY-MM-DD",
  "maturity": {"level": 1, "people": 0, "meetings_processed": 0}
}
```

##### Sub-agent input/output contracts (weekly mode)

| Sub-agent | Input | Output | Failure mode |
|-----------|-------|--------|-------------|
| Calendar | integrations.md, monday date, offset=7 | JSON: events, open slots, priority flags | Return `status: error`, briefing proceeds without calendar |
| Tasks | integrations.md, date range | JSON: due this week, overdue, stale backlog, completed last week | Return `status: error`, briefing proceeds without tasks |
| Memory/Context | people index, initiatives index, journal index, schedule, inbox, system state | JSON: people context, initiatives, last week summary, system status | Return partial data, briefing uses what is available |

After all three sub-agents complete, collect their JSON results and proceed to synthesis.

5. **Cross-reference and enrich**
   - Match calendar attendees against memory people context
   - Link tasks to meeting topics
   - Identify preparation needed for high-priority meetings
   - Match open time slots with highest priority tasks

6. **Generate briefing**

```markdown
### Last week summary
- Achievements (completed tasks, delivered items)
- Planned but incomplete (with reasons if known)

### This week's meetings
- **High-priority**: Leadership, clients, board meetings (flag)
- **All meetings**: Chronological with date/time, title, purpose

### Open tasks
- **Due this week**: Tasks with explicit due dates
- **Meeting-related**: Tasks connected to meeting topics
- **Preparation needed**: Items requiring work before meetings

### Milestones and initiatives
- Current week milestones
- Upcoming milestones needing advance preparation
- Initiative status updates

### People context
- **Responses owed**: Promises or follow-ups to people I'm meeting
- **Questions to ask**: Follow-up items or open threads

### Recommended focus time
- Open slots matched with highest priority tasks
- Specific time blocks with suggested assignments

### Backlog review
- Backlog items older than 90 days (flag as stale)
- Suggest: keep, reprioritize, or remove

### System status
- TARS maturity: Level [N] ([X] people, [Y] meetings). Next: [milestone]
- Inbox: [N] items pending
- Last housekeeping: [date]
- Last index rebuild: [date]
```

7. **Save and display**
   - Save to `journal/YYYY-MM/YYYY-MM-DD-weekly-briefing.md`
   - Display key highlights to user

---

## Progress tracking (TodoWrite)

Use the `TodoWrite` tool to give the user real-time visibility into briefing generation. Create the todo list at the start and update as steps complete:

**Daily mode:**
```
1. Determine date and read integrations                  [in_progress → completed]
2. Fetch calendar data (parallel sub-agent)              [pending → completed]
3. Fetch task data (parallel sub-agent)                  [pending → completed]
4. Query memory and context (parallel sub-agent)         [pending → completed]
5. Cross-reference and enrich data                       [pending → completed]
6. Generate and save briefing                            [pending → completed]
```

**Weekly mode:**
```
1. Determine date range and read integrations            [in_progress → completed]
2. Fetch calendar data (parallel sub-agent)              [pending → completed]
3. Fetch task data (parallel sub-agent)                  [pending → completed]
4. Query memory and context (parallel sub-agent)         [pending → completed]
5. Cross-reference and enrich data                       [pending → completed]
6. Generate and save briefing                            [pending → completed]
```

**Parallelization note**: Steps 2, 3, and 4 run concurrently as sub-agents. Mark ALL THREE as `in_progress` when spawning them. Mark each `completed` as its sub-agent returns. Do not wait for all three before updating individual statuses.

---

## Frontmatter (both modes)

```yaml
---
date: YYYY-MM-DD
title: Daily Briefing | Weekly Briefing
type: briefing-daily | briefing-weekly
---
```

---

## Context budget
- Memory: Read `_index.md` for people and initiatives + up to 5 targeted files
- Tasks: Execute task integration `list` operation for Active (+ all lists for weekly mode)
- Calendar: Execute calendar integration `list_events` operation for today (daily) or full week (weekly)
- Journal: Current month `_index.md` for last week summary (weekly only)
- Inbox: Read `inbox/pending/` file list
- System: Read `reference/.housekeeping-state.yaml` and `reference/maturity.yaml`

---

## Absolute constraints

- NEVER skip calendar lookup (fall back to tasks-only if calendar integration is unreachable)
- NEVER output briefing without saving to journal
- ALWAYS resolve dates to `YYYY-MM-DD` format before any calendar query
- ALWAYS look up memory profiles for meeting attendees
- ALWAYS flag overdue tasks (via task integration `overdue` operation)
- ALWAYS check calendar integration constraints in reference/integrations.md before querying
