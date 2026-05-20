---
name: job-change-signal-tracker
description: >
  Track job changes for key contacts, research their new companies, and generate warm re-engagement outreach based on your prior relationship.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Signal Monitoring"
compatibility: Requires Amplemarket MCP server
---

# Job Change Signal Tracker

Track job changes for key contacts, research their new companies, and generate warm re-engagement outreach based on your prior relationship.

## Instructions

When a user wants to track whether contacts have changed jobs, enrich each contact to detect role or company changes, research the new organization, and produce re-engagement materials with dynamic fields.

### Steps

1. **Gather tracking inputs** by asking the user:
    - 
        1. "Who do you want to track?" Accept any of the following input types. Multiple contacts can be provided at once:
        - **LinkedIn URL** (e.g., `linkedin.com/in/username`)
        - **Email address** (e.g., `jane@acme.com`)
        - **Name + Company** (e.g., "Jane Smith at Acme Corp")
        - **Amplemarket lead list name** (e.g., "Q4 Closed Won Champions")
    - 
        1. "What's the context?" Determine the relationship type. This shapes the re-engagement tone and suggested opener:
        - **Former champion** - warm, familiar tone referencing shared wins
        - **Closed-won contact** - gratitude-based tone referencing successful partnership
        - **Engaged prospect** - professional tone referencing prior conversations
        - **Customer contact** - service-oriented tone referencing ongoing relationship
    - 
        1. "What was their expected company?" The company where the user last interacted with each contact. This baseline is used to detect whether a change has occurred. If a lead list is provided, the expected company is inferred from the list data.
2. **Retrieve contacts from lead list** (if applicable). If the user provided a lead list name, call `mcp__claude_ai_Amplemarket__list_lead_lists` to find the list, then call `mcp__claude_ai_Amplemarket__get_lead_list` with the list `id` to retrieve all contacts and their associated company information. Use the company stored in the list as the expected company for each contact.
3. **Enrich each contact** by calling `mcp__claude_ai_Amplemarket__enrich_person` for every contact with the best available identifier:
    - `linkedin_url` if provided
    - `email` if provided
    - `name` + `company_name` or `company_domain` if provided
    - Set `reveal_email` to `true` to obtain current contact details at the new company.
4. **Compare current data against expected.** For each contact, compare the enriched current company and role against the expected company provided in step 1. Flag a job change when:
    - The current company name or domain differs from the expected company
    - The person's title or department has significantly changed even within the same company (internal move)
    - The enrichment returns no data at the expected company (possible departure)
    
    Classify each contact into one of four categories:
    
    - **Job Change Detected** - contact is now at a different company
    - **Internal Move Detected** - same company but different role, title, or department
    - **No Change** - contact remains at the expected company in the expected role
    - **Unable to Determine** - enrichment data is inconclusive or contact not found
    
    When comparing company names, strip common suffixes (Inc., LLC, Ltd., Corp., Co.) and compare root domains to avoid false positives from naming variations.
    
5. **Research new companies** for contacts with detected job changes:
    - Call `mcp__claude_ai_Amplemarket__enrich_company` with the new company's domain to get firmographics, size, industry, and tech stack.
    - Call `WebSearch` to find recent news about the new company (funding rounds, product launches, leadership changes, acquisitions). Use a query like "[Company Name] news [current year]".
    - Combine both sources into a new company profile that includes:
        - Company overview (name, domain, industry, size, headquarters)
        - Growth signals (recent funding, hiring trends, product launches)
        - Relevance to the user's product or service
6. **Find additional stakeholders** at the new company by calling `mcp__claude_ai_Amplemarket__search_people` with:
    - `company_domains`: [new company domain]
    - `person_seniorities`: ["C-Suite", "VP", "Head", "Director"] or seniorities matching the user's ICP
    - `full_output`: true
    - `page_size`: 10
    - This identifies potential multi-threading targets alongside the moved contact.
7. **Generate re-engagement dynamic fields and draft outreach.** For each contact with a job change:
    - Populate all `{{jobchange_*}}` dynamic fields (see Dynamic Fields Generated below).
    - Draft a re-engagement message that follows this structure:
        - **Opening:** Congratulate the move and reference the past relationship
        - **Bridge:** Connect a recent new company event or challenge to your value proposition
        - **Ask:** Propose a low-commitment next step (quick call, resource share)
    - Tailor tone based on the relationship context from step 1:
        - Champion = warm and familiar, reference specific wins you achieved together
        - Closed-won contact = gratitude-based, reference the successful partnership
        - Engaged prospect = professional and helpful, reference prior conversations or interest
        - Customer contact = service-oriented, reference ongoing value delivered
