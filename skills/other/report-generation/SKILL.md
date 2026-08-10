---
name: report-generation
description: Generate professional reports — sprint retrospectives, financial summaries, analytics dashboards, and incident postmortems — from structured data with templates, charts, and multi-format output. Use when the user requests report generation or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Report Generation

This skill enables an AI agent to produce polished, data-driven reports from structured input. The agent accepts data in JSON, CSV, or API response format, applies a report template, generates narrative insights alongside tables and chart specifications, and outputs the final report in Markdown, HTML, or PDF. It supports common report types including sprint retrospectives, financial summaries, analytics dashboards, and incident postmortems.

## Workflow

1. **Ingest and validate the source data.** Accept the input data file or payload in JSON, CSV, YAML, or raw API response format. Validate the schema — check for required fields, correct data types, missing values, and outliers. If the data is incomplete (e.g., a sprint retro JSON missing the velocity field), flag the gap and either infer a default, request the missing value, or note the omission in the report. Normalize date formats, currency symbols, and units for consistency.

2. **Select or customize the report template.** Match the data to a report template based on the report type specified by the user. Built-in templates include: `sprint_retrospective`, `financial_summary`, `analytics_dashboard`, `incident_postmortem`, and `weekly_status`. Each template defines the section order, required data mappings, chart types, and tone (analytical for financial reports, constructive for retros, urgent for postmortems). Users can customize templates by overriding sections, adding fields, or changing the visual theme.

3. **Compute metrics and generate insights.** Derive computed metrics from the raw data — percentage changes, averages, rankings, trend directions, and anomaly flags. For a sprint retro, calculate velocity variance and commitment accuracy. For an analytics report, compute conversion rates and segment-level breakdowns. Then generate narrative insights: not just "conversion rate was 3.2%" but "conversion rate dropped 0.8pp from last period, driven primarily by a 15% decline in mobile traffic."

4. **Populate the report structure.** Fill the template sections with the computed metrics, narrative insights, and formatted data tables. Generate chart specifications (bar, line, pie, or table) for each visualization slot in the template. Use Markdown table syntax for inline tables and a chart spec format (e.g., Mermaid, Vega-Lite, or Chart.js JSON) for visual charts. Add section headers, executive summary, and any appendices.

5. **Format and render the output.** Produce the final report in the requested format. For Markdown, output a clean `.md` file with tables and chart code blocks. For HTML, wrap the Markdown output in a styled template with CSS for print-friendly rendering. For PDF, convert the HTML version using a headless browser or a tool like Puppeteer or WeasyPrint. Ensure charts render correctly in all formats and that tables don't break across pages in PDF.

6. **Review and finalize.** Run a quality check: verify all data points in the report trace back to the source data, ensure no template variables remain unresolved (e.g., `{{quarter}}`), confirm that insights are supported by the numbers, and check that the report length matches the expected range for its type. Deliver the report with a brief summary of what was generated.

## Usage

Provide the agent with the report type, source data, any customization preferences, and the desired output format. The agent returns a complete, formatted report.

**Prompt format:**

~~~
Generate a [report type] report.
Data source: [path to JSON/CSV file, or inline data]
Time period: [date range or sprint number]
Template: [built-in template name or "custom"]
Output format: [markdown / html / pdf]
~~~

## Examples

### Example 1: Sprint Retrospective Report from Structured Data

**Input data (JSON):**

~~~json
{
  "sprint": {
    "number": 14,
    "start_date": "2026-01-27",
    "end_date": "2026-02-07",
    "goal": "Ship checkout flow redesign and analytics instrumentation"
  },
  "velocity": {
    "committed": 34,
    "completed": 29,
    "previous_sprints": [31, 28, 33, 30]
  },
  "stories": {
    "total": 12,
    "completed": 10,
    "carried_over": 2,
    "carried_over_items": [
      "CHECKOUT-142: Edge case handling for international addresses",
      "ANALYTICS-89: Cross-domain tracking for subdomain events"
    ]
  },
  "what_went_well": [
    "Checkout redesign shipped 2 days early",
    "Zero P1 bugs in production release",
    "Effective pairing sessions between frontend and backend teams"
  ],
  "what_could_improve": [
    "Sprint scope increased mid-sprint with 3 unplanned tickets",
    "QA bottleneck on Thursday caused idle time for 2 developers",
    "Standup meetings ran over 15 minutes on 3 of 10 days"
  ],
  "action_items": [
    { "owner": "Priya", "action": "Add a mid-sprint scope freeze policy" },
    { "owner": "James", "action": "Schedule a dedicated QA window on Wednesdays" },
    { "owner": "Dana", "action": "Timekeeper rotation for standups" }
  ]
}
~~~

