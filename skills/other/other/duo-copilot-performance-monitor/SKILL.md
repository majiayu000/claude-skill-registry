---
name: duo-copilot-performance-monitor
description: >
  Post a weekly Duo Copilot performance report to a Slack channel, covering activity metrics for the current week and outcome/performance metrics over a 30-day rolling window.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Copilot Tools"
compatibility: Requires Amplemarket MCP server
---


# Duo Copilot Performance Monitor

Post a weekly Duo Copilot performance report to a Slack channel, covering activity metrics for the current week and outcome/performance metrics over a 30-day rolling window.

## Instructions

When invoked on a recurring weekly schedule, query Amplemarket analytics for Duo Copilot metrics and post a structured report to the designated Slack channel.

### Steps

1. **Receive configuration from the prompt.** The recurring prompt that triggers this skill should include:
    - **Slack channel:** Which channel to post to
    - **Team scope:** Full account, a specific team, or multiple teams with separate reports
    - **Alert thresholds** (optional): Dismiss rate threshold to flag (default: 40%), week-over-week dismiss rate increase threshold (default: 10 percentage points)
    
    If any required parameter is missing, ask the user before proceeding.
    
2. **Submit analytics questions** by calling `mcp__claude_ai_Amplemarket__ask_analytics` for each of the following. Activity metrics cover the current week (Mon-Sun). Performance metrics cover a 30-day rolling window.
    
    **Activity (this week):**
    
    - "How many Duo leads were generated this week?"
    - "How many Duo leads were actioned vs dismissed this week?"
    - "What is the Duo lead dismiss rate this week?"
    - "How many Duo leads did each rep action this week?"
    - "What are the dismiss reasons for Duo leads this week? Break down by Bad lead, Bad company, Bad signal, and Other."
    - "What is the dismiss rate by signal type this week?"
    - "Which reps have the longest streak of business days without actioning a Duo lead?"
    
    **Activity (prior week, for comparison):**
    
    - "How many Duo leads were generated last week?"
    - "What was the Duo lead dismiss rate last week?"
    - "How many Duo leads did each rep action last week?"
    
    **Performance (last 30 days, rolling):**
    
    - "How many interested replies came from Duo-sourced leads in the last 30 days?"
    - "How many meetings were booked from Duo-sourced leads in the last 30 days?"
    - "Which signal types have the highest interested and reply rate from Duo-sourced leads in the last 30 days?"
    - "Which signal types generate the most Duo leads in the last 30 days?"
    
    Store each returned `request_id` for polling. Submit all queries in parallel.
    
3. **Wait approximately 20 seconds**, then call `mcp__claude_ai_Amplemarket__get_analytics_result` for each `request_id`. If any result is still processing, wait another 20 seconds and retry. Repeat up to 3 total attempts per request. Proceed with available data if some results remain unavailable.
4. **Compile the report** with seven sections:
    
    **Section 1: Outcomes (30-day rolling window)**
    

| Metric | Last 30 Days |
| --- | --- |
| Interested replies from Duo | [number] |
| Meetings booked from Duo | [number] |

Note: Outcomes use a 30-day rolling window to allow time for leads to receive replies and book meetings. This number shifts forward each week.

**Section 2: Activity (this week)**

| Metric | This Week | Last Week | Change |
| --- | --- | --- | --- |
| Leads generated | [number] | [number] | [+/- %] |
| Leads actioned | [number] | [number] | [+/- %] |
| Dismiss rate | [%] | [%] | [+/- pts] |

**Section 3: Signal Performance (30-day rolling window)**

Rank signal types by volume and by engagement rate:

*Top signals by volume (last 30 days):* Top 3 signal types by number of Duo leads generated.

*Top signals by interested/reply rate (last 30 days):* Top 3 signal types by interested and reply rate. Flag any signal with meaningful volume (50+ leads) and below 1% interested rate as underperforming.

**Section 4: Rep Leaderboard (this week)**

Top 10 reps by Duo leads actioned this week. Include count and change vs last week.

If more than 10 reps, show top 10 and bottom 3. Summarize the middle: "12 additional reps actioned between 15-30 leads each."

**Section 5: Rep Inactivity (this week)**

Reps with 3+ consecutive business days without actioning a Duo lead. List rep name and streak length. Weekends and holidays do not count toward the streak.

If no reps meet the threshold, note: "All reps active this week."

**Section 6: Dismiss Analysis (this week)**

| Reason | Count | % of Dismisses |
| --- | --- | --- |
| Bad lead | [n] | [%] |
| Bad company | [n] | [%] |
| Bad signal | [n] | [%] |
| Other | [n] | [%] |

