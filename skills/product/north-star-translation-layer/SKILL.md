---
name: north-star-translation-layer
description: A framework for aligning sub-team metrics with a primary company North Star. Use this when sub-teams struggle to see their impact on high-level goals, when cross-prioritizing resources between disparate functions (e.g., Eng vs. Marketing), or during quarterly planning to set data-driven targets.
---

The North Star Translation Layer creates a "common currency" that converts local team metrics (like app load time or email conversion) into a single macro metric (like Monthly Active Orders or SQL Pipeline). This allows leadership to make objective resource allocation decisions across different departments.

## 1. Define the Dual North Star
Select at most two metrics to guide the entire growth organization.
- **Volume Metric:** A motivating, intuitive lead indicator of value (e.g., Monthly Active Orders, not just Revenue).
- **Efficiency Metric:** A guardrail to ensure quality (e.g., Payback Period based on contribution margin, not just CAC).

## 2. Map Local Team Metrics
Identify the specific "micro" metrics that each sub-team directly influences. 
- **Product/Eng:** Load times, checkout conversion rate, search success rate.
- **Marketing:** Email open rates, landing page conversion, ad click-through rate.
- **Sales/Growth Eng:** Lead response time, lead-to-qualified-opportunity rate.

## 3. Build the Translation Layer
Work with Finance and Data teams to create the mathematical relationship between the Micro and the Macro.
- **Regression Analysis:** Determine exactly how much one unit of a micro-metric (e.g., 100ms faster load time) contributes to the North Star (e.g., +0.05 Monthly Active Orders).
- **Holdout Groups:** Use long-term holdouts (keeping a small % of users on an old experience) to measure the cumulative impact of sub-team improvements over 6-12 months.
- **The "70/30" Rule:** Accept that these formulas are 70–80% accurate. Use them to guide big decisions, not to over-analyze marginal 5% differences.

## 4. Operationalize the Currency
- **Cross-Prioritization:** When deciding whether to fund a new SEO project vs. a Checkout optimization, compare their projected "North Star Impact" using the translation factors.
- **Refresh Cycle:** Update the translation factors every 6 months during the planning cycle to account for changing user behavior or market conditions.

## 5. Experimentation: Fail Conclusively
In B2B environments with low volume (low "N"), don't just "fail fast." Use the "Maximized Treatment" approach:
- **Go Big Early:** If testing a new lead-gen strategy, throw every possible tactic at it (custom landing pages, personalized gifts, executive outreach).
- **The Rationale:** If the "Best Case Version" fails, you have failed *conclusively* and never need to revisit the idea. If it works, you can cost-optimize the tactics later.

---

**Example 1: E-commerce/Marketplace (Instacart Model)**
- **North Star:** Monthly Active Orders (MAO).
- **Sub-Team:** Performance Engineering.
- **Local Metric:** App Load Time.
- **Translation:** Data shows that for every 1 second of reduced load time, MAO increases by 2%. 
- **Application:** The team prioritizes a $500k infrastructure project because it translates to a predictable 10,000 additional orders per month.

**Example 2: B2B SaaS (Ramp Model)**
- **North Star:** Dollars of SQL (Sales Qualified Lead) Pipeline.
- **Sub-Team:** Website/Growth.
- **Local Metric:** Landing Page Email Submission Rate.
- **Translation:** 10 "Bips" (0.10%) of conversion increase = $250k in SQL Pipeline.
- **Application:** A copy-change experiment that projects a 20 bip increase is prioritized over a new experimental channel that has unknown translation factors.

---

## Common Pitfalls
- **Using Lagging Metrics:** Do not use Revenue or Equity Value as the North Star for the Growth team; it is too far downstream for teams to feel accountable for daily.
- **Building In-House prematurely:** Do not build internal experimentation or CRM tools unless they are a proprietary competitive advantage. Use off-the-shelf tools (e.g., Mutiny for personalization, Airtable for sprint scoring) to maintain velocity.
- **Ignoring Payback Period:** Avoid focusing solely on CAC. A high-CAC customer with high contribution margin and a 10-month payback is often better than a low-CAC customer who churns in 3 months.
- **Lack of "Day" Mentality:** Don't work in quarters or weeks. Track "Days since founding" to remind the team that every 24-hour cycle is a unit of execution. Never put off for tomorrow what can be shipped today.