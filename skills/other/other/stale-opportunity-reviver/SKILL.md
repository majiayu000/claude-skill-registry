---
name: stale-opportunity-reviver
description: >
  Find open HubSpot deals that have gone stale, verify contacts are still in their roles, research company news for fresh angles, and generate revival outreach to re-engage dormant pipeline.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Pipeline Management"
compatibility: Requires Amplemarket MCP server
---

# Stale Opportunity Reviver

Find open HubSpot deals that have gone stale, verify contacts are still in their roles, research company news for fresh angles, and generate revival outreach to re-engage dormant pipeline.

## Instructions

When a user wants to identify and revive stale opportunities, systematically pull deal data from HubSpot, enrich contacts, research companies, and produce a prioritized revival plan.

### Steps

1. **Gather revival parameters** by asking the user:
    
    **(a) "How many days of inactivity makes a deal stale?"** Offer defaults:
    
    - 14 days (aggressive, for fast sales cycles)
    - 30 days (standard, for mid-market deals)
    - 60 days (conservative, for enterprise deals)
    - Custom number of days
    
    **(b) "Which deal stages should I look at?"** Common options:
    
    - All open stages
    - Specific stages (e.g., "Qualification", "Proposal Sent", "Negotiation")
    - Exclude early-stage (e.g., skip "Appointment Scheduled")
    
    **(c) "Is there a minimum deal amount?"** Accept a dollar threshold or "any amount".
    
    **(d) "Filter by deal owner?"** Accept an owner name/email or "all owners".
    
2. **Retrieve the current user's identity** by calling `mcp__claude_ai_HubSpot__get_user_details` to get the authenticated user's name, email, and HubSpot user ID. This is needed if the user wants to filter by "my deals" or if you need to resolve owner references.
3. **Discover relevant deal properties** by calling `mcp__claude_ai_HubSpot__search_properties` with:
    - `object_type`: "deals"
    - `query`: "activity" or "last" to find date fields like `notes_last_updated`, `hs_last_sales_activity_date`, `hs_lastmodifieddate`
    
    Also search for stage and amount properties to confirm their field names:
    
    - `query`: "stage" to confirm `dealstage`
    - `query`: "amount" to confirm `amount`
    
    This ensures you use the correct property names for filtering and retrieval.
    
4. **Search for stale deals** by calling `mcp__claude_ai_HubSpot__search_crm_objects` with:
    - `object_type`: "deals"
    - `filter_groups`: Build filters combining:
        - Deal pipeline stage is not "closedwon" and not "closedlost" (open deals only)
        - Last activity date is before the staleness threshold (today minus X days)
        - Amount is greater than or equal to the minimum (if specified)
        - Owner ID matches the specified owner (if specified)
    - `properties`: ["dealname", "amount", "dealstage", "pipeline", "hubspot_owner_id", "hs_lastmodifieddate", "notes_last_updated", "hs_last_sales_activity_date", "closedate", "createdate"]
    - `limit`: 50
    
    If the user specified deal stages, add a `dealstage` filter with `operator`: "IN" and the matching stage IDs.
    
5. **Calculate staleness for each deal.** For each returned deal:
    - Determine the last activity date from whichever is most recent: `hs_last_sales_activity_date`, `notes_last_updated`, or `hs_lastmodifieddate`
    - Calculate days since last activity
    - Sort deals by staleness (most stale first)
6. **Retrieve associated contacts** by calling `mcp__claude_ai_HubSpot__get_crm_objects` with:
    - `object_type`: "contacts"
    - `object_ids`: IDs of contacts associated with the stale deals
    - `properties`: ["firstname", "lastname", "email", "jobtitle", "company", "phone", "hs_lead_status"]
    - `associations`: ["deals"]
    
    Alternatively, for each deal, call `mcp__claude_ai_HubSpot__search_crm_objects` with `object_type`: "contacts" and filter by associated deal ID to find related contacts.
    
7. **Resolve deal owners** by calling `mcp__claude_ai_HubSpot__search_owners` with the `hubspot_owner_id` values from the deals to get owner names and emails. This maps owner IDs to human-readable names for the output.
8. **Enrich contacts to verify current status** by calling `mcp__claude_ai_Amplemarket__enrich_person` for the primary contact on each stale deal (limit to top 10-15 deals to manage credit usage):
    - Use `email` or `linkedin_url` from the HubSpot contact record
    - Set `reveal_email`: true
    - Compare the enriched current company and title against the HubSpot record
    - Flag contacts who have left the company. These deals need a new contact strategy
