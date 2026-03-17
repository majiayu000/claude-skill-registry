---
name: stats-tracker
description: Track Claude Code usage statistics and skill effectiveness for CircleTel. Monitor productivity, model usage, streaks, and skill performance metrics.
version: 2.0.0
dependencies: error-registry, compound-learnings
---

# Stats Tracker

Skill for tracking Claude Code usage statistics AND **skill effectiveness** (RSI metrics).

## When to Use

This skill activates when you:
- Want to see your usage statistics
- Track productivity over time
- Analyze model usage patterns
- Monitor usage streaks
- Plan based on usage limits
- **NEW**: Review skill effectiveness metrics
- **NEW**: Generate weekly effectiveness reports

**Keywords**: stats, usage, analytics, productivity, streak, model usage, tokens, sessions, cost, skill effectiveness, skill metrics

## Quick Commands

| Command | Description |
|---------|-------------|
| `/stats` | View usage stats, streak, favorite model |
| `/stats skills` | **NEW**: View skill effectiveness dashboard |
| `/stats skills [name]` | **NEW**: Deep-dive on specific skill |
| `/usage` | View token usage and limits |
| `/context` | View current context usage |
| `/cost` | View session cost breakdown |

## Understanding /stats Output

```
/stats

📊 Your Claude Code Stats
────────────────────────────
🏆 Favorite Model: Sonnet 4 (78% of sessions)
🔥 Current Streak: 12 days
📈 This Week: 847K tokens across 23 sessions
📉 Usage Graph: [▁▃▅▇█▆▄▂] (last 7 days)
```

### Metrics Explained

| Metric | Description |
|--------|-------------|
| Favorite Model | Most frequently used model |
| Current Streak | Consecutive days using Claude Code |
| This Week | Total tokens and sessions |
| Usage Graph | Visual of daily usage pattern |

## Understanding /usage Output

```
/usage

📊 Usage This Period
────────────────────────────
Sonnet: ████████░░ 78%
Opus:   ██░░░░░░░░ 15%
Haiku:  █░░░░░░░░░ 7%

Resets: Monday 00:00 UTC
```

## Model Selection Guide

Choose the right model for the task:

| Task Type | Model | Why |
|-----------|-------|-----|
| General coding | Sonnet | Best balance of speed/quality |
| Complex architecture | Opus | Deep reasoning, long context |
| Quick fixes | Haiku | Fast, efficient |
| Code exploration | Haiku (Explore) | Optimized for search |
| Documentation | Sonnet | Good writing quality |
| Bug investigation | Sonnet/Opus | Depends on complexity |

### Cost Efficiency

| Model | Relative Cost | Best For |
|-------|---------------|----------|
| Haiku | $ | Quick tasks, exploration |
| Sonnet | $$ | Most development work |
| Opus | $$$ | Complex problems |

## Daily Workflow with Stats

### Morning Routine
```
1. /stats                 # Check streak, plan day
2. /usage                 # Check remaining budget
3. /rename feature-x      # Name today's session
4. Start coding           # Use appropriate model
```

### During Development
```
# After complex task
/context                  # Check context usage

# When switching tasks
/stats                    # Quick progress check
```

### End of Day
```
/stats                    # Review productivity
/usage                    # Check usage remaining
/cost                     # See session cost
```

## Usage Optimization Strategies

### If Usage is High

1. **Use Haiku more** - For exploration and quick tasks
2. **Spawn Explore agents** - Uses efficient Haiku model
3. **Background tasks** - Don't consume extra tokens
4. **Be more targeted** - Specific queries use less context

### If Starting Fresh Week

1. **Plan major tasks** - Allocate Opus for complex work
2. **Default to Sonnet** - Best general-purpose model
3. **Reserve Haiku** - For quick lookups and exploration

### Maximizing Efficiency

```
# Good: Specific query
"Fix the null check on line 45 of auth.ts"

# Bad: Vague query (uses more context/tokens)
"Help me with the auth system"
```

## Tracking by Feature

