---
name: account-research-brief
description: "Use when preparing to engage a target account, researching a company before outreach, or building pre-call intelligence. Triggers: 'research this company', 'account brief for [company]', 'company research', 'what do I need to know about [company]', 'pre-outreach research'."
version: 1.0.0
---

# Account Research Brief

Produce a comprehensive 1-page company intelligence brief in 2-3 minutes using WebSearch. Everything a GTM engineer needs to engage a target account — from company overview to ready-to-use outreach angles.

## Steps

### 1. Collect Input

Ask the user for:

- **Company name** (required)
- **Your product/service** (optional) — if provided, engagement angles will be tailored to the user's offering. If omitted, angles stay generic but actionable.
- **Target persona title** (optional) — focuses the Decision Makers section on that role. Default to CRO / VP Sales / Head of Growth if not specified.

Do NOT proceed until you have at least the company name.

### 2. Company Overview

Run 1-2 WebSearch queries (e.g., `"{company} what does it do"`, `"{company} funding crunchbase"`).

Gather:

- What they do (one paragraph, plain language)
- Founded year and HQ location
- Company size — employee count, revenue range if public
- Funding stage and total raised (for startups / private companies)
- Key product(s) or service(s)
- Recent news from the last 90 days (1-3 headlines with URLs)

If any data point is not findable, write "Not found" — NEVER fabricate company data.

### 3. Decision Makers

Run 1-2 WebSearch queries (e.g., `"{company} CEO founder"`, `"{company} {target persona title}"`).

Gather:

- CEO / Founder — name, short background (prior companies, notable achievements)
- Target persona — name and title of the person matching the user's specified role (or CRO / VP Sales / Head of Growth by default)
- LinkedIn activity themes — what topics they post or comment about (if findable)
- Recent public content — podcast appearances, conference talks, blog posts, tweets
- Org structure clues — approximate size of their sales / marketing / growth team (from LinkedIn headcount or job postings)

### 4. Technology Stack

Run 1-2 WebSearch queries (e.g., `"{company} tech stack job postings"`, `"{company} integrations partners"`).

Gather:

- CRM platform (Salesforce, HubSpot, etc.)
- Marketing automation (Marketo, Pardot, HubSpot, etc.)
- Outreach / sales engagement tools (Outreach, Salesloft, Apollo, etc.)
- Other known tools from job postings, integrations pages, G2 profiles, case studies
- Stack gaps — if the user provided their product/service, note where their product could fit

### 5. Recent Signals

Run 1-2 WebSearch queries (e.g., `"{company} news 2026"`, `"{company} hiring jobs"`).

Gather and present as a table:

| Signal | Detail | Date | Source |
|--------|--------|------|--------|

Signal types to look for:

- Fundraise announcements
- Hiring patterns (what roles are they adding? volume?)
- Product launches or major feature releases
- Partnership announcements
- Press mentions or media coverage
- Leadership changes (new C-suite, VP hires)

**ICP cross-reference:** If `docs/icp.md` exists in the project, read it and cross-reference the signals above against the ICP's buying signal list. Flag any matches explicitly (e.g., "MATCH: ICP buying signal 'Series B+ fundraise' — Company raised Series C in Jan 2026").

### 6. Competitive Landscape

Run 1-2 WebSearch queries (e.g., `"{company} competitors"`, `"{company} vs alternatives"`).

Gather:

- 3-5 main competitors
- How the target company positions itself vs. competitors (messaging, pricing tier, feature differentiation)
- Recent competitive moves — pricing changes, feature launches, market entries
- Market dynamics that affect them (regulation, consolidation, shifts in buyer behavior)

### 7. Engagement Angles

Based on ALL findings from steps 2-6, generate 3-5 outreach angles.

Each angle must include:

1. **Angle name** — a short label (e.g., "Hiring Surge Play", "Stack Gap Angle")
2. **Finding** — the specific research finding that makes this angle relevant
3. **Value connection** — how this finding connects to a pain point or opportunity
4. **One-sentence opener** — a ready-to-send first line for email, LinkedIn, or cold call

