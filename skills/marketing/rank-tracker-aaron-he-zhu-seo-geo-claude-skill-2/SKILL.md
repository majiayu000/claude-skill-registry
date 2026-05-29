---
name: rank-tracker
description: Tracks and analyzes keyword ranking positions over time for both traditional search results and AI-generated responses. Monitors ranking changes, identifies trends, and alerts on significant movements.
geo-relevance: "medium"
---

# Rank Tracker

This skill helps you track, analyze, and report on keyword ranking positions over time. It monitors both traditional SERP rankings and AI/GEO visibility to provide comprehensive search performance insights.

## When to Use This Skill

- Setting up ranking tracking for new campaigns
- Monitoring keyword position changes
- Analyzing ranking trends over time
- Comparing rankings against competitors
- Tracking SERP feature appearances
- Monitoring AI Overview inclusions
- Creating ranking reports for stakeholders

## What This Skill Does

1. **Position Tracking**: Records and tracks keyword rankings
2. **Trend Analysis**: Identifies ranking patterns over time
3. **Movement Detection**: Flags significant position changes
4. **Competitor Comparison**: Benchmarks against competitors
5. **SERP Feature Tracking**: Monitors featured snippets, PAA
6. **GEO Visibility Tracking**: Tracks AI citation appearances
7. **Report Generation**: Creates ranking performance reports

## How to Use

### Set Up Tracking

```
Set up rank tracking for [domain] targeting these keywords: [keyword list]
```

### Analyze Rankings

```
Analyze ranking changes for [domain] over the past [time period]
```

### Compare to Competitors

```
Compare my rankings to [competitor] for [keywords]
```

### Generate Reports

