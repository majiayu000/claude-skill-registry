---
name: lookalike-audience-builder
description: >
  Build a lookalike audience from a seed person, company, lead list, or website with customer logos, then search for similar profiles with match reasoning and personalization fields.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Prospecting & Lead Generation"
compatibility: Requires Amplemarket MCP server
---

# Lookalike Audience Builder

Build a lookalike audience from a seed person, company, lead list, or website with customer logos, then search for similar profiles with match reasoning and personalization fields.

## Instructions

When a user wants to find prospects similar to an existing person, company, lead list, or set of customers visible on a website, follow these steps to extract seed attributes, refine criteria, and search for lookalike matches.

### Steps

1. **Ask the user for a seed.** The seed can be any of:
    - A LinkedIn URL or email address (person seed)
    - A person's name + company (person seed)
    - A company name or domain (company seed)
    - An Amplemarket lead list name or ID (lead list seed)
    - A website URL that displays customer logos (website seed)
    
    If the user's request is ambiguous, ask which seed type they intend.
    
2. **Determine seed type and extract attributes.** Process the seed based on its type:
    - **Person seed:** Call `mcp__claude_ai_Amplemarket__enrich_person` with the LinkedIn URL, email, or name + company. Then call `mcp__claude_ai_Amplemarket__enrich_company` with the person's company domain. Extract:
        - Title and role keywords
        - Seniority level
        - Department / job function
        - Industry and sub-industry
        - Company size range
        - Company type
        - Location (person and company)
    - **Company seed:** Call `mcp__claude_ai_Amplemarket__enrich_company` with the company domain or LinkedIn URL. Extract:
        - Industry and sub-industry
        - Company size range
        - Company type (public, private, etc.)
        - Headquarters location
        - Tech stack and key signals
    - **Lead list seed:** Call `mcp__claude_ai_Amplemarket__get_lead_list` with the list ID or name. Analyze the leads to find common patterns:
        - Most frequent titles and seniority levels
        - Most common industries
        - Dominant company size ranges
        - Top locations
        - Shared departments or job functions
    - **Website seed:** Call `WebFetch` with the URL to retrieve the page content. Identify customer logos, company names, or "Trusted by" sections. For each identified customer company, call `mcp__claude_ai_Amplemarket__enrich_company` with the company domain. Aggregate the enrichment results to extract common attributes across the customer base:
        - Most frequent industries
        - Dominant company size ranges
        - Common company types
        - Geographic clusters
3. **Present extracted seed attributes** to the user in a clear summary. For person seeds, show a profile card. For company seeds, show a company card. For list and website seeds, show a pattern analysis table with frequency counts.
4. **Ask the user to prioritize attributes.** Present: "Based on the seed, here are the common attributes: [list]. Which are most important for finding lookalikes? Any attributes to exclude or override?" Wait for the user's response before proceeding.
5. **Resolve enum values** by calling:
    - `mcp__claude_ai_Amplemarket__get_industries` to validate and map industry terms to exact API values.
    - `mcp__claude_ai_Amplemarket__get_job_functions` to validate and map job function terms to exact API values.
    
    Match the user's prioritized attributes to the correct enum values.
    
6. **Run the lookalike search** by calling `mcp__claude_ai_Amplemarket__search_people` with refined filters based on the user's priorities. Set `full_output` to `true` and `page_size` to 20. Apply filters:
    - `person_titles`: title keywords from the seed (use variations)
    - `person_seniorities`: matched seniority level(s)
    - `person_departments`: matched department(s)
    - `person_locations`: seed location(s) or user-specified locations
    - `company_industries`: validated industry values
    - `company_sizes`: seed company size range (expand by one tier in each direction)
    - `company_types`: seed company type if relevant
    - Exclude the seed person or company from results where possible using negative filters.
7. **Present results with match reasoning.** Format results as a table with columns: Name, Title, Company, Location, Match Reason. For each prospect, generate a concise match reason explaining which attributes align with the seed (e.g., "Same seniority + industry + company size range as seed").
8. **Generate dynamic fields** for each matched prospect. Populate the `{{lookalike_*}}` fields described in the Dynamic Fields Generated section below. These fields can be used in outreach templates to reference the similarity between the prospect and the seed.
9. **Offer to create a lead list** with the lookalike results. If the user agrees, call `mcp__claude_ai_Amplemarket__create_lead_list` with:
    - `name`: a descriptive name (e.g., "Lookalikes of Sarah Chen - VP Marketing - Mar 2026")
    - `type`: "linkedin" (if LinkedIn URLs are available) or "email"
    - `leads`: array of lead objects from the search results
    - `options`: ask about enrichment preferences (`enrich`, `validate_email`, `reveal_phone_numbers`)
    
    Include the lookalike context fields in the list description so downstream outreach can reference the match reasoning.
    

