---
name: marketing-leads-generation
description: Revenue-aligned demand generation with lead types, funnel design, conversion paths, scoring/routing, attribution, and compliance for B2B pipeline building.
---

# LEAD GENERATION — PIPELINE OS (OPERATIONAL)

Built as a **no-fluff execution skill** for revenue-aligned demand generation.

**Structure**: Core lead generation fundamentals first. AI-specific automation in clearly labeled "Optional: AI / Automation" sections.

---

## Core: Lead Type Definitions

Clear definitions prevent Sales/Marketing friction. Align on these before building pipeline.

| Lead Type | Definition | Qualification Criteria | Owner |
|-----------|------------|----------------------|-------|
| **Lead** | Any identified contact | Has email/phone, some interest signal | Marketing |
| **MQL** (Marketing Qualified Lead) | Fits ICP + engaged with marketing | Firmographic fit + behavior threshold | Marketing |
| **SQL** (Sales Qualified Lead) | Ready for sales conversation | MQL + explicit buying signal or demo request | Sales |
| **PQL** (Product Qualified Lead) | Used product, shows upgrade potential | Trial/freemium + usage threshold | Product + Sales |
| **SAL** (Sales Accepted Lead) | SQL accepted by sales rep | Sales confirms qualification after first contact | Sales |

### What “Good” Looks Like (Operational)

Set targets from your own baseline, then improve stage-by-stage:
- Sales acceptance rate (SQL → SAL)
- Speed-to-lead (time to first touch)
- Stage conversion rates and time-in-stage
- Pipeline created per channel (not leads)

---

## Core: Funnel Design Framework

| Stage | User State | Content/Action | Goal |
|-------|-----------|----------------|------|
| **Awareness** | Problem-aware | Blog, social, SEO, ads | Capture attention |
| **Interest** | Solution-curious | Guides, webinars, comparisons | Capture contact info |
| **Consideration** | Evaluating options | Case studies, demos, free tools | Convert to MQL |
| **Decision** | Ready to buy | Pricing, proposals, trials | Convert to SQL → Opportunity |
| **Activation** | New customer | Onboarding, training, quick wins | Reduce churn, increase expansion |

### Funnel Diagnostic Questions

1. Where is the biggest drop-off? (Measure stage-to-stage conversion)
2. What's your time-in-stage for each? (Long times = friction)
3. Are leads skipping stages? (May indicate misalignment)
4. What percentage of MQLs get accepted by Sales? (Low = quality issue)

For full funnel setup including MQL/SQL criteria and SLAs, use [lead-funnel-definition.md](templates/lead-funnel-definition.md).

---

## Core: Gating Strategy

Not all content should be gated. Use this decision framework:

| Content Type | Gate? | Why |
|--------------|-------|-----|
| Blog posts, how-to guides | **No** | Build SEO, trust, awareness |
| Comparison guides, buyers guides | **Light gate** (email only) | High intent, worth capturing |
| Industry reports, original research | **Gate** | High value, worth exchange |
| ROI calculators, assessments | **Gate** | Strong buying signals |
| Product demos, pricing | **Gate** | Direct sales intent |
| Case studies | **Optional** | Gate if detailed; ungate if brief |

### Do (Gating)

- Ask only for fields you'll use (email + company is often enough)
- Progressive profiling: collect more data over multiple interactions
- A/B test gated vs ungated for the same content
- Honor the value exchange: gated content must deliver real value

### Avoid (Gating)

- Gating everything (kills organic discovery)
- Long forms for top-of-funnel content (start with the minimum fields you will use)
- Requiring phone number for early-stage content
- Gating content that's freely available elsewhere

---

## Core: Attribution Fundamentals + Limitations

### Attribution Models

| Model | How It Works | Best For | Limitation |
|-------|--------------|----------|------------|
| **First-touch** | 100% credit to first interaction | Understanding awareness sources | Ignores nurture journey |
| **Last-touch** | 100% credit to final touch | Understanding closing sources | Ignores awareness |
| **Linear** | Equal credit to all touches | Simple multi-touch | Over-credits low-value touches |
| **Time-decay** | More credit to recent touches | Long sales cycles | Complex to implement |
| **Position-based** | 40/20/40 to first/middle/last | Balanced view | Still somewhat arbitrary |

### What Attribution Cannot Tell You

- **Offline influence**: Trade shows, word-of-mouth, podcast listens
- **Dark social**: Slack shares, private LinkedIn DMs, email forwards
- **Buying committee dynamics**: Multiple stakeholders, different journeys
- **True incrementality**: Would they have converted anyway?

