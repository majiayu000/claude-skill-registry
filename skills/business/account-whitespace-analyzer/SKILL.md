---
name: account-whitespace-analyzer
description: >
  Analyze existing HubSpot customer accounts to find untapped departments and personas, map whitespace against the full organizational structure from Amplemarket, and generate expansion outreach referencing the existing customer relationship.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Account Intelligence"
compatibility: Requires Amplemarket MCP server
---

# Account Whitespace Analyzer

Analyze existing HubSpot customer accounts to find untapped departments and personas, map whitespace against the full organizational structure from Amplemarket, and generate expansion outreach referencing the existing customer relationship.

## Instructions

When a user wants to identify expansion opportunities within existing accounts, pull account and contact data from HubSpot, map organizational coverage, identify whitespace, and produce a prioritized expansion plan.

### Steps

1. **Gather analysis parameters** by asking the user:
    
    **(a) "Which accounts should I analyze for whitespace?"** Accept:
    
    - "My top 10 accounts by deal value"
    - Specific account names
    - "All accounts with closed-won deals"
    - "Accounts tagged as [segment]"
    
    **(b) "Which departments or functions are expandable?"** Present common options:
    
    - Engineering / Technology
    - Sales / Revenue
    - Marketing
    - Finance / Accounting
    - HR / People Operations
    - Operations
    - Product
    - Customer Success / Support
    - Legal
    - IT / Security
    
    Let the user select which departments represent cross-sell or upsell opportunities.
    
    **(c) "What seniority levels should I look for?"** Default:
    
    - VP and above for enterprise accounts
    - Director and above for mid-market
    - Manager and above for SMB
    Allow customization.
    
    **(d) "What's your current product/use case at these accounts?"** This context helps tailor the expansion pitch, e.g., "We currently serve the Sales team with [product]. The Marketing team could benefit from [related capability]."
    
2. **Retrieve the current user's identity** by calling `mcp__claude_ai_HubSpot__get_user_details` to get the authenticated user's name, email, and HubSpot user ID for filtering and personalization.
3. **Search for target accounts** by calling `mcp__claude_ai_HubSpot__search_crm_objects` with:
    - `object_type`: "deals"
    - `filter_groups`: Filter for closed-won deals, optionally by owner or date range
    - `properties`: ["dealname", "amount", "dealstage", "pipeline", "hubspot_owner_id", "closedate"]
    - `associations`: ["contacts", "companies"]
    - `sorts`: [{"propertyName": "amount", "direction": "DESCENDING"}]
    - `limit`: 20
    
    Group deals by company to identify unique accounts and their total deal value.
    
4. **Retrieve all existing contacts at each account** by calling `mcp__claude_ai_HubSpot__get_crm_objects` with:
    - `object_type`: "contacts"
    - `object_ids`: all contact IDs associated with deals at each account
    - `properties`: ["firstname", "lastname", "email", "jobtitle", "company", "phone", "linkedin_url", "hs_lead_status"]
    
    Also retrieve company data:
    
    - `object_type`: "companies"
    - `object_ids`: company IDs from the deals
    - `properties`: ["name", "domain", "industry", "numberofemployees", "city", "state", "country"]
5. **Map existing contacts by department and seniority.** For each account, categorize every HubSpot contact:
    
    **Department mapping by title keywords:**
    
    - Engineering: "Engineer", "Developer", "CTO", "VP Engineering", "Architecture", "DevOps", "SRE"
    - Sales: "Sales", "Revenue", "Business Development", "Account Executive", "SDR", "CRO"
    - Marketing: "Marketing", "Growth", "Demand Gen", "Content", "Brand", "CMO"
    - Finance: "Finance", "CFO", "Controller", "Accounting", "FP&A", "Treasury"
    - HR: "HR", "People", "Talent", "Recruiting", "CHRO", "Culture"
    - Operations: "Operations", "COO", "Strategy", "Process", "Supply Chain"
    - Product: "Product", "CPO", "Product Manager", "Product Design", "UX"
    - Customer Success: "Customer Success", "Support", "Client", "Account Management"
    - Legal: "Legal", "Counsel", "Compliance", "Regulatory", "Privacy"
    - IT/Security: "IT", "Information Technology", "CISO", "Security", "Infrastructure"
    
    Build a coverage matrix: departments with contacts vs departments without contacts.
    
6. **Enrich each target company** by calling `mcp__claude_ai_Amplemarket__enrich_company` with the company `domain`:
    - Get current firmographics: size, departments, growth trajectory
    - Understand the company's organizational structure and potential expansion areas
    - Limit to top 10 accounts by deal value to manage credits
