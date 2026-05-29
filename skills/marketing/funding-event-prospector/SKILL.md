---
name: funding-event-prospector
description: >
  Find companies that recently raised funding and identify decision-makers for timely, signal-based outreach.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Signal Monitoring"
compatibility: Requires Amplemarket MCP server
---

# Funding Event Prospector

Find companies that recently raised funding and identify decision-makers for timely, signal-based outreach.

## Instructions

When a user wants to prospect into companies that have recently raised funding, execute this multi-step research and enrichment workflow.

### Steps

1. **Gather targeting criteria** from the user. Ask these five questions:
    - **Funding stages:** Which rounds are you targeting? (Seed, Series A, Series B, Series C, Series D+, Growth Equity, etc.)
    - **Amount range:** What funding amount range are you interested in? (e.g., $5M-$20M, $50M+, any)
    - **Timeframe:** How recent should the funding be? (e.g., last 7 days, last 30 days, last 90 days)
    - **Industry/geography filters:** Any specific industries or geographies? (e.g., fintech in the US, healthtech in Europe)
    - **Target roles:** Which roles do you want to reach at these companies? (e.g., VP of Engineering, CTO, Head of Sales)
    
    If the user provides a broad request, infer reasonable defaults and confirm: "I'll search for Series A-C rounds in the last 30 days across all industries. Want me to narrow this down?"
    
2. **Construct WebSearch queries** targeting funding news sources. Run multiple searches to maximize coverage:
    - `"Series [A/B/C]" "raised" [timeframe] site:techcrunch.com`
    - `"funding round" "[amount range]" [industry] site:crunchbase.com`
    - `"raised" "million" [industry] [geography] [timeframe]`
    
    Vary the queries based on user criteria. For example, if the user wants Series B in fintech:
    
    - `"Series B" "raised" "fintech" site:techcrunch.com 2026`
    - `"Series B" "funding" "fintech" site:crunchbase.com`
    - `"raised" "Series B" "million" "fintech" 2026`
    
    Run 3-5 searches to ensure broad coverage across sources.
    
3. **WebFetch top results** to extract structured funding details from each article. For each result, capture:
    - **Company name** and domain
    - **Funding amount** (exact figure)
    - **Round type** (Seed, Series A, B, C, etc.)
    - **Lead investor** and participating investors
    - **Stated use of funds** (hiring, expansion, product development, etc.)
    - **Date** of the funding announcement
    - **Source URL** for reference
    
    Prioritize the 10-15 most relevant results. Skip duplicates where the same company appears in multiple articles.
    
4. **Enrich each funded company** by calling `mcp__claude_ai_Amplemarket__enrich_company` with the company `domain` extracted from the funding articles. Key data points to capture:
    - Industry and sub-industry
    - Employee count and growth trajectory
    - Headquarters location
    - Company description and value proposition
    - Tech stack (if available)
    
    If the domain is unclear from the article, search for it using the company name + "website" via WebSearch.
    
5. **Filter against user's ICP criteria.** Compare enriched company data against the user's requirements:
    - Does the industry match their target vertical?
    - Is the company size in their sweet spot?
    - Is the geography aligned?
    - Does the funding stage and amount match their criteria?
    
    Remove companies that do not fit and note why they were excluded. Present the filtered list to the user before proceeding.
    
6. **Search for decision-makers** at each matching company by calling `mcp__claude_ai_Amplemarket__search_people` with:
    - `company_domains`: [company domain]
    - `person_titles`: based on user's target roles
    - `person_seniorities`: mapped from target roles (e.g., ["VP", "Head", "Director", "C-Suite"])
    - `full_output`: true
    - `page_size`: 10
    
    Focus on roles most likely to be involved in post-funding initiatives (hiring, procurement, expansion).
    
