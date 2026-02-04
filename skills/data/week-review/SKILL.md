---
name: week-review
description: Review week's progress with concrete accomplishments (not fake percentages), pattern detection, and goal tracking.
---

## Purpose

Create a synthesis of the week reviewing activity, progress, and what was accomplished. **Uses concrete metrics, not vague percentages.**

---

## Data Sources

### 1. Task Progress
- `03-Tasks/Tasks.md` — Task completion status
- `02-Week_Priorities/Week_Priorities.md` — Weekly priorities

### 2. Project Activity
- `04-Projects/**/*.md` — Modified this week

### 3. Meetings & People
- `00-Inbox/Meetings/*.md` — Meeting notes from this week
- `People/**/*.md` — Person pages updated

### 4. Learnings
- `06-Resources/Learnings/**/*.md` — Explicit learnings
- `System/Session_Learnings/*.md` — Auto-captured session learnings

### 5. Daily Reviews
- `07-Archives/Reviews/Daily_Review_YYYY-MM-DD.md` — This week's reviews

### 6. Journals (If Enabled)
- `00-Inbox/Journals/YYYY/MM-Month/` — Morning/evening journals

---

## Analysis Process

### 1. Weekly Priority Completion (Concrete, Not Percentages)

**Don't say:** "Goal X went from 40% to 55%"
**Do say:** "You completed 2 of 3 weekly priorities"

```
Use: get_week_progress()
```

For each weekly priority:
- **Complete:** ✅ What was the deliverable? When did you finish?
- **In Progress:** 🔄 What specifically got done? What's left?
- **Not Started:** ❌ Why? Should it carry forward?

**Surface concrete accomplishments:**

> "**This week's priorities:**
> 
> 1. ✅ **Ship pricing page** — Complete (pushed to prod Wednesday)
>    - Deliverable: New pricing page live at /pricing
>    - Tasks completed: 5 of 5
> 
> 2. 🔄 **Write Q1 strategy doc** — 60% complete
>    - Done: Outline, competitive analysis, recommendations
>    - Remaining: Executive summary, financial projections
>    - 2 tasks left
> 
> 3. ❌ **Customer interviews** — Not started
>    - Reason: Calendar was too stacked
>    - Recommendation: Carry to next week with protected time"

### 2. Task Completion Stats (Concrete Numbers)

Scan `03-Tasks/Tasks.md` for completion timestamps from this week:
- Count tasks completed (look for `✅ YYYY-MM-DD` in date range)
- Count tasks added mid-week
- Count tasks carried over

**Surface:**

> "**Tasks this week:**
> - Completed: 14 tasks
> - Added mid-week: 6 tasks (scope creep?)
> - Carried over: 3 tasks
> 
> **Completion rate:** 82% (14 of 17 planned)"

### 3. Quarterly Goals Progress (Concrete Milestones)

**Don't use fake percentages.** Use milestone counts and specific accomplishments.

```
Use: get_quarterly_goals()
Use: get_goal_status(goal_id) for each goal
```

For each goal:
- Milestones completed this week
- Total milestones done vs. total
- Weeks since last milestone
- Specific accomplishments that moved the goal

> "**Quarterly Goals Progress:**
> 
> | Goal | Milestones | This Week | Status |
> |------|------------|-----------|--------|
> | Launch v2.0 | 3 of 5 | +1 (Pricing page shipped) | On track |
> | Improve NPS | 1 of 4 | No change | ⚠️ Stalled (3 weeks) |
> | Team Capacity | 2 of 3 | No change | On track |
> 
> **Goal 1** advanced because you completed Priority 1.
> **Goal 2** needs attention — no linked work completed this week."

### 4. Daily Completion Rate Trend (NEW)

If daily reviews exist, calculate completion trends:

> "**Daily plan completion this week:**
> 
> | Day | Planned | Done | Rate |
> |-----|---------|------|------|
> | Mon | 3 | 2 | 67% |
> | Tue | 3 | 3 | 100% |
> | Wed | 3 | 2 | 67% |
> | Thu | 3 | 1 | 33% |
> | Fri | 3 | 2 | 67% |
> 
> **Week average:** 67%
> **Pattern:** Thursday was rough (too many meetings?)"

### 5. Meeting Analysis

Review meeting notes from the week:
- Meetings held
- Key decisions
- Action items created
- Follow-ups that might have slipped

### 6. Learning Compilation & Pattern Detection

Review `System/Session_Learnings/` files from this week:

**Pattern Detection:**
- **Recurring issues:** Same mistake 2+ times? Suggest adding to Mistake_Patterns.md
- **Consistent preferences:** User repeatedly mentioned a workflow preference?

