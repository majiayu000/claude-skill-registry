---
name: shape-up
description: "Escape the build trap and endless backlogs. Use Basecamp's methodology to ship meaningful work in 6-week cycles with fixed time, variable scope. Use when: **Product planning** to replace endless backlogs; **Feature development** with clear time boundaries; **Team autonomy** when you want self-directed teams; **Scope management** when projects tend to balloon; **Startup development** with limited resources"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Shape Up

> Escape the build trap and endless backlogs. Use Basecamp's methodology to ship meaningful work in 6-week cycles with fixed time, variable scope.

## When to Use This Skill

- **Product planning** to replace endless backlogs
- **Feature development** with clear time boundaries
- **Team autonomy** when you want self-directed teams
- **Scope management** when projects tend to balloon
- **Startup development** with limited resources
- **Agency/consulting projects** with fixed timelines

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | Ryan Singer - Shape Up (2019), developed at Basecamp |
| **Core Principle** | "Fixed time, variable scope. Appetite, not estimates. Shape before you build." |
| **Why This Matters** | Traditional methods either micromanage (waterfall) or leave too much open (agile sprints without direction). Shape Up gives teams direction AND autonomy. |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Introduces shaping** - Defining work at the right level of abstraction
2. **Sets appetites over estimates** - How much time is this worth?
3. **Enables cycles** - 6-week focused work, 2-week cooldown
4. **Empowers teams** - Autonomy within boundaries
5. **Provides betting tables** - Principled prioritization
6. **Manages scope dynamically** - Must-haves vs. nice-to-haves

## How to Use

### Shape a Feature Idea
```
I want to shape this feature idea: [description]
Apply Shape Up methodology to define it at the right level.
Appetite: [2 weeks / 6 weeks]
```

### Plan a Cycle
```
We have these potential projects for the next cycle:
[List of ideas]
Help me run a betting table to decide what to build.
```

### Manage Scope During Build
```
We're in week 3 of a 6-week cycle building [feature].
We're running behind. Help me apply Shape Up scope hammering.
```

## Instructions

### Step 1: Understand the Shape Up Principles

```
## The Shape Up Philosophy

### Fixed Time, Variable Scope

**Traditional approach:**
"How long will this take?" → Estimate → Build → Deadline slips

**Shape Up approach:**
"How much time is this worth?" → Appetite → Shape to fit → Ship on time

**The mindset shift:**
Instead of estimating how long a feature will take,
decide how much time you're willing to spend.
Then shape the work to fit that time.

### Appetite, Not Estimates

**Appetite:** How much time is this problem WORTH solving?

- Small batch: 2 weeks or less
- Big batch: 6 weeks max

**Key insight:**
A feature can be built in 2 weeks OR 6 months.
The question is: What version fits your appetite?

**Example:**
"Auto-complete for search"
- 6-month version: ML-powered, personalized, learns preferences
- 6-week version: Pre-populated common searches, basic matching
- 2-week version: Static list of top searches

All solve the problem. Choose based on appetite.

### Shaping vs. Building

**Shaping (Senior people):**
- Define the problem
- Set boundaries
- Identify risks
- Rough solution direction
- Leave room for builder creativity

**Building (Teams):**
- Detailed implementation
- Technical decisions
- UX specifics
- Scope management within boundaries
```

---

### Step 2: The Shaping Process

```
## How to Shape Work

### Step 1: Set the Appetite

Before anything else, decide:
- Is this a **small batch** (2 weeks) or **big batch** (6 weeks)?
- Is this worth doing at all at this appetite?

**Questions to ask:**
- What problem are we solving?
- How painful is this problem?
- What's the opportunity cost of not doing it?
- What's the opportunity cost of spending more time on it?

### Step 2: Narrow the Problem

Don't shape "improve search."
Shape "help new users find their first project template."

**Narrowing technique:**
1. Start with the raw idea
2. Ask: Who specifically has this problem?
3. Ask: In what specific situation?
4. Ask: What's the minimum viable solution?

### Step 3: Rough Out the Solution

**Fat marker sketches:**
Draw the solution with a thick marker (no detail).
You're defining spaces and flows, not buttons and fields.

**Breadboarding:**
For flows, use words not wireframes:
```
[Search box] → [Results page] → [Template detail]
              ↓
         [No results] → [Suggest categories]
