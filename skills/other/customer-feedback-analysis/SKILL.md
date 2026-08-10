---
name: customer-feedback-analysis
description: Analyze NPS, CSAT, and qualitative customer feedback to extract themes, identify trends, and generate actionable insight reports. Use when the user requests customer feedback analysis or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Customer Feedback Analysis

Transform raw customer feedback from NPS surveys, CSAT responses, support interactions, and app store reviews into structured insights. This skill extracts recurring themes from open-text responses, calculates quantitative score distributions, identifies emerging trends over time, and produces reports that connect customer sentiment to specific product areas and business outcomes.

## Workflow

1. **Collect feedback data** — Aggregate feedback from all available sources: NPS survey responses (score + open text), CSAT ratings from support interactions, in-app feedback widgets, app store reviews, social media mentions, G2/Capterra reviews, and sales call notes. Tag each response with metadata: date, customer segment, plan tier, account tenure, and source channel. Ensure consistent schema across all sources.

2. **Clean and normalize** — Deduplicate responses from the same customer across channels. Standardize rating scales (convert 1-5 CSAT to 1-10 for cross-comparison). Strip PII from open-text responses. Handle multilingual responses by detecting language and translating to English while preserving the original. Remove bot/spam responses using pattern detection (identical text, suspicious timing, single-word noise).

3. **Extract themes from open-text responses** — Apply topic modeling to cluster open-text feedback into coherent themes. Common theme categories include: product reliability, ease of use, specific feature feedback, pricing/value perception, support quality, onboarding experience, and competitive comparison. Assign each response to one or more themes with a confidence score. Pull representative verbatim quotes for each theme.

4. **Calculate quantitative scores** — Compute aggregate metrics: NPS (% Promoters minus % Detractors), CSAT average, and theme frequency distribution. Break scores down by segment (plan tier, industry, account size, tenure) to identify which cohorts are most and least satisfied. Calculate statistical significance for segment differences to avoid acting on noise.

5. **Identify trends** — Compare current period metrics against previous periods (month-over-month, quarter-over-quarter). Flag themes with significant volume changes (up or down 20%+ from baseline). Detect emerging themes that appear for the first time or cross a frequency threshold. Correlate sentiment shifts with product releases, pricing changes, or market events.

6. **Generate insight report** — Produce a structured report with: executive summary (3-5 key takeaways), quantitative scorecard, theme breakdown with representative quotes, trend analysis, segment comparison, and recommended actions. Each recommendation should be tied to a specific theme and prioritized by frequency and business impact.

## Usage

Provide feedback data (CSV, JSON, or describe the dataset) and specify the analysis scope. The agent returns a structured insight report.

```
Analyze our Q4 NPS survey results (850 responses). Break down scores by plan
tier, extract the top themes from detractor comments, and identify any new
themes that weren't present in Q3.
```

## Examples

### Example 1: NPS survey analysis

**Input:** 850 NPS survey responses from Q4, segmented by plan tier.

**Output:**

**Executive Summary:**
- Overall NPS: +32 (up from +28 in Q3, statistically significant at p<0.05)
- Enterprise NPS: +52 | Pro NPS: +31 | Starter NPS: +14
- Top detractor theme: "Reporting is too slow" (38% of detractor comments, up from 22% in Q3)
- New emerging theme: "Need better mobile experience" (appeared in 12% of Q4 responses, absent in Q3)
- Promoter loyalty driver: "Customer support is exceptional" (45% of promoter comments)

**Score Distribution:**

| Segment | Promoters (9-10) | Passives (7-8) | Detractors (0-6) | NPS | Responses |
|---------|-----------------|----------------|-------------------|-----|-----------|
| Enterprise | 68% | 16% | 16% | +52 | 180 |
| Pro | 52% | 27% | 21% | +31 | 420 |
| Starter | 38% | 38% | 24% | +14 | 250 |
| **Overall** | **51%** | **28%** | **21%** | **+32** | **850** |

**Theme Breakdown (Detractor Comments, n=179):**

