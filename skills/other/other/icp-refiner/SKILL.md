---
name: icp-refiner
description: >
  Interactively refine your Ideal Customer Profile through guided questions, web research, and iterative Amplemarket searches until your targeting criteria are dialed in.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Configuration"
compatibility: Requires Amplemarket MCP server
---

| Problem | Solution |
| --- | --- |
| Zero results returned | Relax filters one at a time in this order: 1) Remove geography restrictions. 2) Broaden company size by one tier in each direction. 3) Add adjacent seniority levels (e.g., add Manager if only targeting Director+). 4) Try related industry values from `mcp__claude_ai_Amplemarket__get_industries`. Report each change and its impact on result count. |
| Too many results (10,000+) | Add filters progressively: 1) Restrict seniority to Director+ or VP+. 2) Narrow company size to 1-2 tiers. 3) Add geography constraints. 4) Exclude low-fit industries. Show the user the count after each change so they can decide when to stop. |
| Industry values don't match user's description | Call `mcp__claude_ai_Amplemarket__get_industries` and present the closest 5-10 options. Let the user pick which ones apply. Common mismatches: "SaaS" maps to "Computer Software" or "Internet"; "fintech" maps to "Financial Services" or "Banking". |
| User doesn't know their ICP at all | Start with WebSearch to research their company and product. Identify the product category, then suggest a default ICP based on common buyer personas for that category (e.g., developer tools typically sell to VP Engineering / CTO at mid-market software companies). Run a broad initial search and let the data guide refinement. |
| Conflicting criteria from user | Surface the conflict explicitly: "You mentioned targeting startups (1-50 employees) but also said your average deal is $50K/year. That price point typically fits 200+ employee companies. Which should we prioritize?" Let the user resolve the tension, then adjust. |
| search_people returns unexpected results | Verify enum values by rechecking `mcp__claude_ai_Amplemarket__get_industries` and `mcp__claude_ai_Amplemarket__get_job_functions`. Common issues: 1) Industry values are outdated, so re-fetch. 2) Title keywords match unrelated roles, so add department filter to constrain. 3) Location strings are ambiguous, so use "City, Country" format. 4) Company size enum doesn't match, so use exact values like "201-500 employees". |
| Enriched best customer has sparse data | Try enriching with the company's LinkedIn URL or alternate domains. If firmographic data is limited, fall back to asking the user to describe the company profile manually and use that as the basis for the ICP hypothesis. |

# ICP Refiner

Interactively refine your Ideal Customer Profile through guided questions, web research, and iterative Amplemarket searches until your targeting criteria are dialed in.

## Instructions

When a user wants help defining, sharpening, or narrowing their Ideal Customer Profile, guide them through a structured conversation that combines their domain knowledge with real market data from Amplemarket.

### Steps

1. **Ask the user foundational questions** to establish a starting ICP hypothesis. Gather:
    - **What product/service do you sell?** Understanding the value prop determines which roles and industries to target.
    - **Who are your best customers today?** Ask for 2-3 company names or domains. These anchor the firmographic profile.
    - **What role buys your product?** Target titles, seniority, and department (e.g., "VP of Engineering" or "marketing leaders").
    - **What is your typical deal size?** This guides company size targeting (smaller deals align with SMB, larger with enterprise).
    - **Who should be excluded?** Industries, company types, or geographies that are not a fit (e.g., "no government or non-profits").
    - **Who are your competitors?** Ask for competitor company names and/or domains. These will be excluded from all search results to ensure the ICP only contains potential buyers, not competitors or companies that sell similar products.
    
    If the user already has a partial ICP, skip questions they have answered and focus on gaps. Present questions conversationally, do not dump all five at once. Start with the most important (product and best customers) and follow up based on responses.
    
