---
name: daily-web-signal-prospector
description: >
  Search the web for buying signals relevant to your ICP within a user-defined timeframe, then find and enrich decision-makers at signal-matching companies.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Prospecting & Lead Generation"
compatibility: Requires Amplemarket MCP server
---

# Daily Web Signal Prospector

Search the web for buying signals relevant to your ICP within a user-defined timeframe, then find and enrich decision-makers at signal-matching companies.

## Instructions

When a user wants to find companies exhibiting buying signals and connect them to actionable prospects, execute this multi-step research and enrichment workflow.

### Steps

1. **Gather signal preferences from the user.** Ask three questions before executing:
    
    **(a) "What buying signals matter most?"** Present the following list and let the user select one or more:
    
    1. Funding rounds (Series A, B, C, etc.)
    2. Executive hires (new C-suite, VP, or Director appointments)
    3. Layoffs or restructuring
    4. Product launches or major feature releases
    5. Expansion or new office openings
    6. Earnings reports or revenue milestones
    7. Strategic partnerships or integrations
    8. Acquisitions or mergers
    9. Tech stack changes or new technology adoption
    
    **(b) "What timeframe should I search?"** Offer options:
    
    - Last 7 days (most recent, fewer results)
    - Last 30 days (balanced coverage)
    - Last 90 days (broadest coverage, more noise)
    
    **(c) "What's your ICP?"** Ask for:
    
    - Target titles (e.g., VP of Sales, CTO, Head of Marketing)
    - Target industries (e.g., fintech, healthcare, SaaS)
    - Company size preferences (e.g., 51-500 employees, 501-5000 employees)
2. **Construct signal-specific WebSearch queries.** For each selected signal type, build targeted search queries using the following patterns:
    - **Funding rounds:**`"raised" OR "funding round" OR "Series" site:techcrunch.com OR site:crunchbase.com`
    Add industry keywords from the user's ICP to narrow results.
    - **Executive hires:**`"appointed" OR "named" OR "joins as" [title] [industry]`
    Target specific C-suite or VP-level titles relevant to the user's outreach.
    - **Layoffs or restructuring:**`"layoffs" OR "restructuring" OR "workforce reduction" [industry]`
    Focus on companies that may be re-evaluating vendors or consolidating tools.
    - **Product launches:**`"launches" OR "announces" OR "introduces" [product type] [industry]`
    Target companies investing in growth and innovation.
    - **Expansion or new offices:**`"opens office" OR "expands to" OR "new headquarters" OR "expands operations" [industry]`
    Companies expanding geographically often need new tools and services.
    - **Earnings reports:**`"revenue" OR "earnings" OR "quarterly results" OR "annual report" [industry]`
    Focus on companies reporting growth or strategic pivots.
    - **Partnerships:**`"partners with" OR "integrates with" OR "strategic partnership" OR "collaboration" [industry]`
    Companies forming partnerships may be expanding their ecosystem.
    - **Acquisitions:**`"acquires" OR "acquisition" OR "merger" OR "acquired by" [industry]`
    M&A activity often triggers new vendor evaluations.
    - **Tech stack changes:**`"migrates to" OR "adopts" OR "implements" OR "switches to" [technology] [industry]`
    Companies changing tools are actively evaluating alternatives.
    
    Append timeframe qualifiers (e.g., current month/year) to each query to filter for recency.
    
3. **Run WebSearch for each signal type.** Call `WebSearch` with each constructed query. Run searches in parallel where possible to reduce execution time. Aim for 3-5 search queries per signal type to ensure broad coverage.
4. **Fetch and extract signal details.** Use `WebFetch` on the top 5-10 results per signal type to extract:
    - Company name
    - Signal details (e.g., funding amount, new hire name and title, product launched)
    - Date of the event
    - Source URL
    - Any additional context (investors, partners, geographic details)
    
    Deduplicate companies that appear across multiple signal types.
    
5. **Enrich each company found.** For each unique company, call `mcp__claude_ai_Amplemarket__enrich_company` with the company `domain` to retrieve:
    - Industry and sub-industry
    - Company size (employee count)
    - Company type (public, private, startup)
    - Headquarters location
    - Description and value proposition
    - Tech stack (if available)