| Theme | Frequency | Change vs Q3 | Representative Quotes |
|-------|-----------|-------------|----------------------|
| Slow reporting | 38% | +16pp | "Dashboards take 20+ seconds to load with large datasets. This is killing our team's productivity." |
| Pricing concerns | 24% | -3pp | "The price jump from Pro to Enterprise is too steep. We need the features but can't justify 3x the cost." |
| Missing integrations | 18% | -5pp | "Still no native Salesforce integration. We've been asking for over a year." |
| Mobile experience | 12% | NEW | "I can't review dashboards on my phone during commute. Competitors have solid mobile apps." |
| Complex setup | 8% | -8pp | "Initial configuration took our team 3 weeks. Onboarding docs are outdated." |

**Recommended Actions:**
1. **P0 — Reporting performance:** Invest in query optimization and caching. 38% of detractors cite this, and it's growing fast. Estimated NPS impact: +5-8 points if resolved.
2. **P1 — Mobile experience:** Commission a competitive analysis of mobile offerings. 12% is a new theme trending upward — get ahead of it before Q1 NPS.
3. **P2 — Pricing tier gap:** Introduce a "Pro Plus" tier between Pro and Enterprise to capture accounts that need select enterprise features without the full price tag.

### Example 2: App store review sentiment analysis

**Input:** 1,200 app store reviews from the past 6 months (iOS and Android combined).

**Output:**

**Overall Sentiment:** 3.8★ average (iOS: 4.1★, Android: 3.4★)

**Sentiment by Star Rating:**
- 5★ (34%): "Love the design," "Fast and reliable," "Best in category"
- 4★ (22%): "Great but needs offline mode," "Almost perfect"
- 3★ (18%): "Decent but buggy on Android," "OK for basic use"
- 2★ (14%): "Crashes frequently," "Too expensive for what it offers"
- 1★ (12%): "Lost my data," "Customer support unresponsive," "App doesn't open"

**Feature Request Extraction (from 3★ and above reviews):**

| Feature Request | Mentions | Platform | Sample Quote |
|----------------|----------|----------|-------------|
| Offline mode | 87 | Both | "I travel a lot and need to access my data without WiFi." |
| Dark mode | 64 | Both | "Using this at night is blinding. Please add dark mode." |
| Widget support | 43 | iOS | "Would love a home screen widget to see my daily stats." |
| Export to PDF | 38 | Both | "I need to share reports with people who don't have accounts." |
| Android stability | 112 | Android | "Crashes every time I try to edit a dashboard. Pixel 8, Android 14." |

**Critical Finding:** Android rating (3.4★) drags overall score down. 72% of 1-2★ reviews are from Android users. Top complaint is crash on dashboard edit (Samsung and Pixel devices, Android 14+). Fixing this single bug could lift Android rating by an estimated 0.4 stars.

## Best Practices

- Analyze detractor and promoter comments separately — blending them into a single theme analysis dilutes the signal from each group.
- Always report confidence intervals and sample sizes alongside NPS scores. A segment NPS of +60 from 15 responses is not actionable.
- Use verbatim quotes in reports to leadership — raw customer voice is more persuasive than statistical summaries and prevents misinterpretation of theme labels.
- Close the feedback loop by responding to detractors within 48 hours of survey completion. Customers who receive follow-up after negative feedback are 2x more likely to improve their score next cycle.
- Track theme frequency over time rather than reacting to a single snapshot. A theme trending upward over 3 quarters is a structural issue; a one-quarter spike may be a temporary reaction to a specific release.
- Separate "feature absence" complaints from "feature broken" complaints in your theme taxonomy — they require different organizational responses (product roadmap vs. engineering fix).

## Edge Cases

- **Low response rates (<15%)** — Results may suffer from non-response bias where only the most satisfied and most dissatisfied customers respond. Note the response rate prominently and recommend increasing it before drawing segment-level conclusions.
- **Survey fatigue** — Accounts surveyed more than once per quarter show declining response rates and more negative scores. Cap survey frequency and rotate which customers are surveyed.
- **Sarcastic or ironic responses** — "Oh great, another update that breaks everything, love it! 10/10" reads as positive to naive sentiment analysis. Flag responses where sentiment score and NPS score are contradictory for manual review.
- **Feedback influenced by recent outage** — A single incident can dominate an entire survey period. Segment responses by pre/post incident and report both views. Consider extending the survey window to dilute the recency effect.
- **Competitor mentions in feedback** — Responses like "I'm switching to CompetitorX" contain valuable competitive intelligence. Extract competitor mentions into a separate analysis and route to product strategy.
