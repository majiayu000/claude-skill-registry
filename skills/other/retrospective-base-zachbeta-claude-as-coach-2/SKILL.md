---
name: retrospective-base
description: Framework for retrospectives at any time scale (daily, weekly, monthly, quarterly, yearly). Trigger with "daily retro", "weekly retro", "monthly retro", "[month] retro" (e.g., "december retro", "january retro"), "retro for [month]", or "end of month review". Answers three questions - what worked, what didn't, how to improve. Inputs vary by scale - daily uses raw logs, weekly uses daily summaries, monthly uses weekly retros, etc. Fractal compression pattern.
---

# Retrospective (Base Framework)

**Core insight:** The retrospective process is the same at any time scale. What changes is the inputs and the time horizon framing.

## The Three Questions

Every retrospective answers these three questions:

1. **What Worked?** → Do more of this
2. **What Didn't Work?** → Experiment on changing this
3. **How Do We Improve the Retro Process?** → Meta-improvement loop

That's it. Everything else is structure to support these questions.

## Time Scale as Parameter

| Scale | Inputs | Horizon | Output |
|-------|--------|---------|--------|
| Daily | Raw observations | 1 day | Daily summary |
| Weekly | Daily summaries | 7 days | Weekly retro |
| Monthly | Weekly retros | 4 weeks | Monthly retro |
| Quarterly | Monthly retros | 3 months | Quarterly retro |
| Yearly | Quarterly retros | 12 months | Yearly retro |

**Fractal pattern:** Each level compresses the previous level's outputs into inputs for the next.

## Process

### 1. Establish Boundaries

```bash
# Verify current date
TZ='America/New_York' date '+%A, %B %d, %Y - %I:%M %p %Z'
```

**Confirm the period being reviewed:**
- Daily: "Reviewing [Date]. Correct?"
- Weekly: "Reviewing [Start] - [End]. Correct?"
- Monthly: "Reviewing [Month Year]. Correct?"
- Quarterly: "Reviewing Q[X] [Year]. Correct?"
- Yearly: "Reviewing [Year]. Correct?"

### 2. Load Context

**Load inputs appropriate to scale:**
- Daily: Load today's notes/logs
- Weekly: Load daily summaries for the week
- Monthly: Load weekly retros for the month
- Quarterly: Load monthly retros for the quarter
- Yearly: Load quarterly retros for the year

**Also load:**
- Previous period's retro (for comparison)
- Current goals/plans at that scale
- Relevant project documents

**If inputs missing:** Note gaps, proceed with available data.

### Load Level Criteria from Plan

When a plan document exists for the period being reviewed:
1. Pull Level 0/1/2/3 criteria verbatim from the plan
2. Assess each criterion individually (✓/✗)
3. Roll up to overall level assessment
4. This is the primary success measure - Success Metrics table is secondary detail

### 3. Day-by-Day Review (Default for Weekly+)

**When to use:** Weekly or longer retrospectives with daily summaries available. This is the **default** approach for weekly retros - it's valuable enough to do every time.

**Purpose:** Before synthesizing patterns, walk through each day briefly. This surfaces details that might otherwise get lost and helps the user reconnect with the full week.

**Process:**
1. Present each day's summary briefly (2-3 key points per day)
2. Ask: "Anything to add or correct for [Day]?"
3. Let user react, add context, or say "looks right"
4. Move to next day
5. After walkthrough, create empty framework doc

**Why this helps:**
- Surfaces forgotten details ("Oh right, Tuesday was rough")
- Catches summary gaps or errors
- Warms up memory before synthesis
- Low effort (reactions, not generation)
- Produces condensed timeline for final doc

**Keep it light:** This is orientation, not analysis. Save synthesis for the main sections.

### 4. Show Empty Framework First

**CRITICAL:** Create structure-only artifact and explain it to user before filling anything.

**Process:**
1. Generate empty artifact with all section headers
2. Present to user: "Here's the structure we'll fill in together"
3. Briefly explain each section's purpose
4. Then proceed to fill ONE SECTION AT A TIME

