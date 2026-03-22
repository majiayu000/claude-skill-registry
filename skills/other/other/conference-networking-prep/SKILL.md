---
name: conference-networking-prep
description: >
  Research conference speakers, sponsors, and attendees, cross-reference against your ICP, and produce a tiered networking playbook with per-person personalization, icebreakers, and follow-up openers.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Outreach & Personalization"
compatibility: Requires Amplemarket MCP server
---

# Conference Networking Prep

Research conference speakers, sponsors, and attendees, cross-reference against your ICP, and produce a tiered networking playbook with per-person personalization, icebreakers, and follow-up openers.

## Instructions

When a user wants to prepare for a conference or event, build a comprehensive networking playbook that identifies the highest-value people to meet and arms the user with personalized talking points for each.

### Steps

1. **Gather event context from the user.** Ask for:
    - **Event name and/or URL** - needed to research speakers, sponsors, and agenda.
    - **ICP criteria** - who counts as a high-value contact (target titles, industries, company sizes, departments).
    - **Goal** - what the user wants to achieve at the event: pipeline generation, meeting prospects, recruiting, partnerships, brand awareness, or a combination.
    - **Is the user speaking?** - if yes, gather talk title and topic so the playbook can reference it in icebreakers and follow-ups.
    - **Meeting capacity** - how many meaningful conversations the user can realistically have (e.g., 10-15 meetings over 2 days). This determines how many Tier 1 targets to prioritize.
    
    If any of these are missing, ask before proceeding.
    
2. **Research the conference** by calling `WebSearch` with the event name to find the official website, speaker list, sponsor list, agenda, and session descriptions. Then call `WebFetch` on the most promising URLs to extract:
    - Full speaker list with names, titles, companies, and talk titles
    - Sponsor list organized by tier (Platinum, Gold, Silver, etc.)
    - Agenda with session times, topics, and panel compositions
    - Any published attendee list or networking directory
    
    If the conference website is gated or incomplete, try alternate sources: LinkedIn event pages, conference recap blogs from prior years, press releases announcing speakers, and sponsor announcement posts.
    
3. **Enrich speaker and sponsor companies** by calling `mcp__claude_ai_Amplemarket__enrich_company` for each unique company represented by speakers and sponsors. Extract:
    - Industry and sub-industry
    - Company size (employee count)
    - Company type
    - Headquarters location
    - Description and value proposition
    
    Compare each company's firmographics against the user's ICP criteria. Flag companies that match on 2+ ICP dimensions as high-priority.
    
4. **Find decision-makers at ICP-matching companies** by calling `mcp__claude_ai_Amplemarket__search_people` for each ICP-matching company with:
    - `company_domains`: [company domain]
    - `person_seniorities`: based on user's ICP (e.g., ["VP", "Director", "C-Suite"])
    - `person_departments`: relevant to the user's product
    - `full_output`: true
    - `page_size`: 5
    
    Then call `mcp__claude_ai_Amplemarket__enrich_person` for the top 2-3 targets per company (prioritize speakers first, then other senior leaders who may also attend). Set `reveal_email` to `true` for contact details. **Credit note:** Enabling `reveal_email` and `reveal_phone_numbers` consumes additional Amplemarket credits per reveal.
    
5. **Research each top target for personalization** by calling `WebSearch` for each Tier 1 and Tier 2 target with queries like:
    - "[Person name] [company] podcast" - recent podcast appearances
    - "[Person name] [company] blog" - published articles or thought leadership
    - "[Person name] [company] news" - recent press mentions, funding announcements, product launches
    - "[Person name] conference talk" - prior speaking appearances or recorded talks
    
    Extract 1-2 recent, specific data points per person that can fuel icebreakers and follow-up openers.
    
6. **Prioritize targets into tiers** based on a scoring framework:
    - **Tier 1 (Must-Meet):** ICP match + speaking at the event + relevant talk topic. These are the highest-value targets because their talk topic signals active interest in the user's domain, and they are guaranteed to be present. Limit Tier 1 to the user's meeting capacity.
    - **Tier 2 (High-Priority):** ICP match + sponsor company representative OR ICP match + panelist on a relevant session. Sponsors have booths and are accessible; panelists are semi-public figures at the event.
    - **Tier 3 (Opportunistic):** ICP match + confirmed attendee or company known to attend. These are targets of opportunity, worth pursuing if the user has bandwidth after covering Tier 1 and Tier 2.
    
    Within each tier, rank by ICP match strength (more matching dimensions = higher rank).
    
