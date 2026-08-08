---
name: suede-prospecting
description: "Suede-owned prospecting and qualification discipline. Use when defining an ICP, sourcing and enriching a bounded lead list, finding early adopters or design partners, scoring account fit, or documenting disqualification evidence. NOT FOR: sending outreach (use suede-cold-email), changing CRM routing (use suede-revops), or profiling competitors instead of prospects (use suede-competitor-profiling)."
metadata:
  version: 1.1.0
---

# Suede Prospecting

Suede Prospecting turns an approved ICP into a source-backed, scored lead sheet
across B2B SaaS, general B2B, local business, and early demand-signal motions.
Every candidate carries qualification evidence, disqualification logic, and a
compliance-aware handoff before outreach begins.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

## Pick the Branch

Prospecting motions differ enough that the workflow forks at intake. Pick **one** branch based on who the user is selling to:

| Branch | Sell to | What "qualified" looks like | Possible sources after access and terms checks |
|--------|---------|----------------------------|-----------------------------------------------|
| **SaaS** | Other SaaS companies / digital businesses | ICP fit + tech stack match + growth signals (funding, hiring, product velocity) | Public company sites, directories, developer sources, or licensed data available to the user |
| **B2B** | Non-SaaS B2B (services, manufacturers, enterprises, mid-market) | Industry + size + geographic fit + buying signals (trigger events, vendor changes) | Public company records, industry directories, or licensed business data available to the user |
| **Local SMB** | Local small businesses (shops, gyms, restaurants, clinics, salons, services) | Active business + website status + proximity + decision-maker access | Public business sites and manually reviewed listings allowed by their terms |
| **Demand-signal** | Early-stage: first customers, design partners, or beta users | A cited public pain, demand, or timing signal, not just firmographic fit | Public forums, reviews, issues, posts, jobs, and launch records reachable with current authorized tools or manual review |

Before using any named platform or vendor, discover what is currently callable,
authenticated, authorized, and permitted by its terms. If no research connector
or browser is available, give the user a manual source checklist and work from
URLs, exports, screenshots, or source text they provide.

If the user describes a hybrid motion (e.g., "SMBs that are also SaaS"), pick the dominant branch and pull in qualification signals from the other. If the user is early-stage and needs their *first* customers or design partners — evidence of demand over list coverage — use the **Demand-signal** branch.

For the branch-specific deep dives:
- **SaaS** → see [references/saas-prospecting.md](references/saas-prospecting.md)
- **B2B** → see [references/b2b-prospecting.md](references/b2b-prospecting.md)
- **Local SMB** → see [references/local-prospecting.md](references/local-prospecting.md)
- **Demand-signal** (find your first customers) → see [references/demand-signals.md](references/demand-signals.md)

---

## Shared Framework (all branches)

Every prospecting engagement follows the same five phases. Tools and qualification signals change per branch; the phases don't.

### Phase 1 — Define the ICP

Pull from `product-marketing.md` if available. Otherwise, gather:

1. **Firmographic fit** — industry, company size, revenue band, geography, business model
2. **Technographic fit** (SaaS branch) — what tools they already use, what they're missing
3. **Buying signal** — why now? (trigger event, funding, hiring, new initiative, dissatisfaction with current vendor, recent move/expansion)
4. **Decision-maker profile** — role, seniority, what they care about
5. **Disqualifiers** — what makes a prospect a clear "skip"

Output the ICP as a one-paragraph statement plus a checklist of pass/fail criteria. Don't move to discovery without this.

### Phase 2 — Build the candidate list (discovery)

Start with a bounded candidate sample sized to the requested output, source
access, and review capacity. Expand only when observed disqualification rates
show that another batch is needed.

- **SaaS / B2B**: cross-check material claims across available first-party,
  public, or licensed sources. Named vendors are candidates only after access,
  freshness, terms, and cost checks.
- **Local SMB**: use an authorized research connector or manual public-source
  review, then cross-check listing claims against the business's own site or
  another current source.

A smaller evidence-complete list is preferable to padding the output with
unverified candidates.

### Phase 3 — Qualify each candidate

Score every candidate against the ICP checklist. Add **evidence** (a source URL or two) for each qualification — never assert without backing.

**Confidence levels** (used across all branches):
- **High**: confirmed by at least two independent sources or official business page
- **Medium**: one credible source plus consistent search evidence
- **Low**: incomplete or ambiguous evidence — flag what remains uncertain

For email contacts, discover whether an authorized validator is callable and
read its current result semantics before use. If none is available, label the
address `unverified`, keep it out of send-ready exports, and provide a
user-operated validation checklist. Never claim that validation guarantees
delivery.

### Phase 4 — Score and prioritize

Apply this rubric for the **SaaS, B2B, and Local SMB** branches. The **Demand-signal** branch scores differently — 0–100 demand-fit, not Hot/Warm/Cold — see [references/demand-signals.md](references/demand-signals.md).

