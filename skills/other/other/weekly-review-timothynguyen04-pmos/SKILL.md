---
name: weekly-review
description: Review week's progress, meetings, learnings
---

## Quick Start

1. Run `/weekly-review` on Friday afternoon (best time) or Monday morning
2. I will scan your workspace: weekly plans, daily plans, PRDs, meeting notes, decisions, and launches from the past 7 days
3. I will generate a focused review comparing plan vs. actual, surfacing key wins, blockers, and learnings
4. Output goes to `outputs/weekly-reviews/YYYY-WXX-weekly-review.md`
5. After the review, I will suggest running `/weekly-plan` to plan next week

**Default output is focused (~150 lines max).** Say "full review" if you want the expanded version with stakeholder pulse, task-level execution metrics, and pattern analysis.

## Purpose

End-of-week synthesis reviewing what you accomplished, what you learned, and what needs attention. Feeds into next week's planning and builds institutional memory.

## Usage

- `/weekly-review` - Review current/past week
- `/weekly-review last-week` - Review previous week (if you forgot)

---

## Context Routing

**Check these files first:**
1. `outputs/weekly-plans/` - This week's plan (what you intended)
2. `outputs/daily-plans/` - Daily plans from this week (what actually happened)
3. `outputs/prds/` - PRDs modified this week
4. `outputs/meeting-notes/` - Meeting notes from past 7 days
5. `context-library/launches/` - Launches that happened this week
6. `context-library/decisions/` - Decisions made this week
7. `outputs/research-synthesis/` - Research conducted
8. `context-library/strategy/` - Quarter goals (to track progress)

**MCP Queries (if available):**
- **Linear/Jira MCP** - Tasks completed this week
- **Analytics MCP** - Metrics for features launched recently
- **GitHub MCP** - Code activity (if relevant to your role)
- **Slack MCP** - Key conversations and decisions

**Fallback:** File-based analysis of PM OS workspace + manual input for completions.

---

## Workflow

### Step 1: Determine Review Period

1. **Calculate week to review:**
   - Default: Current week (if Friday or later)
   - If Monday-Thursday: Ask "Review last week or current week?"
   - If user specified: Use that week

2. **Check if review already exists:**
   - Look for `outputs/weekly-reviews/YYYY-WXX-weekly-review.md`
   - If exists: Ask "Update existing review or create new version?"

---

### Step 2: Data Collection

**A. Weekly Plan (What Was Intended):**

Read `outputs/weekly-plans/YYYY-WXX-weekly-plan.md`:

Extract:
- Top 3 priorities for the week
- Key tasks under each priority
- Success criteria
- Expected meeting load

If no weekly plan exists:
- Note: "Week wasn't planned. Reviewing what happened only."
- Suggest: "Next week, run `/weekly-plan` on Monday for better focus."

---

**B. PRD Progress:**

Scan `outputs/prds/` and `context-library/prds/`:

Method 1 - File modification dates:
```bash
# Files modified in the past 7 days
find outputs/prds/ context-library/prds/ -name "*.md" -mtime -7
```

For each PRD touched this week:
- Read frontmatter or first section for current stage
- Compare to last week's stage (if weekly review from last week exists)
- Determine: Advanced, Stalled, or New

Method 2 - If Git available:
```bash
# PRDs with commits this week
git log --since="7 days ago" --name-only --pretty=format: | grep -E "prds/.*\.md$" | sort -u
```

**Categorize:**
- **Advanced:** Moved to next stage (Team Kickoff → Planning Review)
- **Active:** Work happened but didn't advance stage
- **Stalled:** No activity this week
- **New:** Started this week

---

**C. Feature Launches:**

Check `context-library/launches/`:
- Launches completed this week
- Launch checklists finished
- Post-launch monitoring started

For each launch:
If Analytics MCP available:
```
Query metrics since launch date
Compare to success criteria from PRD
```

Categorize:
- ✅ On track (meeting targets)
- ⚠️ Needs attention (below targets)
- ❌ Underperforming (significantly below)
- 🚀 Exceeding (beating targets)

---

**D. Meetings & Decisions:**

Scan `outputs/meeting-notes/` from past 7 days:

For each meeting:
- Extract date, attendees, topic
- Look for: Decisions made, action items created, blockers identified

