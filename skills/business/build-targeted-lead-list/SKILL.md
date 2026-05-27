---
name: build-targeted-lead-list
description: >
  End-to-end workflow to search for prospects, preview results, refine criteria, and create a confirmed lead list in Amplemarket.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Prospecting & Lead Generation"
compatibility: Requires Amplemarket MCP server
---

# Build Targeted Lead List

End-to-end workflow to search for prospects, preview results, refine criteria, and create a confirmed lead list in Amplemarket.

## Instructions

Guide the user through building a lead list from scratch. This is a multi-step, interactive workflow.

### Steps

1. **Gather search criteria** from the user. Ask for any of:
    - Target titles and seniority levels
    - Target departments or job functions
    - Person locations
    - Company names, domains, industries, sizes, or types
    - Any other qualifying criteria
    
    If the user gives a broad description, parse it into structured filters (see the prospect-icp-search skill for mapping guidance).
    
2. **Resolve enum values** by calling:
    - `mcp__claude_ai_Amplemarket__get_industries` to match industry terms to valid API values.
    - `mcp__claude_ai_Amplemarket__get_job_functions` to match job function terms to valid API values.
3. **Execute the search** by calling `mcp__claude_ai_Amplemarket__search_people` with the mapped parameters. Set `full_output` to `true` and `page_size` to 20 for the preview.
4. **Present a preview** of the results to the user:
    - Show the first 10-20 results in a table (Name, Title, Company, Location).
    - Report the total number of matching prospects.
    - Ask: "Does this look right? Would you like to refine the search or proceed with creating the list?"
5. **Refine if needed.** If the user wants changes:
    - Adjust filters based on feedback.
    - Re-run `mcp__claude_ai_Amplemarket__search_people` with updated parameters.
    - Show the updated preview.
    - Repeat until the user approves.
6. **Collect all results** once approved. If total results exceed one page, paginate through all pages using the `page` parameter to gather all LinkedIn URLs (up to the 10,000 lead limit).
7. **Ask for list configuration:**
    - **List name** (suggest a descriptive default like "VP Sales - Fintech - NYC - Mar 2026")
    - **List type** - determine based on available data:
        - `"linkedin"` if leads have LinkedIn URLs
        - `"email"` if leads have email addresses
        - `"titles_and_company"` if leads have title + company domain
    - **Enrichment options:** Ask if they want to enable (note: each option consumes additional Amplemarket credits per lead):
        - Email enrichment (`enrich`: true)
        - Email validation (`validate_email`: true)
        - Phone number reveal (`reveal_phone_numbers`: true)
    - Inform the user of the credit implications before enabling enrichment: "Enabling enrichment will use credits for each lead. For a list of [N] leads, that's [N] enrichment credits. Want to proceed?"
8. **Create the lead list** by calling `mcp__claude_ai_Amplemarket__create_lead_list` with:
    - `type`: determined list type
    - `name`: chosen name
    - `leads`: array of lead objects (with `linkedin_url`, `email`, or `title` + `company_domain` depending on type)
    - `options`: enrichment settings
    
    If total leads exceed the batch that fits in a single create call, use `mcp__claude_ai_Amplemarket__add_leads_to_lead_list` to add remaining leads to the created list using the returned `lead_list_id`.
    
9. **Confirm creation** with the user:
    - Lead list ID
    - Total leads added
    - Enrichment settings enabled
    - Estimated processing time

### Important Notes

- The `leads` array in `create_lead_list` supports a maximum of 10,000 entries.
- Always show a preview before creating the list. Never create without user confirmation.
- When using `add_leads_to_lead_list`, include the `lead_list_id` from the create response.
- If the user provides a ready-made list of LinkedIn URLs or emails, skip the search step and go directly to list creation.

## Examples

### Example 1: Full Workflow from Search to List

