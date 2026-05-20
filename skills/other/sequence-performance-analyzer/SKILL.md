---
name: sequence-performance-analyzer
description: >
  Compare outreach sequences side by side to identify top performers, flag underperformers, and surface A/B testing insights that improve reply rates.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Pipeline Management"
compatibility: Requires Amplemarket MCP server
---

# Sequence Performance Analyzer

Compare outreach sequences side by side to identify top performers, flag underperformers, and surface A/B testing insights that improve reply rates.

## Instructions

When a user wants to evaluate their sequences, query the Amplemarket analytics engine for per-sequence metrics, classify each sequence by performance tier, and generate actionable recommendations.

### Steps

1. **Clarify scope and timeframe.** Ask the user:
    - "What timeframe would you like to analyze? (default: last 30 days)"
    - "Any specific sequences to focus on, or all active sequences?"
    
    If the user does not specify, default to the last 30 days and all active sequences.
    
2. **Submit analytics questions** by calling `mcp__claude_ai_Amplemarket__ask_analytics` for each of the following (adjust the timeframe accordingly):
    - "What are the open rates by sequence in the last [timeframe]?"
    - "What are the reply rates by sequence in the last [timeframe]?"
    - "How many emails were sent per sequence in the last [timeframe]?"
    - "What are the bounce rates per sequence in the last [timeframe]?"
    - "Which sequences have the most meetings booked in the last [timeframe]?"
    
    Store each returned `request_id` for polling.
    
3. **Wait approximately 20 seconds**, then call `mcp__claude_ai_Amplemarket__get_analytics_result` for each `request_id` to retrieve the answers.
4. **Handle pending results.** If any result is still processing, wait another 20 seconds and retry. Repeat up to 3 total attempts per request. If a result remains unavailable, proceed with the data you have and note the gap.
5. **Compile the sequence performance table:**
    
    Sequence Name | Emails Sent | Open Rate | Reply Rate | Bounce Rate | Meetings |
    
    Sort by reply rate by default, or by another metric if the user requests it.
    
6. **Classify each sequence** into performance tiers:
    - **Top Performer:** Above average on both reply rate and open rate. These sequences are working well.
    - **Steady:** Near the average on most metrics. Functional but not exceptional.
    - **Underperformer:** Below average on reply rate with a meaningful sample size (50+ emails sent). Not delivering results.
    - **At Risk:** High bounce rate (above 3%) or extremely low engagement. May be harming deliverability.
    - **Insufficient Data:** Fewer than 50 emails sent. Too early to judge.
7. **Generate actionable recommendations** for each tier:
    - **Top Performers:** "Scale this sequence. Increase volume or replicate its approach in new sequences. What makes it work: [specific observations]."
    - **Steady:** "This sequence is doing its job. Consider A/B testing subject lines or CTAs to push it into top performer territory."
    - **Underperformers:** "Consider pausing [sequence name]. A 1.2% reply rate after 500 sends is not working. Review the targeting, messaging, and timing."
    - **At Risk:** "Pause immediately. A 6% bounce rate on [sequence name] is damaging your domain reputation. Clean the lead list before resuming."
    - If two sequences target similar personas, compare them: "Sequence A and B both target VP Sales at mid-market SaaS companies, but A has 3x the reply rate. Adopt A's messaging and retire B."
8. **Offer next steps.** Suggest follow-up actions:
    - "Want me to check which reps are using the top-performing sequences?"
    - "Should I analyze the email steps within the underperforming sequences to find where prospects drop off?"
    - "Want me to compare this period's performance to the previous period?"

### Important Notes

- Submit all five analytics questions in parallel to minimize wait time.
- Sequences with fewer than 50 emails sent should be flagged as "Insufficient Data" rather than classified as underperformers. Small sample sizes produce unreliable rates.
- Bounce rate is a critical health metric. Any sequence above 3% bounce rate should be flagged regardless of other metrics.
- If the user asks about a single sequence, provide a detailed breakdown of that sequence rather than a comparison table.
- The analytics engine may group data differently than expected. Adapt the presentation to match whatever structure is returned.
- When classifying sequences, always weight reply rate most heavily. Open rate is useful but can be inflated by email privacy features. Reply rate is the most honest indicator of message resonance.
- For A/B comparisons to be valid, both sequences should have similar send volumes and target similar audiences. Flag when comparisons are between unequal groups.
- If the user mentions a sequence name that does not appear in the results, the sequence may be inactive, recently created, or named differently in the system. Ask the user to confirm the exact name.