7. **Generate the networking playbook** with per-person personalization. For each target, provide:
    
    **Per-Person Card:**
    
    - Name, title, company
    - Priority tier and ICP match reason
    - Talk title and relevance (if speaking)
    - Recent activity or news (from WebSearch)
    - Icebreaker (a natural conversation opener referencing their talk, recent news, or shared context)
    - Follow-up opener (a post-event email or LinkedIn message opener that references the conference interaction)
    - Shared sessions (sessions both the user and the target might attend)
    - Company news (recent company-level developments)
    
    **Playbook Structure:**
    
    - Executive summary: event name, dates, user's goal, total targets identified per tier
    - Tier 1 targets with full per-person cards
    - Tier 2 targets with full per-person cards
    - Tier 3 targets with abbreviated cards (name, title, company, ICP match reason, one-line icebreaker)
    - Day-by-day schedule overlay: which sessions to attend based on where Tier 1 and Tier 2 targets will be
    - General networking tips tailored to the event format (e.g., "Sponsor booths are best visited during the afternoon lull between 2-3pm")
8. **Populate dynamic fields** for each target in the playbook. Generate the `{{confprep_*}}` fields described in the Dynamic Fields Generated section below. These fields enable downstream outreach templates to reference conference-specific personalization.
9. **Offer to create a lead list** with all identified targets. If the user agrees, call `mcp__claude_ai_Amplemarket__create_lead_list` with:
    - `name`: descriptive name (e.g., "SaaStr Annual 2026 - Networking Targets - Mar 2026")
    - `type`: "linkedin" (if LinkedIn URLs are available) or "email"
    - `leads`: array of lead objects from the research
    - `options`: ask about enrichment preferences (`enrich`, `validate_email`, `reveal_phone_numbers`)
    
    Include the tier classification and conference context in the list description so downstream outreach can reference the event.
    

### Important Notes

- Conference websites vary widely in structure. If `WebFetch` fails on the main speaker page, try alternate URLs: /speakers, /agenda, /schedule, /sponsors, /partners, /exhibitors.
- Start by enriching companies before enriching individual people. Company enrichment determines ICP fit and prevents wasting credits on people at non-ICP companies.
- Icebreakers should feel natural and specific. Reference the person's actual talk title, a real quote from a recent article, or a concrete company milestone. Never generic compliments.
- If the user is also speaking, weave their talk topic into icebreakers: "I'm presenting on [topic] in the afternoon session. Would love to get your perspective given your work on [related area]."
- Respect the user's meeting capacity. If they say 10 meetings, keep Tier 1 at 10 or fewer and present Tier 2 as backup options.

## Dynamic Fields Generated

| Field | Description |
| --- | --- |
| `{{confprep_person_name}}` | Full name of the conference target |
| `{{confprep_person_title}}` | Current job title of the target |
| `{{confprep_company}}` | Company name of the target |
| `{{confprep_priority_tier}}` | Assigned tier: Tier 1 (Must-Meet), Tier 2 (High-Priority), or Tier 3 (Opportunistic) |
| `{{confprep_icp_match_reason}}` | Why this person's company matches the user's ICP (e.g., "SaaS, 201-500 employees, Series B, US-based") |
| `{{confprep_talk_title}}` | Title of the person's conference talk or panel (blank if not speaking) |
| `{{confprep_talk_relevance}}` | Why the talk topic is relevant to the user's product or goal (blank if not speaking) |
| `{{confprep_recent_activity}}` | Most recent notable activity: podcast appearance, blog post, press mention, or social post |
| `{{confprep_icebreaker}}` | Natural conversation opener for approaching this person at the event |
| `{{confprep_followup_opener}}` | Post-event email or LinkedIn message opener referencing the conference interaction |
| `{{confprep_shared_sessions}}` | Sessions both the user and the target are likely to attend based on agenda overlap |
| `{{confprep_company_news}}` | Recent company-level news: funding, product launches, expansions, partnerships |

