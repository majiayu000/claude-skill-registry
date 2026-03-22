---
name: closed-lost-revival-scanner
description: >
  Scan closed-lost HubSpot deals, research trigger events that occurred since the loss date, score revival potential, and generate re-engagement outreach for the highest-potential opportunities.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Pipeline Management"
compatibility: Requires Amplemarket MCP server
---

# Closed-Lost Revival Scanner

Scan closed-lost HubSpot deals, research trigger events that occurred since the loss date, score revival potential, and generate re-engagement outreach for the highest-potential opportunities.

## Instructions

When a user wants to revisit closed-lost deals and find those worth re-opening, pull deal data from HubSpot, research trigger events, score revival potential, and produce a prioritized re-engagement plan.

### Steps

1. **Gather scanning parameters** by asking the user:
    
    **(a) "What timeframe of closed-lost deals should I scan?"** Offer options:
    
    - Last 3 months (recent losses, highest re-engagement potential)
    - Last 6 months (balanced coverage)
    - Last 12 months (broadest scan, some contacts may have moved)
    - Custom date range
    
    **(b) "Is there a minimum deal size?"** Accept a dollar threshold or "any amount".
    
    **(c) "Filter by close reason?"** Common closed-lost reasons:
    
    - Lost to competitor
    - Budget/timing
    - No decision / went dark
    - Not a good fit
    - All reasons
    
    **(d) "Filter by deal owner?"** Accept an owner name/email or "all owners".
    
2. **Retrieve the current user's identity** by calling `mcp__claude_ai_HubSpot__get_user_details` to get the authenticated user's name, email, and HubSpot user ID. Use this to resolve "my deals" references and map owner filters.
3. **Discover relevant deal properties** by calling `mcp__claude_ai_HubSpot__search_properties` with:
    - `object_type`: "deals"
    - `query`: "closed" to find `closed_lost_reason`, `closedate`, and related fields
    - Also search `query`: "lost" to find custom close reason properties
    
    Identify the exact property names for close date, close reason, and deal stage values for "closedlost".
    
4. **Search for closed-lost deals** by calling `mcp__claude_ai_HubSpot__search_crm_objects` with:
    - `object_type`: "deals"
    - `filter_groups`: Build filters combining:
        - `dealstage` equals the closed-lost stage ID (typically "closedlost")
        - `closedate` is after the start of the user's timeframe
        - `amount` is greater than or equal to the minimum (if specified)
        - `hubspot_owner_id` matches the specified owner (if specified)
        - Close reason matches the filter (if specified and the property exists)
    - `properties`: ["dealname", "amount", "dealstage", "pipeline", "hubspot_owner_id", "closedate", "createdate", "closed_lost_reason", "hs_lastmodifieddate", "notes_last_updated"]
    - `sorts`: [{"propertyName": "amount", "direction": "DESCENDING"}]
    - `limit`: 50
5. **Retrieve associated contacts and companies** by calling `mcp__claude_ai_HubSpot__get_crm_objects` with:
    - `object_type`: "contacts"
    - `object_ids`: contact IDs associated with the closed-lost deals
    - `properties`: ["firstname", "lastname", "email", "jobtitle", "company", "phone", "linkedin_url"]
    
    Also retrieve company information:
    
    - `object_type`: "companies"
    - `object_ids`: company IDs associated with the deals
    - `properties`: ["name", "domain", "industry", "numberofemployees", "city", "state", "country"]
6. **Resolve deal owners** by calling `mcp__claude_ai_HubSpot__search_owners` with the `hubspot_owner_id` values from the deals to map owner IDs to names and emails.
7. **Enrich companies for trigger event detection** by calling `mcp__claude_ai_Amplemarket__enrich_company` for each unique company associated with a closed-lost deal (limit to top 15 by deal amount):
    - Use the company `domain` from HubSpot
    - Extract current firmographics: size, funding, industry, tech stack
    - Compare against what was known at close time to detect changes (growth, funding, tech changes)