6. **Filter companies against the user's ICP.** Compare enriched firmographic data against the user's stated ICP criteria:
    - Does the company's industry match the target industries?
    - Does the company size fall within the desired range?
    - Does the location align with geographic preferences?
    
    Remove companies that do not match. Flag borderline matches for the user to review.
    
7. **Find decision-makers at matching companies.** For each ICP-matching company, call `mcp__claude_ai_Amplemarket__search_people` with:
    - `company_domains`: [company domain]
    - `person_titles`: based on the user's target titles
    - `person_seniorities`: ["C-Suite", "VP", "Head", "Director"] (adjust based on ICP)
    - `full_output`: true
    - `page_size`: 5
    
    Extract name, title, LinkedIn URL, and email (if available) for each decision-maker.
    
8. **Present signal-enriched results.** Group findings by signal type and present in a structured format:
    
    **Signal Type: [e.g., Funding Rounds]**
    
    | Company | Signal Detail | Date | Industry | Size | Decision Maker | Title | Suggested Opener |
    | --- | --- | --- | --- | --- | --- | --- | --- |
    | Acme Corp | Raised $50M Series C | 2026-03-02 | SaaS | 201-500 | Jane Smith | VP Sales | "Congrats on the Series C. Scaling the sales org after a raise like that usually means..." |
    
    For each result, generate the following dynamic fields:
    
    - `{{signal_type}}`: The category of buying signal detected
    - `{{signal_date}}`: When the signal event occurred
    - `{{signal_detail}}`: Specific details of the signal (amount raised, person hired, product launched)
    - `{{signal_source_url}}`: URL of the original source article
    - `{{signal_company_name}}`: Company name from enrichment
    - `{{signal_company_industry}}`: Industry from enrichment
    - `{{signal_company_size}}`: Employee count range from enrichment
    - `{{signal_relevance}}`: ICP match score (Strong / Medium / Weak)
    - `{{signal_suggested_opener}}`: A personalized opening line referencing the signal
    - `{{signal_decision_maker}}`: Name of the identified decision-maker
    - `{{signal_decision_maker_title}}`: Title of the identified decision-maker
    
    Include a summary at the top:
    
    - Total signals found
    - Companies matching ICP
    - Decision-makers identified
    - Breakdown by signal type
9. **Offer to create a lead list with signal context.** Ask the user if they want to save the results as an Amplemarket lead list. If yes, call `mcp__claude_ai_Amplemarket__create_lead_list` with:
    - `type`: "linkedin" (using decision-maker LinkedIn URLs)
    - `name`: descriptive name (e.g., "Funding Signals - SaaS - Mar 2026")
    - `leads`: array of lead objects with `linkedin_url` for each decision-maker
    - `context`: include signal type, signal detail, and suggested opener for each lead
    - `options`: ask about enrichment preferences (`enrich`, `validate_email`, `reveal_phone_numbers`)
    
    Inform the user of credit implications before proceeding.
    

### Important Notes

- WebSearch and WebFetch results depend on publicly available information. Not all signals will be captured, especially for private companies that do not announce events publicly.
- Each `enrich_company` and `search_people` call consumes Amplemarket credits. For large signal sweeps (20+ companies), warn the user about credit usage before proceeding with enrichment.
- Timeframe filtering relies on search engine recency. Results from the "last 7 days" option will be most accurate; "last 90 days" may surface some older content.
- Signal quality varies by type. Funding rounds and acquisitions tend to produce the most reliable data. Tech stack changes and restructuring signals may require manual verification.
- Always deduplicate companies across signal types before enriching. A single company may appear in multiple signal categories (e.g., a company that raised funding and hired a new CTO).

## Dynamic Fields Generated

The following dynamic fields are populated for each signal-matched prospect and can be used in outreach templates:

| Field | Description | Example Value |
| --- | --- | --- |
| `{{signal_type}}` | Category of buying signal detected | "Funding Round" |
| `{{signal_date}}` | Date the signal event occurred | "2026-03-02" |
| `{{signal_detail}}` | Specific details of the signal event | "Raised $50M Series C led by Sequoia" |
| `{{signal_source_url}}` | URL of the source article or announcement | "https://techcrunch.com/2026/03/02/acme-series-c" |
| `{{signal_company_name}}` | Enriched company name | "Acme Corp" |
| `{{signal_company_industry}}` | Industry from company enrichment | "Computer Software / SaaS" |
| `{{signal_company_size}}` | Employee count range | "201-500 employees" |
| `{{signal_relevance}}` | ICP match strength | "Strong" |
| `{{signal_suggested_opener}}` | Personalized opener referencing the signal | "Congrats on the Series C. When teams scale post-raise..." |
| `{{signal_decision_maker}}` | Name of the identified decision-maker | "Jane Smith" |
| `{{signal_decision_maker_title}}` | Title of the decision-maker | "VP of Sales" |
| `{{signal_decision_maker_linkedin}}` | LinkedIn URL of the decision-maker | "linkedin.com/in/janesmith" |

