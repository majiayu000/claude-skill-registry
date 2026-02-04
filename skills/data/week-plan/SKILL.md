---
name: week-plan
description: Set weekly priorities and plan the week ahead with intelligent suggestions based on goals, calendar shape, and task effort.
---

## Purpose

Set priorities and plan the week ahead. Now with **intelligent priority suggestions** based on quarterly goals, calendar capacity, and task effort classification.

## Usage

- `/week-plan` — Plan current week (or next week if run on Friday/weekend)
- `/week-plan next` — Explicitly plan next week
- `/week-plan current` — Force planning current week

---

## When to Use

**Best times:**
- **Monday morning** - Before diving into daily work
- **Friday evening** - Set up next week while context is fresh
- **Sunday evening** - Weekend planning session

---

## Step 0: Demo Mode Check

Check `System/user-profile.yaml` for `demo_mode`. If true, use demo paths.

---

## Step 1: Determine Target Week

Calculate target week (current or next) based on day of week and user parameter.

---

## Step 2: Context Gathering (ENHANCED)

Gather comprehensive context to inform **intelligent priority suggestions**.

### 2.1 Last Week's Review

Check for `00-Inbox/Weekly_Synthesis_[last-monday].md`:
- "Next Week" section → Suggested priorities
- "Carried Over" section → Unfinished tasks
- "Blocked Items" → Things that need resolution
- "Learnings" → Insights to apply

### 2.2 Quarterly Goals Status

```
Use: get_quarterly_goals()
Use: get_goal_status(goal_id) for each goal
```

For each goal, get:
- Current progress (concrete: "2 of 5 milestones complete")
- Linked priorities count
- Weeks since last activity
- Stall warnings

**Identify goals needing attention:**
- Goals with no linked priorities (orphaned)
- Goals with no activity in 2+ weeks (stalled)
- Goals behind expected pace

### 2.3 Open Tasks and Projects

```
Use: list_tasks(include_done=False)
```

Get all open tasks and:
- Classify by effort (deep_work / medium / quick)
- Group by pillar alignment
- Identify P0/P1 items
- Find tasks that could advance stalled goals

### 2.4 Calendar Shape Analysis (NEW)

```
Use: analyze_calendar_capacity(days_ahead=7, events=[...from calendar MCP...])
```

Understand the **shape of the week**:

| Day | Type | Largest Block | Best For |
|-----|------|---------------|----------|
| Mon | Stacked (7 meetings) | 45 min | Quick tasks only |
| Tue | Moderate (4 meetings) | 90 min | Medium tasks |
| Wed | **Open** (2 meetings) | **3 hours** | **Deep work day** ✨ |
| Thu | Stacked (6 meetings) | 30 min | Quick tasks only |
| Fri | Moderate (3 meetings) | 2 hours | Medium tasks, wrap-up |

**Week capacity summary:**
- Deep work opportunities: {{count}} days with 2+ hour blocks
- Total deep work hours available: ~{{X}} hours
- Stacked days to avoid scheduling deep work: {{list}}

### 2.5 Task-to-Time Matching (NEW)

```
Use: classify_task_effort(title) for key tasks
Use: suggest_task_scheduling(include_all_tasks=True, calendar_events=[...])
```

Get intelligent matching:
- Which tasks need deep work time?
- Which can fit in gaps?
- Are there enough slots for all deep work?

**Capacity check:**

> "You have 5 deep work tasks totaling ~12 hours.
> You have 2 open days with ~6 hours of deep work capacity.
> 
> ⚠️ **Capacity gap:** Consider deferring 2 deep work items or protecting more time."

### 2.6 Commitments and Follow-ups

```
Use: get_commitments_due(date_range="this_week")
```

Surface things you've committed to that are due this week.

---

## Step 3: Intelligent Priority Suggestions (NEW)

**Don't just ask "What are your Top 3?" — Suggest priorities based on analysis.**

### 3.1 Generate Suggestions

Based on the gathered context, generate 4-5 suggested priorities:

**Goal-driven suggestions:**
- "Goal X has no activity in 3 weeks. Suggested priority: {{specific work that advances it}}"
- "Goal Y is at 2 of 5 milestones with 6 weeks left. Suggested priority: Complete milestone 3"

**Commitment-driven suggestions:**
- "You committed to {{X}} with {{person}} — due this week"

**Carried-over suggestions:**
- "{{Priority}} carried over from last week — still important?"

**Calendar-aware suggestions:**
- "You have a deep work day Wednesday — good time for {{specific deep work task}}"
- "Friday is light — good for {{wrap-up task}}"

### 3.2 Present Suggestions

> "Based on your goals, tasks, and calendar shape, here's what I suggest for this week:
> 
> **Suggested priorities:**
> 
> 1. **Complete pricing proposal** — Goal 1 (Launch v2.0) needs this to hit milestone 3. You have deep work time Wednesday.
> 
> 2. **Customer interview batch** — Goal 2 (Improve NPS) has no activity in 3 weeks. You could do 2-3 calls on Tue/Thu between meetings.
> 
> 3. **Follow up on Acme contract** — Committed to Sarah by Friday. Meeting Thursday, prep needed.
> 
> 4. **Review team roadmap** — Carried over from last week. Still a priority?
> 
> **Calendar fit:**
> - Priority 1 → Wednesday (3-hour block)
> - Priority 2 → Tue/Thu (between meetings)
> - Priority 3 → Friday (follow-up after Thursday meeting)
> 
> **Does this feel right?** Adjust as needed."

