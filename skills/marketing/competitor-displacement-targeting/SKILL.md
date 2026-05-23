---
name: competitor-displacement-targeting
description: >
  Find companies using a competitor's product across multiple evidence vectors and target decision-makers for rip-and-replace campaigns.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Account Intelligence"
compatibility: Requires Amplemarket MCP server
---

# Competitor Displacement Targeting

Find companies using a competitor's product across multiple evidence vectors and target decision-makers for rip-and-replace campaigns.

## Instructions

When a user wants to identify companies using a competitor's product and prospect into those accounts, execute this multi-step research and targeting workflow.

### Steps

1. **Gather targeting criteria** from the user. Ask for:
    - **Competitor name(s):** Which product(s) or vendor(s) to target (e.g., "Salesforce", "HubSpot CRM", "Outreach and Salesloft")
    - **Evidence types to search:** Which vectors matter most: case studies, G2/Capterra reviews, job postings, tech stack databases, social proof (default: all)
    - **Target decision-maker roles:** Who should receive outreach (e.g., "VP of Sales", "CTO", "Head of Revenue Operations")
    - **ICP filters:** Industry, company size, geography, or other firmographic constraints
    
    If the user provides only a competitor name, ask: "What roles should I target at these companies, and any filters on industry, size, or geography?"
    
2. **Construct WebSearch queries** across multiple evidence vectors. Run at least 4 of the following searches per competitor using `WebSearch`:
    - **Case studies:** `"[competitor]" "case study" OR "customer story" OR "success story"`
    - **Review sites:** `"[competitor]" site:g2.com OR site:capterra.com`
    - **Social proof:** `"[competitor]" "we use" OR "we switched to" OR "we chose" OR "we implemented"`
    - **Job postings:** `"[competitor]" "experience with" OR "proficiency in" job OR hiring`
    - **Tech stack databases:** `"[competitor]" site:stackshare.io OR site:builtwith.com`
    
    For multiple competitors, run separate query sets for each competitor name. Adapt queries to include the competitor's common product names and abbreviations.
    
3. **Extract company names** by calling `WebFetch` on the top 5-10 results from each evidence vector. For each fetched page, extract:
    - Company name mentioned as a customer or user
    - Type of evidence (case study, review, job posting, etc.)
    - Specific details about their usage (pain points, use case, duration)
    - URL of the source for reference
4. **Deduplicate companies** found across vectors. Merge companies that appear in multiple evidence sources and track which vectors confirmed each company. Assign an evidence strength score:
    - **Strong (3+ vectors):** Company appears in case studies AND reviews AND job postings
    - **Medium (2 vectors):** Company appears in two different evidence types
    - **Light (1 vector):** Company appears in only one source
5. **Enrich each identified company** by calling `mcp__claude_ai_Amplemarket__enrich_company` with the company `domain` (inferred from the company name or extracted from evidence URLs). Key data points to extract:
    - Industry and sub-industry
    - Company size and employee count
    - Headquarters and locations
    - Company type and description
6. **Filter against the user's ICP.** Remove companies that do not match the user's firmographic criteria:
    - Industry mismatch
    - Company size outside target range
    - Geography outside target region
    - Company type mismatch (e.g., user only wants privately held)
    
    Report how many companies passed vs. were filtered out.
    
7. **Search for decision-makers** at matching companies by calling `mcp__claude_ai_Amplemarket__search_people` with:
    - `company_domains`: [matching company domain]
    - `person_titles`: target titles from user's criteria
    - `person_seniorities`: appropriate seniority levels
    - `full_output`: true
    - `page_size`: 10
    
    For efficiency, batch companies with similar domains and run searches for the top 10-15 highest-evidence-strength companies first.
    
8. **Present results grouped by evidence strength.** Format the output as a Competitor Displacement Report with dynamic fields populated for each prospect:
    
    **Displacement Opportunity Summary**
    
    - Competitor targeted
    - Total companies identified
    - Companies passing ICP filter
    - Decision-makers found
    - Breakdown by evidence strength (Strong / Medium / Light)
    
    **Strong Evidence Accounts** (table with company, evidence types, evidence detail, decision-makers found)
    
    **Medium Evidence Accounts** (same format)
    
    **Light Evidence Accounts** (same format)
    
    For each decision-maker, populate the `{{competitor_*}}` dynamic fields described in the Dynamic Fields Generated section below.
    
9. **Offer to create a lead list** with competitor context. If the user agrees, call `mcp__claude_ai_Amplemarket__create_lead_list` with:
    - `name`: descriptive name (e.g., "Salesforce Displacement - VP Sales - SaaS - Mar 2026")
    - `type`: "linkedin" (using LinkedIn URLs from search_people results)
    - `leads`: array of lead objects from the decision-maker search
    - `options`: enrichment settings as requested
    
    Include competitor context in the list name so the outreach team understands the targeting angle.
    

