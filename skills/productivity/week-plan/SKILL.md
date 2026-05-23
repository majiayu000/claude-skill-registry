---
name: week-plan
description: Set weekly priorities and plan the week ahead
---

## Purpose

Set priorities and plan the week ahead. Can be run on Monday morning to plan the current week, or Friday evening to plan next week.

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

Before anything else, check if demo mode is active:

1. Read `System/user-profile.yaml`
2. Check `demo_mode` value
3. **If `demo_mode: true`:**
   - Use demo paths: `System/Demo/00-Inbox/`, `System/Demo/Active/`, etc.
   - Skip calendar/task integrations (use sample data)
4. **If `demo_mode: false`:** Proceed normally

---

## Step 1: Determine Target Week

**If no parameter or "current":**
- If today is Mon-Thu → Plan current week
- If today is Fri-Sun → Offer choice: "Plan current week or next week?"

**If parameter is "next":**
- Plan next Monday's week

Calculate:
- `target_week_start` (Monday of target week)
- `target_week_end` (Sunday of target week)

---

## Step 2: Context Gathering

Gather context to inform planning:

### From Last Week's Review

Check for `00-Inbox/Weekly_Synthesis_[last-monday].md`:

**If exists, extract:**
- "Next Week" section → Suggested priorities
- "Carried Over" section → Unfinished tasks
- "Blocked Items" → Things that need resolution
- "Learnings" → Insights to apply

**If missing:**
- Note that no review exists
- Suggest running `/week-review` for last week

### From 03-Tasks/Tasks.md

```
Use: list_tasks (if Work MCP enabled)
```

Extract:
- P0 and P1 tasks
- Overdue items
- Tasks without dates that need scheduling
- Blocked tasks

### From Calendar (if enabled)

```
Use: calendar_get_events_with_attendees for target week
```

Extract:
- All meetings for the week
- Key meetings that need prep
- Back-to-back days
- Free time blocks

### From Current Week Priorities

Read `02-Week_Priorities/Week_Priorities.md`:
- Last week's Top 3
- What was completed vs carried over
- End of week review notes (if filled in)

### From Pillars

Read `System/pillars.yaml`:
- Strategic pillars
- Check recent balance (from last few weeks)
- Identify neglected areas

### From Quarterly Goals (if enabled)

Read `System/user-profile.yaml` to check if `quarterly_planning.enabled: true`:

**If quarterly planning is enabled:**
- Use `get_quarterly_goals()` MCP tool to fetch goals
- Use `get_goal_status(goal_id)` for each goal to check:
  - Progress percentage
  - Linked priorities count
  - Stall warnings (no activity in >2 weeks)
- Identify which goals need attention this week

**If quarterly planning is disabled:**
- Skip this section entirely

---

## Step 3: Interactive Planning

Present context and guide user through planning:

### Review Last Week (if available)

> "Last week's Top 3 were:
> 1. [Priority 1] — ✅ Done
> 2. [Priority 2] — 🔄 In progress
> 3. [Priority 3] — ❌ Didn't get to it
>
> What carried over that's still important?"

Wait for user input, extract carried-over items.

### Present Quarterly Context (if enabled)

**If quarterly planning is enabled:**

Use `get_quarterly_goals()` and `get_goal_status(goal_id)` to build context:

> "**Your Q1 2026 goals:**
> 1. [Goal 1] — [Pillar] — Progress: [X%] [🟢/🟡/🔴] — [N] priorities linked
> 2. [Goal 2] — [Pillar] — Progress: [Y%] [🟢/🟡/🔴] — [N] priorities linked
> 3. [Goal 3] — [Pillar] — Progress: [Z%] [🟢/🟡/🔴] — ⚠️ No activity (stalled)
> 
> **Goals needing attention:**
> - Goal 3 has no linked priorities yet
> 
> Which of these quarterly goals are you pushing forward this week?"

Wait for user to identify 1-2 quarterly goals this week advances.

**If quarterly planning is disabled:**
- Skip this section

### Skills Gap Check (if Career system enabled)

**If `05-Areas/Career/` exists:**

