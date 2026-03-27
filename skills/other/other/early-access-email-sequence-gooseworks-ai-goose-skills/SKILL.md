---
name: early-access-email-sequence
description: >
  Generate a personalized 7-email onboarding sequence for Goose early access signups.
  Takes a LinkedIn profile URL and company domain, researches the person and company,
  classifies their role, and produces all 7 emails ready to send — personalized with
  real context, not merge tags. Outputs to a Notion database (one row per user, columns
  for each email). Use this skill whenever someone signs up for Goose early access, when
  you need to generate onboarding emails for new users, when the user says "generate
  emails for a new signup", "onboard this person", "add them to the email sequence",
  or provides a LinkedIn URL with a company domain in the context of the launch.
  Also use when processing a batch of signups.
tags: [outreach]
---

# Early Access Email Sequence Generator

Research a new Goose signup, then generate all 7 onboarding emails personalized with real context about their role and company. Output goes to a shared Notion database — one row per person, every email ready to copy-paste and send on schedule.

The sequence runs over 14 days (Day 0, 2, 5, 8, 10, 12, 14). Emails 2 and 4 are personalized by role. Emails 1, 5, 6 are universal. Emails 3 and 7 branch by activation status (generate the default version; note when to swap).

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `linkedin_url` | Yes | LinkedIn profile URL of the signup |
| `company_domain` | Yes | Company website domain (e.g., `posthog.com`) |
| `signup_date` | Yes | Date they signed up (to calculate send dates). Default: today. |
| `sender_name` | No | Name to sign emails with. Default: ask the user. |
| `calendly_link` | No | Calendly URL for feedback calls. Default: ask the user. |
| `notion_db_url` | No | Existing Notion database URL to add the row to. If not provided, create a new database. |

For batch processing, accept a list of `{linkedin_url, company_domain, signup_date}` objects and process each one sequentially.

## Procedure

### Phase 1: Research the Person

Use web search to gather context on the signup. Do NOT scrape LinkedIn directly — use web search queries that surface LinkedIn profile data.

1. **Search for the person:**
   - WebSearch: `"{{linkedin_url}}" OR site:linkedin.com/in/{{handle}}`
   - WebSearch: `"{{person_name}}" {{company}} LinkedIn` (once you have their name)

2. **Extract:**
   - Full name
   - Current title and role
   - Company they work at (confirm it matches the provided domain)
   - Seniority level (IC, Manager, Director, VP, C-suite, Founder)
   - Any recent LinkedIn posts or activity themes (if surfaced in search results)
   - Background: previous companies, career trajectory

3. **If LinkedIn data is thin**, supplement with:
   - WebSearch: `"{{person_name}}" {{company}}` (company blog, press mentions, podcast appearances)
   - This additional context helps personalize Emails 2 and 4

### Phase 2: Research the Company

Run these searches in parallel where possible:

1. **What they do:**
   - WebFetch: `https://{{company_domain}}` — extract tagline, product description, target audience
   - If the site is JS-rendered and returns little content, fall back to WebSearch: `{{company_domain}} what does {{company}} do`

2. **GTM motion:**
   - Check for self-serve signup / free trial (PLG signal)
   - Look for "Book a demo" / "Contact sales" (sales-led signal)
   - Check pricing page: transparent pricing = PLG, "Contact us" = sales-led
   - WebSearch: `{{company}} careers sales OR marketing OR growth` — are they hiring GTM roles?

3. **Size and stage:**
   - WebSearch: `{{company}} funding round series` — latest funding, stage
   - WebSearch: `{{company}} headcount employees` — approximate team size
   - Check LinkedIn company page follower count if surfaced

4. **Competitors:**
   - WebSearch: `{{company}} competitors alternatives vs`
   - WebSearch: `{{company}} G2 category` — what category are they in?
   - Identify 2-3 named competitors (used to personalize Email 4 marketing variant)

5. **Compile a company summary** (2-3 sentences):
   - What they do, who they sell to, how they sell (PLG vs sales-led), approximate size, key competitors

### Phase 3: Classify Role

Based on the person's title, classify into one of four buckets. This determines which variants of Emails 2 and 4 to use.

