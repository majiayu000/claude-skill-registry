---
name: account-expansion-mapper
description: >
  Map untapped departments and roles within existing accounts to surface
  expansion opportunities, then find contacts in whitespace areas with
  personalization that references your existing relationship.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Account Intelligence"
compatibility: Requires Amplemarket MCP server
---

# Account Expansion Mapper

Map untapped departments and roles within existing accounts to surface expansion opportunities, then find contacts in whitespace areas with personalization that references your existing relationship.

## Instructions

When a user wants to find expansion opportunities within an existing account, follow these steps to map the org, identify whitespace departments, and generate personalized outreach fields for new contacts.

### Steps

1. **Gather account details from the user.** Ask for:
    - Account(s) to expand: company name(s) or domain(s)
    - Departments already sold into (e.g., "We sold to Engineering and IT")
    - Departments that could benefit from the product (e.g., "Marketing and RevOps could also use it")
    - Target seniority levels for new contacts (e.g., "Director and above")
    
    If the user provides only a company name, ask which departments they have already engaged before proceeding.
    
2. **Enrich the company** by calling `mcp__claude_ai_Amplemarket__enrich_company` with:
    - `domain` if the user provided a domain or you can infer it
    - `linkedin_url` if the user provided a LinkedIn company URL
    This returns firmographics: industry, size, type, location, description, tech stack, headcount, and more. Use company size to calibrate how many departments to expect.
3. **Check existing Amplemarket engagement data** by calling `mcp__claude_ai_Amplemarket__list_accounts` with the company `name` or `domain` to find the account. If found, call `mcp__claude_ai_Amplemarket__get_account` with the account `id` to retrieve:
    - Engagement stats (emails sent, opened, replied)
    - Known contacts and their departments
    - CRM data and opportunity status
    - Account owner and tags
    - AI-generated insights
    
    Cross-reference the account's known contacts against the departments the user mentioned to validate which departments are already engaged.
    
4. **Map the org across multiple departments** by calling `mcp__claude_ai_Amplemarket__search_people` multiple times with:
    - `company_names` or `company_domains`: [target company]
    - `person_seniorities`: user-specified seniority levels (default: ["C-Suite", "VP", "Head", "Director"])
    - `person_departments`: vary this across calls to cover all relevant departments (e.g., "Marketing", "Revenue", "Engineering & Technical", "Finance & Accounting", "Operations", "Human Resources", "IT & Information Security")
    - `full_output`: true
    - `page_size`: 20
    
    Run separate searches for engaged departments (to confirm known contacts) and whitespace departments (to discover new contacts).
    
5. **Cross-reference against known contacts.** Compare search results with:
    - Contacts from `get_account` engagement data
    - Departments the user identified as already sold into
    - Any CRM contact data available
    
    Classify each department as: **Engaged** (existing contacts and outreach), **Partially Engaged** (some contacts but gaps in seniority or sub-teams), or **Whitespace** (no contacts found in Amplemarket data).
    
6. **Research company org structure** by calling `WebSearch` for:
    - "[Company name] org chart" or "[Company name] leadership team"
    - "[Company name] [department] head" for specific whitespace departments
    - "[Company name] new hires [department]" for recent additions to target departments
    - "[Company name] department structure" for insight into how teams are organized
    
    Use this to fill gaps where `search_people` returned limited results and to understand reporting structures.
    
7. **Present the expansion map.** Organize findings into a clear visual format:
    
    **Engaged Departments** - list known contacts, engagement status, and any gaps in coverage.
    
    **Whitespace Departments** - list discovered contacts, their titles, and why the department is a relevant expansion target.
    
    **Partially Engaged Departments** - list known contacts alongside newly discovered contacts who have not been reached.
    
    Include a summary table showing department, status, number of known contacts, number of new contacts found, and recommended action.
    
8. **Generate dynamic fields** for each whitespace contact. Populate the `{{expansion_*}}` fields described in the Dynamic Fields Generated section below. These fields enable personalized outreach that references the existing relationship at the company.
9. **Offer to create a lead list** with whitespace contacts. If the user agrees, call `mcp__claude_ai_Amplemarket__create_lead_list` with:
    - `name`: a descriptive name (e.g., "Expansion - Datadog - Marketing & RevOps - Mar 2026")
    - `type`: "linkedin" (if LinkedIn URLs are available) or "email"
    - `leads`: array of lead objects from the whitespace search results
    - `options`: ask about enrichment preferences (`enrich`, `validate_email`, `reveal_phone_numbers`)
    
    Optionally, call `mcp__claude_ai_Amplemarket__add_leads_to_lead_list` if the user wants to add contacts to an existing list.
    

### Important Notes