9. **Research company news for revival hooks** by calling `WebSearch` for the top 10 stale deal companies:
    - Query: "[Company Name] news [current year]" or "[Company Name] announcement [current quarter]"
    - Look for trigger events: new funding, product launches, leadership changes, expansion, earnings reports
    - These provide fresh conversation starters for re-engagement
10. **Build the prioritized revival list.** Score each stale deal on revival priority:
- **High Priority:** Large deal + contact still there + recent company news (fresh hook available)
- **Medium Priority:** Moderate deal + contact still there but no news, OR large deal but contact has left
- **Low Priority:** Small deal + no news + contact may have left
    
    Present the output with:
    
- Executive summary (total stale deals, total pipeline value at risk, distribution by priority)
- Priority-ordered deal table with all dynamic fields
- Per-deal revival recommendations with suggested openers
- Flagged deals where the contact has left (need new champion)

### Important Notes

- Limit `enrich_person` calls to the top 10-15 deals by amount to manage Amplemarket credit usage. For larger batches, warn the user: "I found X stale deals. Enriching all contacts would use X credits. Shall I focus on the top 10-15 by deal size?"
- If the HubSpot account uses custom deal stages, the stage names may not match standard labels. Use `search_properties` to discover the actual stage values.
- Deals with no associated contacts should be flagged separately: "This deal has no contacts. It may need manual review in HubSpot."
- The staleness calculation depends on which activity date fields are populated. If `hs_last_sales_activity_date` is empty, fall back to `notes_last_updated`, then `hs_lastmodifieddate`.
- When a contact has left the company, do not suggest re-engaging them at the old company. Instead, recommend finding a replacement contact or using the deal-contact-gap-analysis skill.

## Dynamic Fields Generated

The following dynamic fields are populated for each stale deal and can be used in revival outreach templates:

| Field | Description | Example Value |
| --- | --- | --- |
| `{{deal_name}}` | Name of the stale HubSpot deal | "Acme Corp - Enterprise License" |
| `{{deal_amount}}` | Deal value in dollars | "$125,000" |
| `{{deal_stage}}` | Current deal pipeline stage | "Proposal Sent" |
| `{{deal_days_stale}}` | Number of days since last activity | "47 days" |
| `{{deal_contact_name}}` | Primary contact name on the deal | "Sarah Martinez" |
| `{{deal_contact_still_there}}` | Whether the contact is still at the company | "Yes - same role" or "No - left company" |
| `{{deal_company_recent_news}}` | Recent company news or trigger events | "Raised $40M Series C in Feb 2026" |
| `{{deal_revival_hook}}` | A relevant hook based on news or context | "Post-funding scaling initiatives" |
| `{{deal_suggested_opener}}` | Personalized opening line for re-engagement | "Hi Sarah, saw Acme just closed your Series C. Congrats!..." |
| `{{deal_owner}}` | Name of the deal owner in HubSpot | "James Rodriguez" |
| `{{deal_last_activity_date}}` | Date of the last recorded activity | "2026-01-21" |
| `{{deal_contact_current_title}}` | Contact's current verified title from enrichment | "VP of Operations" |
| `{{deal_pipeline_value_at_risk}}` | Total value of stale pipeline for this owner | "$485,000" |

## Examples

### Example 1: Standard 30-Day Stale Deal Review

