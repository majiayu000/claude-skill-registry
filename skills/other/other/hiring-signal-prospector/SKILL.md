---
name: hiring-signal-prospector
description: >
  Find companies hiring for roles that signal product need, then enrich and identify decision-makers to target.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Signal Monitoring"
compatibility: Requires Amplemarket MCP server
---

# Hiring Signal Prospector

Find companies hiring for roles that signal product need, then enrich and identify decision-makers to target.

## Instructions

When a user wants to find companies whose job postings indicate buying intent for their product, execute this hiring-signal research workflow.

### Steps

1. **Gather signal criteria** from the user. Ask:
    - **Signal roles:** What job titles or roles should we look for? (e.g., "SDR", "Data Engineer", "RevOps Manager")
    - **Why it's a signal:** Why does hiring for this role indicate they need your product? (e.g., "Building an outbound team means they need sales engagement tools")
    - **Geography and company size:** Any location or size filters? (e.g., "US-based, 50-500 employees")
    - **Decision-maker roles:** Who should we target once we find these companies? (e.g., "VP of Sales", "CRO", "Head of Revenue Operations")
    - **Timeframe:** How recent should the job postings be? (e.g., "Last 30 days", "Currently open")
    
    If the user provides partial criteria, infer reasonable defaults and confirm before proceeding.
    
2. **Construct WebSearch queries** to find job postings across multiple sources. Run several searches using `WebSearch`:
    - `"[signal role]" hiring OR "open position" OR "we're looking for" [geography]`
    - `site:linkedin.com/jobs "[signal role]" [industry]`
    - `site:greenhouse.io OR site:lever.co "[signal role]"`
    - `"[signal role]" "job description" [company size indicator]`
    
    Vary the queries to maximize coverage across job boards (LinkedIn Jobs, Indeed, Greenhouse, Lever, Ashby, Workable). Run at least 3-4 different query variations to ensure broad coverage.
    
3. **Fetch and extract job details** by calling `WebFetch` on the top 10-15 results. For each job posting, extract:
    - Company name and domain
    - Exact job title
    - Key responsibilities and requirements
    - Tools and technologies mentioned
    - Team size or reporting structure clues
    - Posting date and location
    
    Deduplicate companies that appear in multiple postings.
    
4. **Analyze job descriptions for pain points.** For each posting, identify:
    - What business problems the role is meant to solve
    - What tools or processes are mentioned (current stack signals)
    - What gaps or challenges are implied by the requirements
    - How these pain points connect to the user's product or solution
    - Team maturity signals (e.g., "first hire" vs. "joining a team of 10")
5. **Enrich each hiring company** by calling `mcp__claude_ai_Amplemarket__enrich_company` with the `domain` for each unique company discovered. Extract:
    - Industry, company size, type
    - Headquarters and locations
    - Tech stack and tools used
    - Funding stage and recent growth signals
    - Company description
6. **Filter against the user's ICP.** Compare enriched company data against the user's stated geography and company size preferences. Remove companies that fall outside the target criteria. Rank remaining companies by signal strength:
    - **Strong signal:** Multiple related job postings, "first hire" language, explicit mention of building a new function
    - **Medium signal:** Single posting for the signal role, growing team language
    - **Soft signal:** Replacement hire or role that may be tangentially related
7. **Find decision-makers** at qualifying companies by calling `mcp__claude_ai_Amplemarket__search_people` with:
    - `company_domains`: [company domain]
    - `person_titles` or `person_seniorities`: based on the user's specified decision-maker roles
    - `full_output`: true
    - `page_size`: 5
    
    Focus on the user's stated decision-maker roles. For each company, identify 2-3 key contacts.
    
8. **Present the results** in a structured hiring-signal report:
    
    **Hiring Signal Summary**
    
    - Total companies found hiring for [signal role]
    - Companies matching ICP after filtering
    - Signal strength distribution (strong / medium / soft)
    
    **Company Results** (table for each company):
    | Field | Detail |
    |-----|-----|
    | Company | {{hiring_company_name}} |
    | Domain | {{hiring_company_domain}} |
    | Signal Role | {{hiring_role_title}} |
    | Posting URL | {{hiring_posting_url}} |
    | Posting Date | {{hiring_posting_date}} |
    | JD Snippet | {{hiring_job_description_snippet}} |
    | Pain Point | {{hiring_pain_point}} |
    | Product Connection | {{hiring_connection_to_product}} |
    | Tools Mentioned | {{hiring_tools_mentioned}} |
    | Team Size Signal | {{hiring_team_size_signal}} |
    | Signal Strength | Strong / Medium / Soft |
    
    **Decision Makers** (per company):
    | Name | Title | LinkedIn | Suggested Opener |
    |----|-----|-------|-----------|
    | ... | ... | ... | {{hiring_suggested_opener}} |
    