### Important Notes

- Always validate industry and job function values via the API before searching. Never guess enum values.
- For website seeds, only extract companies that are clearly identifiable as customers (look for "Trusted by", "Our customers", "Used by" sections). Do not include partners or integration logos.
- When the seed is a lead list, analyze at least 10 leads (or all leads if fewer than 10) to establish reliable patterns.
- If the lookalike search returns zero results, relax filters one at a time in priority order: location first, then company size, then seniority, then industry.
- Exclude the original seed person or company from the results to avoid duplicate outreach.

## Dynamic Fields Generated

| Field | Description |
| --- | --- |
| `{{lookalike_seed_name}}` | Name of the seed person or company used as the basis for the search |
| `{{lookalike_match_reason}}` | Why this prospect matches the seed (e.g., "Same title + industry + company size as seed") |
| `{{lookalike_shared_attributes}}` | Comma-separated list of shared attributes (e.g., "VP-level, SaaS industry, 201-500 employees") |
| `{{lookalike_company_similarity}}` | How the prospect's company compares to the seed company (e.g., "Similar stage Series B SaaS, 30% smaller headcount") |
| `{{lookalike_seniority_match}}` | Whether seniority level matches the seed (e.g., "Exact match: VP-level") |
| `{{lookalike_industry_match}}` | Whether industry matches the seed (e.g., "Same industry: Computer Software") |
| `{{lookalike_title_similarity}}` | How the prospect's title compares to the seed (e.g., "Equivalent role: VP Marketing vs. Head of Marketing") |
| `{{lookalike_location_match}}` | Whether location aligns with the seed (e.g., "Same metro: San Francisco Bay Area") |
| `{{lookalike_company_size_match}}` | Whether company size is similar to the seed (e.g., "Adjacent range: 501-1000 vs. seed 201-500") |
| `{{lookalike_suggested_opener}}` | Draft opening line referencing the similarity (e.g., "I work with several VP Marketing leaders at Series B SaaS companies like [seed company]. Thought you might face similar challenges at [prospect company].") |

## Examples

### Example 1: Person Seed (LinkedIn URL)

**User prompt:** "Find people like linkedin.com/in/sarah-chen-vp-marketing"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `linkedin_url`: "https://linkedin.com/in/sarah-chen-vp-marketing", `reveal_email`: true.
2. Calls `mcp__claude_ai_Amplemarket__enrich_company` with domain from enrichment (e.g., "cloudmetrics.io").
3. Extracts seed attributes: VP of Marketing, VP seniority, Marketing department, Cloud Analytics / Computer Software industry, 180 employees (201-500 range), Austin TX.
4. Presents: "Seed profile - Sarah Chen, VP Marketing at CloudMetrics. Key attributes: VP-level, Marketing, Software/Analytics industry, 201-500 employees, Austin TX. Which matter most?"
5. User says: "Title and industry are most important, location doesn't matter."
6. Calls `mcp__claude_ai_Amplemarket__get_industries` and `mcp__claude_ai_Amplemarket__get_job_functions` to validate values.
7. Calls `mcp__claude_ai_Amplemarket__search_people` with:
- `person_titles`: ["VP of Marketing", "VP Marketing", "Vice President of Marketing", "Head of Marketing"]
- `person_seniorities`: ["VP", "Head"]
- `person_departments`: ["Marketing"]
- `company_industries`: [matched software/analytics values]
- `company_sizes`: ["51-200 employees", "201-500 employees", "501-1000 employees"]
- `full_output`: true, `page_size`: 20

**Example output:**

| Name | Title | Company | Location | Match Reason |
| --- | --- | --- | --- | --- |
| David Park | VP of Marketing | DataLoom | Boston, MA | Same title + industry + company size as seed |
| Lisa Nguyen | Head of Marketing | MetricFlow | Denver, CO | Equivalent seniority, same industry, adjacent size |
| Tom Rivera | VP Marketing & Growth | AnalyticsPro | Chicago, IL | Same title + industry, slightly larger company |

Found 83 total lookalike matches. Showing page 1 of 5.