Check `context-library/decisions/`:
- Decision docs created this week
- Link to related meetings

**Build stakeholder pulse:**
- Who did you meet with most? (frequency)
- Who did you miss syncing with? (gaps)
- What topics dominated discussions? (themes)

---

**E. Tasks Completed:**

If Linear/Jira MCP available:
```
Query: Tasks completed in past 7 days
Group by: Priority, PRD/Initiative
Calculate: Planned vs actual completion rate
```

If MCP not available:
- Scan daily plans for checked-off tasks
- Scan meeting notes for completed action items

**Categorize by initiative:**
```
Initiative: [PRD Name]
- ✅ Task 1 (from Priority 1)
- ✅ Task 2 (from Priority 1)
- [ ] Task 3 (carried over - why?)
```

**Calculate metrics:**
- Tasks completed vs planned
- % completion rate
- Carry-over rate

---

**F. User Research & Insights:**

Check `context-library/research/`:
- New interview notes this week
- Competitive analysis updates

Check `outputs/research-synthesis/`:
- Synthesis reports created
- Themes identified

Extract:
- Key findings
- Recurring themes (mentioned in multiple sources)
- Recommendations for roadmap

---

**G. Learnings & Patterns:**

This is where weekly review gets powerful - surfacing patterns.

**From daily plans:**
- What consistently took longer than expected?
- What got deprioritized every day? (maybe not important)
- What meeting prep was valuable vs not?

**From outcomes:**
- What decisions went well? (process to repeat)
- What decisions went poorly? (what to change)
- What blockers kept recurring? (systemic issue)

**From stakeholder interactions:**
- What communication worked well?
- What caused confusion or misalignment?
- Who needs more/less frequent updates?

---

### Step 3: Analysis & Synthesis

**PRD Pipeline Analysis:**

For each PRD:
- Last week's stage → This week's stage
- Movement: ✅ Advanced / → Active / ⚠️ Stalled

**Why analysis:**
- Advanced: What unblocked it? (repeat this)
- Stalled: What's blocking? (action needed)

---

**Strategic Alignment:**

Read `context-library/strategy/` for quarter goals.

For each goal:
- Which priorities/tasks contributed to it this week?
- Progress estimate: X% → Y% (did we move the needle?)
- Velocity: Are we on track for quarter target?

**Pillar balance:**
If strategy has defined pillars:
- Pillar 1: X% of time this week
- Pillar 2: Y% of time
- Pillar 3: Z% of time

Compare to target allocation: Are we balanced?

---

**Pattern Detection:**

Look for:
- **Recurring blockers:** Same dependency/person blocked multiple things
- **Underestimated tasks:** Consistently took 2x longer than planned
- **Overcommitted weeks:** Planned 30 hours with 25 hours of meetings
- **Meeting value:** Which meetings led to outcomes vs were FYI only?
- **Best working times:** When did deep work happen? (protect these blocks)

---

### Step 4: Generate Weekly Review

Create file: `outputs/weekly-reviews/YYYY-WXX-weekly-review.md`

**Output Length Guidance:**

**Default (focused review, ~150 lines max).** Include only:
1. TL;DR (5-6 bullet summary)
2. Priority Completion (plan vs actual for top 3 priorities)
3. Key Decisions Made (list with one-line rationale each)
4. Metrics Movement (table of metrics that changed)
5. Top 3 Learnings (what worked, what did not, what to change)
6. Next Week Preview (draft priorities + items to unblock)

**Full review (when user asks for it).** Expand to also include:
- Stakeholder pulse (engagement gaps, new relationships)
- Task-level execution metrics (completion rate, carry-over rate, scope creep indicator)
- PRD pipeline table with stage movement
- Meeting value assessment (high/medium/low for each meeting)
- Pattern analysis (recurring blockers, underestimated task types, best working times)
- User research and competitive intelligence updates

**Template:**