Use Career MCP `skills_gap_analysis` tool:
- Call with `lookback_days: 90` (check last 3 months)
- Call with `stale_threshold_days: 42` (6 weeks)

**If gaps or stale skills found, surface warning:**

> "⚠️ **Career development note:**
> 
> You haven't worked on these skills recently:
> - **[Stale Skill 1]**: No activity in [X] days — Required for [target level]
> - **[Gap Skill 1]**: Not being developed — Required for [target level]
> 
> Consider adding a priority this week that develops one of these."

**If no gaps:** Skip this section.

---

### Review Upcoming Week

> "Looking at next week (Mon [Date] - Fri [Date]):
> 
> **Key meetings:**
> - Mon: [Meeting 1], [Meeting 2]
> - Wed: [Meeting 3]
> - Thu: [Meeting 4]
> 
> **Open tasks:**
> - P0: [Count] must-do items
> - P1: [Count] important items
> 
> Any of these meetings need special prep or follow-up?"

Wait for user input.

### Define Top 3

> "What are the 3 most important outcomes for this week?
> 
> These should be specific results, not just activities. For example:
> - ✅ 'Ship v2.0 to production'
> - ❌ 'Work on v2.0'
> 
> What's your Top 3?"

Wait for user to provide 3 priorities. For each priority collected, use `create_weekly_priority` MCP tool:

```bash
create_weekly_priority(
  title: "[Priority title]",
  pillar: "[pillar_id]",
  quarterly_goal_id: "[Q1-2026-goal-X]" or "operational",
  success_criteria: "[What success looks like]",
  week_date: "[YYYY-MM-DD Monday]"
)
```

For each, ask:
- Which pillar does this align with?
- **If quarterly planning enabled:** Which quarterly goal does this advance? (provide goal_id, or mark as "operational")
- What's the success criteria?

### Map Tasks to Priorities

> "Here are your open P0/P1 tasks:
> - [ ] [Task 1]
> - [ ] [Task 2]
> - [ ] [Task 3]
> 
> Which of these support your Top 3? Any that should be rescheduled or de-prioritized?"

Wait for user input, organize tasks by priority level.

### Pillar Balance Check

> "This week's focus:
> - [Pillar 1]: [Count] tasks, [X] meetings
> - [Pillar 2]: [Count] tasks, [Y] meetings
> - [Pillar 3]: [Count] tasks, [Z] meetings
> 
> Does this feel balanced? Any pillar getting neglected?"

Note any imbalances.

---

## Step 3.5: PKM Improvement Check (Optional)

Check if there are high-priority improvement ideas worth tackling this week.

### Check Dex Backlog

Read `System/Dex_Backlog.md` if it exists:
- Extract ideas with score >= 85 (High Priority)
- Count total high-priority ideas

### Present Opportunities

**If 1-2 high-priority ideas exist:**

> "💡 **PKM Improvement Opportunity**
> 
> You have [count] high-priority idea(s) that could improve your workflow:
> 
> 1. [[idea-XXX]] [Title] (Score: [score])
>    - [Why now: brief reasoning]
>    - Effort: [Quick win / 1-2 hours / Half day]
> 
> Want to tackle one this week? Or run `/dex-backlog` to see full rankings."

Wait for user response:
- If yes → Note as part of week priorities
- If no → Continue with planning
- If "show me" → Run `/dex-backlog` and return to planning after

**If 3+ high-priority ideas:**

> "💡 **Dex System Note:** You have [count] high-priority improvement ideas waiting.
> 
> Consider running `/dex-backlog` to review and prioritize them.
> Or block time this week to tackle 1-2 quick wins."

**If no high-priority ideas or Dex_Backlog.md doesn't exist:**
- Skip this section silently

---

## Step 4: Generate Week Priorities

