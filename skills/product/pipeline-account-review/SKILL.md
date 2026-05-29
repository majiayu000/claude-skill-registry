---
name: pipeline-account-review
description: >
  Audit pipeline accounts by analyzing engagement data, mapping stakeholders, identifying gaps, and prioritizing next actions.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Account Intelligence"
compatibility: Requires Amplemarket MCP server
---

# Pipeline Account Review

Audit pipeline accounts by analyzing engagement data, mapping stakeholders, identifying gaps, and prioritizing next actions.

## Instructions

When a user wants to review their pipeline, systematically analyze each account and produce an actionable summary.

### Steps

1. **Retrieve accounts** by calling `mcp__claude_ai_Amplemarket__list_accounts` with relevant filters:
    - `owner_email` if the user wants to review their own accounts
    - `tags` if filtering by segment or category
    - `name` or `domain` if looking at specific accounts
    - Set `page_size` to 20 for a manageable review batch
    
    If no filters are specified, ask the user: "Would you like to review all accounts, or filter by owner, tags, or specific accounts?"
    
2. **Get detailed data for each account** by calling `mcp__claude_ai_Amplemarket__get_account` for each account ID returned. Extract:
    - Engagement stats (emails sent, opens, replies, meetings booked)
    - CRM opportunity data (stage, amount, close date)
    - AI-generated insights
    - Account tags and owner
    - Last activity date
3. **Map stakeholders at key accounts** by calling `mcp__claude_ai_Amplemarket__search_people` for the top-priority accounts with:
    - `company_domains`: [account domain]
    - `person_seniorities`: ["C-Suite", "VP", "Head", "Director", "Manager"]
    - `full_output`: true
    - `page_size`: 10
    
    Compare found stakeholders against the contacts already engaged (from account data) to identify gaps in the buying committee.
    
4. **Score account health** for each account on a scale of 1-10 based on:
    - **Engagement recency** (3 points): Last activity within 7 days = 3, within 30 days = 2, within 90 days = 1, older = 0
    - **Engagement depth** (3 points): Replies received = 3, opens only = 1, no engagement = 0
    - **Stakeholder coverage** (2 points): 3+ stakeholders engaged = 2, 1-2 = 1, none = 0
    - **Pipeline stage** (2 points): Active opportunity = 2, prospecting = 1, no opportunity = 0
5. **Classify each account** into priority tiers:
    - **Hot (8-10):** Active engagement, strong multi-threading, opportunity in pipeline
    - **Warm (5-7):** Some engagement but gaps in coverage or stalled momentum
    - **Cold (1-4):** No recent engagement, limited stakeholder access, no active opportunity
    - **At Risk:** Previously warm/hot but engagement has dropped significantly
6. **Generate recommended actions** for each account:
    - Hot: Advance the deal. Suggest specific next steps
    - Warm: Re-engage or multi-thread. Identify who to contact and with what message
    - Cold: Re-evaluate fit or re-approach. Suggest new angles or stakeholders
    - At Risk: Urgent action needed. Specific recovery plays
7. **Format the pipeline review** with:
    - Executive summary (total accounts, distribution by tier, key trends)
    - Priority-ordered account table with health scores
    - Detailed recommendations per account
    - Stakeholder gap analysis

### Important Notes

- Limit the detailed stakeholder search (step 3) to the top 5-10 accounts to avoid excessive API calls.
- If reviewing a large pipeline, offer to paginate: "You have 45 accounts. Shall I review the first 20 and then continue?"
- Adjust health scoring criteria if the user specifies their own definitions of engagement quality.

## Customizing Health Score Thresholds

The default thresholds (7-day / 30-day / 90-day engagement windows) work for typical mid-market sales cycles of 30-60 days. Adjust them for different selling motions:

- **Enterprise sales (90-180 day cycles):** Relax recency thresholds. Last activity within 30 days = 3 points (instead of 7 days). Within 90 days = 2. Within 180 days = 1. Enterprise deals naturally have longer gaps between touchpoints.
- **SMB / transactional sales (7-21 day cycles):** Tighten thresholds. Last activity within 3 days = 3 points. Within 7 days = 2. Within 14 days = 1. Stale SMB deals are likely dead.
- **PLG / product-led motions:** Add product usage signals if available. Deprioritize outbound engagement metrics and weight pipeline stage and stakeholder coverage more heavily.

Tell the user: "I'm using default health scoring for a mid-market sales cycle. Want me to adjust thresholds for your typical deal length?"

## Examples

### Example 1: Full Pipeline Review