### Important Notes

- Evidence from case studies and review sites is the strongest signal. A company featured in a competitor's case study is almost certainly a current customer.
- Job postings mentioning a competitor tool indicate usage but may also indicate planned adoption. Flag this ambiguity when presenting results.
- Social proof from blog posts or social media can be outdated. Note the date of the source when available and flag evidence older than 18 months.
- Always respect rate limits when running multiple WebSearch and WebFetch calls. Space out requests and prioritize the highest-value evidence vectors first.
- Some competitors have common names that produce noisy results (e.g., "Monday" for monday.com). Use the full product name or domain in queries to reduce false positives.

## Dynamic Fields Generated

| Field | Description |
| --- | --- |
| `{{competitor_name}}` | Name of the competitor product being displaced (e.g., "Salesforce Sales Cloud") |
| `{{competitor_evidence_type}}` | Type of evidence found (e.g., "Case Study", "G2 Review", "Job Posting", "Tech Stack", "Social Proof") |
| `{{competitor_evidence_detail}}` | Specific detail about their usage (e.g., "Featured in Salesforce's 2025 enterprise case study for pipeline management") |
| `{{competitor_evidence_url}}` | URL of the source where evidence was found |
| `{{competitor_pain_points}}` | Pain points mentioned in evidence (e.g., "Cited complexity and high cost in G2 review") |
| `{{competitor_company_name}}` | Name of the company identified as a competitor customer |
| `{{competitor_company_size}}` | Employee count or size range of the target company |
| `{{competitor_company_industry}}` | Industry of the target company |
| `{{competitor_switch_reason}}` | Inferred or stated reason the company might switch (e.g., "G2 review mentions frustration with reporting limitations") |
| `{{competitor_suggested_opener}}` | Draft opening line referencing the competitor context (e.g., "I noticed your team uses Salesforce for pipeline management. Several companies your size have told us reporting flexibility was a pain point. Curious if that resonates.") |
| `{{competitor_evidence_strength}}` | Evidence strength rating: Strong (3+ vectors), Medium (2 vectors), or Light (1 vector) |

## Examples

### Example 1: Finding Salesforce Users for CRM Displacement

**User prompt:** "Find companies using Salesforce that could switch to our CRM. Target VP of Sales and CROs at mid-market SaaS companies in the US."

**What the skill does:**
1. Runs WebSearch queries:
- `"Salesforce" "case study" OR "customer story" OR "success story"`
- `"Salesforce" site:g2.com OR site:capterra.com`
- `"Salesforce" "we use" OR "we switched to" OR "we chose" site:linkedin.com OR site:reddit.com`
- `"Salesforce CRM" "experience with" OR "proficiency in" job OR hiring`
- `"Salesforce" site:stackshare.io OR site:builtwith.com`
2. Calls WebFetch on top results from each vector.
3. Extracts and deduplicates 47 companies found across vectors.
4. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each company.
5. Filters to 23 companies matching ICP (mid-market SaaS, US, 201-5000 employees).
6. Calls `mcp__claude_ai_Amplemarket__search_people` with `person_titles`: ["VP of Sales", "CRO", "Chief Revenue Officer"], `person_seniorities`: ["VP", "C-Suite"] for each company.

**Example output (abbreviated):**

---

**COMPETITOR DISPLACEMENT REPORT: Salesforce**

**Summary**
| Metric | Value |
|-----|-----|
| Competitor | Salesforce Sales Cloud |
| Companies Identified | 47 |
| Passed ICP Filter | 23 |
| Decision-Makers Found | 41 |
| Strong Evidence | 8 companies |
| Medium Evidence | 9 companies |
| Light Evidence | 6 companies |

**Strong Evidence Accounts**

| Company | Domain | Size | Evidence Types | Key Detail | Decision-Makers |
| --- | --- | --- | --- | --- | --- |
| CloudMetrics | cloudmetrics.io | 320 | Case Study + G2 + Job Posts | Featured in Salesforce case study; G2 review cites reporting gaps | 2 found |
| DataLoom | dataloom.com | 510 | Case Study + StackShare + Social | Listed on StackShare; founder posted about CRM frustrations | 3 found |
| RevStack | revstack.io | 280 | G2 + Job Posts + Social | 3-star G2 review mentioning cost concerns; hiring for "Salesforce admin" | 1 found |

