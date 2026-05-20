---
name: conference-event-lead-finder
description: >
  Scrape conference and event websites for speakers, sponsors, and exhibitors, enrich them via Amplemarket, filter against your ICP, and find decision-makers at those companies.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Prospecting & Lead Generation"
compatibility: Requires Amplemarket MCP server
---

# Conference & Event Lead Finder

Scrape conference and event websites for speakers, sponsors, and exhibitors, enrich them via Amplemarket, filter against your ICP, and find decision-makers at those companies.

## Instructions

When a user wants to find leads from a specific conference, event, or trade show, extract attendee and company data from the event website and enrich it into actionable prospect lists.

### Steps

1. **Gather event details** from the user's request. Extract or ask for:
    - **Event name and/or URL** (e.g., "SaaStr Annual 2026", "https://saas-conference.example.com")
    - **What to find:** speakers, sponsors, exhibitors, attendees, or all
    - **Target roles** at discovered companies (e.g., "VP of Sales", "CTO", "Head of Marketing")
    - **Specific sessions or tracks** of interest (optional, e.g., "AI track", "Growth stage talks")
    - **ICP filters** (optional, company size, industry, geography)
    
    If the user provides only an event name without a URL, proceed to step 2 to find the event website.
    
2. **Find the event website** by calling `WebSearch` with the event name plus keywords like "speakers", "sponsors", or "agenda". Target queries:
    - `"[Event Name] speakers 2026"`
    - `"[Event Name] sponsors exhibitors"`
    - `"[Event Name] agenda schedule"`
    
    Identify the official event website and the specific pages for speakers, sponsors, and agenda.
    
3. **Extract speaker and sponsor data** by calling `WebFetch` on the identified pages:
    
    **For speakers:**
    
    - Fetch the speakers page URL
    - Extract: speaker name, title, company, talk title, session/track, bio snippet
    - If speakers are spread across multiple pages (pagination or separate session pages), fetch each page
    
    **For sponsors:**
    
    - Fetch the sponsors or partners page URL
    - Extract: company name, sponsorship tier (Platinum/Gold/Silver/Bronze), logo, website URL
    - Note the tier level as it indicates budget and commitment level
    
    **For exhibitors:**
    
    - Fetch the exhibitors or expo hall page URL
    - Extract: company name, booth number (if listed), website URL, description
4. **Enrich discovered companies** by calling `mcp__claude_ai_Amplemarket__enrich_company` with the `domain` for each unique company identified from speakers, sponsors, and exhibitors. Key data points to extract:
    - Industry and sub-industry
    - Company size and employee count
    - Headquarters location
    - Tech stack
    - Funding stage and recent rounds
    - Company description
    
    Batch efficiently. Deduplicate companies that appear in multiple roles (e.g., a company that is both a sponsor and has a speaker).
    
5. **Filter companies against the user's ICP.** If the user specified ICP criteria (company size, industry, geography), filter the enriched companies. If no ICP was specified, present all companies and ask: "Want me to filter these by company size, industry, or geography?"
6. **Find decision-makers at matching companies** by calling `mcp__claude_ai_Amplemarket__search_people` with:
    - `company_domains`: [matched company domain]
    - `person_titles` or `person_seniorities`: based on the user's target roles
    - `full_output`: true
    - `page_size`: 5
    
    For each matching company, find the contacts most relevant to the user's outreach goals.
    
7. **Enrich speakers for deeper context.** For speakers specifically, gather additional personalization data:
    - Use `WebSearch` to find their talk title, abstract, and bio if not already extracted
    - Call `mcp__claude_ai_Amplemarket__enrich_person` with `name` and `company_name` (or `linkedin_url` if found) to get career history, LinkedIn URL, and contact details. Set `reveal_email` to `true` if the user wants contact information. **Credit note:** Enabling `reveal_email` and `reveal_phone_numbers` consumes additional Amplemarket credits per reveal.
    - Note the talk topic as a personalization hook for outreach
