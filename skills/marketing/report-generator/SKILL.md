---
name: report-generator
description: 'Use when the user asks to "create a campaign report", "build an executive summary", or "deliver client results"; produces audience-tailored influencer marketing reports (executive, client, internal team) with data tables, narrative, key learnings, and recommendations. Not for raw metric computation — use performance-analyzer.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Activate after a campaign or reporting period ends and the user needs a written report for a specific stakeholder. Triggers include post-campaign wrap-ups, executive or board summaries, client-facing results decks, internal team retrospectives, and monthly or quarterly performance reports. Pick this when the inputs are already-computed metrics that need structure, narrative, and recommendations for a named audience."
argument-hint: "<campaign name> [audience: executive|client|team|board]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Track
---

# Report Generator

This skill helps you create professional influencer marketing reports that tell the story of your campaign performance. It adapts content and depth based on the audience.

## Quick Start

Shortest invocation:

```
Create a campaign report for [campaign name] for [audience: executive/client/team]
```

Common scenario:

```
Generate an executive summary for our Q3 influencer campaigns
```

## Skill Contract

- **Reads**: campaign name, reporting period, target audience, and computed metrics (reach, engagement, conversions, spend, revenue, ROI/ROAS, per-influencer results). Prior outputs from `performance-analyzer` and `roi-calculator` if available.
- **Writes**: a finished report in the audience-appropriate template, saved to `memory/influencer/report-generator/YYYY-MM-DD-<topic>.md`.
- **Promotes**: durable verdicts (final ROI/ROAS, top performers, renew/drop calls, headline learnings) to `memory/hot-cache.md`.
- **Done when**:
  1. The report matches the requested audience template (executive, client, team, or board).
  2. Every metric is paired with context (target, benchmark, or prior period).
  3. The report ends with concrete recommendations and, where relevant, action items.
- **Primary next skill**: [content-quality-auditor](../../cross-cutting/content-quality-auditor/SKILL.md)

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family ships Tier 1: every step works with no live integration. Give the skill the campaign metrics directly and it builds the report from your inputs.

Optional connectors that can pre-fill data where available:

- `~~social platform analytics` — reach, impressions, engagement, video views per post
- `~~influencer database` — creator handles, tiers, fees, audience demographics
- `~~analytics` — link clicks, conversions, attributed revenue
- `~~CRM` — new-customer counts and downstream revenue

Without any of these, the skill asks you for the numbers and proceeds. See [CONNECTORS.md](../../CONNECTORS.md) for the free/keyless data recipe per category.

## Instructions

When a user requests a report:

1. **Determine Report Parameters**

   ```markdown
   ### Report Parameters

   **Report Type**: [Post-campaign/Monthly/Quarterly/Annual]
   **Campaign(s)**: [campaign name(s)]
   **Period**: [dates covered]
   **Audience**: [Executive/Client/Team/Board]

   **Audience Needs**:
   | Audience | Focus | Detail Level | Key Questions |
   |----------|-------|--------------|---------------|
   | Executive | ROI, Strategy | High-level | "Was it worth it?" |
   | Client | Results, Value | Medium | "What did I get?" |
   | Team | Learnings, Optimization | Detailed | "What can we improve?" |
   | Board | Business Impact | Summary | "How does this grow the business?" |
   ```

2. **Executive Report Template**

   ```markdown
   # [Campaign Name] Executive Report

   **Prepared for**: [Executive/Leadership]
   **Date**: [Date]
   **Period**: [Campaign Dates]

   ---

   ## Executive Summary

   [2-3 sentences summarizing the campaign and key outcome]

   **Bottom Line**: [One-line verdict - e.g., "Campaign exceeded targets, achieving 3.2x ROAS"]

   ### Key Results at a Glance

   | Metric | Target | Actual | Status |
   |--------|--------|--------|--------|
   | ROI | [X]% | [X]% | ✅/❌ |
   | Revenue | $[X] | $[X] | ✅/❌ |
   | Reach | [X]M | [X]M | ✅/❌ |
   | New Customers | [X] | [X] | ✅/❌ |

   ---

   ## Investment & Return

   | | Amount |
   |---------|--------|
   | **Total Investment** | $[X] |
   | **Revenue Generated** | $[X] |
   | **Net Return** | $[X] |
   | **ROI** | **[X]%** |

   ---

   ## Strategic Highlights

   ### What Worked
   1. [Key success with impact]
   2. [Key success with impact]

   ### Opportunities Identified
   1. [Opportunity for future]
   2. [Opportunity for future]

   ---

   ## Recommendation

   [1-2 sentences on recommended next steps/future investment]

   ---

   *Detailed analysis available in appendix*
   ```

