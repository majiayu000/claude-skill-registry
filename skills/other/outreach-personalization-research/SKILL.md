---
name: outreach-personalization-research
description: >
  Research a prospect deeply and generate actionable personalization angles with draft opening lines for cold outreach.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Outreach & Personalization"
compatibility: Requires Amplemarket MCP server
---

# Outreach Personalization Research

Research a prospect deeply and generate actionable personalization angles with draft opening lines for cold outreach.

## Instructions

When a user wants to personalize outreach to a specific prospect, gather rich context and synthesize it into concrete angles and openers.

### Steps

1. **Identify the prospect.** Extract any available identifiers from the user's request:
    - LinkedIn URL
    - Email address
    - Name + company
    If the user provides minimal info, ask for at least a name and company or a LinkedIn URL.
2. **Enrich the person** by calling `mcp__claude_ai_Amplemarket__enrich_person` with all available identifiers. Set `reveal_email` to `true` for contact details. **Credit note:** Enabling `reveal_email` and `reveal_phone_numbers` consumes additional Amplemarket credits per reveal. Key data points to extract:
    - Current title and role
    - Career history and previous companies
    - Education and schools
    - Skills and endorsements
    - Location
3. **Enrich the company** by calling `mcp__claude_ai_Amplemarket__enrich_company` with the company `domain` or `linkedin_url`. Key data points to extract:
    - Industry and sub-industry
    - Company size and growth trajectory
    - Tech stack and tools used
    - Company description and value proposition
    - Headquarters and locations
    - Recent funding or milestones