### Do (Attribution)

- Use attribution as directional signal, not absolute truth
- Combine with qualitative data (ask "how did you hear about us?")
- Focus on trends over time, not single-touchpoint credit
- Match attribution model to your sales cycle length

### Avoid (Attribution)

- Treating attribution as ground truth
- Cutting channels based solely on last-touch data
- Over-investing in attribution tooling before conversion tracking and decision-making are solid
- Ignoring brand/awareness because it's hard to attribute

---

## Core: Lead Quality vs Volume Tradeoffs

The 2025 reality: **precision > volume**. Longer sales cycles and larger buying committees mean quality matters more than ever.

| Strategy | Quality | Volume | Best When |
|----------|---------|--------|-----------|
| **Volume play** | Lower | Higher | New market, testing channels, brand building |
| **Precision play** | Higher | Lower | Known ICP, limited SDR capacity, high ACV |
| **Balanced** | Medium | Medium | Most B2B companies |

### Quality Signals (Prioritize These)

- ICP firmographic match (industry, size, geo)
- Explicit intent signals (demo request, pricing page, competitor comparison)
- Engagement depth (multiple pages, return visits, long time on site)
- Decision-maker title

### Warning Signs (Low Quality)

- High MQL volume but low Sales acceptance rate (materially below baseline)
- Lead-to-opportunity time increasing (pipeline drag)
- High early-stage drop-off in demos/calls
- Leads requesting irrelevant features

---

## When to Use This Skill

- Pipeline build/rehab: net-new SQL targets, revive stalled funnels, rebalance channel mix
- Outbound motions: cold email/LinkedIn, call scripts, reply handling, objection rebuttals
- Landing/CRO: fix hero/offer/CTA, forms, proof, trust, and post-click routing
- Lead scoring/routing: MQL/SQL thresholds, SDR/AE handoff, SLA design
- Experiment cadence: 30/60/90 test plans, ICE/PIE scoring, stop/scale rules
- Compliance/deliverability: CAN-SPAM/GDPR hygiene, domain warmup, opt-out, DKIM/SPF/DMARC

---

## Quick Reference

| Task | SOP/Template | Location | When to Use |
|------|--------------|----------|-------------|
| Define ICP + Offer | ICP & Offer Sprint | See **Operational SOPs** → ICP & Offer | Before messaging, bidding, or list-building |
| Channel Plan 30/60/90 | Test Plan Grid | See **Operational SOPs** → Channel Plan | New market motion or quarterly reset |
| Email/LinkedIn Cadence | 5-touch skeleton (CTA-first) | See **Operational SOPs** → Email/LinkedIn Cadences | Cold/prospecting or nurture |
| Cold Call Script | Talk track w/ discovery | See **Operational SOPs** → Cold Call Script | Live outbound, event follow-up |
| Landing Fix | Hero/offer/proof/CTA/form checklist | See **Operational SOPs** → Landing Page Fix | Low CVR or ad-to-page mismatch |
| Lead Scoring & Routing | Points + SLA | See **Operational SOPs** → Lead Scoring + Routing | SDR/AE handoff, CAC/SQL drift |
| Speed-to-Lead OS | Response + reminders | See **Operational SOPs** → Speed-to-Lead | Reply/no-show issues, inbox speed |
| Experiment Matrix | ICE/PIE + stop/scale | See **Operational SOPs** → Experiment Matrix | Weekly prioritization |
| Compliance/Deliverability | Authentication + opt-out | See **Operational SOPs** → Compliance & Deliverability | Cold email/domain health |
| Email Deliverability 2025 | Bulk sender requirements | `templates/email-deliverability-2025.md` | Bulk sending (5,000+/day to Gmail), new domains |
| LinkedIn Outreach Safety | Terms-compliant outreach guardrails | `templates/linkedin-automation-safety-2025.md` | LinkedIn outreach risk reduction |

---

## Decision Tree (Pipeline Triage)