| Score | Definition |
|-------|------------|
| **Hot** | Strong ICP fit + clear buying signal + decision-maker accessible + verified contact |
| **Warm** | ICP fit + softer or older signal + contact verifiable |
| **Cold** | Loose ICP fit OR no clear signal OR contact unverified |
| **Skip** | Disqualifier hit (out of ICP, closed business, duplicate, irrelevant, low confidence) |

Branch-specific signals refine the scoring — see each reference file. Let the
evidence determine the number in each label; never force a Hot/Warm/Cold quota.

### Phase 5 — Output the lead sheet

(SaaS / B2B / Local SMB. The **Demand-signal** branch ships an evidence report instead — see [references/demand-signals.md](references/demand-signals.md).)

Default to a markdown table in chat. Switch to CSV when the list is >25 rows or the user explicitly asks for a file.

After the table, add **"Priority review candidates"** when the evidence supports
one or more: a bounded set ranked by current signal strength, with one sentence
on what was verified and what still needs review.

Columns vary by branch (see reference files), but every lead sheet includes:
- score, business/company name, contact (where applicable), why-it's-a-prospect, source(s), confidence, last verified date

---

## Compliance Guardrails

These apply to every branch. **Read first, every engagement.**

1. **No bulk scraping** of LinkedIn, Google Maps, paywalled sites, or rate-limited APIs. Browser is an assisted research tool, not a scraper.
2. **No CAPTCHA, login wall, or bot protection bypass.** If a site requires it, work with what's publicly visible.
3. **Public business contact channels only.** Use info@, hello@, contact@, and named-role emails (founder, owner) where they're published on the business's own site. Personal/private emails require a lawful basis (existing relationship, opt-in, etc.).
4. **GDPR / CAN-SPAM / CASL aware.** Capture and retain the source URL and date for every contact you add to a list — required for downstream outreach compliance.
5. **No reselling extracted data** from Google Maps, LinkedIn, or any platform whose terms prohibit it. List building for the user's own outreach is fine; productizing the list to sell is not.
6. **Rate limit yourself.** Even on public sources, space requests. Don't fingerprint as a bot.
7. **No breached, leaked, or unprovenanced data.** Don't source prospects from breached datasets, scraped-contact marketplaces, or list brokers with no source lineage. Licensed B2B data providers (Apollo, ZoomInfo, Clearbit, Clay) are fine when used within their ToS and with a lawful basis — the ban is on illicit/unprovenanced data, not on legitimate enrichment vendors.
8. **Never target or infer sensitive traits.** Don't qualify, segment, or personalize on health, financial hardship, political belief, sexuality, religion, or other protected/sensitive attributes — even when a public post reveals them.

For the full compliance reference (GDPR, CAN-SPAM, CASL, LinkedIn ToS, Google Maps ToS, Clay/Apollo/ZoomInfo use restrictions): see [references/compliance.md](references/compliance.md).

---

## Inputs to Collect

If missing, ask once, then infer reasonable defaults and continue:

- **Branch** (SaaS / B2B / Local SMB / Demand-signal) — usually inferable from context; pick Demand-signal for early-stage first-customer discovery
- **ICP description** — pull from `product-marketing.md` if present
- **Target count** — use the requested count or propose a bounded pilot justified
  by source coverage and review capacity
- **Geography** (essential for Local SMB; useful for B2B; less critical for SaaS)
- **Tools the user has access to** — discover current callable tools and
  authenticated accounts; never assume a vendor connector or browser exists
- **Output format** — chat table (default) or CSV
- **Buying signal preference** — what triggers should they prioritize? (funding rounds, hiring, recent move, etc.)

---

## Tool Selection Quick Picks

Full breakdown in [references/data-sources.md](references/data-sources.md). Quick picks:

Treat every named product below as a candidate, not an available capability.
Discover currently callable tools and verify the user's authenticated access,
license, source terms, and cost first.

| If the user has access to... | Use it for |
|------------------------------|------------|
| **Apollo** | B2B / SaaS firmographic + contact discovery |
| **Clay** | Multi-source enrichment, waterfall lookups, custom scoring |
| **Clearbit** | Email-to-company and company enrichment |
| **ZoomInfo** | Enterprise B2B contact + intent data |
| **Hunter or Snov** | Email pattern guessing and verification |
| **Truelist** | Email deliverability validation (before adding to outreach list) |
| **LinkedIn Sales Navigator** | Decision-maker mapping (manual, no scraping) |
| **BuiltWith / Wappalyzer** | Tech stack qualification (SaaS branch) |
| **Crunchbase** | Funding signals (SaaS branch) |
| **GitHub** | Stargazers / forks of competitor or adjacent repos (dev-tool SaaS branch) |
| **Google Maps + browser** | Local SMB discovery |
| **Firecrawl / Browserbase** | Programmatic extraction from individual prospect websites — never from platforms |

**If the user has no enrichment or browser tools**: provide exact public-source
queries and a qualification worksheet, then work from URLs, exports, or
screenshots the user supplies.

---

## Output Formats

### Default — chat table

For SaaS / B2B (≤25 rows):