8. **Research trigger events since loss date** by calling `WebSearch` for each company:
    - Query: "[Company Name] funding OR announcement OR expansion OR acquisition [year]"
    - Query: "[Company Name] new [CTO OR CEO OR VP] [year]"
    - Focus on events that occurred AFTER the deal was lost. These are the revival triggers
    - Look for: new funding rounds, leadership changes, product launches, expansion, restructuring, M&A activity, competitor issues
9. **Score revival potential** for each closed-lost deal. Assign a score of High, Medium, or Low based on:
    
    **High Revival Potential:**
    
    - Strong trigger event found (new funding, leadership change, competitor issue)
    - Original close reason was timing/budget (not "not a good fit")
    - Contact is still at the company
    - Company has grown since the loss
    
    **Medium Revival Potential:**
    
    - Moderate trigger event or company growth signal
    - Original close reason was "went dark" or "no decision"
    - Contact is still at the company but may have changed roles
    
    **Low Revival Potential:**
    
    - No significant trigger events found
    - Original close reason was "not a good fit" or "lost to competitor" (without competitor issues)
    - Contact has left the company
    - Company has shrunk or faces challenges
10. **Present the prioritized revival list** with:
- Executive summary: total deals scanned, total value, revival potential distribution, top trigger events
- Priority-ordered table with all dynamic fields
- Per-deal revival strategy with suggested openers referencing the trigger event
- Deals grouped by close reason for pattern analysis
- Recommendation on which deals to re-open first

### Important Notes

- Limit company enrichment and WebSearch to the top 15 deals by amount to manage credit usage and execution time. For larger scans, offer to batch: "I found X closed-lost deals. Shall I research the top 15 by deal value first?"
- Trigger events must have occurred AFTER the deal close date to be valid revival signals. A funding round that happened before the loss is not a new trigger.
- When the close reason was "lost to competitor," search specifically for negative news about that competitor (layoffs, outages, price increases, acquisitions) as these are powerful revival hooks.
- Deals closed as "not a good fit" have the lowest revival potential unless the company's situation has fundamentally changed (e.g., massive growth, different use case emerged).
- If the HubSpot account does not have a `closed_lost_reason` property, skip that filter and note: "No close reason data available, so scoring is based on trigger events and contact status only."

## Dynamic Fields Generated

The following dynamic fields are populated for each closed-lost deal and can be used in revival outreach templates:

| Field | Description | Example Value |
| --- | --- | --- |
| `{{revival_deal_name}}` | Name of the closed-lost deal | "MegaCorp - Platform License" |
| `{{revival_deal_amount}}` | Original deal value | "$175,000" |
| `{{revival_close_date}}` | Date the deal was marked closed-lost | "2025-11-14" |
| `{{revival_close_reason}}` | Reason the deal was lost | "Budget - not prioritized this quarter" |
| `{{revival_months_since_lost}}` | Number of months since the deal was lost | "4 months" |
| `{{revival_trigger_event}}` | Category of trigger event detected | "New Funding Round" |
| `{{revival_trigger_detail}}` | Specific details of the trigger event | "Raised $60M Series D led by Tiger Global in Jan 2026" |
| `{{revival_company_change}}` | How the company has changed since the loss | "Grew from 500 to 750 employees; new CTO hired" |
| `{{revival_contact_status}}` | Whether the original contact is still at the company | "Still there, promoted to SVP" |
| `{{revival_priority}}` | Revival priority score | "High" |
| `{{revival_suggested_opener}}` | Personalized opener referencing the trigger event | "Hi Marcus, congrats on the Series D, and with the growth ahead..." |
| `{{revival_source_url}}` | URL of the source for the trigger event | "https://techcrunch.com/2026/01/megacorp-series-d" |
| `{{revival_deal_owner}}` | Name of the original deal owner | "Lisa Chen" |
| `{{revival_original_objection}}` | The objection or blocker that caused the loss | "Budget was frozen for Q4" |

## Examples

### Example 1: Full Revival Scan of Last 6 Months