8. **Offer to create a lead list** at the new companies. Ask the user: "Would you like me to create a lead list with these contacts at their new companies, including the job change context?" If yes:
    - Call `mcp__claude_ai_Amplemarket__create_lead_list` with a descriptive name (e.g., "Job Changes - Q1 2026 Champions").
    - Call `mcp__claude_ai_Amplemarket__add_leads_to_lead_list` to add the changed contacts using their enriched data at the new company.
    - Include any additional stakeholders found in step 6 if the user wants to multi-thread into the new organization.
    - Provide the final list URL and contact count for confirmation.

### Important Notes

- Enrichment data reflects the most recent snapshot available in Amplemarket's database. Very recent job changes (within the last 1-2 weeks) may not yet be captured. If a change is suspected but not confirmed, flag it as "Unable to Determine" and suggest the user verify via LinkedIn.
- Batch enrichment consumes Amplemarket credits for each contact enriched. For large lead lists (50+ contacts), inform the user of the approximate credit cost before proceeding and suggest processing in smaller batches if needed.
- When comparing company names, normalize for common variations (e.g., "Stripe, Inc." vs "Stripe", "The New York Times" vs "NYT") to avoid false positives.
- Internal moves (same company, different role) are worth flagging separately. A contact promoted to a decision-making role can be a stronger opportunity than before.
- If a contact cannot be found via enrichment at all, they may have left the workforce, moved to a private company, or changed their public profile. Flag these as "Unable to Determine" rather than "No Change."

## Dynamic Fields Generated

These fields are populated for each contact where a job change is detected. Use them in outreach templates or pass them to sequence tools.

| Field | Description | Example Value |
| --- | --- | --- |
| `{{jobchange_person_name}}` | Full name of the contact who changed jobs | Sarah Chen |
| `{{jobchange_previous_company}}` | Name of the company where you previously engaged with the contact | Notion |
| `{{jobchange_previous_role}}` | The contact's title/role at the previous company | Director of Sales |
| `{{jobchange_new_company}}` | Name of the company the contact has moved to | Rippling |
| `{{jobchange_new_role}}` | The contact's current title/role at the new company | VP of Revenue |
| `{{jobchange_new_company_size}}` | Employee count or size range of the new company | 1001-5000 |
| `{{jobchange_new_company_industry}}` | Industry classification of the new company | Human Resources Technology |
| `{{jobchange_new_company_domain}}` | Website domain of the new company | rippling.com |
| `{{jobchange_tenure_at_previous}}` | Approximate time the contact spent at the previous company | ~2 years 4 months |
| `{{jobchange_time_at_new_company}}` | Approximate time since the contact joined the new company | ~3 months |
| `{{jobchange_relationship_context}}` | The relationship type provided by the user | Champion |
| `{{jobchange_new_company_news}}` | Recent news or notable events at the new company from WebSearch | Raised $200M Series E (Jan 2026) |
| `{{jobchange_suggested_opener}}` | A personalized opening line referencing the job change and past relationship | Congratulations on the move to Rippling - VP of Revenue is a well-deserved step up! |

**Usage note:** Fields are left blank for contacts classified as "No Change" or "Unable to Determine." For internal moves, `{{jobchange_new_company}}` and `{{jobchange_previous_company}}` will be the same, while `{{jobchange_new_role}}` and `{{jobchange_previous_role}}` will differ.

## Examples

### Example 1: Single Champion Tracking

**User prompt:** "Check if Sarah Chen changed jobs. She was our champion at Notion. Here's her LinkedIn: linkedin.com/in/sarahchen-sales"

**What the skill does:**
1. Identifies input: LinkedIn URL, context = champion, expected company = Notion.
2. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `linkedin_url`: "https://linkedin.com/in/sarahchen-sales", `reveal_email`: true.
3. Enrichment returns: Sarah Chen is now VP of Revenue at Rippling (domain: rippling.com). Job change detected.
4. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "rippling.com".
5. Calls `WebSearch` with query "Rippling news 2026" to find recent company developments.
6. Calls `mcp__claude_ai_Amplemarket__search_people` with `company_domains`: ["rippling.com"], `person_seniorities`: ["C-Suite", "VP", "Director"], `full_output`: true.
7. Generates dynamic fields and re-engagement draft.

