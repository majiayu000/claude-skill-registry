---
name: cycle-plan
description: Plan Linear cycles using velocity analytics. Suggests scope based on historical capacity, identifies dependency risks, balances workload.
---

# Cycle Plan Skill - Sprint Planning

You are an expert at planning software development cycles based on team velocity.

## When to Use

Use this skill when:
- Planning the next sprint/cycle
- Deciding what to include in a cycle
- Balancing workload across team members

## Process

1. **Analyze Historical Velocity**
   ```bash
   linear cycles analyze --team ENG --count 5
   ```

2. **Review Available Capacity**
   - Check team size
   - Account for PTO/holidays
   - Consider focus time needs

3. **Select Issues for Cycle**
   - Start with P1/P2 issues
   - Respect dependencies
   - Balance across team members

4. **Validate Plan**
   - Total estimates <= capacity
   - No cross-cycle blockers
   - Even distribution

## Velocity Analysis

The `linear cycles analyze` command provides:

```
VELOCITY ANALYSIS: Team ENG (5 cycles)
════════════════════════════════════════
Average Velocity: 34 points/cycle
Completion Rate: 85%
Scope Creep: 12%

CYCLE HISTORY
────────────────────────────────────────
Cycle 23: 38 pts (92% complete)
Cycle 22: 32 pts (88% complete)
Cycle 21: 35 pts (82% complete)
Cycle 20: 28 pts (78% complete)
Cycle 19: 37 pts (90% complete)

RECOMMENDATION
────────────────────────────────────────
Target: 32-36 points for next cycle
Buffer: Reserve 10% for unplanned work
```

## Planning Output

```
CYCLE PLAN: Sprint 24
════════════════════════════════════════
Capacity: 40 points (4 engineers)
Target: 36 points (90% capacity)
Buffer: 4 points for unplanned work

PLANNED ISSUES
────────────────────────────────────────
ENG-201 [P1] Auth refactor      8pts @alice
ENG-202 [P1] Payment fix        5pts @bob
ENG-203 [P2] Dashboard update   8pts @carol
ENG-204 [P2] API optimization   5pts @dave
ENG-205 [P3] Docs update        3pts @alice
ENG-206 [P3] Test coverage      5pts @bob
────────────────────────────────────────
Total: 34 points

WORKLOAD BALANCE
────────────────────────────────────────
@alice: 11 pts (28%)
@bob:   10 pts (25%)
@carol: 8 pts (20%)
@dave:  5 pts (13%)
Unassigned: 0 pts

DEPENDENCY RISKS
────────────────────────────────────────
ENG-203 blocked by ENG-201 (same cycle - OK)
```

## Commands Used

```bash
# Analyze velocity
linear cycles analyze --team ENG --count 5

# List upcoming issues
linear issues list --team ENG

# Check dependencies
linear deps --team ENG

# Assign to cycle
linear issues update ENG-201 --cycle current
linear issues update ENG-202 --cycle next
```

## Best Practices

1. **Leave buffer** - Plan to 80-90% capacity
2. **Front-load blockers** - Schedule blocking issues early
3. **Balance workload** - Distribute evenly across team
4. **Avoid cross-cycle deps** - Don't plan work blocked by next cycle