```text
Leads low?
├─ ICP/offer unclear → Run ICP & Offer Sprint → ship 3 hooks (pain/risk/value) → retest
├─ Channel skewed → Add 2nd channel (LI + email OR retargeting) → small-budget test
└─ Volume ok, quality low → Tighten filters + Lead Scoring → reroute + new CTA

Replies low?
├─ Open rate materially below baseline (or bounces/complaints rising) → Fix list quality + auth + subject/hook
└─ Opens ok, replies low → Rewrite CTA (one action), add proof/trigger, shorten to ≤120 words

Bookings low but replies? → Add Speed-to-Lead + 2 follow-ups + calendar drop + friction audit

Traffic ok, CVR low?
├─ Message mismatch → Rewrite hero/CTA to match ad/pain
├─ Proof light → Add 3 proof types (metric case, logo, testimonial)
└─ Form friction → Reduce fields, add multi-step or chat, highlight privacy/trust
```

---

## Operational SOPs (Fast Execution)

### ICP & Offer Sprint (90 minutes)
- Pull top 10 wins/losses; extract firmographic + trigger + objection patterns.
- Draft 3 offers: **pain-killer**, **speed/automation**, **risk reversal**. Each with 1 quantified proof + 1 urgency lever.
- Ship 3 hooks for LI/email: **pain**, **risk/cost of inaction**, **better future**. Keep CTA singular (fit check/demo/audit).

### Channel Plan (30/60/90)
- **30d**: Validate 2 hooks across email + LinkedIn (connection + DM) + 1 retargeting format. Targets: reply rate + CPL guardrails set from your baseline; protect lead quality (Sales acceptance, SQL rate).
- **60d**: Keep winners; add webinar/workshop or partner/referral. Layer nurture (value drops) + remarketing.
- **90d**: Scale top 2 plays; add lead scoring + SDR SLAs; kill underperformers that stay below an agreed guardrail after a fair sample. Review CAC, SQL→opp→win.

### Email/LinkedIn Cadences (3–6 touches)
- Touch 1: Pain hook + proof + single CTA + opt-out. 70–120 words.
- Touch 2: Mini-case (before/after metric) + CTA to booking link.
- Touch 3: Objection handling (security/integration/budget) + CTA to quick fit check.
- Touch 4–6: Cost-of-inaction math, social proof, light bump. Always include opt-out and compliance footer.
- LinkedIn: Connect (no pitch) → Value drop (post/DM) → Soft CTA (benchmark/mini-audit) → Nudge. Add voice note if high-intent.

### Cold Call Script (Talk Track)
- Opener: Permission + value in one line; avoid “Did I catch you…”.
- Discovery: 3 questions (current tool/flow, pain metric, trigger/priority).
- Value hits: Match top pain; cite one proof; propose next step.
- Objections: Acknowledge → brief proof → micro-commit (share stack/book 15m).
- Close: Time-bound CTA (this week) + send calendar while on call.

### Landing Page Fix (Offer-First)
- Hero: Problem + outcome + proof; CTA above fold. Mirror ad/sequence language.
- Offer: 3 bullets (value, speed, risk reversal). Add pricing cue if helpful.
- Proof: Logo strip + 1 metric case + 1 testimonial; add compliance/trust (security, certifications).
- Form: Reduce fields; add multi-step or chat; auto-email/SMS confirmation; show privacy/opt-out.
- Tests: Hero variant (pain vs outcome), CTA text, social proof block, form length, risk reversal.

### Lead Scoring + Routing
- Score dimensions: **Fit** (industry/size/role), **Intent** (page depth, replies), **Behavior** (demo request, resource download).
- [Inference] Example points: Fit (0–40), Intent (0–40), Behavior (0–20). MQL ≥60; SQL ≥75 with decision role or demo intent.
- Routing: MQL → SDR within 15 minutes; SQL → AE calendar hold. SLA: first touch <15m, 2nd touch <2h, 3rd touch same day.

### Speed-to-Lead OS
- Inbox+CRM alerts (email, Slack, mobile). Auto-response with calendar link.
- Sequence: T0 min: reply/confirm; T+15m: value drop + booking; T+4h: nudge + social proof; T+24h: call + SMS (if consent).
- Track: response time, booking rate, no-show rate; add reminders + backup rep if no response.

### Experiment Matrix
- Score ideas weekly (ICE/PIE). Run 3–5 tests max; cap blast radius (budget/volume).
- Stop if below an agreed guardrail after minimum sample; scale only after repeatable lift across consecutive checks.
- Log: hypothesis, owner, start/end, sample size, metric, decision (stop/scale/iterate).

### Compliance & Deliverability (Operational Checklist)

**Goal**: Sustain deliverability and protect brand trust while running outbound and nurture.