## Examples

### Example 1: Full Sequence Audit

**User prompt:** "Which of my sequences are working and which should I pause?"

**What the skill does:**
1. Confirms the 30-day default timeframe.
2. Submits five analytics questions via `mcp__claude_ai_Amplemarket__ask_analytics`.
3. Waits 20 seconds, then polls each `request_id` with `mcp__claude_ai_Amplemarket__get_analytics_result`.
4. Compiles the performance table, classifies sequences, and generates recommendations.

**Example output:**

**SEQUENCE PERFORMANCE REPORT - Last 30 Days**

**Summary**
- Active sequences analyzed: 8
- Total emails sent: 9,850
- Average open rate: 48.7%
- Average reply rate: 5.3%
- Total meetings from sequences: 22

**Performance Table**

| Sequence | Emails Sent | Open Rate | Reply Rate | Bounce Rate | Meetings | Tier |
| --- | --- | --- | --- | --- | --- | --- |
| Q1 Enterprise Outreach | 1,850 | 56.2% | 9.8% | 1.1% | 7 | Top Performer |
| VP Sales - Pain Point v2 | 1,420 | 52.1% | 8.1% | 1.4% | 5 | Top Performer |
| Mid-Market SaaS Play | 1,680 | 49.3% | 5.4% | 1.8% | 4 | Steady |
| Inbound Follow-Up | 920 | 61.8% | 7.2% | 0.8% | 3 | Top Performer |
| Cold Outreach v3 | 1,540 | 42.1% | 3.1% | 2.2% | 2 | Steady |
| New Logo Prospecting | 1,280 | 38.4% | 1.9% | 3.8% | 1 | At Risk |
| Director IT Campaign | 890 | 35.6% | 1.2% | 2.1% | 0 | Underperformer |
| Startup Founders Blast | 270 | 44.3% | 4.8% | 1.5% | 0 | Insufficient Data |

**Recommendations**

- **Scale:** "Q1 Enterprise Outreach" is your best sequence with a 9.8% reply rate. Increase send volume and consider replicating its messaging for other personas.
- **Watch:** "Inbound Follow-Up" has the highest open rate (61.8%) but lower volume. These are warm leads, so maximizing speed-to-lead on this sequence could boost meetings.
- **A/B Insight:** "VP Sales - Pain Point v2" outperforms "Cold Outreach v3" by 2.6x on reply rate. Both target similar seniority levels. Review what v2 does differently in subject lines and opening hooks.
- **Pause:** "Director IT Campaign" has a 1.2% reply rate after 890 sends. This sequence is not resonating. Pause it and review the targeting and messaging before relaunching.
- **Fix Urgently:** "New Logo Prospecting" has a 3.8% bounce rate. Pause this sequence, clean the associated lead list, and validate emails before resuming. The bounce rate is putting your sending domain at risk.
- **Wait:** "Startup Founders Blast" only has 270 sends. Early metrics look promising (4.8% reply rate) but the sample is too small to draw conclusions. Let it run to 500+ sends before evaluating.

**Efficiency Rankings (Meetings per 1,000 Emails)**

| Sequence | Meetings / 1K Emails |
| --- | --- |
| Inbound Follow-Up | 3.26 |
| Q1 Enterprise Outreach | 3.78 |
| VP Sales - Pain Point v2 | 3.52 |
| Mid-Market SaaS Play | 2.38 |
| Cold Outreach v3 | 1.30 |
| New Logo Prospecting | 0.78 |
| Director IT Campaign | 0.00 |

This efficiency view highlights that "Inbound Follow-Up" and "Q1 Enterprise Outreach" are not just getting replies, they are converting those replies into meetings at a high rate.

---

### Example 2: Comparing Two Specific Sequences