- Always confirm which departments are already engaged before mapping. False whitespace leads to wasted outreach.
- For companies with fewer than 100 employees, expect fewer distinct departments. Adjust the department search accordingly and note that one person may cover multiple functions.
- For companies with 1000+ employees, expect sub-departments and regional teams. Search with more specific titles to avoid missing relevant contacts.
- If the user does not specify target departments, suggest departments based on the product category (e.g., for sales tools, suggest Marketing, RevOps, Customer Success, Finance).
- When generating the internal reference field, always use verifiable information from the engagement data. Never fabricate contact names or engagement details.

## Dynamic Fields Generated

| Field | Description |
| --- | --- |
| `{{expansion_company_name}}` | The target company name for the expansion effort |
| `{{expansion_existing_department}}` | The department(s) already sold into at this account (e.g., "Engineering") |
| `{{expansion_existing_contact}}` | Name and title of a known contact in the engaged department (e.g., "Sarah Chen, VP Engineering") |
| `{{expansion_target_department}}` | The whitespace department being targeted (e.g., "Marketing") |
| `{{expansion_contact_name}}` | Full name of the new whitespace contact |
| `{{expansion_contact_title}}` | Title of the new whitespace contact (e.g., "Director of Demand Generation") |
| `{{expansion_internal_reference}}` | Reference to the existing relationship (e.g., "Your Engineering team has been using our platform since Q3 2025") |
| `{{expansion_department_relevance}}` | Why this department would benefit from the product (e.g., "Marketing teams at similar companies use our analytics to measure campaign ROI") |
| `{{expansion_company_context}}` | Relevant company context such as recent news, growth signals, or strategic initiatives |
| `{{expansion_suggested_opener}}` | Draft opening line referencing the existing relationship and department relevance (e.g., "Your engineering team at Datadog has been leveraging our platform, and I thought your marketing team might benefit from the same analytics capabilities.") |
| `{{expansion_company_size}}` | Company size bracket for segmentation (e.g., "5001-10000 employees") |

## Examples

### Example 1: Full Expansion Map for a Large Account

**User prompt:** "Find expansion opportunities at Datadog. We already sell to their Engineering team. I think Marketing, RevOps, and IT could benefit too. Target Director and above."

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "datadoghq.com".
2. Calls `mcp__claude_ai_Amplemarket__list_accounts` with `domain`: "datadoghq.com". Account found, so calls `mcp__claude_ai_Amplemarket__get_account` with the account ID.
3. Calls `mcp__claude_ai_Amplemarket__search_people` with `company_domains`: ["datadoghq.com"], `person_departments`: ["Engineering & Technical"], `person_seniorities`: ["Director", "VP", "Head", "C-Suite"], `full_output`: true, to confirm known Engineering contacts.
4. Calls `mcp__claude_ai_Amplemarket__search_people` three more times for whitespace departments:
- `person_departments`: ["Marketing"], same seniority and company filters
- `person_departments`: ["Revenue"], same filters (for RevOps contacts)
- `person_departments`: ["IT & Information Security"], same filters
5. Cross-references search results with `get_account` engagement data.
6. Calls `WebSearch` with "Datadog marketing leadership" and "Datadog RevOps team" for additional context.
7. Presents expansion map and generates dynamic fields for whitespace contacts.

**Example output:**

---

**ACCOUNT EXPANSION MAP: Datadog**

| Field | Detail |
| --- | --- |
| Company | Datadog, Inc. |
| Domain | datadoghq.com |
| Industry | Computer Software / Cloud Monitoring |
| Size | 5001-10000 employees |
| HQ | New York, NY |

**Department Coverage Summary**

| Department | Status | Known Contacts | New Contacts Found | Recommended Action |
| --- | --- | --- | --- | --- |
| Engineering | Engaged | 3 | 5 additional | Deepen multi-threading |
| Marketing | Whitespace | 0 | 8 | Priority outreach |
| Revenue / RevOps | Whitespace | 0 | 6 | Priority outreach |
| IT & Security | Whitespace | 0 | 4 | Secondary outreach |

**Engaged Department: Engineering**
| Name | Title | Engagement Status |
|----|-----|-------------|
| Jordan Lee | VP of Engineering | 3 emails sent, 1 reply |
| Sam Gupta | Director of Platform Engineering | 2 emails sent, opened |
| Priya Sharma | Head of SRE | 1 email sent, no open |

**Whitespace Department: Marketing**
| Name | Title | LinkedIn |
|----|-----|-------|
| Lisa Park | CMO | linkedin.com/in/lpark |
| Marco Silva | VP of Demand Generation | linkedin.com/in/msilva |
| Rachel Kim | Director of Product Marketing | linkedin.com/in/rkim |
| Amir Hassan | Director of Marketing Operations | linkedin.com/in/ahassan |