8. **Present results** organized by conference role (speakers, sponsors, exhibitors) with the following dynamic fields available for outreach personalization:
    - `{{conference_name}}` - Name of the conference or event
    - `{{conference_date}}` - Date or date range of the event
    - `{{conference_role}}` - The lead's role at the event (Speaker, Sponsor, Exhibitor, Attendee)
    - `{{conference_talk_title}}` - Title of the speaker's talk or panel
    - `{{conference_talk_topic}}` - Topic area or track of the session
    - `{{conference_company_name}}` - Company name as listed at the event
    - `{{conference_sponsorship_tier}}` - Sponsor level (Platinum, Gold, Silver, Bronze)
    - `{{conference_bio_highlight}}` - Key highlight from the speaker's bio or abstract
    - `{{conference_shared_session}}` - Session or track the user and lead both attended
    - `{{conference_suggested_opener}}` - AI-generated opening line referencing the event context
    - `{{conference_speaker_linkedin}}` - Speaker's LinkedIn profile URL
    
    Format the output as:
    
    **Event Summary**
    
    - Event name, date, location
    - Total speakers, sponsors, and exhibitors found
    - Companies matching ICP
    
    **Speakers** (table with: Name, Title, Company, Talk Title, Topic/Track, LinkedIn)
    
    **Sponsors** (table with: Company, Tier, Domain, Industry, Size, ICP Match)
    
    **Exhibitors** (table with: Company, Domain, Industry, Size, ICP Match)
    
    **Decision-Makers Found** (table with: Name, Title, Company, Conference Role, Email, LinkedIn)
    
    **Personalization Hooks** - For each top lead, a suggested opener referencing their conference participation.
    
9. **Offer to create a lead list** with event context. If the user wants to proceed:
    - Call `mcp__claude_ai_Amplemarket__create_lead_list` with a name like "[Event Name] - [Role] Leads"
    - Call `mcp__claude_ai_Amplemarket__add_leads_to_lead_list` with the discovered leads
    - Confirm the list was created and provide the count of leads added

### Important Notes

- WebFetch may be blocked by some event websites that use JavaScript-heavy rendering or anti-scraping protections. If WebFetch returns empty or blocked content, ask the user to paste the speaker/sponsor list directly and proceed from step 4.
- Deduplicate across speakers, sponsors, and exhibitors before enriching to avoid redundant API calls.
- Speaker personalization is the highest-value output. A reference to someone's specific talk topic is a strong outreach hook.
- Sponsorship tier correlates with budget: Platinum/Diamond sponsors are investing heavily and may be more receptive to vendor conversations.
- For large conferences with 100+ speakers, ask the user to narrow by track or session topic before enriching all companies.
- Never fabricate speaker names, talk titles, or company associations. Only use data extracted from the event website or returned by enrichment APIs.

## Dynamic Fields Generated

The following dynamic fields are populated during the workflow and can be used in outreach templates:

| Field | Description | Source |
| --- | --- | --- |
| `{{conference_name}}` | Name of the conference or event | User input / WebFetch |
| `{{conference_date}}` | Date or date range of the event | WebFetch from event page |
| `{{conference_role}}` | Lead's role at the event (Speaker, Sponsor, Exhibitor) | WebFetch extraction |
| `{{conference_talk_title}}` | Title of the speaker's presentation or panel | WebFetch from agenda/speaker page |
| `{{conference_talk_topic}}` | Topic area, track, or theme of the session | WebFetch from agenda page |
| `{{conference_company_name}}` | Company name as listed at the event | WebFetch extraction |
| `{{conference_sponsorship_tier}}` | Sponsor level (Platinum, Gold, Silver, Bronze) | WebFetch from sponsor page |
| `{{conference_bio_highlight}}` | Key highlight from the speaker's bio or talk abstract | WebFetch + WebSearch |
| `{{conference_shared_session}}` | Session or track the user and lead both attended | User input + agenda matching |
| `{{conference_suggested_opener}}` | AI-generated opening line referencing event context | Synthesized from all fields |
| `{{conference_speaker_linkedin}}` | Speaker's LinkedIn profile URL | `enrich_person` result |

## Examples

### Example 1: SaaS Conference Speaker List

**User prompt:** "Find leads from SaaStr Annual 2026. I want to reach out to speakers who are VP+ at companies with 200-2000 employees"

**What the skill does:**
1. Calls `WebSearch` with "SaaStr Annual 2026 speakers list" and "SaaStr Annual 2026 agenda schedule".
2. Calls `WebFetch` on the SaaStr speakers page to extract speaker names, titles, companies, and talk titles.
3. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each unique company (e.g., domain: "gong.io", domain: "salesloft.com").
4. Filters companies to 200-2000 employees.
5. Calls `mcp__claude_ai_Amplemarket__search_people` at matching companies with `person_seniorities`: ["VP", "Head", "Director", "C-Suite"].
6. Calls `mcp__claude_ai_Amplemarket__enrich_person` for each speaker with `reveal_email`: true.
7. Compiles results with personalization hooks.

**Example output:**

---

**EVENT LEAD REPORT: SaaStr Annual 2026**

**Event Summary**
| Field | Detail |
|-----|-----|
| Event | SaaStr Annual 2026 |
| Date | September 15-17, 2026 |
| Location | San Mateo, CA |
| Speakers Found | 87 |
| Unique Companies | 72 |
| ICP Matches (200-2000 employees) | 28 |

**Speakers at ICP-Matching Companies**