```markdown
---
week: YYYY-WXX
week_start: YYYY-MM-DD
week_end: YYYY-MM-DD
quarter: Q[X] YYYY
---

# Weekly Review - Week of [Month] [DD], [YYYY]

## TL;DR

- **PRDs:** [X active], [Y advanced], [Z stalled]
- **Launches:** [N features shipped]
- **Meetings:** [M total], [P key decisions]
- **Completion rate:** [X%] of planned tasks done
- **Key win:** [Biggest accomplishment]
- **Key challenge:** [Biggest blocker/lesson]

---

## Strategic Progress

**Quarter Goal:** [Primary goal for Q]
**Progress This Week:** [What moved forward]

| Goal | Start of Week | End of Week | This Week | Status |
|------|---------------|-------------|-----------|--------|
| [Goal 1] | X% | Y% | +Z% | ✅ On track |
| [Goal 2] | A% | B% | +C% | ⚠️ Behind |

**Velocity check:**
- [X] weeks left in quarter
- [Y%] progress needed per week to hit goal
- [Z%] actual progress this week
- **Assessment:** [On track / Need to accelerate / Ahead]

---

## Top 3 Priorities Review

[Compare planned vs actual]

### Priority 1: [Title]

**Planned:** [What we intended to achieve]
**Actual:** [What we achieved]

**Tasks:**
- ✅ [Task 1] - Done
- ✅ [Task 2] - Done
- [ ] [Task 3] - Carried over because [reason]

**Status:** ✅ Complete / 🟡 Partial / ❌ Not started

**Key outcome:**
- [What this unlocked or enabled]

**Learning:**
- [What went well or what to change]

---

### Priority 2: [Title]

[Same structure]

---

### Priority 3: [Title]

[Same structure]

---

## PRD Pipeline

| PRD | Stage (Start of Week) | Stage (End of Week) | Movement | Next Action |
|-----|----------------------|---------------------|----------|-------------|
| [Name] | Team Kickoff | Planning Review | ✅ Advanced | Get eng estimates |
| [Name] | Solution Review | Solution Review | ⚠️ Stalled | Need legal review |
| [Name] | - | Team Kickoff | 🆕 New | Scope and plan |

**Analysis:**
- **Advanced:** [PRD X] moved forward because [stakeholder signed off / design done / etc.]
- **Stalled:** [PRD Y] blocked on [dependency / decision / resource]
- **Recommendation:** [What to prioritize next week to unblock]

---

## Launches & Impact

### Shipped This Week

[If anything launched]

**[Feature Name]** (Launched [Day])

**Success Criteria (from PRD):**
- [Metric 1]: Target [X], Actual [Y] ([+/-Z%])
- [Metric 2]: Target [A], Actual [B] ([+/-C%])

**Early assessment:** ✅ On track / ⚠️ Needs attention / ❌ Below target / 🚀 Exceeding

**Insights:**
- [User feedback received]
- [Unexpected behavior observed]
- [Next iteration needed]

---

### Post-Launch Monitoring

[Features launched in past 4 weeks still being monitored]

| Feature | Launch Date | Key Metric | Target | Actual | Trend | Status |
|---------|-------------|------------|--------|--------|-------|--------|
| [Name] | [Date] | [Metric] | [X] | [Y] | [↗↘→] | [✅⚠️❌] |

---

## Key Decisions Made

1. **[Decision]** ([Date] - [Meeting])
   - **Context:** [Why this came up]
   - **Decision:** [What was decided]
   - **Rationale:** [Why we chose this]
   - **Owner:** [Who's executing]
   - **Impact:** [What this affects]
   - **Doc:** [Link if exists]

2. **[Decision 2]**
   [Same structure]

---

## Meetings & Stakeholder Pulse

### Meetings This Week: [Total]

| Day | Meeting | Attendees | Outcome | Value |
|-----|---------|-----------|---------|-------|
| Mon | [Topic] | [Names] | [Decision/Alignment] | 🟢 High |
| Tue | [Topic] | [Names] | [Info sharing] | 🟡 Medium |
| Wed | [Topic] | [Names] | [Cancelled] | ⚫ None |

**Meeting load:** [X] hours / 40 = [Y%]
**Deep work time:** [Z] hours (vs [A] hours planned)

**Value assessment:**
- 🟢 High value: Led to decision or unblocked work
- 🟡 Medium value: Useful context but no immediate action
- 🔴 Low value: Could have been async or skipped

**Recommendation:** [Which meetings to keep/change/cancel]

---

### Stakeholder Pulse

**High engagement this week:**
- **[Name]** - [Why: Multiple syncs, key decision, strong collaboration]
  - Impact: [What this enabled]
  - Continue: [Keep this cadence / Increase collaboration]

**Needs attention:**
- **[Name]** - [Why: Haven't synced in 2+ weeks, blocking issue, misalignment suspected]
  - Impact: [What's at risk]
  - Action: [Specific next step - schedule 1:1, send update, etc.]

**New relationships:**
- **[Name]** - [Met for first time, context]
  - Follow-up: [Add to stakeholder profiles, schedule regular sync]

---

## User Research & Insights

[Only include if research happened]

**New Research This Week:**
- **[Interview/Study]** - [Date]
  - Key finding: [Insight]
  - Validates: [Which hypothesis or PRD]
  - Challenges: [What assumption or approach]

**Recurring Themes:**
- **[Theme 1]** - Mentioned in [X] sources
  - Evidence: [Quote or data point]
  - Implication: [What this means for roadmap]

- **[Theme 2]** - Validates hypothesis from [PRD]
  - Evidence: [Quote or data point]
  - Recommendation: [Accelerate this PRD / Pivot approach]

**Competitive Intelligence:**
[If competitive analysis updated]
- [Competitor] launched [Feature]
- Implication: [How this affects our strategy]

---

## Tasks & Execution

**Completion Metrics:**
- **Completed:** [X] tasks
- **Carried over:** [Y] tasks ([Z%] carry-over rate)
- **Added mid-week:** [A] tasks (scope creep indicator)

**By initiative:**

### [Initiative/PRD Name]

- ✅ [Task completed]
- ✅ [Task completed]
- [ ] [Task carried over] - **Why:** [Blocked by X / Deprioritized for Y / Under-estimated]

### [Initiative 2]

[Same structure]

**Patterns:**
- Tasks that took longer than expected: [Type/category]
- Blockers that repeated: [Dependency on X person/team]
- Tasks that got bumped repeatedly: [Maybe not actually important?]

---

## Learnings & Patterns

**What Worked Well:**
- **[Approach/Decision]** - [Why it was effective]
  - Example: [Specific instance]
  - Repeat: [How to apply this pattern again]

**What Didn't Work:**
- **[Mistake/Inefficiency]** - [What happened]
  - Impact: [Consequence]
  - Root cause: [Why this happened]
  - Fix: [Specific change for next time]

**Process Improvements:**
- [ ] [Specific improvement to implement]
  - Why: [Problem it solves]
  - How: [Concrete action]
  - Owner: You
  - By when: [Next week / Next sprint]

**Personal Development:**
[If applicable]
- Skill practiced: [What you worked on]
- Feedback received: [From whom, about what]
- Growth area identified: [What to develop]

---

## Next Week Preview

### Top 3 Priorities (Draft)

[Based on this week's outcomes, suggest next week's priorities]

1. **[Priority 1]** - [Why: Carries over from this week / New urgent item / Strategic next step]
2. **[Priority 2]** - [Why]
3. **[Priority 3]** - [Why]

> Note: Run `/weekly-plan` to formalize these and add detail

---

### Key Meetings Next Week

[From calendar if available]
- **[Day]:** [Meeting] - [Goal/Outcome needed]
- **[Day]:** [Meeting] - [Prep needed]

---

### Items to Unblock

| Item | Blocked Since | Blocked By | Action Needed |
|------|---------------|------------|---------------|
| [PRD/Task] | [Date/Week] | [Person/Dependency/Decision] | [Specific ask] |

**Priority unblocks:**
1. [Most critical blocker to address Monday]
2. [Second priority]

---

## Metrics to Monitor Next Week

[Features to keep watching]

- **[Feature 1]** - [Why: Early launch / Trending down / Critical metric]
  - Watch: [Specific metric]
  - Check: [Daily / Every other day]
  - Flag if: [Threshold or condition]

---

*Generated: [Timestamp]*
*Data sources: [Weekly plan, Daily plans, PRDs, Meeting notes, Linear/Jira, Analytics]*
*Next: Run `/weekly-plan` to plan next week*
```

