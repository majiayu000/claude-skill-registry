---
name: prioritize
description: Classify PM tasks using LNO Framework (Leverage/Neutral/Overhead) to focus on high-impact work.
disable-model-invocation: false
user-invocable: true
---

# Task Prioritization: LNO Framework

**When to use:** When overwhelmed with tasks, during weekly planning, or when feeling busy but not productive

**Framework source:** Shreyas Doshi's LNO Framework (popularized by Aakash Gupta)

## Quick Start

1. Paste your task list (calendar, to-do list, or just describe your week)
2. I will classify each task as **L** (Leverage/10x), **N** (Neutral/1x), or **O** (Overhead/<1x)
3. I will calculate your L/N/O time distribution and compare to the healthy target (40/35/20)
4. I will suggest specific tasks to eliminate, delegate, or timebox
5. Output: a prioritized weekly plan with calendar blocking recommendations

**Healthy target:** 40-50% Leverage, 30-40% Neutral, 10-20% Overhead. If Leverage is below 30%, something is wrong.

---

## The LNO Framework

Classify every task into one of three categories:

### L = Leverage Tasks (10x your impact)

**Definition:** Activities that disproportionately increase your impact

**Characteristics:**
- High effort, HIGH impact
- Compound over time
- Often urgent AND important
- Create lasting value

**Examples:**
- Writing a PRD that aligns 5 teams
- Building a dashboard that automates reporting
- Creating a decision framework teams can reuse
- Designing an onboarding flow that improves activation
- Strategic 1:1s with key stakeholders
- User research that uncovers major insights

**Impact:** 10x

---

### N = Neutral Tasks (Regular impact)

**Definition:** Necessary work with linear impact

**Characteristics:**
- Regular effort, regular impact
- Doesn't compound
- Often important but not urgent
- Maintenance work

**Examples:**
- Routine status updates
- Standard sprint planning
- Responding to most emails
- Attending most meetings
- Bug triage (non-critical)
- Backlog grooming
- Documentation (routine)

**Impact:** 1x

**The key insight:** Aim for C+/B- on Neutral tasks
- Don't overinvest
- Good enough is fine
- Preserve energy for Leverage tasks

---

### O = Overhead Tasks (Minimal impact)

**Definition:** Activities with very little impact relative to time spent

**Characteristics:**
- High effort, LOW impact
- Feels urgent but isn't important
- Often reactive
- Creates no lasting value

**Examples:**
- Most Slack threads (especially drama/politics)
- Meetings you're CC'd on "just in case"
- Over-polishing decks for internal reviews
- Formatting documents obsessively
- Responding to every FYI email
- Bikeshedding in design reviews
- Arguing over naming conventions
- Attending meetings where you have no input

**Impact:** Near zero

**Goal:** Minimize, delegate, automate, or eliminate

---

## How to Use This Framework

### Step 1: Audit Your Current Week

List everything you did last week:

```
Use /prioritize

Here's everything I did last week:
[paste your calendar/task list]

Help me classify each task as L, N, or O.
Then calculate:
- % time spent on Leverage tasks
- % time spent on Neutral tasks
- % time spent on Overhead tasks
```

**Healthy distribution for senior PMs:**
- Leverage: 40-50%
- Neutral: 30-40%
- Overhead: 10-20%

**If you're below 30% Leverage, something's wrong.**

---

### Step 2: Classify Tasks Before Doing Them

Before you work on something, ask:

**Is this Leverage?**
- Will this create disproportionate impact?
- Will this compound over time?
- If yes → Do it yourself, invest deeply

**Is this Neutral?**
- Is this necessary but not game-changing?
- Can I do "good enough" instead of perfect?
- If yes → Timebox it, aim for B- quality

**Is this Overhead?**
- Could I not do this and nothing bad happens?
- Am I doing this out of obligation, not impact?
- If yes → Delegate, automate, or skip

---

### Step 3: Protect Your Leverage Time

**Block calendar time for Leverage work:**
- Monday morning: 3-hour strategy block
- Wednesday afternoon: 2-hour deep work
- Friday morning: 2-hour planning/thinking time

**Treat it like a meeting:**
- Decline conflicting invitations
- Turn off Slack
- Close email

---