**User prompt:** "Review my pipeline - my email is rep@ourcompany.com"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__list_accounts` with `owner_email`: "rep@ourcompany.com".
2. Calls `mcp__claude_ai_Amplemarket__get_account` for each account.
3. Calls `mcp__claude_ai_Amplemarket__search_people` for top accounts to find stakeholder gaps.
4. Produces the pipeline review.

**Example output:**

---

**PIPELINE REVIEW - rep@ourcompany.com**

**Executive Summary**
- Total accounts: 18
- Hot: 3 | Warm: 7 | Cold: 5 | At Risk: 3
- Average engagement score: 5.2/10
- Key concern: 3 previously active accounts have gone silent in the last 30 days.

**Account Priority Table**

| Rank | Account | Health | Tier | Stage | Engaged Contacts | Last Activity | Top Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Acme Corp | 9/10 | Hot | Negotiation | 4 | 2 days ago | Send revised proposal |
| 2 | TechFlow | 8/10 | Hot | Demo Scheduled | 3 | 5 days ago | Prep for demo, loop in CTO |
| 3 | DataPrime | 8/10 | Hot | Evaluation | 3 | 1 day ago | Share case study |
| 4 | CloudBase | 6/10 | Warm | Prospecting | 2 | 12 days ago | Multi-thread to VP Eng |
| 5 | FinServ Inc | 5/10 | Warm | Prospecting | 1 | 20 days ago | Find champion in IT |
| ... | ... | ... | ... | ... | ... | ... | ... |
| 16 | OldCorp | 2/10 | Cold | None | 0 | 90+ days ago | Re-evaluate ICP fit |
| 17 | StaleInc | 3/10 | At Risk | Stalled | 2 | 45 days ago | Breakup email to re-engage |
| 18 | GhostCo | 1/10 | At Risk | Stalled | 1 | 60 days ago | New stakeholder approach |

**Stakeholder Gap Analysis (Top 5 Accounts)**

| Account | Engaged Roles | Missing Roles | Action |
| --- | --- | --- | --- |
| Acme Corp | CRO, VP Sales, Dir Ops, CFO | CTO | Search for and engage CTO for technical buy-in |
| TechFlow | VP Eng, Dir Product, CTO | CFO/Finance | Loop in finance before pricing discussion |
| DataPrime | CMO, Dir Marketing, VP Sales | CTO/IT | No technical evaluator - find one before POC |
| CloudBase | VP Eng, Senior Dev | VP/Dir level decision maker | Need executive sponsor |
| FinServ Inc | Dir IT | Everyone else | Single-threaded - high risk, need 2+ more contacts |

---

### Example 2: Filtered Review by Tag

**User prompt:** "Show me account health for my enterprise accounts"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__list_accounts` with `tags`: ["enterprise"].
2. Retrieves and scores each account.
3. Returns a focused enterprise pipeline review.

### Example 3: Stalled Account Identification

**User prompt:** "Which accounts should I focus on this week? I want to find stalled deals."

**What the skill does:**
1. Retrieves all accounts for the user.
2. Scores and classifies each.
3. Filters to "At Risk" and "Warm" tiers with declining engagement.
4. Returns a focused action plan for the 5-7 accounts that need immediate attention this week.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| No accounts returned | Fallback chain: 1) Remove all filters and call `list_accounts` to verify accounts exist. 2) Try without `owner_email` in case the email format is different. 3) Try searching by `tags` or `name` instead. 4) If still empty, inform user: "No accounts found. This may mean accounts haven't been imported into Amplemarket yet." |
| Account details are sparse | Score with available data and explicitly flag which scoring factors were affected. For example: "Engagement score: 0/3 (no activity data available). This score may underrepresent account health if engagement is tracked outside Amplemarket." |
| Too many accounts to review | Offer to batch the review. Start with accounts that have active opportunities, then move to prospecting-stage accounts. |
| Stakeholder search returns too many people | Narrow `person_seniorities` to "C-Suite" and "VP" only for large companies. |
| User wants to take action on a specific account | Pivot to the competitive-account-research skill for a deep dive, or build-targeted-lead-list to add missing stakeholders. |
| Engagement history data seems stale | Flag with: "[Data may be stale - last activity DATE]. This may not reflect recent interactions outside Amplemarket." Then suggest: "Want me to re-enrich this account's contacts for the latest signals?" |
| Person enrichment succeeds but company enrichment fails for a pipeline account | Fallback chain: 1) Use account-level data from `get_account` as the primary source. 2) Try `enrich_company` with domain instead of name. 3) Try the LinkedIn company URL. 4) Score based on internal engagement data and flag: "Company enrichment unavailable - scoring based on internal data only." |