**Output (Markdown report):**

~~~markdown
# Sprint 14 Retrospective

**Sprint dates:** January 27 – February 7, 2026
**Sprint goal:** Ship checkout flow redesign and analytics instrumentation

---

## Executive Summary

Sprint 14 delivered 85% of committed story points (29 of 34), slightly below
the team's rolling average velocity of 30.5. The primary sprint goal was
partially met: the checkout redesign shipped ahead of schedule, but two
analytics stories carried over due to mid-sprint scope changes and a QA
bottleneck. Zero P1 bugs were introduced, reflecting strong code quality.

## Velocity

| Metric               | Sprint 14 | 4-Sprint Average |
|----------------------|-----------|------------------|
| Committed            | 34 pts    | 31.0 pts         |
| Completed            | 29 pts    | 30.5 pts         |
| Commitment accuracy  | 85%       | 98%              |

The team over-committed by 3 points relative to the historical average.
The shortfall is attributable to 3 unplanned tickets added mid-sprint,
which consumed approximately 5 story points of capacity.

## Story Completion

- **Completed:** 10 of 12 stories (83%)
- **Carried over:** 2 stories
  - CHECKOUT-142: Edge case handling for international addresses
  - ANALYTICS-89: Cross-domain tracking for subdomain events

Both carried-over stories are estimated at 2-3 points each and will be
prioritized at the top of Sprint 15.

## What Went Well

- Checkout redesign shipped 2 days ahead of the sprint end date, allowing
  extra time for integration testing.
- Zero P1 bugs in the production release — the team's pairing sessions
  caught issues early in development.
- Cross-functional pairing sessions were cited by 3 team members as the
  highlight of the sprint.

## What Could Improve

- **Mid-sprint scope creep:** 3 unplanned tickets were added after sprint
  planning, consuming capacity and contributing to the 2 carried-over stories.
- **QA bottleneck:** All completed stories landed in QA on Thursday, creating
  a pileup that left 2 developers idle on Friday morning.
- **Standup duration:** Standups exceeded 15 minutes on 3 of 10 days.

## Action Items

| Owner | Action                                           | Target Date |
|-------|--------------------------------------------------|-------------|
| Priya | Add a mid-sprint scope freeze policy             | Feb 10      |
| James | Schedule a dedicated QA window on Wednesdays     | Feb 10      |
| Dana  | Implement timekeeper rotation for standups       | Feb 10      |

---

*Report generated from sprint data. Source: sprint-14-retro.json*
~~~

### Example 2: Analytics Report with Insights and Recommendations

**Input:**

~~~
Generate an analytics report for the marketing website.
Data source: /data/website-analytics-jan-2026.json
Time period: January 2026
Output format: markdown
~~~

**Output:**

~~~markdown
# Website Analytics Report — January 2026

**Reporting period:** January 1–31, 2026
**Compared to:** December 2025

---

## Executive Summary

Website traffic increased 12% month-over-month to 284,000 sessions, driven
primarily by organic search growth (+18%). However, overall conversion rate
declined from 4.0% to 3.2%, with the sharpest drop on mobile devices. The
pricing page continues to be the highest-converting entry point, while the
blog showed strong traffic growth but low conversion intent.

## Traffic Overview

| Metric             | January 2026 | December 2025 | Change  |
|--------------------|-------------|---------------|---------|
| Total sessions     | 284,000     | 253,500       | +12.0%  |
| Unique visitors    | 198,600     | 179,400       | +10.7%  |
| Pages per session  | 3.2         | 3.4           | -5.9%   |
| Avg session dur.   | 2m 48s      | 3m 05s        | -9.2%   |
| Bounce rate        | 42%         | 38%           | +4pp    |