**Whitespace Department: Revenue / RevOps**
| Name | Title | LinkedIn |
|----|-----|-------|
| Alex Rivera | CRO | linkedin.com/in/arivera |
| Kim Tanaka | VP of Sales, Americas | linkedin.com/in/ktanaka |
| Derek Foster | Director of Revenue Operations | linkedin.com/in/dfoster |

**Whitespace Department: IT & Security**
| Name | Title | LinkedIn |
|----|-----|-------|
| Nina Patel | Director of IT | linkedin.com/in/npatel |
| Chris Wu | Head of Information Security | linkedin.com/in/cwu |

**Dynamic fields for Marco Silva (VP of Demand Generation, Marketing):**
- `{{expansion_company_name}}`: Datadog
- `{{expansion_existing_department}}`: Engineering
- `{{expansion_existing_contact}}`: Jordan Lee, VP of Engineering
- `{{expansion_target_department}}`: Marketing
- `{{expansion_contact_name}}`: Marco Silva
- `{{expansion_contact_title}}`: VP of Demand Generation
- `{{expansion_internal_reference}}`: Your Engineering team has been evaluating our platform. Jordan Lee's team has seen the product in action
- `{{expansion_department_relevance}}`: Marketing teams at companies like Datadog use our analytics to tie campaign performance to pipeline impact across their cloud monitoring product lines
- `{{expansion_company_context}}`: Datadog recently expanded its product suite with new APM and security features, creating more demand gen needs across product lines
- `{{expansion_suggested_opener}}`: "Your engineering team at Datadog has been exploring our platform, and I thought your demand gen team might benefit from the same analytics capabilities, especially with the new product lines launching."
- `{{expansion_company_size}}`: 5001-10000 employees

Would you like me to create a lead list with these 18 whitespace contacts?

---

### Example 2: Small Company Expansion (Fewer Departments)

**User prompt:** "Who else can I sell to at Loom? We've been working with their Product team."

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "loom.com".
2. Calls `mcp__claude_ai_Amplemarket__list_accounts` with `domain`: "loom.com". Account found, so calls `mcp__claude_ai_Amplemarket__get_account` with the account ID.
3. Notes company size is 201-500 employees, and expects fewer distinct departments and smaller leadership teams.
4. Calls `mcp__claude_ai_Amplemarket__search_people` with `company_domains`: ["loom.com"], `person_seniorities`: ["C-Suite", "VP", "Head", "Director", "Manager"], `full_output`: true, `page_size`: 20, a broad search to map the entire leadership team at once.
5. Cross-references results with engagement data to identify whitespace.
6. Calls `WebSearch` with "Loom leadership team" for org context.
7. Presents a compact expansion map suited to the company size.

**Example output:**

---

**ACCOUNT EXPANSION MAP: Loom**

| Field | Detail |
| --- | --- |
| Company | Loom (acquired by Atlassian) |
| Domain | loom.com |
| Industry | Computer Software / Video |
| Size | 201-500 employees |
| HQ | San Francisco, CA |

**Department Coverage Summary**

| Department | Status | Known Contacts | New Contacts Found | Recommended Action |
| --- | --- | --- | --- | --- |
| Product | Engaged | 2 | 1 additional | Maintain relationship |
| Engineering | Whitespace | 0 | 3 | Priority - close to Product |
| Marketing | Whitespace | 0 | 2 | Secondary outreach |
| People/HR | Whitespace | 0 | 1 | Low priority |

Note: At 201-500 employees, Loom has fewer distinct departments. Finance, Legal, and Operations may be handled by a small shared team or at the Atlassian parent level.

**Whitespace Department: Engineering**
| Name | Title | LinkedIn |
|----|-----|-------|
| Jay Patel | VP of Engineering | linkedin.com/in/jpatel |
| Maria Santos | Director of Engineering | linkedin.com/in/msantos |
| Tom Grant | Head of Infrastructure | linkedin.com/in/tgrant |

**Dynamic fields for Jay Patel (VP of Engineering):**
- `{{expansion_company_name}}`: Loom
- `{{expansion_existing_department}}`: Product
- `{{expansion_existing_contact}}`: [Known product contact name and title from engagement data]
- `{{expansion_target_department}}`: Engineering
- `{{expansion_contact_name}}`: Jay Patel
- `{{expansion_contact_title}}`: VP of Engineering
- `{{expansion_internal_reference}}`: Your Product team has been using our platform. They can speak to the value firsthand
- `{{expansion_department_relevance}}`: Engineering teams at product-led companies like Loom typically benefit from the same tooling their Product counterparts use, especially for async collaboration workflows
- `{{expansion_company_context}}`: Loom's integration into the Atlassian ecosystem may create new engineering workflow needs
- `{{expansion_suggested_opener}}`: "Your Product team at Loom has been working with us, and given how closely your Engineering and Product teams collaborate, I thought it might be relevant for your team too."
- `{{expansion_company_size}}`: 201-500 employees