9. **Offer to create a lead list** with hiring context. If the user wants to proceed:
    - Call `mcp__claude_ai_Amplemarket__create_lead_list` with a descriptive name (e.g., "Companies Hiring [Signal Role] - [Date]")
    - Call `mcp__claude_ai_Amplemarket__add_leads_to_lead_list` to add the discovered decision-makers
    - Include hiring context in the list description for future reference

### Important Notes

- Job postings are time-sensitive. Always note the posting date and flag any postings older than 60 days as potentially filled.
- WebSearch and WebFetch results depend on public availability. Some job boards may block fetching. If a page fails to load, skip it and note the company for manual review.
- Signal strength matters more than volume. A company posting their "first-ever SDR" is a stronger signal than a Fortune 500 backfilling one of fifty SDRs.
- Always connect the hiring signal back to the user's product. The value is not just that a company is hiring, but why that hire means they likely need the user's solution.
- Respect rate limits and API usage. Limit WebFetch calls to the most promising results and batch `enrich_company` calls efficiently.

## Dynamic Fields Generated

The following dynamic fields are populated for each company discovered through hiring signals:

| Field | Description |
| --- | --- |
| `{{hiring_company_name}}` | Name of the company with the hiring signal |
| `{{hiring_company_domain}}` | Domain of the hiring company |
| `{{hiring_role_title}}` | Exact title of the signal job posting |
| `{{hiring_job_description_snippet}}` | Key excerpt from the job description (2-3 sentences) |
| `{{hiring_pain_point}}` | Primary pain point inferred from the job posting |
| `{{hiring_team_size_signal}}` | Team size or maturity indicator (e.g., "first hire", "team of 5", "scaling from 3 to 10") |
| `{{hiring_posting_date}}` | Date the job was posted or first discovered |
| `{{hiring_posting_url}}` | Direct URL to the job posting |
| `{{hiring_connection_to_product}}` | How the hiring signal connects to the user's product |
| `{{hiring_tools_mentioned}}` | Tools, technologies, or platforms mentioned in the JD |
| `{{hiring_suggested_opener}}` | Personalized opening line referencing the hiring signal |

## Examples

### Example 1: Companies Hiring SDRs (Signal: Building Outbound Team)

**User prompt:** "Find companies hiring SDRs - that means they're building an outbound team and need sales tools"

**What the skill does:**
1. Confirms criteria: signal role = SDR/BDR, signal = building outbound, geography = US, decision-makers = VP Sales/CRO, timeframe = last 30 days.
2. Runs `WebSearch` with queries:
- `"SDR" OR "Sales Development Representative" hiring "open position" United States`
- `site:linkedin.com/jobs "SDR" OR "BDR" SaaS`
- `site:greenhouse.io OR site:lever.co "Sales Development Representative"`
- `"SDR" "first hire" OR "building outbound" "job description"`
3. Calls `WebFetch` on top results to extract company names and job details.
4. Analyzes JDs for pain points (e.g., "no outbound motion yet", "first SDR hire", "building pipeline from scratch").
5. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each unique company.
6. Filters to ICP and ranks by signal strength.
7. Calls `mcp__claude_ai_Amplemarket__search_people` with `person_titles`: ["VP of Sales", "CRO", "Head of Sales"] for each company.
8. Presents report.

**Example output (abbreviated):**

---

**HIRING SIGNAL REPORT: Companies Hiring SDRs**

**Summary:** 23 companies found hiring SDRs in the US. 14 match ICP after filtering. 5 strong signals, 6 medium, 3 soft.

**Top Results:**

| Field | Detail |
| --- | --- |
| Company | CloudMetrics |
| Domain | cloudmetrics.io |
| Signal Role | Sales Development Representative (First Hire) |
| Posting URL | lever.co/cloudmetrics/sdr-001 |
| Posting Date | 2026-02-28 |
| JD Snippet | "We're looking for our first SDR to build the outbound engine from the ground up. You'll define the playbook, select tooling, and establish our outbound motion." |
| Pain Point | No outbound motion exists - need to build from scratch |
| Product Connection | Building outbound from zero requires sales engagement tooling, sequencing, and prospecting platform |
| Tools Mentioned | Salesforce, LinkedIn Sales Navigator |
| Team Size Signal | First SDR hire - no existing outbound team |
| Signal Strength | Strong |

