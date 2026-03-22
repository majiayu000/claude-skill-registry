---
name: pre-call-research-brief
description: >
  Generate a comprehensive, structured research brief before any sales call by combining person enrichment, company intelligence, CRM history, web research, and competitive analysis into a single actionable document.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Outreach & Personalization"
compatibility: Requires Amplemarket MCP server
---

# Pre-Call Research Brief

Generate a comprehensive, structured research brief before any sales call by combining person enrichment, company intelligence, CRM history, web research, and competitive analysis into a single actionable document.

## Instructions

When a user wants to prepare for a sales call, gather deep context from every available source and synthesize it into an 8-section brief with talking points, landmines, and dynamic personalization fields.

### Steps

1. **Gather call context from the user.** Ask these 5 questions if the information is not already provided:
    - Who is the call with? (name, LinkedIn URL, or email address)
    - What company are they at? (name or domain)
    - What type of call is this? (discovery / demo / negotiation / renewal / expansion)
    - What is your product or solution? (brief description so talking points are relevant)
    - Any specific topics or concerns you want researched? (optional)
    
    If the user provides most of this context upfront, skip the questions that are already answered and only ask for what is missing. At minimum you need the person identifier and the call type to proceed.
    
2. **Person research.** Run these in parallel:
    - Call `mcp__claude_ai_Amplemarket__enrich_person` with all available identifiers (`linkedin_url`, `email`, or `name` + `company_name`). Set `reveal_email` to `true`. Extract: current title, career history, education, skills, location, social profiles.
    - Call `WebSearch` for the person's name + company to find recent activity: blog posts, podcast appearances, conference talks, LinkedIn posts, press quotes, and interviews.
    - Call `WebFetch` on the 2-3 most relevant URLs from the search results to extract detailed content (quotes, topics discussed, positions taken).
    
    Key data to capture: career trajectory, communication style clues (formal vs. casual from their writing), topics they care about publicly, recent role changes.
    
3. **Company research.** Run these in parallel:
    - Call `mcp__claude_ai_Amplemarket__enrich_company` with the company `domain` or `linkedin_url`. Extract: industry, employee count, revenue range, tech stack, headquarters, funding history, description.
    - Call `WebSearch` for the company name + "news" to find: recent funding rounds, product launches, leadership changes, partnerships, acquisitions, layoffs, earnings reports.
    - Call `WebFetch` on the 2-3 most relevant news articles to extract details.
    
    Key data to capture: growth trajectory, recent strategic moves, public challenges, market positioning.
    
4. **CRM context (if HubSpot is connected).** This step degrades gracefully if HubSpot is unavailable.
    - Call `mcp__claude_ai_HubSpot__get_user_details` to verify the connection and check permissions.
    - If connected, call `mcp__claude_ai_HubSpot__search_crm_objects` with `object_type`: "contacts" and filter by the prospect's email to find existing contact records.
    - Call `mcp__claude_ai_HubSpot__search_crm_objects` with `object_type`: "deals" and filter by the company name or associated contact to find deal history.
    - Call `mcp__claude_ai_HubSpot__get_crm_objects` for each deal ID to retrieve full deal details: stage, amount, close date, associated notes, and activity timeline.
    - Summarize: total deals, won/lost/open, last interaction date, key notes from previous conversations, assigned owner.
    
    If HubSpot is not connected or the call fails, skip this step entirely and omit the CRM History section from the brief. Do not prompt the user to connect HubSpot.
    
5. **Competitive context.** Run these in parallel:
    - Call `WebSearch` for the company name + "uses" or "tech stack" or "tools" to find what software and competitors they currently use.
    - Cross-reference the tech stack data from `enrich_company` (step 3) with known competitors to your user's product.
    - Identify potential displacement opportunities (tools they use that your product replaces) and integration angles (tools they use that your product complements).