**User prompt:** "Find my deals with no activity in the last 30 days. My email is jrodriguez@ourcompany.com"

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__get_user_details` to confirm the user identity.
2. Calls `mcp__claude_ai_HubSpot__search_properties` with `object_type`: "deals", `query`: "activity" to find the correct last-activity date field.
3. Calls `mcp__claude_ai_HubSpot__search_crm_objects` with `object_type`: "deals", filtering for open deals owned by jrodriguez@ourcompany.com with last activity before 2026-02-07.
4. Calls `mcp__claude_ai_HubSpot__get_crm_objects` for associated contacts.
5. Calls `mcp__claude_ai_HubSpot__search_owners` to resolve owner names.
6. Calls `mcp__claude_ai_Amplemarket__enrich_person` for the primary contact on the top 10 deals.
7. Calls `WebSearch` for recent news on each deal's company.
8. Produces the prioritized revival list.

**Example output:**

---

**STALE OPPORTUNITY REPORT - James Rodriguez**

**Executive Summary**
- Stale deals (30+ days no activity): 8
- Total pipeline at risk: $742,000
- High priority: 3 | Medium priority: 3 | Low priority: 2
- Contacts who left their company: 1 (needs new champion)

**Priority Revival Table**

| Priority | Deal | Amount | Stage | Days Stale | Contact | Still There? | Revival Hook | Suggested Opener |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| High | Acme Corp - Enterprise | $185,000 | Negotiation | 34 days | Sarah Martinez, VP Ops | Yes | Raised $40M Series C (Feb 2026) | "Hi Sarah, congrats on the Series C. With the growth ahead, I'd love to revisit our conversation about scaling operations." |
| High | TechFlow - Platform Deal | $210,000 | Proposal Sent | 41 days | Kevin Park, CTO | Yes | Launched new API marketplace | "Kevin, saw TechFlow just launched the API marketplace. That aligns perfectly with what we discussed. Worth revisiting?" |
| High | DataSync - Annual License | $125,000 | Qualification | 38 days | Maya Patel, Dir Eng | Yes | New CTO hired (Jan 2026) | "Hi Maya, noticed DataSync brought on a new CTO. New leadership often means fresh priorities. Shall we reconnect?" |
| Medium | CloudBase - Starter | $92,000 | Demo Scheduled | 45 days | Tom Rivera, VP Sales | Yes | No recent news | "Tom, we had a great demo conversation last month. Wanted to check if priorities have shifted or if there's a better time to reconnect." |
| Medium | FinServ - Expansion | $65,000 | Proposal Sent | 52 days | Rachel Kim, CFO | No - left company | N/A | Flag: Contact has left. Find new champion via deal-contact-gap-analysis. |
| Medium | NovaTech - Pilot | $35,000 | Qualification | 37 days | Alex Wu, Head of IT | Yes | Office expansion to Austin | "Alex, saw NovaTech is expanding to Austin. Scaling infrastructure across locations is exactly where we help." |
| Low | SmallCo - Starter | $15,000 | Appointment Set | 60 days | Jamie Lee, Founder | Yes | No recent news | "Hi Jamie, wanted to follow up on our conversation. Is this still a priority for your team?" |
| Low | MicroTech - Basic | $15,000 | Qualification | 55 days | Chris Tan, CEO | Yes | No recent news | "Chris, checking in on our earlier conversation. Has anything changed on your end?" |

**Action Items:**
1. FinServ deal ($65K) needs a new contact. Rachel Kim has left the company. Use deal-contact-gap-analysis to find a replacement.
2. Top 3 deals represent $520K in pipeline. Prioritize revival outreach this week.
3. TechFlow and DataSync both have strong trigger events. They are the best candidates for immediate re-engagement.

---

### Example 2: Enterprise Deals Over $100K Stale for 60+ Days

**User prompt:** "Which opportunities over $100K have been stuck for more than 60 days? Show me across all reps."

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__get_user_details` to get authenticated user context.
2. Calls `mcp__claude_ai_HubSpot__search_properties` to discover activity date fields.
3. Calls `mcp__claude_ai_HubSpot__search_crm_objects` filtering for open deals with amount >= 100000 and last activity before 60 days ago, without owner filter.
4. Resolves all deal owners via `mcp__claude_ai_HubSpot__search_owners`.
5. Enriches top contacts and searches for company news.
6. Groups results by deal owner for management review.

**Example output (abbreviated):**

---

**STALE ENTERPRISE DEALS - All Owners (60+ Days, $100K+)**

Summary: 5 deals | $1.2M total pipeline at risk | 3 owners affected

| Owner | Deal | Amount | Days Stale | Contact Status | Revival Hook |
| --- | --- | --- | --- | --- | --- |
| James Rodriguez | Acme Corp - Enterprise | $185,000 | 64 days | Still there | Series C funding |
| Lisa Chen | MegaCorp - Platform | $350,000 | 72 days | Still there | New VP of Engineering hired |
| Lisa Chen | GlobalTech - Suite | $280,000 | 88 days | Left company | Need new champion |
| David Park | EnterpriseOne - License | $245,000 | 69 days | Still there | Expansion to EMEA |
| David Park | BigScale - Annual | $140,000 | 91 days | Still there | No recent news |

