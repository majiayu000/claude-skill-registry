---
name: analytics-reporting
description: Generate comprehensive marketing analytics reports by collecting KPIs, analyzing trends, and delivering actionable insights with attribution modeling and funnel analysis. Use when the user requests analytics reporting or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Analytics Reporting

This skill enables an AI agent to generate detailed marketing analytics reports that go beyond raw numbers to deliver actionable insights. The agent collects data across traffic, engagement, conversion, and revenue metrics, applies attribution models to understand channel contribution, performs funnel and cohort analysis, and produces executive-ready reports with clear recommendations. The output helps marketing teams make data-driven decisions about budget allocation, campaign optimization, and strategy shifts.

## Workflow

1. **Define reporting scope and KPIs.** Clarify the report type (monthly overview, campaign-specific, channel deep-dive) and time period. Establish the primary KPIs to track: traffic metrics (sessions, unique visitors, pageviews), engagement metrics (bounce rate, time on page, pages per session), conversion metrics (conversion rate, leads generated, cost per acquisition), and revenue metrics (customer lifetime value, return on ad spend, marketing-attributed revenue).

2. **Collect data from all sources.** Pull data from web analytics (Google Analytics, Plausible), search console (impressions, clicks, average position), advertising platforms (Google Ads, Meta Ads, LinkedIn Ads), email marketing (Mailchimp, SendGrid), CRM (HubSpot, Salesforce), and social media analytics (native platform insights). Normalize date ranges and metric definitions across sources to ensure comparability.

3. **Analyze trends and identify patterns.** Compare current period metrics against previous period and year-over-year baselines. Calculate growth rates, identify statistically significant changes, and flag anomalies (traffic spikes from viral content, drops from algorithm updates or site outages). Segment data by channel, device, geography, and user cohort to uncover hidden patterns.

4. **Apply attribution modeling.** Move beyond last-click attribution to understand the full customer journey. Apply multi-touch models — linear (equal credit), time-decay (more credit to recent touchpoints), or data-driven (algorithmic) — to evaluate how each channel contributes to conversions. This prevents over-investing in bottom-funnel channels while starving the awareness channels that feed the pipeline.

5. **Perform funnel and cohort analysis.** Map the conversion funnel from first visit to purchase or signup. Calculate drop-off rates at each stage: landing page → lead form → MQL → SQL → customer. Identify the highest-friction stages and recommend tests to improve them. Run cohort analysis to understand retention — do users acquired from organic search retain better than those from paid ads after 30, 60, and 90 days?

6. **Generate the report with visualizations and recommendations.** Structure the report with an executive summary, channel-by-channel breakdown, top-performing content, funnel analysis, and a prioritized recommendation section. Include tables, trend charts, and comparison visualizations. End every section with a "So what?" — the specific action the team should take based on the data.

## Usage

Provide the agent with the reporting period, data sources or raw data exports, and which KPIs matter most to your team. The agent returns a structured analytics report with insights and recommendations.

**Prompt:** `Generate a January 2025 marketing analytics report for our e-commerce site. Data sources: Google Analytics, Google Ads, and Shopify. Focus on traffic trends, conversion rate by channel, and ROAS.`

## Examples

### Example 1: Monthly Marketing Analytics Report

**Request:** Generate the February 2025 monthly report for `acmesaas.com`.

**Executive Summary:**

| Metric | Feb 2025 | Jan 2025 | MoM Change | YoY Change |
|--------|----------|----------|------------|------------|
| Total Sessions | 84,200 | 78,500 | +7.3% | +22.1% |
| Unique Visitors | 61,400 | 57,800 | +6.2% | +18.9% |
| Bounce Rate | 42.1% | 45.3% | -3.2 pts | -5.8 pts |
| Avg Session Duration | 3:42 | 3:18 | +12.1% | +8.4% |
| Lead Form Submissions | 1,240 | 1,080 | +14.8% | +31.2% |
| Trial Signups | 386 | 342 | +12.9% | +28.7% |
| CAC (blended) | $127 | $143 | -11.2% | -19.1% |
| Marketing-Attributed Revenue | $94,200 | $81,600 | +15.4% | +41.3% |

**Channel Breakdown:**

| Channel | Sessions | Conv. Rate | Leads | Cost | CAC |
|---------|----------|------------|-------|------|-----|
| Organic Search | 38,100 | 2.1% | 800 | $0 | $0 |
| Paid Search (Google) | 18,400 | 1.8% | 331 | $24,800 | $74.92 |
| LinkedIn Ads | 8,200 | 1.4% | 115 | $18,600 | $161.74 |
| Email Marketing | 12,600 | 3.2% | 403 | $1,200 | $2.98 |
| Direct / Referral | 6,900 | 0.9% | 62 | $0 | $0 |

