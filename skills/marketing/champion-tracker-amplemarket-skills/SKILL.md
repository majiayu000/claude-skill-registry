---
name: champion-tracker
description: >
  Track former champions from closed-won HubSpot deals who have moved to new companies, research their new organizations, and generate warm re-engagement outreach leveraging your shared deal history.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Signal Monitoring"
compatibility: Requires Amplemarket MCP server
---

# Champion Tracker

Track former champions from closed-won HubSpot deals who have moved to new companies, research their new organizations, and generate warm re-engagement outreach leveraging your shared deal history.

## Instructions

When a user wants to find former champions who have moved to new companies, pull closed-won deal data from HubSpot, enrich contacts to detect job changes, research the new companies, and produce re-engagement materials.

### Steps

1. **Gather tracking parameters** by asking the user:
    
    **(a) "What timeframe of closed-won deals should I check?"** Offer options:
    
    - Last 6 months (most likely to have recent moves)
    - Last 12 months (balanced coverage)
    - Last 24 months (broadest, more moves expected but older relationships)
    - All time
    
    **(b) "Any specific accounts to focus on?"** Accept:
    
    - Specific company names
    - "All closed-won deals"
    - "My top 20 customers by deal value"
    
    **(c) "What product or solution did you sell?"** This context is used to tailor re-engagement outreach at the new company, e.g., "We helped [previous company] with [solution], and I think [new company] could benefit similarly."
    
2. **Retrieve the current user's identity** by calling `mcp__claude_ai_HubSpot__get_user_details` to get the authenticated user's name, email, and HubSpot user ID. This is used for owner-based filtering and to personalize the outreach voice.
3. **Search for closed-won deals** by calling `mcp__claude_ai_HubSpot__search_crm_objects` with:
    - `object_type`: "deals"
    - `filter_groups`: Build filters for:
        - `dealstage` equals the closed-won stage ID (typically "closedwon")
        - `closedate` is after the start of the user's timeframe
        - `hubspot_owner_id` matches the user (if filtering to "my deals")
    - `properties`: ["dealname", "amount", "dealstage", "pipeline", "hubspot_owner_id", "closedate", "createdate"]
    - `sorts`: [{"propertyName": "amount", "direction": "DESCENDING"}]
    - `associations`: ["contacts", "companies"]
    - `limit`: 50
4. **Retrieve associated contacts** by calling `mcp__claude_ai_HubSpot__get_crm_objects` with:
    - `object_type`: "contacts"
    - `object_ids`: contact IDs associated with the closed-won deals
    - `properties`: ["firstname", "lastname", "email", "jobtitle", "company", "phone", "linkedin_url", "hs_lead_status"]
    
    Also retrieve company data to establish the baseline company for comparison:
    
    - `object_type`: "companies"
    - `object_ids`: company IDs from the deals
    - `properties`: ["name", "domain", "industry", "numberofemployees"]
5. **Resolve deal owners** by calling `mcp__claude_ai_HubSpot__search_owners` with the `hubspot_owner_id` values to map owner IDs to names.
6. **Enrich contacts to detect job changes** by calling `mcp__claude_ai_Amplemarket__enrich_person` for each contact from the closed-won deals:
    - Use `email` or `linkedin_url` from the HubSpot contact record
    - Set `reveal_email`: true to get their current email at the new company
    - Limit to 20-25 contacts per batch to manage credit usage
    
    For each contact, compare:
    
    - **Enriched current company** vs **HubSpot company record** (the company where the deal was closed)
    - Normalize company names (strip Inc., LLC, etc.) and compare domains
    - Classify each contact as: **Moved to New Company**, **Still at Customer**, **Internal Move**, or **Unable to Determine**