```
Create a ranking report for [domain/campaign]
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~SEO tool + ~~search console + ~~analytics + ~~AI monitor connected:**
Automatically pull ranking positions from ~~SEO tool, search impressions/clicks from ~~search console, traffic data from ~~analytics, and AI Overview citation tracking from ~~AI monitor. Daily automated rank checks with historical trend data.

**With manual data only:**
Ask the user to provide:
1. Keyword ranking positions (current and historical if available)
2. Target keyword list with search volumes
3. Competitor domains and their ranking positions for key terms
4. SERP feature status (featured snippets, PAA appearances)
5. AI Overview citation data (if tracking GEO metrics)

Proceed with the full analysis using provided data. Note in the output which metrics are from automated collection vs. user-provided data.

## Instructions

When a user requests rank tracking or analysis:

1. **Set Up Keyword Tracking**

   ```markdown
   ## Rank Tracking Setup
   
   ### Tracking Configuration
   
   **Domain**: [domain]
   **Tracking Location**: [country/city]
   **Device**: [Mobile/Desktop/Both]
   **Language**: [language]
   **Update Frequency**: [Daily/Weekly/Monthly]
   
   ### Keywords to Track
   
   | Keyword | Volume | Current Rank | Type | Priority |
   |---------|--------|--------------|------|----------|
   | [keyword 1] | [vol] | [rank] | Primary | High |
   | [keyword 2] | [vol] | [rank] | Primary | High |
   | [keyword 3] | [vol] | [rank] | Secondary | Medium |
   | [keyword 4] | [vol] | [rank] | Long-tail | Medium |
   | [keyword 5] | [vol] | [rank] | Brand | High |
   
   ### Competitor Tracking
   
   Track these competitors for benchmark:
   1. [Competitor 1] - [domain]
   2. [Competitor 2] - [domain]
   3. [Competitor 3] - [domain]
   
   ### Tracking Categories
   
   | Category | Keywords | Description |
   |----------|----------|-------------|
   | Brand | [X] | Brand name variations |
   | Product | [X] | Product-related terms |
   | Informational | [X] | Educational queries |
   | Commercial | [X] | Buying intent terms |
   ```

2. **Record Current Rankings**

   ```markdown
   ## Current Ranking Snapshot
   
   **Date**: [date]
   **Domain**: [domain]
   
   ### Ranking Overview
   
   | Position Range | Keyword Count | % of Total |
   |----------------|---------------|------------|
   | #1 | [X] | [X]% |
   | #2-3 | [X] | [X]% |
   | #4-10 | [X] | [X]% |
   | #11-20 | [X] | [X]% |
   | #21-50 | [X] | [X]% |
   | #51-100 | [X] | [X]% |
   | Not ranking | [X] | [X]% |
   
   ### Position Distribution
   
   ```
   Position 1:     ████████ [X] keywords
   Position 2-3:   ██████ [X] keywords
   Position 4-10:  ████████████████ [X] keywords
   Position 11-20: ████████████ [X] keywords
   Position 21+:   ██████████ [X] keywords
   ```
   
   ### Detailed Rankings
   
   | Keyword | Position | URL | SERP Features | Change |
   |---------|----------|-----|---------------|--------|
   | [kw 1] | 3 | [url] | Featured Snippet | +2 ↑ |
   | [kw 2] | 7 | [url] | PAA | -1 ↓ |
   | [kw 3] | 12 | [url] | None | New |
   | [kw 4] | 1 | [url] | Featured Snippet | — |
   ```

3. **Analyze Ranking Changes**

   ```markdown
   ## Ranking Change Analysis
   
   **Period**: [start date] to [end date]
   
   ### Overall Movement
   
   | Metric | Start | End | Change |
   |--------|-------|-----|--------|
   | Avg Position | [X] | [Y] | [+/-Z] |
   | Keywords in Top 10 | [X] | [Y] | [+/-Z] |
   | Keywords in Top 3 | [X] | [Y] | [+/-Z] |
   | Keywords #1 | [X] | [Y] | [+/-Z] |
   
   ### Biggest Improvements 📈
   
   | Keyword | Old Rank | New Rank | Change | Est. Traffic Impact |
   |---------|----------|----------|--------|---------------------|
   | [kw 1] | 15 | 4 | +11 | +[X] visits/mo |
   | [kw 2] | 25 | 9 | +16 | +[X] visits/mo |
   | [kw 3] | 8 | 2 | +6 | +[X] visits/mo |
   
   **Possible causes**:
   - [kw 1]: [hypothesis - e.g., content refresh may have improved relevance]
   - [kw 2]: [hypothesis]

   ### Biggest Declines 📉

   | Keyword | Old Rank | New Rank | Change | Est. Traffic Impact |
   |---------|----------|----------|--------|---------------------|
   | [kw 1] | 3 | 12 | -9 | -[X] visits/mo |
   | [kw 2] | 7 | 18 | -11 | -[X] visits/mo |

   **Likely factors**:
   - [kw 1]: [hypothesis - e.g., competitor may have published updated guide]
   - [kw 2]: [hypothesis]

   > These are hypotheses based on available signals, not confirmed causes. Investigate each with the relevant skill (on-page-seo-auditor, content-quality-auditor, backlink-analyzer) to confirm.
   
   **Recommended actions**:
   - [kw 1]: [action to recover]
   - [kw 2]: [action to recover]
   
   ### Stable Keywords
   
   [X] keywords remained within ±3 positions (stable)
   
   ### New Rankings
   
   | Keyword | Position | URL | Notes |
   |---------|----------|-----|-------|
   | [kw 1] | [pos] | [url] | [notes] |
   
   ### Lost Rankings
   
   | Keyword | Last Position | URL | Action |
   |---------|---------------|-----|--------|
   | [kw 1] | [pos] | [url] | [investigate/refresh] |
   ```

4. **Track SERP Features**

   ```markdown
   ## SERP Feature Tracking
   
   ### Feature Ownership
   
   | Feature | Your Count | Competitor Avg | Opportunity |
   |---------|------------|----------------|-------------|
   | Featured Snippets | [X] | [Y] | [+/-Z] |
   | People Also Ask | [X] | [Y] | [+/-Z] |
   | Image Pack | [X] | [Y] | [+/-Z] |
   | Video Results | [X] | [Y] | [+/-Z] |
   | Local Pack | [X] | [Y] | [+/-Z] |
   
   ### Featured Snippet Status
   
   | Keyword | You Own? | Current Owner | Winnable? |
   |---------|----------|---------------|-----------|
   | [kw 1] | ✅ Yes | You | Maintain |
   | [kw 2] | ❌ No | [Competitor] | High |
   | [kw 3] | ❌ No | [Competitor] | Medium |
   
   ### PAA Appearances
   
   | Question | Your Answer? | Position | Action |
   |----------|--------------|----------|--------|
   | [Question 1] | ✅/❌ | [pos] | [action] |
   | [Question 2] | ✅/❌ | [pos] | [action] |
   ```

5. **Track GEO/AI Visibility**

   ```markdown
   ## AI/GEO Visibility Tracking
   
   ### AI Overview Presence
   
   | Keyword | AI Overview | You Cited? | Citation Position |
   |---------|-------------|------------|-------------------|
   | [kw 1] | Yes | ✅ | 1st source |
   | [kw 2] | Yes | ✅ | 3rd source |
   | [kw 3] | Yes | ❌ | Not cited |
   | [kw 4] | No | N/A | N/A |
   
   ### AI Citation Rate
   
   | Metric | Value |
   |--------|-------|
   | Keywords with AI Overview | [X]/[Total] ([Y]%) |
   | Your citations in AI Overview | [X]/[Y] ([Z]%) |
   | Avg citation position | [X] |
   
   ### GEO Performance Trend
   
   | Period | AI Overviews Tracked | Your Citations | Rate |
   |--------|---------------------|----------------|------|
   | Last week | [X] | [Y] | [Z]% |
   | 2 weeks ago | [X] | [Y] | [Z]% |
   | Month ago | [X] | [Y] | [Z]% |
   
   ### GEO Improvement Opportunities
   
   | Keyword | Has AI Overview | You Cited? | Content Gap |
   |---------|-----------------|------------|-------------|
   | [kw 1] | Yes | No | Need clearer definition |
   | [kw 2] | Yes | No | Missing quotable stats |
   ```

6. **Compare Against Competitors**

   ```markdown
   ## Competitor Ranking Comparison
   
   ### Share of Voice
   
   | Domain | Keywords Ranked | Avg Position | Visibility |
   |--------|-----------------|--------------|------------|
   | [Your site] | [X] | [Y] | [Z]% |
   | [Competitor 1] | [X] | [Y] | [Z]% |
   | [Competitor 2] | [X] | [Y] | [Z]% |
   | [Competitor 3] | [X] | [Y] | [Z]% |
   
   ### Head-to-Head Comparison
   
   **You vs [Competitor 1]**:
   
   | Keyword | Your Rank | Their Rank | Winner |
   |---------|-----------|------------|--------|
   | [kw 1] | 3 | 7 | You ✅ |
   | [kw 2] | 12 | 5 | Them ❌ |
   | [kw 3] | 1 | 4 | You ✅ |
   
   **Summary**: You win [X]/[Y] keywords vs [Competitor 1]
   
   ### Competitor Movement Alerts
   
   | Competitor | Keyword | Their Change | Threat Level |
   |------------|---------|--------------|--------------|
   | [Comp 1] | [kw] | +15 positions | 🔴 High |
   | [Comp 2] | [kw] | +8 positions | 🟡 Medium |
   ```

7. **Generate Ranking Report**

   ```markdown
   # Ranking Performance Report
   
   **Domain**: [domain]
   **Report Period**: [start] to [end]
   **Generated**: [date]
   
   ## Executive Summary
   
   **Overall Trend**: [Improving/Stable/Declining]
   
   | Metric | Value | vs Last Period | Status |
   |--------|-------|----------------|--------|
   | Total keywords tracked | [X] | [+/-Y] | [status] |
   | Keywords in top 10 | [X] | [+/-Y] | [status] |
   | Keywords in top 3 | [X] | [+/-Y] | [status] |
   | Average position | [X] | [+/-Y] | [status] |
   | Estimated traffic | [X] | [+/-Y]% | [status] |
   
   ## Position Distribution
   
   ```
   Position 1:     ████████████ [X]%
   Position 2-3:   ████████ [X]%
   Position 4-10:  ████████████████ [X]%
   Position 11-20: ██████████ [X]%
   Position 21+:   ████ [X]%
   ```
   
   ## Key Highlights
   
   ### Wins 🎉
   - [Achievement 1]
   - [Achievement 2]
   - [Achievement 3]
   
   ### Concerns ⚠️
   - [Issue 1]
   - [Issue 2]
   
   ### Opportunities 💡
   - [Opportunity 1]
   - [Opportunity 2]
   
   ## Detailed Analysis
   
   ### Top Performing Keywords
   
   | Keyword | Position | Change | Traffic | Notes |
   |---------|----------|--------|---------|-------|
   | [kw 1] | 1 | — | [X] | Stable leader |
   | [kw 2] | 2 | +3 | [X] | Growing |
   | [kw 3] | 3 | +5 | [X] | Big improvement |
   
   ### Keywords Needing Attention
   
   | Keyword | Position | Change | Issue | Recommended Action |
   |---------|----------|--------|-------|-------------------|
   | [kw 1] | 15 | -8 | Dropped | Refresh content |
   | [kw 2] | 22 | -5 | Competitor surge | Analyze competitor |
   
   ## SERP Feature Report
   
   | Feature | Count | Change | Competitor Avg |
   |---------|-------|--------|----------------|
   | Featured Snippets | [X] | [+/-Y] | [Z] |
   | PAA | [X] | [+/-Y] | [Z] |
   
   ## GEO/AI Visibility Report
   
   | Metric | This Period | Last Period | Trend |
   |--------|-------------|-------------|-------|
   | AI Overview appearances | [X] | [Y] | [↑/↓] |
   | Your citations | [X] | [Y] | [↑/↓] |
   | Citation rate | [X]% | [Y]% | [↑/↓] |
   
   ## Competitive Position
   
   **Share of Voice Ranking**: #[X] of [Y] competitors
   
   | Rank | Domain | Visibility |
   |------|--------|------------|
   | 1 | [domain] | [X]% |
   | 2 | [domain] | [X]% |
   | 3 | [domain] | [X]% |
   
   ## Recommendations
   
   ### Immediate Actions
   1. [Action] for [keyword] - [expected impact]
   2. [Action] for [keyword] - [expected impact]
   
   ### This Month
   1. [Action]
   2. [Action]
   
   ### Next Quarter
   1. [Strategic action]
   2. [Strategic action]
   
   ## Next Report

   Scheduled: [date]
   Focus areas: [areas to monitor]
   ```

## Validation Checkpoints

### Input Validation
- [ ] Keywords list is complete with search volumes
- [ ] Target domain and tracking location are specified
- [ ] Competitor domains identified for comparison
- [ ] Historical baseline data available or initial tracking period set

### Output Validation
- [ ] Every metric cites its data source and collection date
- [ ] Ranking changes include context (vs. previous period)
- [ ] Significant movements have explanations or investigation notes
- [ ] Source of each data point clearly stated (~~SEO tool data, ~~search console data, user-provided, or estimated)

## Example

**User**: "Analyze my ranking changes for the past month"

**Output**:

```markdown
# Ranking Analysis: [current month, year]

