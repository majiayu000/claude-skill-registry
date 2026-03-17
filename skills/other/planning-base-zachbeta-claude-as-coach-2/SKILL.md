---
name: planning-base
description: Framework for planning at any time scale (daily, weekly, monthly, quarterly, yearly). Trigger with "plan my day", "weekly planning", "monthly planning", "[month] planning" (e.g., "january planning", "december planning"), "plan for [period]", or "let's plan [period]". Identifies constraints FIRST, then suggests priorities. Uses Level 0-3 success framework. Inputs vary by scale - daily uses yesterday summary, weekly uses weekly retro, monthly uses monthly retro, etc.
---

# Planning (Base Framework)

**Core insight:** The planning process is the same at any time scale. What changes is the inputs, the time horizon, and the granularity of experiments.

## The Core Structure

Every planning session covers:

1. **Coming From** → Where capacity/state is now
2. **Constraints** → What's fixed that we plan around
3. **Priorities** → 2-3 key focuses (max)
4. **Experiments** → What to test/try/explore
5. **Success Levels** → What "good enough" looks like (0-3)

## Time Scale as Parameter

| Scale | Inputs | Horizon | Output |
|-------|--------|---------|--------|
| Daily | Yesterday's summary | 1 day | Today's focus |
| Weekly | Weekly retro | 7 days | Weekly plan |
| Monthly | Monthly retro | 4 weeks | Monthly plan |
| Quarterly | Quarterly retro | 3 months | Quarterly plan |
| Yearly | Yearly retro | 12 months | Yearly plan |

**Natural flow:** Retro → Planning at same scale. Insights fresh, immediately inform forward planning.

## Process

### 1. Establish Boundaries

```bash
# Verify current date
TZ='America/New_York' date '+%A, %B %d, %Y - %I:%M %p %Z'
```

**Confirm the period being planned:**
- Daily: "Planning [Date]. Correct?"
- Weekly: "Planning [Start] - [End]. Correct?"
- Monthly: "Planning [Month Year]. Correct?"
- Quarterly: "Planning Q[X] [Year]. Correct?"
- Yearly: "Planning [Year]. Correct?"

### 2. Load Context

**Load inputs appropriate to scale:**
- Daily: Yesterday's summary, today's calendar
- Weekly: This week's retro, monthly goals
- Monthly: This month's retro, quarterly goals
- Quarterly: This quarter's retro, yearly goals
- Yearly: This year's retro, multi-year vision

**Purpose:** Understand current capacity and context before planning.

### 3. Identify Constraints FIRST ⚠️ CRITICAL

**Before suggesting priorities, identify what's fixed:**

