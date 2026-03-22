---
name: prospect-icp-search
description: >
  Search for prospects matching an Ideal Customer Profile using natural language. This skill translates human-friendly buyer descriptions into structured Amplemarket API queries and returns formatted results.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Prospecting & Lead Generation"
compatibility: Requires Amplemarket MCP server
---

# Prospect ICP Search

Search for prospects matching an Ideal Customer Profile using natural language. This skill translates human-friendly buyer descriptions into structured Amplemarket API queries and returns formatted results.

## Instructions

When a user describes their ideal prospect in natural language, follow these steps to execute a precise search using the Amplemarket MCP tools.

### Steps

1. **Parse the user's criteria** into structured filters:
    - **Titles** (e.g., "VP of Sales", "Head of Marketing")
    - **Seniority levels** (map to enums: "Owner", "Founder", "C-Suite", "Partner", "VP", "Head", "Director", "Manager", "Senior", "Entry", "Intern", "Other")
    - **Person locations** (cities, states, countries, max 10)
    - **Departments** (map to enums: "Senior Leadership", "Design", "Education", "Consulting", "Engineering & Technical", "Finance", "Human Resources", "Information Technology", "Legal", "Marketing", "Operations", "Revenue", "Medical & Health", "Product")
    - **Company names or domains**
    - **Company locations**
    - **Company industries** (resolve via step 2)
    - **Company sizes** (map to enums: "1-10 employees", "11-50 employees", "51-200 employees", "201-500 employees", "501-1000 employees", "1001-5000 employees", "5001-10000 employees", "10001+ employees")
    - **Company types** (map to enums: "Public Company", "Educational", "Self Employed", "Government Agency", "Non Profit", "Self Owned", "Privately Held", "Partnership")
2. **Resolve industries and job functions** by calling:
    - `mcp__claude_ai_Amplemarket__get_industries` to get the list of valid industry values and match the user's description to the closest ones.
    - `mcp__claude_ai_Amplemarket__get_job_functions` to get valid job function values if the user specifies functional areas.
3. **Execute the search** by calling `mcp__claude_ai_Amplemarket__search_people` with the mapped parameters. Set `full_output` to `true` for detailed results. Start with `page_size` of 10 unless the user requests more.
4. **Format the results** as a clean table with columns:
    - Name
    - Title
    - Company
    - Location
    - LinkedIn URL
5. **Offer next actions** after presenting results:
    - "Would you like me to enrich any of these prospects for full contact details?"
    - "Should I create a lead list from these results?"
    - "Want me to expand the search with different criteria or load more results?"

### Important Notes

- Always resolve industries and job functions from the API before searching. Do not guess enum values.
- If the user's criteria are ambiguous, ask for clarification before searching.
- When location is specified as a broad region (e.g., "Europe"), break it into specific countries.
- If the search returns zero results, suggest relaxing one filter at a time and explain which filter is most likely too restrictive.

## Examples

### Example 1: Role + Industry + Location + Size

**User prompt:** "Find me VP of Sales at fintech companies in New York with 50 to 200 employees"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__get_industries` to find the correct fintech industry value.
2. Calls `mcp__claude_ai_Amplemarket__search_people` with:
- `person_titles`: ["VP of Sales"]
- `person_seniorities`: ["VP"]
- `person_locations`: ["New York, US"]
- `company_industries`: [matched fintech industry value]
- `company_sizes`: ["51-200 employees"]
- `full_output`: true
3. Returns a formatted table of matching prospects.

**Example output:**

| Name | Title | Company | Location | LinkedIn |
| --- | --- | --- | --- | --- |
| Sarah Chen | VP of Sales | PayTech Inc | New York, NY | linkedin.com/in/sarachen |
| Marcus Johnson | VP of Sales & Partnerships | FinFlow | New York, NY | linkedin.com/in/marcusj |
| Priya Patel | Vice President, Sales | LendStack | Brooklyn, NY | linkedin.com/in/priyap |

Found 47 total results. Showing page 1 of 5.

Would you like me to:
- Enrich any of these prospects for email and phone?
- Create a lead list from all 47 results?
- See the next page of results?

### Example 2: Department + Seniority + Company Type

**User prompt:** "Search for marketing directors at publicly traded SaaS companies in the Bay Area"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__get_industries` to resolve SaaS/Software industry values.
2. Calls `mcp__claude_ai_Amplemarket__search_people` with:
- `person_titles`: ["Marketing Director", "Director of Marketing"]
- `person_seniorities`: ["Director"]
- `person_departments`: ["Marketing"]
- `person_locations`: ["San Francisco Bay Area, US"]
- `company_types`: ["Public Company"]
- `company_industries`: [matched SaaS/Software values]
- `full_output`: true

### Example 3: Multi-Title Search with Company Size

**User prompt:** "Look up Heads of Engineering and CTOs at startups with 11-50 employees in London and Berlin"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__search_people` with:
- `person_titles`: ["Head of Engineering", "CTO", "Chief Technology Officer"]
- `person_seniorities`: ["Head", "C-Suite"]
- `person_departments`: ["Engineering & Technical"]
- `person_locations`: ["London, UK", "Berlin, DE"]
- `company_sizes`: ["11-50 employees"]
- `full_output`: true

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Zero results returned | Broaden one filter at a time in this order: 1) Remove geography filter and retry. 2) Broaden company size range by one tier in each direction. 3) Broaden seniority to include one level below target. 4) Try related industry values from `get_industries`. After each retry, report to the user what was changed and how many results the broadened criteria returned. |
| Too many results | Add more filters. Narrow by seniority, department, or company size. |
| Industry not matching | Call `mcp__claude_ai_Amplemarket__get_industries` and present the list to the user so they can pick the right value. |
| Location too broad | Break regions into specific cities or countries (max 10 locations per query). |
| Unexpected titles in results | Use `person_seniorities` and `person_departments` in addition to `person_titles` to improve precision. |
| Company definitely exists but `search_companies` returns 0 | Fallback chain: 1) Try `enrich_company` with the company domain directly. 2) Try searching by partial name. 3) Check for parent/subsidiary company names. 4) Try the company's LinkedIn URL in `enrich_company`. |
| Multiple people match a specific name | Use additional filters like `person_locations` or `company_domains` to narrow results. If still ambiguous, present matches and ask the user to confirm. |