Cross-reference dismiss reasons with signal types. If a single signal type accounts for more than 40% of all dismisses, call it out: "Signal [X] is driving [Y%] of all dismisses this week. Consider reviewing this signal's targeting criteria."

**Section 7: Alerts** (only if thresholds are breached)

- Dismiss rate alert: "Dismiss rate hit [X%], above the [threshold%] threshold. Top contributor: [signal type] at [Y%] dismiss rate."
- Inactivity alert: "[Rep name] has not actioned a Duo lead in [N] business days."
- Signal quality alert: "[Signal type] has [N] leads generated but [X%] interested rate over the last 30 days. Underperforming."

If no thresholds are breached, omit this section entirely.

1. **Format for Slack** using Slack mrkdwn syntax. Structure the message as:
    - Bold header: `*Duo Performance Report -- Week of [date range]*`
    - Each section as a separate block with a bold section title
    - Tables formatted with monospace blocks for alignment
    - Alerts formatted with `:warning:` emoji and bold text
    - Footer: `_Report generated automatically via Amplemarket MCP. Reply in thread to drill deeper._`
2. **Post to Slack** by calling the Slack MCP send message tool with:
    - `channel`: the configured channel
    - `message`: the formatted report
    
    If the Slack post fails, retry once. If it fails again, notify the user directly.
    

### Important Notes

- Submit all analytics queries in parallel to minimize wait time. The report depends on ~14 queries.
- Activity metrics (generated, actioned, dismissed, rep leaderboard, inactivity) are reported on the current week because they reflect immediate behavior.
- Performance/outcome metrics (interested replies, meetings, signal interested rate) use a 30-day rolling window because leads need time to mature -- a lead sequenced today may not get a reply for 1-2 weeks. The 30-day window ensures outcomes are measured fairly.
- Week-over-week comparison applies to activity metrics only. Outcome metrics shift naturally as the 30-day window rolls forward.
- The 4 dismiss reasons (Bad lead, Bad company, Bad signal, Other) are the values stored in the system. If dismiss reasons skew heavily toward "Other", it may mean reps are not selecting specific reasons -- flag this as a data quality note.
- Inactivity streaks should only count business days. Weekends and company holidays do not count.
- If the account has multiple teams and the user configured per-team reports, submit separate analytics queries scoped to each team and post separate Slack messages. Do not combine teams.
- Keep the Slack message scannable. Lead with outcomes and activity, then signal quality, then rep-level detail, then dismiss analysis. Alerts go last but are visually prominent.
- If analytics data is partially unavailable, post the report with available data and note which sections are incomplete: "*Signal performance data is still processing. Will update when available.*"

## Examples

### Example 1: Standard Weekly Report (Healthy Week)

**Recurring prompt:** "Using Amplemarket's MCP, check team performance with Duo Copilot and report back to #sales-duo-insights on a weekly basis. Full team. Flag if dismiss rate exceeds 40%."

**What the skill does:**

1. Submits 14 analytics queries (7 current week + 3 prior week + 4 rolling 30-day) via `mcp__claude_ai_Amplemarket__ask_analytics`.
2. Waits 20 seconds, polls all results via `mcp__claude_ai_Amplemarket__get_analytics_result`.
3. Compiles the report.
4. Posts to `#sales-duo-insights` via Slack MCP.

**Example Slack message:**

> *Duo Performance Report -- Week of Mar 3-9, 2026*
> 

> 
> 

> *Outcomes (last 30 days)*
> 

> 
> 

> Interested replies from Duo: 142
> 

> Meetings booked from Duo: 38
> 

> 
> 

> *Activity (this week)*
> 

> 
> 

> Leads generated: 280 (last week: 265, +5.7%)
> 

> Leads actioned: 188 (last week: 175, +7.4%)
> 

> Dismiss rate: 28% (last week: 31%, -3 pts)
> 

> 
> 

> *Signal Performance (last 30 days)*
> 

> 
> 

> By volume: Job Change (512), Funding Round (348), Hiring Surge (290)
> 

> By interested/reply rate: Funding Round (8.9% / 14.2%), Job Change (6.5% / 11.8%), Tech Adoption (5.2% / 9.1%)
> 

> 
> 

> *Rep Leaderboard (this week)*
> 

> 
> 

> Sarah Chen: 48 (+6), James Wilson: 41 (+3), Maria Lopez: 37 (-2), Alex Patel: 33 (+8), David Kim: 29 (+1)
> 

> 8 additional reps actioned between 12-25 leads each.
> 

> 
> 

> *Rep Inactivity*
> 

> All reps active this week.
> 

> 
> 

> *Dismiss Analysis (this week)*
> 

> 
> 

