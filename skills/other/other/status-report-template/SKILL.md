---
name: status-report-template
description: Эксперт по статус-отчётам. Используй для создания шаблонов отчётов, executive summaries и project dashboards.
---

# Status Report Template Generator

Эксперт по созданию эффективных статус-отчётов для проектной коммуникации на всех уровнях организации.

## Core Principles

### Foundational Requirements

```yaml
effective_status_report:
  principles:
    - name: "Consistent Formatting"
      description: "Use consistent structure and hierarchy across all reports"

    - name: "Audience-Specific"
      description: "Tailor depth and focus to reader's needs"

    - name: "Traffic Light System"
      description: "Green/Yellow/Red for quick visual assessment"

    - name: "Data-Driven"
      description: "Include specific dates, percentages, measurable outcomes"

    - name: "Actionable"
      description: "Clear next steps with ownership and deadlines"

    - name: "Honest"
      description: "Direct communication about issues while maintaining professionalism"
```

### Audience Differentiation

| Audience | Focus | Depth | Frequency |
|----------|-------|-------|-----------|
| **Executive** | Business impact, strategic alignment | High-level metrics | Weekly/Monthly |
| **Team** | Operational details, blockers | Detailed tasks | Daily/Weekly |
| **Client** | Deliverables, timeline | Balanced detail | Weekly |
| **Board** | Strategic metrics, risks | Executive summary | Monthly/Quarterly |
| **Stakeholders** | Relevant updates, decisions needed | Customized | As needed |

---

## Standard Templates

### Executive Summary Template

```markdown
# Project Status Report: [Project Name]
**Report Date:** [Date]
**Reporting Period:** [Start Date] - [End Date]
**Report Author:** [Name]

---

## Executive Summary

### Overall Status: 🟢 GREEN / 🟡 YELLOW / 🔴 RED

| Dimension | Status | Trend |
|-----------|--------|-------|
| Schedule  | 🟢 On Track | ↗️ Improving |
| Budget    | 🟡 At Risk | → Stable |
| Scope     | 🟢 On Track | → Stable |
| Quality   | 🟢 On Track | ↗️ Improving |

### Key Highlights
1. [Major accomplishment with measurable impact]
2. [Important milestone reached]
3. [Significant decision made]

### Attention Required
1. **[Issue]** - [Impact] - Decision needed by [Date]
2. **[Risk]** - [Mitigation status] - Escalation: [Yes/No]

---

## Decisions Needed

| Decision | Owner | Deadline | Impact if Delayed |
|----------|-------|----------|-------------------|
| [Decision description] | [Name] | [Date] | [Impact] |
```

### Progress Tracking Section

```markdown
## Progress Summary

### Completed This Period
| Task | Owner | Completed | Impact |
|------|-------|-----------|--------|
| [Task name] | [Name] | [Date] | [Business impact] |
| [Task name] | [Name] | [Date] | [Business impact] |

### In Progress
| Task | Owner | % Complete | ETA | Status |
|------|-------|------------|-----|--------|
| [Task name] | [Name] | 75% | [Date] | 🟢 On Track |
| [Task name] | [Name] | 40% | [Date] | 🟡 At Risk |

### Upcoming (Next Period)
| Task | Owner | Start Date | Priority |
|------|-------|------------|----------|
| [Task name] | [Name] | [Date] | High |
| [Task name] | [Name] | [Date] | Medium |

### Milestone Tracker
| Milestone | Baseline Date | Current Date | Variance | Status |
|-----------|---------------|--------------|----------|--------|
| Phase 1 Complete | Mar 15 | Mar 15 | 0 days | 🟢 Complete |
| Phase 2 Complete | Apr 30 | May 7 | +7 days | 🟡 At Risk |
| Go Live | Jun 1 | Jun 1 | 0 days | ⬜ Planned |
```

### Risk Management Matrix

```markdown
## Risk & Issue Management

### Active Risks
| ID | Risk Description | Probability | Impact | Score | Mitigation | Owner | Status |
|----|------------------|-------------|--------|-------|------------|-------|--------|
| R01 | [Risk description] | High | High | 🔴 9 | [Mitigation plan] | [Name] | Monitoring |
| R02 | [Risk description] | Medium | High | 🟡 6 | [Mitigation plan] | [Name] | Mitigating |
| R03 | [Risk description] | Low | Medium | 🟢 2 | [Mitigation plan] | [Name] | Accepted |

**Risk Scoring:** Low=1, Medium=2, High=3 | Score = Probability × Impact

### Active Issues
| ID | Issue Description | Severity | Impact | Resolution Plan | Owner | Target Date |
|----|-------------------|----------|--------|-----------------|-------|-------------|
| I01 | [Issue description] | Critical | [Impact] | [Resolution] | [Name] | [Date] |
| I02 | [Issue description] | Major | [Impact] | [Resolution] | [Name] | [Date] |

### Escalations
| Item | Escalated To | Date | Status | Resolution |
|------|--------------|------|--------|------------|
| [Description] | [Name/Committee] | [Date] | Pending | [Update] |
```