**Owner Breakdown:**
- **Lisa Chen:** 2 stale deals ($630K). GlobalTech contact has left. Assign new champion immediately. MegaCorp has a strong hook with the new VP Eng hire.
- **David Park:** 2 stale deals ($385K). EnterpriseOne EMEA expansion is a timely hook. BigScale needs a creative re-approach.
- **James Rodriguez:** 1 stale deal ($185K). Series C funding provides a natural re-entry point.

**Recommended Management Actions:**
1. Schedule pipeline review with Lisa Chen. $630K at risk across 2 deals, one with a departed contact.
2. Prioritize MegaCorp and EnterpriseOne for immediate outreach. Both have strong trigger events.
3. BigScale ($140K, 91 days stale) may need to be reclassified. Consider whether it is still a viable opportunity.
4. Consider running a team-wide stale deal review weekly to catch deals before they exceed 60 days of inactivity.

---

### Example 3: Stale Deals in Specific Stage

**User prompt:** "Find deals stuck in Proposal Sent stage for more than 14 days"

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__get_user_details`.
2. Calls `mcp__claude_ai_HubSpot__search_properties` with `query`: "stage" to find the stage property and its options.
3. Calls `mcp__claude_ai_HubSpot__search_crm_objects` filtering for `dealstage` = "proposalpendingreview" (or equivalent ID) and last activity > 14 days ago.
4. Enriches contacts and researches companies.
5. Presents results focused on proposal follow-up strategies.

**Example output (abbreviated):**

---

**STALE PROPOSALS - Deals in "Proposal Sent" (14+ Days)**

Summary: 6 deals stuck in proposal stage | $430K total value

| Deal | Amount | Days Since Proposal | Contact | Suggested Follow-Up |
| --- | --- | --- | --- | --- |
| Acme Corp | $125,000 | 18 days | Sarah Martinez | Reference their Series C and offer a revised timeline aligned with growth plans |
| CloudBase | $92,000 | 22 days | Tom Rivera | Ask if there are specific concerns or if a technical deep-dive would help |
| DataPipe | $78,000 | 16 days | Jordan Lee | Share a relevant case study from their industry |

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| No stale deals found | Fallback chain: 1) Verify the staleness threshold. 14 days may be too aggressive for enterprise cycles. Try extending to 30 or 60 days. 2) Check that `hs_last_sales_activity_date` is populated in HubSpot. Some accounts track activity differently. Try filtering on `hs_lastmodifieddate` instead. 3) Remove the deal amount filter to check if deals exist below the threshold. 4) Remove the owner filter to search across all reps. |
| Activity date fields are empty | Some HubSpot configurations do not populate `hs_last_sales_activity_date`. Call `mcp__claude_ai_HubSpot__search_properties` with `query`: "date" or "modified" to discover alternative date fields. Fall back to `hs_lastmodifieddate` which is always populated but includes system updates, not just sales activity. |
| Deal stage IDs do not match expected names | HubSpot uses internal stage IDs (e.g., "appointmentscheduled") rather than display names. Call `mcp__claude_ai_HubSpot__search_properties` with `query`: "dealstage" to retrieve the property definition including all stage options with their internal values and labels. Map user-provided stage names to internal IDs before filtering. |
| Contact enrichment shows different company | This means the contact has left the deal company. Flag the deal as needing a new champion. Suggest the user find a replacement via the deal-contact-gap-analysis skill or manually update the HubSpot contact. Do not suggest re-engaging the contact at the old company. |
| Too many stale deals returned (50+) | Apply stricter filters: increase the minimum amount, narrow to specific stages, or filter by owner. Offer to batch: "I found X stale deals. Shall I focus on the top 15 by deal value and enrich those first?" |
| Owner ID cannot be resolved | If `mcp__claude_ai_HubSpot__search_owners` returns no results for an owner ID, display the raw ID and note: "Owner could not be resolved. This may be a deactivated user or an integration-created record." |
| WebSearch returns no company news | This is common for smaller or private companies. Set `{{deal_company_recent_news}}` to "No recent public news found" and use a generic revival opener based on the deal context instead. Suggest the user check the company's LinkedIn page for recent posts. |
| Deal has no associated contacts | Flag the deal separately: "This deal has no contacts in HubSpot. It cannot be revived without a contact. Consider adding a contact manually or searching for decision-makers via Amplemarket." |