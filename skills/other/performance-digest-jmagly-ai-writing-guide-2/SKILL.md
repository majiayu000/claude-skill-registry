# performance-digest

Generate executive-ready performance summaries with insights and recommendations.

## Triggers

- "performance summary"
- "marketing report"
- "how are we doing"
- "executive summary"
- "campaign results"
- "KPI update"

## Purpose

This skill generates clear, actionable performance summaries by:
- Aggregating metrics across all marketing channels
- Highlighting key wins and areas of concern
- Providing context through comparisons and trends
- Translating data into strategic insights
- Delivering recommendations with priority

## Behavior

When triggered, this skill:

1. **Determines report scope**:
   - Time period (daily, weekly, monthly, quarterly)
   - Audience level (team, manager, executive)
   - Focus area (overall, channel, campaign)

2. **Aggregates metrics**:
   - Pull data from data-pipeline
   - Calculate period-over-period changes
   - Compare against targets

3. **Identifies highlights**:
   - Top performers
   - Underperformers
   - Anomalies and outliers
   - Trend shifts

4. **Generates insights**:
   - Why metrics moved
   - What it means for business
   - What action to take

5. **Formats for audience**:
   - Executive: High-level, strategic
   - Manager: Tactical, actionable
   - Team: Detailed, operational

## Report Types

### Daily Digest

```yaml
daily_digest:
  audience: marketing_team
  time: 9:00 AM
  length: 2 minutes read

  sections:
    - yesterday_snapshot
    - notable_changes
    - today_priorities
    - quick_wins

  metrics:
    - spend_vs_budget
    - conversions
    - anomalies
```

### Weekly Summary

```yaml
weekly_summary:
  audience: marketing_manager
  time: Monday 8:00 AM
  length: 5 minutes read

  sections:
    - week_performance
    - channel_breakdown
    - campaign_highlights
    - next_week_focus

  metrics:
    - all_core_kpis
    - week_over_week
    - trend_analysis
```

### Monthly Report

```yaml
monthly_report:
  audience: marketing_leadership
  time: 1st of month
  length: 10 minutes read

  sections:
    - executive_summary
    - goal_progress
    - channel_performance
    - campaign_analysis
    - competitive_context
    - recommendations

  metrics:
    - all_kpis
    - month_over_month
    - year_over_year
    - target_vs_actual
```

### Quarterly Review

```yaml
quarterly_review:
  audience: c_suite
  time: End of quarter
  length: 15 minutes read

  sections:
    - quarter_highlights
    - business_impact
    - market_position
    - strategic_progress
    - next_quarter_plan
    - investment_request

  metrics:
    - revenue_impact
    - market_share
    - brand_metrics
    - efficiency_ratios
```

## Report Templates

### Executive Summary Template

```markdown
# Marketing Performance Summary

**Period**: [Date Range]
**Prepared For**: [Audience]
**Prepared By**: performance-digest skill

---

## At a Glance

| KPI | Actual | Target | Status |
|-----|--------|--------|--------|
| Revenue | $X | $Y | ✅ 110% |
| New Customers | X | Y | ⚠️ 95% |
| CAC | $X | $Y | ✅ -8% |
| ROAS | X.Xx | Y.Yx | ❌ 85% |

**Overall Status**: On Track / At Risk / Behind

---

## Key Wins 🎯

1. **[Win Title]**
   - Result: [Metric achieved]
   - Impact: [Business impact]
   - Credit: [Team/campaign]

2. **[Win Title]**
   - Result: [Metric achieved]
   - Impact: [Business impact]

---

## Areas of Concern ⚠️

1. **[Issue Title]**
   - Current: [Metric]
   - Target: [Target]
   - Gap: [X%]
   - Action: [Recommendation]

---

## Channel Performance

| Channel | Spend | Revenue | ROAS | vs Target |
|---------|-------|---------|------|-----------|
| Paid Search | $X | $Y | Z.Zx | ✅ +12% |
| Paid Social | $X | $Y | Z.Zx | ⚠️ -5% |
| Email | $X | $Y | Z.Zx | ✅ +25% |
| Organic | $0 | $Y | - | ✅ +8% |

---

## Top Campaigns

| Rank | Campaign | Revenue | ROAS | Notes |
|------|----------|---------|------|-------|
| 1 | [Name] | $X | Z.Zx | [Insight] |
| 2 | [Name] | $X | Z.Zx | [Insight] |
| 3 | [Name] | $X | Z.Zx | [Insight] |

---

## Trends

### Positive Trends ↑
- [Trend 1]: [X% improvement over Y period]
- [Trend 2]: [X% improvement over Y period]

### Concerning Trends ↓
- [Trend 1]: [X% decline over Y period]
- [Trend 2]: [X% decline over Y period]

---

## Recommendations

### Immediate Actions (This Week)
1. [ ] [Action] - Expected impact: [X%]
2. [ ] [Action] - Expected impact: [X%]

### Strategic Recommendations (This Quarter)
1. [ ] [Recommendation] - Investment: $X, ROI: Y%
2. [ ] [Recommendation] - Investment: $X, ROI: Y%

---

## Next Period Outlook

- **Target**: [Key goal]
- **Focus**: [Priority areas]
- **Risks**: [Key risks to monitor]
- **Opportunities**: [Growth opportunities]
```

