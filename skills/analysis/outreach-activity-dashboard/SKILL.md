---
name: outreach-activity-dashboard
description: >
  Build an activity dashboard with volume trends, engagement snapshots, and consistency analysis to help sales leaders spot gaps and keep the team on track.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Pipeline Management"
compatibility: Requires Amplemarket MCP server
---

# Outreach Activity Dashboard

Build an activity dashboard with volume trends, engagement snapshots, and consistency analysis to help sales leaders spot gaps and keep the team on track.

## Instructions

When a user wants to see outreach activity, query the Amplemarket analytics engine for volume and engagement data, identify trends, and present a structured dashboard.

### Steps

1. **Clarify scope, timeframe, and granularity.** Ask the user:
    - "What timeframe would you like to review? (default: last 30 days)"
    - "What granularity do you prefer? (daily, weekly, or monthly)"
    - "Full team or specific reps?"
    
    If the user does not specify, default to the last 30 days with weekly granularity for the full team.
    
2. **Submit analytics questions** by calling `mcp__claude_ai_Amplemarket__ask_analytics` for each of the following (adjust the timeframe and granularity accordingly):
    - "How many emails were sent per [day/week/month] in the last [timeframe]?"
    - "What is the overall reply rate in the last [timeframe]?"
    - "How many total emails were sent in the last [timeframe]?"
    - "What is the open rate trend in the last [timeframe]?"
    - "How many leads were added to lists in the last [timeframe]?"
    
    Store each returned `request_id` for polling.
    
3. **Wait approximately 20 seconds**, then call `mcp__claude_ai_Amplemarket__get_analytics_result` for each `request_id` to retrieve the answers.
4. **Handle pending results.** If any result is still processing, wait another 20 seconds and retry. Repeat up to 3 total attempts per request. Proceed with available data if some results remain unavailable.
5. **Compile the activity summary** with key metrics:
    
    
    | Metric | Value |
    | --- | --- |
    | Total Emails Sent | [number] |
    | Avg Daily/Weekly Volume | [number] |
    | Open Rate | [percentage] |
    | Reply Rate | [percentage] |
    | Leads Added | [number] |
6. **Identify trends** across the timeframe. Look for:
    - Volume spikes or drops (e.g., "Email volume dropped 30% in week 3. Was there a holiday or team change?")
    - Engagement changes (e.g., "Open rate climbed from 48% to 55% over the month. New subject lines may be working.")
    - Consistent ramp-up or ramp-down patterns
    - Day-of-week patterns if daily granularity is available
7. **Flag consistency issues.** Identify any periods with zero or very low activity. If per-rep data is available, flag individual reps who had significant activity gaps:
    - "No emails sent during the week of March 1-7. Was this intentional?"
    - "Alex Patel had zero sends on 8 out of 22 business days. Inconsistent cadence reduces pipeline momentum."
8. **Offer next steps.** Suggest follow-up actions:
    - "Want me to break this down by rep to see individual consistency?"
    - "Should I check if the volume drop in week 3 correlates with a sequence being paused?"
    - "Want me to compare this month to the previous month for trend analysis?"

### Important Notes

- Submit all five analytics questions in parallel to minimize wait time.
- Default to weekly granularity for 30-day views and monthly granularity for 90+ day views. Daily granularity works best for periods of 14 days or fewer.
- If per-rep breakdown is not available from the initial queries, offer to submit a follow-up query specifically for per-rep activity.
- When presenting trends, use percentage changes and directional indicators (increasing, decreasing, flat) rather than raw numbers alone.
- Activity volume alone does not indicate quality. Always pair volume metrics with engagement rates for a balanced view.
- Weekends and holidays naturally show zero or low activity. Do not flag these as consistency issues. Only flag business days with unexpectedly low or zero sends.
- If the user asks for a comparison (e.g., this month vs. last month), submit separate analytics queries for each period and present results side by side.
- Lead sourcing volume (leads added to lists) is a leading indicator. If lead additions drop, email volume will follow 1-2 weeks later. Flag this early.

## Examples

### Example 1: Monthly Activity Dashboard

**User prompt:** "Show me our outreach activity for the last 30 days."

**What the skill does:**
1. Confirms the 30-day timeframe with weekly granularity.
2. Submits five analytics questions via `mcp__claude_ai_Amplemarket__ask_analytics`.
3. Waits 20 seconds, then polls each `request_id` with `mcp__claude_ai_Amplemarket__get_analytics_result`.
4. Compiles the dashboard with trends and consistency flags.

**Example output:**

**OUTREACH ACTIVITY DASHBOARD - Last 30 Days**

**Key Metrics**

| Metric | Value | Trend |
| --- | --- | --- |
| Total Emails Sent | 11,240 | - |
| Avg Weekly Volume | 2,810 | - |
| Open Rate | 51.4% | Increasing (+3.2 pts vs prior 30 days) |
| Reply Rate | 5.8% | Flat (no significant change) |
| Leads Added | 1,450 | - |

**Weekly Volume Breakdown**

| Week | Emails Sent | vs. Avg |
| --- | --- | --- |
| Week 1 (Feb 7-13) | 3,120 | +11% above avg |
| Week 2 (Feb 14-20) | 2,940 | +4.6% above avg |
| Week 3 (Feb 21-27) | 1,980 | -29.5% below avg |
| Week 4 (Feb 28 - Mar 6) | 3,200 | +13.9% above avg |