## Examples

### Example 1: Full Networking Playbook for SaaStr Annual

**User prompt:** "Prep me for SaaStr Annual 2026. I sell sales engagement software to VP/Director of Sales at mid-market SaaS companies (200-1000 employees). Goal is pipeline generation. I can realistically have 12 meetings over the 3 days."

**What the skill does:**
1. Asks if the user is speaking (user says no).
2. Calls `WebSearch` with "SaaStr Annual 2026 speakers sponsors agenda" to find event details.
3. Calls `WebFetch` on the SaaStr Annual speakers page, sponsors page, and agenda page.
4. Identifies 85 speakers across 40 companies and 30 sponsor companies.
5. Calls `mcp__claude_ai_Amplemarket__enrich_company` for all 70 unique companies.
6. Filters to 18 ICP-matching companies (mid-market SaaS, 200-1000 employees).
7. Calls `mcp__claude_ai_Amplemarket__search_people` for each ICP-matching company to find VP/Director of Sales.
8. Calls `mcp__claude_ai_Amplemarket__enrich_person` for top targets (speakers first).
9. Calls `WebSearch` for each Tier 1 target to find recent news, podcast appearances, and blog posts.
10. Produces tiered playbook.

**Example output:**

---

**CONFERENCE NETWORKING PLAYBOOK: SaaStr Annual 2026**

**Event:** SaaStr Annual 2026 | San Francisco, CA | Sep 15-17
**Your Goal:** Pipeline generation - sales engagement software
**ICP:** VP/Director of Sales at mid-market SaaS (200-1000 employees)
**Meeting Capacity:** 12 meetings over 3 days

**Summary:** Identified 28 high-value targets across 18 ICP-matching companies. 8 are speakers with relevant talk topics (Tier 1), 11 are at sponsor companies (Tier 2), and 9 are at companies known to attend (Tier 3).

---

**TIER 1: MUST-MEET (8 targets)**

**1. Rachel Torres - VP of Sales, CloudFlow (cloudflow.io)**
| Field | Detail |
|-----|-----|
| Priority | Tier 1 |
| ICP Match | SaaS, 420 employees, Series C, US-based, Revenue department |
| Talk | "Scaling Outbound at the Mid-Market: What Works in 2026" (Day 1, 2:00 PM, Main Stage) |
| Talk Relevance | Directly discusses outbound sales scaling, the core use case for sales engagement software |
| Recent Activity | Guest on "The Revenue Podcast" last month discussing AI-powered sequencing tools |
| Icebreaker | "Your point on the podcast about AI sequencing replacing manual cadences really resonated. I'd love to hear how that's playing out at CloudFlow since you made the switch." |
| Follow-Up Opener | "Rachel, really enjoyed your SaaStr talk on scaling outbound at the mid-market. Your point about sequence personalization at scale is exactly the problem we're solving at [Company]." |
| Shared Sessions | Day 1 Main Stage (her talk), Day 2 "Sales Tech Stack" roundtable |
| Company News | CloudFlow closed a $45M Series C in Q1 2026 and is expanding their sales team from 40 to 80 reps |

**2. David Kim - Director of Revenue Operations, MetricStack (metricstack.io)**
| Field | Detail |
|-----|-----|
| Priority | Tier 1 |
| ICP Match | SaaS, 310 employees, Series B, US-based, Revenue department |
| Talk | "RevOps as the Connective Tissue: Aligning Sales, Marketing, and CS" (Day 2, 10:30 AM, Track B) |
| Talk Relevance | RevOps leaders evaluate and implement sales engagement platforms, making them a direct buyer persona |
| Recent Activity | Published a blog post on "Why We Ripped Out Our Sales Engagement Tool" last quarter |
| Icebreaker | "I read your post about ripping out your sales engagement tool. I'm curious what broke and what you're looking for in the replacement." |
| Follow-Up Opener | "David, your SaaStr session on RevOps alignment hit home. Given what you shared about tool consolidation, I think you'd find our approach to sales engagement interesting." |
| Shared Sessions | Day 2 Track B (his talk), Day 2 "Tool Consolidation" panel |
| Company News | MetricStack launched a new analytics product in January and doubled their customer base in H2 2025 |