```

**Key principle:**
Leave room for the builders to be creative.
Define WHAT, not exactly HOW.

### Step 4: Identify Risks and Rabbit Holes

**Rabbit holes:** Technical or design problems that could explode in scope.

**For each potential rabbit hole:**
- Name it
- Decide: Solve it in shaping? Or declare it out of scope?
- Document the boundary

**Example:**
"If we build template search, what about user-generated templates?"
Decision: Out of scope. Only show official templates.

### Step 5: Write the Pitch

**Pitch elements:**
1. **Problem:** What are we solving?
2. **Appetite:** How long is this worth?
3. **Solution:** Fat marker sketch / breadboard
4. **Rabbit holes:** What we're explicitly NOT doing
5. **No-gos:** Boundaries and constraints
```

---

### Step 3: The Cycle

```
## Six-Week Cycles

### The Rhythm

**6 weeks building:**
- Long enough for meaningful work
- Short enough to maintain urgency
- Teams own their projects completely

**2 weeks cooldown:**
- Bug fixes
- Technical debt
- Exploration
- Shaping for next cycle
- Recovery

### Why 6 Weeks?

**Shorter (2-week sprints):**
- Not enough time for real progress
- Constant planning overhead
- Work gets chopped up artificially

**Longer (quarters):**
- Deadlines feel far away
- Scope creeps
- No urgency until the end

**6 weeks:**
- Urgent from day one
- Room to figure things out
- Clean endpoint

### Team Structure

**Small teams:**
- 1-2 designers + 1-3 programmers
- Self-managed during the cycle
- No daily standups with managers
- Check-ins when THEY need help

**Circuit breaker:**
If work isn't done at 6 weeks, it doesn't automatically continue.
It goes back to the betting table. Maybe it gets another cycle.
Maybe it doesn't.

### What Teams Do in a Cycle

**Week 1-2: Figure it out**
- Understand the shaped work
- Spike on unknowns
- Get oriented
- Early integration

**Week 3-4: Build the core**
- Make vertical slices
- Connect the pieces
- Working software early

**Week 5-6: Polish and ship**
- Cut scope if needed
- Must-haves only
- Ship by end of cycle
```

---

### Step 4: The Betting Table

```
## Choosing What to Build

### The Betting Table

**Who:** Senior people who can make commitments
**When:** During cooldown, before next cycle
**Input:** Shaped pitches
**Output:** Cycle bets

### The Process

**1. Review pitches**
Each pitch should be complete:
- Clear problem
- Shaped solution
- Identified risks
- Appetite set

**2. Consider each bet**

For each pitch, ask:
- Is this the right time?
- Do we have the right team?
- Are there dependencies?
- What's the opportunity cost?

**3. Make decisions**

Options:
- **Bet:** Assign to next cycle
- **Park:** Good but not now
- **Kill:** Not worth doing

**No backlog:**
If you don't bet on something, it goes away.
Good ideas come back. Bad ideas don't.

### Betting Criteria

**1. Strategic fit**
Does this support current company goals?

**2. Problem significance**
How painful is this for customers?

**3. Appetite match**
Can this actually be done in the proposed time?

**4. Team availability**
Who would work on this?

**5. Dependencies**
What else needs to be true?

### Anti-Patterns

**Carry-over:**
"We didn't finish last cycle, so we'll continue."
No. Circuit breaker. Re-evaluate. Maybe it's not worth it.

**Backlog grooming:**
"Let's go through the 200 ideas and prioritize."
No. Only consider shaped pitches. Unshaped ideas aren't real options.

**Consensus:**
"Let's vote on what to build."
No. Decision-makers decide. Not democracy.
```

---

### Step 5: Managing Scope