---

### Example 3: Multiple Accounts Batch Analysis

**User prompt:** "Account expansion for Snowflake, Confluent, and Databricks. We sell to Engineering at all three. Find Marketing and Finance contacts."

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_company` three times with domains: "snowflake.com", "confluent.io", "databricks.com".
2. Calls `mcp__claude_ai_Amplemarket__list_accounts` three times to check existing engagement at each account.
3. For each account found, calls `mcp__claude_ai_Amplemarket__get_account` to retrieve engagement data.
4. Calls `mcp__claude_ai_Amplemarket__search_people` six times total (Marketing + Finance for each of the three companies):
- `company_domains`: ["snowflake.com"], `person_departments`: ["Marketing"], `person_seniorities`: ["Director", "VP", "Head", "C-Suite"], `full_output`: true
- `company_domains`: ["snowflake.com"], `person_departments`: ["Finance & Accounting"], same filters
- Repeat for confluent.io and databricks.com
5. Cross-references all results with engagement data.
6. Calls `WebSearch` for leadership pages at each company to fill gaps.
7. Presents a consolidated expansion map across all three accounts.

**Example output (abbreviated):**

---

**BATCH EXPANSION SUMMARY**

| Company | Size | Engineering (Engaged) | Marketing (Whitespace) | Finance (Whitespace) |
| --- | --- | --- | --- | --- |
| Snowflake | 5001-10000 | 4 contacts | 7 new contacts found | 3 new contacts found |
| Confluent | 1001-5000 | 2 contacts | 4 new contacts found | 2 new contacts found |
| Databricks | 5001-10000 | 3 contacts | 6 new contacts found | 4 new contacts found |
| **Total** |  | **9 engaged** | **17 new contacts** | **9 new contacts** |

Total whitespace contacts found: 26 across 3 accounts.

[Full expansion map for each company follows the same format as Example 1]

Would you like me to create separate lead lists per company, or one combined list with all 26 whitespace contacts?

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| User is unsure which departments are already engaged | Call `mcp__claude_ai_Amplemarket__list_accounts` and `mcp__claude_ai_Amplemarket__get_account` first to pull engagement data. Present known contacts grouped by department and ask: "Based on our records, it looks like you have engaged [departments]. Does this match your understanding?" |
| Account not found in Amplemarket | The company may be net-new. Proceed with `mcp__claude_ai_Amplemarket__enrich_company` and `mcp__claude_ai_Amplemarket__search_people` to map the org. Note that all departments are technically whitespace since there is no engagement history. Ask the user if they have engaged the company through other channels. |
| Company is too small for multi-department expansion | For companies with fewer than 50 employees, department-based expansion is less relevant. Instead, search for all senior contacts and present them by function. Note: "At this company size, individuals often cover multiple functions, so a single conversation may open multiple use cases." |
| `search_people` returns zero results for a whitespace department | Fallback chain: 1) Broaden seniority to include "Manager" and "Senior". 2) Try alternate department names (e.g., "Revenue" instead of "Sales", "People" instead of "Human Resources"). 3) Search by title keywords instead of department filter. 4) Use `WebSearch` for "[Company] [department] head" to find names, then `mcp__claude_ai_Amplemarket__enrich_person` to get their details. |
| Too many contacts found in a single department | Filter by the most relevant seniority levels first. For large enterprises (10000+ employees), add location or sub-department title keywords (e.g., "Demand Gen" within Marketing). Present the top 5-10 most relevant contacts and note the total available. |
| User wants to reference the existing relationship but engagement data is sparse | Use only verifiable data from `get_account`. If engagement data is minimal (e.g., only 1 email sent with no reply), frame the internal reference more cautiously: "We have been in touch with your Engineering team" rather than "Your Engineering team loves our platform." Never fabricate engagement details. |
| Batch analysis across many accounts is slow or hits rate limits | Process accounts sequentially rather than in parallel. Prioritize the largest or most strategic accounts first. For batches of 5+ accounts, suggest splitting into multiple sessions and offer to start with the top 3. |
| Expansion contacts overlap with contacts found by other skills | Deduplicate against existing lead lists by calling `mcp__claude_ai_Amplemarket__list_lead_lists` and checking for the target company. Flag any contacts that already appear in other lists so the user can avoid duplicate outreach. |