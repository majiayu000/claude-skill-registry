---
name: competitive-account-research
description: >
  Generate a comprehensive account brief by combining company enrichment, decision-maker mapping, and engagement history from Amplemarket.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Account Intelligence"
compatibility: Requires Amplemarket MCP server
---

# Competitive Account Research

Generate a comprehensive account brief by combining company enrichment, decision-maker mapping, and engagement history from Amplemarket.

## Instructions

When a user asks for research on a target account, compile a multi-source intelligence brief using the following workflow.

### Steps

1. **Identify the target account.** Extract the company name or domain from the user's request. If ambiguous, ask for clarification.
2. **Enrich the company** by calling `mcp__claude_ai_Amplemarket__enrich_company` with:
    - `domain` if the user provided a domain or you can infer it
    - `linkedin_url` if the user provided a LinkedIn company URL
    This returns firmographics: industry, size, type, location, description, tech stack, and more.
3. **Check internal account data** by calling `mcp__claude_ai_Amplemarket__list_accounts` with the company `name` or `domain` to find if this account already exists in the system. If found, call `mcp__claude_ai_Amplemarket__get_account` with the account `id` to retrieve:
    - Engagement stats (emails sent, opened, replied)
    - CRM data and opportunity status
    - AI-generated insights
    - Account owner and tags
4. **Map key decision makers** by calling `mcp__claude_ai_Amplemarket__search_people` with:
    - `company_names` or `company_domains`: [target company]
    - `person_seniorities`: ["C-Suite", "VP", "Head", "Director"]
    - `full_output`: true
    - `page_size`: 20
    
    Then organize results by department to identify the buying committee.
    
5. **Identify stakeholder gaps.** Based on the decision makers found, flag any missing roles that would typically be part of the buying committee for your product category (e.g., if no IT stakeholder was found, note this as a gap).
6. **Compile the account brief** with five sections:
    
    **Section 1: Company Overview**
    
    - Company name, domain, industry, size, type
    - Headquarters and other locations
    - Description and value proposition
    - Tech stack (if available)
    - Recent funding or growth signals
    
    **Section 2: Key Decision Makers**
    
    - Table of identified stakeholders grouped by department
    - Seniority level and LinkedIn URL for each
    - Highlight the likely economic buyer and champions
    
    **Section 3: Engagement History** (if account exists in system)
    
    - Email engagement metrics
    - Previous outreach attempts and responses
    - CRM opportunity status and stage
    - Account owner
    
    **Section 4: Competitive Landscape**
    
    - Known competitors based on industry and tech stack
    - Potential competitive positioning angles
    - Technology overlap or displacement opportunities
    
    **Section 5: Recommended Approach**
    
    - Suggested entry point (which stakeholder to contact first)
    - Messaging angle based on company profile and pain points
    - Multi-threading strategy across the buying committee
    - Timing considerations

### Important Notes

- If `list_accounts` returns no results, the account is net-new. Note this and skip the engagement history section.
- Prioritize the search for decision makers in departments most relevant to the user's product.
- If the user mentions which product or solution they sell, tailor the Competitive Landscape and Recommended Approach sections accordingly.

## Examples

### Example 1: Domain-Based Research

**User prompt:** "Research this account for me: datadog.com"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "datadog.com".
2. Calls `mcp__claude_ai_Amplemarket__list_accounts` with `domain`: "datadog.com".
3. If account found, calls `mcp__claude_ai_Amplemarket__get_account` with the account ID.
4. Calls `mcp__claude_ai_Amplemarket__search_people` with `company_domains`: ["datadog.com"], `person_seniorities`: ["C-Suite", "VP", "Head", "Director"], `full_output`: true.
5. Compiles the five-section account brief.

**Example output (abbreviated):**

---

**ACCOUNT BRIEF: Datadog**

**1. Company Overview**
| Field | Detail |
|-----|-----|
| Company | Datadog, Inc. |
| Domain | datadog.com |
| Industry | Computer Software / Cloud Monitoring |
| Size | 5001-10000 employees |
| Type | Public Company (NASDAQ: DDOG) |
| HQ | New York, NY |
| Description | Cloud-scale monitoring and analytics platform for infrastructure, applications, and logs |