```
## Scope Hammering

### The Principle

Scope grows naturally. Left unchecked, projects expand to fill time.
Your job is to constantly hammer scope back to what matters.

### Must-Haves vs. Nice-to-Haves

**Must-haves:**
- Core value delivery
- Without this, the feature doesn't work
- Absolutely required for ship

**Nice-to-haves:**
- Polish
- Edge cases
- Delighters
- "While we're at it..."

**Rule:** Identify nice-to-haves early. Cut them first.

### The Scope Hammer

**When you're behind (week 3+):**

1. **List all remaining work**
2. **Classify each item:**
   - Must-have for THIS version
   - Nice-to-have (cut or defer)
3. **Cut aggressively:**
   - What's the smallest version that still delivers value?
   - What can be a follow-up?
   - What can we not do at all?

### Scope Hammering Questions

- "Is this necessary for launch, or is it polish?"
- "What's the simplest version that still solves the problem?"
- "Can this be a fast-follow?"
- "What would happen if we just... didn't do this?"
- "Are we building for the 80% case or the edge case?"

### Hill Charts

**Track progress visually:**

```
        ┌─────────────────────────────────┐
        │                 ↗ Feature C     │
        │       ↗ Feature B               │
        │ ↗ Feature A            ↘ Feature D
        └─────────────────────────────────┘
         Figuring it out    Making it happen
```

- **Uphill:** Still figuring it out (risky)
- **Downhill:** Know what to do, just executing (safe)

**Use for:**
- Early warning when something is stuck uphill
- Identifying where help is needed
- Manager visibility without micromanagement
```

---

## Examples

### Example 1: Shaping a Feature

**Input:**
> "We want to add notifications to our project management app. Can you help me shape this using Shape Up?"

**Output:**

## Shaped Pitch: Project Notifications

### Problem

Users miss important updates because they only check the app occasionally.
When they do check, they see a firehose of activity with no way to know
what actually matters.

**Specific situation:** A project manager logs in after a day away and
can't quickly tell what needs their attention.

### Appetite

**6 weeks (Big Batch)**

Notifications are foundational. Worth investing in properly.
But not worth 3 months. We'll scope to fit 6 weeks.

### Solution

**Breadboard:**
```
[Activity happens] → [Notification created] → [Notification center]
                                                       ↓
                                              [Settings: what to notify]
```

**Fat marker sketch:**