*(6 more Tier 1 targets follow the same format)*

---

**TIER 2: HIGH-PRIORITY (11 targets)**

**3. Sarah Chen - VP of Sales, Amplify Data (amplifydata.com)**
| Field | Detail |
|-----|-----|
| Priority | Tier 2 (Gold Sponsor) |
| ICP Match | SaaS, 580 employees, Series C, US-based |
| Talk | Not speaking |
| Recent Activity | Promoted to VP of Sales 3 months ago, previously Director of Enterprise Sales |
| Icebreaker | "Congratulations on the VP promotion. Scaling from enterprise into a broader sales leadership role at a company growing as fast as Amplify must be an exciting challenge." |
| Follow-Up Opener | "Sarah, great meeting you at the Amplify booth at SaaStr. As you're building out the sales org in your new VP role, I'd love to show you how we help teams like yours scale outbound." |
| Shared Sessions | Day 1 "Women in Sales Leadership" networking lunch, Day 3 closing keynote |
| Company News | Amplify Data is a Gold Sponsor at SaaStr, recently expanded into EMEA |

*(10 more Tier 2 targets follow the same format)*

---

**TIER 3: OPPORTUNISTIC (9 targets)**

| Name | Title | Company | ICP Match | Icebreaker |
| --- | --- | --- | --- | --- |
| Tom Nakamura | Director of Sales | PipelineIQ | SaaS, 250 emp, Series A | "I saw PipelineIQ just launched the new forecasting module. How's the sales team handling the expanded pitch?" |
| Lisa Okafor | VP of Revenue | SignalPath | SaaS, 400 emp, Series B | "SignalPath's growth has been impressive. Curious what your outbound strategy looks like at your current scale." |
| *(7 more abbreviated entries)* |  |  |  |  |

---

**DAY-BY-DAY SCHEDULE**

**Day 1 (Sep 15):**
- 2:00 PM - Main Stage: Rachel Torres talk (Tier 1) - arrive early, introduce yourself after
- 3:30 PM - Visit Amplify Data booth (Tier 2, Sarah Chen)
- 5:00 PM - Networking reception: target Tier 3 contacts

**Day 2 (Sep 16):**
- 10:30 AM - Track B: David Kim talk (Tier 1) - reference his blog post in conversation
- 12:00 PM - Women in Sales Leadership lunch (Sarah Chen likely attending)
- 2:00 PM - Sponsor hall walk: visit remaining Tier 2 sponsor booths

**Day 3 (Sep 17):**
- Morning open networking: pursue remaining Tier 1 and Tier 2 contacts
- Closing keynote: good opportunity for Tier 3 casual encounters

---

**Dynamic fields for Rachel Torres:**
- `{{confprep_person_name}}`: Rachel Torres
- `{{confprep_person_title}}`: VP of Sales
- `{{confprep_company}}`: CloudFlow
- `{{confprep_priority_tier}}`: Tier 1 (Must-Meet)
- `{{confprep_icp_match_reason}}`: SaaS, 420 employees, Series C, US-based, Revenue department
- `{{confprep_talk_title}}`: Scaling Outbound at the Mid-Market: What Works in 2026
- `{{confprep_talk_relevance}}`: Directly discusses outbound sales scaling, the core use case for sales engagement software
- `{{confprep_recent_activity}}`: Guest on "The Revenue Podcast" discussing AI-powered sequencing tools
- `{{confprep_icebreaker}}`: "Your point on the podcast about AI sequencing replacing manual cadences really resonated. I'd love to hear how that's playing out at CloudFlow since you made the switch."
- `{{confprep_followup_opener}}`: "Rachel, really enjoyed your SaaStr talk on scaling outbound at the mid-market. Your point about sequence personalization at scale is exactly the problem we're solving at [Company]."
- `{{confprep_shared_sessions}}`: Day 1 Main Stage (her talk), Day 2 "Sales Tech Stack" roundtable
- `{{confprep_company_news}}`: Closed $45M Series C in Q1 2026, expanding sales team from 40 to 80 reps

