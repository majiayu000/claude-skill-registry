---
name: tiktok-ads-optimization
description: TikTok Ads best practices for mobile app install campaigns. Use when creating, optimizing, or analyzing TikTok ad campaigns. Provides guidance on budget allocation, campaign structure, targeting, bidding, creative rotation, and KPI benchmarks.
---

# TikTok Ads Optimization Skill

This skill provides comprehensive guidance for running TikTok ads for mobile app installs, especially with limited budgets ($20-100/day).

## When to Use This Skill

- Creating new TikTok ad campaigns
- Analyzing campaign performance
- Optimizing underperforming campaigns
- Setting up targeting and bidding strategies
- Deciding on creative rotation schedules

## Core Principles

### 1. Budget Concentration > Distribution

**Never split limited budgets across multiple campaigns/ad groups.**

| Budget/Day | Structure |
|------------|-----------|
| < $30 | 1 Campaign, 1 Ad Group (mandatory) |
| $30-50 | 1 Campaign, 1-2 Ad Groups |
| $50-100 | 1 Campaign, 2-3 Ad Groups |
| $100+ | Test CBO with 3-5 Ad Groups |

**Why**: TikTok requires 50 conversions in 7 days to exit learning phase. Splitting budget = "zombie campaigns" that never learn.

### 2. Learning Phase Math

```
Minimum Daily Budget = 10 × Target CPI

Example:
- Target CPI: $4
- Minimum Budget: $40/day
- Time to 50 conversions: 12-13 days
```

### 3. Low Budget Strategy: Click → Install Progression

For budgets under $50/day:

| Phase | Duration | Optimization Goal | Purpose |
|-------|----------|-------------------|---------|
| Phase 1 | Week 1-2 | **Click** | Build pixel data, find winning creatives |
| Phase 2 | Week 3+ | **App Install** | Use learned data for efficient installs |

**Rationale**: Click optimization collects 10x more data at same budget, teaching the algorithm who your audience is.

## Campaign Settings Reference

### Campaign Level

| Setting | Recommended Value | Notes |
|---------|-------------------|-------|
| Objective | App Promotion → App Install | - |
| Budget Type | Daily Budget | Not Lifetime |
| Campaign Structure | Manual (not Smart+) | Smart+ needs $200+/day |

### Ad Group Level

| Setting | Recommended Value | Notes |
|---------|-------------------|-------|
| Optimization Goal | Click (Phase 1) or Install (Phase 2) | See progression strategy |
| Bidding Strategy | Maximum Delivery (Lowest Cost) | For discovery phase |
| Targeting | **Automatic (Broad)** | Narrow targeting fails with limited budget |
| Age | 18-44 (or custom) | Let algorithm optimize within range |
| Gender | All | Don't restrict |
| Location | Single country or region | Don't split by country |
| Placement | TikTok Only | Exclude Pangle for quality |
| Schedule | Always On | Let algorithm optimize delivery time |

### Why Broad Targeting?

TikTok official data shows:
- **CPA 15% lower** with broad targeting
- **CVR 20% higher** than interest-based targeting

Limited budget + narrow targeting = insufficient data = poor optimization.

## Bidding Strategy Progression

```
Week 1-2: Maximum Delivery (Lowest Cost)
    ↓ Gather 50+ conversions
Week 3+: Cost Cap (1.2× baseline CPA)
    ↓ If delivery drops
Increase Cost Cap by 10-20%
```

| Strategy | When to Use |
|----------|-------------|
| Maximum Delivery | Discovery phase, unknown CPA |
| Cost Cap | After baseline established |
| Bid Cap | Strict budget control (limits delivery) |

## Creative Management

### TikTok Fatigue is 4x Faster Than Meta

| Metric | TikTok | Meta |
|--------|--------|------|
| Peak Performance | Days 1-7 | Days 1-14 |
| Fatigue Onset | Week 2 | Week 3-4 |

### Creative Rotation Schedule

| Budget/Day | Active Creatives | Rotation Frequency | Monthly Production |
|------------|------------------|-------------------|-------------------|
| < $50 | 3-5 | Every 7 days | 4-6 new concepts |
| $50-100 | 5-8 | Every 5-7 days | 8-12 new concepts |
| $100+ | 8-15 | Every 3-5 days | 15-20 new concepts |

### Kill Criteria (48-72 hours)

| Metric | Kill Threshold | Action |
|--------|---------------|--------|
| Hook Rate (2-sec views) | < 20% | Kill immediately, remake hook |
| CTR | < 1% | Kill after 48hrs |
| CPI | > 2× target | Kill after 72hrs |
| Zero conversions | After 5 days | Kill |

### Let It Run Criteria