| Name | Title | Company | Talk Title | Track | LinkedIn |
| --- | --- | --- | --- | --- | --- |
| Maria Santos | VP of Revenue Ops | CloudMetrics | "Scaling RevOps from $10M to $100M ARR" | Growth Stage | linkedin.com/in/msantos |
| James Liu | CRO | DataSync | "Building a Predictable Pipeline Machine" | Sales Leadership | linkedin.com/in/jliu |
| Priya Sharma | VP of Customer Success | FlowStack | "Net Revenue Retention as a Growth Engine" | CS & Retention | linkedin.com/in/psharma |
| ... | ... | ... | ... | ... | ... |

**Additional Decision-Makers at Speaker Companies**

| Name | Title | Company | Conference Role | Email | LinkedIn |
| --- | --- | --- | --- | --- | --- |
| Tom Rodriguez | Head of Partnerships | CloudMetrics | Speaker's Company | tom@cloudmetrics.io | linkedin.com/in/trodriguez |
| Sarah Kim | VP of Engineering | DataSync | Speaker's Company | sarah.k@datasync.com | linkedin.com/in/skim |
| ... | ... | ... | ... | ... | ... |

**Personalization Hooks**

**Maria Santos (CloudMetrics):**
- `{{conference_suggested_opener}}`: "Maria, your SaaStr talk on scaling RevOps from $10M to $100M really resonated. We have been seeing similar patterns with our customers around the ops bottlenecks that emerge at that growth stage."
- `{{conference_talk_topic}}`: Revenue Operations, Scaling
- `{{conference_bio_highlight}}`: Scaled CloudMetrics RevOps team from 2 to 18 in 18 months

**James Liu (DataSync):**
- `{{conference_suggested_opener}}`: "James, caught the description of your 'Predictable Pipeline Machine' session at SaaStr. Curious whether the framework you outline accounts for the signal-to-noise problem most teams hit at scale."
- `{{conference_talk_topic}}`: Pipeline Generation, Sales Leadership
- `{{conference_bio_highlight}}`: Former VP Sales at Outreach, grew ARR 4x in 2 years

Shall I create a lead list called "SaaStr Annual 2026 - Speaker Leads"?

---

### Example 2: Sponsor Logo Extraction

**User prompt:** "Get me the sponsors from AWS re:Invent 2026. I want to find decision-makers at Gold and Platinum sponsors"

**What the skill does:**
1. Calls `WebSearch` with "AWS re:Invent 2026 sponsors partners page".
2. Calls `WebFetch` on the sponsors page to extract company names and sponsorship tiers.
3. Filters to Gold and Platinum tier sponsors only.
4. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each sponsor domain.
5. Calls `mcp__claude_ai_Amplemarket__search_people` at each sponsor company with `person_seniorities`: ["VP", "Head", "Director", "C-Suite"], `page_size`: 5.
6. Presents results organized by sponsorship tier.

**Example output:**

---

**EVENT LEAD REPORT: AWS re:Invent 2026 - Sponsors**

**Sponsors by Tier**

*Platinum Sponsors*
| Company | Domain | Industry | Size | HQ |
|------|-----|-------|----|---|
| Datadog | datadog.com | Cloud Monitoring | 5001-10000 | New York, NY |
| HashiCorp | hashicorp.com | Infrastructure Software | 2001-5000 | San Francisco, CA |
| Snowflake | snowflake.com | Data Cloud | 5001-10000 | Bozeman, MT |

*Gold Sponsors*
| Company | Domain | Industry | Size | HQ |
|------|-----|-------|----|---|
| LaunchDarkly | launchdarkly.com | Feature Management | 501-1000 | Oakland, CA |
| Fivetran | fivetran.com | Data Integration | 1001-2000 | Oakland, CA |
| ... | ... | ... | ... | ... |

**Decision-Makers at Sponsor Companies**

| Name | Title | Company | Tier | LinkedIn |
| --- | --- | --- | --- | --- |
| Jordan Lee | VP of Engineering | Datadog | Platinum | linkedin.com/in/jlee |
| Anita Patel | Head of Alliances | HashiCorp | Platinum | linkedin.com/in/apatel |
| ... | ... | ... | ... | ... |

`{{conference_suggested_opener}}`: "Anita, saw that HashiCorp is a Platinum sponsor at re:Invent this year. Given your investment in the AWS ecosystem, I'd love to discuss how we complement that strategy."

---

### Example 3: Specific Track or Session Leads

**User prompt:** "Find people speaking on the AI/ML track at Web Summit 2026. We sell MLOps tools and want to reach out to engineering leaders"