| Bucket | Matching Titles | Notes |
|--------|----------------|-------|
| **Sales** | SDR, BDR, AE, Account Executive, Sales Manager, VP Sales, CRO, Head of Sales, Sales Director, Revenue | Anyone whose job is closing deals or generating pipeline |
| **Marketing** | Content, SEO, Demand Gen, CMO, Marketing Manager, VP Marketing, Growth Marketing, Brand, Communications, PR | Anyone whose job is creating demand or content |
| **Growth / RevOps** | Growth, RevOps, GTM Ops, Revenue Operations, Head of Growth, Business Operations, Strategy & Ops | Anyone running GTM systems, ops, or cross-functional growth |
| **Founder** | CEO, Co-founder, Founder, CTO (at <20 person company), COO (at <20 person company) | Founders wearing the GTM hat. If company is <20 people and title is C-suite, classify as Founder. |

**Ambiguous cases:**
- "Head of Growth Marketing" → Marketing (has "Marketing" in title)
- "VP Revenue" → Sales (Revenue usually maps to sales leadership)
- "COO" at a 200-person company → Growth/RevOps (not a founder wearing all hats)
- "Product Manager" → Growth/RevOps (closest fit; PM cares about activation, not sales)
- If truly ambiguous, default to **Founder** — it's the most general variant

### Phase 4: Generate Emails

Read the email templates from `references/email-templates.md` in this skill's directory.

For each email, apply the research to personalize:

**Email 1 (Day 0) — Welcome:**
- Replace `{{first_name}}`, `{{sender_name}}`, `{{calendly_link}}`
- No heavy personalization needed

**Email 2 (Day 2) — Use Case #1:**
- Select the variant matching the role bucket
- Replace all standard variables
- Write the `[PERSONALIZE]` section: 1-2 sentences connecting the workflow to something specific about their company, based on your Phase 2 research. This is where the value is — reference their GTM motion, their market, their competitors, or their stage. Be specific and concrete, not generic.

**Email 3 (Day 5) — Nudge:**
- Generate the "not activated" version (default)
- Add a note: "If {{first_name}} has completed a workflow by Day 5, swap to the activated variant: [include activated variant text]"

**Email 4 (Day 8) — Use Case #2:**
- Select the variant matching the role bucket
- Replace all standard variables
- Write the `[PERSONALIZE]` section: connect the second workflow to their specific situation. Use competitor names, industry events, or market context from your research.

**Email 5 (Day 10) — Community Spotlight:**
- Output as template with placeholders intact ({{top_workflow}}, {{X}}, etc.)
- Add a note: "WRITE THIS LIVE on {{send_date}} with real usage data. Do not send with placeholder content."

**Email 6 (Day 12) — Skills Page:**
- Replace `{{first_name}}` and `{{sender_name}}`
- No personalization needed

**Email 7 (Day 14) — Feedback Ask:**
- Generate the "not activated" version (default)
- Add a note: "If {{first_name}} has been active, swap to the activated variant: [include activated variant text]"

### Phase 5: Calculate Send Dates

From the `signup_date`, calculate each email's send date:

| Email | Day Offset | Send Date |
|-------|-----------|-----------|
| Email 1 | Day 0 | signup_date |
| Email 2 | Day 2 | signup_date + 2 days |
| Email 3 | Day 5 | signup_date + 5 days |
| Email 4 | Day 8 | signup_date + 8 days |
| Email 5 | Day 10 | signup_date + 10 days |
| Email 6 | Day 12 | signup_date + 12 days |
| Email 7 | Day 14 | signup_date + 14 days |

### Phase 6: Output to Notion

#### First-time setup (no existing database)

If `notion_db_url` is not provided, create a new Notion database. Use the Notion MCP `notion-create-database` or create a database page manually.

**Database schema:**

