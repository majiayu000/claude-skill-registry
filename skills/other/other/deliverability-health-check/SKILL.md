---
name: deliverability-health-check
description: >
  Audit your email deliverability by analyzing bounce rates, open rate anomalies, and sending patterns across reps and sequences to catch domain reputation issues early.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Deliverability"
compatibility: Requires Amplemarket MCP server
---

# Deliverability Health Check

Audit your email deliverability by analyzing bounce rates, open rate anomalies, and sending patterns across reps and sequences to catch domain reputation issues early.

## Instructions

When a user wants to check deliverability health, query the Amplemarket analytics engine for bounce and engagement data, classify the overall health status, and flag any reps or sequences that pose a risk.

### Steps

1. **Clarify scope and concerns.** Ask the user:
    - "What timeframe would you like to check? (default: last 30 days)"
    - "Any specific concerns? For example: high bounces, low open rates, or suspected spam folder placement."
    
    If the user does not specify, default to the last 30 days and run a comprehensive check.
    
2. **Submit analytics questions** by calling `mcp__claude_ai_Amplemarket__ask_analytics` for each of the following (adjust the timeframe accordingly):
    - "What is the bounce rate by rep in the last [timeframe]?"
    - "What is the bounce rate by sequence in the last [timeframe]?"
    - "What is the overall bounce rate in the last [timeframe]?"
    - "What are the open rates by rep in the last [timeframe]?"
    - "How many emails were sent vs delivered in the last [timeframe]?"
    
    Store each returned `request_id` for polling.
    
3. **Wait approximately 20 seconds**, then call `mcp__claude_ai_Amplemarket__get_analytics_result` for each `request_id` to retrieve the answers.
4. **Handle pending results.** If any result is still processing, wait another 20 seconds and retry. Repeat up to 3 total attempts per request. Proceed with available data if some results remain unavailable.
5. **Compile the deliverability health report** with three components:
    
    **Overall Health Score:**
    
    - Healthy (below 2% bounce rate): Deliverability is in good shape. No immediate action required.
    - Warning (2-5% bounce rate): Some issues need attention. Investigate the sources of bounces.
    - Critical (above 5% bounce rate): Immediate action required. Domain reputation is at risk.
    
    **Per-Rep Breakdown:**
    
    | Rep | Emails Sent | Bounce Rate | Open Rate | Health Status |
    | --- | --- | --- | --- | --- |
    
    **Per-Sequence Breakdown:**
    
    | Sequence | Emails Sent | Bounce Rate | Open Rate | Health Status |
    | --- | --- | --- | --- | --- |
6. **Flag critical issues** with specific, actionable callouts:
    - Any rep with a bounce rate above 5%: "Marcus has a 6.1% bounce rate. This can damage your sending domain. Investigate his lead sources immediately."
    - Any sequence with a bounce rate above 3%: "Cold Outreach v3 has an 8% bounce rate vs. the 1.5% team average. The lead list feeding this sequence likely contains stale or invalid emails."
    - Any rep or sequence with an open rate below 20%: "An open rate of 15% may indicate emails are landing in spam folders rather than inboxes. Review the sending domain, subject lines, and email content for spam triggers."
7. **Identify patterns and root causes.** Connect the dots between metrics:
    - High bounce + specific sequence = lead list quality issue
    - High bounce + specific rep = that rep may be importing unvalidated lists
    - Low open rate across all reps = potential domain reputation problem
    - Low open rate for one rep only = that rep's email account may have deliverability issues
8. **Generate recommendations** based on the health classification:
    
    **Critical actions:**
    
    - "Pause [sequence/rep] immediately until the bounce rate issue is resolved."
    - "Run all lead lists through email validation before importing."
    - "Check your sending domain's reputation on Google Postmaster Tools and other monitoring services."
    
    **Warning actions:**
    
    - "Enable email validation on future lead list imports to catch invalid addresses before sending."
    - "Review the lead sources for sequences with above-average bounce rates."
    - "Monitor weekly. If bounce rates continue to climb, escalate to critical."
    
    **Healthy maintenance:**
    
    - "Deliverability looks good. Keep monitoring monthly to catch issues early."
    - "Continue validating lead lists before import to maintain this healthy status."
    
    Offer next steps: "Want me to check which lead lists are feeding the high-bounce sequences?" or "Should I run a full team audit to compare deliverability across all reps?"
    