**Decision Makers:**
| Name | Title | LinkedIn | Suggested Opener |
|----|-----|-------|-----------|
| Alex Rivera | VP of Sales | linkedin.com/in/arivera | "Alex, saw CloudMetrics is hiring its first SDR. Building outbound from scratch is exciting but the tooling decisions you make now will define the team's velocity for years." |
| Jordan Lee | CRO | linkedin.com/in/jlee | "Jordan, noticed CloudMetrics is building out the SDR function. Curious what sales stack you are evaluating as you stand up the outbound motion." |

---

### Example 2: Companies Hiring Data Engineers (Signal: Investing in Data Infrastructure)

**User prompt:** "Who's posting jobs for data engineers? Companies investing in data infrastructure probably need our data observability tool."

**What the skill does:**
1. Confirms criteria: signal role = Data Engineer/Analytics Engineer, signal = data infrastructure investment, decision-makers = VP Engineering/Head of Data/CTO.
2. Runs `WebSearch` with queries:
- `"Data Engineer" hiring OR "open position" United States`
- `site:linkedin.com/jobs "Data Engineer" OR "Analytics Engineer" SaaS`
- `site:greenhouse.io OR site:lever.co "Data Engineer" "data pipeline"`
- `"Data Engineer" "first hire" OR "building data team" "job description"`
3. Calls `WebFetch` on top results to extract company names and job details.
4. Analyzes JDs for data stack mentions (Snowflake, dbt, Airflow, Fivetran) and pain points (data quality issues, scaling pipelines, migrating to modern stack).
5. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each unique company.
6. Filters to ICP and ranks by signal strength.
7. Calls `mcp__claude_ai_Amplemarket__search_people` with `person_titles`: ["VP of Engineering", "Head of Data", "CTO"] for each company.
8. Presents report.

**Example output (abbreviated):**

---

**HIRING SIGNAL REPORT: Companies Hiring Data Engineers**

**Summary:** 31 companies found hiring Data Engineers. 18 match ICP after filtering. 7 strong signals, 8 medium, 3 soft.

**Top Results:**

| Field | Detail |
| --- | --- |
| Company | FinLedger |
| Domain | finledger.io |
| Signal Role | Senior Data Engineer (First Data Hire) |
| Posting URL | greenhouse.io/finledger/data-eng-01 |
| Posting Date | 2026-02-20 |
| JD Snippet | "We're building our data infrastructure from the ground up. You'll be our first dedicated data engineer, responsible for designing pipelines, selecting the warehouse, and establishing data quality practices." |
| Pain Point | No existing data infrastructure - building from zero with no observability |
| Product Connection | Greenfield data stack needs observability from day one to avoid data quality debt |
| Tools Mentioned | Python, SQL, AWS, "modern data stack" |
| Team Size Signal | First data hire - no existing data team |
| Signal Strength | Strong |

**Decision Makers:**
| Name | Title | LinkedIn | Suggested Opener |
|----|-----|-------|-----------|
| Priya Sharma | CTO | linkedin.com/in/psharma | "Priya, saw FinLedger is hiring its first data engineer. Building the data stack from scratch is the perfect time to bake in observability before pipeline complexity makes it painful." |
| Marcus Webb | VP of Engineering | linkedin.com/in/mwebb | "Marcus, noticed FinLedger is standing up a data function. Curious if data observability is part of the architecture plan or something you are planning to add later." |

---

### Example 3: Companies Hiring RevOps Manager (Signal: Scaling Revenue Operations)

**User prompt:** "Find companies hiring a RevOps Manager - that signals they're scaling and need revenue intelligence tooling"

**What the skill does:**
1. Confirms criteria: signal role = RevOps Manager/Revenue Operations, signal = scaling revenue operations, decision-makers = CRO/VP Revenue Operations/VP Sales.
2. Runs `WebSearch` with queries:
- `"RevOps Manager" OR "Revenue Operations Manager" hiring`
- `site:linkedin.com/jobs "Revenue Operations" SaaS B2B`
- `site:greenhouse.io OR site:lever.co "RevOps" OR "Revenue Operations"`
- `"Revenue Operations" "first hire" OR "building RevOps" "job description"`
3. Calls `WebFetch` on top results to extract company names and job details.
4. Analyzes JDs for pain points: CRM hygiene, forecasting accuracy, pipeline visibility, tool consolidation.
5. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each unique company.
6. Filters to Series B+ companies with 100-2000 employees (typical RevOps hire profile).
7. Calls `mcp__claude_ai_Amplemarket__search_people` with `person_titles`: ["CRO", "VP of Sales", "VP Revenue Operations"] for each company.
8. Presents report.