| Property | Type | Description |
|----------|------|-------------|
| Name | Title | Person's full name |
| Company | Text | Company name |
| Role Bucket | Select (Sales, Marketing, Growth/RevOps, Founder) | Classified role |
| LinkedIn URL | URL | Profile link |
| Signup Date | Date | When they signed up |
| Status | Select (New, Email 1 Sent, Email 2 Sent, ..., All Sent) | Sending progress tracker |
| Person Summary | Text | Research notes on the person |
| Company Summary | Text | Research notes on the company |
| Email 1 Subject | Text | Subject line |
| Email 1 Body | Text | Full email body |
| Email 1 Send Date | Date | When to send |
| Email 2 Subject | Text | Subject line |
| Email 2 Body | Text | Full email body |
| Email 2 Send Date | Date | When to send |
| Email 3 Subject | Text | Subject line |
| Email 3 Body | Text | Full email body |
| Email 3 Send Date | Date | When to send |
| Email 4 Subject | Text | Subject line |
| Email 4 Body | Text | Full email body |
| Email 4 Send Date | Date | When to send |
| Email 5 Subject | Text | Subject line |
| Email 5 Body | Text | Template — fill live on send date |
| Email 5 Send Date | Date | When to send |
| Email 6 Subject | Text | Subject line |
| Email 6 Body | Text | Full email body |
| Email 6 Send Date | Date | When to send |
| Email 7 Subject | Text | Subject line |
| Email 7 Body | Text | Full email body |
| Email 7 Send Date | Date | When to send |
| Notes | Text | Swap notes, activation variants, special observations |

#### Adding a row

Use `notion-create-pages` with the database as parent. Fill all properties from the generated content.

In the **Notes** column, include:
- The activated variant text for Email 3 (to swap if needed)
- The activated variant text for Email 7 (to swap if needed)
- Any special observations from research that might be useful for the sender

#### After creating the row

Confirm to the user:
```
Added {{name}} ({{role_bucket}}) at {{company}} to the email sequence.
- Email 1 ready to send: {{email_1_send_date}}
- Email 2 ready to send: {{email_2_send_date}} ({{role_bucket}} variant: {{use_case_1}})
- ...through Email 7 on {{email_7_send_date}}
- Company summary: {{company_summary_short}}
```

## Batch Processing

When given multiple signups at once:

1. Collect all `{linkedin_url, company_domain, signup_date}` entries
2. Process each person sequentially through Phases 1-5
3. Add all rows to the same Notion database
4. After all are processed, show a summary table:

| # | Name | Company | Role | Email 1 Date | Email 7 Date |
|---|------|---------|------|-------------|-------------|
| 1 | ... | ... | ... | ... | ... |

## Email Writing Rules

These are non-negotiable — every generated email must follow them:

1. **No filler openers.** Never "I hope this finds you well", "I hope you're having a great week"
2. **Under 150 words per email.** Most should be 80-120 words.
3. **One CTA per email.** Never two asks in one email.
4. **Sound like a founder, not a marketing team.** Casual, direct, no corporate speak.
5. **The [PERSONALIZE] sections are the entire value.** Generic personalization ("since you're in B2B SaaS...") is worthless. Reference specific things: their competitor names, their GTM motion, their funding stage, their market. If research didn't surface anything specific enough, say something honest about why this workflow matters for companies at their stage.
6. **Sign off with name only.** No "Best regards", no title, no company. Just the name.
7. **No emoji in emails.** Professional but warm.

## Example

**Input:**
```
linkedin_url: https://www.linkedin.com/in/jamesmith
company_domain: posthog.com
signup_date: 2026-03-10
```

**Research findings:**
- Jane Smith, Head of Growth at PostHog
- PostHog: open-source product analytics, PLG motion, ~80 employees, Series B ($45M), competes with Amplitude, Mixpanel, Heap
- Role bucket: Growth / RevOps

**Email 2 personalization (Growth/RevOps variant):**
> Since you're running growth at PostHog, this one's for you:
> ...
> Given PostHog's open-source PLG motion and the Amplitude/Mixpanel competitive landscape, the audit's competitive positioning section will show you exactly where PostHog's content gaps are vs. those incumbents — and the white space map tends to surface channels that open-source companies underinvest in.

That level of specificity — naming their competitors, referencing their PLG motion, noting the open-source angle — is what makes the email feel personal rather than templated.

## Dependencies

- Web search and web fetch capabilities (for research)
- Notion MCP tools (`notion-create-pages`, `notion-fetch`, optionally `notion-create-database`)
- Email templates at `references/email-templates.md` in this skill's directory
