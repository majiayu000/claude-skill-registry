---
name: today
description: Interactive daily productivity review with guided priority setting. Supports morning planning, midday check-ins, and end-of-day wrap-ups. Use for daily ritual or cron automation.
version: 1.1.0
category: productivity
last_updated: 2026-01-21
related_skills:
  - context-management
  - planning
---

# Today - Daily Productivity Skill

## Overview

A daily ritual skill that reviews your workspace activity, summarizes progress, identifies blockers, and suggests focus items for sustained productivity. Features **interactive review mode** that guides you through priority setting and progress tracking.

## Quick Start

```bash
# Interactive review (auto-detects morning/midday/evening)
/today

# Specific modes
/today morning    # Full review + set priorities
/today midday     # Quick progress check
/today --eod      # End-of-day wrap-up

# Weekly review
/today --week

# Cron automation (runs at 6 AM)
0 6 * * * /path/to/workspace-hub/scripts/productivity/daily_today.sh
```

## Interactive Modes

| Mode | When | Duration | What It Does |
|------|------|----------|--------------|
| **Morning** | Before noon | 5 min | Full review, set 3 priorities |
| **Midday** | Noon-5pm | 2 min | Progress check, log blockers |
| **Evening** | After 5pm / `--eod` | 3 min | Wrap-up, capture tomorrow's focus |

### Morning Flow
1. Review yesterday's git activity
2. See open TODOs and in-progress work
3. **Interactive:** Choose your top 3 priorities
4. Optional: Block focus time

### Midday Flow
1. Quick status on priority #1
2. Log any blockers
3. Adjust priorities if needed

### Evening Flow
1. Mark priorities as done/partial/blocked
2. Capture blockers for tomorrow
3. Set tomorrow's starting focus

## When to Use

- Start of workday ritual
- After returning from break/vacation
- Weekly planning sessions
- Automated daily reports via cron
- Before standup meetings

## Instructions

### Daily Review Process

Execute these steps in order:

#### 1. Gather Context (Automated)

Collect data from these sources:

| Source | What to Extract |
|--------|-----------------|
| Git logs | Commits from last 24h across all repos |
| TODO files | Open items in `TODO.md`, `TASKS.md` |
| Specs | In-progress specs in `specs/modules/` |
| Calendar | Today's meetings (if integrated) |
| Notes | Recent entries in daily notes |

#### 2. Generate Daily Summary

```markdown
## Daily Summary - {DATE}

### Completed Yesterday
- [ ] List completed tasks from git commits
- [ ] Closed issues/PRs

### In Progress
- [ ] Active branches/PRs
- [ ] Open specs/plans

### Blocked/Waiting
- [ ] Items awaiting input
- [ ] Dependency blockers

### Today's Focus (Recommended)
1. **High Priority:** [Most impactful task]
2. **Quick Wins:** [Tasks completable in <30min]
3. **Deep Work:** [Requires focus time]
```

#### 3. Long-Term Productivity Suggestions

Analyze patterns and suggest improvements:

| Pattern | Suggestion |
|---------|------------|
| Many small commits | Consider batching related changes |
| Stale branches | Clean up or merge abandoned work |
| Repeated context switches | Block focus time for deep work |
| No tests in commits | Add TDD to workflow |
| Large uncommitted changes | Commit more frequently |

#### 4. Create Daily Log Entry

Save to `logs/daily/{YYYY-MM-DD}.md`:

```markdown
---
date: {YYYY-MM-DD}
generated: auto
reviewed: false
---

# Daily Log - {DATE}

## Summary
[Auto-generated summary]

## Priorities
1.
2.
3.

## Notes
[Space for manual notes]

## End of Day Review
- [ ] Completed priorities
- [ ] Blockers encountered
- [ ] Tomorrow's focus
```

### Data Sources Configuration

Configure in `.claude/config/today.yaml`:

```yaml
today:
  sources:
    git:
      enabled: true
      lookback_hours: 24
      repos:
        - .  # Current repo
        - ../related-project

    files:
      todo_patterns:
        - "**/TODO.md"
        - "**/TASKS.md"
        - "**/.todo"

      notes_dir: "logs/daily"

    calendar:
      enabled: false  # Requires calendar integration

  output:
    daily_log_dir: "logs/daily"
    summary_format: "markdown"

  automation:
    cron_enabled: true
    notify_on_complete: false
```

## Cron Setup

### Installation

```bash
# Make script executable
chmod +x scripts/productivity/daily_today.sh

# Add to crontab (runs at 6 AM daily)
crontab -e
# Add line:
0 6 * * * /path/to/workspace-hub/scripts/productivity/daily_today.sh >> /tmp/daily_today.log 2>&1
```

### Cron Script Features

- Generates daily summary without interactive Claude
- Creates log file in `logs/daily/`
- Can trigger notifications (configurable)
- Supports multiple workspace roots

## Examples

### Morning Ritual

```
User: /today

Claude: ## Daily Summary - 2026-01-21

### Completed Yesterday
- Merged PR #42: Add user authentication
- Fixed 3 bugs in payment module
- Updated API documentation

### In Progress
- Feature: Dashboard analytics (branch: feature/analytics)
- Spec: Mobile app redesign (specs/modules/mobile-v2/)

### Blocked
- Waiting: Design review for mobile spec
- Dependency: Backend team to deploy auth service

### Today's Focus (Recommended)
1. **High Priority:** Complete analytics dashboard tests
2. **Quick Wins:** Review open PRs (2 waiting)
3. **Deep Work:** Start mobile navigation implementation

### Long-Term Suggestions
- Consider: 15 context switches yesterday - block 2h focus time
- Action: Stale branch `feature/old-feature` (30 days) - archive or delete
```

### Weekly Planning

```
User: /today --week

Claude: ## Weekly Summary - Week of 2026-01-20

### Accomplishments
- 23 commits across 4 repositories
- 5 PRs merged, 2 pending
- 2 specs completed

### Patterns Observed
- Most productive: Tuesday (8 commits)
- Most meetings: Wednesday (4 hours)
- Suggestion: Protect Tuesday mornings for deep work

### Next Week Focus
1. Complete mobile spec review
2. Ship analytics v1
3. Technical debt: Refactor auth module
```

## Best Practices

### Do

1. Run `/today` at consistent time each morning
2. Review and adjust auto-generated priorities
3. Update end-of-day notes before closing
4. Use cron for consistent data collection
5. Archive old daily logs monthly

### Don't

1. Skip the review - consistency builds habits
2. Overload daily priorities (max 3-5 items)
3. Ignore long-term suggestions repeatedly
4. Let daily logs accumulate without review

## Error Handling

| Situation | Action |
|-----------|--------|
| No git activity | Note "No commits" - suggest catching up |
| Missing config | Use defaults, create template config |
| Calendar unavailable | Skip calendar section, note in summary |
| Cron fails | Check log at `/tmp/daily_today.log` |

## Metrics

Track these for productivity insights:

| Metric | Target | Description |
|--------|--------|-------------|
| Daily completion rate | >70% | Priorities marked done |
| Focus time | >4h/day | Uninterrupted work blocks |
| Context switches | <10/day | Task transitions |
| Commit frequency | 3-8/day | Healthy progress indicators |

## Output Locations

| Output | Location |
|--------|----------|
| Daily logs | `logs/daily/{YYYY-MM-DD}.md` |
| Weekly summaries | `logs/weekly/{YYYY-WW}.md` |
| Cron output | `/tmp/daily_today.log` |
| Config | `.claude/config/today.yaml` |

## Related Skills

- [context-management](../../context-management/SKILL.md) - Manage context efficiently
- [planning](../../development/planning/SKILL.md) - Detailed planning methodology

---

## Version History

- **1.1.0** (2026-01-21): Add interactive review mode with morning/midday/evening flows
- **1.0.0** (2026-01-21): Initial release with daily review, cron support, long-term suggestions