3. **Client Report Template**

   ```markdown
   # [Campaign Name] Performance Report

   **Client**: [Client Name]
   **Campaign**: [Campaign Name]
   **Period**: [Dates]
   **Prepared by**: [Your Name/Agency]

   ---

   ## Campaign Overview

   ### Objectives
   [What we set out to achieve]

   ### Strategy
   [Brief summary of approach]

   ### Execution
   - **Influencers**: [X] creators across [platforms]
   - **Content**: [X] pieces created
   - **Timeline**: [X] weeks

   ---

   ## Performance Summary

   ### Overall Results

   | Metric | Goal | Delivered | Performance |
   |--------|------|-----------|-------------|
   | Total Reach | [X] | [X] | [+/-X%] vs. goal |
   | Impressions | [X] | [X] | [+/-X%] vs. goal |
   | Engagements | [X] | [X] | [+/-X%] vs. goal |
   | Engagement Rate | [X]% | [X]% | [+/-X%] vs. goal |
   | Link Clicks | [X] | [X] | [+/-X%] vs. goal |
   | Conversions | [X] | [X] | [+/-X%] vs. goal |

   ### Return on Investment

   | Investment | Return |
   |------------|--------|
   | Total Spend: $[X] | Revenue: $[X] |
   | | **ROAS: [X]:1** |

   ---

   ## Content Performance

   ### Top Performing Content

   **#1: @[handle] - [Platform]**

   [Screenshot/embed]

   - Reach: [X]
   - Engagement Rate: [X]%
   - Why it worked: [Brief analysis]

   **#2: @[handle] - [Platform]**

   [Screenshot/embed]

   - Reach: [X]
   - Engagement Rate: [X]%
   - Why it worked: [Brief analysis]

   ---

   ## Influencer Performance

   ### Partner Summary

   | Creator | Platform | Reach | ER | Conversions |
   |---------|----------|-------|-------|-------------|
   | @[handle1] | [platform] | [X] | [%] | [X] |
   | @[handle2] | [platform] | [X] | [%] | [X] |
   | @[handle3] | [platform] | [X] | [%] | [X] |

   ### Top Performers

   1. **@[handle]**: [Why they excelled]
   2. **@[handle]**: [Why they excelled]

   ---

   ## Audience Insights

   ### Who We Reached

   [Demographics, interests, behaviors observed]

   ### Sentiment & Feedback

   **Positive Themes**:
   - [Theme 1]
   - [Theme 2]

   **Questions/Feedback**:
   - [Common question]
   - [Common feedback]

   ---

   ## Key Learnings

   ### What Worked Well

   1. **[Learning 1]**: [Explanation]
   2. **[Learning 2]**: [Explanation]

   ### Opportunities for Future

   1. **[Opportunity 1]**: [Recommendation]
   2. **[Opportunity 2]**: [Recommendation]

   ---

   ## Recommendations

   Based on campaign results, we recommend:

   1. [Recommendation 1]
   2. [Recommendation 2]
   3. [Recommendation 3]

   ---

   ## Next Steps

   - [Next step 1]
   - [Next step 2]
   - [Proposed timeline]

   ---

   ## Appendix

   - Full influencer performance data
   - Content gallery
   - Detailed analytics

   ---

   *Thank you for your partnership. Questions? Contact [Name] at [Email]*
   ```