## Specific Tactics by Category

### Tactics for Leverage Tasks:

**1. Do them FIRST**
- Morning energy > afternoon energy
- Don't wait until "everything else is done"

**2. Invest disproportionately**
- Spend 8 hours on a 10x task
- Don't spend 1 hour on 8 different 1x tasks

**3. Seek multipliers**
- Build frameworks others can reuse
- Create templates that scale
- Automate repetitive decisions

**4. Example weekly planning:**
```
Monday AM: Write high-impact PRD (Leverage)
Monday PM: Routine meetings (Neutral)
Tuesday AM: User research synthesis (Leverage)
Tuesday PM: Sprint planning (Neutral)
Wednesday AM: Strategic 1:1s with stakeholders (Leverage)
Wednesday PM: Bug triage (Neutral)
Thursday AM: Build metrics dashboard (Leverage)
Thursday PM: Status updates (Neutral)
Friday AM: Reflect & plan next week (Leverage)
Friday PM: Clear Slack backlog (Overhead - timeboxed)
```

---

### Tactics for Neutral Tasks:

**1. Timebox ruthlessly**
- Sprint planning: 60 minutes MAX
- Status updates: 30 minutes
- Email: 2x/day for 20 minutes each

**2. Use templates**
- Status update template
- Meeting notes template
- Decision log template
- Don't reinvent each time

**3. Batch similar tasks**
- All status updates on Friday
- All 1:1s on Tuesday/Thursday
- All email at 9am and 3pm

**4. Aim for B- quality**
- Status update doesn't need perfect prose
- Meeting notes don't need perfect formatting
- Backlog grooming doesn't need perfect prioritization

**The mantra:** "Good enough is great for Neutral tasks"

---

### Tactics for Overhead Tasks:

**1. Eliminate**
- Decline meetings where you're optional
- Unsubscribe from FYI email threads
- Leave Slack channels you don't contribute to

**2. Delegate**
- Can an APM or intern handle this?
- Can engineering lead own this decision?
- Can designer lead the review?

**3. Automate**
- Set up Slack status: "Focus time 9-12, async responses only"
- Create email filters and auto-responses
- Build dashboards instead of manual reports

**4. Say no**
- "I don't think I can add value to this meeting"
- "Can you send me the notes instead?"
- "Let's async this in a doc rather than meet"

**Example overhead elimination:**
- 10 meetings/week → 6 meetings (saved 4 hours)
- 2 hours Slack → 30 min (saved 1.5 hours)
- 1 hour manual reporting → automated (saved 1 hour)
- **Total reclaimed: 6.5 hours/week for Leverage work**

---

## Weekly Planning Template

Use this every Sunday or Friday:

### 1. Leverage Tasks This Week (Aim for 3-5)
- [ ] Task 1: ___________ (Time: ____ hours)
- [ ] Task 2: ___________ (Time: ____ hours)
- [ ] Task 3: ___________ (Time: ____ hours)

**Total Leverage hours: _____ / 40 hours (Target: 40%+)**

### 2. Neutral Tasks (Necessary)
- [ ] Task 1: ___________ (Timeboxed: ____ min)
- [ ] Task 2: ___________ (Timeboxed: ____ min)
- [ ] Task 3: ___________ (Timeboxed: ____ min)

### 3. Overhead to Eliminate/Delegate
- ~~Task 1~~ → Declined/delegated to _____
- ~~Task 2~~ → Automated with _____
- ~~Task 3~~ → Skipping (no impact)

### 4. Calendar Blocks
- [ ] Monday 9-12: Leverage block (no meetings)
- [ ] Wednesday 2-4: Leverage block (no meetings)
- [ ] Friday 9-11: Reflect & plan

---

## Real-World Examples

### Example 1: Writing a PRD

**Leverage approach:**
- Spend 8 hours writing a comprehensive PRD
- Get input from engineering, design, data
- Create clear alignment across 5 teams
- Result: Smooth execution, no mid-sprint confusion
- **ROI: 10x** (saves 80 hours of misalignment downstream)

**Neutral approach:**
- Spend 2 hours on quick spec
- Just enough to start building
- Some gaps, but good enough
- Result: Team can start, questions arise later
- **ROI: 1x** (regular productivity)