Archive old `02-Week_Priorities/Week_Priorities.md` to `07-Archives/Plans/YYYY-Wxx.md` (with last week's week number).

Create updated `02-Week_Priorities/Week_Priorities.md`:

```markdown
# Week Priorities

**Week of:** [Monday YYYY-MM-DD]

---

## 🎯 Quarterly Context *(if quarterly planning enabled)*

**Q1 2026 Goals:**
1. [Goal 1] — [Pillar] — Progress: [X%] [🟢/🟡/🔴]
2. [Goal 2] — [Pillar] — Progress: [Y%] [🟢/🟡/🔴]
3. [Goal 3] — [Pillar] — Progress: [Z%] [🟢/🟡/🔴]

**This week advances:** Goals #[X], #[Y]

---

## 🎯 Top 3 This Week

The most important outcomes for this week. Everything else is secondary.

1. [Priority 1] — **[Pillar]**
   - Success criteria: [What done looks like]
   - Quarterly goal: [Q1 Goal #X] *(if applicable)*
   
2. [Priority 2] — **[Pillar]**
   - Success criteria: [What done looks like]
   - Quarterly goal: [Q1 Goal #X] *(if applicable)*
   
3. [Priority 3] — **[Pillar]**
   - Success criteria: [What done looks like]
   - Quarterly goal: [Q1 Goal #X] *(if applicable)*

---

## 📋 Tasks

### Must Complete (P0)
- [ ] [Task] — Supports: [Which Top 3 priority]

### Should Complete (P1)
- [ ] [Task] — Supports: [Which Top 3 priority]

### If Time Permits (P2)
- [ ] [Task]

---

## 📅 Key Meetings

| Day | Time | Meeting | Prep Needed |
|-----|------|---------|-------------|
| Mon | [Time] | [Meeting] | [Prep status or link] |
| Tue | [Time] | [Meeting] | [Prep status or link] |
| Wed | [Time] | [Meeting] | [Prep status or link] |
| Thu | [Time] | [Meeting] | [Prep status or link] |
| Fri | [Time] | [Meeting] | [Prep status or link] |

---

## 📊 Pillar Check

How does this week's work align to your strategic pillars?

| Pillar | Tasks/Focus | Balance |
|--------|-------------|---------|
| [Pillar 1] | [Brief description] | [🟩 Good / 🟨 Light / 🟥 Neglected] |
| [Pillar 2] | [Brief description] | [🟩 Good / 🟨 Light / 🟥 Neglected] |
| [Pillar 3] | [Brief description] | [🟩 Good / 🟨 Light / 🟥 Neglected] |

---

## 🔄 Carried Over

Tasks from last week that still need attention:

- [ ] [Task from last week] — [Why it carried over]

---

## 📝 Notes

[Any additional context about the week]

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

## Step 5: Track Usage (Silent)

After generating the week priorities file, silently update usage tracking:

1. Read `System/usage_log.md`
2. Update: `- [ ] Weekly planning (/week-plan)` → `- [x] Weekly planning (/week-plan)`
3. No announcement to user

---

## Step 6: Summary

After generating the file, provide a summary:

> "Week planned and saved to `02-Week_Priorities/Week_Priorities.md`
> 
> **Your Top 3 this week:**
> 1. [Priority 1]
> 2. [Priority 2]
> 3. [Priority 3]
> 
> **Pillar balance:** [Note any imbalances]
> 
> **Key meetings:** [Count] this week, [X] need prep
> 
> Ready to run `/daily-plan` for Monday?"

If it's Monday and user says yes, flow directly into `/daily-plan`.

---

## Graceful Degradation

### With Calendar + Tasks
- Full meeting context
- Task prioritization aligned to calendar
- Prep needs identified

### With Tasks Only
- Priority-based planning
- No meeting context (prompt user to add manually)

### Minimal Setup
- Manual input mode
- Guide user through questions
- Create priorities file from their answers

---

## Integration with Other Commands

**Called from `/week-review`:**
- Receives "Next Week Focus" suggestions from review
- Pre-fills some context

**Called from `/daily-plan` on Monday:**
- If week not planned, offers to run this first
- Then flows back to daily planning

**Manual invocation:**
- User runs directly when they want to plan

---

## MCP Dependencies

| Integration | MCP Server | Tools Used |
|-------------|------------|------------|
| Calendar | dex-calendar-mcp | `calendar_get_events_with_attendees` |
| Work | dex-work-mcp | `list_tasks`, `list_week_priorities` |
| Granola | dex-granola-mcp | (Optional) `get_upcoming_meetings` |