## Examples

### Example 1: Funding Signals in Last 7 Days

**User prompt:** "Find companies that just raised funding in the last week. I sell to VP Sales at SaaS companies with 100-1000 employees"

**What the skill does:**
1. Sets signal type to "Funding rounds", timeframe to "last 7 days", ICP to VP Sales / SaaS / 100-1000 employees.
2. Calls `WebSearch` with queries like `"raised" OR "funding round" OR "Series" site:techcrunch.com 2026` and `"series A" OR "series B" OR "series C" SaaS 2026`.
3. Calls `WebFetch` on top results to extract company names, funding amounts, investors, and dates.
4. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each company found (e.g., domain: "acmesaas.com").
5. Filters to SaaS companies with 100-1000 employees.
6. Calls `mcp__claude_ai_Amplemarket__search_people` with `company_domains`: ["acmesaas.com"], `person_titles`: ["VP of Sales", "Vice President of Sales"], `person_seniorities`: ["VP"], `full_output`: true.
7. Presents results grouped under "Funding Rounds".

**Example output:**

---

**WEB SIGNAL REPORT: Funding Rounds (Last 7 Days)**

Summary: 14 signals found | 8 companies match ICP | 12 decision-makers identified

**Funding Rounds**

| Company | Signal Detail | Date | Industry | Size | Decision Maker | Title | Suggested Opener |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Acme SaaS | Raised $50M Series C led by Sequoia | 2026-03-05 | SaaS / Sales Enablement | 201-500 | Jane Smith | VP of Sales | "Congrats on the Series C. Scaling revenue post-raise usually means rethinking the sales stack. Curious if that's on your radar." |
| CloudSync | Raised $25M Series B led by a16z | 2026-03-03 | SaaS / Data Integration | 101-250 | Marcus Johnson | VP of Sales | "Saw CloudSync just closed your Series B. When teams grow fast after a raise, pipeline generation usually becomes the bottleneck." |
| DataPipe | Raised $15M Series A led by Greylock | 2026-03-07 | SaaS / Analytics | 51-200 | Sarah Lee | Head of Sales | "Series A is an exciting milestone, typically the point where founders start building out a repeatable sales engine." |

---

Shall I create a lead list with these prospects? Enrichment and email validation would use credits for each lead.

---

### Example 2: Hiring Signals for Specific ICP

**User prompt:** "Find trigger events for my ICP. Companies hiring new CTOs or VPs of Engineering. I sell developer tools to mid-market companies."

**What the skill does:**
1. Sets signal type to "Executive hires", ICP to CTO/VP Eng buyers at mid-market developer tools companies.
2. Calls `WebSearch` with queries like `"appointed CTO" OR "named CTO" OR "new CTO" OR "joins as CTO" technology 2026` and `"VP of Engineering" OR "Vice President of Engineering" "joins" OR "appointed" 2026`.
3. Fetches and extracts details: who was hired, their background, the company.
4. Enriches each company and filters to mid-market (201-5000 employees).
5. Since the signal itself identifies the decision-maker, uses `mcp__claude_ai_Amplemarket__search_people` to find their profile and additional contacts.
6. Presents results under "Executive Hires" with openers referencing the new role.

**Example output (abbreviated):**

---

**WEB SIGNAL REPORT: Executive Hires**

| Company | Signal Detail | Date | Size | Decision Maker | Suggested Opener |
| --- | --- | --- | --- | --- | --- |
| NovaTech | Appointed Maria Garcia as CTO (prev. Staff Eng at Google) | 2026-03-01 | 501-1000 | Maria Garcia, CTO | "Congrats on the CTO appointment. New technical leaders often reassess the dev toolchain in their first 90 days." |
| BuildKit | Named Raj Patel as VP Engineering | 2026-02-28 | 201-500 | Raj Patel, VP Eng | "Saw you recently joined BuildKit. Curious what's top of mind as you shape the engineering org." |