## Traffic by Channel

| Channel        | Sessions | Share | MoM Change |
|----------------|----------|-------|------------|
| Organic Search | 142,000  | 50%   | +18.3%     |
| Direct         | 62,500   | 22%   | +5.1%      |
| Paid Search    | 39,800   | 14%   | +8.7%      |
| Social         | 25,600   | 9%    | +2.3%      |
| Referral       | 14,100   | 5%    | -3.8%      |

**Insight:** Organic search growth (+18.3%) was the primary traffic driver,
likely attributable to the 6 new blog posts published in January. However,
the drop in pages-per-session and increased bounce rate suggest this new
organic traffic has lower engagement intent than existing visitors.

## Conversion Funnel

| Stage                  | Visitors | Rate   | MoM Change |
|------------------------|----------|--------|------------|
| Homepage to Pricing    | 84,200   | 29.6%  | -1.2pp     |
| Pricing to Signup      | 15,400   | 18.3%  | -2.1pp     |
| Signup to Activation   | 9,100    | 59.1%  | +0.8pp     |
| **Overall conversion** | **9,100**| **3.2%** | **-0.8pp** |

**Insight:** The conversion drop is concentrated in the Pricing to Signup
step (-2.1pp). A/B test data shows the new pricing page variant (launched
Jan 15) underperforms the control by 1.8pp. Recommendation: revert to the
control pricing page and redesign the variant.

## Recommendations

1. **Revert the pricing page A/B test.** The new variant is underperforming
   by 1.8pp on the key Pricing to Signup conversion step.
2. **Add conversion-intent CTAs to blog posts.** The 18% organic traffic
   growth is not converting. Embed contextual product CTAs within blog
   content to capture high-intent readers.
3. **Investigate mobile conversion drop.** Mobile sessions grew 15% but
   mobile conversion fell 1.2pp. Audit the mobile signup flow for UX
   friction, particularly form field usability and page load speed.
4. **Double down on organic content.** The SEO investment is paying off
   in traffic. Publish 8 posts in February targeting mid-funnel keywords
   with stronger commercial intent.

---

*Report generated from website-analytics-jan-2026.json. Data: Google Analytics.*
~~~

## Best Practices

- **Lead with the executive summary.** Decision-makers read the first paragraph and skim the rest. Put the most important finding and recommendation at the top, not buried in the middle of the report.
- **Show comparisons, not just numbers.** Raw metrics lack context. Always include a comparison baseline — previous period, target, industry benchmark, or historical average — so the reader knows whether a number is good or bad.
- **Generate narrative insights, not just data dumps.** A table of numbers requires the reader to do analytical work. Pair every data table with a sentence explaining what the data means and why it matters.
- **Use consistent formatting throughout.** Align table columns, use the same date format everywhere, and maintain a uniform heading hierarchy. Inconsistent formatting erodes trust in the data.
- **Keep reports scannable.** Use section headers, bullet points, bold key numbers, and whitespace generously. A wall of prose in a report is as ineffective as a wall of text in an email.
- **Cite your data sources.** Include a footer or appendix noting where the data came from, when it was pulled, and any filters or exclusions applied. This makes the report auditable and reproducible.

## Edge Cases

- **Incomplete or missing data fields.** When the source data is missing expected fields, note the gap explicitly in the report (e.g., "Velocity data unavailable — commitment accuracy not calculated") rather than silently omitting the section or inventing numbers.
- **Data with outliers or anomalies.** Flag unusual data points (e.g., a 10x traffic spike from a bot attack) and note whether they were included or excluded from aggregate calculations.
- **Multiple data sources that conflict.** When two sources disagree (e.g., CRM shows 120 deals closed, finance shows 118), note the discrepancy, state which source was used, and recommend a reconciliation.
- **Very large datasets.** For data files with thousands of rows, summarize at the appropriate granularity (daily, weekly, by segment) rather than listing every row. Offer to generate a detailed appendix on request.
- **Sensitive financial or personnel data.** Apply access controls to the generated report. Redact individual compensation figures in team-level reports. Flag reports containing PII or financial data for restricted distribution.