**User prompt:** "Review our closed-lost deals from the last 6 months. Any worth revisiting? Focus on deals over $50K."

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__get_user_details` to get user context.
2. Calls `mcp__claude_ai_HubSpot__search_properties` with `object_type`: "deals", `query`: "closed" and `query`: "lost" to find relevant properties.
3. Calls `mcp__claude_ai_HubSpot__search_crm_objects` filtering for `dealstage` = "closedlost", `closedate` after 2025-09-09, `amount` >= 50000.
4. Calls `mcp__claude_ai_HubSpot__get_crm_objects` for associated contacts and companies.
5. Calls `mcp__claude_ai_HubSpot__search_owners` to resolve deal owners.
6. Calls `mcp__claude_ai_Amplemarket__enrich_company` for the top 15 deal companies.
7. Calls `WebSearch` for trigger events at each company since their respective close dates.
8. Scores and presents the prioritized revival list.

**Example output:**

---

**CLOSED-LOST REVIVAL SCAN - Last 6 Months ($50K+)**

**Executive Summary**
- Deals scanned: 23
- Total lost pipeline: $2.8M
- High revival potential: 4 deals ($680K)
- Medium revival potential: 8 deals ($920K)
- Low revival potential: 11 deals ($1.2M)
- Top trigger events found: 3 funding rounds, 2 leadership changes, 1 competitor issue

**High Priority Revival Targets**

| Priority | Deal | Amount | Close Date | Close Reason | Trigger Event | Contact Status | Suggested Opener |
| --- | --- | --- | --- | --- | --- | --- | --- |
| High | MegaCorp - Platform | $250,000 | 2025-10-22 | Budget frozen | Raised $60M Series D (Jan 2026) | Marcus Wei, VP Ops, still there, promoted to SVP | "Hi Marcus, congrats on the SVP promotion and the Series D. With fresh budget and a mandate to scale, I'd love to revisit our platform conversation." |
| High | TechFlow - Enterprise | $175,000 | 2025-11-05 | Lost to Competitor X | Competitor X had major outage (Feb 2026) | Kevin Park, CTO, still there | "Kevin, I noticed Competitor X has been having reliability issues lately. We've been investing heavily in uptime guarantees. Worth a fresh look?" |
| High | DataSync - Annual | $145,000 | 2025-12-18 | Went dark | New CTO hired from AWS (Jan 2026) | Maya Patel, Dir Eng, still there | "Hi Maya, saw DataSync brought on a new CTO from AWS. New technical leadership often re-evaluates the stack. Would it be helpful to reconnect?" |
| High | CloudBase - Suite | $110,000 | 2026-01-10 | Timing, Q1 priorities | Company expanded to 3 new markets (Feb 2026) | Tom Rivera, VP Sales, still there | "Tom, saw CloudBase is expanding into new markets. That growth is exactly the use case we discussed. Is the timing better now?" |

**Medium Priority Deals**

| Deal | Amount | Close Date | Close Reason | Signal | Contact Status |
| --- | --- | --- | --- | --- | --- |
| FinServ - Starter | $95,000 | 2025-11-30 | No decision | Company grew 40% YoY | Rachel Kim, left company |
| NovaTech - License | $85,000 | 2025-10-15 | Budget | No strong trigger | Alex Wu, still there |
| BigScale - Platform | $80,000 | 2025-12-01 | Went dark | New VP Sales hired | Jordan Lee, still there |
| ... | ... | ... | ... | ... | ... |

**Pattern Analysis by Close Reason:**
- Budget/timing (9 deals, $1.1M): Highest revival potential. Re-approach when triggers suggest budget availability
- Went dark (7 deals, $850K): Medium potential. New leadership or company changes may create re-entry
- Lost to competitor (4 deals, $520K): Low unless competitor issues found (1 case identified)
- Not a good fit (3 deals, $330K): Lowest potential. Only revisit if fundamental company change

---

### Example 2: Competitor-Loss Revival

**User prompt:** "Find deals we lost to CompetitorX in the last year. Any chance to win them back?"

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__get_user_details`.
2. Calls `mcp__claude_ai_HubSpot__search_properties` to find the close reason property.
3. Calls `mcp__claude_ai_HubSpot__search_crm_objects` filtering for closed-lost deals with close reason containing "CompetitorX" in the last 12 months.
4. Enriches companies and searches for CompetitorX-related negative signals.
5. Scores revival potential based on competitor vulnerabilities.

**Example output (abbreviated):**

---