### Financial Summary

```markdown
## Financial Summary

### Budget Overview
| Category | Budget | Actual | Variance | % Used |
|----------|--------|--------|----------|--------|
| Labor | $500,000 | $475,000 | $25,000 ↓ | 95% |
| Hardware | $100,000 | $98,000 | $2,000 ↓ | 98% |
| Software | $50,000 | $55,000 | -$5,000 ↑ | 110% |
| Contingency | $50,000 | $10,000 | $40,000 ↓ | 20% |
| **Total** | **$700,000** | **$638,000** | **$62,000** | **91%** |

### Burn Rate Analysis
- **Planned Monthly Burn:** $100,000
- **Actual Monthly Burn:** $95,000
- **Trend:** 5% under budget
- **Projected End Cost:** $665,000 (5% under budget)

### Resource Utilization
| Role | Planned Hours | Actual Hours | Utilization |
|------|---------------|--------------|-------------|
| Developers | 800 | 780 | 97.5% |
| QA | 200 | 220 | 110% |
| PM | 160 | 165 | 103% |
```

---

## Dashboard Templates

### Weekly Team Dashboard

```markdown
# Team Weekly Update: [Team Name]
**Week of:** [Date Range]

## This Week's Focus
🎯 [Primary objective for the week]

## Wins 🏆
- ✅ [Accomplishment 1]
- ✅ [Accomplishment 2]
- ✅ [Accomplishment 3]

## Challenges 🚧
- ⚠️ [Challenge 1] → [Action being taken]
- ⚠️ [Challenge 2] → [Action being taken]

## Team Velocity
| Sprint | Committed | Completed | Velocity |
|--------|-----------|-----------|----------|
| Current | 45 pts | 38 pts | 84% |
| Previous | 40 pts | 42 pts | 105% |
| Average | - | - | 95% |

## Next Week Preview
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Help Needed
- [ ] [Specific request 1] - [From whom]
- [ ] [Specific request 2] - [From whom]
```

### Monthly Executive Dashboard

```markdown
# Executive Dashboard: [Project/Program Name]
**Period:** [Month Year]

## At a Glance

```
┌─────────────────────────────────────────────────────────┐
│  SCHEDULE    BUDGET     SCOPE      QUALITY    TEAM      │
│    🟢          🟡         🟢          🟢        🟢       │
│  On Track   At Risk   On Track   On Track   On Track   │
└─────────────────────────────────────────────────────────┘
```

## OKR Progress

### Objective 1: [Objective Name]
| Key Result | Target | Current | Progress |
|------------|--------|---------|----------|
| KR1: [Description] | 100 | 75 | ████████░░ 75% |
| KR2: [Description] | 50 | 45 | █████████░ 90% |
| KR3: [Description] | 10 | 10 | ██████████ 100% |

### Objective 2: [Objective Name]
| Key Result | Target | Current | Progress |
|------------|--------|---------|----------|
| KR1: [Description] | 500 | 350 | ███████░░░ 70% |

## Strategic Alignment
- **Business Impact:** [Quantified impact on business metrics]
- **Customer Satisfaction:** [NPS or CSAT score change]
- **Revenue Impact:** [Revenue influenced or generated]

## Key Decisions Made
1. [Decision] - [Date] - [Impact]
2. [Decision] - [Date] - [Impact]

## Upcoming Milestones (Next 30 Days)
| Milestone | Date | Dependencies | Confidence |
|-----------|------|--------------|------------|
| [Milestone] | [Date] | [Dependencies] | High |
```

---

## Advanced Techniques

### Trend Analysis Integration

```markdown
## Performance Trends (3-Month Rolling)

### Schedule Performance Index (SPI)
| Month | Planned Value | Earned Value | SPI | Trend |
|-------|---------------|--------------|-----|-------|
| Jan | $100,000 | $95,000 | 0.95 | - |
| Feb | $200,000 | $195,000 | 0.98 | ↗️ |
| Mar | $300,000 | $305,000 | 1.02 | ↗️ |

**Analysis:** Schedule performance improving. Current trajectory suggests on-time delivery.

### Cost Performance Index (CPI)
| Month | Actual Cost | Earned Value | CPI | Trend |
|-------|-------------|--------------|-----|-------|
| Jan | $100,000 | $95,000 | 0.95 | - |
| Feb | $190,000 | $195,000 | 1.03 | ↗️ |
| Mar | $280,000 | $305,000 | 1.09 | ↗️ |

**Analysis:** Cost efficiency improving. Projecting 5% under budget at completion.

### Velocity Trend
```
Velocity (Story Points)
50 │         ╭─────╮
40 │    ╭────╯     ╰────
30 │────╯
   └──────────────────────
     S1  S2  S3  S4  S5  S6