**2. Key Decision Makers**

*Revenue/Sales*
| Name | Title | LinkedIn |
|----|-----|-------|
| Alex Rivera | CRO | linkedin.com/in/arivera |
| Kim Tanaka | VP of Sales, Americas | linkedin.com/in/ktanaka |

*Engineering & Technical*
| Name | Title | LinkedIn |
|----|-----|-------|
| Jordan Lee | VP of Engineering | linkedin.com/in/jlee |
| Sam Gupta | Director of Platform Engineering | linkedin.com/in/sgupta |

*Marketing*
| Name | Title | LinkedIn |
|----|-----|-------|
| Lisa Park | CMO | linkedin.com/in/lpark |

Gap identified: No IT/Security stakeholder found at Director+ level.

**3. Engagement History**
| Metric | Value |
|-----|-----|
| Emails Sent | 12 |
| Opens | 8 |
| Replies | 1 |
| Last Contact | 2026-01-15 |
| CRM Stage | Prospecting |
| Account Owner | rep@ourcompany.com |

**4. Competitive Landscape**
- Direct competitors in their space: New Relic, Splunk, Dynatrace
- Tech stack may include: AWS, Kubernetes, Go
- Displacement angle: If selling complementary tooling, position as enhancing their existing stack

**5. Recommended Approach**
- Entry point: Jordan Lee (VP Eng), most likely technical evaluator
- Multi-thread to Alex Rivera (CRO) for budget authority
- Messaging: Focus on how your solution complements their cloud-native architecture
- Timing: Previous engagement showed interest (1 reply). Follow up on that thread

---

### Example 2: Company Name Research

**User prompt:** "Give me intel on Stripe before my call tomorrow"

**What the skill does:**
1. Calls `mcp__claude_ai_Amplemarket__enrich_company` with `domain`: "stripe.com".
2. Checks for existing account via `mcp__claude_ai_Amplemarket__list_accounts`.
3. Maps decision makers via `mcp__claude_ai_Amplemarket__search_people`.
4. Returns a concise account brief focused on call preparation.

### Example 3: Account with Specific Product Context

**User prompt:** "Deep dive on Shopify. We sell sales engagement software."

**What the skill does:**
1. Enriches Shopify and maps decision makers.
2. Focuses decision-maker search on Revenue and IT departments.
3. Tailors competitive landscape to sales engagement tools (Outreach, Salesloft, Apollo).
4. Customizes recommended approach for selling sales engagement software to an e-commerce platform company.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Company not found in enrichment | Fallback chain: 1) Try the company domain in `enrich_company`. 2) Try the LinkedIn company URL. 3) Try the parent company domain. 4) Ask user: "Could not find [company]. Can you confirm the exact domain or LinkedIn URL?" |
| No decision makers found | Fallback chain: 1) Broaden seniority to include "Manager" and "Senior". 2) Try searching by company name instead of domain. 3) Try broader departments (e.g., add "Senior Leadership" if only searching specific functions). 4) For companies with <50 employees, search for "Founder" and "C-Suite" only. |
| Account not in system | This is normal for net-new accounts. Skip Section 3 and note this is a new target. |
| Too many decision makers | Filter by specific departments relevant to the user's product. Focus on the 5-8 most relevant stakeholders. |
| User wants deeper research on one person | Pivot to the enrich-and-score-lead skill for individual prospect deep dives. |
| Company enrichment succeeds but `search_people` finds no decision makers | Try broadening seniority to include "Manager" and "Senior". Also try searching by company name instead of domain, as some companies have multiple domains. |
| Engagement history data seems stale | Flag with: "[Data may be stale, last updated DATE]. This may not reflect recent off-platform interactions." Then suggest: "Want me to re-enrich this account for the latest data?" |
| `search_companies` returns 0 for a company that definitely exists | Fallback chain: 1) Try `enrich_company` with the domain directly. 2) Try the LinkedIn company URL. 3) Try alternate or parent company domains. Some companies are indexed by domain but not searchable by name. |