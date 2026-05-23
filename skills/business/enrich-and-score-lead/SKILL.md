---
name: enrich-and-score-lead
description: >
  Enrich a single prospect using any available identifier and produce a structured profile with an ICP fit score and recommended next actions.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Prospecting & Lead Generation"
compatibility: Requires Amplemarket MCP server
---

# Enrich and Score Lead

Enrich a single prospect using any available identifier and produce a structured profile with an ICP fit score and recommended next actions.

## Instructions

When a user provides a LinkedIn URL, email address, or name + company combination, enrich the person and their company, then synthesize the data into a scored profile.

### Steps

1. **Identify the input type** provided by the user:
    - **LinkedIn URL** (e.g., `linkedin.com/in/username`)
    - **Email address** (e.g., `jane@acme.com`)
    - **Name + Company** (e.g., "Jane Smith at Acme Corp")
    - If insufficient info is provided, ask the user for at least one of the above.
2. **Enrich the person** by calling `mcp__claude_ai_Amplemarket__enrich_person` with the available identifiers:
    - `linkedin_url` if provided
    - `email` if provided
    - `name` + `company_name` or `company_domain` if provided
    - Set `reveal_email` to `true` and `reveal_phone_numbers` to `true` to get full contact details.
    - **Credit note:** Enabling `reveal_email` and `reveal_phone_numbers` consumes additional Amplemarket credits per reveal. Factor this in when enriching large batches.
3. **Enrich the company** by calling `mcp__claude_ai_Amplemarket__enrich_company` with:
    - `domain` from the person enrichment result, or
    - `linkedin_url` of the company if the domain is not available.
4. **Calculate an ICP Fit Score** (1-100) based on these weighted factors:
    - **Seniority level** (30 points): C-Suite/VP/Founder = 25-30, Director/Head = 18-24, Manager = 10-17, Senior/Entry = 1-9
    - **Company size** (25 points): Score based on how well the company size matches typical B2B SaaS buying capacity (201-5000 = highest)
    - **Industry relevance** (20 points): Technology, Financial Services, SaaS = highest; score other industries based on typical B2B fit
    - **Data completeness** (15 points): Email found = 8, Phone found = 7
    - **Company signals** (10 points): Growth indicators, funding, tech stack relevance
    
    If the user has previously stated their ICP criteria, adjust the scoring weights to match their specific requirements.
    
5. **Format the output** as a structured profile:
    
    **Contact Card:**
    
    - Full name, title, seniority, department
    - Email, phone (if revealed)
    - LinkedIn URL
    - Location
    
    **Company Card:**
    
    - Company name, domain, industry
    - Size, type, founded year
    - Headquarters location
    - Description/tagline
    - Tech stack (if available)
    
    **ICP Fit Score:**
    
    - Overall score (1-100) with letter grade (A/B/C/D/F)
    - Score breakdown by factor with reasoning
    
    **Recommended Next Steps:**
    
    - Specific outreach suggestions based on the score and profile
    - Whether to prioritize, nurture, or deprioritize

### Important Notes

- Always attempt both person and company enrichment for the fullest picture.
- If the user has not defined their ICP, ask them before scoring: "What does your ideal customer look like? Industry, company size, seniority level, and any other criteria?" Only fall back to a general B2B SaaS baseline if the user explicitly asks you to proceed without specifying criteria.
- Be transparent about which data came from enrichment vs. inference.

## Examples

### Example 1: LinkedIn URL Enrichment

**User prompt:** "Enrich this lead: linkedin.com/in/johndoe-vpsales"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `linkedin_url`: "https://linkedin.com/in/johndoe-vpsales", `reveal_email`: true, `reveal_phone_numbers`: true.
2. Extracts company domain from the result.
3. Calls `mcp__claude_ai_Amplemarket__enrich_company` with the extracted domain.
4. Calculates ICP fit score.
5. Returns structured profile.

**Example output:**

**Contact Card**
| Field | Value |
|-----|-----|
| Name | John Doe |
| Title | VP of Sales |
| Seniority | VP |
| Department | Revenue |
| Email | john.doe@techcorp.com |
| Phone | +1 (555) 123-4567 |
| LinkedIn | linkedin.com/in/johndoe-vpsales |
| Location | San Francisco, CA |