```
```

### Visual Health Dashboard

```markdown
## Project Health Indicators

### Health Matrix
```
                    LOW IMPACT    MED IMPACT    HIGH IMPACT
                   ┌────────────┬────────────┬────────────┐
HIGH PROBABILITY   │    🟡      │    🟠      │    🔴      │
                   ├────────────┼────────────┼────────────┤
MED PROBABILITY    │    🟢      │    🟡      │    🟠      │
                   ├────────────┼────────────┼────────────┤
LOW PROBABILITY    │    🟢      │    🟢      │    🟡      │
                   └────────────┴────────────┴────────────┘
```

### Current Risk Distribution
- 🔴 Critical: 1 (Resource availability)
- 🟠 High: 2 (Integration complexity, Vendor dependency)
- 🟡 Medium: 4
- 🟢 Low: 8

### Quality Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Defect Density | < 0.5/KLOC | 0.3/KLOC | 🟢 |
| Test Coverage | > 80% | 85% | 🟢 |
| Code Review Coverage | 100% | 100% | 🟢 |
| Critical Bugs | 0 | 0 | 🟢 |
```

### Predictive Elements

```markdown
## Predictive Analysis

### Completion Forecast
Based on current velocity and remaining scope:

| Scenario | Completion Date | Confidence |
|----------|-----------------|------------|
| Best Case | May 15 | 20% |
| Most Likely | May 28 | 60% |
| Worst Case | Jun 15 | 20% |

**Factors affecting forecast:**
- ↗️ Positive: Team velocity increasing, key risks mitigated
- ↘️ Negative: Scope additions (+15 points), holiday schedule

### Budget Forecast
| Metric | Value |
|--------|-------|
| Budget at Completion (BAC) | $700,000 |
| Estimate at Completion (EAC) | $665,000 |
| Variance at Completion (VAC) | +$35,000 (5% under) |
| To-Complete Performance Index (TCPI) | 0.95 |

### Scope Creep Indicator
```
Scope Growth Rate
  15% │    ╭──── Warning Zone ────
  10% │────╯
   5% │
   0% │════════════════════════
      Week 1   2   3   4   5   6
```
**Current Rate:** 8% | **Threshold:** 10%
```

---

## Report Types by Context

### Client Status Report

```markdown
# [Project Name] - Client Status Report
**Report #:** [Number]
**Date:** [Date]
**Prepared for:** [Client Name]

## Project Overview
**Overall Status:** 🟢 On Track

We're pleased to report continued progress on [Project Name]. This week, we achieved [key milestone] and remain on track for [upcoming deliverable].

## Deliverable Progress

### Completed Deliverables
| Deliverable | Acceptance Date | Sign-off |
|-------------|-----------------|----------|
| [Deliverable 1] | [Date] | ✅ Approved |
| [Deliverable 2] | [Date] | ✅ Approved |

### In Progress
| Deliverable | Progress | Expected Delivery |
|-------------|----------|-------------------|
| [Deliverable 3] | 75% | [Date] |
| [Deliverable 4] | 40% | [Date] |

## Timeline Update
[Visual timeline or Gantt chart summary]

## Items Requiring Your Input
1. **[Decision Item]**
   - Context: [Brief context]
   - Options: [A, B, C]
   - Recommendation: [Our recommendation]
   - Needed by: [Date]

## Next Steps
- [Action 1] - [Date]
- [Action 2] - [Date]

## Meeting Schedule
- Next Status Call: [Date/Time]
- Demo Session: [Date/Time]
```

### Steering Committee Report

```markdown
# Steering Committee Report
**Program:** [Program Name]
**Meeting Date:** [Date]
**Prepared by:** [PMO]

## Executive Summary
[2-3 sentence summary of overall program health]

## Program Dashboard

### Portfolio Status
| Project | Status | Budget | Schedule | Key Issue |
|---------|--------|--------|----------|-----------|
| Project A | 🟢 | 🟢 | 🟢 | None |
| Project B | 🟡 | 🟢 | 🟡 | Resource constraint |
| Project C | 🔴 | 🔴 | 🟡 | Vendor delay |

### Resource Allocation
| Resource Pool | Allocated | Available | Utilization |
|---------------|-----------|-----------|-------------|
| Development | 45 | 50 | 90% |
| QA | 12 | 15 | 80% |
| Infrastructure | 8 | 10 | 80% |

## Decisions Required

### Decision 1: [Title]
- **Background:** [Context]
- **Options:**
  - Option A: [Description] - Cost: $X, Risk: Low
  - Option B: [Description] - Cost: $Y, Risk: Medium
- **Recommendation:** Option A
- **Impact of No Decision:** [Consequences]

## Strategic Risks
| Risk | Impact | Mitigation | Owner |
|------|--------|------------|-------|
| [Risk 1] | [Impact] | [Action] | [Name] |

## Financial Summary
- **YTD Spend:** $X of $Y budget (X%)
- **Forecast:** On/Under/Over budget by X%
```