**Why this matters:**
- User sees the whole picture before diving in
- Reduces cognitive load (knows what's coming)
- Enables reactions over generation

**Filename template:**
```
[Scale]-Retro-[Date-Range].md
```

**Examples:**
- `Daily-Summary-2025-12-05.md`
- `Weekly-Retro-2025-12-01-to-07.md`
- `Monthly-Retro-2025-12.md`
- `Quarterly-Retro-2025-Q4.md`
- `Yearly-Retro-2025.md`

### 5. Framework Structure

```markdown
# [Scale] Retro: [Theme/Title]

**Period:** [Date range]
**Context:** [Brief context line]

---

## TL;DR - [Period] Summary

**Format: Bulleted list for easy scanning**
- Major pattern 1
- Major pattern 2
- Key discovery
- Primary challenge
- Overall trajectory

---

## Day-by-Day Timeline (Weekly+)

**Include for weekly or longer retros. Condensed reference from day-by-day review.**

| Day | Date | Context Tag | Key Events |
|-----|------|-------------|------------|
| Mon | [Date] | [tag] | [1-2 key events] |
| Tue | [Date] | [tag] | [1-2 key events] |
| ... | ... | ... | ... |

**Context Tag:** Optional column for domain-specific state tracking (defined in personal extension).

---

## Plan vs Actual (Weekly+ When Plan Exists)

**Include for weekly, monthly, quarterly, yearly retros when a plan document exists.**

### Theme Assessment
**Planned theme:** [From plan]
**Did it hold?** [Yes/Partially/No + evidence]

### Success Metrics

| Area | Target | Actual | Assessment |
|------|--------|--------|------------|
| [Priority 1] | [Goal] | [Result] | ✓ Met / ◐ Partial / ✗ Below |
| [Priority 2] | [Goal] | [Result] | ✓ Met / ◐ Partial / ✗ Below |

### Level Assessment (from [Period] Plan)

**Level 0 (Foundation):** [✓ Met / ◐ Partial / ✗ Not met]
- [Criterion 1 from plan] [✓/✗]
- [Criterion 2 from plan] [✓/✗]

**Level 1 (Base):** [✓ Met / ◐ Partial / ✗ Not met]
- [Criterion 1 from plan] [✓/✗]
- [Criterion 2 from plan] [✓/✗]

**Level 2 (Target):** [✓ Met / ◐ Partial / ✗ Not met]
- [Criterion 1 from plan] [✓/✗]

**Level 3 (Reach):** [✓ Met / ◐ Partial / ✗ Not met] (if applicable)
- [Criterion 1 from plan] [✓/✗]

### Venn Diagram

**Planned Only:**
- [Things planned but didn't happen]

**Both:**
- [Things that happened as planned]

**Actual Only:**
- [Things that happened but weren't in the plan]

---

## What Worked (Want More Of)

[Fill conversationally through observations → reactions]

---

## What Didn't Work (+ Experiments to Try)

**Format: Challenge → Proposed experiments**

### Challenge 1: [Issue]
**Why problematic:** [Impact]
**Experiments to try:**
- **Next [shorter period]:** [Immediate test]
- **Next [current period]:** [Medium-term experiment]
- **Longer timeframe:** [Deferred approach]

---

## Progress Tracking

**Compare against relevant intervals:**

### Last [Period]
**Previous:** [Summary]
**Current:** [Summary]
**Trajectory:** [Better/Stable/Declining + evidence]

### Longer Timeframe (if data available)
**Then:** [State]
**Now:** [State]
**Arc:** [What shifted]

---

## [Scale]-Retro (Improve This Process)

[Meta observations about the retrospective itself]
- What worked about this retro format?
- What was awkward or missing?
- Skill updates needed?

---

## Gratitude

[Positive closing anchor - peak-end rule]

What are you grateful for from this [period]?
```

### 6. Fill ONE QUESTION AT A TIME

**⚠️ CRITICAL: Ask one question, wait for response, update artifact, then move to next.**

**Pattern per section:**
1. Make observation from input data
2. Ask ONE focused question about that observation
3. Wait for user response
4. Update artifact in real-time
5. Confirm before moving to next section

**Lead with observations, not open questions:**
- ✅ "I noticed [pattern]. Want more of that?"
- ✅ "[Challenge] kept coming up. What experiment addresses it?"
- ❌ "What was most significant?" (requires generation from scratch)
- ❌ Asking multiple questions at once

**Pacing by section:**
- "What Worked" → flows fast (observation → agreement)
- "What Didn't Work" → needs depth (experiments develop interactively)
- "Retro-Retro" → one question about process
- "Gratitude" → save for last (positive anchor)

### 7. Save and Archive

**Save to:** `/mnt/user-data/outputs/[filename]`

**Remind user:** "Click 'add to project' to save permanently."

**Archive previous level's inputs:**
- After weekly retro → archive daily summaries
- After monthly retro → archive weekly retros
- Keeps context lean, preserves history locally

## Core Principles

**Same questions, any scale:** The three questions work whether you're reviewing a day or a year.

**Inputs compress to outputs:** Each retro compresses its inputs into a summary that becomes input for the next level.

**Observations → Reactions:** Humans react better than they generate from scratch.

**Experiments over judgments:** "What didn't work + what to try" beats "what failed."

**Peak-end rule:** End with gratitude regardless of period difficulty.

**Meta-improvement:** The retro process itself should improve over time.

## Edge Cases

**First retro at a scale:**
- Skip comparisons (no previous data)
- Focus on establishing baseline patterns

**Missing inputs:**
- Proceed with available data
- Note gaps for future improvement

**Combined scales:**
- Can do weekly + monthly in same session if context allows
- Natural flow: weekly insights → monthly synthesis

## Flexibility

**Structure is guide, not prescription:**
- Skip sections if not relevant
- Add domain-specific sections
- Adapt length to complexity
- Focus on signal over noise