**User prompt:** "Build me a lead list of engineering managers at healthcare companies in the US with 500-5000 employees"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__get_industries` to resolve healthcare industry values.
2. Calls `mcp__claude_ai_Amplemarket__search_people` with:
- `person_titles`: ["Engineering Manager"]
- `person_seniorities`: ["Manager"]
- `person_departments`: ["Engineering & Technical"]
- `person_locations`: ["United States"]
- `company_industries`: [matched healthcare values]
- `company_sizes`: ["501-1000 employees", "1001-5000 employees"]
- `full_output`: true, `page_size`: 20
3. Presents preview table and total count.
4. On user approval, collects all results across pages.
5. Calls `mcp__claude_ai_Amplemarket__create_lead_list` with:
- `type`: "linkedin"
- `name`: "Eng Managers - Healthcare US - 500-5K - Mar 2026"
- `leads`: [{"linkedin_url": "..."}, ...]
- `options`: {"enrich": true, "validate_email": true}

**Example confirmation:**

Lead list created successfully.

| Detail | Value |
| --- | --- |
| List ID | lst_abc123def456 |
| List Name | Eng Managers - Healthcare US - 500-5K - Mar 2026 |
| Total Leads | 312 |
| Type | LinkedIn |
| Enrichment | Enabled |
| Email Validation | Enabled |
| Status | Processing |

Your list is now being enriched. You can check its status anytime.

### Example 2: Quick List from Existing URLs

**User prompt:** "Create a lead list called 'Q1 Targets' from these LinkedIn URLs: linkedin.com/in/user1, linkedin.com/in/user2, linkedin.com/in/user3"

**What the skill does:**
1. Skips search since the user has provided leads directly.
2. Calls `mcp__claude_ai_Amplemarket__create_lead_list` with:
- `type`: "linkedin"
- `name`: "Q1 Targets"
- `leads`: [{"linkedin_url": "https://linkedin.com/in/user1"}, {"linkedin_url": "https://linkedin.com/in/user2"}, {"linkedin_url": "https://linkedin.com/in/user3"}]
- `options`: {"enrich": true, "validate_email": true, "reveal_phone_numbers": true}

### Example 3: Refined Search Workflow

**User prompt:** "Put together a list of senior marketing people at Series B+ SaaS companies in Europe"

**What the skill does:**
1. Resolves industries via `mcp__claude_ai_Amplemarket__get_industries`.
2. Runs initial search with `person_seniorities`: ["Senior", "Manager", "Director", "VP", "Head"], `person_departments`: ["Marketing"], `person_locations`: ["United Kingdom", "Germany", "France", "Netherlands", "Sweden", ...], matched SaaS industries.
3. Shows preview. User says "too many junior people, only Directors and above."
4. Re-runs with `person_seniorities`: ["Director", "VP", "Head", "C-Suite"].
5. Shows updated preview. User approves.
6. Creates list with all results.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Too many results to fit in one list | Paginate through results and use `mcp__claude_ai_Amplemarket__add_leads_to_lead_list` for batches after the first create call. |
| List creation fails | Verify that leads array format matches the list type. LinkedIn lists need `linkedin_url`, email lists need `email`, titles_and_company lists need `title` + `company_domain`. |
| Search returns irrelevant results | Tighten filters progressively: 1) Add `person_seniorities` to exclude junior titles. 2) Add `person_departments` to restrict to relevant functions. 3) Add `company_sizes` if results include wrong-size companies. Show the user a preview after each refinement so they can confirm the direction. |
| User wants to add to existing list | Use `mcp__claude_ai_Amplemarket__list_lead_lists` to find the existing list, then `mcp__claude_ai_Amplemarket__add_leads_to_lead_list` with its ID. |
| Enrichment not working | Check that the `options` object is correctly structured with boolean values for `enrich`, `validate_email`, and `reveal_phone_numbers`. |
| `search_companies` returns 0 results for a known company | Fallback chain: 1) Try searching by company domain instead of name. 2) Try `enrich_company` with the domain directly, as some companies are enrichable but not searchable by name. 3) Try parent company domain or alternate domains. |
| Search returns results but list creation fails | Verify that the leads array format matches the list type. LinkedIn lists need `linkedin_url`, email lists need `email`. |