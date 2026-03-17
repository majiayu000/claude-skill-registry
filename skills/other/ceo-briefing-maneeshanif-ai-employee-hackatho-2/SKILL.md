---
name: ceo-briefing
description: Generates executive business briefings, weekly audits, and strategic reports. Use when creating Monday Morning CEO Briefings, business summaries, performance reports, or strategic analysis.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# CEO Briefing Skill

This skill generates comprehensive executive briefings that transform raw business data into actionable intelligence for the Personal AI Employee.

## Briefing Types

| Type | Frequency | Generated | Delivered |
|------|-----------|-----------|-----------|
| Weekly CEO Briefing | Sunday night | 10 PM | Monday 8 AM |
| Monthly Business Review | End of month | Last day | 1st of month |
| Quarterly Strategic Summary | End of quarter | Last week | Q+1 Week 1 |
| Ad-hoc Analysis | On demand | Immediate | Immediate |

## Briefing Structure

```markdown
# [Period] CEO Briefing

## Executive Summary
[2-3 sentence high-level overview]

## Revenue & Financial Health
- This Period: $X,XXX
- Period-to-Date: $X,XXX (XX% of target)
- Trend: [On track | Ahead | Behind]

## Completed Objectives
- [x] [Accomplishment 1]
- [x] [Accomplishment 2]

## Bottlenecks & Risks
| Issue | Impact | Suggested Action |
|-------|--------|------------------|

## Proactive Suggestions
### Cost Optimization
### Growth Opportunities
### Upcoming Deadlines

## Key Metrics Dashboard
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
```

## Data Sources

- `/Accounting/` - Financial data
- `/Tasks/Done/` - Completed work
- `Business_Goals.md` - Targets
- `Dashboard.md` - Current status

## Reference

For detailed templates, see [reference.md](reference.md)

For example briefings, see [examples.md](examples.md)
