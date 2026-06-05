---
name: kai-daily-ad-review
description: Daily ad performance check-in across platforms. Pulls live metrics from Meta, Google, and LinkedIn via deterministic scripts, compares against benchmarks and previous period, flags overspend/underperformers/policy issues, and outputs a quick daily summary with action items. Use when "daily ad review", "how are my ads doing today", "ad check-in", "morning ad report", "daily ad summary", "check ad performance", "ad dashboard", "daily ads", or any request for a recurring or quick-glance ad performance review.
---

Daily ad performance check-in. Pull live data via scripts, compare against benchmarks, flag problems, output a summary with action items.

This is NOT the same as `/kai-ad-campaign` (which creates/evaluates campaigns end-to-end). This is a fast daily pulse check — meant to run every morning or on-demand.

## Phase 0: Pull Ad Data

Run the unified pull script. It auto-detects which platforms have credentials and pulls everything.

```bash
cd E:/Dev2/kai-cmo-harness-work && python scripts/ads/pull_all.py
```

This writes structured JSON to `workspace/ads/pulls/YYYY-MM-DD/`:
- `meta.json` — Full Meta/Facebook/Instagram data (if META_ACCESS_TOKEN configured)
- `google.json` — Full Google Ads data (if GOOGLE_ADS_* configured)
- `linkedin.json` — Full LinkedIn Ads data (if LINKEDINADS_* configured)
- `summary.json` — Cross-platform totals

To pull a specific platform only: `python scripts/ads/pull_all.py --platforms meta`

### What the scripts pull (comprehensive)

**Meta** (`scripts/ads/meta.py pull`):
- Account insights: today, yesterday, 7d, 14d, 28d
- Campaign insights: 7d aggregate + 14d daily breakdown
- Ad set insights: 7d aggregate + 14d daily + **targeting spec with LAL/audience classification**
- Ad insights: 7d with creative details
- Breakdowns: age/gender, platform/position, device
- Fields include: impressions, **reach**, **frequency**, spend, clicks, unique_clicks, ctr, unique_ctr, cpc, cpm, actions, cost_per_action_type, conversions, **quality_ranking**, **engagement_rate_ranking**, **conversion_rate_ranking**, video_p25/50/75/100, video_thruplay
- **Mutations**: `meta.py pause/activate/budget/create-campaign/create-adset/create-ad/upload-image/upload-video/duplicate-adset` (dry-run by default, `--execute` to apply)

**Google** (`scripts/ads/google.py pull`):
- Campaign performance: 30d daily breakdown
- Ad group performance: 14d daily
- Ad performance: 14d aggregate with RSA headline/description details
- Search terms report: top 100 by spend (7d)
- Audience segments: campaign-level
- Keyword quality scores: quality_score, creative_quality, post_click_quality, predicted_ctr
- **Mutations**: `google.py pause/activate/budget/add-negative` (dry-run by default, `--execute` to apply)

**LinkedIn** (`scripts/ads/linkedin.py pull`):
- Campaign group and campaign insights: 7d, 14d daily, 28d
- Creative-level insights: 7d
- Audience breakdowns: company size, industry, job function, seniority, country
- Audience classification from targeting criteria
- **Mutations**: `linkedin.py pause/activate/budget` (dry-run by default, `--execute` to apply)

### If a platform isn't configured

The script will skip it and log which env vars are missing. At minimum, Meta should be configured:
```
META_ACCESS_TOKEN=<long-lived token>
META_AD_ACCOUNT_ID=<numeric, without act_ prefix>
```

## Phase 1: Read and Analyze Pull Data

Read the JSON files from today's pull:

```python
import json
from pathlib import Path

date = "YYYY-MM-DD"  # today's date
pull_dir = Path(f"workspace/ads/pulls/{date}")

# Read whatever's available
for f in pull_dir.glob("*.json"):
    with open(f) as fh:
        data = json.load(fh)
    # Analyze...
```

### Key metrics to extract per platform

**From Meta (meta.json):**
- `account_insights.last_7d` → spend, impressions, reach, frequency, ctr, cpc
- `campaigns[].insights_7d` → per-campaign performance
- `adsets[].audience_type` → LAL vs custom vs interest vs advantage+ vs broad
- `adsets[].insights_daily` → day-by-day trends for fatigue detection
- `ads[].insights_7d` → per-ad creative performance
- `ads[].insights_7d.quality_ranking` → Meta's diagnostic: ABOVE_AVERAGE_35, AVERAGE, BELOW_AVERAGE_35
- `breakdowns.age_gender` → demographic performance
- `breakdowns.platform_position` → FB Feed vs IG Reels vs Stories etc.

**From Google (google.json):**
- `campaigns[].insights_daily` → day-by-day CPC/CPA trends
- `search_terms` → wasted spend on irrelevant queries
- `keyword_quality` → quality score distribution (flag anything < 5)
- `audience_segments` → which audiences are converting

**From LinkedIn (linkedin.json):**
- `campaigns[].insights_7d` → engagement rate (higher baseline than Meta/Google)
- `breakdowns.industry` + `breakdowns.job_function` → who's engaging
- `campaigns[].audience_type` → matched audience vs professional targeting

## Phase 2: Cross-Reference with PostHog

Load: `harness/references/posthog-marketing-queries.md`