---

### Step 5: Follow-Up Prompts

After generating review, prompt user with contextual suggestions:

**Always offer:**
> "Week synthesized and saved! Next steps:
>
> 1. **Plan next week?** Run `/weekly-plan` (5-10 min) - I've drafted initial priorities above
> 2. **Share with team?** I can format this as a stakeholder update
>
> What would help?"

**If significant wins:**
> "🎉 Nice work on [Achievement]! Worth documenting this:
>
> - Add to portfolio/resume
> - Share in team update
> - Capture as case study for future reference
>
> Want me to help with any of these?"

**If patterns emerged:**
> "📊 I noticed some patterns:
>
> - [Recurring blocker X] appeared [Y] times
> - [Task type Z] consistently took 2x longer than estimated
>
> Want to dig into these and create process improvements?"

**If learnings captured:**
> "💡 This week's learnings worth remembering:
>
> - [Learning 1]
> - [Learning 2]
>
> I'll surface these in future planning. Want me to add to `context-library/personal-context/lessons-learned.md`?"

**If metrics concerning:**
> "⚠️ [Feature] metrics need attention:
>
> - [Metric] is [X%] below target
> - Trending [down/flat] since launch
>
> Run `/feature-results` for deeper analysis? Or schedule stakeholder review?"

---

## Integration with Other Skills