**User prompt:** "Compare my Enterprise Outreach sequence to the Cold Outreach v3 sequence."

**What the skill does:**
1. Submits analytics questions scoped to the two named sequences.
2. Polls results and presents a head-to-head comparison.

**Example output:**

**HEAD-TO-HEAD COMPARISON**

| Metric | Q1 Enterprise Outreach | Cold Outreach v3 | Winner |
| --- | --- | --- | --- |
| Emails Sent | 1,850 | 1,540 | Enterprise (+20%) |
| Open Rate | 56.2% | 42.1% | Enterprise (+14 pts) |
| Reply Rate | 9.8% | 3.1% | Enterprise (+6.7 pts) |
| Bounce Rate | 1.1% | 2.2% | Enterprise (lower is better) |
| Meetings | 7 | 2 | Enterprise (3.5x) |

Enterprise Outreach outperforms Cold Outreach v3 on every metric. Key differences to investigate: subject line approach, personalization depth, and lead list quality.

**Recommendation:** Retire Cold Outreach v3 and migrate its leads to the Enterprise Outreach sequence (or a variant adapted for the same audience). The data strongly supports this consolidation.

---

### Example 3: Finding Sequences to Pause

**User prompt:** "Should I pause any of my sequences?"

**What the skill does:**
1. Queries all sequence metrics for the last 30 days.
2. Filters to sequences classified as "Underperformer" or "At Risk."
3. Presents only the sequences that need attention with specific pause/fix recommendations.

**Example output:**

**SEQUENCES TO REVIEW**

Two sequences should be paused or reworked:

1. **Director IT Campaign** - 1.2% reply rate, 0 meetings, 890 emails sent. This sequence has had enough volume to confirm it is not working. Recommended action: pause immediately and review targeting plus messaging before relaunch.
2. **New Logo Prospecting** - 3.8% bounce rate with 1.9% reply rate. The high bounce rate is the primary concern. Recommended action: pause, clean the lead list, validate all email addresses, and consider tightening the ICP criteria for this sequence.

All other sequences are performing at or above average. No further pauses recommended.

## Classification Thresholds

The tier classification uses these default thresholds. Adjust based on the user's industry and typical performance benchmarks:

- **Top Performer:** Reply rate above the team average AND open rate above the team average, with at least 100 emails sent.
- **Steady:** Within 20% of the team average on reply rate, with no critical bounce issues.
- **Underperformer:** Reply rate more than 40% below the team average, with at least 50 emails sent to confirm the pattern.
- **At Risk:** Bounce rate above 3%, regardless of other metrics. Deliverability trumps engagement.
- **Insufficient Data:** Fewer than 50 emails sent. Rates are unreliable at this volume.

For teams with very high or very low baseline performance, adjust thresholds relative to the team average rather than using fixed percentages.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Analytics result still processing after 3 attempts | Present whatever data is available. Tell the user: "Some queries are still processing. I have results for [available metrics]. Want me to present partial results or retry in a few minutes?" |
| No sequence data returned | The analytics engine may not have sequence-level data for very short timeframes. Try expanding to 30 or 60 days. If still no data, the user may not have active sequences or sequence tracking may not be configured. |
| Sequence names are truncated or unclear | Present the names exactly as returned by analytics. Ask the user: "Do you recognize these sequence names? Some may be abbreviated." |
| Very few sequences (1-2 only) | Adapt the output to a detailed single-sequence breakdown rather than a comparison table. Comparisons require at least 2-3 sequences to be meaningful. |
| Rate limiting on multiple queries | Space out `ask_analytics` calls by a few seconds if you hit rate limits. Submit reply rate and emails sent first, as these are the most important metrics for sequence evaluation. |
| User asks about step-level performance | Submit a follow-up question to `mcp__claude_ai_Amplemarket__ask_analytics`: "What is the reply rate by step for sequence [name] in the last [timeframe]?" The analytics engine may support step-level breakdowns. |
| Bounce rate data not available | Open rate can serve as a proxy signal for deliverability. Very low open rates (below 20%) may indicate spam folder placement even if bounce data is missing. Note this in the report. |