If PostHog is connected, pull:
- **Today's ad traffic** — pageviews with UTM breakdown (query #2)
- **Conversion events** — campaign attribution (query #8)
- **Landing page bounce** — for pages receiving ad traffic

This connects ad spend to actual on-site behavior.

## Phase 3: Benchmark Comparison

### Performance Benchmarks

| Metric | Poor | OK | Good | Great |
|--------|------|----|------|-------|
| CTR | < 0.5% | 0.5-1% | 1-2% | > 2% |
| CPC | > $5 | $3-5 | $1.50-3 | < $1.50 |
| CPL | > $50 | $30-50 | $15-30 | < $15 |
| ROAS | < 1x | 1-2x | 2-4x | > 4x |
| Frequency | > 4.0 | 3.0-4.0 | 1.5-3.0 | 1.0-1.5 |

Adjust benchmarks to the vertical (from `MARKETING.md` if available).

### Trend Detection

Compare today vs 7-day average:
- **Spend**: flag if today's pace > 120% of daily average (overspend)
- **CTR**: flag if today < 70% of 7-day avg (creative fatigue)
- **CPC**: flag if today > 130% of 7-day avg (competition spike or audience saturation)
- **Conversions**: flag if today < 50% of daily avg (broken funnel or tracking issue)
- **Frequency**: flag if > 3.0 (audience seeing ads too often — fatigue incoming)
- **Quality ranking**: flag if BELOW_AVERAGE_35 on any diagnostic dimension

### Audience Performance (from LAL tagging)

Compare ad set performance by `audience_type`:
- LAL audiences should have lower CPL than broad
- Custom retarget audiences should have highest CTR
- If Advantage+ is outperforming manual targeting, note it
- If LAL is underperforming interest targeting, flag for investigation

## Phase 4: Issue Detection

Flag these automatically:

| Issue | Trigger | Severity |
|-------|---------|----------|
| **Overspend** | Daily spend pace > 120% of budget | HIGH |
| **Zero impressions** | Active ad with 0 impressions today | HIGH |
| **CTR crash** | CTR < 50% of 7-day avg | HIGH |
| **CPC spike** | CPC > 150% of 7-day avg | MEDIUM |
| **No conversions** | Spend > $50 today with 0 conversions | MEDIUM |
| **Creative fatigue** | CTR declining 3+ consecutive days | MEDIUM |
| **Frequency overload** | Frequency > 3.5 on any ad set | MEDIUM |
| **Quality warning** | Any ad with BELOW_AVERAGE quality ranking | MEDIUM |
| **Budget underspend** | < 50% of daily budget used by midday | LOW |
| **Learning phase** | Ad set in learning phase > 7 days | LOW |
| **LAL underperform** | LAL CPL > broad/interest CPL | LOW |
| **Wasted search spend** | Google search term with > $20 spend, 0 conversions | MEDIUM |

## Phase 5: Daily Summary Output

Output format — keep it scannable:

```markdown
# Daily Ad Review — [Date]

## Snapshot
| Metric | Today | 7-Day Avg | Trend |
|--------|-------|-----------|-------|
| Spend | $X | $X/day | up/down/flat |
| Impressions | X | X/day | |
| Reach | X | X/day | |
| Frequency | X.X | X.X | |
| Clicks | X | X/day | |
| CTR | X% | X% | |
| CPC | $X | $X | |
| Conversions | X | X/day | |
| CPL | $X | $X | |

## Flags
- [HIGH] Overspend: Campaign "X" pacing 140% of daily budget
- [MEDIUM] Frequency: Ad set "Y" at 3.8 — rotate creative or expand audience
- [MEDIUM] Quality: Ad "Z" has BELOW_AVERAGE engagement ranking

## Audience Performance
| Audience Type | Ad Sets | Spend | Leads | CPL | CTR |
|---------------|---------|-------|-------|-----|-----|
| Lookalike 1% | 2 | $X | X | $X | X% |
| Custom Retarget | 1 | $X | X | $X | X% |
| Interest | 1 | $X | X | $X | X% |
| Advantage+ | 1 | $X | X | $X | X% |

## Campaign Breakdown
| Campaign | Spend | Clicks | CTR | CPC | Conversions | CPL | Status |
|----------|-------|--------|-----|-----|-------------|-----|--------|

## Top Performers
1. [Ad name] — [metric that makes it stand out]
2. [Ad name] — [metric]

## Underperformers
1. [Ad name] — [what's wrong] — **Action:** [pause/adjust/replace creative]
2. [Ad name] — [what's wrong] — **Action:** [specific fix]

## Quality Diagnostics
| Ad | Quality | Engagement | Conversion |
|----|---------|------------|------------|
(only show non-ABOVE_AVERAGE entries)

## Action Items
- [ ] [Specific action with campaign/ad name]
- [ ] [Specific action]
- [ ] [Specific action]
```

Write output to `workspace/ads/daily-reviews/[YYYY-MM-DD]-daily-review.md`.

## Phase 6: Historical Tracking

If previous daily reviews exist in `workspace/ads/daily-reviews/`, compare:
- Week-over-week spend trend
- Which flags are recurring (persistent issues need `/kai-ad-campaign` evaluation)
- Which action items from yesterday were addressed

If previous pull data exists in `workspace/ads/pulls/`, diff today's metrics against yesterday's for precise trend detection.

If the same flag appears 3+ days in a row, escalate: recommend running `/kai-ad-campaign` in evaluation mode for a deeper audit.

## Scheduling

This skill is designed to run daily. Recommend the user set up a schedule:
- `/schedule` to create a recurring morning trigger
- Or run manually with `/kai-daily-ad-review`