7. **Enrich top prospects** by calling `mcp__claude_ai_Amplemarket__enrich_person` for the highest-priority contacts at each company. Set `reveal_email` to `true` for contact details. **Credit note:** Each person enrichment with email and phone reveal consumes Amplemarket credits. Warn the user before enriching: "I found [N] prospects across [M] companies. Enriching all of them will use [N] credits. Want me to proceed with all, or select the top prospects?"
8. **Present results grouped by funding recency.** Organize the output into three tiers:
    - **This week:** Companies that raised in the last 7 days (hottest signal)
    - **This month:** Companies that raised in the last 8-30 days
    - **Recent:** Companies that raised in the last 31-90 days
    
    For each company, display:
    
    - Funding details (round, amount, lead investor, use of funds)
    - Company firmographics (industry, size, location)
    - Decision-makers found (name, title, email if enriched)
    - Suggested opener referencing the funding event
    
    Include dynamic fields (see Dynamic Fields Generated below) that can be used in outreach templates.
    
9. **Offer lead list creation with funding context.** Ask: "Would you like me to create a lead list from these prospects? I can name it something like '[Funding Stage] - [Industry] - [Month Year]'." If the user agrees, pivot to creating a lead list via `mcp__claude_ai_Amplemarket__create_lead_list` using the discovered prospects' LinkedIn URLs.

### Important Notes

- Funding news decays quickly in relevance. Prioritize the most recent announcements and flag anything older than 60 days as potentially stale for outreach timing.
- WebSearch results may include false positives (e.g., articles mentioning funding in passing). Always verify by WebFetching the article to confirm an actual funding round.
- Some companies may not be found in Amplemarket enrichment, especially very early-stage startups. Note these gaps and provide what data is available from the funding article itself.
- Credit costs can add up when enriching many prospects. Always warn the user about the number of enrichments before proceeding and offer to prioritize a subset.
- Funding amounts reported in the press may differ from official filings. Treat all amounts as approximate and flag any discrepancies found during enrichment.

## Dynamic Fields Generated

The following dynamic fields are produced for each funded company and can be used in outreach templates:

| Field | Description | Example Value |
| --- | --- | --- |
| `{{funding_round}}` | Type of funding round | "Series B" |
| `{{funding_amount}}` | Amount raised in the round | "$45M" |
| `{{funding_date}}` | Date of the funding announcement | "2026-02-28" |
| `{{funding_lead_investor}}` | Lead investor in the round | "Andreessen Horowitz" |
| `{{funding_all_investors}}` | All participating investors | "a16z, Sequoia Capital, Tiger Global" |
| `{{funding_use_of_funds}}` | Stated use of the new capital | "Expanding engineering team and entering European markets" |
| `{{funding_company_name}}` | Company name | "CloudMetrics" |
| `{{funding_company_domain}}` | Company website domain | "cloudmetrics.io" |
| `{{funding_company_size}}` | Employee count range | "201-500 employees" |
| `{{funding_company_industry}}` | Company industry vertical | "Cloud Computing / SaaS" |
| `{{funding_growth_signal}}` | Inferred growth signal from the funding | "Hiring 50+ engineers, opening London office" |
| `{{funding_source_url}}` | URL of the funding announcement article | "https://techcrunch.com/2026/02/28/cloudmetrics-series-b" |
| `{{funding_suggested_opener}}` | Ready-to-use opening line referencing the funding event | "Congrats on CloudMetrics' $45M Series B. With plans to scale the engineering team, I imagine tooling decisions are top of mind right now." |

## Examples

### Example 1: Series B Funding in Fintech, Last 30 Days

**User prompt:** "Find companies that raised a Series B in fintech in the last 30 days. I want to reach VPs of Engineering."

**What the skill does:**
1. Runs WebSearch queries:
- `"Series B" "raised" "fintech" site:techcrunch.com 2026`
- `"Series B" "funding" "fintech" site:crunchbase.com 2026`
- `"raised" "Series B" "million" "fintech" February 2026`
2. WebFetches top 10 articles to extract funding details.
3. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each company found.
4. Filters to confirmed fintech companies.
5. Calls `mcp__claude_ai_Amplemarket__search_people` at each company with `person_titles`: ["VP of Engineering", "Vice President of Engineering"], `person_seniorities`: ["VP"].
6. Enriches top prospects with email reveal.

**Example output:**

---

**FUNDING EVENT PROSPECTS: Series B Fintech - Last 30 Days**

**This Week (3 companies)**