**Key Insights:**
1. **Organic search is the efficiency leader.** It delivered 65% of all leads at zero marginal cost. The 22% YoY session growth reflects SEO investments from Q3–Q4 2024 compounding.
2. **Email marketing has the highest conversion rate at 3.2%.** The new onboarding drip sequence launched in January drove a 40% lift in email-sourced trial signups.
3. **LinkedIn Ads CAC is elevated at $161.74.** However, LinkedIn leads convert to paid customers at 2.4x the rate of Google Ads leads. When measured by LTV:CAC ratio, LinkedIn is more efficient.
4. **Bounce rate improved 3.2 points MoM.** This correlates with the homepage redesign deployed February 3rd, which added social proof and clearer CTAs above the fold.

**Recommendations:**
- Increase organic content investment: publish 2 additional SEO-targeted posts per week focused on high-intent commercial keywords identified in the January keyword gap analysis.
- Scale LinkedIn Ads budget by 20% but narrow targeting to Director+ titles at companies with 200–2,000 employees to reduce CAC.
- A/B test the trial signup page — current 12.9% growth is strong but the 1.8% paid search conversion rate suggests friction on the landing page.

### Example 2: Campaign Performance Analysis

**Request:** Analyze the "Q1 Product Launch" paid campaign running Jan 15–Feb 28 across Google Ads and Meta Ads.

**Campaign Summary:**

| Metric | Google Ads | Meta Ads | Combined |
|--------|-----------|----------|----------|
| Impressions | 1,240,000 | 2,860,000 | 4,100,000 |
| Clicks | 31,000 | 22,880 | 53,880 |
| CTR | 2.5% | 0.8% | 1.3% |
| Cost | $18,600 | $14,200 | $32,800 |
| CPC | $0.60 | $0.62 | $0.61 |
| Conversions (signups) | 620 | 274 | 894 |
| Conv. Rate | 2.0% | 1.2% | 1.7% |
| Cost per Conversion | $30.00 | $51.82 | $36.69 |

**Attribution Analysis (Multi-Touch, Time-Decay Model):**

| Touchpoint Path | Conversions | Avg Days to Convert |
|----------------|-------------|-------------------|
| Google Ad → Direct → Signup | 312 | 1.4 |
| Meta Ad → Google Ad → Signup | 186 | 4.2 |
| Meta Ad → Organic → Email → Signup | 142 | 8.6 |
| Organic → Meta Ad (retarget) → Signup | 98 | 6.1 |
| Other multi-touch paths | 156 | 5.8 |

**Findings:**
1. Google Ads drives direct, fast conversions (1.4-day avg) — ideal for capturing high-intent demand.
2. Meta Ads plays a crucial **assist role**: 186 conversions touched Meta first before converting via Google. Under last-click attribution, Meta would receive zero credit for these.
3. The Meta → Organic → Email path shows that awareness campaigns create a delayed pipeline that converts through nurture. Cutting Meta spend would reduce email conversions within 2–4 weeks.

**Recommendations:**
- Maintain Google Ads at current spend; test increasing bids on top 10 converting keywords by 15%.
- Shift 30% of Meta budget from prospecting to retargeting — the retargeting path converts at 2.1x the rate of prospecting at half the cost.
- Extend the campaign 2 weeks: the time-decay model shows conversions are still accelerating as the multi-touch paths mature.

## Best Practices

- **Always compare against a baseline.** Raw numbers are meaningless without context. Show month-over-month, year-over-year, and target-vs-actual comparisons for every metric.
- **Segment before you summarize.** Aggregate numbers hide critical patterns. Always break data down by channel, device, geography, and user segment before drawing conclusions.
- **Use multi-touch attribution for any campaign with more than one channel.** Last-click attribution systematically undervalues awareness and mid-funnel channels, leading to misallocated budgets.
- **Lead with insights, not data.** Executives don't need 50 metrics — they need 3–5 actionable findings. Structure reports as "what happened → why it matters → what to do next."
- **Automate data collection, not interpretation.** Scripts and dashboards should pull data automatically, but the narrative — the "so what" — requires human or AI judgment applied to the specific business context.
- **Include confidence indicators.** For small sample sizes or short time windows, note that trends may not be statistically significant. Avoid making major budget decisions on fewer than 100 conversions per variant.

## Edge Cases

- **Data discrepancies between platforms.** Google Analytics and ad platforms often disagree on conversion counts due to different attribution windows, cookie handling, and tracking methodologies. Document the source of truth for each metric and note known discrepancies in the report.
- **Cookie consent and tracking gaps.** In regions with GDPR or CCPA enforcement, 20–40% of users may decline tracking cookies. Reported traffic and conversions are understated. Use server-side tracking or consent-mode modeling to estimate true values, and note the adjustment methodology.
- **Seasonality masking real trends.** A 15% traffic drop in December may be seasonal, not a problem. Always include year-over-year comparisons for seasonal businesses and flag whether changes are within normal seasonal variance.
- **Attribution for offline conversions.** B2B sales with long cycles often close offline via sales calls. Implement UTM-to-CRM mapping and closed-loop reporting so marketing can claim attribution for pipeline it influenced.
- **Zero-conversion campaigns in early stages.** New awareness campaigns may show zero direct conversions for 4–8 weeks. Measure leading indicators — impressions, reach, video view rate, landing page visits — to assess whether the campaign is building pipeline before judging ROI.
