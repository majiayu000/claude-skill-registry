---
name: market-mapping
description: >
  Search for companies in a target market, find key buyers at each, and produce a segmented market map with the option to create a lead list.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Prospecting & Lead Generation"
compatibility: Requires Amplemarket MCP server
---

# Market Mapping

Search for companies in a target market, find key buyers at each, and produce a segmented market map with the option to create a lead list.

## Instructions

When a user wants to understand a market landscape or map companies and buyers in a segment, execute this multi-step research workflow.

### Steps

1. **Define the market criteria** from the user's request. Extract:
    - **Industry/vertical** (e.g., "fintech", "healthcare SaaS", "cybersecurity")
    - **Geography** (e.g., "US", "Europe", "Bay Area")
    - **Company size** (e.g., "startups", "mid-market", "enterprise")
    - **Company type** (e.g., "privately held", "public")
    - **Segmentation preference** - ask the user how they want the map organized:
        - By company size (small / mid / large)
        - By geography (country or region)
        - By sub-industry or use case
    - **Competitors to exclude** - Ask: "Who are your direct competitors? I'll exclude them and similar companies from the market map so it only shows potential customers, not companies selling similar products."
    
    If criteria are vague, ask: "How would you like me to segment this market - by size, geography, or sub-vertical?"
    
2. **Resolve industry values** by calling `mcp__claude_ai_Amplemarket__get_industries` to match the user's description to valid API values.
3. **Search for companies** by calling `mcp__claude_ai_Amplemarket__search_companies` with:
    - `company_industries`: matched industry values
    - `company_locations`: target geography
    - `company_sizes`: target size ranges
    - `company_types`: if specified
    - `full_output`: true
    - `page_size`: 50 (or as needed for comprehensive coverage)
    
    If the market is large, paginate through results using the `page` parameter to build a complete picture.
    
    **Competitor exclusion:** After retrieving results, remove any companies the user identified as competitors. Additionally, use `WebSearch` to identify other companies in the same product category as the user (e.g., `"[user's product category] companies" OR "[user's company] competitors" OR "[user's company] alternatives"`). Cross-reference the market map results against this competitor list and remove matches. For any company whose description closely resembles the user's product, flag it: "I found [company]. Their description suggests they sell [similar product]. Excluding as a likely competitor." This ensures the market map only contains potential customers, not competitors or lookalike vendors.
    
4. **Segment the results** according to the user's preferred grouping:
    - **By size:** Group into tiers (1-50, 51-500, 501-5000, 5000+)
    - **By geography:** Group by country or region
    - **By sub-industry:** Group by specific industry tags or company descriptions
5. **Estimate TAM sizing** for each segment. Ask the user for their average contract value (ACV). Then calculate:
    - **TAM** = Total companies found × ACV (total addressable opportunity if every company bought)
    - **SAM** = Companies matching the user's ICP filters × ACV (serviceable addressable market)
    - **SOM** = Companies in the user's target segment with high competitive accessibility × ACV (realistically targetable)
    
    If the user does not provide an ACV, ask: "What's your average deal size? I'll use it to estimate the market opportunity for each segment."
    
    Present TAM sizing as a summary table:
    | Segment | Companies | Est. TAM (at $X ACV) | Competitive Density | Priority |
    |------|-------|--------------|--------------|-------|
    
6. **Find key buyers at top companies** by calling `mcp__claude_ai_Amplemarket__search_people` for the most relevant companies in each segment. Use filters:
    - `company_domains`: [company domain]
    - `person_seniorities`: based on company size. Use ["C-Suite", "Founder", "VP"] for small companies, ["VP", "Head", "Director"] for mid-market, ["Director", "Manager"] for enterprise
    - `person_departments`: relevant to the user's product
    - `full_output`: true
    - `page_size`: 5
    
    Limit buyer search to the top 3-5 companies per segment to manage API usage.
    
7. **Compile the market map** with:
    
    **Market Overview**
    
    - Total companies found
    - Distribution across segments
    - Key observations and trends
    - TAM/SAM/SOM estimates (from step 5)
    
    **Segment Detail** (repeat for each segment)
    
    - Segment name and defining criteria
    - Number of companies
    - Table of companies with: Name, Domain, Size, Location, Description
    - Key buyers at representative companies
    
    **White Space Analysis** (structured format)
    For each segment, provide:
    | Segment | Company Count | Competitive Density | Recommended Priority | Reasoning |
    |------|---------|-------------|-------------|-------|
    
    - **Competitive Density** = High (10+ established players with significant funding), Medium (3-9 established players), Low (0-2 established players, whitespace opportunity)
    - **Recommended Priority** = High / Medium / Low based on combination of market size, competitive density, and ICP fit
    
    **Recommended Next Steps**
    
    - Which segments to prioritize and why (with specific reasoning tied to whitespace analysis)
    - Offer to create a lead list from selected segments
8. **Offer to create a lead list** from the market map. If the user wants to proceed, pivot to the build-targeted-lead-list workflow using the discovered prospects.

### Important Notes

- Market mapping can involve many API calls. Start with company search, show the overview, and then offer to drill into specific segments for buyer mapping.
- For very large markets (1000+ companies), recommend narrowing criteria or focusing on specific segments.
- Always present the company search results before making per-company people searches.
- Always exclude competitors and companies selling similar products from the market map. Use the user's competitor list plus WebSearch to build a comprehensive exclusion list. If uncertain whether a company is a competitor or a potential customer, check their company description and ask the user.