**Dynamic fields for CloudMetrics contacts:**
- `{{competitor_name}}`: Salesforce Sales Cloud
- `{{competitor_evidence_type}}`: Case Study, G2 Review, Job Posting
- `{{competitor_evidence_detail}}`: Featured in Salesforce 2025 mid-market case study; left 3-star G2 review citing reporting limitations
- `{{competitor_evidence_url}}`: https://salesforce.com/customer-stories/cloudmetrics
- `{{competitor_pain_points}}`: Reporting inflexibility, high per-seat cost, complex admin overhead
- `{{competitor_company_name}}`: CloudMetrics
- `{{competitor_company_size}}`: 320 employees
- `{{competitor_company_industry}}`: Computer Software / Cloud Analytics
- `{{competitor_switch_reason}}`: G2 review explicitly mentions evaluating alternatives for better reporting
- `{{competitor_suggested_opener}}`: "I noticed CloudMetrics uses Salesforce for pipeline management. A few analytics companies your size have told us the reporting flexibility wasn't keeping up with their growth. Curious if that's something your team has run into."
- `{{competitor_evidence_strength}}`: Strong (3 vectors)

Would you like me to create a lead list from these 41 decision-makers?

---

### Example 2: Targeting Companies Using a Marketing Automation Tool

**User prompt:** "Find companies using Marketo. I want to reach Heads of Demand Gen and Marketing Directors at B2B companies with 500-2000 employees."

**What the skill does:**
1. Runs WebSearch queries across all 5 vectors using "Marketo" and "Adobe Marketo Engage" as search terms.
2. Fetches and extracts companies from case studies on marketo.com/customers, G2 reviews, job postings requiring "Marketo experience," and StackShare profiles.
3. Deduplicates 62 companies. Enriches via `mcp__claude_ai_Amplemarket__enrich_company`.
4. Filters to 31 B2B companies in the 500-2000 range.
5. Searches for `person_titles`: ["Head of Demand Gen", "Head of Demand Generation", "Director of Marketing", "Marketing Director"], `person_seniorities`: ["Head", "Director"].
6. Returns results grouped by evidence strength with `{{competitor_*}}` fields populated.
7. Offers to create lead list: "Marketo Displacement - Demand Gen Leaders - B2B 500-2K - Mar 2026".

**Example output (abbreviated):**

---

**COMPETITOR DISPLACEMENT REPORT: Marketo**

**Summary**
| Metric | Value |
|-----|-----|
| Competitor | Adobe Marketo Engage |
| Companies Identified | 62 |
| Passed ICP Filter | 31 |
| Decision-Makers Found | 48 |
| Strong Evidence | 11 companies |
| Medium Evidence | 12 companies |
| Light Evidence | 8 companies |

**Strong Evidence Accounts**

| Company | Domain | Size | Evidence Types | Key Detail | Decision-Makers |
| --- | --- | --- | --- | --- | --- |
| GrowthEngine | growthengine.io | 720 | Case Study + G2 + StackShare | Marketo customer story on Adobe site; listed on StackShare; G2 review mentions complexity | 3 found |
| LeadFlow | leadflow.com | 1,100 | G2 + Job Posts + Social | Hiring "Marketo Certified Expert"; founder posted about automation challenges | 2 found |
| PipelineHQ | pipelinehq.com | 580 | Case Study + Job Posts + BuiltWith | Featured in Marketo webinar; BuiltWith confirms Marketo tracking code | 2 found |

**Dynamic fields for GrowthEngine contacts:**
- `{{competitor_name}}`: Adobe Marketo Engage
- `{{competitor_evidence_type}}`: Case Study, G2 Review, StackShare
- `{{competitor_evidence_detail}}`: Featured in Adobe customer story for lead scoring automation; G2 review rates 3.5 stars citing steep learning curve
- `{{competitor_pain_points}}`: Complex setup requiring dedicated admin, steep learning curve, high cost relative to usage
- `{{competitor_company_name}}`: GrowthEngine
- `{{competitor_company_size}}`: 720 employees
- `{{competitor_company_industry}}`: Computer Software / Marketing Technology
- `{{competitor_switch_reason}}`: G2 review mentions "considering simpler alternatives", which indicates active evaluation
- `{{competitor_suggested_opener}}`: "I saw GrowthEngine uses Marketo for lead scoring. A few marketing teams your size have told us the complexity of maintaining Marketo workflows was pulling their ops team away from strategy work. Is that something you've experienced?"
- `{{competitor_evidence_strength}}`: Strong (3 vectors)

---

### Example 3: Multi-Competitor Search

**User prompt:** "Find companies using Outreach, Salesloft, or Apollo for sales engagement. Target VP Sales and Revenue Operations leaders at companies with 200-1000 employees."