**What the skill does:**
1. Calls `WebSearch` with "Web Summit 2026 AI ML track speakers agenda".
2. Calls `WebFetch` on the agenda page, filtering for AI/ML track sessions.
3. Extracts speakers from AI/ML sessions only: names, titles, companies, talk titles.
4. Calls `mcp__claude_ai_Amplemarket__enrich_company` for each speaker's company.
5. Filters for companies where MLOps tooling is relevant (tech companies, 100+ employees, engineering-heavy orgs).
6. Calls `mcp__claude_ai_Amplemarket__search_people` at matching companies with `person_titles`: ["VP of Engineering", "Head of ML", "Director of Data Science", "CTO", "Head of AI"], `full_output`: true.
7. Calls `mcp__claude_ai_Amplemarket__enrich_person` for each speaker to get LinkedIn and email.
8. Presents results with MLOps-specific personalization hooks.

**Example output:**

---

**EVENT LEAD REPORT: Web Summit 2026 - AI/ML Track**

**Event Summary**
| Field | Detail |
|-----|-----|
| Event | Web Summit 2026 |
| Track | AI/ML & Data Science |
| Sessions in Track | 24 |
| Speakers Found | 31 |
| ICP Matches (tech, 100+ employees) | 18 |

**AI/ML Track Speakers**

| Name | Title | Company | Talk Title | LinkedIn |
| --- | --- | --- | --- | --- |
| Dr. Lin Wei | VP of AI | ScaleML | "Production ML: From Notebook to Pipeline" | linkedin.com/in/linwei |
| Marcus Johnson | Head of Data Science | FinanceAI | "Building Responsible AI at Scale" | linkedin.com/in/mjohnson |
| Elena Kovar | CTO | DeepOps | "The MLOps Stack of 2027" | linkedin.com/in/ekovar |
| ... | ... | ... | ... | ... |

**Engineering Leaders at Speaker Companies**

| Name | Title | Company | Email | LinkedIn |
| --- | --- | --- | --- | --- |
| Raj Patel | Director of Platform Eng | ScaleML | raj@scaleml.ai | linkedin.com/in/rpatel |
| ... | ... | ... | ... | ... |

**Personalization Hooks**

**Dr. Lin Wei (ScaleML):**
- `{{conference_suggested_opener}}`: "Dr. Wei, your Web Summit talk on moving from notebook to production pipeline is exactly the problem we are solving at [Company]. Would love to compare notes on the infrastructure gaps you highlighted."
- `{{conference_talk_topic}}`: MLOps, Production ML
- `{{conference_bio_highlight}}`: Led ML infrastructure at Google Brain before joining ScaleML

Shall I create a lead list called "Web Summit 2026 - AI/ML Track Leads"?

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| WebFetch returns empty or blocked content | Many event websites use JavaScript rendering or anti-bot protections that prevent scraping. Fallback: Ask the user to paste the speaker list, sponsor list, or agenda content directly into the chat. Then proceed from step 4 (enrichment) using the pasted data. You can also try fetching a cached version via `WebSearch` with `"cache:[URL]"`. |
| Event website not found via WebSearch | Fallback chain: 1) Try alternate search queries. Include the year, city, or organizer name. 2) Search for "[Event Name] speakers list" on LinkedIn or Twitter. 3) Ask the user for the direct URL: "I could not find the official website for [Event]. Can you share the URL or paste the speaker/sponsor list?" |
| No ICP matches among conference companies | Expand ICP filters: 1) Broaden company size range. 2) Include adjacent industries. 3) Remove geography restrictions. If still no matches, present all discovered companies and let the user decide which to target. |
| Speaker page is paginated or split across multiple pages | Fetch each page sequentially. Look for URL patterns like `/speakers?page=2` or `/speakers/day-1`, `/speakers/day-2`. If pagination is JavaScript-driven and WebFetch cannot access subsequent pages, ask the user to share the full list. |
| Too many speakers or sponsors (100+) | Ask the user to narrow the scope: "This event has 150+ speakers. Want me to focus on a specific track (e.g., AI/ML, Growth, Sales) or filter by seniority (VP+ only)?" Process in batches of 20-30 companies to manage API usage. |
| Speaker enrichment returns wrong person | Disambiguate by using both `name` and `company_name` in `mcp__claude_ai_Amplemarket__enrich_person`. If still ambiguous, use the speaker's LinkedIn URL if found on the event page. Confirm with the user before including in the lead list. |
| Sponsor tier information not available | Some event pages list sponsors without explicit tiers. Infer tier from logo size or page placement (larger logos at top = higher tier). If uncertain, label all sponsors as "Sponsor" without a tier and note: "Tier information was not available on the event page." |
| Company enrichment succeeds but `search_people` finds no decision-makers | Fallback chain: 1) Broaden seniority to include "Manager" and "Senior". 2) Try searching by company name instead of domain. 3) For small companies (<50 employees), search for "Founder" and "C-Suite" only. 4) Use `mcp__claude_ai_Amplemarket__enrich_person` with the speaker's name and company as a direct fallback. |