---

## Best Practices

### Do's ✅

```yaml
best_practices:
  timing:
    - "Send reports consistently (same day/time each period)"
    - "Allow 24 hours for review before meetings"
    - "Distribute before, not during, status meetings"

  content:
    - "Lead with executive summary"
    - "Use data and metrics, not just descriptions"
    - "Include both wins and challenges"
    - "Provide clear action items with owners and dates"
    - "Quantify everything possible"

  formatting:
    - "Use consistent templates across projects"
    - "Apply traffic light colors sparingly and consistently"
    - "Include visual elements for quick scanning"
    - "Keep executive summary to one page"

  distribution:
    - "Create audience-specific versions"
    - "Archive for historical analysis"
    - "Make searchable and accessible"
```

### Don'ts ❌

```yaml
common_mistakes:
  - mistake: "Burying critical issues"
    impact: "Stakeholders blindsided by problems"
    fix: "Lead with issues requiring attention"

  - mistake: "Activity reporting vs outcome reporting"
    impact: "No clarity on actual progress"
    fix: "Focus on completed deliverables and business impact"

  - mistake: "Vague language"
    impact: "Ambiguity and miscommunication"
    fix: "Use specific numbers, dates, percentages"

  - mistake: "Missing action items"
    impact: "No accountability or follow-through"
    fix: "Every issue needs owner and deadline"

  - mistake: "Over-optimistic assessment"
    impact: "Lost trust when reality emerges"
    fix: "Honest assessment with mitigation plans"

  - mistake: "Too much detail for executives"
    impact: "Key points lost in noise"
    fix: "Executive summary + detailed appendix"
```

---

## Automation Integration

### JIRA Integration Query

```sql
-- Sprint progress query for status report
SELECT
    sprint_name,
    COUNT(CASE WHEN status = 'Done' THEN 1 END) as completed,
    COUNT(CASE WHEN status = 'In Progress' THEN 1 END) as in_progress,
    COUNT(CASE WHEN status = 'To Do' THEN 1 END) as todo,
    SUM(CASE WHEN status = 'Done' THEN story_points ELSE 0 END) as completed_points,
    SUM(story_points) as total_points,
    ROUND(SUM(CASE WHEN status = 'Done' THEN story_points ELSE 0 END) * 100.0 /
          NULLIF(SUM(story_points), 0), 1) as completion_percentage
FROM issues
WHERE sprint_id = :current_sprint
GROUP BY sprint_name;
```

### Slack Status Bot Template

```javascript
// Automated status collection bot
const statusPrompt = {
  blocks: [
    {
      type: "section",
      text: {
        type: "mrkdwn",
        text: "*Weekly Status Update*\nPlease provide your status for the week:"
      }
    },
    {
      type: "input",
      element: {
        type: "plain_text_input",
        action_id: "accomplishments",
        multiline: true,
        placeholder: { type: "plain_text", text: "What did you accomplish?" }
      },
      label: { type: "plain_text", text: "Accomplishments" }
    },
    {
      type: "input",
      element: {
        type: "plain_text_input",
        action_id: "blockers",
        multiline: true,
        placeholder: { type: "plain_text", text: "Any blockers or challenges?" }
      },
      label: { type: "plain_text", text: "Blockers" }
    },
    {
      type: "input",
      element: {
        type: "plain_text_input",
        action_id: "next_week",
        multiline: true,
        placeholder: { type: "plain_text", text: "What's planned for next week?" }
      },
      label: { type: "plain_text", text: "Next Week's Focus" }
    }
  ]
};
```

---

## Лучшие практики

1. **Консистентность важнее красоты** — используй один и тот же шаблон
2. **Executive summary всегда первым** — руководители читают только его
3. **Честность в оценках** — лучше предупредить о рисках заранее
4. **Конкретика вместо общих фраз** — "завершено 75%" вместо "почти готово"
5. **Action items с владельцами** — каждый риск и issue должен иметь ответственного
6. **Архивируй отчёты** — они нужны для post-mortem и планирования
7. **Адаптируй под аудиторию** — разная глубина для разных читателей