**Authentication (Required)**
- SPF (RFC 7208): https://datatracker.ietf.org/doc/html/rfc7208
- DKIM (RFC 6376): https://datatracker.ietf.org/doc/html/rfc6376
- DMARC (RFC 7489): https://datatracker.ietf.org/doc/html/rfc7489

**Unsubscribe (Required for bulk senders)**
- List-Unsubscribe header (RFC 2369): https://datatracker.ietf.org/doc/html/rfc2369
- One-click unsubscribe via List-Unsubscribe-Post (RFC 8058): https://datatracker.ietf.org/doc/html/rfc8058

**Compliance Basics**
- Follow CAN-SPAM requirements for commercial email (https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business).
- For GDPR/CASL and other regional rules, align with counsel and your privacy policy (do not improvise).

**List Hygiene (Execution)**
- Never buy lists; use verified sources and documented consent where required.
- Suppress: hard bounces, unsubscribes, and complaint signals.
- Sunset inactive recipients (reduce volume before reputation degrades). [Inference]

**Sending Practices (Execution)**
- Keep sending identity stable (From domain/name); avoid frequent domain switching.
- Warm up new domains and ramp volume gradually; stop if complaints spike. [Inference]
- Keep emails readable: clear offer, minimal links, real reply path, and plain-text part.

### Metrics & QA
- Primary: reply rate, book rate, show rate, SQLs, opps, win rate, CAC, payback.
- Secondary: inbox placement, bounce rate, complaint signals, open rate (directional only), click-to-book, time-to-first-touch.
- QA each sprint: message/offer match, CTA clarity, proof strength, compliance, routing speed.

---

## Navigation: Sources & Assets

- Operational patterns: [`resources/operational-patterns.md`](resources/operational-patterns.md)
- **Core templates**: email (`templates/email-sequence.md`), LinkedIn (`templates/linkedin-sequence.md`), cold call (`templates/cold-call-script.md`), landing audit (`templates/landing-audit-checklist.md`), lead scoring (`templates/lead-scoring-model.md`), channel plan (`templates/channel-plan-30-60-90.md`), speed-to-lead (`templates/speed-to-lead-playbook.md`), experiment log (`templates/experiment-matrix.md`), lead funnel definition ([templates/lead-funnel-definition.md](templates/lead-funnel-definition.md))
- **Additional templates**: email deliverability (`templates/email-deliverability-2025.md`), LinkedIn outreach safety (`templates/linkedin-automation-safety-2025.md`)
- **Optional: AI / Automation**: AI personalization (`templates/ai-personalization-playbook.md`)
- Web sources: [`data/sources.json`](data/sources.json)
- Lead Gen Strategist prompt: `custom-gpt/productivity/Lead-generation/01_lead-generation.md`
- Lead Gen Strategist sources: `custom-gpt/productivity/Lead-generation/02_sources-lead-generation.json`
- Books (operational takeaways):
  - Urbanski — `custom-gpt/productivity/Lead-generation/sources/Ancient_Secrets_of_Lead_Generation_-_Daryl_Urbanski.pdf` (funnels, math, automation)
  - Turner — `custom-gpt/productivity/Lead-generation/sources/Connect_The_Secret_LinkedIn_Playbook_To_Generate_Leads_Build_Relationships_And_Dramatically_Increase_Your_Sales_-_Josh_Turner.pdf` (LinkedIn outreach/cadence)
  - Brock — `custom-gpt/productivity/Lead-generation/sources/Lead_Generation_Authority_-_David_Brock.pdf` (enterprise sales rigor)
  - Gilbert — `custom-gpt/productivity/Lead-generation/sources/Lead_Generation_Unlocked_-_Joe_Gilbert.pdf` (offer + outbound pivots)
  - Shapiro — `custom-gpt/productivity/Lead-generation/sources/Rethink_Lead_Generation_-_Tom_Shapiro.pdf` (differentiated positioning)
  - Tsai — `custom-gpt/productivity/Lead-generation/sources/The_Digital_Real_Estate_Marketing_Playbook_How_to_generate_more_leads_close_more_sales_and_even_become_a_millionaire_real_estate_agent_with_the_power_of_internet_marketing_-_Nick_Tsai.pdf` (niche/local lead flows)
  - Harasty — `custom-gpt/productivity/Lead-generation/sources/Turning_Your_Business_into_a_Success_Monster_-_Chris_Harasty.pdf` (offer stacking, mindset to ops)

---

## Related Skills