6. **Team context.** Call `mcp__claude_ai_Amplemarket__search_people` with:
    - `company_domains`: [prospect's company domain]
    - `person_seniorities`: matching and adjacent to the prospect's level (e.g., if prospect is VP, search for C-Suite, VP, and Director)
    - `page_size`: 10
    - `full_output`: true
    
    Map the organizational structure around the prospect: who they report to, who reports to them, peers in adjacent functions. This helps identify multi-threading opportunities and internal champions or blockers.
    
7. **Synthesize the brief** into 8 sections:
    
    **Section 1: Executive Summary** (1 paragraph)
    A concise overview of who you are meeting, what their company does, the call type, and the 2-3 most important things to know going in.
    
    **Section 2: Person Profile**
    
    - Current role and tenure
    - Career highlights (previous companies, promotions, notable achievements)
    - Recent public activity (posts, talks, articles, podcast appearances)
    - Communication style clues (inferred from their public content)
    - Education and notable affiliations
    
    **Section 3: Company Snapshot**
    
    - Firmographics (industry, size, revenue, location, founding year)
    - Funding and financial status
    - Recent developments (last 6 months of news)
    - Growth trajectory (hiring trends, expansion signals)
    - Tech stack overview
    
    **Section 4: CRM History** (skip entirely if HubSpot is not connected)
    
    - Previous deals and their outcomes
    - Engagement timeline (emails, meetings, calls)
    - Key notes from past conversations
    - Current deal stage and next steps if applicable
    
    **Section 5: Talking Points** (3-5 points tailored to the call type)
    
    - Discovery: focus on uncovering pain points, understanding their current state, qualifying fit
    - Demo: focus on their specific use cases, mapping features to their needs, addressing likely objections
    - Negotiation: focus on value quantification, competitive differentiation, urgency drivers
    - Renewal: focus on ROI achieved, usage patterns, satisfaction signals, expansion opportunities
    - Expansion: focus on new use cases, additional teams, complementary products, increased volume
    
    **Section 6: Landmines to Avoid**
    Sensitive topics to steer clear of: recent layoffs, bad press, failed products, executive departures, lawsuits, controversial company decisions. Sourced from web research. If no landmines are found, state that explicitly.
    
    **Section 7: Questions to Ask** (3-5 insightful questions)
    Questions that demonstrate you did your research and open up valuable conversation threads. Tailored to the call type and informed by the research findings.
    
    **Section 8: Competitive Intel**
    Known tools and platforms the company uses. Potential displacement targets. Integration angles. Competitive positioning notes relevant to the conversation.
    
8. **Generate dynamic fields.** After the brief, output a Dynamic Fields Reference table with 17+ fields and their values. These can be copied into templates, CRM notes, or follow-up emails:
    
    
    | Field | Value | Source |
    | --- | --- | --- |
    | `{{brief_person_name}}` | [full name] | enrich_person |
    | `{{brief_person_title}}` | [current title] | enrich_person |
    | `{{brief_company_name}}` | [company name] | enrich_company |
    | `{{brief_company_stage}}` | [funding stage and amount] | enrich_company + WebSearch |
    | `{{brief_company_size}}` | [employee count] | enrich_company |
    | `{{brief_recent_news}}` | [most notable recent development] | WebSearch |
    | `{{brief_career_highlight}}` | [most relevant career detail] | enrich_person |
    | `{{brief_podcast_mention}}` | [podcast or talk appearance] | WebSearch |
    | `{{brief_blog_post}}` | [recent article or post] | WebSearch |
    | `{{brief_tech_stack}}` | [key tools and platforms] | enrich_company |
    | `{{brief_competitor_used}}` | [relevant competitor tool] | WebSearch |
    | `{{brief_crm_history}}` | [deal history summary] | HubSpot CRM |
    | `{{brief_talking_point_1}}` | [first talking point] | Analysis |
    | `{{brief_talking_point_2}}` | [second talking point] | Analysis |
    | `{{brief_talking_point_3}}` | [third talking point] | Analysis |
    | `{{brief_question_1}}` | [first research-backed question] | Analysis |
    | `{{brief_question_2}}` | [second research-backed question] | Analysis |
    | `{{brief_landmine}}` | [primary landmine to avoid] | WebSearch |
    | `{{brief_followup_opener}}` | [suggested follow-up email opener] | Analysis |
    
    If a field has no data available, set its value to "Not available" and note the reason.
    
9. **Offer follow-up actions.** After delivering the brief, ask the user:
    - "Would you like me to draft a follow-up email template based on this brief?"
    - "Want me to create a pre-call agenda you can share with the prospect?"
    - "Should I research any of these topics more deeply?"

### Important Notes

- Never fabricate data. If enrichment or web research returns no results for a data point, explicitly state "Not found" or "No data available" rather than inventing plausible-sounding information. Fabricated data in a pre-call brief can destroy credibility in seconds.
- Clearly label sources for every data point. Use inline annotations like (Source: Amplemarket enrichment), (Source: TechCrunch, Jan 2026), or (Source: HubSpot CRM) so the user knows what to trust and what to verify.
- If HubSpot is not connected, skip the CRM History section gracefully. Do not display an empty section or error message. Simply omit Section 4 and renumber nothing. The user understands not all sections apply every time.
- Warn about credit costs upfront. Before running enrichments, inform the user: "This brief will use Amplemarket enrichment credits for person and company data. Enabling email and phone reveals consumes additional credits. Proceed?" Wait for confirmation before calling enrichment APIs.
- Distinguish verified data from web research. Enrichment data from Amplemarket is structured and verified. Web search results are unverified and may be outdated or inaccurate. Flag web-sourced data points with a note like "[Web research - verify before citing]" when the source is not a highly authoritative outlet.
- Prioritize quality over speed. It is better to deliver a brief with 5 high-confidence data points than 15 uncertain ones. If web searches return thin results, focus the brief on the strong enrichment data and be transparent about gaps.

## Examples

### Example 1: Full Pre-Call Brief for a Discovery Call

**User prompt:** "Prep me for a call with Sarah Chen, VP of Marketing at CloudMetrics. It's a discovery call. We sell an AI-powered sales engagement platform."

**What the skill does:**
1. Skips the intake questions since the user provided person, company, call type, and product.
2. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `name`: "Sarah Chen", `company_name`: "CloudMetrics", `reveal_email`: true.
3. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "cloudmetrics.io".
4. Calls `WebSearch` for "Sarah Chen CloudMetrics" and "CloudMetrics news 2026".
5. Calls `WebFetch` on relevant results (podcast appearance, funding announcement).
6. Calls `mcp__claude_ai_HubSpot__get_user_details` to check HubSpot connection.
7. Calls `mcp__claude_ai_HubSpot__search_crm_objects` for deals associated with CloudMetrics.
8. Calls `mcp__claude_ai_Amplemarket__search_people` at cloudmetrics.io for org context.
9. Calls `WebSearch` for "CloudMetrics tech stack" and "CloudMetrics tools".
10. Synthesizes all data into the 8-section brief.

**Example output:**

---

**PRE-CALL RESEARCH BRIEFCall:** Discovery | **Date:** March 10, 2026
**Prospect:** Sarah Chen, VP of Marketing @ CloudMetrics
**Prepared for:** [Your Name] | **Your Solution:** AI-powered sales engagement platform

---

**1. Executive Summary**

You are meeting with Sarah Chen, VP of Marketing at CloudMetrics, a Series B cloud analytics company based in Austin, TX with approximately 180 employees. Sarah joined CloudMetrics 8 months ago from HubSpot, where she spent 4 years as Senior Director of Demand Gen. CloudMetrics raised a $45M Series B in July 2025 and has been aggressively scaling their go-to-market team. This is a discovery call. Focus on understanding how their current outbound and demand gen processes are keeping up with their rapid growth, and whether their existing tooling can scale with them.

**2. Person Profile**

- **Current Role:** VP of Marketing at CloudMetrics (joined July 2025) (Source: Amplemarket enrichment)
- **Previous Role:** Senior Director of Demand Gen at HubSpot (2021-2025) (Source: Amplemarket enrichment)
- **Earlier Career:** Marketing Manager at Drift (2018-2021), Marketing Coordinator at Salesforce (2016-2018) (Source: Amplemarket enrichment)
- **Education:** MBA, Wharton School of Business; BS Marketing, University of Texas at Austin (Source: Amplemarket enrichment)
- **Recent Activity:**
    - Guest on the "SaaS Metrics Podcast" (Episode 142, January 2026). Discussed the challenges of building a demand gen engine at a scaling startup vs. an established company. Key quote: "The biggest mistake I see is teams trying to copy enterprise playbooks into a Series B environment." [Web research - verify before citing] (Source: SaaS Metrics Podcast, Jan 2026)
    - Published an article on LinkedIn: "Why Your Demand Gen Strategy Needs to Break Before It Scales" (February 2026). Argued that most marketing teams over-invest in top-of-funnel before they have mid-funnel conversion figured out. [Web research - verify before citing] (Source: LinkedIn, Feb 2026)
    - Spoke at SaaStr Annual 2025 on "From HubSpot to Startup: Resetting Your Marketing Assumptions" (Source: WebSearch, SaaStr event page)
- **Communication Style Clues:** Based on her podcast appearance and LinkedIn writing, Sarah communicates directly, uses data to support arguments, and has low patience for generic vendor pitches. She values practitioners who understand the nuances of scaling. Expect her to push back on claims that are not backed by specifics.

**3. Company Snapshot**

- **Company:** CloudMetrics (cloudmetrics.io) (Source: Amplemarket enrichment)
- **Industry:** Cloud Analytics / Business Intelligence (Source: Amplemarket enrichment)
- **Founded:** 2020 (Source: Amplemarket enrichment)
- **Headquarters:** Austin, TX (Source: Amplemarket enrichment)
- **Employees:** ~180 (up from ~120 six months ago) (Source: Amplemarket enrichment)
- **Revenue Range:** $15M-$25M ARR (estimated) (Source: Amplemarket enrichment)
- **Funding:** Series B, $45M raised in July 2025 led by Insight Partners. Total funding: $62M. (Source: Amplemarket enrichment + TechCrunch, Jul 2025)
- **Recent Developments:**
    - Launched a new self-serve analytics dashboard in February 2026 targeting mid-market customers (Source: CloudMetrics blog, Feb 2026)
    - Opened a second office in New York City in January 2026 (Source: LinkedIn company page)
    - Hired a new CRO, Marcus Webb (ex-Datadog), in November 2025 (Source: CloudMetrics press release, Nov 2025)
    - Named to G2's "Best Analytics Tools 2026" list (Source: G2, Jan 2026)
- **Tech Stack:** Salesforce, Marketo, Snowflake, Google Analytics, Intercom, Slack, AWS (Source: Amplemarket enrichment)
- **Growth Trajectory:** Aggressive. 50% headcount growth in 6 months, new CRO hire, second office, product expansion into self-serve. Classic post-Series B scaling pattern.

**4. CRM History**

- **Previous Deals:** 2 deals on record (Source: HubSpot CRM)
    - Deal 1: "CloudMetrics - Pilot" | Created: March 2025 | Amount: $18,000 | Stage: Closed-Lost (June 2025) | Loss Reason: "Timing - post-fundraise priorities shifted" | Owner: Jamie Rodriguez
    - Deal 2: "CloudMetrics - Inbound Demo Request" | Created: September 2025 | Amount: $45,000 | Stage: Closed-Lost (November 2025) | Loss Reason: "Went with Outreach - pricing" | Owner: Jamie Rodriguez
- **Engagement Timeline:** 14 emails sent across both deals, 9 opens, 2 replies, 1 meeting held (demo in Oct 2025). No activity since November 2025.
- **Key Notes:** From Jamie's notes on Deal 2: "Sarah was not involved in previous eval. Decision was made by the former Head of Sales Ops (now departed). Sarah mentioned on the demo that she 'inherited the Outreach decision and is not fully bought in.' Worth re-engaging in Q1 2026."
- **Important:** Sarah herself indicated dissatisfaction with the current tool. This is a warm re-engagement, not a cold discovery.

**5. Talking Points**

1. **Inherited tool stack, fresh perspective.** Sarah did not choose Outreach. She inherited it. Reference her podcast quote about not copying enterprise playbooks into a startup environment. Ask whether Outreach fits CloudMetrics' current go-to-market motion or was chosen for a different stage. (Source: CRM notes + SaaS Metrics Podcast)
2. **Post-Series B scaling pressure.** CloudMetrics grew 50% in 6 months and hired a new CRO. The demand gen engine needs to scale with the team. Explore whether their current tooling is creating bottlenecks as they add reps and expand into self-serve. (Source: Amplemarket enrichment + WebSearch)
3. **Self-serve product launch = new pipeline motion.** The February 2026 self-serve dashboard launch likely requires a different go-to-market approach (PLG + outbound hybrid). Ask how her team's workflow is adapting to support both enterprise and self-serve motions simultaneously. (Source: CloudMetrics blog, Feb 2026)
4. **Marketing-sales alignment with new CRO.** With Marcus Webb (ex-Datadog) joining as CRO in November, there is likely a re-evaluation of the entire revenue tech stack happening. Position your platform as part of that strategic review. (Source: CloudMetrics press release, Nov 2025)
5. **Data-driven decision maker.** Sarah's LinkedIn article and podcast appearance both emphasize data-driven approaches and mid-funnel conversion metrics. Lead with analytics, attribution, and measurable outcomes rather than feature lists. (Source: LinkedIn + SaaS Metrics Podcast)

**6. Landmines to Avoid**

- **Previous deal losses.** Do not lead with "I know we've talked before". Let Sarah bring it up. She may not be aware of the full history with Jamie Rodriguez. If she does reference it, acknowledge it without being defensive about the pricing loss. (Source: HubSpot CRM)
- **Outreach comparison.** Avoid unprompted bashing of Outreach. Sarah said she is "not fully bought in" but that does not mean she wants to hear a competitive teardown. Let her articulate the gaps herself. (Source: HubSpot CRM notes)
- **Engineering layoffs.** CloudMetrics quietly laid off 12 engineers in January 2026 as part of a "refocusing" according to a Blind post. Do not bring this up. It may be a sensitive internal topic and the source is unverified. [Web research - verify before citing] (Source: Blind, Jan 2026)

**7. Questions to Ask**

1. "You mentioned on SaaS Metrics Podcast that startup teams should not copy enterprise playbooks. How has that philosophy shaped how you are building the demand gen engine at CloudMetrics?" (Source: SaaS Metrics Podcast, Jan 2026)
2. "With the new self-serve dashboard launch, how is your team balancing the PLG motion with traditional outbound? Are those separate workflows or integrated?" (Source: CloudMetrics blog, Feb 2026)
3. "Now that Marcus Webb has been CRO for a few months, are there any changes in how marketing and sales are collaborating on pipeline generation?" (Source: CloudMetrics press release, Nov 2025)
4. "What does your current demand gen tech stack look like, and where are the biggest friction points as you scale?" (Source: Discovery best practice)
5. "If you could change one thing about how your team generates and converts pipeline today, what would it be?" (Source: Discovery best practice)

**8. Competitive Intel**

- **Current Sales Engagement:** Outreach (adopted pre-Sarah, previous Head of Sales Ops decision). Sarah has expressed she is "not fully bought in." (Source: HubSpot CRM notes)
- **Marketing Automation:** Marketo (Source: Amplemarket enrichment)
- **CRM:** Salesforce (Source: Amplemarket enrichment)
- **Analytics:** Snowflake + Google Analytics (Source: Amplemarket enrichment)
- **Customer Comms:** Intercom (Source: Amplemarket enrichment)
- **Displacement Opportunity:** Outreach is the primary displacement target. Key angles: AI-native vs. legacy architecture, better Marketo/Salesforce integration, pricing that scales with a growing team, unified analytics across marketing and sales engagement.
- **Integration Angle:** Position deep Salesforce and Marketo integrations as a strength. CloudMetrics already relies on both and will not rip those out.
- **Competitive Risk:** Outreach may offer aggressive renewal pricing to retain. Salesloft is also likely in consideration if they are evaluating alternatives.

---

**Dynamic Fields Reference**

| Field | Value | Source |
| --- | --- | --- |
| `{{brief_person_name}}` | Sarah Chen | enrich_person |
| `{{brief_person_title}}` | VP of Marketing | enrich_person |
| `{{brief_company_name}}` | CloudMetrics | enrich_company |
| `{{brief_company_stage}}` | Series B, $45M raised (July 2025) | enrich_company + WebSearch |
| `{{brief_company_size}}` | ~180 employees | enrich_company |
| `{{brief_recent_news}}` | Launched self-serve analytics dashboard (Feb 2026) | WebSearch |
| `{{brief_career_highlight}}` | Senior Director of Demand Gen at HubSpot (4 years) | enrich_person |
| `{{brief_podcast_mention}}` | Guest on SaaS Metrics Podcast (Jan 2026), discussed PLG growth | WebSearch |
| `{{brief_blog_post}}` | "Why Your Demand Gen Strategy Needs to Break Before It Scales" (LinkedIn, Feb 2026) | WebSearch |
| `{{brief_tech_stack}}` | Salesforce, Marketo, Snowflake, Google Analytics, Intercom | enrich_company |
| `{{brief_competitor_used}}` | Outreach (sales engagement - inherited, not fully bought in) | HubSpot CRM + WebSearch |
| `{{brief_crm_history}}` | 2 previous deals, both closed-lost (Jun 2025, Nov 2025) | HubSpot CRM |
| `{{brief_talking_point_1}}` | Inherited Outreach - she did not choose it, fresh eval opportunity | Analysis |
| `{{brief_talking_point_2}}` | Post-Series B scaling pressure on go-to-market team | Analysis |
| `{{brief_talking_point_3}}` | Self-serve launch requires new pipeline motion | Analysis |
| `{{brief_question_1}}` | How has your "no enterprise playbook" philosophy shaped demand gen here? | Analysis |
| `{{brief_question_2}}` | How are you balancing PLG and outbound workflows? | Analysis |
| `{{brief_landmine}}` | Do not mention January 2026 engineering layoffs (unverified, sensitive) | WebSearch |
| `{{brief_followup_opener}}` | Great speaking today, Sarah. Following up on our conversation about scaling demand gen at CloudMetrics | Analysis |

---

### Example 2: Demo Call with Existing CRM History

**User prompt:** "I have a demo with Alex Rivera, Head of Revenue Operations at FinFlow tomorrow. We're showing them our analytics dashboard."

**What the skill does:**
1. Identifies: person = Alex Rivera, company = FinFlow, call type = demo, product = analytics dashboard.
2. Enriches Alex Rivera and FinFlow via Amplemarket.
3. Searches web for Alex Rivera's activity and FinFlow news.
4. Pulls CRM history from HubSpot, which includes an open deal in "Demo Scheduled" stage with 3 previous touchpoints.
5. Searches for RevOps peers at FinFlow to understand team structure.
6. Researches FinFlow's current analytics tools for competitive context.
7. Generates the 8-section brief tailored to a demo call: talking points focus on mapping features to FinFlow's specific use cases, questions probe for technical requirements and evaluation criteria, competitive intel highlights the tools the dashboard would replace.

**Key differences from a discovery brief:**
- Talking points are feature-mapped rather than exploratory
- Questions focus on evaluation criteria, timeline, and decision process
- CRM section highlights the engagement journey leading to this demo
- Landmines include any previous objections or concerns noted in CRM

### Example 3: Renewal Call with Expansion Opportunity

**User prompt:** "Meeting prep for my renewal call with David Kim, CTO at NexaHealth. Their contract is up next month and I want to expand to their European team."

**What the skill does:**
1. Identifies: person = David Kim, company = NexaHealth, call type = renewal + expansion.
2. Enriches David Kim and NexaHealth via Amplemarket.
3. Pulls extensive CRM history, including the active deal, usage data, support tickets, and NPS scores.
4. Searches for NexaHealth's European expansion news and any new offices or hires in EMEA.
5. Searches for David Kim's peers and reports to identify who leads the European team.
6. Researches NexaHealth's European competitors and any region-specific tool requirements (GDPR compliance, data residency).
7. Generates the 8-section brief tailored to renewal + expansion: talking points emphasize ROI delivered, usage growth, and European team needs. Questions probe for expansion decision criteria and European team structure. Competitive intel covers EMEA-specific alternatives.

**Key differences from a discovery brief:**
- Executive summary leads with the relationship history and expansion opportunity
- Person profile includes interaction history, not just public research
- Talking points center on ROI achieved and scaling to new teams
- Questions probe for European team needs, compliance requirements, and budget process
- Competitive intel shifts to EMEA-specific alternatives that might have local advantages

## Troubleshooting

| Problem | Solution |
| --- | --- |
| HubSpot not connected | Graceful degradation: skip CRM History (Section 4) entirely. Do not show an error or empty section. Add a note at the end of the brief: "CRM history not available. HubSpot integration not detected. Connect HubSpot for deal history, engagement timelines, and notes from previous conversations." The remaining 7 sections should still provide a comprehensive brief. |
| Sparse person data from enrichment | Fallback chain: 1) Try alternative identifiers. If you used name + company, try LinkedIn URL or email instead. 2) Lean heavily on WebSearch for the person's public activity (LinkedIn posts, conference talks, articles, podcast appearances). 3) Use company-level data and role-based assumptions to fill gaps. 4) Be transparent in the brief: "Limited person data available. Profile sections are based primarily on web research and role-based analysis." |
| No recent news found for the company | State this explicitly in the Company Snapshot: "No significant news coverage found in the last 6 months." Shift focus to enrichment data (funding history, employee growth trends, tech stack changes). Check the company's own blog and press page via WebFetch as a secondary source. |
| Person has a common name (disambiguation) | If `enrich_person` returns results that do not match the expected company or title, do not proceed with bad data. Ask the user: "I found multiple matches for [name]. Can you confirm their LinkedIn URL or email for an exact match?" If the user cannot provide it, use `company_domain` as a filter and present the best match with a confidence note. |
| enrich_person returns the wrong person | Verify the returned profile against the user's description (company, title). If it does not match: 1) Re-try with LinkedIn URL if available. 2) Try with email address. 3) Try with `company_domain` instead of `company_name`. 4) If still wrong, inform the user and build the brief from web research and company enrichment only, noting: "Person enrichment returned an incorrect match. Person profile is based on web research only." |
| WebFetch blocked or returns errors | Some websites block automated fetching. Fallback: 1) Use the WebSearch snippet text, which often contains enough context. 2) Try fetching the Google Cache version. 3) Note in the brief which sources could not be fully accessed: "[Article could not be fully retrieved - summary based on search snippet]." |
| Rate limiting on batch enrichment | If you hit rate limits when enriching multiple people in the team context step (step 6), reduce the `page_size` to 5 and prioritize the prospect's direct reports and manager. Inform the user: "Rate limits reached. Team context is based on a smaller sample. I can research additional team members separately if needed." |