**Company Card**
| Field | Value |
|-----|-----|
| Company | TechCorp |
| Domain | techcorp.com |
| Industry | Computer Software |
| Size | 201-500 employees |
| Type | Privately Held |
| HQ | San Francisco, CA |
| Description | AI-powered sales automation platform |

**ICP Fit Score: 82/100 (A)**
| Factor | Score | Reasoning |
|-----|-----|-------|
| Seniority | 27/30 | VP-level is a key decision maker |
| Company Size | 22/25 | 201-500 is ideal for B2B SaaS |
| Industry | 18/20 | Software/Tech is a core ICP industry |
| Data Completeness | 15/15 | Both email and phone found |
| Company Signals | 0/10 | No specific growth signals detected |

**Recommended Next Steps:**
- HIGH PRIORITY: This is a strong ICP fit. Proceed with personalized outreach.
- Suggested channel: Direct email to john.doe@techcorp.com
- Research TechCorp's current sales tech stack for a tailored value proposition.

### Example 2: Email-Based Enrichment

**User prompt:** "Score this prospect: maria.garcia@finova.io"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `email`: "maria.garcia@finova.io", `reveal_phone_numbers`: true.
2. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "finova.io".
3. Calculates and returns scored profile.

### Example 3: Name + Company Enrichment

**User prompt:** "What can you tell me about David Kim at Stripe?"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_person` with `name`: "David Kim", `company_name`: "Stripe", `reveal_email`: true, `reveal_phone_numbers`: true.
2. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "stripe.com".
3. Calculates and returns scored profile.

## Customizing Your ICP Score

The default scoring weights (Seniority 30%, Company Size 25%, Industry 20%, Data Completeness 15%, Company Signals 10%) work well for mid-market B2B SaaS. Adjust them when your ICP differs:

- **Selling to startups?** Increase Company Signals weight (funding stage, growth rate) and decrease Company Size weight. A 20-person Series A with strong growth signals is more valuable than a 500-person company with no momentum.
- **Selling to enterprise?** Increase Company Size weight and add a penalty for companies under 1,000 employees. Seniority should weight Director+ more heavily since VPs are the typical entry point.
- **Industry-specific product?** Increase Industry Relevance to 30%+ and be strict about which industries score highly. A perfect-seniority contact at the wrong industry is a wasted touch.
- **Selling contact data or enrichment?** Decrease Data Completeness weight since it measures Amplemarket's coverage, not the prospect's fit.

Tell the user: "I'm using default ICP scoring weights. Want me to adjust for your specific selling motion?"

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Person not found | Fallback chain: 1) Try LinkedIn URL if not already used. 2) Try company domain + full name. 3) Try `search_people` with `company_domains` + `person_titles` as a fuzzy match. 4) If still not found, inform user with suggestions: "Could not find this person. Try providing their LinkedIn URL or exact company domain." |
| Company enrichment fails | Fallback chain: 1) Try the company domain instead of name (or vice versa). 2) Try the LinkedIn company URL. 3) Try the parent company domain if this is a subsidiary. 4) If still failing, use whatever company data was returned in person enrichment and flag the gap. |
| Person enrichment succeeds but company enrichment fails | Use whatever company data was returned in the person enrichment (company name, domain). Present the person profile and note that company details are limited. Score with available data and flag the gap. |
| Company enrichment succeeds but person enrichment fails | Present the company profile and suggest alternative identifiers. Try searching for the person via `search_people` with company domain + title as a fallback. |
| Multiple people match the same name + company | Present all matches with titles and ask the user to confirm which person they mean. If LinkedIn URLs are available, show those for disambiguation. |
| Email not revealed | The contact may not have a verified business email. Suggest LinkedIn outreach instead. |
| Low data completeness | Combine multiple identifiers in the enrichment call for better match rates. If email is missing, suggest LinkedIn outreach. If phone is missing, note it in the profile and suggest email as primary channel. Always score with available data and flag which factors were impacted by missing data. |
| Score seems off | Ask the user to define their specific ICP criteria so scoring weights can be adjusted. |