**Overhead approach:**
- Spend 8 hours making the PRD perfect
- Obsess over formatting and edge cases
- No one reads the 20-page doc anyway
- Result: Time wasted, no added value
- **ROI: <1x** (negative productivity)

---

### Example 2: Stakeholder Update

**Leverage approach:**
- Create reusable dashboard that auto-updates weekly
- Spend 4 hours building it once
- Result: Never manually report again, stakeholders self-serve
- **ROI: 10x** (saves 1 hour/week = 52 hours/year)

**Neutral approach:**
- Send weekly email with 3 bullet points
- Takes 30 minutes
- Result: Stakeholders informed, expectations met
- **ROI: 1x** (necessary, but not multiplier)

**Overhead approach:**
- Create 10-slide deck every week
- Spend 2 hours formatting and polishing
- Result: No one asks for this level of detail
- **ROI: <1x** (wasted effort)

---

## Common Mistakes

### Mistake #1: Treating All Tasks Equally

**Problem:** Spending 1 hour on 10 tasks instead of 10 hours on 1 Leverage task

**Fix:** Prioritize ruthlessly. Say no to good things to say yes to great things.

---

### Mistake #2: Perfectionism on Neutral Tasks

**Problem:** Spending 3 hours on a status update that deserves 20 minutes

**Fix:** Set a timer. Aim for B-. Ship it.

---

### Mistake #3: Not Blocking Leverage Time

**Problem:** Meetings fill your calendar, no time for deep work

**Fix:** Block 2-3 mornings per week. Treat them as non-negotiable.

---

### Mistake #4: Confusing Urgent with Important

**Problem:** Overhead tasks FEEL urgent (Slack pings, meeting invites)

**Fix:** Distinguish:
- Urgent + Important = Leverage or Neutral
- Urgent + Unimportant = Overhead (ignore or delegate)
- Not Urgent + Important = Leverage (block time)
- Not Urgent + Unimportant = Overhead (eliminate)

---

## LNO Self-Audit Questions

Ask yourself weekly:

**Leverage:**
- [ ] Did I spend 40%+ of my time on Leverage tasks?
- [ ] Did I create something that multiplies my impact?
- [ ] Will this work compound over time?

**Neutral:**
- [ ] Did I timebox Neutral tasks effectively?
- [ ] Did I aim for "good enough" instead of perfect?
- [ ] Could I have batched these more efficiently?

**Overhead:**
- [ ] What did I do this week that had near-zero impact?
- [ ] What meetings could I have skipped?
- [ ] What tasks can I eliminate next week?

---

## Advanced: LNO for Career Growth

**Apply LNO to career decisions:**

### Leverage career moves:
- Taking on a high-visibility project
- Building relationships with executives
- Developing a unique expertise (AI PM, growth, platform)
- Writing/speaking publicly

### Neutral career moves:
- Meeting performance expectations
- Completing assigned projects
- Networking within your org

### Overhead career moves:
- Office politics that go nowhere
- Working on projects no one cares about
- Staying in a role too long (no growth)

**Focus on Leverage career moves to accelerate growth.**

---

## Related Skills

- `/strategy-sprint` - Leverage strategy work
- `/prd-draft` - Leverage through great PRDs
- `/activation-analysis` - Leverage through product improvements
- `/user-research-synthesis` - Leverage through insights

---

## Delegation Awareness

**For VP/Director-level PMs managing a team,** add a "Delegation Recommendation" column to the task classification.

| Task | LNO | Est. Hours | Delegation Recommendation |
|------|-----|-----------|--------------------------|
| Write activation PRD | L | 8 | Do yourself -- high strategic value |
| Sprint planning | N | 1 | Delegate to tech lead or senior engineer |
| Status update deck | N | 1.5 | Delegate to APM or program manager |
| Bug triage review | O | 1 | Delegate to engineering lead |
| Formatting PRD template | O | 0.5 | Delegate to APM or skip entirely |

**Rules:**
- **Leverage tasks:** Generally do these yourself. They are your highest-value contribution.
- **Neutral tasks:** For each, ask: "Could someone on my team do this at B- quality?" If yes, delegate. Reference names from stakeholder profiles in `context-library/stakeholder-template.md`.
- **Overhead tasks:** Always delegate, automate, or eliminate. If you cannot delegate, timebox aggressively (set a hard stop).