4. **Search for additional context** by calling `mcp__claude_ai_Amplemarket__search_people` with `company_domains`: [prospect's company domain], `person_seniorities` matching the prospect's level, `page_size`: 5 to understand the team structure around them.
5. **Identify personalization angles.** Analyze the enriched data to find 3-5 angles from these categories:
    - **Role-based:** Pain points specific to their title and department (e.g., a VP of Sales likely cares about pipeline velocity)
    - **Company stage:** Tailor to their company size and growth phase (startup vs. enterprise challenges)
    - **Career trajectory:** Reference a recent role change, promotion, or career milestone
    - **Tech stack:** Mention specific tools they use and how your solution integrates or compares
    - **Industry trends:** Connect to challenges or opportunities in their specific industry
    - **Shared context:** Same alma mater, previous company, mutual connections, shared geography
    - **Company news:** Recent funding, product launches, hiring sprees, or expansions
    - **Team structure:** Reference their team size or recent hires in their department
6. **Draft opening lines.** For each angle, write a concise, natural-sounding opening line (1-2 sentences) that:
    - Demonstrates specific research (not generic)
    - Connects to a plausible pain point or interest
    - Feels human, not templated
    - Avoids being sycophantic or over-the-top
7. **Format the output** as a Personalization Brief:
    
    **Prospect Summary** (one-paragraph context)
    
    **Personalization Angles** (3-5 angles, each with):
    
    - Angle name and category
    - Supporting data point from enrichment
    - Draft opening line
    - Strength rating (Strong / Medium / Soft)
    
    **Recommended Best Angle** with reasoning
    
    **Contact Details** for executing the outreach
    

### Important Notes

- Quality over quantity: 3 strong angles are better than 5 weak ones.
- Never fabricate data points. Only use information returned from the enrichment APIs.
- If enrichment data is sparse, be transparent about it and focus angles on the data that is available.
- Adapt tone guidance if the user specifies their outreach style (formal, casual, humorous).

## Examples

### Example 1: LinkedIn URL Personalization

**User prompt:** "Help me personalize outreach to linkedin.com/in/sarah-chen-vp-marketing"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `linkedin_url`: "https://linkedin.com/in/sarah-chen-vp-marketing", `reveal_email`: true.
2. Calls `mcp__claude_ai_Amplemarket__enrich_company` with domain extracted from enrichment.
3. Calls `mcp__claude_ai_Amplemarket__search_people` with the company domain and seniority filter to understand team structure.
4. Synthesizes angles and drafts openers.

**Example output:**

---

**PERSONALIZATION BRIEF: Sarah Chen**

**Prospect Summary**
Sarah Chen is the VP of Marketing at CloudMetrics (cloudmetrics.io), a Series B cloud analytics company with 180 employees based in Austin, TX. She joined 8 months ago from HubSpot where she was a Senior Director of Demand Gen. She holds an MBA from Wharton. CloudMetrics recently raised a $45M Series B and appears to be scaling their go-to-market team.

**Personalization Angles**

**1. New Role, New Strategy (Career Trajectory) - Strong**
Data: Sarah joined CloudMetrics 8 months ago as VP Marketing, coming from HubSpot.
Opening line: "Sarah, transitioning from a marketing powerhouse like HubSpot to lead marketing at a Series B company is a big shift. I imagine you are rebuilding the demand gen playbook from scratch rather than inheriting one."

**2. Post-Funding Growth (Company News) - Strong**
Data: CloudMetrics raised $45M Series B; headcount grew from 120 to 180 in 6 months.
Opening line: "With CloudMetrics' recent Series B and the team nearly doubling, I'd guess the pressure to scale pipeline in lockstep with headcount growth is very real right now."

**3. Tech Stack Gap (Technology) - Medium**
Data: CloudMetrics uses Salesforce, Marketo, and Google Analytics but no ABM or intent data platform detected.
Opening line: "I noticed CloudMetrics is running Marketo and Salesforce but doesn't seem to have an intent data layer yet. Curious if that's on your roadmap as you scale outbound."

**4. Team Building (Team Structure) - Medium**
Data: Search shows 3 marketing hires in the last 3 months, all junior/mid-level.
Opening line: "Looks like you have been building out the marketing team quickly at CloudMetrics. When you are scaling a team that fast, having the right tooling in place before the team outgrows it can save a lot of rework."

**5. Wharton Connection (Shared Context) - Soft**
Data: Sarah holds an MBA from Wharton.
Opening line: "Fellow Wharton alum here. Saw you are leading marketing at CloudMetrics and wanted to reach out."
(Only use if sender is also a Wharton alum.)

**Recommended Best Angle:** Angle 1 (New Role) or Angle 2 (Post-Funding Growth). Both are timely, specific, and connect to real pain points. Combine them for maximum impact.

**Contact Details**
- Email: sarah.chen@cloudmetrics.io
- LinkedIn: linkedin.com/in/sarah-chen-vp-marketing
- Location: Austin, TX

---

### Example 2: Name + Company Personalization

**User prompt:** "Find personalization angles for James Park, CTO at Notion"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `name`: "James Park", `company_name`: "Notion", `reveal_email`: true.
2. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "notion.so".
3. Searches for engineering leadership context at Notion.
4. Returns personalization brief with CTO-specific angles (technical challenges, engineering team growth, infrastructure decisions).

### Example 3: Personalization with Style Guidance

**User prompt:** "Write an opener for maria@finova.io - keep it casual and short"

**What the skill does:**
1. Enriches Maria via email.
2. Enriches finova.io.
3. Generates angles with casual, concise opening lines (1 sentence max, conversational tone).

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Very sparse enrichment data | Fallback chain: 1) Try additional identifiers (LinkedIn URL, company domain) to improve match quality. 2) Focus angles on company-level data (industry, size, funding, hiring signals) when person data is thin. 3) Search for the prospect's peers at the same company to infer team structure and role context. 4) Be transparent: "Limited data on this person. Angles are based primarily on company signals." |
| No email found | Suggest LinkedIn InMail or connection request. Provide the draft opener adapted for LinkedIn format. |
| Angles feel generic | Ensure you are pulling specific data points. If enrichment is thin, recommend the user share any additional context they have about the prospect. |
| User wants more angles | Search for the prospect's content (posts, articles) or expand the company enrichment to find additional data points. |
| Wrong person enriched | Verify with the user by confirming title and company. Fallback: use `company_domain` instead of `company_name` for disambiguation, or ask for LinkedIn URL for exact match. |
| Person enrichment succeeds but company enrichment fails | Fallback chain: 1) Try `enrich_company` with domain instead of name. 2) Try LinkedIn company URL. 3) Use person-level data for role-based and career trajectory angles, and note: "Company data unavailable. Angles focus on the prospect's career and role." |
| Multiple people match the same name + company | Present all matches with titles and LinkedIn URLs. Ask the user to confirm before generating angles. Never generate personalization for the wrong person. |
| Company exists but `search_companies` returns 0 results | Fallback chain: 1) Try `enrich_company` with domain directly. 2) Try the LinkedIn company URL. 3) Try parent company domain. Some companies are enrichable by domain but not searchable by name. |