### Daily Digest Template

```markdown
# Daily Marketing Digest

**Date**: 2025-12-08
**Prepared**: 9:00 AM

---

## Yesterday's Snapshot

| Metric | Yesterday | Avg (7d) | Status |
|--------|-----------|----------|--------|
| Spend | $4,523 | $4,200 | +8% |
| Impressions | 245K | 220K | +11% |
| Clicks | 3,421 | 3,100 | +10% |
| Conversions | 87 | 75 | +16% |

**Overall**: Strong day, above average on all metrics

---

## Notable Changes

### ✅ Wins
- Email campaign "Holiday Sale" hit 32% open rate (vs 24% avg)
- LinkedIn ads CPC dropped 15% with new creative

### ⚠️ Watch
- Google Ads CTR down 8% - reviewing ad copy
- Instagram reach declined for 3rd day

### 🚨 Action Needed
- Facebook ad account approaching spending limit
- [Action: Increase daily budget]

---

## Today's Priorities

1. [ ] Review and approve new ad creative for launch
2. [ ] Increase FB budget to avoid delivery issues
3. [ ] Prep weekly report for 10am team meeting

---

## Quick Stats

```
Budget Pacing: ████████████████░░░░ 78% spent, 80% of month
Conversion Goal: ████████████████░░░░ 82% achieved
```
```

## Insight Generation

### Performance Insights

```yaml
insight_types:
  win:
    template: "[Metric] exceeded target by [X%] driven by [cause]"
    example: "Email revenue exceeded target by 25% driven by holiday campaign"

  concern:
    template: "[Metric] fell [X%] below target due to [cause], recommend [action]"
    example: "CAC rose 15% above target due to increased competition, recommend testing new channels"

  trend:
    template: "[Metric] has [increased/decreased] [X%] over [period], indicating [interpretation]"
    example: "Organic traffic has increased 12% over 3 months, indicating SEO investments paying off"

  anomaly:
    template: "[Metric] showed unusual [spike/drop] of [X%] on [date], likely due to [cause]"
    example: "Conversions showed unusual spike of 200% on Friday, likely due to influencer mention"
```

### Context Additions

```yaml
context_types:
  comparison:
    - vs_target: "Target: $X, Actual: $Y (Z%)"
    - vs_prior_period: "vs Last Week: +X%"
    - vs_prior_year: "vs Last Year: +X%"
    - vs_industry: "Industry Avg: X%, Our Performance: Y%"

  benchmark:
    - channel_benchmark: "Email avg open rate: 21%, Ours: 28%"
    - competitor_context: "While competitors pulled back spend, we maintained"

  explanation:
    - why_up: "Driven by [factor1], [factor2]"
    - why_down: "Impacted by [factor1], [factor2]"
    - external_factor: "Industry-wide due to [event]"
```

## Usage Examples

### Weekly Summary