---

### Example 3: Multiple Signal Types Combined

**User prompt:** "Search for buying signals (funding, new hires, and expansion) in the fintech space over the last 30 days. My targets are Directors and VPs at companies with 200-2000 employees."

**What the skill does:**
1. Sets signal types to "Funding rounds", "Executive hires", "Expansion/new offices". Timeframe: last 30 days. ICP: Directors/VPs at fintech companies, 200-2000 employees.
2. Runs parallel `WebSearch` queries for all three signal types with fintech keywords.
3. Fetches top results, extracts signal details, and deduplicates companies across types.
4. Enriches all unique companies via `mcp__claude_ai_Amplemarket__enrich_company`.
5. Filters to fintech companies with 200-2000 employees.
6. Finds decision-makers at matching companies via `mcp__claude_ai_Amplemarket__search_people`.
7. Presents results grouped by signal type, with a combined summary.

**Example output (abbreviated):**

---

**WEB SIGNAL REPORT: Multi-Signal Sweep - Fintech (Last 30 Days)**

Summary: 38 signals found across 3 types | 22 companies match ICP | 31 decision-makers identified

**Funding Rounds (12 signals)**

| Company | Signal Detail | Date | Decision Maker | Title |
| --- | --- | --- | --- | --- |
| PayFlow | Raised $80M Series D | 2026-02-20 | Tom Rivera | VP of Product |
| LendTech | Raised $30M Series B | 2026-02-15 | Amy Chen | Director of Engineering |

**Executive Hires (16 signals)**

| Company | Signal Detail | Date | Decision Maker | Title |
| --- | --- | --- | --- | --- |
| FinServe | Hired new VP of Sales from Stripe | 2026-03-01 | David Kim | VP of Sales |
| CryptoBase | Named new CTO | 2026-02-22 | Lisa Park | CTO |

**Expansion / New Offices (10 signals)**

| Company | Signal Detail | Date | Decision Maker | Title |
| --- | --- | --- | --- | --- |
| NeoBank | Opened London office | 2026-02-18 | James Wright | Director of Operations |
| PayFlow | Expanding to APAC | 2026-03-04 | Tom Rivera | VP of Product |

Note: PayFlow appears in both Funding and Expansion, a strong buying signal (double trigger).

---

Shall I create a lead list from all 31 decision-makers, or would you like to focus on a specific signal type?

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| WebSearch returns no results for a signal type | Broaden the query: 1) Remove `site:` restrictions to search across all sources. 2) Extend the timeframe to 30 or 90 days. 3) Use more general keywords (e.g., "funding" instead of "Series B"). 4) Try alternative search terms for the same signal. |
| WebFetch fails to load a page | Skip the failed URL and move to the next result. Some sites block automated fetching. Note which sources were inaccessible and suggest the user check them manually. |
| Too many companies found (50+) | Apply stricter ICP filters before enrichment. Ask the user: "I found [N] companies. Want me to narrow by industry, size, or geography before enriching?" This avoids unnecessary credit usage. |
| Company enrichment returns no data | Fallback chain: 1) Try alternate domains (e.g., company.io vs company.com). 2) Try the LinkedIn company URL. 3) If enrichment fails entirely, include the company in results with web-sourced data only and flag: "Enrichment unavailable. Signal data from web sources only." |
| No decision-makers found at a matching company | Fallback chain: 1) Broaden seniority to include "Manager" and "Senior". 2) Try searching by company name instead of domain. 3) For companies with fewer than 50 employees, search for "Founder" and "C-Suite" only. 4) Note the gap: "No contacts found. Company may be too small or too new for people data." |
| Signal data appears outdated despite recent timeframe | Web search results may include older content that was recently re-indexed. Verify dates by checking the source article directly via WebFetch. Discard signals with confirmed dates outside the requested timeframe. |
| Duplicate companies across signal types | This is expected and valuable. Companies with multiple signals represent stronger buying opportunities. Deduplicate before enrichment but preserve all signal types in the final output. Flag multi-signal companies: "Double trigger: [Company] appears in both [Signal A] and [Signal B]." |
| User wants to monitor signals regularly | This skill runs on demand. Suggest the user run it weekly or daily with the "last 7 days" timeframe for ongoing monitoring. Recommend saving each run's results as a dated lead list for tracking over time. |