Would you like me to create a lead list with all 28 targets tagged by tier?

---

### Example 2: Niche Industry Conference

**User prompt:** "I'm attending FinTech Connect in London next month. Who should I meet? We sell compliance automation to Head of Compliance and VP Risk at banks and fintech companies with 500+ employees."

**What the skill does:**
1. Asks about goal and meeting capacity. User says: "Goal is pipeline. I can do 8 meetings."
2. Calls `WebSearch` with "FinTech Connect London 2026 speakers sponsors" to find event details.
3. Calls `WebFetch` on the FinTech Connect speakers page and sponsors page.
4. Identifies 50 speakers and 20 sponsor companies.
5. Calls `mcp__claude_ai_Amplemarket__enrich_company` for all unique companies, filtering for banks and fintech with 500+ employees.
6. Finds 12 ICP-matching companies.
7. Calls `mcp__claude_ai_Amplemarket__search_people` with `person_titles`: ["Head of Compliance", "VP of Risk", "Chief Compliance Officer", "Director of Risk"], `company_domains`: [each ICP company].
8. Calls `mcp__claude_ai_Amplemarket__enrich_person` for top targets.
9. Calls `WebSearch` for each Tier 1 target to find recent regulatory news affecting their company, published thought leadership on compliance topics, and conference speaking history.
10. Produces a playbook focused on compliance and regulatory angles, with icebreakers referencing specific regulations (e.g., "With the new FCA guidelines coming into effect in Q3, I imagine your team is under pressure to automate reporting").

**Example output (abbreviated):**

---

**CONFERENCE NETWORKING PLAYBOOK: FinTech Connect London 2026**

**Summary:** 19 targets across 12 ICP-matching companies. 5 Tier 1 (speakers on compliance/risk panels), 8 Tier 2 (sponsor companies with compliance leadership), 6 Tier 3 (attendee companies).

**Tier 1 highlight:James Whitfield - Head of Compliance, NeoBank UK**
- Talk: "Automating Compliance in a Post-FCA World" (Day 1, Panel C)
- Icebreaker: "Your panel topic is exactly what we're hearing from every compliance leader right now. Curious whether NeoBank is further along on automation than most or if you're still in the evaluation phase."
- Company News: NeoBank received a conditional banking license last quarter and is ramping compliance infrastructure

---

### Example 3: User is Also Speaking

**User prompt:** "Prepare my event playbook for DevTechSummit. I'm giving a talk called 'AI Agents in the Sales Stack' on Day 2. I sell AI-powered sales tools to engineering leaders at tech companies with 100-500 employees. Goal is partnerships and pipeline. 10 meeting slots."

**What the skill does:**
1. Notes the user is speaking and records talk title and day.
2. Calls `WebSearch` and `WebFetch` for DevTechSummit speakers, sponsors, and agenda.
3. Enriches companies, filters against ICP (tech companies, 100-500 employees).
4. For each target, checks if they are attending sessions adjacent to the user's talk on the agenda.
5. Weaves the user's talk into icebreakers and follow-ups:
- Pre-event icebreaker: "I'm presenting on AI agents in the sales stack at DevTechSummit. Given your work on [related topic], would love to get your take before I finalize my examples."
- At-event icebreaker: "Thanks for coming to my session. I noticed you asked about [specific question]. Happy to go deeper on that."
- Follow-up opener: "Great connecting at DevTechSummit. After my talk on AI agents, several people mentioned [related challenge]. Curious if that resonates at [company] too."
6. Splits Tier 1 into two sub-groups: partnership targets (other speakers/companies with complementary products) and pipeline targets (ICP-matching companies with buying intent).
7. Suggests pre-event outreach: "You're speaking. Use that as social proof to book meetings before the event. Here are LinkedIn message templates for each Tier 1 target."

**Example output (abbreviated):**

---

**CONFERENCE NETWORKING PLAYBOOK: DevTechSummit 2026**

**Your Talk:** "AI Agents in the Sales Stack" - Day 2, 11:00 AM, Track A
**Goal:** Partnerships + Pipeline
**Meeting Capacity:** 10

