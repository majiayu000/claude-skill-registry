---
name: deal-contact-gap-analysis
description: >
  Analyze open HubSpot deals to map existing contacts against the typical buying committee, identify missing roles, and find recommended contacts to fill the gaps via Amplemarket.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Account Intelligence"
compatibility: Requires Amplemarket MCP server
---

# Deal Contact Gap Analysis

Analyze open HubSpot deals to map existing contacts against the typical buying committee, identify missing roles, and find recommended contacts to fill the gaps via Amplemarket.

## Instructions

When a user wants to analyze the buying committee coverage on their deals, pull deal and contact data from HubSpot, map roles to a buying committee framework, identify gaps, and find candidates to fill them.

### Steps

1. **Gather analysis parameters** by asking the user:
    
    **(a) "Which deals should I analyze?"** Accept:
    
    - A specific deal name or list of deal names
    - "All deals in [stage]" (e.g., "all deals in Negotiation")
    - "My top deals" (sorted by amount)
    - "All open deals" (with a warning about volume)
    
    **(b) "What does your typical buying committee look like?"** Offer a default framework and let the user customize:
    
    - Economic Buyer (CFO, VP Finance, CEO - person who controls budget)
    - Champion (day-to-day advocate - often the person who initiated the evaluation)
    - Technical Evaluator (CTO, VP Engineering, IT Director - validates technical fit)
    - End User / Operator (Manager, Director of the team that will use the product)
    - Legal / Procurement (General Counsel, Procurement Director - handles contracts)
    - Executive Sponsor (C-Suite or SVP - signs off on strategic decisions)
    
    If the user has a different framework (e.g., MEDDPICC roles, custom roles), adapt to their model.
    
    **(c) "Which deal stages should I focus on?"** Default to mid-to-late stages where multi-threading matters most (Qualification, Demo, Proposal, Negotiation). Allow the user to adjust.
    
2. **Retrieve the current user's identity** by calling `mcp__claude_ai_HubSpot__get_user_details` to get the authenticated user's name, email, and HubSpot user ID for owner-based filtering.
3. **Search for target deals** by calling `mcp__claude_ai_HubSpot__search_crm_objects` with:
    - `object_type`: "deals"
    - `filter_groups`: Based on user input - deal name, stage, owner, or open status
    - `properties`: ["dealname", "amount", "dealstage", "pipeline", "hubspot_owner_id", "closedate", "createdate", "hs_lastmodifieddate"]
    - `associations`: ["contacts", "companies"]
    - `sorts`: [{"propertyName": "amount", "direction": "DESCENDING"}]
    - `limit`: 20
4. **Retrieve associated contacts for each deal** by calling `mcp__claude_ai_HubSpot__get_crm_objects` with:
    - `object_type`: "contacts"
    - `object_ids`: contact IDs associated with each deal
    - `properties`: ["firstname", "lastname", "email", "jobtitle", "company", "phone", "linkedin_url", "hs_lead_status"]
    
    Also retrieve company data:
    
    - `object_type`: "companies"
    - `object_ids`: company IDs from the deals
    - `properties`: ["name", "domain", "industry", "numberofemployees"]
5. **Map contacts to buying committee roles.** For each deal, analyze each contact's job title and map them to the buying committee framework:
    
    **Mapping logic by title keywords:**
    
    - Economic Buyer: titles containing CFO, VP Finance, CEO, COO, "Head of Finance", "Finance Director"
    - Champion: the primary contact or the one with the most engagement (often the deal creator)
    - Technical Evaluator: titles containing CTO, VP Engineering, "VP of Technology", "IT Director", "Head of Engineering", "Solutions Architect"
    - End User / Operator: titles containing Manager, Director (non-C-suite, non-VP), "Team Lead", "Head of [functional area]"
    - Legal / Procurement: titles containing "General Counsel", "Legal", "Procurement", "Vendor Management", "Contracts"
    - Executive Sponsor: titles containing CEO, President, COO, SVP, "Managing Director", "General Manager"
    
    Flag contacts that cannot be clearly mapped to a role as "Unclassified" and note their title for user review.
    