7. **Search for contacts in whitespace departments** by calling `mcp__claude_ai_Amplemarket__search_people` for each account where gaps exist:
    - `company_domains`: [account domain]
    - `person_titles`: titles matching the missing department (e.g., for missing Marketing department: "CMO", "VP Marketing", "Head of Marketing", "Director of Marketing")
    - `person_seniorities`: based on user's seniority preference
    - `full_output`: true
    - `page_size`: 10
    
    Limit to 3-5 whitespace searches per account, focused on the most strategically valuable departments.
    
8. **Enrich top whitespace contacts** by calling `mcp__claude_ai_Amplemarket__enrich_person` for the top 1-2 candidates per whitespace department:
    - Use `linkedin_url` from search results
    - Set `reveal_email`: true
    - Get verified contact information for outreach
9. **Research account-level expansion signals** by calling `WebSearch` for the top 5 accounts:
    - Query: "[Account Name] [target department] initiative OR expansion OR hiring [year]"
    - Look for department-specific initiatives (e.g., "Acme Corp marketing transformation", "Acme Corp engineering hiring")
    - These provide context for why the expansion pitch is timely
10. **Build the whitespace map and expansion plan.** For each account, present:
    
    **Coverage Matrix:**
    | Department | Contacts in CRM | Seniority Coverage | Status |
    |--------|-----------|-------------|-----|
    | Sales | 4 contacts | VP, Director, Manager | Covered |
    | Engineering | 0 contacts | None | WHITESPACE |
    | Marketing | 1 contact | Manager only | PARTIAL - missing leadership |
    
    **Whitespace Opportunities:** For each gap, provide:
    
- Recommended contacts to engage
- Expansion rationale connecting existing product use to the new department
- Internal champion who can facilitate introduction
- Suggested opener referencing the existing relationship
    
    **Account-Level Summary:**
    
- Coverage percentage across all target departments
- Total whitespace contacts identified
- Recommended expansion priority (based on account size, deal value, and whitespace volume)

### Important Notes

- Whitespace analysis is most valuable for accounts with 200+ employees where multiple departments can independently buy. For small companies (<50 employees), most people already know about your product, so skip those accounts.
- The existing customer relationship is your biggest advantage. Every outreach should reference it: "We already work with your [department] team and they've seen [results]."
- Identify the internal champion (the existing contact with the strongest relationship) who can facilitate introductions to whitespace departments.
- Limit `search_people` and `enrich_person` calls to the top 10 accounts and 2-3 whitespace departments per account. Offer to expand: "Shall I also analyze whitespace in accounts 11-20?"
- Partial coverage (e.g., a department with only junior contacts) is still whitespace for leadership-level outreach. Flag these as "PARTIAL" and target senior contacts.
- If the user's product serves specific departments better than others, prioritize whitespace in those departments.

## Dynamic Fields Generated

The following dynamic fields are populated for each whitespace opportunity and can be used in expansion outreach templates:

| Field | Description | Example Value |
| --- | --- | --- |
| `{{whitespace_account_name}}` | Name of the customer account | "Acme Corp" |
| `{{whitespace_current_department}}` | Department currently using your product | "Sales" |
| `{{whitespace_current_product}}` | Product or use case at this account | "Sales engagement platform for SDR team" |
| `{{whitespace_target_department}}` | Department identified as whitespace | "Marketing" |
| `{{whitespace_target_contact}}` | Name of the recommended contact in the whitespace department | "Lisa Park" |
| `{{whitespace_target_title}}` | Title of the recommended contact | "VP of Marketing" |
| `{{whitespace_target_email}}` | Verified email of the recommended contact | "lisa.park@acmecorp.com" |
| `{{whitespace_expansion_rationale}}` | Why this department would benefit from your product | "Marketing team runs outbound campaigns that could leverage the same engagement platform" |
| `{{whitespace_internal_champion}}` | Existing contact who can introduce you | "David Kim, Director of Sales (your current champion)" |
| `{{whitespace_account_news}}` | Recent account news relevant to the expansion | "Acme Corp is investing in demand gen, hiring 5 marketing roles" |
| `{{whitespace_suggested_opener}}` | Personalized opener for the whitespace contact | "Hi Lisa, we work with David Kim's sales team at Acme and they've seen a 40% increase in reply rates..." |
| `{{whitespace_coverage_percentage}}` | Current department coverage at this account | "30% (3 of 10 departments covered)" |
| `{{whitespace_expansion_value}}` | Estimated expansion deal value | "$45,000 (based on similar department deployments)" |