### Important Notes

- Submit all five analytics questions in parallel to minimize wait time.
- Bounce rate is the primary health indicator. Open rate is a secondary signal because privacy features (like Apple Mail Privacy Protection) can inflate open rates, making them less reliable as a standalone metric.
- A bounce rate above 5% is an urgent issue. Always flag this prominently, even if the user asked about something else.
- Very low send volume (under 100 emails) can produce misleading bounce rates. A single bounce out of 20 emails is a 5% bounce rate but may not indicate a real problem. Always consider sample size when classifying health.
- If the user mentions spam complaints, note that Amplemarket analytics may not track spam complaint rates directly. Suggest checking Google Postmaster Tools or similar services for complaint data.

## Examples

### Example 1: Full Deliverability Health Check

**User prompt:** "Check my deliverability. I want to make sure we are not having any issues."

**What the skill does:**
1. Confirms the 30-day default timeframe.
2. Submits five analytics questions via `mcp__claude_ai_Amplemarket__ask_analytics`.
3. Waits 20 seconds, then polls each `request_id` with `mcp__claude_ai_Amplemarket__get_analytics_result`.
4. Compiles the health report with per-rep and per-sequence breakdowns.

**Example output:**

**DELIVERABILITY HEALTH CHECK - Last 30 Days**

**Overall Health: WARNING (2.8% bounce rate)**

Your overall bounce rate of 2.8% is above the healthy threshold of 2%. While not yet critical, this needs attention to prevent domain reputation damage.

**Summary**

| Metric | Value |
| --- | --- |
| Total Emails Sent | 11,240 |
| Total Delivered | 10,925 |
| Total Bounced | 315 |
| Overall Bounce Rate | 2.8% |
| Overall Open Rate | 51.4% |

**Per-Rep Breakdown**

| Rep | Emails Sent | Bounce Rate | Open Rate | Status |
| --- | --- | --- | --- | --- |
| Sarah Chen | 1,820 | 1.1% | 58.2% | Healthy |
| James Wilson | 2,650 | 1.8% | 54.1% | Healthy |
| Maria Lopez | 2,410 | 2.0% | 51.6% | Healthy |
| Alex Patel | 2,200 | 1.9% | 49.8% | Healthy |
| David Kim | 1,950 | 2.4% | 50.3% | Warning |
| Marcus Brown | 1,420 | 6.1% | 38.4% | Critical |

**Per-Sequence Breakdown**

| Sequence | Emails Sent | Bounce Rate | Open Rate | Status |
| --- | --- | --- | --- | --- |
| Q1 Enterprise Outreach | 2,800 | 1.2% | 56.2% | Healthy |
| VP Sales - Pain Point v2 | 2,100 | 1.5% | 52.1% | Healthy |
| Mid-Market SaaS Play | 2,400 | 1.8% | 49.3% | Healthy |
| Inbound Follow-Up | 1,200 | 0.4% | 61.8% | Healthy |
| Cold Outreach v3 | 1,540 | 2.2% | 42.1% | Warning |
| New Logo Prospecting | 1,200 | 8.0% | 32.1% | Critical |

**Critical Issues**

1. **Marcus Brown - 6.1% bounce rate.** This is well above the 2% healthy threshold. His bounce rate alone is pulling the team average into warning territory. His lead sources need immediate review. His low open rate (38.4%) may also indicate some emails are landing in spam.
2. **New Logo Prospecting sequence - 8.0% bounce rate.** This is the primary source of bounce issues. The lead list feeding this sequence likely contains a high percentage of invalid or outdated email addresses. Pause this sequence immediately and validate the email list before resuming.

**Recommendations**
- Pause the "New Logo Prospecting" sequence until the lead list is cleaned and validated.
- Review Marcus Brown's lead import process. He may be adding contacts without email validation.
- Monitor David Kim's bounce rate (2.4%). It is borderline and could worsen.
- The rest of the team and sequences are healthy. No action needed for them.