## Examples

### Example 1: Industry + Geography Market Map

**User prompt:** "Map the market for cybersecurity companies in the US, segmented by size"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__get_industries` to resolve cybersecurity industry values.
2. Calls `mcp__claude_ai_Amplemarket__search_companies` with:
- `company_industries`: [matched cybersecurity values]
- `company_locations`: ["United States"]
- `full_output`: true
- `page_size`: 50
3. Segments results by size tiers.
4. For top companies in each tier, calls `mcp__claude_ai_Amplemarket__search_people` to find key buyers.

**Example output:**

---

**MARKET MAP: US Cybersecurity Companies**

**Market Overview**
- Total companies found: 284
- Segment distribution: Startup (1-50): 98 | Mid-Market (51-500): 112 | Growth (501-5K): 52 | Enterprise (5K+): 22
- Key trend: Heavy concentration in the 51-500 range, suggesting a maturing market with many companies in growth phase.

**Segment 1: Startups (1-50 employees) - 98 companies**

| Company | Domain | Size | Location | Focus |
| --- | --- | --- | --- | --- |
| SecureAI | secureai.io | 1-10 | San Francisco, CA | AI-powered threat detection |
| VaultNet | vaultnet.com | 11-50 | Austin, TX | Zero-trust network access |
| CipherGuard | cipherguard.co | 11-50 | New York, NY | Encryption-as-a-service |
| ... | ... | ... | ... | ... |

Key buyers at representative companies:
| Company | Contact | Title | LinkedIn |
|------|------|-----|-------|
| SecureAI | Alex Kim | CEO/Founder | linkedin.com/in/alexkim |
| VaultNet | Rachel Torres | CTO | linkedin.com/in/rtorres |
| CipherGuard | David Park | VP Engineering | linkedin.com/in/dpark |

**Segment 2: Mid-Market (51-500 employees) - 112 companies**

| Company | Domain | Size | Location | Focus |
| --- | --- | --- | --- | --- |
| CrowdShield | crowdshield.com | 201-500 | Denver, CO | Endpoint protection |
| NetWatch | netwatch.io | 51-200 | Boston, MA | Network monitoring |
| ... | ... | ... | ... | ... |

*(Key buyers table follows same format)*

**Segment 3: Growth (501-5000 employees) - 52 companies**

*(Same format)*

**Segment 4: Enterprise (5000+ employees) - 22 companies**

*(Same format)*

**White Space Analysis**
- The startup segment (1-50) has the highest count but likely the least buying power. Best for partnership or channel strategies.
- Mid-market (51-500) is the densest and most competitive segment. Expect multiple vendors competing for these accounts.
- Growth segment (501-5K) offers the best balance of buying power and accessibility.
- Enterprise segment is dominated by incumbents (CrowdStrike, Palo Alto, etc.). Requires different go-to-market approach.

**Recommended Next Steps**
- Priority 1: Target Growth segment (501-5K) for highest ROI.
- Priority 2: Mid-Market with differentiated positioning.
- Shall I create a lead list of the key buyers from the Growth segment?

---

### Example 2: Vertical + Sub-Segment Map

**User prompt:** "Show me all healthtech companies in Europe, grouped by sub-vertical"

**What the skill does:**
1. Resolves healthtech industry values.
2. Searches companies across European locations.
3. Groups by sub-vertical based on company descriptions (telemedicine, health data, biotech platforms, digital therapeutics, etc.).
4. Maps key buyers per sub-vertical.

### Example 3: Competitive Landscape Map

**User prompt:** "What does the landscape look like for marketing automation companies with 200-1000 employees?"

**What the skill does:**
1. Resolves marketing technology / marketing automation industry values.
2. Searches with `company_sizes`: ["201-500 employees", "501-1000 employees"].
3. Segments by geography or product focus.
4. Maps CXO and VP-level contacts at each company.
5. Highlights which companies are direct competitors vs. adjacent players.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Too many companies returned | Add filters for company size, type, or narrow the geography. Offer to focus on a specific sub-segment. |
| Too few companies (<5 results) | Broaden industry filter by one level and retry. If still <5 results, remove the geography filter and search globally. If still <5, try related industry values from `get_industries` and present alternatives to the user. |
| No buyers found at a company | Try broadening seniority to include "Manager" and "Senior". If still no results, try searching by company name instead of domain. For companies with <50 employees, suggest the user look up founders directly via `enrich_person` with name + company. |
| User wants to drill into one segment | Run a focused `mcp__claude_ai_Amplemarket__search_companies` with tighter criteria for that segment and do deeper buyer mapping. |
| Market map is too large to display | Summarize with counts and top companies per segment. Offer to export or create lead lists per segment. |
| `search_companies` returns 0 for a known market | Step 1: Try broader or related industry values by calling `get_industries` and presenting the closest 3-5 options. Step 2: Try searching by company domain if you know specific players. Step 3: Try removing all filters except geography and re-adding one at a time to identify which filter is too restrictive. |
| No buyers found at mapped companies | Focus buyer mapping on companies with 50+ employees. For smaller companies, use `enrich_person` with founder names + company domain as a fallback. If `search_people` returns 0 for a company that exists, try searching by company name instead of domain. |