Rules:

- If the user provided their product/service, make every angle specific to their offering.
- If they did not, keep angles generic but grounded in the research (never vague).
- Each angle must tie to a SPECIFIC finding, not a generic observation.

### 8. Write the Brief

Write the output file to `docs/accounts/{company-name-slug}.md`.

The slug is the company name lowercased with spaces replaced by hyphens and special characters removed (e.g., "HubSpot" becomes `hubspot`, "Scale AI" becomes `scale-ai`).

Create the `docs/accounts/` directory if it does not exist.

Use this structure for the output file:

```markdown
# {Company Name} — Account Research Brief

**Website:** {url}
**HQ:** {location}
**Researched:** {YYYY-MM-DD}

---

## Company Overview

{One paragraph on what they do, key products/services}

- **Founded:** {year}
- **Employees:** {count or range}
- **Revenue:** {range or "Private"}
- **Funding:** {stage, total raised, last round date}

### Recent News
- {headline} — {source} ({date})
- ...

---

## Decision Makers

**CEO / Founder:** {name}
- {background, 1-2 sentences}

**{Target Persona Title}:** {name, if found}
- {background, activity themes, recent content}

**Team Size Clues:** {what's known about sales/marketing/growth org size}

---

## Tech Stack

| Category | Tool(s) |
|----------|---------|
| CRM | {tool} |
| Marketing Automation | {tool} |
| Sales Engagement | {tool} |
| Other | {tools} |

{If user provided their product: "**Stack Gap:** {where your product fits}"}

---

## Recent Signals

| Signal | Detail | Date | Source |
|--------|--------|------|--------|
| {type} | {detail} | {date} | [{source}]({url}) |
| ... | ... | ... | ... |

{If ICP cross-reference was done: "**ICP Signal Matches:** {list matches}"}

---

## Competitive Landscape

**Main Competitors:** {list}

**Positioning:** {how they differentiate}

**Recent Competitive Moves:** {notable shifts}

**Market Context:** {dynamics affecting them}

---

## Engagement Angles

1. **{Angle Name}**
   - *Finding:* {specific research finding}
   - *Value Connection:* {why this matters / pain point}
   - *Opener:* "{ready-to-send first sentence}"

2. **{Angle Name}**
   - *Finding:* ...
   - *Value Connection:* ...
   - *Opener:* "..."

3. ...

---

## Sources

- [{title or description}]({url})
- ...
```

After writing the file, tell the user the file path and offer to refine any section.

## Tools

- **WebSearch** — primary tool. Run 5-10 searches per company to cover all sections. Prioritize speed over exhaustive coverage.
- **Read** — check if `docs/icp.md` exists for ICP cross-referencing in the signals section.
- **Write** — output the final brief to `docs/accounts/{company-name-slug}.md`.

## Rules

1. **Speed is the value.** The entire brief should take 2-3 minutes. Do not over-research. Run searches in parallel when possible. One or two searches per section is enough.
2. **Use WebSearch aggressively.** 5-10 total searches per company. Batch independent searches into the same message to run them in parallel.
3. **Always cite sources.** Every claim must trace back to a URL in the Sources section. Include the URL inline in tables where applicable.
4. **Never fabricate.** If a data point is not findable after searching, write "Not found." Never guess at revenue, funding, employee count, or names.
5. **Keep it to one page.** The brief should be concise and scannable. No filler paragraphs. Use tables and bullet points. A busy salesperson should absorb the whole thing in 3 minutes.
6. **No internal references.** This skill is part of a public playbook. Never reference Earleads, Notion databases, Apify, internal agents, or any proprietary tooling.
7. **Works universally.** This skill works for any B2B company researching any target account. Do not assume a specific industry, company size, or GTM motion.
8. **Create directories as needed.** If `docs/accounts/` does not exist, create it before writing the file.