**1. PayFlow** - $38M Series B (March 5, 2026)
| Field | Detail |
|-----|-----|
| Domain | payflow.io |
| Industry | Fintech / Payments |
| Size | 120 employees |
| Lead Investor | Accel |
| Use of Funds | Scaling engineering team, launching in LATAM |
| Source | techcrunch.com/2026/03/05/payflow-series-b |

Decision Makers Found:
| Name | Title | Email | LinkedIn |
|----|-----|-----|-------|
| James Liu | VP of Engineering | j.liu@payflow.io | linkedin.com/in/jamesliu |
| Nina Patel | Head of Platform Engineering | n.patel@payflow.io | linkedin.com/in/ninapatel |

`{{funding_suggested_opener}}`: "James, congrats on PayFlow's $38M Series B. With plans to scale engineering and launch in LATAM, I imagine you are making some key infrastructure decisions right now."

**2. LendStack** - $52M Series B (March 3, 2026)
| Field | Detail |
|-----|-----|
| Domain | lendstack.com |
| Industry | Fintech / Lending |
| Size | 200 employees |
| Lead Investor | Sequoia Capital |
| Use of Funds | Product expansion, doubling engineering headcount |
| Source | crunchbase.com/funding_round/lendstack-series-b |

Decision Makers Found:
| Name | Title | Email | LinkedIn |
|----|-----|-----|-------|
| Sarah Kim | VP of Engineering | sarah.k@lendstack.com | linkedin.com/in/sarahkim-eng |

`{{funding_suggested_opener}}`: "Sarah, saw LendStack just closed a $52M Series B led by Sequoia. Doubling the engineering team is a big undertaking, and getting the right tooling in place early can save months of rework."

**This Month (5 companies)**

*(Same format continues for companies that raised 8-30 days ago)*

**Summary**
- Total funded companies found: 8
- Matching ICP after filtering: 6
- Total decision-makers identified: 14
- Enriched with contact details: 8

Would you like me to create a lead list from these 14 prospects? I'd suggest naming it "Series B - Fintech - Mar 2026".

---

### Example 2: Seed/Series A in Healthtech, US West Coast

**User prompt:** "Who just raised Seed or Series A in healthtech on the US West Coast? I want to reach founders and CTOs."

**What the skill does:**
1. Runs WebSearch queries:
- `"Seed" OR "Series A" "raised" "healthtech" OR "health tech" OR "digital health" site:techcrunch.com 2026`
- `"Seed round" OR "Series A" "healthcare" "California" OR "Oregon" OR "Washington" site:crunchbase.com`
- `"raised" "million" "digital health" "San Francisco" OR "Los Angeles" OR "Seattle" OR "Portland" 2026`
2. WebFetches top articles to extract company names, amounts, investors, and use of funds.
3. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each company found.
4. Filters to companies in healthtech-related industries located in California, Oregon, or Washington.
5. Calls `mcp__claude_ai_Amplemarket__search_people` with `person_seniorities`: ["Founder", "C-Suite"], `person_titles`: ["Founder", "Co-Founder", "CTO", "Chief Technology Officer"], `company_domains`: [each matching company domain].
6. Enriches top founder and CTO contacts with email reveal.
7. Presents results grouped by recency, distinguishing Seed from Series A rounds.

**Example output (abbreviated):**

---

**FUNDING EVENT PROSPECTS: Seed/Series A Healthtech - US West Coast**

**This Week (2 companies)**

**1. MedSync** - $8M Seed (March 6, 2026)
| Field | Detail |
|-----|-----|
| Domain | medsync.health |
| Industry | Digital Health / Telemedicine |
| Size | 15 employees |
| Lead Investor | Khosla Ventures |
| Use of Funds | Building initial product team, FDA pathway |
| Source | techcrunch.com/2026/03/06/medsync-seed |

Decision Makers Found:
| Name | Title | Email | LinkedIn |
|----|-----|-----|-------|
| Dr. Anika Rao | Co-Founder & CEO | a.rao@medsync.health | linkedin.com/in/anikarao |
| Marcus Chen | Co-Founder & CTO | m.chen@medsync.health | linkedin.com/in/marcuschen |