**Trends and Observations**
- Volume dipped significantly in week 3, dropping 29.5% below the weekly average. This may correlate with a holiday, team absence, or a paused sequence. Worth investigating.
- Week 4 rebounded strongly with the highest volume of the month (3,200 emails). The team appears to have ramped back up.
- Open rates are trending upward, gaining 3.2 percentage points compared to the prior 30 days. If subject line or targeting changes were made, they appear to be working.
- Reply rate is flat at 5.8%. Volume increases are not yet translating into higher engagement. Consider reviewing email copy and personalization.
- 1,450 new leads were added to lists, roughly 48 per business day. This is a healthy pipeline input rate.

**Consistency Score**
- Team consistency: 3 out of 4 weeks were within 15% of the average. This is solid.
- Week 3 dip is the only outlier. If this was due to a specific event (holiday, offsite, sequence pause), it is not a concern. If unexplained, investigate further.

**Recommended Next Steps**
- "Want me to break down the week 3 dip by rep to see who stopped sending?"
- "Should I check if any sequences were paused during that period?"

---

### Example 2: Weekly Breakdown for a Specific Rep

**User prompt:** "Show me Sarah Chen's daily activity for the last two weeks."

**What the skill does:**
1. Submits analytics questions scoped to Sarah Chen with daily granularity for 14 days.
2. Polls results and presents a daily activity breakdown.

**Example output:**

**DAILY ACTIVITY - Sarah Chen (Last 14 Days)**

| Date | Emails Sent | Notes |
| --- | --- | --- |
| Mon, Feb 24 | 95 | - |
| Tue, Feb 25 | 110 | - |
| Wed, Feb 26 | 88 | - |
| Thu, Feb 27 | 102 | - |
| Fri, Feb 28 | 45 | Below average |
| Mon, Mar 3 | 108 | - |
| Tue, Mar 4 | 115 | Highest day |
| Wed, Mar 5 | 0 | No activity |
| Thu, Mar 6 | 92 | - |
| Fri, Mar 7 | 78 | - |

**Observations:**
- Sarah averaged 83 emails per day over this period, excluding the zero-activity day.
- Wednesday March 5 had zero sends. This could be PTO, a meeting-heavy day, or a technical issue.
- Friday volumes are consistently lower (45 and 78). This is common but worth noting if the team has Friday send targets.

**Recommendations:**
- Follow up on the zero-activity day (March 5). If it was planned PTO, no concern. If unplanned, ensure sequences are configured to continue sending even when the rep is unavailable.
- Sarah's daily average of 83 emails is below the team average of 112. However, if her engagement rates are high, this may be intentional quality-over-quantity positioning.

---

### Example 3: Quarter-Over-Quarter Comparison

**User prompt:** "Compare our outreach activity this quarter vs last quarter."

**What the skill does:**
1. Submits analytics questions for both the current quarter and the prior quarter.
2. Polls results and presents a side-by-side comparison with trend analysis.

**Example output:**

**QUARTER-OVER-QUARTER COMPARISON**

| Metric | This Quarter (Q1) | Last Quarter (Q4) | Change |
| --- | --- | --- | --- |
| Total Emails | 34,500 | 28,200 | +22.3% |
| Avg Monthly Volume | 11,500 | 9,400 | +22.3% |
| Open Rate | 52.1% | 49.3% | +2.8 pts |
| Reply Rate | 6.2% | 5.7% | +0.5 pts |
| Leads Added | 4,200 | 3,100 | +35.5% |

**Analysis:**
- Volume is up 22.3% quarter over quarter, driven by both increased rep headcount and higher per-rep output.
- Lead sourcing is up even more at 35.5%, which is fueling the volume increase.
- Engagement rates are slightly improved. The team is sending more without sacrificing quality.
- If this trajectory continues, Q2 could see 40,000+ emails with a 6.5%+ reply rate.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Analytics result still processing after 3 attempts | Present whatever data is available. Inform the user: "Volume data is ready but engagement trends are still processing. Here is what I have so far." Offer to retry the pending queries in a few minutes. |
| No daily or weekly breakdown available | The analytics engine may return totals rather than time-series data. Present the totals and suggest the user try a different granularity. If monthly data is available but weekly is not, use monthly as the fallback. |
| Per-rep data not included in the response | Submit a follow-up question to `mcp__claude_ai_Amplemarket__ask_analytics` specifically requesting per-rep data: "How many emails did each rep send per week in the last [timeframe]?" |
| Very short timeframe produces sparse data | For timeframes under 7 days, daily granularity may show only a few data points. Note this limitation and suggest expanding the timeframe for more meaningful trends. |
| Rate limiting on multiple queries | Space out `ask_analytics` calls by a few seconds if rate limits are hit. Prioritize total volume and reply rate queries, as these are the most important for an activity dashboard. |
| Data seems inconsistent (e.g., reply rate higher than open rate) | Flag the inconsistency to the user. This can happen if the analytics engine counts unique opens differently from total opens, or if reply tracking differs from open tracking. Present the data as-is and note: "Reply rate appears higher than open rate, which may indicate different counting methodologies." |
| User wants real-time data | Analytics queries reflect processed data, which may have a delay of a few hours. Inform the user: "Analytics data may lag by a few hours. For today's activity, results will be most accurate tomorrow." |