4. **Internal Team Report Template**

   ```markdown
   # [Campaign] Internal Performance Report

   **Date**: [Date]
   **Author**: [Name]
   **Distribution**: [Team/Department]

   ---

   ## TL;DR

   [3-5 bullet points summarizing key outcomes and learnings]

   ---

   ## Campaign Overview

   ### Objectives & KPIs

   | Objective | KPI | Target | Result | Status |
   |-----------|-----|--------|--------|--------|
   | [Objective 1] | [KPI] | [Target] | [Result] | ✅/❌ |
   | [Objective 2] | [KPI] | [Target] | [Result] | ✅/❌ |

   ### Campaign Details

   - **Duration**: [X] weeks ([dates])
   - **Budget**: $[X]
   - **Influencers**: [X] total ([breakdown by tier])
   - **Platforms**: [platforms]
   - **Content pieces**: [X]

   ---

   ## Detailed Performance Analysis

   ### Overall Metrics

   | Metric | Result | Target | vs. Target | vs. Benchmark |
   |--------|--------|--------|------------|---------------|
   | Reach | [X] | [X] | [+/-X%] | [+/-X%] |
   | Impressions | [X] | [X] | [+/-X%] | [+/-X%] |
   | Engagements | [X] | [X] | [+/-X%] | [+/-X%] |
   | ER | [X]% | [X]% | [+/-X%] | [+/-X%] |
   | Video Views | [X] | [X] | [+/-X%] | [+/-X%] |
   | Clicks | [X] | [X] | [+/-X%] | [+/-X%] |
   | Conversions | [X] | [X] | [+/-X%] | [+/-X%] |
   | Revenue | $[X] | $[X] | [+/-X%] | N/A |
   | ROAS | [X]:1 | [X]:1 | [+/-X%] | [+/-X%] |

   ### Platform Breakdown

   [Detailed platform-by-platform analysis]

   ### Influencer Analysis

   #### Full Roster Performance

   | Rank | Creator | Platform | Fee | Reach | ER | Conversions | ROAS | Recommendation |
   |------|---------|----------|-----|-------|-------|-------------|------|----------------|
   | 1 | @[handle] | [platform] | $[X] | [X] | [%] | [X] | [X]:1 | Renew |
   | 2 | @[handle] | [platform] | $[X] | [X] | [%] | [X] | [X]:1 | Renew |
   | ... | ... | ... | ... | ... | ... | ... | ... | ... |

   #### Performance Insights

   **Top Performers**: [Analysis of why they succeeded]
   **Underperformers**: [Analysis of why they underperformed]
   **Surprises**: [Any unexpected results]

   ### Content Analysis

   #### By Format

   | Format | Pieces | Avg Reach | Avg ER | Best Performer |
   |--------|--------|-----------|--------|----------------|
   | [Format 1] | [#] | [X] | [%] | @[handle] |
   | [Format 2] | [#] | [X] | [%] | @[handle] |

   #### By Theme

   | Theme | Pieces | Avg ER | Conversions |
   |-------|--------|--------|-------------|
   | [Theme 1] | [#] | [%] | [X] |
   | [Theme 2] | [#] | [%] | [X] |

   #### Content Learnings

   - [Learning about what content worked]
   - [Learning about messaging]
   - [Learning about creative approach]

   ---

   ## Cost Analysis

   ### Budget vs. Actual

   | Category | Budgeted | Actual | Variance |
   |----------|----------|--------|----------|
   | Influencer fees | $[X] | $[X] | [+/-$X] |
   | Product/Gifting | $[X] | $[X] | [+/-$X] |
   | Production | $[X] | $[X] | [+/-$X] |
   | Amplification | $[X] | $[X] | [+/-$X] |
   | **Total** | **$[X]** | **$[X]** | **[+/-$X]** |

   ### Efficiency Metrics

   | Metric | Result | Target | Industry Avg |
   |--------|--------|--------|--------------|
   | CPM | $[X] | $[X] | $[X] |
   | CPE | $[X] | $[X] | $[X] |
   | CPC | $[X] | $[X] | $[X] |
   | CPA | $[X] | $[X] | $[X] |

   ---

   ## Learnings & Recommendations

   ### Key Learnings

   | Learning | Evidence | Implication |
   |----------|----------|-------------|
   | [Learning 1] | [Data/example] | [What to do with this] |
   | [Learning 2] | [Data/example] | [What to do with this] |
   | [Learning 3] | [Data/example] | [What to do with this] |

   ### What Worked Well (Do More)

   1. [Tactic/approach]: [Why it worked]
   2. [Tactic/approach]: [Why it worked]

   ### What Didn't Work (Do Less/Differently)

   1. [Tactic/approach]: [Why it didn't work]
   2. [Tactic/approach]: [Why it didn't work]

   ### Recommendations for Future Campaigns

   | Area | Current Approach | Recommended Change | Expected Impact |
   |------|------------------|-------------------|-----------------|
   | [Area 1] | [Current] | [Recommended] | [Impact] |
   | [Area 2] | [Current] | [Recommended] | [Impact] |

   ---

   ## Action Items

   | Action | Owner | Deadline | Status |
   |--------|-------|----------|--------|
   | [Action 1] | [Name] | [Date] | ⬜ |
   | [Action 2] | [Name] | [Date] | ⬜ |
   | [Action 3] | [Name] | [Date] | ⬜ |

   ---

   ## Appendix

   - Raw data exports
   - All content screenshots
   - Full influencer contracts summary
   - Sentiment analysis details

   ---
   ```