Use named sessions to track usage per feature:

```bash
# Start feature work
/rename billing-feature

# Work on feature...

# Check stats
/stats  # See usage for this session

# Compare features
"How many tokens did billing vs auth use?"
```

## Weekly Review Pattern

Every Friday:
```
1. /stats              # Review week's usage
2. /usage              # Check budget status
3. Note completions    # What features finished?
4. Plan next week      # Allocate model usage
```

### Weekly Goals Template
```
Week Goals:
- [ ] Maintain 5-day streak
- [ ] Complete 3 features
- [ ] Use Opus only for architecture decisions
- [ ] Try Explore agent for research tasks
- [ ] Stay under 80% usage
```

## Integration with Other Skills

### With Session Manager
```
# Track stats per named session
/rename billing-feature
[work on feature]
/stats
# See usage specific to this session
```

### With Context Manager
```
# Monitor both context and usage
/context  # Current context budget
/stats    # Overall usage patterns
```

### With Async Runner
```
# Background tasks don't inflate usage
"Run build in background"
# Build output doesn't use tokens
```

## Gamification Ideas

### Streak Challenges
- 5-day streak: Bronze
- 10-day streak: Silver
- 30-day streak: Gold
- Try to never break your streak!

### Model Efficiency Challenge
```
Challenge: Complete task with Haiku
1. Try Haiku first for any task
2. Escalate to Sonnet only if needed
3. Use Opus sparingly for max impact
```

### Weekly Competition (Team)
- Compare completed features
- Compare usage efficiency
- Share tips for optimization

## External Tools

### ccusage (CLI Analytics)
```bash
# Install
npm install -g ccusage

# View usage
ccusage

# Daily breakdown
ccusage --daily

# Monthly view
ccusage --monthly
```

### Claude Code Usage Monitor
Real-time terminal monitoring with:
- Token tracking
- Burn rate analysis
- Predictions for limits

## CircleTel Productivity Patterns

### Feature Development Session
```
Start: /rename feature-customer-billing
       /stats  # Baseline

Middle: [coding work]
        /context  # Check context

End: /stats  # Compare to baseline
     /cost   # Session cost
```

### Bug Fix Session
```
/rename BUG-1234-fix
/stats  # Note starting point

[investigation and fix]

/stats  # See investigation cost
# Typically: Sonnet for analysis, quick fixes
```

### Architecture Planning
```
/rename architecture-review

# Use Opus for deep thinking
"Think about the best approach for..."

/stats  # Higher usage expected
/cost   # Worth it for good architecture
```

---

## Skill Effectiveness Tracking (RSI Metrics)

**NEW in v2.0**: Track which skills perform best and feed insights back for improvement.

### Command: `/stats skills`

```
/stats skills

═══════════════════════════════════════════════════════════════
  SKILL EFFECTIVENESS DASHBOARD - February 2026
═══════════════════════════════════════════════════════════════

MOST EFFECTIVE (by success rate)      │ NEEDS IMPROVEMENT
──────────────────────────────────────┼────────────────────────────
1. database-migration      95% ✓      │ 1. coverage-check      70% ⚠
2. bug-fixing              89% ✓      │ 2. refactor            75% ⚠
3. compound-learnings      87% ✓      │
                                      │
MOST USED (activations)               │ UNDERUTILIZED
──────────────────────────────────────┼────────────────────────────
1. bug-fixing              47 times   │ 1. mobile-testing       2 times
2. context-manager         35 times   │ 2. deployment-check     3 times
3. stats-tracker           28 times   │

INSIGHT: bug-fixing success rate improved 12% after adding
        error-registry integration last week.

RECOMMENDATION: Consider promoting mobile-testing skill
               (high success rate, low activation).
═══════════════════════════════════════════════════════════════
```

### Metrics Tracked Per Skill

| Metric | Description | How Measured |
|--------|-------------|--------------|
| Activation Count | Times skill triggered | Keyword detection |
| Success Rate | Completed without correction | No follow-up corrections |
| Resolution Time | From activation to completion | Session timestamps |
| Correction Rate | How often skill was corrected | Links to compound-learnings |
| Pattern Contribution | New patterns generated | Links to learnings/ |