**COMPETITOR LOSS REVIVAL - Deals Lost to CompetitorX (Last 12 Months)**

Summary: 6 deals lost to CompetitorX | $890K total value | 2 deals show revival potential

| Deal | Amount | Close Date | CompetitorX Vulnerability | Revival Potential |
| --- | --- | --- | --- | --- |
| TechFlow | $175,000 | 2025-11-05 | Major outage Feb 2026, 4hr downtime | High, contact confirmed frustration on LinkedIn |
| DataPipe | $95,000 | 2025-09-20 | CompetitorX raised prices 30% in Q1 2026 | High, budget-sensitive buyer may reconsider |
| CloudSync | $220,000 | 2025-08-15 | No negative signals found | Low |
| ... | ... | ... | ... | ... |

---

### Example 3: Single Owner Revival Focus

**User prompt:** "I want to re-open some old deals. My email is lchen@ourcompany.com. Show me my closed-lost from Q4 last year."

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__get_user_details` and resolves lchen@ourcompany.com to an owner ID.
2. Calls `mcp__claude_ai_HubSpot__search_crm_objects` filtering for closed-lost deals owned by that ID, with close date between 2025-10-01 and 2025-12-31.
3. Enriches companies, researches triggers, scores revival potential.
4. Presents a personal revival action plan for Lisa Chen.

**Example output (abbreviated):**

---

**YOUR CLOSED-LOST REVIVAL PLAN - Lisa Chen (Q4 2025)**

Summary: 7 deals | $645K total lost | 2 high-priority revival targets

| Deal | Amount | Why It Was Lost | What Changed Since | Priority | Next Step |
| --- | --- | --- | --- | --- | --- |
| MegaCorp | $250,000 | Budget frozen | Series D raised ($60M) | High | Re-engage Marcus Wei this week |
| GlobalTech | $120,000 | Went dark | New VP of Procurement hired | High | Approach new VP as fresh entry point |
| SmallCo | $55,000 | Not a good fit | No changes | Low | Skip, original objection still valid |

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| No closed-lost deals found | Fallback chain: 1) Extend the timeframe to 12 months. 2) Remove the amount filter. 3) Remove the owner filter. 4) Check that the closed-lost stage ID is correct. Call `mcp__claude_ai_HubSpot__search_properties` with `query`: "dealstage" to see all stage values. Some HubSpot accounts use custom pipeline stages. |
| Close reason property does not exist | Not all HubSpot accounts configure a close reason field. Skip the close reason filter and note: "No close reason data available in your HubSpot. I'll score based on trigger events and contact status instead." Consider searching `mcp__claude_ai_HubSpot__search_properties` with `query`: "reason" or `query`: "lost" to find custom properties. |
| Trigger events found are before the close date | Only include trigger events that occurred AFTER the deal was lost. Events before the close date are not new information and should not count as revival signals. Filter WebSearch results by date and verify each event's timestamp. |
| Contact has left the company | Flag the deal as needing a new entry point. Search for a replacement contact using `mcp__claude_ai_Amplemarket__search_people` at the deal company, or suggest using the deal-contact-gap-analysis skill. Update the revival opener to reference the company rather than a personal relationship. |
| WebSearch returns no trigger events | This is common for smaller or private companies. Score based on time elapsed and close reason only. Set `{{revival_trigger_event}}` to "No trigger events found" and recommend the user check the company's LinkedIn for recent activity. A deal lost to timing/budget may still be worth a periodic check-in even without a trigger. |
| Too many closed-lost deals to research | Prioritize by deal amount and recency. Offer to batch: "I found X closed-lost deals. Shall I research the top 15 by value first?" Focus enrichment and WebSearch credits on the highest-value opportunities. |
| Deal owner is no longer at the company | If the owner has left, the deal may be unassigned. Note this in the output and suggest the user's manager reassign the deal before re-engagement. Use `mcp__claude_ai_HubSpot__search_owners` to verify owner status. |
| Company enrichment returns very different data | The company may have undergone significant changes (acquisition, rebrand, pivot). This is actually a positive signal. Document the changes in `{{revival_company_change}}` and use them as conversation starters in the revival outreach. |