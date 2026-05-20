---
name: time-management
description: Manage time effectively - timeboxing, focus, duration estimation, productivity breaks
category: Session Knowledge
---

# Skill: time-management

## What I do

I help manage work sessions effectively through timeboxing, focus techniques, duration estimation, and knowing when to take breaks. I provide duration data to token-cost-estimation for accurate planning.

## When to use me

- When planning work session duration
- When needing to timebox tasks
- When focus is degrading
- When estimating how long tasks will take
- When token-cost-estimation needs duration multipliers

## Core principles

1. **Timebox ruthlessly** - Set time limits, respect them
2. **Focus in blocks** - Deep work needs uninterrupted time
3. **Breaks restore efficiency** - Fatigue increases token usage
4. **Estimate duration explicitly** - Don't drift without awareness
5. **Know when to stop** - Diminishing returns are real

## Duration Estimation

### Task Duration Categories

| Category | Duration | Token Efficiency | Notes |
|----------|----------|------------------|-------|
| **Quick** | <15 min | Highest | Single-focus, no context switch |
| **Short** | 15-30 min | High | Minimal overhead |
| **Medium** | 30-90 min | Moderate | Some iteration expected |
| **Long** | 90-180 min | Lower | Fatigue begins, breaks needed |
| **Extended** | >180 min | Lowest | Multiple breaks required |

### Duration Impact on Tokens

Longer sessions increase token usage due to:
- Context rebuilding after breaks
- Fatigue-induced inefficiency
- Increased iteration cycles
- Re-reading previous work

**Efficiency formula:**
```
Effective tokens = Base tokens × Duration multiplier
Duration multiplier:
  - Short: 1.0x
  - Medium: 1.3x
  - Long: 1.7x
  - Extended: 2.0x+
```

## Timeboxing Patterns

### Sprint Timeboxing
- Set explicit time limit before starting
- At 80% of timebox: assess progress
- At 100%: stop and evaluate, don't extend automatically

## Break Recommendations

| Session Length | Break Frequency | Break Duration |
|----------------|-----------------|----------------|
| <30 min | None needed | - |
| 30-60 min | 1 break | 5 min |
| 60-90 min | 2 breaks | 5 min each |
| 90+ min | Every 25-30 min | 5-10 min |

**Breaks maintain token efficiency** - Fatigued reasoning uses more tokens for same output.

## Anti-patterns to avoid

- ❌ Open-ended sessions without time limits
- ❌ Skipping breaks to "save time" (increases total tokens)
- ❌ Not estimating duration before starting
- ❌ Extending timeboxes repeatedly
- ❌ Ignoring fatigue signals

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Workflow-Orchestration/Time Management.md`

## Related skills

- `token-cost-estimation` - Uses duration for token estimates
- `estimation` - Duration is a form of estimation
- `scope-management` - Scope affects duration
- `task-tracker` - Track time per task