**Example output:**

**JOB CHANGE DETECTED**

| Field | Value |
| --- | --- |
| Contact | Sarah Chen |
| Status | Job Change Detected |
| Previous Company | Notion |
| Previous Role | Director of Sales |
| New Company | Rippling |
| New Role | VP of Revenue |
| New Company Size | 1001-5000 employees |
| New Company Industry | Human Resources Technology |
| New Company Domain | rippling.com |
| Tenure at Notion | ~2 years 4 months |
| Time at Rippling | ~3 months |
| Email at New Company | sarah.chen@rippling.com |

**New Company Profile**
| Field | Detail |
|-----|-----|
| Company | Rippling |
| Industry | HR Tech / Workforce Management |
| Size | 1001-5000 |
| HQ | San Francisco, CA |
| Recent News | Raised $200M Series E at $13.5B valuation (Jan 2026); Launched global payroll in 12 new markets |

**Additional Stakeholders at Rippling**
| Name | Title | LinkedIn |
|----|-----|-------|
| Marcus Webb | CRO | linkedin.com/in/mwebb |
| Priya Patel | VP of Sales Operations | linkedin.com/in/ppatel |
| James Okonkwo | Director of Enterprise Sales | linkedin.com/in/jokonkwo |

**Suggested Re-Engagement:**
> "Hi Sarah, congratulations on the move to Rippling. VP of Revenue is a well-deserved step up! I loved working with you at Notion and saw that Rippling just expanded global payroll to 12 new markets. As you scale the revenue org, I'd love to catch up on how we might support the growth. Worth a quick chat?"

**Dynamic Fields:**
- `{{jobchange_person_name}}` = Sarah Chen
- `{{jobchange_previous_company}}` = Notion
- `{{jobchange_previous_role}}` = Director of Sales
- `{{jobchange_new_company}}` = Rippling
- `{{jobchange_new_role}}` = VP of Revenue
- `{{jobchange_new_company_size}}` = 1001-5000
- `{{jobchange_new_company_industry}}` = Human Resources Technology
- `{{jobchange_new_company_domain}}` = rippling.com
- `{{jobchange_tenure_at_previous}}` = ~2 years 4 months
- `{{jobchange_time_at_new_company}}` = ~3 months
- `{{jobchange_relationship_context}}` = Champion
- `{{jobchange_new_company_news}}` = Raised $200M Series E (Jan 2026); Global payroll expansion to 12 new markets
- `{{jobchange_suggested_opener}}` = Congratulations on the move to Rippling - VP of Revenue is a well-deserved step up!

### Example 2: Batch Tracking from Lead List