```
User: "Weekly performance summary"

Skill generates:
1. Aggregate week's data
2. Compare to prior week
3. Highlight wins/concerns
4. Generate recommendations

Output:
"Weekly Marketing Performance

Week of Dec 2-8, 2025

Summary:
- Revenue: $342,100 (+22% vs last week)
- Spend: $125,432 (+12%)
- ROAS: 2.73x (target: 2.5x) ✅
- New Customers: 3,421 (+8%)

Top Win:
Holiday email campaign drove $45K revenue (32% of total)
with industry-leading 28% open rate

Area of Concern:
Paid social ROAS declined to 2.1x (from 2.5x)
- Cause: Increased competition during holiday
- Action: Refresh creative, test new audiences

Recommendations:
1. Double down on email (highest ROAS at 8.5x)
2. Test new social audiences before year end
3. Increase retargeting budget by 20%

Full report: .aiwg/marketing/reports/weekly-2025-12-08.md"
```

### Quick Status

```
User: "How are we doing?"

Skill returns quick status:
"Marketing Performance Status

Period: MTD (Dec 1-8)

✅ On Track:
- Revenue: 105% of target
- Email: Exceeding all metrics
- Organic: Traffic up 12% MoM

⚠️ Watch:
- Paid social ROAS down 10%
- CAC creeping up (now $42 vs $38 target)

❌ Action Needed:
- Conversion rate drop on landing page
- Investigate and fix today

Overall: Solid performance, one issue to address"
```

### Executive Report

```
User: "Prepare executive summary for leadership meeting"

Skill generates executive-ready report:
"Preparing Executive Marketing Summary...

Report: Q4 Marketing Performance Review

Key Highlights:
1. Revenue attribution: $1.2M (+18% YoY)
2. Marketing efficiency improved: CAC down 12%
3. Brand awareness: Share of voice up 5 points

Investment Recommendation:
Request 15% budget increase for Q1 based on:
- Proven ROAS of 3.2x
- Market opportunity in healthcare vertical
- Competitor pullback creating opportunity

Full report with visualizations prepared.

Location: .aiwg/marketing/reports/exec-q4-2025.md"
```

## Integration

This skill uses:
- `data-pipeline`: Source all marketing data
- `competitive-intel`: Market context
- `artifact-metadata`: Track report versions

## Agent Orchestration

```yaml
agents:
  analysis:
    agent: marketing-analyst
    focus: Data analysis and insights

  reporting:
    agent: reporting-specialist
    focus: Report formatting and visualization

  strategy:
    agent: campaign-strategist
    focus: Recommendations and action items
```

## Configuration

### Report Scheduling

```yaml
schedule:
  daily_digest:
    time: "09:00"
    timezone: "America/New_York"
    recipients: [marketing_team]

  weekly_summary:
    day: "Monday"
    time: "08:00"
    recipients: [marketing_manager, director]

  monthly_report:
    day: 1
    time: "08:00"
    recipients: [leadership, finance]
```

### Metric Thresholds

```yaml
thresholds:
  green:
    vs_target: ">= 100%"
    vs_prior: ">= -5%"

  yellow:
    vs_target: "80-99%"
    vs_prior: "-5% to -15%"

  red:
    vs_target: "< 80%"
    vs_prior: "< -15%"
```

### Audience Customization

```yaml
audience_config:
  executive:
    detail_level: high
    focus: business_impact
    length: brief
    visualizations: summary_charts

  manager:
    detail_level: medium
    focus: tactical_insights
    length: moderate
    visualizations: detailed_charts

  team:
    detail_level: detailed
    focus: operational_metrics
    length: comprehensive
    visualizations: data_tables
```

## Output Locations

- Daily digests: `.aiwg/marketing/reports/daily/`
- Weekly summaries: `.aiwg/marketing/reports/weekly/`
- Monthly reports: `.aiwg/marketing/reports/monthly/`
- Executive reports: `.aiwg/marketing/reports/executive/`

## References

- Report templates: templates/marketing/report-*.md
- KPI definitions: .aiwg/marketing/config/kpis.yaml
- Benchmark data: .aiwg/marketing/benchmarks/