## Summary

Your average position improved from 15.3 to 12.8 (-2.5 positions = better)
Keywords in top 10 increased from 12 to 17 (+5)

## Biggest Wins

| Keyword | Old | New | Change | Possible Cause |
|---------|-----|-----|--------|----------------|
| email marketing tips | 18 | 5 | +13 | Likely driven by content refresh |
| best crm software | 24 | 11 | +13 | Correlates with new backlinks acquired |
| sales automation | 15 | 7 | +8 | Correlates with schema markup addition |

## Needs Attention

| Keyword | Old | New | Change | Action |
|---------|-----|-----|--------|--------|
| marketing automation | 4 | 12 | -8 | Likely displaced by new HubSpot guide |

**Recommended**: Update your marketing automation guide with [current year] statistics and examples.
```

## Tips for Success

1. **Track consistently** - Same time, same device, same location
2. **Include enough keywords** - 50-200 for meaningful data
3. **Segment by intent** - Track brand, commercial, informational separately
4. **Monitor competitors** - Context makes your data meaningful
5. **Track SERP features** - Position 1 without snippet may lose to position 4 with snippet
6. **Include GEO metrics** - AI visibility increasingly important

## Rank Change Analysis Framework

### Why Rankings Move — Root Cause Taxonomy

| Category | Causes | Detection Method |
|----------|--------|-----------------|
| **Algorithm Updates** | Google core update, helpful content update, spam update | Check Google Search Status Dashboard, SEO news |
| **Competitor Action** | New content published, content updated, new backlinks | Monitor competitor pages, SERP changes |
| **Your Changes** | Content edit, technical change, migration | Cross-reference with deploy/change log |
| **SERP Feature Changes** | New featured snippet, AI Overview added/removed | SERP monitoring tools |
| **Seasonal Patterns** | Predictable demand shifts | Year-over-year comparison |
| **Technical Issues** | Crawl errors, speed degradation, indexing problems | Search Console, crawl reports |
| **Link Profile Changes** | Lost backlinks, new backlinks, disavow | Backlink monitoring |

### Rank Change Response Protocol

| Change | Timeframe | Action |
|--------|-----------|--------|
| Drop 1-3 positions | Wait 1-2 weeks | Monitor — may be normal fluctuation |
| Drop 3-5 positions | Investigate within 1 week | Check for technical issues, competitor changes |
| Drop 5-10 positions | Investigate immediately | Full diagnostic: technical, content, links |
| Drop off page 1 | Emergency response | Comprehensive audit + recovery plan |
| Position gained | Document and learn | What worked? Can you replicate? |

## Position Distribution Benchmarks

### Click-Through Rate by Position

| Position | Desktop CTR | Mobile CTR | Notes |
|----------|------------|------------|-------|
| #1 | 31.7% | 24.0% | 10x more than position #10 |
| #2 | 14.7% | 13.1% | ~50% drop from #1 |
| #3 | 10.7% | 9.5% | Significant value |
| #4 | 6.7% | 6.1% | Still above fold usually |
| #5 | 5.1% | 4.6% | Often near fold |
| #6 | 4.1% | 3.5% | Below fold on most devices |
| #7 | 3.4% | 2.8% | Rapidly diminishing |
| #8 | 2.9% | 2.3% | |
| #9 | 2.5% | 1.9% | |
| #10 | 2.2% | 1.6% | Bottom of page 1 |
| #11-20 | <1.5% | <1.0% | Page 2 — minimal visibility |

_Note: CTR varies significantly by query type, SERP features, and industry. These are averages._

### CTR Impact of SERP Features

| SERP Feature Present | Effect on Organic CTR |
|---------------------|---------------------|
| Featured Snippet (you own) | +20-30% CTR for your result |
| Featured Snippet (competitor) | -15-25% CTR for position #1 |
| AI Overview | -10-30% CTR for all organic results |
| PAA boxes | -5-10% CTR for positions 3-6 |
| Shopping results | -10-20% CTR for commercial queries |
| Knowledge Panel | -5-15% CTR for navigational queries |

## SERP Volatility Context

### Algorithm Update Impact Assessment

| Update Type | Typical Impact | Recovery Time | Response Strategy |
|------------|---------------|---------------|-------------------|
| Core update | ±20-50% traffic shifts | 3-6 months (next core update) | Improve content quality broadly |
| Helpful Content | Content quality focused | 1-3 months | Remove/improve unhelpful content |
| Spam update | Penalizes manipulative tactics | Varies (may require disavow) | Clean up link profile, remove spam |
| Product Reviews | Review content specific | 1-2 months | Improve review depth and expertise |
| Link Spam | Targets artificial links | 2-4 months | Disavow toxic links, build quality links |

## Tracking Configuration Best Practices

| Setting | Recommendation | Why |
|---------|---------------|-----|
| Check frequency | Daily for top 20 keywords; weekly for others | Balance accuracy vs. API costs |
| Location settings | Match target market; track local separately | Rankings vary by location |
| Device tracking | Track mobile AND desktop separately | Mobile rankings differ significantly |
| Competitor tracking | Track 3-5 competitors for key terms | Context for your own movements |
| SERP features | Track which features appear | Explain CTR changes |
| Keyword grouping | Group by topic cluster, intent, funnel stage | Identify patterns, not just keywords |

## Reference Materials

- [Tracking Setup Guide](./references/tracking-setup-guide.md) — Configuration best practices, device/location settings, and SERP feature tracking setup

## Related Skills

- [keyword-research](../../research/keyword-research/) — Find keywords to track
- [serp-analysis](../../research/serp-analysis/) — Understand SERP composition
- [alert-manager](../alert-manager/) — Set up ranking alerts
- [performance-reporter](../performance-reporter/) — Comprehensive reporting
- [memory-management](../../cross-cutting/memory-management/) — Store ranking history in project memory