7. **For contacts who moved, research the new company** by calling `mcp__claude_ai_Amplemarket__enrich_company` with the new company's domain:
    - Extract firmographics: size, industry, funding, tech stack, headquarters
    - Assess ICP fit: does the new company match your target profile?
    - Note: if the new company is a competitor, existing customer, or known disqualified account, flag this
    
    Then call `WebSearch` for recent company news:
    
    - Query: "[New Company Name] news [current year]"
    - Look for: funding, growth, product launches, challenges, anything that creates a conversation opener
8. **Find additional stakeholders at new companies** by calling `mcp__claude_ai_Amplemarket__search_people` at each new company:
    - `company_domains`: [new company domain]
    - `person_seniorities`: ["C-Suite", "VP", "Director"] or matching your ICP
    - `full_output`: true
    - `page_size`: 5
    - Identify potential multi-threading targets alongside the moved champion
9. **Generate re-engagement materials.** For each moved champion:
    - Populate all `{{champion_*}}` dynamic fields
    - Draft a warm re-engagement message that:
        - Congratulates them on the move
        - References the shared deal history (what you accomplished together at the previous company)
        - Connects your solution to the new company's needs
        - Suggests a casual reconnection (not a hard pitch)
    - Tailor the tone: these are warm relationships, not cold outreach
10. **Present the champion tracking report** with:
- Executive summary: total contacts checked, job changes detected, new companies identified, ICP matches
- Job change table with all dynamic fields for moved champions
- New company profiles with ICP fit assessment
- Per-champion re-engagement strategy and suggested openers
- Champions still at customer (for retention/upsell awareness)
- Offer to create an Amplemarket lead list with the moved champions

### Important Notes

- Champion tracking is the highest-ROI outbound motion. Former champions who know and trust your product convert at 3-5x the rate of cold outreach. Emphasize this in the output.
- Limit `enrich_person` calls to 20-25 contacts per run. For large customer bases, offer to batch: "I found X contacts across your closed-won deals. Shall I check the first 25 for job changes?"
- When a champion has moved to a new company, their previous experience with your product is your biggest asset. Always reference the shared history in suggested openers.
- If a champion moved to one of your existing customer accounts, flag this as a retention/expansion opportunity rather than a new deal opportunity.
- If a champion moved to a known competitor, flag but do not suggest outreach. This requires a different strategy.
- Very recent job changes (within 1-2 weeks) may not be captured in enrichment data. Suggest the user verify via LinkedIn for suspected recent moves.

## Dynamic Fields Generated

The following dynamic fields are populated for each champion who has moved to a new company:

| Field | Description | Example Value |
| --- | --- | --- |
| `{{champion_name}}` | Full name of the champion | "Sarah Chen" |
| `{{champion_previous_company}}` | Company where you closed the deal together | "Notion" |
| `{{champion_previous_role}}` | Their role at the previous company | "Director of Sales" |
| `{{champion_new_company}}` | Company they have moved to | "Rippling" |
| `{{champion_new_role}}` | Their current role at the new company | "VP of Revenue" |
| `{{champion_new_company_size}}` | Employee count of the new company | "1001-5000 employees" |
| `{{champion_new_company_industry}}` | Industry of the new company | "Human Resources Technology" |
| `{{champion_new_company_domain}}` | Domain of the new company | "rippling.com" |
| `{{champion_deal_context}}` | What you sold and accomplished at the previous company | "Enterprise sales engagement platform, helped scale SDR team from 5 to 25" |
| `{{champion_time_at_new_company}}` | Approximate tenure at the new company | "~3 months" |
| `{{champion_new_company_news}}` | Recent news about the new company | "Raised $200M Series E at $13.5B valuation (Jan 2026)" |
| `{{champion_suggested_opener}}` | Warm re-engagement opening line | "Hi Sarah, congrats on the VP of Revenue role at Rippling!..." |
| `{{champion_deal_amount}}` | Value of the deal closed at the previous company | "$85,000" |
| `{{champion_icp_fit}}` | Whether the new company matches your ICP | "Strong fit - right size, industry, and growth stage" |

## Examples

### Example 1: Full Champion Tracking Across Closed-Won Deals