5. **Visualization Recommendations**

   ```markdown
   ## Recommended Visualizations

   ### For Executive Reports

   | Data | Visualization | Why |
   |------|---------------|-----|
   | ROI/ROAS | Large number callout | Immediate impact |
   | Goal vs. Actual | Horizontal bar chart | Easy comparison |
   | Budget allocation | Pie/donut chart | Distribution clarity |
   | Timeline performance | Line chart | Show momentum |

   ### For Client Reports

   | Data | Visualization | Why |
   |------|---------------|-----|
   | Overall results | Dashboard-style metrics | Professional look |
   | Content examples | Screenshots with metrics | Tangible deliverables |
   | Influencer performance | Table with icons | Detailed but scannable |
   | Engagement breakdown | Stacked bar | Show composition |

   ### For Team Reports

   | Data | Visualization | Why |
   |------|---------------|-----|
   | Full metrics | Detailed tables | Complete data |
   | Trends | Line charts over time | Pattern recognition |
   | Comparisons | Side-by-side bars | Easy comparison |
   | Distribution | Histograms | Understand spread |
   ```

6. **Report Writing Best Practices**

   ```markdown
   ## Report Writing Guidelines

   ### Structure Principles

   1. **Lead with outcomes**: Start with results, not methodology
   2. **Answer "so what?"**: Every metric needs context
   3. **Use progressive disclosure**: Summary → Details → Appendix
   4. **Balance positive and constructive**: Celebrate wins, acknowledge learnings

   ### Writing Tips

   **Instead of**: "We achieved 2.4M reach"
   **Write**: "We reached 2.4M people, 20% above our target, primarily through TikTok content that resonated with Gen Z audiences"

   **Instead of**: "Engagement rate was 4.2%"
   **Write**: "Our 4.2% engagement rate outperformed the industry average of 3.1%, indicating content strongly resonated with our target audience"

   ### Narrative Arc

   1. **Setup**: What we set out to do
   2. **Execution**: What we did
   3. **Results**: What happened
   4. **Analysis**: What it means
   5. **Recommendations**: What to do next
   ```

## Example

**User**: "Create an executive report for our holiday campaign: $50K spend, $165K revenue, 3.5M reach across 15 influencers"

**Output**:

```markdown
# Holiday Campaign 2024: Executive Summary

## Bottom Line: Campaign Exceeded All Targets ✅

**ROI: 230%** | **ROAS: 3.3:1** | **Revenue: $165,000**

### Investment & Return

| | |
|---|---|
| Investment | $50,000 |
| Revenue | $165,000 |
| **Net Return** | **$115,000** |

### Key Results

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Revenue | $100K | $165K | ✅ +65% |
| ROAS | 2:1 | 3.3:1 | ✅ +65% |
| Reach | 2M | 3.5M | ✅ +75% |

### Strategic Takeaways

1. **TikTok drove 60% of conversions** - Platform investment should increase
2. **Micro-influencers outperformed macro** - Better ROI at lower individual cost
3. **Product demo content converted 2x vs. lifestyle** - Inform future briefs

### Recommendation

Increase Q1 influencer budget by 25% with focus on TikTok micro-influencers and product-demo content strategy.

---
*Full analysis available upon request*
```

## Tips for Better Reports

1. **Know your audience** - Executive wants ROI, team wants details
2. **Lead with the headline** - Don't bury the lede
3. **Visualize key data** - Charts > tables for executives
4. **Provide context** - Benchmarks make numbers meaningful
5. **End with action** - Reports should drive decisions

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and handoff format
- [state-model.md](../../references/state-model.md) — memory tiers and save-path convention
- [CONNECTORS.md](../../CONNECTORS.md) — free/keyless data recipes per connector category
- [performance-analyzer](../performance-analyzer/SKILL.md) — generates the metrics this report consumes
- [roi-calculator](../roi-calculator/SKILL.md) — supplies ROI/ROAS figures
- [campaign-planner](../../plan/campaign-planner/SKILL.md) — original plan to compare results against
- [content-amplifier](../../convert/content-amplifier/SKILL.md) — amplification results to report on
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/SKILL.md) — quality gate for the report itself

## Next Best Skill

**Primary**: [content-quality-auditor](../../cross-cutting/content-quality-auditor/SKILL.md) — run the finished report through the publish-readiness gate before it goes to a stakeholder.

**Alternates (same Track phase / IMPACT family)**:

- [performance-analyzer](../performance-analyzer/SKILL.md) — if the report exposes data gaps, re-analyze before re-reporting.
- [roi-calculator](../roi-calculator/SKILL.md) — recompute return figures if the financial inputs changed.

**Termination note** (visited-set): if a recommended skill has already been invoked this session, stop and report the chain as complete instead of re-running it. Honor a max chain depth of 3 hops to avoid loops.

## Related Skills

- [performance-analyzer](../performance-analyzer/SKILL.md) - Generate data for reports
- [roi-calculator](../roi-calculator/SKILL.md) - Calculate ROI figures
- [campaign-planner](../../plan/campaign-planner/SKILL.md) - Reference original plans
- [content-amplifier](../../convert/content-amplifier/SKILL.md) - Report on amplification results
