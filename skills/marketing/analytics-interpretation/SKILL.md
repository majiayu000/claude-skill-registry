---
name: analytics-interpretation
description: |
  Interpret GA4, GSC, and SE Ranking data for content optimization.
  Provides benchmarks, status indicators, and actionable insights.
---

# Analytics Interpretation

## When to Use

- Analyzing content performance reports
- Understanding traffic patterns
- Interpreting search console data
- Making data-driven content decisions
- Explaining metrics to stakeholders

## Metric Benchmarks

### Google Analytics 4 (GA4)

| Metric | Good | Warning | Poor | Action When Poor |
|--------|------|---------|------|------------------|
| Avg Time on Page | >3 min | 1-3 min | <1 min | Improve content depth, add multimedia |
| Bounce Rate | <40% | 40-70% | >70% | Add internal links, improve intro hook |
| Engagement Rate | >60% | 30-60% | <30% | Review content quality, add CTAs |
| Scroll Depth | >75% | 50-75% | <50% | Add visual breaks, improve structure |
| Pages/Session | >2.5 | 1.5-2.5 | <1.5 | Improve internal linking |

### Google Search Console (GSC)

| Metric | Good | Warning | Poor | Action When Poor |
|--------|------|---------|------|------------------|
| CTR | >5% | 2-5% | <2% | Improve title/meta description |
| Avg Position | 1-3 | 4-10 | >10 | Strengthen content, build links |
| Impressions Trend | Growing | Stable | Declining | Refresh content, target new keywords |
| Mobile Usability | PASS | - | FAIL | Fix mobile issues immediately |
| Core Web Vitals | GOOD | NEEDS_IMPROVEMENT | POOR | Optimize performance |

### SE Ranking

| Metric | Good | Warning | Poor | Action When Poor |
|--------|------|---------|------|------------------|
| Visibility Score | >50 | 20-50 | <20 | Expand keyword coverage |
| Position Changes | Improving | Stable | Declining | Investigate, refresh content |
| Competitor Gap | Ahead | Even | Behind | Competitive analysis needed |
| Backlink Growth | Positive | Neutral | Negative | Link building campaign |

## Interpreting Combined Signals

### Traffic Quality Matrix

```
                    High Engagement
                          │
           ┌──────────────┼──────────────┐
           │  HIDDEN GEM  │   STAR       │
           │  Low traffic │   High traffic│
           │  High quality│   High quality│
           │  → Promote   │   → Maintain  │
Low ───────┼──────────────┼──────────────┼─── High
Traffic    │              │              │   Traffic
           │  UNDERPERFORM│   LEAKY      │
           │  Low traffic │   High traffic│
           │  Low quality │   Low quality │
           │  → Rework    │   → Optimize  │
           └──────────────┼──────────────┘
                          │
                    Low Engagement
```

### Search Intent Alignment

| GSC Signal | GA4 Signal | Interpretation |
|------------|------------|----------------|
| High impressions | Low clicks | Title/meta mismatch with intent |
| High CTR | High bounce | Content doesn't deliver on promise |
| Low CTR | High engagement (when clicked) | Hidden gem, improve snippet |
| Growing impressions | Stable clicks | Ranking improving, CTR opportunity |

## Score Calculation Methodology

### Content Health Score (0-100)

```
health_score = (
    engagement_score × 0.30 +
    seo_score × 0.30 +
    ranking_score × 0.20 +
    trend_score × 0.20
)
```

**Component Calculations:**

```
engagement_score = normalize(
    time_on_page_score × 0.4 +
    bounce_rate_score × 0.3 +
    scroll_depth_score × 0.3
)

seo_score = normalize(
    ctr_score × 0.4 +
    position_score × 0.4 +
    impressions_growth × 0.2
)

ranking_score = normalize(
    avg_position × 0.5 +
    visibility_score × 0.3 +
    keyword_coverage × 0.2
)

trend_score = normalize(
    traffic_trend × 0.4 +
    ranking_trend × 0.3 +
    engagement_trend × 0.3
)
```

### Score Interpretation

| Score | Rating | Status | Action |
|-------|--------|--------|--------|
| 90-100 | Excellent | Performing optimally | Maintain, minor tweaks |
| 75-89 | Good | Solid performance | Optimize weak areas |
| 60-74 | Fair | Room for improvement | Address key issues |
| 40-59 | Poor | Underperforming | Major revision needed |
| 0-39 | Critical | Failing | Complete overhaul |

## Trend Analysis

### Week-over-Week Comparison

```markdown
| Metric | This Week | Last Week | Change | Status |
|--------|-----------|-----------|--------|--------|
| Sessions | 1,245 | 1,180 | +5.5% | ↑ GROWING |
| Avg Position | 4.2 | 4.8 | +0.6 | ↑ IMPROVING |
| CTR | 2.8% | 2.6% | +0.2pp | ↑ IMPROVING |
| Bounce Rate | 42% | 38% | +4pp | ↓ DECLINING |
```

### Interpreting Trends

| Trend Pattern | Interpretation | Recommended Action |
|---------------|----------------|-------------------|
| ↑↑↑ All metrics up | Content gaining momentum | Double down, create related content |
| ↑↓↑ Mixed signals | Transition period | Monitor closely, identify cause |
| ↓↓↓ All metrics down | Content declining | Urgent refresh needed |
| →→→ All flat | Plateau reached | Experiment with new angles |

## Anomaly Detection

### Significant Change Thresholds

| Metric | Significant Change | Alert Level |
|--------|-------------------|-------------|
| Traffic | ±30% WoW | HIGH |
| CTR | ±1pp WoW | MEDIUM |
| Position | ±5 positions | HIGH |
| Bounce Rate | ±10pp WoW | MEDIUM |

### Common Anomaly Causes

| Anomaly | Possible Causes |
|---------|-----------------|
| Sudden traffic drop | Algorithm update, technical issue, competitor |
| CTR spike | SERP feature win, seasonal interest |
| Position fluctuation | Google testing, competitor changes |
| Engagement drop | Content staleness, UX issue |

## Output Templates

### Metric Summary Card

```markdown
## {Metric Name}

**Current Value**: {value}
**Benchmark**: {benchmark}
**Status**: {GOOD|WARNING|POOR}
**Trend**: {↑|→|↓} ({change}% vs last period)

**Interpretation**: {1-2 sentence explanation}

**Recommended Action**: {specific action if needed}
```

### Executive Summary

```markdown
## Content Performance Summary

**Overall Health**: {score}/100 ({rating})

### Key Wins
- {positive finding 1}
- {positive finding 2}

### Concerns
- {issue 1}
- {issue 2}

### Priority Actions
1. {highest priority action}
2. {second priority action}
3. {third priority action}
```
