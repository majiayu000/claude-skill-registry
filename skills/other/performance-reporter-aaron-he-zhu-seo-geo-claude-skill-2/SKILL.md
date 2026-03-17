---
name: performance-reporter
version: "1.0"
description: Generates comprehensive SEO and GEO performance reports combining rankings, traffic, backlinks, and AI visibility metrics. Creates executive summaries and detailed analyses for stakeholder reporting.
---

# Performance Reporter

This skill creates comprehensive SEO and GEO performance reports that combine multiple metrics into actionable insights. It produces executive summaries, detailed analyses, and visual data presentations for stakeholder communication.

## When to Use This Skill

- Monthly/quarterly SEO reporting
- Executive stakeholder updates
- Client reporting for agencies
- Tracking campaign performance
- Combining multiple SEO metrics
- Creating GEO visibility reports
- Documenting ROI from SEO efforts

## What This Skill Does

1. **Data Aggregation**: Combines multiple SEO data sources
2. **Trend Analysis**: Identifies patterns across metrics
3. **Executive Summaries**: Creates high-level overviews
4. **Visual Reports**: Presents data in clear formats
5. **Benchmark Comparison**: Tracks against goals and competitors
6. **Content Quality Tracking**: Integrates CORE-EEAT scores across audited pages
7. **ROI Calculation**: Measures SEO investment returns
8. **Recommendations**: Suggests actions based on data

## How to Use

### Generate Performance Report

```
Create an SEO performance report for [domain] for [time period]
```

### Executive Summary

```
Generate an executive summary of SEO performance for [month/quarter]
```

### Specific Report Types

```
Create a GEO visibility report for [domain]
```