---

## Team Capacity Check

After classifying tasks, check total estimated hours against available time:

1. **Calculate available deep work hours:** Total work hours minus meetings = deep work hours available.
2. **Sum Leverage task hours:** Add up all Leverage task estimates.
3. **Compare:**
   - If Leverage hours fit within deep work time: You are in good shape. Proceed.
   - If Leverage hours exceed deep work time: **Flag this.** You have more Leverage tasks than time. Consider:
     1. Moving the lowest-impact Leverage item to next week
     2. Delegating a subtask within a Leverage item (e.g., delegate data gathering, keep the synthesis)
     3. Reducing scope on the lowest-impact Leverage item (aim for 80% instead of 100%)
   - If Leverage hours are less than 30% of available time: You are under-investing. Look at Neutral tasks that could be elevated to Leverage with more investment (e.g., turning a routine status update into a reusable dashboard).

---

**Framework credit:** Shreyas Doshi's LNO Framework. Read Aakash Gupta's article: https://www.news.aakashg.com/p/lno-framework-for-product-managers

---

## Context Routing Strategy

When the PM uses `/prioritize`, I automatically:

### 1. Analyze Your Task List Against Strategy
**Source:** `context-library/strategy/`, OKRs, quarterly goals
- **What I look for:** Strategic priorities vs. your task list
- **How I use it:** Classify tasks against declared strategy
- **Example:** "Strategy says focus on retention, but you're 60% on new feature work → recalibrate"

### 2. Extract LNO Patterns from Your Work
**Source:** Calendar, recent decisions, PRDs worked on
- **What I look for:** What types of work you gravitate toward
- **How I use it:** Show bias (e.g., "You're 70% on overhead, underweighting leverage")
- **Example:** "You created 3 PRDs this week (leverage), but spent 2hrs fixing formatting (overhead)"

### 3. Benchmark Against Healthy Distribution
**Source:** LNO framework standards, your past healthy weeks
- **What I look for:** Historical high-performing weeks for you
- **How I use it:** Suggest realistic targets based on your pattern
- **Example:** "Your best weeks are 45% leverage, 35% neutral, 20% overhead"

### 4. Identify Overhead Elimination Opportunities
**Source:** Stakeholder calendar, team habits
- **What I look for:** Recurring meetings, tasks that are truly non-essential
- **How I use it:** Suggest specific elimination tactics with owners
- **Example:** "Weekly status meeting could go async (save 2 hrs). Suggest to manager."

### 5. Flag Leverage Opportunities
**Source:** Current work, strategic goals
- **What I look for:** What if you invested deeper in leverage work?
- **How I use it:** Quantify ROI of shifting time
- **Example:** "If you spent 10 hrs on metrics dashboard, saves 1 hr/week = 52 hrs/year"

### 6. Route for Action
**Routing logic:**
- **Define leverage work:** Link to `/prd-draft`, `/write-prod-strategy`
- **Create blockers list:** Use `/slack-message` to request overhead elimination
- **Track time:** Suggest time-blocking strategies to protect leverage time
- **Weekly audit:** Use this weekly to course-correct

---

## Output Quality Self-Check

Before delivering the prioritization output, verify:

- [ ] **Every task classified:** No task is left without an L, N, or O label. If classification is ambiguous, explain why.
- [ ] **Time estimates included:** Each task has an estimated time in hours or minutes.
- [ ] **Distribution calculated:** L/N/O percentages are shown and compared to the 40/35/20 target.
- [ ] **Capacity check done:** Total Leverage hours are compared against available deep work time. If over capacity, specific recommendations are provided.
- [ ] **Actionable recommendations:** At least 2-3 specific overhead tasks are flagged for elimination or delegation, with a suggested alternative (who to delegate to, or why it can be skipped).
- [ ] **Calendar blocking suggested:** Specific time blocks are recommended for Leverage work (e.g., "Block Monday 9-12 for PRD writing").
- [ ] **Strategy alignment checked:** Leverage tasks are validated against current strategic priorities from `context-library/strategy/`. If a Leverage task does not connect to strategy, flag it.