`{{funding_suggested_opener}}`: "Anika, congrats on MedSync's $8M Seed led by Khosla. Navigating the FDA pathway while building a product team is no small feat. Would love to share how we help early-stage health tech teams move faster."

---

### Example 3: Large Rounds ($50M+) Across All Industries

**User prompt:** "Find companies that raised $50 million or more in the last 60 days. Any industry. Target Heads of Sales and CROs."

**What the skill does:**
1. Runs broad WebSearch queries:
- `"raised" "$50 million" OR "$60 million" OR "$75 million" OR "$100 million" 2026 site:techcrunch.com`
- `"funding" "50M" OR "75M" OR "100M" site:crunchbase.com 2026`
- `"raised" "million" "Series" 2026` (then filters to $50M+ during extraction)
2. WebFetches results, filtering to rounds of $50M or more during data extraction.
3. Calls `mcp__claude_ai_Amplemarket__enrich_company` for all companies regardless of industry.
4. Calls `mcp__claude_ai_Amplemarket__search_people` with `person_titles`: ["Head of Sales", "CRO", "Chief Revenue Officer", "VP of Sales"], `person_seniorities`: ["Head", "C-Suite", "VP"], `company_domains`: [each company domain].
5. Presents a cross-industry view highlighting the largest rounds first, with industry tags for easy scanning.
6. Offers to segment the lead list by industry or round size.

**Example output (abbreviated):**

---

**FUNDING EVENT PROSPECTS: $50M+ Rounds - All Industries - Last 60 Days**

Found 12 companies that raised $50M or more. Showing top results by round size:

| Company | Round | Amount | Industry | Lead Investor | Date |
| --- | --- | --- | --- | --- | --- |
| DataForge | Series C | $120M | Cloud Infrastructure | Tiger Global | Mar 2, 2026 |
| ClimateTech Co | Series B | $85M | Clean Energy | Breakthrough Energy | Feb 25, 2026 |
| SecureNet | Series C | $72M | Cybersecurity | Insight Partners | Feb 18, 2026 |
| ShipFast | Series B | $55M | Logistics / Supply Chain | a16z | Feb 10, 2026 |

Total CROs/Heads of Sales found: 22
Enriched with contact details: 12

Would you like me to create a lead list? I can segment by industry or create one unified list named "$50M+ Rounds - Q1 2026".

## Troubleshooting

| Problem | Solution |
| --- | --- |
| WebSearch returns few or no funding articles | Broaden the search: 1) Remove the `site:` restriction to search across all sources. 2) Extend the timeframe (e.g., 30 days to 90 days). 3) Use broader terms like "raised" or "funding" instead of specific round names. 4) Try alternative sources like Bloomberg, Reuters, or industry-specific publications. |
| Company domain cannot be determined from the article | Fallback chain: 1) WebSearch for "[company name] website" to find the domain. 2) Try common domain patterns (companyname.com, companyname.io). 3) Search for the company on LinkedIn and use the LinkedIn URL for enrichment. 4) If still not found, note the company with available data and skip enrichment. |
| `enrich_company` returns no data for a funded company | This is common for very early-stage startups not yet indexed. Use the data extracted from the funding article (company name, funding details, investors) and flag: "Company not found in Amplemarket. Details sourced from funding announcement only." |
| No decision-makers found at a funded company | Fallback chain: 1) Broaden seniority to include "Manager" and "Senior". 2) Try searching by company name instead of domain. 3) For companies with fewer than 50 employees, search for "Founder" and "C-Suite" only. 4) Check the funding article for named executives and try `enrich_person` with name + company. |
| Duplicate companies across search results | Deduplicate by company domain before enriching. If two articles reference the same company's round, merge the details and keep the most recent or most detailed article as the source URL. |
| Funding article is about a company update, not an actual round | Verify each article by checking for specific funding indicators: round type, dollar amount, investor names, and funding date. Discard articles that mention funding only in passing or reference historical rounds. |
| Too many results consuming excessive credits | Prioritize by: 1) Recency (most recent funding first). 2) ICP fit (filter companies before enriching people). 3) Offer tiered enrichment: "I found 40 prospects. Want me to enrich the top 10 first, then continue if the quality looks good?" |