### 3.3 Interactive Refinement

Wait for user to confirm, adjust, or provide different priorities. For each priority confirmed:

```
Use: create_weekly_priority(
  title="...",
  pillar="...",
  quarterly_goal_id="..." or "operational",
  success_criteria="...",
  week_date="YYYY-MM-DD"
)
```

---

## Step 4: Skills Gap Check (if Career system enabled)

If `05-Areas/Career/` exists, check for stale skills that could be developed this week.

---

## Step 5: PKM Improvement Check (Optional)

Check `System/Dex_Backlog.md` for high-priority improvement ideas worth tackling this week.

---

## Step 6: Generate Week Priorities File

Archive old file to `07-Archives/Plans/YYYY-Wxx.md`.

Create updated `02-Week_Priorities/Week_Priorities.md`:

```markdown
# Week Priorities

**Week of:** [Monday YYYY-MM-DD]

---

## 📊 Week Shape

| Day | Type | Deep Work? | Notes |
|-----|------|------------|-------|
| Mon | Stacked | ❌ | 7 meetings |
| Tue | Moderate | ⚠️ | 90 min block PM |
| Wed | **Open** | ✅ | **Deep work day** (3h morning) |
| Thu | Stacked | ❌ | 6 meetings |
| Fri | Moderate | ⚠️ | 2h block |

**Deep work capacity:** ~5 hours this week
**Best day for focus:** Wednesday

---

## 🎯 Quarterly Goals Context

| Goal | Progress | Status |
|------|----------|--------|
| Launch Product v2.0 | 3 of 5 milestones | On track |
| Improve Customer NPS | 1 of 4 milestones | ⚠️ Stalled (3 weeks) |
| Build Team Capacity | 2 of 3 milestones | On track |

**This week advances:** Goals #1 and #2

---

## 🎯 Top 3 This Week

1. **[Priority 1]** — **[Pillar]** ^week-YYYY-WXX-p1
   - Success criteria: [What done looks like]
   - Quarterly goal: [Q1 Goal #X]
   - **Scheduled:** [Day/time block]
   - Effort: [deep_work / medium / quick]
   
2. **[Priority 2]** — **[Pillar]** ^week-YYYY-WXX-p2
   - Success criteria: [What done looks like]
   - Quarterly goal: [Q1 Goal #X]
   - **Scheduled:** [Day/time block]
   - Effort: [deep_work / medium / quick]
   
3. **[Priority 3]** — **[Pillar]** ^week-YYYY-WXX-p3
   - Success criteria: [What done looks like]
   - Quarterly goal: [Q1 Goal #X] or Operational
   - **Scheduled:** [Day/time block]
   - Effort: [deep_work / medium / quick]

---

## ⚡ Commitments Due This Week

- [ ] [Commitment] — to [person] — due [day]
- [ ] [Commitment] — from [meeting] — due [day]

---

## 📋 Tasks by Priority

### Must Complete (P0)
- [ ] [Task] — Supports: Priority #X — **[Day]**

### Should Complete (P1)
- [ ] [Task] — Supports: Priority #X — **[Day]**

### If Time Permits (P2)
- [ ] [Task]

---

## 📅 Key Meetings

| Day | Time | Meeting | Prep Needed | Related Priority |
|-----|------|---------|-------------|------------------|
| Mon | [Time] | [Meeting] | [Prep] | Priority #X |
| Tue | [Time] | [Meeting] | [Prep] | — |

---

## 📊 Pillar Balance

| Pillar | This Week | Balance |
|--------|-----------|---------|
| [Pillar 1] | [Brief description] | 🟩 Good |
| [Pillar 2] | [Brief description] | 🟨 Light |
| [Pillar 3] | [Brief description] | 🟥 Neglected |

---

## 🔄 Carried Over

- [ ] [Task from last week] — [Why it carried over]

---

## 🏁 End of Week Review

*Fill in on Friday*

### Completed
- 

### Didn't Finish
- 

### Learnings
- 

### Next Week Focus
- 

---

*Generated: [Timestamp]*
*Command: /week-plan*
```

---

## Step 7: Track Usage (Silent)

Update `System/usage_log.md`.

---

## Step 8: Summary

After generating the file, provide a summary:

> "Week planned! Saved to `02-Week_Priorities/Week_Priorities.md`
> 
> **Your Top 3 this week:**
> 1. [Priority 1] — Scheduled for [Day]
> 2. [Priority 2] — Scheduled for [Day]
> 3. [Priority 3] — Scheduled for [Day]
> 
> **Week shape:** 2 stacked days, 1 deep work day (Wednesday)
> 
> **Goals advancing:** #1 and #2
> 
> **Heads up:** 
> - [Capacity warning if applicable]
> - [Stalled goal reminder]
> 
> Ready to run `/daily-plan` for Monday?"

---

## MCP Dependencies (Updated)

| Integration | MCP Server | Tools Used |
|-------------|------------|------------|
| Calendar | dex-calendar-mcp | `calendar_get_events_with_attendees` |
| Work | dex-work-mcp | `list_tasks`, `get_quarterly_goals`, `get_goal_status`, `create_weekly_priority`, `analyze_calendar_capacity`, `classify_task_effort`, `suggest_task_scheduling`, `get_commitments_due` |
| Granola | dex-granola-mcp | `get_upcoming_meetings` (optional) |