**User prompt:** "Track job changes for everyone in my 'Q4 Closed Won Champions' lead list"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__list_lead_lists` to find the list named "Q4 Closed Won Champions".
2. Calls `mcp__claude_ai_Amplemarket__get_lead_list` with the list `id` to retrieve all contacts.
3. Enriches each contact via `mcp__claude_ai_Amplemarket__enrich_person`.
4. Compares enrichment results against the company stored in the lead list for each contact.
5. For contacts with changes: enriches new companies, searches for stakeholders, generates dynamic fields.
6. Returns a summary table and offers to create a new lead list.

**Example output (abbreviated):**

**JOB CHANGE TRACKING SUMMARY - Q4 Closed Won Champions (8 contacts)**

| Contact | Expected Company | Status | New Company | New Role |
| --- | --- | --- | --- | --- |
| Sarah Chen | Notion | Job Change Detected | Rippling | VP of Revenue |
| Michael Torres | Segment | Job Change Detected | Databricks | Head of Sales Dev |
| Emily Watson | Lattice | No Change | - | - |
| David Kim | Figma | No Change | - | - |
| Rachel Green | Gong | Job Change Detected | Clari | Director of Sales |
| Tom Nakamura | Deel | No Change | - | - |
| Lisa Park | Brex | Unable to Determine | - | - |
| James Obi | Ramp | Internal Move Detected | Ramp | VP of Finance (was Director) |

**Summary:** 3 job changes detected, 1 internal move, 3 no change, 1 unable to determine.

**Credit usage:** 8 person enrichments + 3 company enrichments = 11 credits consumed.

*Detailed job change profiles and re-engagement drafts generated for Sarah Chen, Michael Torres, and Rachel Green. James Obi flagged for internal promotion follow-up.*

"Would you like me to create a lead list with the 3 changed contacts at their new companies?"

### Example 3: Contact Still at Same Company

**User prompt:** "Did Alex Rivera move companies? He was VP of Sales at Datadog. Email: alex.rivera@datadog.com"

**What the skill does:**
1. Identifies input: email + name, context not specified (defaults to general), expected company = Datadog.
2. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `email`: "alex.rivera@datadog.com", `name`: "Alex Rivera", `reveal_email`: true.
3. Enrichment returns: Alex Rivera, VP of Sales at Datadog (datadog.com). No change detected.
4. Skips new company research and stakeholder search.

**Example output:**

**NO JOB CHANGE DETECTED**

| Field | Value |
| --- | --- |
| Contact | Alex Rivera |
| Status | No Change |
| Current Company | Datadog |
| Current Role | VP of Sales |
| Expected Company | Datadog |
| Tenure | ~3 years 8 months |

Alex Rivera is still at Datadog as VP of Sales. No job change detected since your last interaction.

**Next Steps:**
- No re-engagement dynamic fields generated (no change occurred).
- If you want to re-engage Alex at Datadog, consider the outreach-personalization-research skill to build a tailored approach based on current company signals.
- To be notified of future changes, add Alex to a tracking lead list and re-run this skill periodically (monthly or quarterly recommended).

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Contact not found in enrichment | Fallback chain: 1) Try LinkedIn URL if not already used. 2) Try email address. 3) Try name + company domain combination. 4) Try `mcp__claude_ai_Amplemarket__search_people` with `company_domains` + `person_titles` as a fuzzy match. 5) If still not found, classify as "Unable to Determine" and suggest the user verify the contact's LinkedIn profile manually. |
| Lead list not found | Verify the exact list name with the user. Call `mcp__claude_ai_Amplemarket__list_lead_lists` without filters to show all available lists. Common issue: list names are case-sensitive. |
| False positive job change detected | Company name variations (e.g., "Stripe, Inc." vs "Stripe") can cause false positives. Normalize names by stripping suffixes (Inc., LLC, Ltd., Corp.) and comparing domains before flagging a change. If uncertain, present the finding with a note: "Possible name variation - please verify." |
| Enrichment returns outdated data | Amplemarket enrichment reflects the latest available snapshot, but very recent changes (1-2 weeks) may not be captured. Suggest the user check the contact's LinkedIn profile directly for confirmation. Flag the result as "Data may not reflect changes within the last 2 weeks." |
| Too many contacts in lead list | For lists with 50+ contacts, warn the user about credit consumption and offer to process in batches of 25. Provide a running summary after each batch so the user can decide whether to continue. |
| WebSearch returns no relevant news for new company | This is common for smaller or private companies. Note "No recent news found" in the `{{jobchange_new_company_news}}` field and rely on company enrichment data for the outreach angle instead. |
| Contact appears to have left workforce | If enrichment returns no current company and the contact cannot be found via search, classify as "Unable to Determine" and note: "This contact may no longer be in a public-facing role. Consider reaching out via LinkedIn to confirm their current status." |
| Internal move detected but user only wants company changes | Clarify with the user whether internal moves (same company, different role) should be included in results. If not, filter them out but offer a separate summary: "2 internal moves were also detected - want to see those?" |
| No stakeholders found at new company | The new company may be very small or recently founded. Fallback: 1) Broaden seniority filters to include "Manager" and "Senior". 2) Try searching by company name instead of domain. 3) If still no results, note that the moved contact may be the primary entry point and suggest direct outreach without multi-threading. |
| WebSearch returns irrelevant results | Refine the search query by adding the company's industry or location. Try alternate queries such as "[Company Name] funding", "[Company Name] product launch", or "[Company Name] leadership". If no relevant results are found after 2-3 attempts, populate `{{jobchange_new_company_news}}` with "No recent news found" and rely on enrichment data for outreach angles. |