Ask about:
- **Non-negotiables:** Deadlines, appointments, obligations (can't move)
- **Known drains:** High-effort tasks, energy-intensive work (need buffer)
- **Timeline pressures:** Reverse-engineering from future dates
- **Ongoing experiments:** Maintain consistency, don't disrupt data

**Scale-appropriate questions:**
- Daily: "What's on the calendar? Any energy drains today?"
- Weekly: "What commitments this week? Any dense days?"
- Monthly: "Major milestones? Travel? Known capacity constraints?"
- Quarterly: "Key deliverables? Seasonal factors?"
- Yearly: "Major life events? Strategic bets?"

**Why this matters:** Suggesting priorities that ignore fixed constraints = plan sets user up for failure.

### 4. Create Empty Framework First

**⚠️ CRITICAL:** Create structure-only artifact BEFORE filling content.

**Process:**
1. Generate empty artifact with all section headers
2. Present to user: "Here's the structure we'll fill in together"
3. Briefly explain each section's purpose
4. Then proceed to fill ONE SECTION AT A TIME

**Why this matters:**
- User sees the whole picture before diving in
- Reduces cognitive load (knows what's coming)
- Enables reactions over generation
- Catches nuances that full-draft approach misses

**After constraints identified, create initial artifact.**

**Filename template:**
```
[Scale]-Plan-[Date-Range].md
```

**Examples:**
- `Daily-Focus-2025-12-05.md`
- `Weekly-Plan-2025-12-01-to-07.md`
- `Monthly-Plan-2025-12.md`
- `Quarterly-Plan-2025-Q1.md`
- `Yearly-Plan-2026.md`

### 5. Framework Structure

```markdown
# [Scale] Plan: [Theme/Focus]

**Period:** [Date range]

---

## Coming From

- [Capacity insight from retro]
- [Major constraints identified]
- [What worked/didn't from previous period]
- [2-3 bullets max, scannable]

---

## Constraints

**Fixed:**
- [Non-negotiable deadlines, appointments]
- [Known drains or high-effort days]

**Important Dates (Weekly+):**

| Date | Event | Notes |
|------|-------|-------|
| [Date] | [Event] | [Context] |

---

## This [Period]'s Priorities

Based on constraints and patterns:

1. [Priority 1 - often constraint-driven]
2. [Priority 2 - from "what worked" + goals]
3. [Priority 3 - stretch, optional]

Does this ordering work given [specific constraint]?

---

## Experiments to Try

**Aligned to success levels:**

**Level 0-1 (Foundation/Base):**
- [Experiment supporting minimum viable progress]

**Level 2 (Target):**
- [Experiment for good week given capacity]

**Level 3 (Reach):**
- [Stretch experiment if everything aligns]

---

## Week Structure (Weekly Plans)

**Include for weekly plans. Day-by-day focus mapping.**

| Day | Date | Focus | Key Activities |
|-----|------|-------|----------------|
| Mon | [Date] | [Primary focus] | [1-2 activities] |
| Tue | [Date] | [Primary focus] | [1-2 activities] |
| ... | ... | ... | ... |

---

## Success Looks Like

### Level 0: Foundation
*Minimum viable engagement with the [period]*
*What counts as "showed up" given current context*
[Fill conversationally]

### Level 1: Base
[Minimum viable progress given current capacity]

### Level 2: Target
[Good [period] for current capacity]

### Level 3: Reach
[Exceptional but achievable]

**Good enough = Level 0 always counts. Level 1 is solid. Level 2 is great. Level 3 is amazing.**

---

## Notes

[Period-specific context, reminders, meta-observations]
```

### 6. Fill ONE SECTION AT A TIME

**⚠️ CRITICAL: Do not generate full document on first pass.**

**Pattern per section:**
1. Make suggestion based on constraints + retro data
2. Ask ONE focused question about that suggestion
3. Wait for user response
4. Update artifact in real-time
5. Confirm before moving to next section

**Interpreting user responses:**
- "proceed" / "continue" / "this is fine" = **move to NEXT SECTION**, not skip to end
- "good enough" = section approved, move on
- "let's discuss" = stay in this section, go deeper

**Do NOT:**
- Generate full document then ask for rubber stamp
- Interpret "proceed" as permission to finish everything
- Skip the conversational calibration on Success Levels

**Pacing by section:**
- "Coming From" → flows fast (pull from retro)
- "Priorities" → needs depth (constraint-aware suggestions → reactions)
- "Experiments" → semi-automatic (select from retro proposals)
- "Success Levels" → interactive (calibrate to current capacity)

**Core principle:** Constraints → Suggestions → Reactions → Refinement

### 7. Save Final Version

**Save to:** `/mnt/user-data/outputs/[filename]`

**Remind user:** "Click 'add to project' to save permanently."

## Success Level Framework

**Level 0: Foundation**
- Always counts
- "I engaged with this at all"
- Protects against all-or-nothing thinking
- Even on hardest days, L0 is achievable

**Level 1: Base**
- Solid progress given capacity
- Sustainable, repeatable
- Not heroic, just consistent

**Level 2: Target**
- What a good [period] looks like
- Stretch but realistic
- Builds momentum

**Level 3: Reach**
- Exceptional outcome
- Everything aligned
- Amazing but not required

**Calibration:** Levels adapt to current capacity. Level 2 during recovery ≠ Level 2 at full capacity.

**Important:** These levels become the primary assessment criteria in the retrospective. Write them clearly so future-you can assess each criterion with ✓/✗.

## Decision Filter (Monthly+)

**For monthly and longer plans, create a 2-question filter to test proposed activities.**

Every activity should pass both questions to proceed. This prevents scope creep and keeps focus on what matters.

**Template:**
1. Does this [action aligned with theme]?
2. Does this [build toward next milestone]?

**Examples:**

*Month 1 (Build Foundation):*
1. Does this build toward the target distance/skill?
2. Can I sustain this without injury/burnout?

*Month 2 (Increase Volume):*
1. Does this increase capacity appropriately?
2. Does this maintain recovery balance?

*Month 3 (Race Prep):*
1. Does this prepare me for the target event?
2. Does this avoid overtraining before the goal?

**Usage:** When new opportunities or tasks arise mid-period, run them through the filter. Both YES = proceed. One NO = defer or delegate. Both NO = decline.

## Core Principles

**2-3 priorities max:** More than that diffuses focus.

**Constraints first:** Understand what's fixed before suggesting what's flexible.

**Work with what is:** Start from actual capacity, not imagined capacity.

**Experiments over commitments:** Frame as tests, not obligations. Permission to pivot.

**Level 0 always counts:** Foundation protects against perfectionism spirals.

**Plans are hypotheses:** Execution adapts in real-time. Retro captures what actually happened.

## Edge Cases

**First plan at a scale:**
- No retro to pull from
- Start with constraint identification
- Set conservative success levels
- Retro at end will establish patterns

**Retro → Planning same session:**
- Natural flow if context headroom available
- Check tokens before proceeding
- Benefits: insights fresh, no context loss
- Risk: may max out mid-planning

**Capacity unknown:**
- Set Level 0 very low
- Let the period reveal capacity
- Retro will capture what was actually possible

## Planning-Retro (Meta-Improvement)

**At end of planning session, briefly reflect:**

- What worked about this planning process?
- What was awkward or missing?
- Skill updates needed?

**Document in Notes section of plan.**

## Flexibility

**Structure is guide, not prescription:**
- Skip sections if not relevant
- Add domain-specific sections
- Adapt length to complexity
- Focus on actionable over comprehensive

**Different scales, same muscles:**
- Daily planning is quick (5-10 min)
- Weekly planning is medium (20-30 min)
- Monthly+ planning is deeper (45-60 min)
- Same structure, different depth