## Examples

### Example 1: Top Account Whitespace Scan

**User prompt:** "Find whitespace in my top 10 accounts by deal value. We sell a sales engagement platform. I want to expand into Marketing, Customer Success, and RevOps. My email is smartinez@ourcompany.com"

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__get_user_details` to confirm identity.
2. Calls `mcp__claude_ai_HubSpot__search_crm_objects` for closed-won deals, sorted by amount, to identify the top 10 accounts.
3. Calls `mcp__claude_ai_HubSpot__get_crm_objects` for all contacts and companies at those accounts.
4. Maps contacts by department and seniority.
5. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each account to understand org structure.
6. Calls `mcp__claude_ai_Amplemarket__search_people` at accounts with gaps in Marketing, Customer Success, and RevOps.
7. Calls `mcp__claude_ai_Amplemarket__enrich_person` for top whitespace candidates.
8. Calls `WebSearch` for expansion signals at top accounts.
9. Presents the whitespace map and expansion plan.

**Example output:**

---

**ACCOUNT WHITESPACE ANALYSIS - Sarah Martinez (Top 10 Accounts)**

**Executive Summary**
- Accounts analyzed: 10
- Total existing deal value: $1.4M
- Average department coverage: 28%
- Total whitespace contacts identified: 34
- Highest-potential expansion accounts: 3 (Acme Corp, TechFlow, DataSync)
- Estimated expansion pipeline: $285K

**Account-by-Account Whitespace Map**

**1. Acme Corp (Total Deal Value: $185,000 | 2,500 employees)**

| Department | CRM Contacts | Seniority | Status |
| --- | --- | --- | --- |
| Sales | David Kim (Dir), Miguel Santos (Mgr), 2 AEs | VP, Dir, Mgr | COVERED |
| Marketing | None | None | WHITESPACE |
| Customer Success | None | None | WHITESPACE |
| RevOps | None | None | WHITESPACE |
| Engineering | Jordan Lee (VP Eng) | VP | Partial - engaged but not a buyer |
| Finance | Catherine Zhao (CFO) | C-Suite | COVERED |

Coverage: 33% (2 of 6 target departments) | Expansion potential: HIGH

**Whitespace Opportunities at Acme Corp:**

| Target Department | Recommended Contact | Title | Email | Expansion Rationale |
| --- | --- | --- | --- | --- |
| Marketing | Lisa Park | VP of Marketing | lisa.park@acmecorp.com | Marketing runs outbound campaigns that could use the same engagement engine as Sales |
| Customer Success | James Wright | Director of CS | james.wright@acmecorp.com | CS team handles renewal outreach, same platform, different motion |
| RevOps | Ana Ruiz | Head of Revenue Operations | ana.ruiz@acmecorp.com | RevOps bridges Sales and Marketing, a natural expansion point |

**Internal Champion:** David Kim (Director of Sales), strong relationship, can introduce to Lisa Park and Ana Ruiz.

**Account Signal:** Acme Corp is hiring 5 marketing roles per LinkedIn (demand gen focus), timely for Marketing expansion.

**Suggested Opener for Lisa Park (VP of Marketing):**
> "Hi Lisa, we've been working with David Kim's sales team at Acme and they've seen a 40% boost in reply rates with our engagement platform. I noticed the marketing team is expanding demand gen, and our platform supports marketing outreach the same way it powers sales. David suggested we connect. Worth 15 minutes?"

---

**2. TechFlow (Total Deal Value: $210,000 | 800 employees)**

| Department | CRM Contacts | Status |
| --- | --- | --- |
| Sales | Kevin Park (CTO, not actually Sales) | MISCLASSIFIED |
| Marketing | None | WHITESPACE |
| Customer Success | None | WHITESPACE |
| RevOps | None | WHITESPACE |

Coverage: 0% of target departments | Expansion potential: HIGH (but needs champion first)

Note: Kevin Park is CTO, not Sales. This account is single-threaded through Engineering. Need to build Sales and Marketing relationships before expansion.

---

**3. DataSync (Total Deal Value: $125,000 | 1,200 employees)** ...

---

**EXPANSION PRIORITY RANKING**

| Rank | Account | Coverage | Whitespace Contacts Found | Internal Champion | Priority |
| --- | --- | --- | --- | --- | --- |
| 1 | Acme Corp | 33% | 8 | David Kim (strong) | High |
| 2 | TechFlow | 0% | 12 | Kevin Park (moderate) | High |
| 3 | DataSync | 17% | 6 | Maya Patel (strong) | High |
| 4 | CloudBase | 50% | 3 | Tom Rivera (moderate) | Medium |
| 5 | FinServ | 33% | 5 | Rachel Kim (left, needs new) | Medium |
| ... | ... | ... | ... | ... | ... |

Shall I create Amplemarket lead lists for each account's whitespace contacts?

---

### Example 2: Single Account Deep Dive

**User prompt:** "Which departments haven't I sold to at Acme Corp? We currently serve their Sales team."

**What the skill does:**
1. Calls `mcp__claude_ai_HubSpot__search_crm_objects` for deals associated with Acme Corp.
2. Retrieves all contacts at Acme Corp from HubSpot.
3. Maps contacts by department.
4. Enriches Acme Corp via `mcp__claude_ai_Amplemarket__enrich_company`.
5. Searches for contacts in all departments without coverage.
6. Presents a single-account whitespace analysis.

### Example 3: Whitespace with Lead List Creation

**User prompt:** "Find expansion opportunities in my top 5 accounts and build a lead list with the whitespace contacts. We sell to Engineering and want to expand into Product and Design."

**What the skill does:**
1. Identifies top 5 accounts from closed-won deals.
2. Maps CRM contacts, confirms Engineering coverage, checks Product and Design gaps.
3. Searches for Product and Design leaders at each account via Amplemarket.
4. Enriches top candidates.
5. Asks: "I found 14 whitespace contacts across Product and Design at your top 5 accounts. Shall I create a lead list?"
6. Calls `mcp__claude_ai_Amplemarket__create_lead_list` with name "Account Expansion - Product & Design - Q1 2026" and the whitespace contacts.

**Example output (abbreviated):**

---

**WHITESPACE LEAD LIST CREATED**

Lead list "Account Expansion - Product & Design - Q1 2026" created with 14 contacts.

| Account | Department | Contact | Title | Internal Champion |
| --- | --- | --- | --- | --- |
| Acme Corp | Product | Chris Martinez | VP of Product | Jordan Lee (VP Eng) |
| Acme Corp | Design | Sam Patel | Head of Design | Jordan Lee (VP Eng) |
| TechFlow | Product | Maria Garcia | Director of PM | Kevin Park (CTO) |
| TechFlow | Design | Alex Kim | VP of Design | Kevin Park (CTO) |
| DataSync | Product | Taylor Swift | Head of Product | Maya Patel (Dir Eng) |
| ... | ... | ... | ... | ... |

Each lead includes expansion context and internal champion details.

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Account has very few contacts in CRM | This may mean the account is under-penetrated overall, not just in specific departments. Recommend a broader account mapping first: "Acme Corp has only 2 contacts in HubSpot across all departments. Before whitespace analysis, consider mapping the full buying committee." |
| Company is too small for meaningful whitespace | For companies with fewer than 50 employees, most functions are handled by a small team. Note: "This company has [X] employees, so departments are likely shared across roles. Focus on finding the 2-3 additional decision-makers rather than department-level expansion." |
| Contact title does not clearly map to a department | Titles like "Head of Growth" or "Chief of Staff" span departments. Classify as "Cross-Functional" and include in the output with a note for the user to manually assign. |
| Existing champion has left the account | Flag immediately: "Your internal champion [Name] appears to have left [Account]. Expansion outreach will be harder without an advocate. Consider re-establishing a champion relationship before pursuing whitespace." Use the champion-tracker skill to find where they went. |
| No whitespace contacts found via Amplemarket search | Fallback chain: 1) Broaden the title search to include more variations. 2) Lower the seniority filter to include "Manager" level. 3) Try searching by company name instead of domain. 4) If the company is too small, note: "Limited people data available, and the company may not have dedicated leaders in target departments." |
| Account is already fully covered | This is a positive finding. Note: "Acme Corp has contacts in all target departments. Consider deepening engagement at existing contacts rather than expanding horizontally. Look for upsell or upgrade opportunities within current departments." |
| User's product does not clearly map to the whitespace department | Ask for clarification: "How would [your product] benefit the [Department] team? I want to make sure the expansion rationale is compelling." Without a clear connection, whitespace outreach will feel forced. |
| WebSearch finds no account-specific expansion signals | Use general industry trends instead: "No specific expansion signals found for Acme Corp's marketing team, but [industry] companies are broadly investing in demand gen and ABM, which may resonate." |