```
┌─────────────────────────────────────┐
│ 🔔 (3)                              │  ← Bell in header with count
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │ ● @you in Project Alpha         │ │  ← Unread notifications
│ │   Sarah mentioned you in a...   │ │
│ │   2 hours ago                   │ │
│ ├─────────────────────────────────┤ │
│ │ ○ Task completed                │ │  ← Read notifications
│ │   Build specs was marked done   │ │
│ │   Yesterday                     │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

**What we're building:**
1. In-app notification center (bell icon, dropdown)
2. Notifications for: @mentions, task assignments, due dates
3. Basic settings (on/off per type)

### Rabbit Holes (Explicitly OUT of Scope)

**Email notifications:**
This is a whole separate system (deliverability, unsubscribes, formatting).
Out of scope. Potential future small batch.

**Mobile push notifications:**
Requires native app work. Out of scope.

**Notification grouping:**
"5 comments on Project Alpha" instead of 5 separate notifications.
Nice-to-have. Cut if we need time.

**Real-time updates:**
WebSockets for instant notifications. Nice-to-have.
Polling every 60 seconds is fine for V1.

**Customization per project:**
"Only notify me for Project X." Too complex.
Start with global settings only.

### No-Gos

- No email notifications
- No mobile push
- No notification sounds
- No digest/summary views
- No team-level settings

### Risks

**Risk 1: Database load**
Many notifications could be created. Need efficient queries.
*Mitigation:* Tech lead should spike on notification storage approach
in first 2 days of cycle.

**Risk 2: UX complexity**
Settings can get complicated fast.
*Mitigation:* Start with just 3 toggles. No per-project settings.

---

### Example 2: Scope Hammering Mid-Cycle

**Input:**
> "We're in week 4 of a 6-week cycle building a reporting dashboard. We're behind. We have: (1) 5 chart types planned, only 2 done, (2) Export to PDF not started, (3) Date filters mostly done, (4) Real-time refresh not started. Help me scope hammer."

**Output:**

## Scope Hammer: Reporting Dashboard

### Current Status (Week 4 of 6)

| Item | Status | Time Needed |
|------|--------|-------------|
| Chart types (5 planned) | 2 done | 1.5 weeks for remaining 3 |
| Export to PDF | Not started | 1 week |
| Date filters | 80% done | 2 days |
| Real-time refresh | Not started | 1 week |

**Total remaining work: ~4 weeks**
**Time available: ~2 weeks**

### Classification

**Must-Have (Core value delivery):**
- At least 3 chart types (line, bar, pie) - most common use cases
- Date filters - useless without filtering
- View/load reports - basic functionality

**Nice-to-Have (Cut or defer):**
- 4th and 5th chart types (table, area)
- Export to PDF
- Real-time refresh

### Recommendation

**Cut now:**
1. **Real-time refresh** → V2. Manual refresh button is fine.
2. **5th chart type (area)** → V2. Rarely used.
3. **Export to PDF** → V2. Users can screenshot or we do fast-follow.

**Keep:**
1. Date filters (finish in 2 days)
2. 3 chart types (line, bar, pie - 3-4 days for remaining 1)
3. 4th chart type (table) - useful for data review (3 days)

### Revised Scope

**Week 5:**
- Day 1-2: Finish date filters
- Day 3-4: Build pie chart (3rd type)
- Day 5: Build table view (4th type)

**Week 6:**
- Day 1-3: Polish, bug fixes, edge cases
- Day 4: Internal testing
- Day 5: Ship

### What to Tell Stakeholders

"We're shipping a fully functional dashboard with 4 chart types
(line, bar, pie, table) and date filters. Export and real-time refresh
will be fast-follows in the next small batch cycle.

This gives users 90% of the value. The remaining features are polish,
not core functionality."

### Post-Cycle Small Batch Candidates

- Export to PDF (2-week batch)
- Real-time refresh (2-week batch)
- Area chart type (1-week add-on)

---

### Example 3: Running a Betting Table

**Input:**
> "We have these 5 pitches for the next cycle. How do I run a betting table to decide? (1) Improved search, (2) Team permissions, (3) Mobile app redesign, (4) API for integrations, (5) Onboarding improvements"

**Output:**

## Betting Table: Next Cycle

### Pre-Work: Pitch Review

Each pitch should be shaped with:
- [ ] Clear problem statement
- [ ] Appetite (2-week or 6-week)
- [ ] Rough solution
- [ ] Rabbit holes identified
- [ ] No-gos defined

**Assessment:**

| Pitch | Shaped? | Appetite | Team Needed |
|-------|---------|----------|-------------|
| Improved search | ✓ Yes | 6 weeks | 1D + 2E |
| Team permissions | ✓ Yes | 6 weeks | 1D + 2E |
| Mobile app redesign | ✗ Too vague | ? | ? |
| API for integrations | ✓ Yes | 6 weeks | 0D + 3E |
| Onboarding improvements | ✓ Yes | 2 weeks | 1D + 1E |

**Mobile app redesign:** Not ready for betting. Needs shaping.
Send back. Consider for future cycle.

### Betting Criteria Evaluation

**1. Improved Search (6-week)**

| Criteria | Score | Notes |
|----------|-------|-------|
| Strategic fit | 4/5 | Supports growth, user requests |
| Problem significance | 3/5 | Pain for power users mainly |
| Appetite match | 4/5 | Well-scoped |
| Team availability | ✓ | Team A available |
| Dependencies | None | |

**Verdict:** CANDIDATE

**2. Team Permissions (6-week)**

| Criteria | Score | Notes |
|----------|-------|-------|
| Strategic fit | 5/5 | Required for enterprise deals |
| Problem significance | 5/5 | Blocking sales |
| Appetite match | 3/5 | Could expand, needs discipline |
| Team availability | ✓ | Team B available |
| Dependencies | None | |

**Verdict:** STRONG CANDIDATE

**3. API for Integrations (6-week)**

| Criteria | Score | Notes |
|----------|-------|-------|
| Strategic fit | 4/5 | Opens partner ecosystem |
| Problem significance | 3/5 | Important but not urgent |
| Appetite match | 4/5 | Scoped to read-only first |
| Team availability | ✓ | Team C available |
| Dependencies | None | |

**Verdict:** CANDIDATE

**4. Onboarding Improvements (2-week)**

| Criteria | Score | Notes |
|----------|-------|-------|
| Strategic fit | 5/5 | Direct impact on activation |
| Problem significance | 4/5 | 40% drop-off in onboarding |
| Appetite match | 5/5 | Small, focused scope |
| Team availability | ✓ | Fits in any team's cycle |
| Dependencies | None | |

**Verdict:** STRONG CANDIDATE (small batch)

### The Bet

**Available capacity:**
- 2 teams for 6-week bets
- 1 team has room for 2-week addition

**Decision:**

| Bet | Team | Rationale |
|-----|------|-----------|
| Team Permissions | Team B | Enterprise blocker, highest urgency |
| API for Integrations | Team C | Opens strategic opportunities |
| Onboarding Improvements | Team A (week 1-2) | High impact, small investment |
| Improved Search | *Parked* | Good but not highest priority now |

**What's NOT bet:**
- Mobile app redesign: Not shaped. Needs work.
- Improved search: Good pitch, wrong timing. Save for next cycle.

### Post-Betting Communication

"Next cycle:
- Team B: Team Permissions (6 weeks)
- Team C: API v1 (6 weeks)
- Team A: Onboarding improvements (2 weeks), then cooldown tasks

Search is a strong pitch. We're parking it for the following cycle.
Mobile app redesign needs more shaping before it's ready to bet."

---

## Checklists & Templates

### Pitch Template

```
## Pitch: [Feature Name]