**Dynamic fields for David Park:**
- `{{lookalike_seed_name}}`: Sarah Chen (VP Marketing, CloudMetrics)
- `{{lookalike_match_reason}}`: Same title, industry, and company size range as seed
- `{{lookalike_shared_attributes}}`: VP-level, Marketing, Computer Software, 201-500 employees
- `{{lookalike_company_similarity}}`: DataLoom is a similar-stage analytics company with 220 employees vs. CloudMetrics' 180
- `{{lookalike_seniority_match}}`: Exact match: VP-level
- `{{lookalike_industry_match}}`: Same industry: Computer Software
- `{{lookalike_title_similarity}}`: Exact match: VP of Marketing
- `{{lookalike_location_match}}`: Different city (Boston vs. Austin), user excluded location
- `{{lookalike_company_size_match}}`: Same range: 201-500 employees
- `{{lookalike_suggested_opener}}`: "I work with several VP Marketing leaders at analytics companies like CloudMetrics. Thought you might face similar demand gen challenges scaling at DataLoom."

Would you like me to create a lead list from these 83 lookalike matches?

### Example 2: Website with Customer Logos Seed

**User prompt:** "Build a lookalike audience from the customers on acme-analytics.com/customers"

**What the skill does:**
1. Calls `WebFetch` with URL "https://acme-analytics.com/customers" to retrieve the page content.
2. Identifies customer logos and company names from the "Trusted by" section: Stripe, Notion, Figma, Datadog, Plaid.
3. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each: stripe.com, notion.so, figma.com, datadoghq.com, plaid.com.
4. Analyzes patterns across the 5 companies:
- Industries: 4/5 Computer Software, 3/5 Fintech-adjacent
- Sizes: 3/5 in 1001-5000 range, 2/5 in 5001-10000 range
- Types: 3/5 Privately Held, 2/5 Public Company
- Locations: 4/5 San Francisco Bay Area
5. Presents pattern analysis and asks: "Common profile across these customers: mid-to-late-stage software companies, 1000-10000 employees, mostly Bay Area. Which attributes matter most?"
6. User says: "Industry and size are key. Search for VP Engineering and CTO at similar companies."
7. Validates enums, then calls `mcp__claude_ai_Amplemarket__search_people` with:
- `person_titles`: ["VP of Engineering", "VP Engineering", "CTO", "Chief Technology Officer"]
- `person_seniorities`: ["VP", "C-Suite"]
- `person_departments`: ["Engineering & Technical"]
- `company_industries`: [matched software values]
- `company_sizes`: ["1001-5000 employees", "5001-10000 employees"]
- `full_output`: true, `page_size`: 20
8. Returns results with match reasoning referencing the customer pattern, not a single seed.

**Example output:**

| Name | Title | Company | Location | Match Reason |
| --- | --- | --- | --- | --- |
| Raj Mehta | VP of Engineering | Streamline AI | San Francisco, CA | Same industry + size range as 4/5 seed customers |
| Kim Okada | CTO | PaymentGrid | New York, NY | Fintech-adjacent software, 2000 employees matches seed pattern |
| Alex Werner | VP Engineering | CloudVault | Austin, TX | Software industry, 1500 employees, matches seed company profile |

Found 156 total lookalike matches. Showing page 1 of 8.

**Dynamic fields for Raj Mehta:**
- `{{lookalike_seed_name}}`: Acme Analytics customer base (Stripe, Notion, Figma, Datadog, Plaid)
- `{{lookalike_match_reason}}`: Company profile matches 4/5 seed customer attributes: Software industry, 1001-5000 employees, Privately Held, Bay Area
- `{{lookalike_shared_attributes}}`: Computer Software, 1001-5000 employees, Privately Held, San Francisco Bay Area
- `{{lookalike_company_similarity}}`: Streamline AI is a mid-stage AI software company with 1,200 employees, similar profile to Datadog and Plaid at comparable stages
- `{{lookalike_seniority_match}}`: VP-level as requested
- `{{lookalike_industry_match}}`: Same industry: Computer Software
- `{{lookalike_title_similarity}}`: VP of Engineering - matches requested persona
- `{{lookalike_location_match}}`: San Francisco Bay Area - matches 4/5 seed customers
- `{{lookalike_company_size_match}}`: Same range: 1001-5000 employees (matches 3/5 seed customers)
- `{{lookalike_suggested_opener}}`: "Companies like Stripe and Datadog trust Acme Analytics for their cloud metrics. Given Streamline AI is at a similar stage, I thought it might be relevant to your engineering team too."

Would you like me to create a lead list from these 156 lookalike matches?

### Example 3: Lead List Seed

