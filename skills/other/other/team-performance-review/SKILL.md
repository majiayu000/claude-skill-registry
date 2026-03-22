---
name: team-performance-review
description: >
  Compare your sales reps side by side on outreach volume, engagement rates, and meetings booked to identify top performers and coaching opportunities.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Team & Coaching"
compatibility: Requires Amplemarket MCP server
---

# Team Performance Review

Compare your sales reps side by side on outreach volume, engagement rates, and meetings booked to identify top performers and coaching opportunities.

## Instructions

When a user wants to review team performance, query the Amplemarket analytics engine for per-rep metrics, compile a leaderboard, and surface actionable insights.

### Steps

1. **Clarify scope and timeframe.** Ask the user:
    - "What timeframe would you like to review? (default: last 30 days)"
    - "Any specific reps to focus on, or the full team?"
    
    If the user does not specify a timeframe, default to the last 30 days.
    
2. **Submit analytics questions** by calling `mcp__claude_ai_Amplemarket__ask_analytics` for each of the following questions (adjust the timeframe to match the user's request):
    - "How many emails were sent by each rep in the last [timeframe]?"
    - "What is the reply rate by rep in the last [timeframe]?"
    - "What is the open rate by rep in the last [timeframe]?"
    - "How many meetings were booked by each rep in the last [timeframe]?"
    - "What is the bounce rate by rep in the last [timeframe]?"
    
    Store each returned `request_id` for polling in the next step.
    
3. **Wait approximately 20 seconds**, then call `mcp__claude_ai_Amplemarket__get_analytics_result` for each `request_id` to retrieve the answers.
4. **Handle pending results.** If any result is still processing, wait another 20 seconds and retry. Repeat up to 3 total attempts per request. If a result is still unavailable after 3 attempts, note it as unavailable and proceed with the data you have.
5. **Compile the team leaderboard.** Build a table with the following columns:
    
    Rep Name | Emails Sent | Open Rate | Reply Rate | Bounce Rate | Meetings Booked |
    
    Sort by reply rate (or another metric if the user requests it).
    
6. **Identify top performers and underperformers** on each metric:
    - Highest reply rate
    - Highest email volume
    - Most meetings booked
    - Highest bounce rate (flag as a concern)
    - Lowest engagement (may need coaching or list quality review)
7. **Generate insights and recommendations.** Provide specific, data-backed observations. For example:
    - "Sarah leads in reply rate (12.4%) but sends the fewest emails. Increasing her volume could multiply results."
    - "Marcus has the highest email volume but a 4.2% bounce rate that needs attention. His lead sources may need cleaning."
    - "The team average reply rate is 6.1%. Three reps are below 3%, which suggests a messaging or targeting issue."
8. **Offer next steps.** Suggest follow-up actions such as:
    - "Want me to drill into a specific rep's sequences to see what is driving their results?"
    - "Should I check which sequences are producing the best engagement?"
    - "Want me to compare this period to the previous period to spot trends?"

### Important Notes

- Submit all five analytics questions in parallel to minimize wait time. Do not submit them one at a time.
- If the user asks about a single rep rather than the full team, adjust the questions to focus on that rep and provide a detailed individual breakdown instead of a leaderboard.
- Bounce rates above 5% are a red flag for domain reputation. Always call these out prominently.
- If the analytics engine returns data grouped differently than expected, adapt the presentation to match whatever grouping is available.
- Default to the last 30 days, but always confirm the timeframe with the user before submitting queries.
- When comparing reps, always include both absolute numbers and rates. A rep with 90% open rate on 20 emails is not comparable to a rep with 50% open rate on 2,000 emails.
- If the user has fewer than 3 reps, skip the leaderboard format and present individual breakdowns side by side instead.
- Reply rate is generally the most meaningful metric for evaluating outreach effectiveness. Use it as the primary sort unless the user requests otherwise.
- Meetings booked is the ultimate outcome metric. Always highlight reps who convert replies to meetings efficiently, even if their raw reply count is lower.

## Examples

### Example 1: Full Team Review - Last 30 Days

**User prompt:** "How is my team doing? Give me a performance overview."

**What the skill does:**
1. Asks the user to confirm the 30-day default timeframe.
2. Submits five analytics questions via `mcp__claude_ai_Amplemarket__ask_analytics`.
3. Waits 20 seconds, then polls each `request_id` with `mcp__claude_ai_Amplemarket__get_analytics_result`.
4. Compiles the leaderboard and generates insights.

**Example output:**

**TEAM PERFORMANCE REVIEW - Last 30 Days**

**Summary**
- Total emails sent: 12,450
- Team average open rate: 52.3%
- Team average reply rate: 6.1%
- Total meetings booked: 34
- Team average bounce rate: 2.1%

**Leaderboard**

| Rank | Rep | Emails Sent | Open Rate | Reply Rate | Bounce Rate | Meetings |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Sarah Chen | 1,820 | 58.2% | 12.4% | 1.1% | 9 |
| 2 | James Wilson | 2,650 | 54.1% | 8.7% | 1.8% | 8 |
| 3 | Maria Lopez | 2,410 | 51.6% | 6.3% | 2.0% | 7 |
| 4 | Alex Patel | 2,200 | 49.8% | 5.1% | 1.9% | 5 |
| 5 | David Kim | 1,950 | 50.3% | 3.2% | 2.4% | 3 |
| 6 | Marcus Brown | 1,420 | 47.1% | 2.1% | 4.2% | 2 |

**Key Insights**
- Sarah Chen leads the team with a 12.4% reply rate, more than double the team average. Her sequences and messaging should be studied and replicated.
- James Wilson has the highest volume (2,650 emails) while maintaining strong engagement. A reliable high performer.
- Marcus Brown has a 4.2% bounce rate, well above the team average of 2.1%. His lead lists need a quality review before they impact domain reputation.
- David Kim and Marcus Brown are both below 3.5% reply rate. Consider reviewing their targeting criteria and email copy.
- Meetings-per-email efficiency: Sarah books 1 meeting per 202 emails sent, while Marcus books 1 per 710 emails. Sarah's approach is 3.5x more efficient.

**Recommended Next Steps**
- "Want me to drill into Sarah's sequences to see what is driving her high reply rate?"
- "Should I check Marcus's bounce sources and recommend list cleaning?"
- "Want me to compare this to the previous 30 days to see if the team is trending up or down?"

---

### Example 2: Specific Rep Deep Dive

**User prompt:** "How is Sarah Chen performing this quarter?"

**What the skill does:**
1. Adjusts analytics questions to focus on Sarah Chen for the last quarter (90 days).
2. Submits and polls the analytics engine.
3. Returns an individual performance breakdown with trends.

**Example output:**

**INDIVIDUAL PERFORMANCE - Sarah Chen (Last 90 Days)**

| Metric | Value | vs. Team Avg |
| --- | --- | --- |
| Emails Sent | 5,240 | -12% below avg |
| Open Rate | 57.8% | +11% above avg |
| Reply Rate | 11.9% | +95% above avg |
| Bounce Rate | 1.2% | -43% below avg |
| Meetings Booked | 24 | +60% above avg |

Sarah is a high-efficiency rep. Lower volume but significantly above average on every engagement metric. Increasing her send volume by even 20% could yield 4-5 additional meetings per month.

**Recommendations for Sarah:**
- Increase daily send volume. She has headroom to send more without sacrificing quality.
- Share her best-performing sequences and email templates with the rest of the team.
- Consider assigning her higher-value accounts where her high engagement rate will have the most impact.

---

### Example 3: Quarterly Comparison

**User prompt:** "Compare my team's performance this month vs last month."

**What the skill does:**
1. Submits analytics questions for both the current month and the previous month.
2. Polls results for all requests.
3. Presents a side-by-side comparison with trend indicators.

**Example output:**

**MONTH-OVER-MONTH COMPARISON**

| Metric | This Month | Last Month | Change |
| --- | --- | --- | --- |
| Total Emails | 4,200 | 3,800 | +10.5% |
| Open Rate | 53.1% | 51.8% | +1.3 pts |
| Reply Rate | 6.4% | 5.9% | +0.5 pts |
| Meetings | 12 | 9 | +33.3% |
| Bounce Rate | 1.9% | 2.3% | -0.4 pts |

Overall positive trend. Email volume is up, engagement is improving, and bounce rate is declining. The team is heading in the right direction.

**Key drivers of improvement:**
- Reply rate gain likely driven by new sequences introduced mid-month.
- Bounce rate decline suggests recent list cleaning efforts are paying off.
- Meeting conversion is up 33%, the strongest improvement of any metric.

**Areas to watch:**
- Open rate improvement is modest (+1.3 pts). Subject line optimization could accelerate this further.
- Volume growth needs to be sustained. Check if the increase was driven by one rep or spread across the team.

## Interpreting the Leaderboard

When reviewing the leaderboard, keep these benchmarks in mind for B2B outbound email:

- **Open rate:** 40-60% is typical. Below 30% may signal deliverability issues or weak subject lines. Above 60% is excellent.
- **Reply rate:** 3-8% is average for cold outreach. Above 10% is strong. Below 2% indicates a problem with targeting, messaging, or both.
- **Bounce rate:** Below 2% is healthy. 2-5% is a warning. Above 5% requires immediate action to protect your domain.
- **Meetings booked:** This depends heavily on sales cycle and product. Focus on the ratio of meetings to replies (conversion rate) rather than absolute numbers.

Adjust these benchmarks based on the user's industry and selling motion. Enterprise outreach typically has lower reply rates but higher deal values, while SMB outreach should have higher reply rates with faster cycles.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Analytics result still processing after 3 attempts | Inform the user: "Some analytics queries are still processing. I have partial results for [available metrics]. Want me to present what I have, or try again in a few minutes?" Present whatever data is available rather than returning nothing. |
| No data returned for the requested timeframe | Try broadening the timeframe. If "last 7 days" returns nothing, suggest "last 30 days" instead. The analytics engine may not have data for very short or very old periods. |
| Rep names do not match expectations | Analytics may return email addresses instead of names, or use different name formats. Present data as returned and let the user identify reps. Ask: "Do these rep identifiers match your team? Let me know if any names look unfamiliar." |
| Partial data returned (some metrics missing) | Present the metrics that are available and note which are missing. For example: "Bounce rate data was not available for this period. All other metrics are shown below." Do not block the entire report for one missing metric. |
| Rate limiting on multiple queries | If you receive rate limit errors, space out the `ask_analytics` calls by a few seconds each. Submit the most important questions first (reply rate, emails sent) so you have core data even if later queries fail. |
| User asks for metrics not covered here | The analytics engine accepts natural language questions. Submit the user's exact question to `mcp__claude_ai_Amplemarket__ask_analytics` and see if it can answer. For example, "What is the click rate by rep?" may work even though it is not in the default set. |
| Very large team (20+ reps) | Offer to split the review into groups. "You have 25 reps. Want me to review the top 10 by volume first, then the rest?" This keeps the output manageable and the analytics queries focused. |