---

### Example 2: Investigating a Specific Rep

**User prompt:** "Marcus has been getting a lot of bounces. Can you check his deliverability?"

**What the skill does:**
1. Submits analytics questions focused on Marcus's sending activity.
2. Polls results and presents a detailed individual breakdown.

**Example output:**

**DELIVERABILITY REPORT - Marcus Brown (Last 30 Days)**

| Metric | Marcus | Team Avg |
| --- | --- | --- |
| Emails Sent | 1,420 | 2,240 |
| Bounce Rate | 6.1% | 2.8% |
| Open Rate | 38.4% | 51.4% |

Marcus's bounce rate is 3x the team average. Combined with a below-average open rate, this suggests two issues:
1. Lead list quality - many email addresses are invalid or outdated.
2. Possible spam folder placement - the low open rate may indicate mailbox providers are flagging his sends.

**Recommended actions:**
- Immediately audit Marcus's recent lead imports for email validity.
- Pause any sequences Marcus is running until bounce rate is under control.
- Check if Marcus is using a different sending domain or email account that may have reputation issues.
- Run his upcoming lead lists through email validation before adding them to sequences.

---

### Example 3: Clean Bill of Health

**User prompt:** "Quick deliverability check - are we in good shape?"

**What the skill does:**
1. Runs the standard five analytics queries for the last 30 days.
2. Finds all metrics within healthy thresholds.
3. Returns a brief, positive report.

**Example output:**

**DELIVERABILITY HEALTH CHECK - Last 30 Days**

**Overall Health: HEALTHY (1.4% bounce rate)**

Everything looks good. Your bounce rate is well below the 2% threshold, and open rates are healthy across all reps and sequences.

| Metric | Value |
| --- | --- |
| Overall Bounce Rate | 1.4% |
| Overall Open Rate | 53.2% |
| Reps Above 2% Bounce | 0 out of 6 |
| Sequences Above 3% Bounce | 0 out of 5 |

No action needed. Continue monitoring monthly to maintain this healthy status. Keep validating lead lists before import to prevent future issues.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Analytics returns no bounce data | Bounce tracking may not be enabled or data may not be available for the requested period. Check if the analytics engine provides bounce data at all by asking a broader question: "What are the bounce statistics for the last 90 days?" If still unavailable, use open rate as a proxy signal. Very low open rates (below 20%) can indicate deliverability problems even without bounce data. |
| Open rate seems unreliable or inflated | Apple Mail Privacy Protection and similar features can pre-load tracking pixels, inflating open rates. If open rates appear unusually high (above 80%), note this caveat: "Open rates may be inflated by email privacy features. Bounce rate is a more reliable deliverability indicator." Focus recommendations on bounce rate rather than open rate. |
| Very low send volume skews bounce rates | A rep or sequence with fewer than 100 emails may show a misleadingly high bounce rate from just a few bounces. Flag this: "Marcus sent only 30 emails with 2 bounces (6.7% rate). This sample is too small to confirm a deliverability problem. Monitor over the next week as volume increases." Require at least 100 sends before classifying health status. |
| Data not available for the requested timeframe | Try a broader timeframe. If "last 7 days" returns nothing, expand to 30 days. The analytics engine may aggregate data at different intervals. |
| Partial results (some queries succeed, others fail) | Present the available data and note what is missing. For example: "Per-rep bounce rates are available but per-sequence data is still processing. Here is the rep-level analysis." Offer to retry failed queries. |
| User asks about spam complaint rates | Amplemarket analytics may not track spam complaints directly. Suggest: "Spam complaint data is typically available through Google Postmaster Tools, Microsoft SNDS, or your email service provider's dashboard. I can analyze bounce rates and open rates from Amplemarket as proxy indicators." |
| User wants to compare deliverability across time periods | Submit analytics questions for both periods. For example: "What is the bounce rate in the last 30 days?" and "What is the bounce rate from 30-60 days ago?" Present a side-by-side comparison to show whether deliverability is improving or declining. |