6. **Identify gaps in each deal.** Compare the mapped contacts against the full buying committee framework:
    - List which roles are covered and by whom
    - List which roles are missing
    - Calculate a coverage score: (roles filled / total roles) as a percentage
    - Flag single-threaded deals (only 1 contact) as highest risk
7. **Find candidates for missing roles** by calling `mcp__claude_ai_Amplemarket__search_people` for each deal company with gaps:
    - `company_domains`: [deal company domain]
    - `person_titles`: titles matching the missing roles (e.g., if missing Technical Evaluator, search for "CTO", "VP Engineering", "VP Technology", "Director Engineering")
    - `person_seniorities`: appropriate seniority levels for the missing role
    - `full_output`: true
    - `page_size`: 5
    
    Limit people searches to the top 10 deals by amount to manage credit usage.
    
8. **Enrich top recommended contacts** by calling `mcp__claude_ai_Amplemarket__enrich_person` for the #1 candidate for each missing role (limit to 10-15 enrichments):
    - Use `linkedin_url` from the search results
    - Set `reveal_email`: true
    - Extract verified email, current title, and background for outreach
9. **Generate approach suggestions** for each gap. Based on the missing role and the existing contacts:
    - Suggest who on the existing contact list could introduce the missing person
    - Draft an approach strategy (direct outreach, warm introduction, event-based)
    - Generate a suggested opener referencing the deal context and the missing person's role
10. **Present the gap analysis** with:
- Summary across all deals: average coverage score, most commonly missing roles, single-threaded deals
- Per-deal breakdown: contacts mapped to roles, gaps identified, recommended candidates
- Risk assessment: deals at highest risk due to gaps (large amount + low coverage)
- Action plan: prioritized list of contacts to add, with approach strategies

### Important Notes

- The buying committee framework should be adapted to the user's sales motion. Enterprise deals may need 6-8 roles; SMB deals may only need 2-3 (champion + economic buyer).
- Title-to-role mapping is imperfect. Titles vary widely across companies. "Head of Growth" could be marketing, sales, or product. Present mappings as suggestions and let the user correct them.
- Single-threaded deals (only 1 contact) in mid-to-late stages are the highest-risk finding. Prioritize these in the output.
- Limit `search_people` and `enrich_person` calls to the top 10 deals by value to manage Amplemarket credits. Offer to expand: "Shall I also search for missing contacts on the remaining X deals?"
- If a deal has no associated contacts at all, flag it immediately: "This deal has zero contacts. It cannot progress without at least a champion identified."

## Dynamic Fields Generated

The following dynamic fields are populated for each identified gap and can be used in multi-threading outreach templates:

| Field | Description | Example Value |
| --- | --- | --- |
| `{{gap_deal_name}}` | Name of the deal being analyzed | "Acme Corp - Enterprise License" |
| `{{gap_deal_stage}}` | Current deal stage | "Proposal Sent" |
| `{{gap_deal_amount}}` | Deal value | "$185,000" |
| `{{gap_missing_role}}` | The buying committee role that is unfilled | "Technical Evaluator" |
| `{{gap_recommended_contact}}` | Name of the recommended person to fill the gap | "Jordan Lee" |
| `{{gap_recommended_title}}` | Title of the recommended contact | "VP of Engineering" |
| `{{gap_recommended_email}}` | Verified email of the recommended contact | "jordan.lee@acmecorp.com" |
| `{{gap_existing_champion}}` | Name of the existing champion who could make an introduction | "Sarah Martinez" |
| `{{gap_coverage_score}}` | Percentage of buying committee roles filled | "33% (2 of 6 roles)" |
| `{{gap_suggested_approach}}` | Recommended approach strategy | "Ask Sarah Martinez for a warm intro to Jordan" |
| `{{gap_suggested_opener}}` | Personalized opener for the missing contact | "Hi Jordan, your team at Acme is evaluating our platform and I'd love your technical perspective..." |
| `{{gap_company_name}}` | Company name for the deal | "Acme Corp" |
| `{{gap_risk_level}}` | Risk level based on gap severity | "High - single-threaded, missing economic buyer" |

