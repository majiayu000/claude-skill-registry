---
name: quarter-review
description: Review quarter completion and capture learnings
---

## Purpose

Review and synthesize the quarter that just ended. Evaluates goal completion, captures learnings, and suggests focus for next quarter.

## Usage

- `/quarter-review` — Review current/recently ended quarter
- `/quarter-review Q4 2025` — Review specific past quarter

---

## Step 0: Check if Quarterly Planning is Enabled

Read `System/user-profile.yaml`:

1. Check `quarterly_planning.enabled` value
2. **If `false`:**
   - Display: "Quarterly planning is disabled. Enable it first with `/quarter-plan`"
   - End command
3. **If `true`:** Continue to Step 1

---

## Step 1: Determine Target Quarter

**If no parameter:**
- Calculate current quarter based on `q1_start_month`
- Assume reviewing current or just-ended quarter

**If parameter provided (e.g., "Q4 2025"):**
- Parse quarter and year
- Review that specific quarter

Calculate:
- `target_quarter`: "Q1 2026"
- `quarter_start`: "2026-01-01"
- `quarter_end`: "2026-03-31"

---

## Step 2: Context Gathering

### Quarter Goals File

Check for `01-Quarter_Goals/Quarter_Goals.md`:

**If exists and matches target quarter:**
- Extract goals that were set
- Note progress percentages (if updated)
- List milestones and completion status

**If missing or wrong quarter:**
- Check `07-Archives/Reviews/[quarter]-goals.md` (archived version)
- If still missing: "No goals found for this quarter"

### Task Completion

Scan `03-Tasks/Tasks.md` for tasks completed during quarter:
- Count completed tasks in date range
- Major completions
- Tasks that were blocked

### Project Activity

Scan `04-Projects/` for activity during quarter:
- Modified files in date range
- Projects launched
- Projects completed
- Projects stalled

### Meetings & People

Scan `00-Inbox/Meetings/` for quarter date range:
- Total meetings held
- Key discussions and decisions
- New relationships formed

### Weekly Syntheses

Look for `00-Inbox/Weekly_Synthesis_*.md` files in quarter:
- Extract recurring themes
- Compile learnings
- Note energy patterns

---

## Step 3: Goal Assessment

For each goal from `01-Quarter_Goals/Quarter_Goals.md`:

**Evaluate:**
- ✅ **Completed:** Fully achieved
- 🔄 **Partial:** Made significant progress but not done
- ❌ **Not Started:** Didn't get to it
- 🚫 **Deprioritized:** Intentionally stopped

For each, capture:
- What was accomplished
- What blocked progress (if incomplete)
- Key learnings

---

## Step 4: Interactive Review

**Goal-by-goal walkthrough:**

> "Goal 1: [Goal title]
> 
> Progress indicator showed: [X%]
> Milestones: [Y of Z completed]
> 
> How would you assess this goal?
> - ✅ Completed
> - 🔄 Partial (what % done?)
> - ❌ Didn't get to it
> - 🚫 Deprioritized"

Wait for user response, then:

> "What happened with this goal? (Key wins, blockers, learnings)"

Capture narrative for each goal.

**Overall quarter reflection:**

> "Stepping back, how did this quarter go?
> 
> - What were your biggest wins?
> - What drained energy or didn't work?
> - What would you do differently?
> - What surprised you?"

---

## Step 5: Pillar Balance Review

Read `System/pillars.yaml` and assess:

> "Pillar balance this quarter:
> - [Pillar 1]: [Goals + activity level]
> - [Pillar 2]: [Goals + activity level]
> - [Pillar 3]: [Goals + activity level]
> 
> Any pillar that needs more attention next quarter?"

---

## Step 5.5: System Health & Backlog Review

Review the Dex system itself and improvement backlog.

### Check Dex Backlog

Read `System/Dex_Backlog.md` if it exists:

**Extract:**
- Total ideas in backlog
- High-priority ideas (score >= 85)
- Ideas captured during this quarter
- Ideas marked as implemented

**Present to user:**

> "**Dex System Improvement Backlog:**
> 
> - Total ideas captured: [count]
> - High-priority (ready to implement): [count]
> - Implemented this quarter: [count]
> 
> Looking at your Dex backlog:
> - Any 1-2 high-impact improvements to prioritize next quarter?
> - Any stale ideas (>6 months old) to archive?"

Wait for user input on:
- Which 1-2 ideas to tackle next quarter
- Any ideas to archive or refine

### Suggest Backlog Review

**If 3+ high-priority ideas exist:**

> "💡 Consider running `/dex-backlog` soon to re-rank ideas based on updated system state."

**If no Dex_Backlog.md exists:**
- Skip this section silently
- In review document, note: "Dex backlog system not yet in use"

---

## Step 6: Generate Quarterly Review

Create `07-Archives/Reviews/[Quarter].md`:

```markdown
---
quarter: Q1 2026
start_date: 2026-01-01
end_date: 2026-03-31
reviewed_on: [date]
---

# Q1 2026 Quarterly Review

**Jan 1 - Mar 31, 2026**

---

## TL;DR

- **Goals:** [X of Y completed]
- **Key win:** [Biggest accomplishment]
- **Key learning:** [Most important insight]
- **Pillar balance:** [Assessment]

---

## Goal Completion

### Goal 1: [Goal Title] — **[Pillar]**

**Status:** ✅ Completed / 🔄 Partial (X%) / ❌ Not Started / 🚫 Deprioritized

**Original success criteria:**
[What was defined in 01-Quarter_Goals/Quarter_Goals.md]

**What happened:**
[Narrative from user + gathered context]

**Key wins:**
- [Specific accomplishment]

**Blockers/Challenges:**
- [What got in the way]

**Learnings:**
- [What was learned]

---

### Goal 2: [Goal Title] — **[Pillar]**

[Same structure]

---

### Goal 3: [Goal Title] — **[Pillar]**

[Same structure]

---

## Quarter Highlights

### Major Accomplishments
- [Project/initiative completed]
- [Milestone reached]
- [Key decision made]

### Projects Shipped
- [Project 1] — [Brief description]
- [Project 2] — [Brief description]

### New Relationships
- [Person] at [Company] — [Context]

### Key Meetings/Decisions
- [Date]: [Meeting/decision] — [Impact]

---

## What Didn't Work

### Incomplete Goals
- [Goal] — [Why it didn't happen]

### Stalled Projects
- [Project] — [What blocked it]

### Time Drains
- [Activity that consumed time without value]

---

## Learnings & Insights

### Process Learnings
- [What worked well]
- [What to change]

### Personal Insights
- [Self-awareness gained]

### System Improvements
- [Dex system improvements identified]

---

## System Health & Improvement Backlog

### Dex Backlog Activity
- **Ideas captured:** [Count during quarter]
- **Ideas implemented:** [Count marked as completed]
- **Current high-priority ideas:** [Count with score >= 85]

### Improvements Implemented This Quarter
- **[idea-XXX]** [Title] — [Brief description of what was built]
- **[idea-YYY]** [Title] — [Impact it had]

### Next Quarter Priorities
Based on backlog review, prioritize these improvements:
1. [Idea to tackle] — [Why now]
2. [Idea to tackle] — [Why now]

*Run `/dex-backlog` for full ranked list*

---

## Pillar Assessment

| Pillar | Goals | Activity | Assessment |
|--------|-------|----------|------------|
| [Pillar 1] | [X goals] | [High/Med/Low] | [Balanced / Over-indexed / Neglected] |
| [Pillar 2] | [Y goals] | [High/Med/Low] | [Assessment] |
| [Pillar 3] | [Z goals] | [High/Med/Low] | [Assessment] |

**Next quarter adjustment:**
[Which pillar needs more/less focus]

---

## Stats

- **Weeks in quarter:** 13
- **Meetings held:** [Count]
- **Tasks completed:** [Count]
- **Projects shipped:** [Count]
- **Weekly syntheses:** [Count completed]

---

## Next Quarter Suggestions

Based on this quarter's learnings:

### Carry Forward
- [ ] [Incomplete goal to continue]
- [ ] [Unfinished initiative]

### New Opportunities
- [Area to explore next quarter]
- [Project idea that emerged]

### Focus Areas
1. [Suggested priority 1]
2. [Suggested priority 2]
3. [Suggested priority 3]

### Process Changes
- [Adjustment to workflow]
- [System improvement to implement]

---

## Energy Assessment

<details>
<summary>Click to expand</summary>

### What Gave Energy
- [Activities/projects that were energizing]

### What Drained Energy
- [Activities that felt like a slog]

### Adjustment for Next Quarter
- [More of X, less of Y]

</details>

---

*Generated: [timestamp]*
*Command: /quarter-review*
```

---

## Step 7: Next Quarter Planning Prompt

After review is complete:

> "Quarter reviewed and saved to `07-Archives/Reviews/Q1-2026.md`
> 
> **Ready to plan next quarter (Q2 2026)?**
> 
> I have suggestions based on what you learned this quarter.
> 
> [Yes, let's plan Q2] [No, I'll do it later]"

**If yes:** Flow directly into `/quarter-plan next`

---

## Follow-up Actions

After review:
1. Archive old `01-Quarter_Goals/Quarter_Goals.md` if not already done
2. Update `System/user-profile.yaml` with completed quarter
3. Suggest running `/quarter-plan` for next quarter

---

## Integration Points

**Called at end of quarter:**
- Natural time: Last week of quarter
- Can run anytime after quarter ends

**Feeds into `/quarter-plan`:**
- Next quarter planning reads this review
- Suggestions inform new goals

**References:**
- `01-Quarter_Goals/Quarter_Goals.md` — Original plan
- Weekly syntheses — Week-by-week activity
- Task completions — Actual work done
- Meeting notes — Context gathered

---

## Graceful Degradation

### Missing Goals File
- Can still review based on tasks, projects, meetings
- Notes that no formal goals were set

### First Quarter
- No previous quarter to compare to
- Focus on establishing baseline

### Incomplete Data
- Works with whatever data is available
- Prompts user to fill in gaps