> "This week's session learnings revealed:
> 
> **Recurring Issues:**
> - Calendar overload (mentioned 3 times) — Consider blocking focus time
> 
> **Workflow Preferences:**
> - Prefer morning for deep work (mentioned 2 times)
> 
> Should I add these to your pattern files?"

---

## Output Format

Create `00-Inbox/Weekly_Synthesis_YYYY-MM-DD.md`:

```markdown
# Weekly Synthesis — Week of [Date]

## TL;DR

- **Weekly priorities:** [X] of 3 complete
- **Tasks:** [X] completed / [Y] planned — [Z]% completion
- **Meetings:** [N] total
- **Key wins:** [1-2 bullets]
- **Carried over:** [1-2 items]

---

## 🎯 Weekly Priorities

### 1. [Priority 1] — ✅ Complete

**Deliverable:** [What was shipped/finished]
**Completed:** [Day]
**Tasks:** 5 of 5

### 2. [Priority 2] — 🔄 In Progress (60%)

**Done this week:**
- [Specific accomplishment]
- [Specific accomplishment]

**Remaining:**
- [Specific task]
- [Specific task]

### 3. [Priority 3] — ❌ Not Started

**Why:** [Reason]
**Recommendation:** [Carry forward / Deprioritize / Defer]

---

## 📊 Task Completion

| Metric | Count |
|--------|-------|
| Tasks completed | 14 |
| Tasks added mid-week | 6 |
| Tasks carried over | 3 |
| **Completion rate** | **82%** |

**Observation:** [Any patterns — e.g., lots of scope creep]

---

## 🎯 Quarterly Goals

| Goal | Milestones | This Week | Status |
|------|------------|-----------|--------|
| [Goal 1] | X of Y | +Z | [Status] |
| [Goal 2] | X of Y | — | [Status] |
| [Goal 3] | X of Y | +Z | [Status] |

**Goals advancing:** [Which ones moved]
**Goals stalled:** [Which ones need attention]

---

## 📊 Daily Completion Trend

| Day | Planned | Done | Rate |
|-----|---------|------|------|
| Mon | 3 | 2 | 67% |
| Tue | 3 | 3 | 100% |
| Wed | 3 | 2 | 67% |
| Thu | 3 | 1 | 33% |
| Fri | 3 | 2 | 67% |

**Week average:** [X]%
**Observation:** [Pattern noticed]

---

## 📅 Meetings & People

### Meetings Held

| Date | Topic | Key Outcome |
|------|-------|-------------|
| [Day] | [Topic] | [Decision/insight] |

### New Contacts
- [Name] at [Company] — [context]

### Action Items from Meetings
- [ ] [Action] — for [who] — due [when]

---

## 💡 Learnings

### Session Learnings (Auto-Captured)
- [Learning 1]
- [Learning 2]

### Patterns Identified
- **Recurring issue:** [Issue] (appeared X times)
- **Preference noted:** [Preference]

### Actionable Improvements
- [ ] [Specific improvement to make]

---

## 📊 Pillar Balance

| Pillar | Tasks Done | Focus |
|--------|------------|-------|
| [Pillar 1] | X tasks | Heavy |
| [Pillar 2] | X tasks | Light |
| [Pillar 3] | X tasks | None |

**Observation:** [Balance assessment]

---

## ➡️ Next Week

### Suggested Priorities

Based on this week's progress:

1. **[Priority]** — [Why: carries over / goal needs attention / commitment]
2. **[Priority]** — [Why]
3. **[Priority]** — [Why]

### Blocked Items Needing Resolution

| Item | Blocked Since | What Would Unblock It |
|------|---------------|-----------------------|
| [Item] | [Date] | [Action needed] |

---

## 🏆 Career Evidence (If Career System Enabled)

**Significant accomplishments worth capturing:**

- [Accomplishment] — demonstrates [skill]
- [Accomplishment] — shows [impact]

> "Want to save any of these as career evidence?"

---

*Generated: [timestamp]*
*Weekly completion: X of 3 priorities*
*Task completion: X%*
```

---

## Follow-up Actions

After synthesis:
1. Update Tasks.md with new priorities
2. Archive completed items
3. Update project pages with status changes
4. Offer to run `/week-plan` for next week

---

## MCP Dependencies

| Integration | MCP Server | Tools Used |
|-------------|------------|------------|
| Work | dex-work-mcp | `list_tasks`, `get_week_progress`, `get_quarterly_goals`, `get_goal_status` |
| Calendar | dex-calendar-mcp | `calendar_get_events_with_attendees` |