## Dynamic Fields Reference

The following fields are generated with every brief. Use them in email templates, CRM updates, or follow-up sequences.

| Field | Example Value | Source |
| --- | --- | --- |
| `{{brief_person_name}}` | "Sarah Chen" | enrich_person |
| `{{brief_person_title}}` | "VP of Marketing" | enrich_person |
| `{{brief_company_name}}` | "CloudMetrics" | enrich_company |
| `{{brief_company_stage}}` | "Series B, $45M raised" | enrich_company + WebSearch |
| `{{brief_company_size}}` | "180 employees" | enrich_company |
| `{{brief_recent_news}}` | "Launched new analytics dashboard in Feb 2026" | WebSearch |
| `{{brief_career_highlight}}` | "Previously Senior Director at HubSpot for 4 years" | enrich_person |
| `{{brief_podcast_mention}}` | "Guest on SaaS Metrics Podcast, discussed PLG growth" | WebSearch |
| `{{brief_blog_post}}` | "Published article on demand gen scaling challenges" | WebSearch |
| `{{brief_tech_stack}}` | "Salesforce, Marketo, Snowflake" | enrich_company |
| `{{brief_competitor_used}}` | "Currently using Outreach for sales engagement" | WebSearch |
| `{{brief_crm_history}}` | "2 previous deals, last closed-lost Q3 2025" | HubSpot CRM |
| `{{brief_talking_point_1}}` | "Their recent product launch creates new pipeline needs" | Analysis |
| `{{brief_talking_point_2}}` | "Post-Series B scaling pressure on go-to-market team" | Analysis |
| `{{brief_talking_point_3}}` | "Team grew 50% in 6 months - tooling may be outpaced" | Analysis |
| `{{brief_question_1}}` | "How has the team's workflow changed since the Series B?" | Analysis |
| `{{brief_question_2}}` | "What's your biggest challenge scaling demand gen now?" | Analysis |
| `{{brief_landmine}}` | "Avoid mentioning recent layoffs in engineering (Jan 2026)" | WebSearch |
| `{{brief_followup_opener}}` | "Great speaking today. Following up on the analytics discussion" | Analysis |