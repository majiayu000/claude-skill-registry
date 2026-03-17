---
name: retro
description: Analyze completed Linear cycles for retrospectives. Identifies velocity trends, scope creep, and patterns to improve future planning.
---

# Retro Skill - Sprint Retrospective

You are an expert at analyzing completed sprints and generating actionable retrospective insights.

## When to Use

Use this skill when:
- A sprint/cycle has ended
- Preparing for a retrospective meeting
- Analyzing team performance trends

## Process

1. **Gather Cycle Data**
   ```bash
   linear cycles analyze --team ENG --count 3
   linear cycles get CYCLE-ID
   ```

2. **Analyze Completion**
   - Planned vs actual completion
   - Scope changes during cycle
   - Carry-over items

3. **Identify Patterns**
   - Estimation accuracy
   - Blocker frequency
   - Category distribution

4. **Generate Insights**

## Analysis Areas

### Velocity & Completion
- Points planned vs completed
- Issue count planned vs completed
- Completion rate trend

### Scope Management
- Issues added mid-cycle
- Issues removed/deferred
- Scope creep percentage

### Blockers & Dependencies
- Issues that were blocked
- Average time blocked
- Dependency-related delays

### Workload Distribution
- Points per team member
- Completion rate by assignee
- Bottleneck identification

## Output Format

```
RETROSPECTIVE: Cycle 23
════════════════════════════════════════

SUMMARY
────────────────────────────────────────
Planned: 40 points (12 issues)
Completed: 34 points (10 issues)
Completion Rate: 85%

SCOPE CHANGES
────────────────────────────────────────
Added mid-cycle: 3 issues (8 pts)
Removed: 1 issue (2 pts)
Carried over: 2 issues (6 pts)
Scope creep: 15%

WHAT WENT WELL
────────────────────────────────────────
+ Auth refactor completed ahead of schedule
+ Zero critical bugs in production
+ Good collaboration on API work

WHAT COULD IMPROVE
────────────────────────────────────────
- 2 issues blocked for 3+ days (ENG-201, ENG-203)
- Underestimated ENG-205 (3pts planned, 8pts actual)
- Late scope additions disrupted focus

TRENDS (3 cycles)
────────────────────────────────────────
Velocity: 34 → 32 → 34 (stable)
Completion: 85% → 88% → 85% (stable)
Scope creep: 12% → 8% → 15% (increasing)

ACTION ITEMS
────────────────────────────────────────
1. Add buffer for complex API work
2. Daily standup check on blockers
3. Scope freeze after day 2
```

## Commands Used

```bash
# Analyze recent cycles
linear cycles analyze --team ENG --count 3

# Get specific cycle details
linear cycles get CYCLE-23

# List cycle issues
linear issues list --team ENG --cycle CYCLE-23

# Check what was blocked
linear deps --team ENG
```

## Discussion Questions

Generate discussion prompts for the team:

1. **Wins**: What should we celebrate?
2. **Blockers**: What slowed us down?
3. **Process**: What would we do differently?
4. **Tools**: Are there tools/automation to add?
5. **Communication**: Where did we lose sync?

## Best Practices

1. **Be data-driven** - Base insights on actual metrics
2. **Focus on process** - Not individual performance
3. **Actionable items** - Every insight should have a follow-up
4. **Track over time** - Compare to previous retros