```
| Score | Company | Industry | Size | Signal | Contact | Email status | Source | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

For Local SMB (≤15 rows) — port from the local-prospector reference:

```
| Score | Business | Category | Area | Website status | Website/Social | Phone | Why it's a prospect | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

### CSV — when >25 rows or user requests a file

SaaS / B2B columns:

```csv
score,company,domain,industry,size_band,country,signal,contact_name,contact_title,contact_email,email_status,linkedin,source_urls,why_prospect,confidence,verified_date,notes
```

Local SMB columns:

```csv
score,business,category,area,distance_km,website_status,website_url,social_urls,phone,email,source_urls,why_prospect,confidence,verified_date,notes
```

### Include after the table

- **Priority review candidates**: a bounded evidence-ranked set with
  one-sentence rationale each
- **Search parameters**: branch, ICP, location/radius, target count, date generated
- **Open questions**: anything you couldn't verify and the user should look at

---

## Quality Checks (before finalizing)

- [ ] Remove duplicates (by domain for SaaS/B2B, by business + address for Local SMB)
- [ ] Every "Hot" lead has a verified contact + at least one source URL
- [ ] Email status comes from a currently authorized validator with documented
      result semantics, or is explicitly `unverified`; failed results stay in a
      separate invalid bucket
- [ ] No lead labeled "Hot" lacks a clear buying signal
- [ ] Confidence levels honest — "High" requires 2 independent sources, not just two of your own searches
- [ ] No leads sourced from prohibited scraping (LinkedIn at scale, Google Maps bulk extract, etc.)
- [ ] Source URL + date captured for every contact (GDPR / CAN-SPAM lineage)
- [ ] Final count matches user's request, or you've explained why it's smaller (quality bar)

---

## Common Mistakes

1. **Starting discovery without an ICP**. Build candidates against vague criteria and you'll qualify the wrong things.
2. **Treating data sources as authoritative without cross-checks**. Apollo and ZoomInfo are out of date often; verify before scoring as "Hot."
3. **Presenting unverified contacts as send-ready**. Use an available authorized
   validator or keep the address labeled `unverified` with a manual validation
   handoff.
4. **Bulk scraping LinkedIn or Google Maps**. Real risk: account suspension + ToS violation. Browser as an assisted tool only.
5. **Mixing branches**. Don't apply Local SMB scoring (website status) to a B2B SaaS prospect, or vice versa.
6. **"Hot" labels without buying signals**. ICP fit alone is not enough — the signal is what makes the timing right.
7. **No source URLs**. Every claim should be traceable to a public source. Future outreach depends on this lineage.
8. **Ignoring quiet hours / time zone** when scheduling the downstream outreach
   (handoff to `suede-cold-email`).
9. **Forgetting to retain consent / lineage records**. Required for GDPR DSARs and CAN-SPAM audits.

---

## Task-Specific Questions

1. Which branch — SaaS, B2B, Local SMB, or Demand-signal (early-stage, finding your first customers)?
2. What's your ICP? (Or: should I pull from your product-marketing context?)
3. How many qualified leads do you want?
4. Which research or validation tools are currently callable and authorized?
   If none, can you provide URLs, exports, or screenshots for manual review?
5. What's the triggering buying signal you care most about?
6. Geography or radius (Local SMB / B2B)?
7. Chat table or CSV?

---

## Tool Integrations

These are selection examples, not guaranteed integrations. Before using one,
verify current vendor documentation, account access, pricing, data freshness,
export rights, platform terms, and whether a callable connector is actually
available in the current session.

| Tool | Best For | Verify Before Use |
|------|----------|-------------------|
| **Apollo** | B2B / SaaS firmographic + contact discovery | Freshness, export terms, email validation |
| **Clay** | Multi-source enrichment + waterfall | Credit cost, providers, field provenance |
| **Clearbit** | Email-to-company enrichment | Current product access and coverage |
| **ZoomInfo** | Enterprise B2B contact + intent | License, export rights, signal freshness |
| **Hunter / Snov** | Email pattern discovery | Verification status and lawful basis |
| **Truelist** | Email deliverability validation | Result meanings and current API limits |
| **Outreach** | Sales engagement after approval | Sequence permissions and suppression rules |
| **RB2B** | Visitor identification | Privacy basis and company-vs-person grain |
| **GitHub** | Public developer-intent signals | API terms, rate limits, company mapping |
| **Firecrawl / Browserbase** | Single-target public-site research | Target terms, scope, and session access |

---

## Boundaries

- Do not send outreach, import contacts, buy data, mutate a CRM, or enroll a
  person in a sequence.
- Do not invent contact details or qualification evidence, evade source terms,
  collect unnecessary personal data, or label a lead verified without a cited
  current source.
- Do not decide legal compliance or claim deliverability. Apply the applicable
  consent, privacy, and suppression rules before any downstream contact.

## Routing

- Use `suede-product-marketing` to define the ICP and positioning context.
- Use `suede-cold-email` after a qualified list is approved for outreach copy.
- Use `suede-revops` for approved CRM routing and lifecycle handoff.
- Use `suede-sales-enablement` for collateral used in active sales work.