| Metric | Condition | Action |
|--------|-----------|--------|
| CPI | 1.2-1.5× target, improving trend | Run 3 more days |
| High Hook + CTR, low CVR | CVR < 5% | Keep ad, fix App Store page |

## KPI Benchmarks (2025-2026)

### CTR (Click-Through Rate)

| Optimization Goal | Poor | Average | Good | Excellent |
|-------------------|------|---------|------|-----------|
| App Install | < 1% | 1.0-1.5% | 1.5-2.0% | > 2.0% |

### CPI (Cost Per Install)

| App Category | Average CPI | Target |
|--------------|-------------|--------|
| Utilities/Tools | $1.50 | < $2 |
| Gaming | $2.00 | < $2.50 |
| Health/Fitness | $2.50 | < $3 |
| Subscription Apps | $4.00 | < $5 |
| Self-Improvement | $3-5 | < $4 |

### CVR (Conversion Rate)

| Metric | Poor | Average | Good |
|--------|------|---------|------|
| Install Rate (click → install) | < 5% | 6-10% | > 10% |

### Other Metrics

| Metric | Benchmark |
|--------|-----------|
| Hook Rate | > 30% |
| Hold Rate (6-sec/2-sec) | > 8% |
| CPC | $0.30-0.80 |
| CPM | $3-10 |
| Frequency (cold audience) | < 2.5 |

## Smart+ vs Manual Campaign

| Aspect | Smart+ | Manual |
|--------|--------|--------|
| Learning Period | 7 days | **3 days** |
| Budget Requirement | $200+/day | $20+/day |
| CPI | 39% lower | Higher but controllable |
| User Quality | Lower | **Higher** |
| Control | Minimal | Full |

**Decision**: Use Manual for budgets under $200/day.

## Geographic Strategy

### Single Language Campaigns

| Language | Countries | Structure |
|----------|-----------|-----------|
| Japanese | Japan only | 1 Ad Group |
| English | US + UK + CA + AU | 1 Ad Group (combined) |

**Never split by country with limited budget** - it fragments data.

### Why Not Split English Countries?

| Structure | Budget/Country | Learning Time |
|-----------|---------------|---------------|
| Split (4 Ad Groups) | $10 each | Never exits learning |
| Combined (1 Ad Group) | $40 total | ~12 days to exit |

## Troubleshooting

### Campaign Not Delivering

| Symptom | Cause | Fix |
|---------|-------|-----|
| 0 impressions | Budget too low, targeting too narrow | Increase budget or broaden targeting |
| Stuck in review | Policy violation | Review creative/landing page |
| Low delivery | Bid too low (Cost Cap) | Increase bid 10-20% |

### CPI Too High

| CPI vs Target | Action |
|---------------|--------|
| 1.2-1.5× | Wait 3 more days |
| 1.5-2× | Test new creatives |
| > 2× | Kill campaign, restart with different approach |

### CTR Too Low

| CTR | Diagnosis | Fix |
|-----|-----------|-----|
| < 0.5% | Hook broken | Remake first 2 seconds |
| 0.5-1% | Weak CTA | Test different CTAs |
| 1-1.5% | Acceptable | Continue testing |

## Weekly Review Checklist

| Day | Check | Action |
|-----|-------|--------|
| Daily | Spend pace, delivery issues | Fix immediately |
| Day 3 | Hook Rate, CTR by creative | Kill losers |
| Day 7 | CPI, CVR, learning phase status | Scaling decision |
| Weekly | Creative fatigue, frequency | Rotate creatives |

## Example Campaign Structure

### Phase 1: Discovery (Week 1-2)

```
Campaign: anicca-jp-click-discovery
├── Budget: 6,000 JPY/day
├── Bidding: Maximum Delivery
└── Ad Group: broad-jp-click
    ├── Optimization: Click
    ├── Targeting: Automatic (Broad)
    ├── Age: 18-44
    ├── Location: Japan
    ├── Placement: TikTok Only
    └── Creatives: 3-5 variations
```

### Phase 2: Install Optimization (Week 3+)

```
Campaign: anicca-jp-install-scale
├── Budget: 6,000-10,000 JPY/day
├── Bidding: Cost Cap (1.2× Phase 1 CPA)
└── Ad Group: broad-jp-install
    ├── Optimization: App Install
    ├── Targeting: Automatic (Broad)
    ├── Creatives: Winning 2-3 from Phase 1 + 2 new tests
```

## Sources

- TikTok Ads Manager Official Documentation
- TikTok Business Help Center
- Industry benchmarks from Varos, AdBacklog, Digital Eagle (2025)
- TikAdTools best practices
- Thesis A/B testing data

---

*Last updated: 2026-01-28*