## Examples

### Example 1: Full Pipeline Gap Analysis

**User prompt:** "Map the buying committee on my open deals. My email is smartinez@ourcompany.com"

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__get_user_details` to confirm user identity.
2. Calls `mcp__claude_ai_HubSpot__search_crm_objects` with `object_type`: "deals", filtering for open deals owned by the user, sorted by amount descending.
3. Calls `mcp__claude_ai_HubSpot__get_crm_objects` for contacts and companies associated with each deal.
4. Maps each contact to a buying committee role based on their title.
5. Identifies missing roles for each deal.
6. Calls `mcp__claude_ai_Amplemarket__search_people` at each deal company to find candidates for missing roles.
7. Calls `mcp__claude_ai_Amplemarket__enrich_person` for the top candidate per missing role.
8. Presents the comprehensive gap analysis.

**Example output:**

---

**BUYING COMMITTEE GAP ANALYSIS - Sarah Martinez**

**Executive Summary**
- Deals analyzed: 8
- Average coverage score: 42%
- Single-threaded deals: 2 (CRITICAL)
- Most commonly missing role: Technical Evaluator (missing in 6 of 8 deals)
- Second most missing: Legal/Procurement (missing in 7 of 8 deals)
- Total pipeline at risk from poor multi-threading: $620K

**Deal-by-Deal Analysis**

**1. Acme Corp - Enterprise License ($185,000 | Proposal Sent)**

| Role | Status | Contact | Title |
| --- | --- | --- | --- |
| Champion | Filled | David Kim | Director of Operations |
| Economic Buyer | Filled | Catherine Zhao | CFO |
| Technical Evaluator | MISSING | - | - |
| End User | Filled | Miguel Santos | Operations Manager |
| Legal/Procurement | MISSING | - | - |
| Executive Sponsor | MISSING | - | - |

Coverage: 50% (3 of 6) | Risk: Medium

**Recommended contacts to fill gaps:**

| Missing Role | Recommended Contact | Title | Email | Approach |
| --- | --- | --- | --- | --- |
| Technical Evaluator | Jordan Lee | VP of Engineering | jordan.lee@acmecorp.com | Ask David Kim for intro, as they work cross-functionally |
| Legal/Procurement | Priya Mehta | Director of Procurement | priya.mehta@acmecorp.com | Direct outreach, reference the active evaluation |
| Executive Sponsor | Robert Chen | COO | robert.chen@acmecorp.com | Ask Catherine Zhao to loop in for final sign-off |

**2. TechFlow - Platform Deal ($210,000 | Negotiation)**

| Role | Status | Contact | Title |
| --- | --- | --- | --- |
| Champion | Filled | Kevin Park | CTO |
| Economic Buyer | MISSING | - | - |
| Technical Evaluator | Filled | Kevin Park | CTO (dual role) |
| End User | MISSING | - | - |
| Legal/Procurement | MISSING | - | - |
| Executive Sponsor | MISSING | - | - |

Coverage: 17% (1 of 6) | Risk: **CRITICAL - single-threaded at $210K in Negotiation**

**Recommended contacts:**

| Missing Role | Recommended Contact | Title | Approach |
| --- | --- | --- | --- |
| Economic Buyer | Amanda Foster | VP of Finance | Critical - need budget holder before contract stage |
| End User | Raj Patel | Senior Platform Engineer | Kevin can introduce, direct report |
| Executive Sponsor | James Wright | CEO | Ask Kevin for executive alignment meeting |

**3. DataSync - Annual License ($125,000 | Qualification)** ...

---

**PRIORITY ACTION PLAN**

1. **URGENT:** TechFlow ($210K) - Single-threaded in Negotiation. Multi-thread to VP Finance and CEO immediately.
2. **HIGH:** Acme Corp ($185K) - Add Technical Evaluator before POC discussion.
3. **MEDIUM:** DataSync ($125K) - Find champion; current contact is too junior.

---

### Example 2: Single Deal Deep Dive

**User prompt:** "Who's missing from the Acme Corp deal? We typically need a champion, economic buyer, technical evaluator, and legal."

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__search_crm_objects` searching for deals with name containing "Acme Corp".
2. Retrieves all associated contacts via `mcp__claude_ai_HubSpot__get_crm_objects`.
3. Maps contacts to the user's 4-role framework.
4. Searches for missing roles at Acme Corp via `mcp__claude_ai_Amplemarket__search_people`.
5. Enriches top candidates via `mcp__claude_ai_Amplemarket__enrich_person`.
6. Presents a focused gap analysis for that single deal.