**Example output (abbreviated):**

---

**HIRING SIGNAL REPORT: Companies Hiring RevOps Managers**

**Summary:** 19 companies found hiring RevOps Managers. 12 match ICP after filtering. 4 strong signals, 5 medium, 3 soft.

**Top Results:**

| Field | Detail |
| --- | --- |
| Company | ScaleFlow |
| Domain | scaleflow.com |
| Signal Role | Revenue Operations Manager (First RevOps Hire) |
| Posting URL | lever.co/scaleflow/revops-001 |
| Posting Date | 2026-03-01 |
| JD Snippet | "We're hiring our first Revenue Operations Manager to bring structure to our go-to-market engine. You'll own CRM administration, build forecasting models, and establish reporting across sales, marketing, and CS." |
| Pain Point | No formalized RevOps function - forecasting and pipeline reporting done ad hoc |
| Product Connection | Formalizing RevOps requires revenue intelligence tooling for pipeline visibility and forecasting accuracy |
| Tools Mentioned | Salesforce, Google Sheets ("migrating from spreadsheets") |
| Team Size Signal | First RevOps hire - no existing operations team |
| Signal Strength | Strong |

**Decision Makers:**
| Name | Title | LinkedIn | Suggested Opener |
|----|-----|-------|-----------|
| Dana Mitchell | CRO | linkedin.com/in/dmitchell | "Dana, saw ScaleFlow is bringing on its first RevOps hire. That transition from spreadsheets to a real revenue operations function is exactly when the right tooling makes or breaks the process." |
| Chris Nakamura | VP of Sales | linkedin.com/in/cnakamura | "Chris, noticed ScaleFlow is formalizing RevOps. Curious how you are thinking about revenue intelligence tooling as you move beyond spreadsheet-based forecasting." |

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| WebSearch returns few job postings | Fallback chain: 1) Broaden the job title (e.g., add variations like "BDR" for "SDR", "Analytics Engineer" for "Data Engineer"). 2) Remove geography constraints and search globally. 3) Try different job board sites (add Ashby, Workable, JazzHR to search queries). 4) Search for the function instead of the exact title (e.g., "outbound sales" instead of "SDR"). |
| WebFetch fails to load a job posting page | Skip the page and note the company name and URL for manual review. Many job boards use JavaScript rendering that blocks fetching. Try fetching the cached or AMP version if available, or search for the same posting on a different job board. |
| Job posting appears outdated or already filled | Check the posting date. If older than 60 days, flag it: "This posting may already be filled - verify before outreach." Still enrich the company, as the hiring signal may still indicate ongoing need. |
| Too many companies found (50+) | Tighten ICP filters: narrow geography, company size, or industry. Alternatively, rank by signal strength and present only the top 15-20 strongest signals. Offer to drill into specific segments. |
| No decision-makers found at a hiring company | Fallback chain: 1) Broaden seniority to include "Manager" and "Senior". 2) Try searching by company name instead of domain. 3) For companies with <50 employees, search for "Founder" and "C-Suite" only. 4) Suggest using `enrich_person` with a specific name if the user has one. |
| Signal role is too niche for broad job board search | Pivot strategy: 1) Search for the broader function (e.g., "machine learning" instead of "MLOps Engineer"). 2) Use industry-specific job boards in WebSearch queries. 3) Search company career pages directly via WebFetch for known target companies. 4) Ask the user for related or adjacent roles that indicate the same buying signal. |
| Company enrichment returns minimal data | Use information from the job posting itself (company description, team size, tech stack mentions) to supplement enrichment data. Flag thin enrichment: "Limited enrichment data - company details sourced primarily from job posting." |
| User's signal hypothesis seems weak | Validate the signal before proceeding. Ask: "How confident are you that hiring for [role] indicates they need [product]? Want me to analyze a few postings first to test the hypothesis before doing the full search?" Run a small pilot search of 3-5 postings and review the JDs together before scaling up. |