**Before `/weekly-review`:**
- `/daily-plan` - Ran throughout the week (provides daily context)
- `/meeting-notes` - Captured meeting outcomes
- `/prd-draft` - Created/updated PRDs this week

**After `/weekly-review`:**
- `/weekly-plan` - Plan next week based on this review
- `/decision-doc` - Document key decisions made
- `/status-update` - Share with stakeholders
- `/feature-results` - Deep dive on launched features

**Parallel use:**
- `/impact-sizing` - Validate completed work had expected impact
- `/competitor-analysis` - If competitive intel emerged this week

---

## Tips for Best Results

**When to run:**
- **Best time:** Friday afternoon (4-5pm)
  - Week is fresh in memory
  - Can plan next week immediately after
  - Creates clean mental closure for weekend
- **Alternative:** Monday morning (reflect before planning)
- **Avoid:** Mid-week (incomplete picture)

**What makes a good review:**
- ✅ Honest about what didn't go well (not just wins)
- ✅ Specific about patterns (not vague "work harder")
- ✅ Actionable improvements (concrete next steps)
- ✅ Connects to strategy (not just task completion)
- ❌ Just a task list (misses the "why" and learnings)
- ❌ All problems, no wins (demotivating)

**How to build the habit:**
- Week 1-2: I'll prompt you Friday afternoon
- Week 3-4: You'll start expecting it (ritual forming)
- Week 5+: Feels incomplete without it

**Use the output:**
- Reference in 1:1s with manager (shows progress)
- Share with stakeholders (transparency)
- Compare month-over-month (velocity trends)
- Review quarterly (pattern detection across multiple weeks)

---

## Related Skills

**Before this:**
- `/daily-plan` - Daily execution throughout week
- `/weekly-plan` - Set priorities at start of week
- `/meeting-notes` - Captured throughout week

**After this:**
- `/weekly-plan` - Plan next week immediately after review
- `/status-update` - Share summary with stakeholders
- `/decision-doc` - Formalize key decisions made

**Periodic use:**
- `/feature-results` - Monthly deep dive on launched features
- `/quarter-review` - (If exists) Quarterly synthesis of weekly reviews

---

## Output Quality Self-Check

Before delivering the weekly review, verify:

- [ ] **Plan vs. actual compared:** If a weekly plan existed, every planned priority is addressed with a status (complete, partial, not started) and a reason for any gap.
- [ ] **Learnings are specific and actionable:** Each learning includes what happened, why, and a concrete change for next time. "Work harder" is not a learning.
- [ ] **Next week priorities are drafted:** At least 3 draft priorities for next week are suggested, grounded in this week's outcomes and strategic goals.
- [ ] **Blockers have owners:** Every unresolved blocker has a specific action and person to contact on Monday.
- [ ] **Metrics referenced where available:** If launches happened or metrics data exists, actual numbers are cited (not just "things went well").
- [ ] **Appropriate length:** Default review is ~150 lines. Full review is longer but still organized with clear section headers. Do not generate a full review unless the user asked for one.
- [ ] **Honest about what did not go well:** The review includes at least one thing that did not go as planned, with root cause analysis. A review with only wins is incomplete.