```
Generate a content performance report
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~analytics + ~~search console + ~~SEO tool + ~~AI monitor connected:**
Automatically aggregate traffic metrics from ~~analytics, search performance data from ~~search console, ranking and backlink data from ~~SEO tool, and GEO visibility metrics from ~~AI monitor. Creates comprehensive multi-source reports with historical trends.

**With manual data only:**
Ask the user to provide:
1. Analytics screenshots or traffic data export (sessions, users, conversions)
2. Search Console data (impressions, clicks, average position)
3. Keyword ranking data for the reporting period
4. Backlink metrics (referring domains, new/lost links)
5. Key performance indicators and goals for comparison
6. AI citation data if tracking GEO metrics

Proceed with the full analysis using provided data. Note in the output which metrics are from automated collection vs. user-provided data.

## Instructions

When a user requests a performance report:

1. **Define Report Parameters**

   ```markdown
   ## Report Configuration
   
   **Domain**: [domain]
   **Report Period**: [start date] to [end date]
   **Comparison Period**: [previous period for comparison]
   **Report Type**: [Monthly/Quarterly/Annual/Custom]
   **Audience**: [Executive/Technical/Client]
   **Focus Areas**: [Rankings/Traffic/Content/Backlinks/GEO]
   ```

2. **Create Executive Summary**

   ```markdown
   # SEO Performance Report
   
   **Domain**: [domain]
   **Period**: [date range]
   **Prepared**: [date]
   
   ---
   
   ## Executive Summary
   
   ### Overall Performance: [Excellent/Good/Needs Attention/Critical]
   
   **Key Highlights**:
   
   🟢 **Wins**:
   - [Win 1 - e.g., "Organic traffic increased 25%"]
   - [Win 2 - e.g., "3 new #1 rankings achieved"]
   - [Win 3 - e.g., "Conversion rate improved 15%"]
   
   🟡 **Watch Areas**:
   - [Area 1 - e.g., "Mobile rankings declining slightly"]
   - [Area 2 - e.g., "Competitor gaining ground on key terms"]
   
   🔴 **Action Required**:
   - [Issue 1 - e.g., "Technical SEO audit needed"]
   
   ### Key Metrics at a Glance
   
   | Metric | This Period | Last Period | Change | Target | Status |
   |--------|-------------|-------------|--------|--------|--------|
   | Organic Traffic | [X] | [Y] | [+/-Z%] | [T] | ✅/⚠️/❌ |
   | Keyword Rankings (Top 10) | [X] | [Y] | [+/-Z] | [T] | ✅/⚠️/❌ |
   | Organic Conversions | [X] | [Y] | [+/-Z%] | [T] | ✅/⚠️/❌ |
   | Domain Authority | [X] | [Y] | [+/-Z] | [T] | ✅/⚠️/❌ |
   | AI Citations | [X] | [Y] | [+/-Z%] | [T] | ✅/⚠️/❌ |
   
   ### SEO ROI
   
   **Investment**: $[X] (content, tools, effort)
   **Organic Revenue**: $[Y]
   **ROI**: [Z]%
   ```

3. **Report Organic Traffic Performance**

   ```markdown
   ## Organic Traffic Analysis
   
   ### Traffic Overview
   
   | Metric | This Period | vs Last Period | vs Last Year |
   |--------|-------------|----------------|--------------|
   | Sessions | [X] | [+/-Y%] | [+/-Z%] |
   | Users | [X] | [+/-Y%] | [+/-Z%] |
   | Pageviews | [X] | [+/-Y%] | [+/-Z%] |
   | Avg. Session Duration | [X] | [+/-Y%] | [+/-Z%] |
   | Bounce Rate | [X]% | [+/-Y%] | [+/-Z%] |
   | Pages per Session | [X] | [+/-Y] | [+/-Z] |
   
   ### Traffic Trend
   
   ```
   [Month 1]  ████████████████████ [X]
   [Month 2]  █████████████████████ [Y]
   [Month 3]  ███████████████████████ [Z]
   [Current]  ████████████████████████ [W]
   ```
   
   ### Traffic by Source
   
   | Channel | Sessions | % of Total | Change |
   |---------|----------|------------|--------|
   | Organic Search | [X] | [Y]% | [+/-Z%] |
   | Direct | [X] | [Y]% | [+/-Z%] |
   | Referral | [X] | [Y]% | [+/-Z%] |
   | Social | [X] | [Y]% | [+/-Z%] |
   
   ### Top Performing Pages
   
   | Page | Sessions | Change | Conversions |
   |------|----------|--------|-------------|
   | [Page 1] | [X] | [+/-Y%] | [Z] |
   | [Page 2] | [X] | [+/-Y%] | [Z] |
   | [Page 3] | [X] | [+/-Y%] | [Z] |
   
   ### Traffic by Device
   
   | Device | Sessions | Change | Conv. Rate |
   |--------|----------|--------|------------|
   | Desktop | [X] ([Y]%) | [+/-Z%] | [%] |
   | Mobile | [X] ([Y]%) | [+/-Z%] | [%] |
   | Tablet | [X] ([Y]%) | [+/-Z%] | [%] |
   ```

4. **Report Keyword Rankings**

   ```markdown
   ## Keyword Ranking Performance
   
   ### Rankings Overview
   
   | Position Range | Keywords | Change | Traffic Impact |
   |----------------|----------|--------|----------------|
   | Position 1 | [X] | [+/-Y] | [Z] sessions |
   | Position 2-3 | [X] | [+/-Y] | [Z] sessions |
   | Position 4-10 | [X] | [+/-Y] | [Z] sessions |
   | Position 11-20 | [X] | [+/-Y] | [Z] sessions |
   | Position 21-50 | [X] | [+/-Y] | [Z] sessions |
   
   ### Ranking Distribution Change
   
   ```
   Last Period:  ▓▓▓▓░░░░░░░░░░░░
   This Period:  ▓▓▓▓▓▓░░░░░░░░░░
                 ↑ More keywords in top positions
   ```
   
   ### Top Ranking Improvements
   
   | Keyword | Previous | Current | Change | Traffic |
   |---------|----------|---------|--------|---------|
   | [kw 1] | [X] | [Y] | +[Z] | [sessions] |
   | [kw 2] | [X] | [Y] | +[Z] | [sessions] |
   | [kw 3] | [X] | [Y] | +[Z] | [sessions] |
   
   ### Rankings That Declined
   
   | Keyword | Previous | Current | Change | Impact | Action |
   |---------|----------|---------|--------|--------|--------|
   | [kw 1] | [X] | [Y] | -[Z] | -[sessions] | [action] |
   
   ### SERP Feature Performance
   
   | Feature | Won | Lost | Opportunities |
   |---------|-----|------|---------------|
   | Featured Snippets | [X] | [Y] | [Z] |
   | People Also Ask | [X] | [Y] | [Z] |
   | Local Pack | [X] | [Y] | [Z] |
   ```

5. **Report GEO/AI Performance**

   ```markdown
   ## GEO (AI Visibility) Performance
   
   ### AI Citation Overview
   
   | Metric | This Period | Last Period | Change |
   |--------|-------------|-------------|--------|
   | Keywords with AI Overview | [X]/[Y] | [X]/[Y] | [+/-Z] |
   | Your AI Citations | [X] | [Y] | [+/-Z%] |
   | Citation Rate | [X]% | [Y]% | [+/-Z%] |
   | Avg Citation Position | [X] | [Y] | [+/-Z] |
   
   ### AI Citation by Topic
   
   | Topic Cluster | Opportunities | Citations | Rate |
   |---------------|---------------|-----------|------|
   | [Topic 1] | [X] | [Y] | [Z]% |
   | [Topic 2] | [X] | [Y] | [Z]% |
   | [Topic 3] | [X] | [Y] | [Z]% |
   
   ### GEO Wins This Period
   
   | Query | Citation Status | Source Page | Impact |
   |-------|-----------------|-------------|--------|
   | [query 1] | 🆕 New citation | [page] | High visibility |
   | [query 2] | ⬆️ Improved position | [page] | Better exposure |
   
   ### GEO Optimization Opportunities
   
   | Query | AI Overview | You Cited? | Gap | Action |
   |-------|-------------|------------|-----|--------|
   | [query] | Yes | No | [gap] | [action] |
   ```

6. **Report Domain Authority (CITE Score)**

   If a CITE domain audit has been run previously (via domain-authority-auditor), include domain authority trends:

   ```markdown
   ## Domain Authority (CITE Score)

   ### CITE Score Summary

   | Metric | This Period | Last Period | Change |
   |--------|-------------|-------------|--------|
   | CITE Score | [X]/100 | [Y]/100 | [+/-Z] |
   | C — Citation | [X]/100 | [Y]/100 | [+/-Z] |
   | I — Identity | [X]/100 | [Y]/100 | [+/-Z] |
   | T — Trust | [X]/100 | [Y]/100 | [+/-Z] |
   | E — Eminence | [X]/100 | [Y]/100 | [+/-Z] |

   **Veto Status**: ✅ No triggers / ⚠️ [item] triggered

   ### Key Changes

   - [Notable improvement or concern 1]
   - [Notable improvement or concern 2]

   _For full 40-item evaluation, run `/seo:audit-domain`_
   ```

   **Note**: If no previous CITE audit exists, note this section as "Not yet evaluated — run domain-authority-auditor for baseline" and skip.

7. **Content Quality (CORE-EEAT Score)**

   If content-quality-auditor has been run on key pages (via `/seo:audit-page`), include content quality metrics:

   ```markdown
   ## Content Quality (CORE-EEAT Score)

   ### Content Quality Summary

   | Metric | Value |
   |--------|-------|
   | Pages Audited | [count] |
   | Average CORE-EEAT Score | [score]/100 ([rating]) |
   | Average GEO Score (CORE) | [score]/100 |
   | Average SEO Score (EEAT) | [score]/100 |
   | Veto Items Triggered | [count] ([item IDs]) |

   ### Dimension Averages Across Audited Pages

   | Dimension | Average Score | Trend |
   |-----------|--------------|-------|
   | C — Contextual Clarity | [score] | [↑/↓/→] |
   | O — Organization | [score] | [↑/↓/→] |
   | R — Referenceability | [score] | [↑/↓/→] |
   | E — Exclusivity | [score] | [↑/↓/→] |
   | Exp — Experience | [score] | [↑/↓/→] |
   | Ept — Expertise | [score] | [↑/↓/→] |
   | A — Authority | [score] | [↑/↓/→] |
   | T — Trust | [score] | [↑/↓/→] |

   ### Key Content Quality Changes

   - [Notable score changes since last report]
   - [Pages with significant quality improvements/declines]

   _For full 80-item evaluation, run `/seo:audit-page` on individual pages. See CORE-EEAT benchmark for methodology._
   ```

   **Note**: If no content quality audit exists, note this section as "Content quality not yet evaluated — run `/seo:audit-page` on key landing pages to establish baseline" and skip.

8. **Report Backlink Performance**

   ```markdown
   ## Backlink Performance
   
   ### Link Profile Summary
   
   | Metric | This Period | Last Period | Change |
   |--------|-------------|-------------|--------|
   | Total Backlinks | [X] | [Y] | [+/-Z] |
   | Referring Domains | [X] | [Y] | [+/-Z] |
   | Domain Authority | [X] | [Y] | [+/-Z] |
   | Avg. Link DA | [X] | [Y] | [+/-Z] |
   
   ### Link Acquisition
   
   | Period | New Links | Lost Links | Net |
   |--------|-----------|------------|-----|
   | Week 1 | [X] | [Y] | [+/-Z] |
   | Week 2 | [X] | [Y] | [+/-Z] |
   | Week 3 | [X] | [Y] | [+/-Z] |
   | Week 4 | [X] | [Y] | [+/-Z] |
   | **Total** | **[X]** | **[Y]** | **[+/-Z]** |
   
   ### Notable New Links
   
   | Source | DA | Type | Value |
   |--------|-----|------|-------|
   | [domain 1] | [DA] | [type] | High |
   | [domain 2] | [DA] | [type] | High |
   
   ### Competitive Position
   
   Your referring domains rank #[X] of [Y] competitors.
   ```

9. **Report Content Performance**

   ```markdown
   ## Content Performance
   
   ### Content Publishing Summary
   
   | Metric | This Period | Last Period | Target |
   |--------|-------------|-------------|--------|
   | New articles published | [X] | [Y] | [Z] |
   | Content updates | [X] | [Y] | [Z] |
   | Total word count | [X] | [Y] | - |
   
   ### Top Performing Content
   
   | Content | Traffic | Rankings | Conversions | Status |
   |---------|---------|----------|-------------|--------|
   | [Title 1] | [X] | [Y] keywords | [Z] | ⭐ Top performer |
   | [Title 2] | [X] | [Y] keywords | [Z] | 📈 Growing |
   | [Title 3] | [X] | [Y] keywords | [Z] | ✅ Stable |
   
   ### Content Needing Attention
   
   | Content | Issue | Traffic Change | Action |
   |---------|-------|----------------|--------|
   | [Title] | [issue] | -[X]% | [action] |
   
   ### Content ROI
   
   | Content Piece | Investment | Traffic Value | ROI |
   |---------------|------------|---------------|-----|
   | [Title 1] | $[X] | $[Y] | [Z]% |
   | [Title 2] | $[X] | $[Y] | [Z]% |
   ```

10. **Generate Recommendations**

   ```markdown
   ## Recommendations & Next Steps
   
   ### Immediate Actions (This Week)
   
   | Priority | Action | Expected Impact | Owner |
   |----------|--------|-----------------|-------|
   | 🔴 High | [Action 1] | [Impact] | [Owner] |
   | 🔴 High | [Action 2] | [Impact] | [Owner] |
   
   ### Short-term (This Month)
   
   | Priority | Action | Expected Impact | Owner |
   |----------|--------|-----------------|-------|
   | 🟡 Medium | [Action 1] | [Impact] | [Owner] |
   | 🟡 Medium | [Action 2] | [Impact] | [Owner] |
   
   ### Long-term (This Quarter)
   
   | Priority | Action | Expected Impact | Owner |
   |----------|--------|-----------------|-------|
   | 🟢 Planned | [Action 1] | [Impact] | [Owner] |
   
   ### Goals for Next Period
   
   | Metric | Current | Target | Action to Achieve |
   |--------|---------|--------|-------------------|
   | Organic Traffic | [X] | [Y] | [action] |
   | Keywords Top 10 | [X] | [Y] | [action] |
   | AI Citations | [X] | [Y] | [action] |
   | Referring Domains | [X] | [Y] | [action] |
   ```

11. **Compile Full Report**

   ```markdown
   # [Company] SEO & GEO Performance Report
   
   ## [Month/Quarter] [Year]
   
   ---
   
   ### Table of Contents
   
   1. Executive Summary
   2. Organic Traffic Performance
   3. Keyword Rankings
   4. GEO/AI Visibility
   5. Domain Authority (CITE Score)
   6. Content Quality (CORE-EEAT Score)
   7. Backlink Analysis
   8. Content Performance
   9. Technical Health
   10. Competitive Landscape
   11. Recommendations
   12. Appendix
   
   ---
   
   [Include all sections from above]
   
   ---
   
   ## Appendix
   
   ### Data Sources
   - ~~analytics (traffic and conversion data)
   - ~~search console (search performance)
   - ~~SEO tool (rankings and backlinks)
   - ~~AI monitor (GEO metrics)

   ### Methodology
   [Explain how metrics were calculated]

   ### Glossary
   - **GEO**: Generative Engine Optimization
   - **DA**: Domain Authority
   - [Additional terms]
   ```

## Validation Checkpoints

### Input Validation
- [ ] Reporting period clearly defined with comparison period
- [ ] All required data sources available or alternatives noted
- [ ] Target audience identified (executive/technical/client)
- [ ] Performance goals and KPIs established for benchmarking

### Output Validation
- [ ] Every metric cites its data source and collection date
- [ ] Trends include period-over-period comparisons
- [ ] Recommendations are specific, prioritized, and actionable
- [ ] Source of each data point clearly stated (~~analytics data, ~~search console data, ~~SEO tool data, user-provided, or estimated)

## Example

**User**: "Create a monthly SEO report for December 2024"

**Output**: [Full report following the structure above with period-specific data and insights]

## Report Templates by Audience

### Executive Report (1 page)

Focus on: Business impact, ROI, top-line metrics, key recommendations

### Marketing Team Report (3-5 pages)

Focus on: Detailed metrics, content performance, campaign results

### Technical SEO Report (5-10 pages)

Focus on: Crawl data, technical issues, detailed rankings, backlink analysis

### Client Report (2-3 pages)

Focus on: Progress against goals, wins, clear recommendations

## Tips for Success

1. **Lead with insights** - Start with what matters, not raw data
2. **Visualize data** - Charts and graphs improve comprehension
3. **Compare periods** - Context makes data meaningful
4. **Include actions** - Every report should drive decisions
5. **Customize for audience** - Executives need different info than technical teams
6. **Track GEO metrics** - AI visibility is increasingly important

## Related Skills

- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) — Include CORE-EEAT scores as page-level content quality KPIs
- [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/) — Include CITE score as a domain-level KPI in periodic reports
- [rank-tracker](../rank-tracker/) — Detailed ranking data
- [backlink-analyzer](../backlink-analyzer/) — Link profile data
- [alert-manager](../alert-manager/) — Set up report triggers
- [serp-analysis](../../research/serp-analysis/) — SERP composition data
- [memory-management](../../cross-cutting/memory-management/) — Archive reports in project memory

