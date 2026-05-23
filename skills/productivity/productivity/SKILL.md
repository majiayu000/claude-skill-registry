---
name: Productivity System
description: Three-beat daily system with continuous vigilance for ADHD productivity. USE WHEN user mentions morning brief, sitrep, debrief, status, energy, priorities, brain dump, venting, task capture, habits, patterns, or any daily rhythm/accountability request. Also triggers on cron events for morning_brief, vigilance_check, afternoon_brief, pattern_log.
---

# Daily Rhythm System

Three-beat daily system: Morning SITREP → Vigilance → Afternoon DEBRIEF.
All outputs via Telegram. Energy-gated via Oura. Personal tasks via Todoist.

## Architecture

```
MORNING (6am/8am) → Energy check, fires, calendar, priorities
VIGILANCE (15min) → Silent monitoring, interrupt-only alerts  
AFTERNOON (5pm)   → Scorecard, threads, tomorrow prep
```

## Quick Reference

| Trigger | Action |
|---------|--------|
| `sitrep` / `morning brief` | Run morning brief |
| `debrief` / `wrap up` | Run afternoon brief |
| `quiet` / `dnd` | Suppress alerts 2h (fires only) |
| `back` | Resume alerts |
| `status` | Mini status report |

## Brain Dump Classifier

**CRITICAL: Most dumps are NOT tasks. Default = THINKING.**

### Classification Order
1. Explicit command → handle
2. Frustration signals → **VENTING** (log, 5 words max)
3. Health signals → **HEALTH** (log + correlate, 3 lines)
4. Commitment to others → **COMMITMENT** (track with decay, 2 lines)
5. Specific action + work context → **WORK_TASK** (create task, 3 lines)
6. Specific action + personal context → **PERSONAL_TASK** (Todoist, 2 lines)
7. Financial signals → **FINANCIAL** (log + context, 4 lines)
8. Idea signals → **IDEA** (log only, DO NOT engage, 1 line)
9. Observation signals → **OBSERVATION** (pattern engine, 2 sentences)
10. Note signals → **NOTE** (store, 1 line)
11. **DEFAULT → THINKING** (log, 1 sentence + "parking/discuss?")

### Response Caps
| Category | Max Response |
|----------|--------------|
| VENTING | 5 words |
| THINKING | 1 sentence |
| IDEA | 1 line (DO NOT ENGAGE) |
| PERSONAL_TASK | 2 lines |
| WORK_TASK | 3 lines |
| COMMITMENT | 2 lines |

### ADHD Rules
- 5+ dumps in 60 min + 0 completions = **SPIRAL** → intervention
- 4+ topics in 30 min = **SCATTER** → redirect
- Ideas feel urgent but aren't → log, park, move on

## Energy Gating

Check Oura FIRST. Energy determines everything.

| Readiness | Label | Max Priorities |
|-----------|-------|----------------|
| ≥85 | FULL | 3 + stretch |
| 70-84 | MODERATE | 3 |
| 55-69 | LOW | 2 |
| <55 | RECOVERY | 1 (emergency only) |

## Memory Structure

```
memory/
├── habits/log.jsonl        ← Daily habit entries
├── habits/trends.md        ← Weekly summaries
├── patterns/observations.jsonl
├── patterns/insights.md    ← Confirmed patterns
├── commitments/personal.jsonl
├── commitments/work.jsonl
└── daily/YYYY-MM-DD.md
```

## References

- **Morning/Afternoon briefs**: See [references/briefs.md](references/briefs.md)
- **Vigilance alerts**: See [references/vigilance.md](references/vigilance.md)
- **Habit tracking**: See [references/habits.md](references/habits.md)
- **Pattern engine**: See [references/patterns.md](references/patterns.md)
- **Configuration**: See [references/config.md](references/config.md)

## Cron Schedule

```cron
0 6 * * 1-5     morning_brief (workday)
0 8 * * 0,6     weekend_brief
*/15 9-17 * * 1-5  vigilance_check
0 17 * * 1-5    afternoon_brief
0 23 * * *      pattern_log
0 10 * * 0      pattern_analysis (Sunday)
0 9 1 * *       monthly_review
```

## Task Routing

| Type | Destination |
|------|-------------|
| Work tasks | WorkOS or memory |
| Personal tasks | Todoist |
| Commitments | Track in memory with decay |
| Everything else | Memory only — NO task |