### Deep-Dive: `/stats skills [name]`

```
/stats skills bug-fixing

═══════════════════════════════════════════════════════════════
  SKILL DEEP-DIVE: bug-fixing
═══════════════════════════════════════════════════════════════
Version: 1.1.0
Dependencies: error-registry

METRICS (February 2026)
────────────────────────────────────────────────────────────────
Activations:        47
Success Rate:       89%
Avg Resolution:     23 min
Corrections:        7 (15%)
Patterns Created:   3

PHASE BREAKDOWN
────────────────────────────────────────────────────────────────
Phase 0 (Registry):   Avg 2min  │ Skip rate: 20%
Phase 1 (Understand): Avg 5min  │ Skip rate: 10%
Phase 2 (Investigate): Avg 10min │ Skip rate: 5%
Phase 3 (Fix):        Avg 5min  │ Success: 95%
Phase 4 (Validate):   Avg 3min  │ Skip rate: 30%

TREND
────────────────────────────────────────────────────────────────
Success rate: ↑ 12% since error-registry integration
Registry hits: 40% of bugs found in known patterns

RECENT CORRECTIONS (to improve)
────────────────────────────────────────────────────────────────
- 2026-02-10: Missed RLS policy check
- 2026-02-08: Used wrong column name
═══════════════════════════════════════════════════════════════
```

### Data Storage

Skill metrics are stored in:
```
.claude/skills/stats-tracker/
├── metrics.json           # Current period metrics
└── reports/
    └── weekly-YYYY-WW.md  # Weekly reports
```

### Weekly Report Generation

Every Monday, generate a skill effectiveness report:

```markdown
# Skill Effectiveness Report - Week 7, 2026

## Summary
- Total skill activations: 142
- Average success rate: 85%
- Most improved: bug-fixing (+12%)
- Needs attention: coverage-check (70%)

## RSI Loop Impact
- Error registry hits: 40% (saving ~10min per known bug)
- Corrections captured: 5
- Rules extracted: 2
- Patterns created: 3

## Recommendations
1. Add more MTN API patterns to error-registry
2. Update coverage-check with fallback providers
3. Promote mobile-testing (underutilized, high success)
```

### Integration with RSI Skills

```
┌─────────────────────────────────────────────────────────────────┐
│                    RSI METRICS FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SKILL ACTIVATION ──► TRACK METRICS ──► WEEKLY ANALYSIS         │
│         │                                      │                 │
│         │                                      ▼                 │
│         │                            GENERATE INSIGHTS           │
│         │                                      │                 │
│         │              ┌───────────────────────┴───────┐         │
│         │              │                               │         │
│         ▼              ▼                               ▼         │
│  CORRECTION? ──► compound-learnings            SKILL UPDATE      │
│                        │                               │         │
│                        ▼                               │         │
│                 error-registry ◄───────────────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Best Practices

1. **Check stats daily** - Start with `/stats`
2. **Match model to task** - Don't use Opus for simple fixes
3. **Track by feature** - Use named sessions
4. **Review weekly** - Adjust workflow based on patterns
5. **Use Haiku for exploration** - Spawn Explore agents
6. **Background for builds** - Don't waste tokens on output
7. **Targeted queries** - Specific questions = efficient usage
8. **NEW**: Review `/stats skills` weekly for improvement opportunities

## Troubleshooting

### Stats seem wrong
```
# Check current session specifically
/cost

# Check usage for period
/usage
```

### High usage unexpectedly
- Check for large file reads
- Review if background tasks are actually background
- Consider if queries could be more specific

### Streak reset
- Streak requires at least one interaction per day
- Even `/stats` counts
- Check timezone (UTC-based)

---

**Version**: 2.0.0
**Last Updated**: 2026-02-12
**For**: Claude Code v2.0.64+
**RSI Integration**: error-registry, compound-learnings