### Example 3: Stage-Based Analysis

**User prompt:** "Check multi-threading on all deals in Negotiation stage. Flag any that are single-threaded"

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__get_user_details`.
2. Calls `mcp__claude_ai_HubSpot__search_properties` to find the correct stage ID for "Negotiation".
3. Calls `mcp__claude_ai_HubSpot__search_crm_objects` filtering for deals in the Negotiation stage.
4. Retrieves contacts for each deal.
5. Flags deals with only 1 contact as single-threaded.
6. Maps contacts to roles and identifies gaps.
7. Prioritizes results by deal amount, highlighting single-threaded deals first.

**Example output (abbreviated):**

---

**MULTI-THREADING ANALYSIS - Negotiation Stage**

Summary: 5 deals in Negotiation | 2 single-threaded (CRITICAL) | Average contacts per deal: 2.4

| Deal | Amount | Contacts | Single-Threaded? | Missing Roles | Risk |
| --- | --- | --- | --- | --- | --- |
| TechFlow | $210,000 | 1 | YES | Economic Buyer, End User, Legal, Exec Sponsor | Critical |
| GlobalTech | $165,000 | 1 | YES | Technical Evaluator, Legal, Exec Sponsor | Critical |
| Acme Corp | $185,000 | 3 | No | Technical Evaluator, Legal | Medium |
| CloudBase | $92,000 | 4 | No | Legal | Low |
| DataPipe | $78,000 | 2 | No | Economic Buyer, Exec Sponsor | Medium |

**Immediate action needed:** TechFlow and GlobalTech are both single-threaded in Negotiation with $375K combined value. These deals are at high risk of stalling or being lost.

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Deal has no associated contacts | Flag immediately: "This deal has zero contacts in HubSpot. It cannot be analyzed for gaps. Add at least one contact to the deal before running gap analysis." Offer to search for contacts at the deal company via `mcp__claude_ai_Amplemarket__search_people`. |
| Contact titles are missing or vague | If HubSpot contact records lack job titles, try enriching them via `mcp__claude_ai_Amplemarket__enrich_person` to get current titles. If titles are vague (e.g., "Manager"), classify as "Unclassified" and ask the user to manually assign the role. |
| Deal company domain is not available | If the associated company record lacks a domain, search for the company by name via `mcp__claude_ai_Amplemarket__enrich_company` to find the domain. Without a domain, `search_people` cannot find candidates for missing roles. |
| No candidates found for a missing role | Fallback chain: 1) Broaden the title search (e.g., add "Senior" level in addition to VP/Director). 2) Try searching by company name instead of domain. 3) For smaller companies (<50 employees), the role may not exist. Note: "Company may be too small to have a dedicated [role]. Suggest the user identify who covers this function." |
| User's buying committee framework differs from default | Adapt the mapping logic to the user's framework. If they use MEDDPICC, map to: Metrics owner, Economic Buyer, Decision criteria owner, Decision process owner, Paper process owner, Identified pain owner, Champion, Competition tracker. Update role-to-title mappings accordingly. |
| Too many deals to analyze | Offer to prioritize: "I found X open deals. Shall I focus on the top 10 by deal value, or would you prefer a specific stage?" Limit `search_people` calls to the top 10 deals to manage credits. |
| Contact appears on multiple deals | This is common. One person may be the champion on several deals at the same company. Map them to the appropriate role on each deal independently. Note the overlap: "David Kim is the champion on 3 Acme Corp deals." |
| Role mapping is ambiguous | Present ambiguous mappings with a note: "David Kim (Director of Business Operations), mapped as End User/Operator. Could also be Champion. Please confirm." Let the user override the mapping. |