**User prompt:** "Track my champions. Check if any contacts from my closed-won deals in the last 12 months changed jobs. My email is jrodriguez@ourcompany.com. We sell a sales engagement platform."

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__get_user_details` to confirm identity.
2. Calls `mcp__claude_ai_HubSpot__search_crm_objects` for closed-won deals owned by jrodriguez@ourcompany.com in the last 12 months.
3. Calls `mcp__claude_ai_HubSpot__get_crm_objects` for contacts and companies on those deals.
4. Calls `mcp__claude_ai_HubSpot__search_owners` to resolve owner names.
5. Calls `mcp__claude_ai_Amplemarket__enrich_person` for each contact (up to 25) to detect job changes.
6. For moved champions: calls `mcp__claude_ai_Amplemarket__enrich_company` on new company domains.
7. Calls `WebSearch` for news at each new company.
8. Calls `mcp__claude_ai_Amplemarket__search_people` at new companies for multi-threading targets.
9. Presents the champion tracking report.

**Example output:**

---

**CHAMPION TRACKER REPORT - James Rodriguez**

**Executive Summary**
- Closed-won deals checked: 14
- Contacts enriched: 22
- Job changes detected: 4
- Champions at new companies matching ICP: 3
- Estimated pipeline opportunity: $320K (based on previous deal values at 1.5x uplift)
- Champions still at customer: 18 (retention signal, positive)

**Champions Who Moved**

| Champion | Previous Company | Previous Role | New Company | New Role | ICP Fit | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Sarah Chen | Notion | Dir of Sales | Rippling | VP of Revenue | Strong | High |
| Michael Torres | Segment | Sr. Sales Mgr | Databricks | Head of Sales Dev | Strong | High |
| Rachel Green | Gong | Sales Ops Mgr | Clari | Director of Revenue Ops | Strong | High |
| Tom Nakamura | Deel | Account Exec | StartupXYZ | Sales Manager | Weak - company too small | Low |

**Champion Detail: Sarah Chen (Notion → Rippling)**

| Field | Detail |
| --- | --- |
| Previous Deal | Notion - Enterprise License ($85,000, closed 2025-07-15) |
| What You Accomplished | Helped scale SDR team from 5 to 25 reps using your platform |
| New Company | Rippling (rippling.com) |
| New Role | VP of Revenue |
| Company Size | 1001-5000 employees |
| Industry | HR Tech / Workforce Management |
| Time at Rippling | ~3 months |
| ICP Fit | Strong - right size, growth stage, and sales team complexity |
| Recent News | Raised $200M Series E (Jan 2026); Expanding global payroll to 12 markets |
| New Company Email | sarah.chen@rippling.com |

**Additional Stakeholders at Rippling:**
| Name | Title | LinkedIn |
|----|-----|-------|
| Marcus Webb | CRO | linkedin.com/in/mwebb |
| Priya Patel | VP Sales Operations | linkedin.com/in/ppatel |

**Suggested Re-Engagement:**
> "Hi Sarah, congratulations on the VP of Revenue role at Rippling, well deserved! I have fond memories of our work together at Notion scaling the SDR team from 5 to 25. With Rippling's Series E and the global expansion, I imagine you're building out the revenue org at scale. Would love to catch up and see if there's a way we can help at Rippling like we did at Notion. Coffee chat?"

---

**Champion Detail: Michael Torres (Segment → Databricks)** ...

**Champion Detail: Rachel Green (Gong → Clari)** ...

---

**Champions Still at Customer (Retention Check)**
| Champion | Company | Role | Deal | Status |
|-------|------|----|----|-----|
| Emily Watson | Lattice | VP Sales | $120K | Still there, same role |
| David Kim | Figma | Dir Sales Ops | $95K | Still there, promoted to VP |
| Lisa Park | Brex | Sales Manager | $65K | Still there, same role |
| ... | ... | ... | ... | ... |

Note: David Kim was promoted to VP at Figma, a potential upsell opportunity.

---

### Example 2: Specific Account Champion Check

**User prompt:** "Did anyone from our Notion deal leave? That was our biggest win last year."

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__search_crm_objects` for closed-won deals with "Notion" in the deal name.
2. Retrieves all contacts from the Notion deal.
3. Enriches each contact to check for job changes.
4. For any who moved, researches the new company.
5. Returns a focused champion tracking report for the Notion account.