> Bad lead: 34 (37%), Bad company: 22 (24%), Bad signal: 18 (20%), Other: 18 (20%)
> 

> No single signal type dominating dismisses. Distribution is healthy.
> 

> 
> 

> *Report generated automatically via Amplemarket MCP. Reply in thread to drill deeper.*
> 

---

### Example 2: Report with Alerts (Problem Week)

**Same configuration as above.**

**Example Slack message:**

> *Duo Performance Report -- Week of Mar 3-9, 2026*
> 

> 
> 

> *Outcomes (last 30 days)*
> 

> 
> 

> Interested replies from Duo: 89
> 

> Meetings booked from Duo: 19
> 

> 
> 

> *Activity (this week)*
> 

> 
> 

> Leads generated: 310 (last week: 265, +17.0%)
> 

> Leads actioned: 142 (last week: 175, -18.9%)
> 

> Dismiss rate: 47% (last week: 31%, +16 pts)
> 

> Volume is up but actioning is down. Dismiss rate spiked significantly.
> 

> 
> 

> *Signal Performance (last 30 days)*
> 

> 
> 

> By volume: Hiring Surge (580), Job Change (310), Funding Round (185)
> 

> By interested/reply rate: Funding Round (7.1% / 12.4%), Job Change (4.8% / 9.6%), Hiring Surge (0.7% / 2.1%)
> 

> :warning: Hiring Surge has 580 leads but only 0.7% interested rate over 30 days. Underperforming.
> 

> 
> 

> *Rep Leaderboard (this week)*
> 

> 
> 

> Top: Sarah Chen: 52 (+8), James Wilson: 44 (+5), Maria Lopez: 15 (-18)
> 

> Bottom: Alex Patel: 12 (-15), David Kim: 8 (-21), Nina Patel: 5 (-9)
> 

> Activity concentrated in top 2 reps.
> 

> 
> 

> *Rep Inactivity*
> 

> David Kim: 4 business days inactive
> 

> Alex Patel: 3 business days inactive
> 

> 
> 

> *Dismiss Analysis (this week)*
> 

> 
> 

> Bad signal: 82 (55%), Bad lead: 28 (19%), Bad company: 24 (16%), Other: 14 (9%)
> 

> "Bad signal" is the dominant reason at 55% of all dismisses. 78% of "Bad signal" dismisses came from Hiring Surge.
> 

> 
> 

> :warning: *Alerts*
> 

> - *Dismiss rate at 47%*, above the 40% threshold. Hiring Surge signal is the primary driver -- 78% of "Bad signal" dismisses trace back to this signal type.
> 

> - *David Kim* has not actioned a Duo lead in 4 business days.
> 

> - *Hiring Surge* has 580 leads generated (30-day) but only 0.7% interested rate. Review targeting criteria for this signal.
> 

> 
> 

> *Report generated automatically via Amplemarket MCP. Reply in thread to drill deeper.*
> 

---

### Example 3: Per-Team Reports

**Recurring prompt:** "Post weekly Duo reports for the Sales team to #sales-duo and the SDR team to #sdr-duo. Flag if dismiss rate exceeds 35% for SDRs or 45% for Sales."

**What the skill does:**

1. Submits analytics queries scoped to each team separately.
2. Compiles separate reports per team.
3. Posts the Sales team report to `#sales-duo` and the SDR team report to `#sdr-duo`.
4. Each report follows the same structure but with team-specific data and alert thresholds.

Cross-team comparison is not included in individual reports. If asked in a thread, offer to compare.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Analytics results still processing after 3 attempts | Post the report with available data. Note incomplete sections: "*Signal performance data is still processing. Will update when available.*" If outcomes and activity sections are both unavailable, delay by 10 minutes and retry once before posting a partial report. |
| Slack channel not found or post fails | Verify the channel name and that the bot has been invited. Private channels require the Slack MCP app to be a member. Retry once, then notify the user directly: "Could not post the Duo report to #channel. Check channel permissions." |
| No Duo activity this week | Post a short report: "No Duo leads were generated or actioned this week. This may indicate Duo is not enabled, signals are paused, or the team has not logged in." Flag as an alert. |
| Dismiss reasons skew heavily toward "Other" | Note in the report: "72% of dismisses are categorized as 'Other'. Reps may not be selecting specific dismiss reasons. Encourage reps to choose Bad lead, Bad company, or Bad signal for better diagnostics." |
| Prior week data not available (first run) | Skip the week-over-week comparison columns for activity metrics. Note: "First report -- weekly comparisons will begin next week." The 30-day rolling window for outcomes should still have data. |
| Too many reps to fit in the leaderboard | Show the top 10 and bottom 3. Summarize the middle: "12 additional reps actioned between 15-30 leads each." |