**User prompt:** "Find more prospects similar to my 'Q4 Closed Won' lead list"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__list_lead_lists` to find the list, then `mcp__claude_ai_Amplemarket__get_lead_list` with the matching list ID.
2. Analyzes the leads in the list (e.g., 25 leads). Finds common patterns:
- Titles: 60% Director-level, 25% VP-level, 15% Manager
- Departments: 80% Revenue/Sales, 20% Marketing
- Industries: 70% Financial Services, 20% Insurance
- Company sizes: 65% 501-1000, 25% 1001-5000
- Locations: 50% Northeast US, 30% Midwest
3. Presents: "Your closed-won leads are predominantly Director/VP-level in Revenue at financial services companies with 500-5000 employees, concentrated in the Northeast. Which patterns should I prioritize?"
4. User says: "Focus on the Director-level Revenue people at financial services. Expand to all US locations."
5. Validates enums and runs:
- `person_seniorities`: ["Director", "VP"]
- `person_departments`: ["Revenue"]
- `company_industries`: [matched financial services values]
- `company_sizes`: ["501-1000 employees", "1001-5000 employees"]
- `person_locations`: ["United States"]
- `full_output`: true, `page_size`: 20
6. Returns results with match reasoning referencing the closed-won pattern.

**Example output:**

| Name | Title | Company | Location | Match Reason |
| --- | --- | --- | --- | --- |
| Angela Torres | Director of Sales | Heritage Financial Group | Dallas, TX | Matches 4/5 closed-won attributes: Director, Revenue, Financial Services, 501-1000 |
| Brian Caldwell | VP of Revenue | Midwest Bancorp | Chicago, IL | Matches 5/5 closed-won attributes: VP, Revenue, Financial Services, 1001-5000, Midwest |
| Nadia Hassan | Director of Business Development | SecureInsure | Atlanta, GA | Matches 3/5: Director, Revenue-adjacent, Insurance (related industry) |

Found 210 total lookalike matches. Showing page 1 of 11.

**Dynamic fields for Angela Torres:**
- `{{lookalike_seed_name}}`: Q4 Closed Won lead list (25 leads)
- `{{lookalike_match_reason}}`: Matches 4/5 closed-won pattern attributes: Director-level, Revenue department, Financial Services, 501-1000 employees
- `{{lookalike_shared_attributes}}`: Director-level, Revenue, Financial Services, 501-1000 employees
- `{{lookalike_company_similarity}}`: Heritage Financial Group is a mid-size financial services firm with 650 employees, aligning with the 501-1000 range dominant in closed-won deals
- `{{lookalike_seniority_match}}`: Exact match: Director-level (60% of closed-won leads)
- `{{lookalike_industry_match}}`: Same industry: Financial Services (70% of closed-won leads)
- `{{lookalike_title_similarity}}`: Director of Sales - consistent with Revenue department pattern
- `{{lookalike_location_match}}`: Dallas, TX - outside the dominant Northeast cluster but within expanded US scope per user request
- `{{lookalike_company_size_match}}`: Same range: 501-1000 employees (65% of closed-won leads)
- `{{lookalike_suggested_opener}}`: "We have helped several Directors of Sales at financial services companies similar to Heritage Financial Group. Happy to share what has worked for them if useful."

1. Offers to create a "Lookalikes of Q4 Closed Won - Mar 2026" lead list.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Zero results from lookalike search | Relax filters one at a time in this order: 1) Remove location filter. 2) Expand company size by one tier in each direction. 3) Broaden seniority to include one adjacent level. 4) Add related industry values from `mcp__claude_ai_Amplemarket__get_industries`. Report each change to the user. |
| Website seed yields no customer logos | Ask the user to provide specific company names instead. Alternatively, try fetching alternate pages like /customers, /case-studies, or /about. |
| Lead list seed has too few leads for pattern analysis | If fewer than 5 leads, warn the user that patterns may not be reliable. Suggest supplementing with additional seed data or treating the top 1-2 leads as individual person seeds. |
| Enrichment fails for seed person or company | Fallback chain: 1) Try alternate identifiers (domain instead of name, LinkedIn URL instead of email). 2) If person enrichment fails, fall back to company-only seed. 3) Ask the user for additional identifiers. |
| Too many results, audience is too broad | Add more filters from the seed attributes the user deprioritized. Tighten company size range. Add `person_departments` or `company_types` constraints. Show a refined preview after each adjustment. |
| Match reasoning feels generic | Ensure you are comparing specific attribute values, not just categories. Reference exact titles, company sizes, and industries rather than saying "similar profile." |
| Seed company exists but `enrich_company` returns sparse data | Fallback chain: 1) Try the company LinkedIn URL. 2) Try `mcp__claude_ai_Amplemarket__search_companies` with the domain. 3) Use whatever partial data is available and note gaps to the user. |
| WebFetch returns blocked or empty page | Some sites block automated fetches. Ask the user to paste the customer list manually, or try an alternate URL on the same domain (e.g., /about, /case-studies). |