### Example 3: Champion Tracking with Lead List Creation

**User prompt:** "Find champions who left and create a lead list for outreach. Focus on my deals over $50K in the last 18 months."

**What the skill does:**
1. Retrieves closed-won deals > $50K from the last 18 months.
2. Enriches all contacts and detects job changes.
3. Researches new companies and generates re-engagement materials.
4. Asks: "I found 5 champions at new companies. Shall I create an Amplemarket lead list?"
5. Calls `mcp__claude_ai_Amplemarket__create_lead_list` with name "Champion Moves - Q1 2026" and the moved champions' LinkedIn URLs.

**Example output (abbreviated):**

---

**CHAMPION MOVES - Lead List Created**

Lead list "Champion Moves - Q1 2026" created with 5 contacts.

| Champion | New Company | New Role | Context Added |
| --- | --- | --- | --- |
| Sarah Chen | Rippling | VP of Revenue | Previous: Notion, $85K deal, SDR scaling |
| Michael Torres | Databricks | Head of Sales Dev | Previous: Segment, $120K deal, outbound automation |
| Rachel Green | Clari | Dir Revenue Ops | Previous: Gong, $75K deal, pipeline analytics |
| Ana Ruiz | Snowflake | VP of GTM | Previous: dbt Labs, $95K deal, RevOps buildout |
| Chris Park | Figma | Dir of Sales | Previous: Canva, $60K deal, team onboarding |

Each lead includes deal context and suggested opener in the lead list notes. Ready for sequence enrollment.

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| No closed-won deals found | Fallback chain: 1) Extend the timeframe to 24 months or "all time". 2) Remove the owner filter to check across all reps. 3) Verify the closed-won stage ID by calling `mcp__claude_ai_HubSpot__search_properties` with `query`: "dealstage". Some HubSpot accounts use custom win stages. |
| Contact enrichment returns the same company | This means the champion is still at the customer company. Classify as "Still at Customer" and include in the retention section. This is actually positive, as it means your champion is still an advocate. |
| Champion moved to an existing customer | Flag as an expansion opportunity, not a new deal. Note: "[Champion] moved to [Company], which is already a customer. This could be a cross-sell or upsell opportunity." Do not treat this as net-new outreach. |
| Champion moved to a competitor | Flag separately: "[Champion] moved to [Competitor]. This requires a different engagement strategy, as they may have insights but outreach should be handled carefully." Do not include in standard re-engagement. |
| Too many contacts to enrich | Offer to prioritize: "I found X contacts across your closed-won deals. Shall I focus on the top 25 by deal value? This will use approximately 25 Amplemarket credits." Process in batches if the user wants a full scan. |
| Enrichment returns no current data for a contact | Classify as "Unable to Determine." The contact may have left the workforce, started a company, or changed their public profile. Suggest: "Unable to verify current status for [Name]. Check their LinkedIn profile manually." |
| New company does not match ICP | Still include in the report but mark ICP fit as "Weak" or "No Fit." The champion relationship is valuable even if the company is not ideal, as they may refer you to others or move again to a better-fit company. |
| WebSearch returns no news about the new company | Set `{{champion_new_company_news}}` to "No recent public news found." Use the company enrichment data and the champion's role change as the primary outreach angle instead. |
| Deal context is unclear from HubSpot data | If the deal record lacks context about what was sold or accomplished, ask the user: "Can you share what you accomplished with [Champion] at [Previous Company]? This context makes the re-engagement much more effective." |