2. **Research the user's company** by calling `WebSearch` with the user's company name or domain to understand their positioning, product category, and competitive landscape. Use the findings to validate and enrich the ICP hypothesis. For example, if the company sells developer tools, prioritize engineering and IT departments.
3. **Enrich best customer examples** if the user provided company names or domains. Call `mcp__claude_ai_Amplemarket__enrich_company` for each example company (up to 3). Extract firmographic attributes:
    - Industry and sub-industry
    - Company size (employee count)
    - Company type (privately held, public, etc.)
    - Location and headquarters
    - Technology stack (if relevant to the user's product)
    
    Look for patterns across the examples. Shared industries, similar sizes, or common company types form the foundation of the ICP.
    
4. **Map descriptions to valid enum values** by calling:
    - `mcp__claude_ai_Amplemarket__get_industries` to match the user's industry descriptions and the enriched company industries to valid API values.
    - `mcp__claude_ai_Amplemarket__get_job_functions` to match target departments and roles to valid API values.
    
    Present the mapped values to the user for confirmation: "Based on your input, I'm mapping your target industries to [X, Y, Z]. Does that look right?"
    
5. **Run the first search with the initial ICP hypothesis** by calling `mcp__claude_ai_Amplemarket__search_people` with:
    - `person_titles`: derived from target role
    - `person_seniorities`: mapped seniority levels
    - `person_departments`: mapped department values
    - `person_locations`: target geographies
    - `company_industries`: resolved industry values
    - `company_sizes`: inferred from deal size and best customer patterns
    - `company_types`: if exclusions specified
    - `full_output`: true
    - `page_size`: 20
    
    **Competitor exclusion:** After retrieving results, filter out any prospects who work at companies the user identified as competitors. Also use `WebSearch` to identify additional competitors in the same product category (e.g., search for "[user's product category] competitors" or "[user's company] alternatives") and exclude those as well. When presenting results, flag and remove any company that appears to sell a similar product, as these are competitors, not prospects. If uncertain whether a company is a competitor, check their website description from enrichment data and ask the user: "I found [company] in the results. They seem to sell [similar product]. Should I exclude them?"
    
    Report the total result count to the user: "Your initial ICP returns **8,421 prospects** (after excluding X competitors). Let's look at the distribution to see if we need to narrow or adjust."
    
6. **Present a distribution breakdown** of the search results. Analyze the returned prospects and summarize:
    - **By title**: Top 5 most common titles and their percentage of results
    - **By industry**: Top 5 industries represented
    - **By company size**: Distribution across size ranges
    - **By location**: Top geographies represented
    
    Present the distribution as a formatted summary:
    
    **Title Distribution:**
    
    - VP of Sales: 18% (2,156)
    - Director of Sales: 29% (3,468)
    - Sales Manager: 38% (4,548)
    - Other: 15% (1,793)
    
    **Industry Distribution:**
    
    - Computer Software: 41%
    - Internet: 22%
    - Staffing & Recruiting: 14%
    - Other: 23%
    
    Ask the user targeted questions based on the distribution:
    
    - "42% of results are Managers - do you want to keep them or focus on Director+ only?"
    - "I see a lot of results from the Staffing & Recruiting industry - should we exclude that?"
    - "Most prospects are in the US - do you want to add or restrict geographies?"
7. **Iterate 2-3 times based on feedback.** For each round of refinement:
    - Adjust the search filters based on user responses (add seniority filters, exclude industries, narrow geographies, change company size ranges).
    - Call `mcp__claude_ai_Amplemarket__search_people` with the updated parameters.
    - Report the new result count and how it changed: "Narrowed from **8,421** to **3,247** by restricting to Director+ seniority and excluding Staffing & Recruiting."
    - Show the updated distribution if the user wants to keep refining.
    - Continue until the user is satisfied or the count is in a reasonable range for their use case.
8. **Present the final ICP definition** in a structured format:
    
    **Your Refined ICP**
    
    | Criteria | Value |
    | --- | --- |
    | Target Titles | VP of Sales, Director of Sales, Head of Revenue |
    | Seniority | VP, Director, Head |
    | Department | Revenue |
    | Industries | Computer Software, Internet, SaaS |
    | Company Size | 201-500 employees, 501-1000 employees |
    | Company Type | Privately Held |
    | Locations | United States, United Kingdom |
    | Exclusions | Non Profit, Government Agency; Staffing & Recruiting industry |
    | Competitors Excluded | Gong, Outreach, Salesloft, Apollo, Groove |
    | **Total Matching Prospects** | **3,247** |
    
    Include a brief refinement summary: "Started with 12,400 prospects. Narrowed to 3,247 by adding VP/Director seniority filter, excluding Staffing & Recruiting industry, and focusing on 201-1000 employee companies."
    
9. **Offer to create a lead list** from the final ICP. Ask: "Would you like me to create a lead list from these 3,247 prospects? I can add them to Amplemarket with enrichment enabled so you have emails and phone numbers ready to go."
    
    If the user agrees, call `mcp__claude_ai_Amplemarket__create_lead_list` with:
    
    - `type`: "linkedin"
    - `name`: descriptive name based on the ICP (e.g., "ICP - VP Sales - SaaS - US/UK - Mar 2026")
    - `leads`: array of `{"linkedin_url": "..."}` objects from the search results
    - `options`: `{"enrich": true, "validate_email": true}`
    
    If the total exceeds one page, paginate through all results using `mcp__claude_ai_Amplemarket__search_people` with incrementing `page` values, then use `mcp__claude_ai_Amplemarket__add_leads_to_lead_list` for subsequent batches.
    
    Confirm creation with the user by showing the list ID, total leads added, and enrichment settings enabled. Inform the user about credit usage: "This list of [N] leads will use [N] enrichment credits. The list is now processing. You can check its status anytime."
    

### Important Notes

- Always validate industries and job functions against the API before using them in searches. Never guess enum values.
- Show the user the result count after every search iteration so they can see the impact of each change.
- If the user does not know their best customers or target role, use WebSearch to research their company and suggest an initial hypothesis based on their product category and competitive positioning.
- Keep refinement to 2-3 iterations to avoid fatigue. If the user is satisfied early, move to the final summary.
- When presenting distributions, focus on the most actionable insights. Highlight filters that would have the biggest impact on narrowing or broadening the results.
- Always exclude competitors from results. Use the user's competitor list plus WebSearch to identify companies that sell similar products. If a company in the results looks like it could be a competitor (similar product description, same category on G2/Capterra), flag it and ask the user before including it.

## Dynamic Fields Generated

| Field | Example Value | Source |
| --- | --- | --- |
| `{{icp_title_pattern}}` | VP/Director of Sales | search_people analysis |
| `{{icp_seniority}}` | VP, Director | User input + validation |
| `{{icp_industry}}` | Computer Software, SaaS | get_industries |
| `{{icp_company_size}}` | 201-1000 employees | User input + search validation |
| `{{icp_location}}` | United States, United Kingdom | User input |
| `{{icp_total_addressable}}` | 3,247 | search_people |
| `{{icp_department}}` | Revenue, Marketing | get_job_functions |
| `{{icp_exclusions}}` | Non Profit, Government Agency | User input |
| `{{icp_competitors_excluded}}` | Gong, Outreach, Salesloft, Apollo | User input + WebSearch |
| `{{icp_company_type}}` | Privately Held | User input |
| `{{icp_refinement_summary}}` | Narrowed from 12K to 3.2K by adding seniority filter | Analysis |

## Examples

### Example 1: Full Refinement Workflow

**User prompt:** "Help me define my ICP - I sell sales engagement software but my targeting feels too broad"

**What the skill does:**
1. Asks foundational questions: product, best customers, target role, deal size, exclusions.
2. User responds: "We sell to sales leaders, our best customers are Gong, Outreach, and Salesloft. Average deal is $25K/year. No government or education."
3. Calls `WebSearch` to research the user's company positioning.
4. Calls `mcp__claude_ai_Amplemarket__enrich_company` for gong.io, outreach.io, and salesloft.com.
5. Discovers pattern: all three are 201-1000 employee, privately held, Computer Software / SaaS companies in the US.
6. Calls `mcp__claude_ai_Amplemarket__get_industries` and `mcp__claude_ai_Amplemarket__get_job_functions` to resolve enum values.
7. Runs `mcp__claude_ai_Amplemarket__search_people` with initial hypothesis. Returns 12,400 results.
8. Shows distribution: 38% Managers, 29% Directors, 18% VPs, 15% other. Top industries: Computer Software (41%), Internet (22%), Staffing (14%).
9. User says: "Drop Managers and exclude Staffing." Reruns search. Now 4,812 results.
10. Shows updated distribution. User says: "Focus on 201-1000 employees only." Reruns. Now 3,247 results.
11. Presents final ICP summary and offers to create a lead list.

**Example output:**

---

**Your Refined ICP**

| Criteria | Value |
| --- | --- |
| Target Titles | VP of Sales, Director of Sales, Head of Sales, Director of Revenue Operations |
| Seniority | VP, Director, Head |
| Department | Revenue |
| Industries | Computer Software, Internet, Information Technology and Services |
| Company Size | 201-500 employees, 501-1000 employees |
| Company Type | Privately Held |
| Locations | United States |
| Exclusions | Non Profit, Government Agency, Educational; Staffing & Recruiting industry |
| **Total Matching Prospects** | **3,247** |

**Refinement Journey:**
- Round 1: Initial search with broad criteria returned **12,400** prospects.
- Round 2: Removed Manager-level seniority, excluded Staffing & Recruiting industry. Result: **4,812** prospects.
- Round 3: Narrowed company size to 201-1000 employees. Result: **3,247** prospects.

**Key Insight:** Your best customers (Gong, Outreach, Salesloft) are all mid-market SaaS companies. Focusing on this segment removed 74% of noise from your initial search.

Would you like me to create a lead list from these 3,247 prospects with email enrichment enabled?

---

### Example 2: Starting from a Best Customer Example

**User prompt:** "Acme Corp is our best customer - find me more companies like them"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_company` with domain "acmecorp.com" to extract firmographic attributes.
2. Discovers: 500 employees, Computer Software industry, Privately Held, headquartered in San Francisco.
3. Asks follow-up: "Acme Corp is a 500-person software company in SF. What role at Acme buys from you, and are there geographies or sizes I should exclude?"
4. User responds: "CTO and VP Engineering. US only, 200-1000 employees."
5. Calls `mcp__claude_ai_Amplemarket__get_industries` and `mcp__claude_ai_Amplemarket__get_job_functions` to resolve values.
6. Runs `mcp__claude_ai_Amplemarket__search_people` with mapped criteria. Returns 5,100 results.
7. Shows distribution: titles skew heavily toward Engineering Manager (45%). User narrows to C-Suite and VP only.
8. Reruns. 1,890 results. User approves and requests a lead list.

**Example output:**

I enriched Acme Corp and found the following profile:

| Attribute | Value |
| --- | --- |
| Industry | Computer Software |
| Employees | 500 |
| Type | Privately Held |
| HQ | San Francisco, CA |

Based on this, I searched for CTOs and VPs of Engineering at similar companies. Here is your refined ICP:

| Criteria | Value |
| --- | --- |
| Target Titles | CTO, VP of Engineering, Chief Technology Officer |
| Seniority | C-Suite, VP |
| Department | Engineering & Technical |
| Industries | Computer Software, Information Technology and Services |
| Company Size | 201-500 employees, 501-1000 employees |
| Locations | United States |
| **Total Matching Prospects** | **1,890** |

Would you like me to create a lead list from these 1,890 prospects?

### Example 3: Narrowing an Overly Broad ICP

**User prompt:** "My ICP is too broad - I'm targeting all marketing people at tech companies and getting 50,000+ results"

**What the skill does:**
1. Asks clarifying questions: "What seniority level actually buys? What company size closes fastest? Any geographies that perform better?"
2. User responds: "Directors and above buy. Companies with 100-500 employees close fastest. US and UK are our main markets."
3. Calls `mcp__claude_ai_Amplemarket__get_industries` to resolve "tech companies" to specific industry values.
4. Runs `mcp__claude_ai_Amplemarket__search_people` with narrowed criteria. Returns 9,200 results.
5. Shows distribution: "Marketing" department dominates, but "Director of Demand Gen" and "VP of Growth" are the highest-converting titles based on user feedback.
6. User narrows titles to demand generation and growth roles specifically. Reruns. 2,100 results.
7. Presents final ICP with the path from 50,000+ to 2,100 clearly documented.
8. Offers to create a lead list from the refined set.

**Example output:**

Your original ICP was returning 50,000+ results. Here is how we narrowed it:

**Refinement Journey:**
- Start: All marketing people at tech companies - **50,000+** prospects
- Round 1: Restricted to Director+ seniority, 51-500 employee companies, US and UK only - **9,200** prospects
- Round 2: Focused on demand generation and growth titles specifically - **2,100** prospects

**Your Refined ICP**

| Criteria | Value |
| --- | --- |
| Target Titles | Director of Demand Generation, VP of Growth, Head of Demand Gen, Director of Marketing Operations |
| Seniority | Director, VP, Head |
| Department | Marketing |
| Industries | Computer Software, Internet, Information Technology and Services |
| Company Size | 51-200 employees, 201-500 employees |
| Locations | United States, United Kingdom |
| **Total Matching Prospects** | **2,100** |

That is a 96% reduction from your original search. These 2,100 prospects are much more likely to be actual buyers. Want me to create a lead list?

## Troubleshooting