**Summary:** 22 targets. 6 Tier 1 (3 partnership, 3 pipeline), 9 Tier 2, 7 Tier 3.

**Pre-Event Outreach Templates:**
Since you are a speaker, leverage this for pre-event meeting requests:

*For partnership targets:*
"Hi [Name], I see we're both speaking at DevTechSummit. I'm presenting on AI agents in the sales stack and noticed your talk on [their topic] covers complementary ground. Would love to grab coffee between sessions to explore potential synergies between [your company] and [their company]."

*For pipeline targets:*
"Hi [Name], I'm speaking at DevTechSummit on Day 2 about AI agents in the sales stack. Given [Company]'s growth in [relevant area], I think you'd find the session relevant. Happy to save you a seat and chat afterward."

**Tier 1 highlight (Partnership):Elena Vasquez - CTO, IntegrationHub (integrationhub.dev)**
- Talk: "Building an Open Ecosystem for Sales Tools" (Day 1, 3:00 PM)
- Partnership Angle: IntegrationHub provides the API layer many sales tools connect through, making them a natural integration partner
- Icebreaker: "Your talk on open ecosystems is right in our wheelhouse. We've been thinking about how AI agents should plug into the broader sales stack rather than replace it."

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Conference website is gated or returns empty content | Fallback chain: 1) Try `WebSearch` for "[conference name] speakers list 2026" to find third-party recaps or press releases. 2) Try `WebFetch` on alternate URLs: /speakers, /agenda, /schedule, /sponsors, /exhibitors, /partners. 3) Search LinkedIn for "[conference name]" event page. 4) Ask the user to paste the speaker/sponsor list manually if no public source is available. |
| Speaker list is incomplete or only shows keynotes | Fallback chain: 1) Search for "[conference name] full agenda" or "[conference name] breakout sessions", as breakout speakers are often on separate pages. 2) Check sponsor pages, as many sponsors have speaking slots listed on their company profiles. 3) Search for prior year agendas to identify likely repeat speakers. 4) Ask the user if they have access to an attendee app or event platform with the full list. |
| Too many speakers and sponsors to enrich (100+ companies) | Prioritize enrichment by starting with keynote speakers and top-tier sponsors (Platinum/Gold). Enrich in batches of 15-20 companies at a time. After the first batch, check ICP match rate. If fewer than 20% match, adjust ICP criteria with the user before continuing. Skip companies that are clearly outside the ICP based on name and description alone (e.g., a catering company sponsoring a tech conference). |
| No ICP-matching companies found among speakers or sponsors | Broaden the search: 1) Expand company size range by one tier in each direction. 2) Include adjacent industries from `mcp__claude_ai_Amplemarket__get_industries`. 3) Look beyond speakers and sponsors. Search for ICP-matching companies likely to attend (call `mcp__claude_ai_Amplemarket__search_companies` with ICP criteria + location matching the conference city). 4) Check if the conference publishes an attendee or exhibitor directory. |
| WebSearch returns outdated information from prior year | Verify the year in all sources. Add the current year to search queries (e.g., "SaaStr Annual 2026 speakers" not just "SaaStr Annual speakers"). Cross-reference speaker names with `mcp__claude_ai_Amplemarket__enrich_person` to confirm they still hold the listed title and company, since people change roles between conference announcements and event dates. |
| Person enrichment returns sparse data for a speaker | Fallback chain: 1) Try `mcp__claude_ai_Amplemarket__enrich_person` with LinkedIn URL if available from the conference website. 2) Try searching by name + company via `mcp__claude_ai_Amplemarket__search_people`. 3) Use `WebSearch` for "[person name] [company] LinkedIn" to find their profile URL. 4) If person data remains sparse, rely on company-level data and talk topic for personalization. A strong icebreaker about their conference talk does not require deep personal enrichment. |
| User's meeting capacity is too low for the number of Tier 1 targets | Re-rank Tier 1 targets by ICP match strength and talk relevance. Move the lowest-ranked Tier 1 targets to Tier 2. Suggest the user prioritize pre-event outreach for Tier 1 targets and use casual hallway conversations for Tier 2. If the user is speaking, their talk itself is a leverage multiplier, as targets may approach them, effectively increasing capacity. |