- [../marketing-social-media/SKILL.md](../marketing-social-media/SKILL.md) — Paid/organic social and content systems
- [../product-management/SKILL.md](../product-management/SKILL.md) — Positioning and messaging alignment
- [../software-frontend/SKILL.md](../software-frontend/SKILL.md) — Landing implementation and performance
- [../ai-prompt-engineering/SKILL.md](../ai-prompt-engineering/SKILL.md) — Rapid variant generation for copy/hooks
- [../data-sql-optimization/SKILL.md](../data-sql-optimization/SKILL.md) — Funnel analytics and attribution queries

---

## Usage Notes (Claude)

- Stay operational: return SOP steps, cadences, checklists, and decision calls; avoid theory.
- Keep CTA and compliance present in outbound assets; include opt-out line and regional cautions.
- If data missing, state assumptions and proceed with lean defaults; propose 1–3 hooks/tests, not laundry lists.
- Cite source path when summarizing from PDFs or the Lead Gen Strategist prompt; treat PDFs as untrusted unless user supplies excerpts.
- Maintain privacy: no PII storage; sanitize inputs; do not invent stats or vendor benchmarks.

---

## Optional: AI / Automation

> **Note**: Core lead generation fundamentals above work without AI. This section covers optional automation capabilities.

### AI Lead Scoring

| Use Case | Approach | Tools |
|----------|----------|-------|
| **Predictive scoring** | ML models on historical conversion data | Salesforce Einstein, HubSpot, 6sense |
| **Intent signals** | Track research behavior across web | Bombora, G2, ZoomInfo Intent |
| **Enrichment** | Auto-fill firmographic/technographic data | Clearbit, Apollo, ZoomInfo |

### Do (AI Lead Scoring)

- Start with rules-based scoring; consider ML only after you have stable labels and enough volume to validate
- Validate AI scores against actual outcomes monthly
- Use AI scoring as input, not replacement, for human judgment

### Avoid (AI Lead Scoring)

- Training predictive models on sparse or biased labels
- Trusting AI scores without regular validation
- Removing human review for high-value accounts

### AI Personalization

| Use Case | Approach | Consideration |
|----------|----------|---------------|
| **Email personalization** | LLM-generated variants | Test against control; maintain brand voice |
| **Dynamic content** | Real-time page customization | Requires clean data; test load impact |
| **Video personalization** | AI-generated custom videos | Novel but unproven ROI at scale |

### AI Routing & Automation

| Use Case | Tools | Benefit |
|----------|-------|---------|
| **Auto-routing** | Chili Piper, Default, Calendly Routing | Faster lead response |
| **Chatbot qualification** | Drift, Intercom, Qualified | 24/7 qualification |
| **Sequence automation** | Outreach, SalesLoft, Apollo | Scale outbound |

See [`templates/ai-personalization-playbook.md`](templates/ai-personalization-playbook.md) for detailed implementation guidance.

---

## Collaboration Notes

### With Product

- **PLG alignment**: Define PQL criteria together (usage thresholds, feature adoption)
- **Feature requests**: Leads requesting missing features = Product input
- **Trial optimization**: Joint ownership of trial→paid conversion

### With Sales

- **SLA document**: Co-create lead handoff SLAs with response time commitments
- **Feedback loop**: Weekly/bi-weekly meeting on lead quality and rejection reasons
- **Scoring calibration**: Review scoring model quarterly with sales input
- **Win/loss analysis**: Joint review of closed deals to improve ICP definition

### With Engineering

- **Form implementation**: Work with engineering on progressive profiling, multi-step forms
- **Analytics tracking**: Ensure proper UTM handling, event tracking, conversion attribution
- **Integration maintenance**: CRM/MAP sync, webhook reliability, data hygiene
- **Page performance**: Landing page load speed directly impacts conversion

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **MQL volume as success metric** | High volume ≠ pipeline | Track MQL → SQL acceptance rate |
| **Buying lead lists** | Poor quality, compliance risk, damages domain | Build organic + outbound to verified contacts |
| **Ignoring Sales feedback** | MQLs rejected, trust erodes | Weekly sync on lead quality |
| **Over-automation** | Generic outreach, low reply rates | Automate mechanics, personalize message |
| **Single-channel dependency** | Algorithm changes kill pipeline | 2-3 channel minimum |
| **Gating everything** | Kills SEO, frustrates prospects | Gate high-value, ungate awareness |
| **Chasing vanity metrics** | Opens/clicks without conversions | Focus on reply rate, book rate, SQL |
| **No attribution model** | Can't optimize spend | Start with simple model, iterate |