**What the skill does:**
1. Runs separate WebSearch query sets for each competitor:
- 5 queries for "Outreach.io" / "Outreach sales engagement"
- 5 queries for "Salesloft" / "SalesLoft sales engagement"
- 5 queries for "Apollo.io" / "Apollo sales engagement"
2. Fetches top results across all three competitors.
3. Deduplicates across competitors, and flags companies found using multiple competitors (e.g., "Previously used Outreach, reviewed Salesloft on G2").
4. Enriches and filters to ICP: 200-1000 employees.
5. Searches for decision-makers: `person_titles`: ["VP of Sales", "VP Sales", "Head of Revenue Operations", "Director of Revenue Operations"], `person_seniorities`: ["VP", "Head", "Director"].
6. Presents results with the specific competitor each company uses in `{{competitor_name}}`, enabling tailored messaging per competitor.

**Example output (abbreviated):**

---

**COMPETITOR DISPLACEMENT REPORT: Outreach / Salesloft / Apollo**

**Summary**
| Metric | Value |
|-----|-----|
| Competitors | Outreach, Salesloft, Apollo |
| Companies Identified | 89 (Outreach: 41, Salesloft: 33, Apollo: 28, overlap: 13) |
| Passed ICP Filter | 52 |
| Decision-Makers Found | 74 |
| Multi-Competitor Companies | 13 (highest priority) |

**Multi-Competitor Accounts (Highest Priority)**

| Company | Domain | Size | Competitors Detected | Evidence | Decision-Makers |
| --- | --- | --- | --- | --- | --- |
| RevOpsHub | revopshub.com | 450 | Outreach + Salesloft | Job posting mentions both tools; G2 review compares the two | 2 found |
| CloseFaster | closefaster.io | 310 | Salesloft + Apollo | StackShare lists Salesloft; recent job post mentions Apollo migration | 1 found |

**Example note:** Multi-competitor accounts are flagged as highest priority because active tool evaluation or dissatisfaction with current tooling is strongly implied. The `{{competitor_name}}` field lists all detected tools (e.g., "Outreach + Salesloft") and `{{competitor_switch_reason}}` references the multi-tool complexity angle (e.g., "Company appears to be evaluating multiple sales engagement tools, which indicates active buying cycle").

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| WebSearch returns noisy results for common competitor names | Use the full product name or add the product category to the query (e.g., `"Monday.com" "project management"` instead of `"Monday"`). Include the competitor's domain in queries when possible (e.g., `site:outreach.io/customers`). |
| Very few companies found across all vectors | Expand evidence types: 1) Try searching for the competitor's integration partners page. 2) Search for conference talks mentioning the competitor. 3) Try `"powered by [competitor]"` or `"built on [competitor]"` queries. 4) Ask the user if they know specific customers to use as seeds. |
| Company enrichment fails for extracted company names | Fallback chain: 1) Try inferring the domain from the company name (e.g., "Acme Corp" -> acme.com). 2) Run a WebSearch for the company name + "site:linkedin.com/company" to find the correct domain. 3) Try `mcp__claude_ai_Amplemarket__enrich_company` with the LinkedIn URL. 4) Skip unenrichable companies and note them separately. |
| No decision-makers found at enriched companies | Fallback chain: 1) Broaden seniority to include "Manager" and "Senior". 2) Try searching by company name instead of domain. 3) For companies with fewer than 100 employees, search for "Founder" and "C-Suite" roles. 4) Suggest the user try `enrich_person` with specific names if they have them from the evidence sources. |
| Evidence is outdated (old case studies, stale reviews) | Flag the date of each evidence source when presenting results. Prioritize evidence from the last 18 months. For older evidence, add a note: "Evidence from [year]. Company may have switched since then. Consider verifying before outreach." Deprioritize to Light evidence strength if older than 2 years. |
| Too many companies pass the ICP filter | Tighten filters progressively: 1) Narrow company size range. 2) Add geography constraints. 3) Restrict to Strong and Medium evidence only. 4) Limit to specific sub-industries. Show the user updated counts after each filter change. |
| G2/Capterra pages blocked by WebFetch | Try alternate review aggregation queries: `"[competitor]" reviews OR "alternative to"`. Search for `"switched from [competitor]"` on Reddit or community forums. Some review content appears in Google snippets even when the full page is blocked. |
| Multiple competitors yield duplicate companies | This is a positive signal. Mark these companies as highest priority. Set `{{competitor_name}}` to list all detected competitors and use the multi-tool angle in `{{competitor_suggested_opener}}` (e.g., "I noticed your team has evaluated both Outreach and Salesloft. That tells me sales engagement tooling is top of mind"). |