### Problem
[What problem are we solving? Who has it? When?]

### Appetite
[2 weeks / 6 weeks]

### Solution

**Breadboard:**
[Flow diagram with words]

**Fat Marker Sketch:**
[Rough visual layout - no details]

### Rabbit Holes
[What could explode in scope? How are we preventing it?]

### No-Gos
[What are we explicitly NOT building?]

### Risks
[What could go wrong? How will we mitigate?]
```

---

### Betting Table Checklist

```
## Betting Table: [Cycle Name]

### Before the Meeting
□ All pitches reviewed for completeness
□ Incomplete pitches sent back for shaping
□ Team availability mapped
□ Strategic priorities clear

### During the Meeting
□ Review each complete pitch
□ Assess against betting criteria
□ Discuss dependencies and timing
□ Make binary decisions (bet / don't bet)
□ Assign teams to bets

### After the Meeting
□ Communicate decisions to teams
□ Archive or park unbetted pitches
□ Schedule cycle kickoffs
□ Clear any dependencies
```

---

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- Singer, Ryan. "Shape Up: Stop Running in Circles and Ship Work that Matters" (2019)
- Basecamp methodology documentation
- 37signals (Basecamp) blog posts
- Shape Up podcast appearances

## Related Skills

- [product-discovery](../product-discovery/) - Discovery before shaping
- [design-sprint](../design-sprint/) - Alternative sprint format
- [lean-canvas](../../validation/lean-canvas/) - Business model context
- [first-principles](../../thinking/first-principles/) - Problem definition

---

## Skill Metadata


- **Mode**: cyborg
```yaml
name: shape-up
category: product
subcategory: methodology
version: 1.0
author: MKTG Skills
source_expert: Ryan Singer
source_work: Shape Up
difficulty: intermediate
estimated_value: $5,000+ process consulting
tags: [product, process, Basecamp, cycles, shaping, scope, betting, development]
created: 2026-01-25
updated: 2026-01-25
```
