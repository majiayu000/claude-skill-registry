---
name: prd-v10-testimonial-collector
description: >
  Systematically harvest short testimonials from customers via NPS, milestones, post-purchase,
  and email during PRD v1.0 Market Adoption. Triggers on requests to collect testimonials,
  set up social proof harvest, gather customer quotes, or when user asks "how do we get
  testimonials?", "social proof harvest", "NPS responses", "testimonial wall", "customer quotes",
  "post-purchase survey", "milestone follow-up". Outputs CFD-TST-* testimonial entries and
  GTM-TST-* placement assets.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Testimonial Collector

Position in workflow: v1.0 Case Study Builder → **v1.0 Testimonial Collector** → GTM channels (placement)

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | One trigger (e.g., NPS promoters) + collection email + 5–10 testimonials processed |
| **standard** | 3 triggers (NPS, milestone, post-purchase) + processing workflow + consent management + per-placement formatting |
| **deep** | 5+ triggers + automated harvest + sentiment-segmentation + per-segment placement targeting + measurement loop |

## What This Does

Systematically harvests **short-form testimonials** — 1–3 sentence quotes with name + role + logo — and processes them into placement-ready assets. Testimonials are the lower-effort complement to case studies: they don't carry a full story but they multiply social proof on landing pages, pricing pages, ad creative, and outreach.

This skill solves the "we have happy customers but no quotes" problem — most teams have plenty of positive feedback in support tickets, NPS responses, and renewal calls, but never capture it as marketing-ready assets. The fix is a system, not heroic effort.

## How It Works

1. **Identify collection triggers** — Each trigger is an event that suggests the customer is in a moment to share positive feedback:
   - **NPS Promoter response** (score 9–10) — Lowest-friction; they already wrote feedback
   - **Activation milestone** (Day 30 / Day 90 active) — They've seen value by now
   - **Post-purchase / post-upgrade** — Decision fresh in mind
   - **Renewal** — Strong signal of ongoing value
   - **Support resolution (positive)** — Acute "you saved my day" moment
   - **Referral from customer** — They already advocated
2. **Build per-trigger collection mechanism**:
   - NPS Promoter → automated email asking permission to use response + adding 1-question follow-up
   - Milestone → in-app prompt or email with one-line ask
   - Post-purchase → email 7 days after purchase
   - Renewal → CSM-led ask during renewal call
   - Support → followup in support thread after positive resolution
3. **Process incoming testimonials** — Each goes through:
   - Consent confirmation (scope: name? role? logo? use anywhere?)
   - Light edit for clarity (their voice; don't rewrite)
   - Tag by segment fit (in-beachhead / adjacent / off-segment)
   - Tag by outcome theme (speed / cost / activation / quality / etc.)
4. **Place in marketing surfaces** — Per testimonial:
   - Pricing page (logo + quote)
   - Landing page hero (1 prominent quote)
   - Feature pages (segment-relevant quotes)
   - Ad creative (testimonial-style ads)
   - Email signatures / sales decks
   - Investor decks
5. **Measure placement performance** [standard+] — Some testimonials convert; some don't. Track per-placement conversion to identify which quotes earn their spot.

## Example

B2B SaaS, 3 collection triggers active.

**Trigger 1: NPS Promoter (9–10)**.
NPS run quarterly. Promoters get followup email:

> *Thanks for the 10! Your response — "Cut our reporting time in half" — would be a powerful testimonial for our pricing page. May we use it with your name and role? Reply YES and we'll send back the version we'd publish for your approval.*

Auto-fires when NPS response submitted with score ≥ 9.

**Trigger 2: Day-30 active milestone**.
In-app prompt at first login after Day 30 active:

> *You've been active for a month! In one sentence, what's working best?* → [text box] → [Submit + permission checkbox]

**Trigger 3: Post-purchase (Day 7)**.
Email 7 days after first paid charge:

> *Quick favor — what convinced you to upgrade? Your answer might appear (with your permission) on our pricing page.*

**Processing**: Inbound testimonials enter a triage doc. Per testimonial:
- Consent confirmed (scope: name / role / logo / anywhere)
- Light edit (clarity only — kept their voice)
- Segment tag (in-beachhead: yes/no)
- Theme tag (speed / cost / activation / quality)
- Placement decision (pricing / landing / feature page / ad / multi)

**Placement**: Pricing page logo wall expanded with 6 new testimonials in the beachhead segment. A/B test the hero-section quote on landing pages.

## What You Get Back

- **CFD-TST-\* entries** — One per testimonial; the durable record with consent, source, segment, theme
- **GTM-TST-\* entries** — Per-placement formatting (the placed quote with surrounding context)
- **Consent records** — Customer-by-customer scope and version history
- **Placement-performance log** — Per-quote conversion rate (which testimonials earn their spot)

## When to Use It

| Trigger | Mode |
|---------|------|
| First testimonial harvest system (none in place) | standard |
| Quarterly NPS run + harvest | quick |
| Pricing page redesign needs more social proof | standard |
| Landing page A/B test needs quote variants | quick |
| Pre-investor / pre-Series A push for logo + quote density | deep |
| New segment expansion (need segment-specific testimonials) | deep |

## Consumes

- **CFD-\* customer feedback** (all sources, especially v0.9 feedback loop) — Raw inbound testimonial material
- **NPS / CSAT data** (from v0.9 Feedback Loop Setup) — Promoter responses are the highest-yield source
- **ADO-REF-\* candidates** — Reference accounts already in cultivation are testimonial-eligible
- **PER-\* personas** + **ADO-BEACHHEAD-\*** — Segment tagging
- **BR-POS-\*** — Tone constraints; testimonials shouldn't contradict positioning

## Produces

- **CFD-TST-\* entries** in `SoT/SoT.customer_feedback.md`
- **GTM-TST-\* entries** (with Type=Testimonial-Placement) per placement
- **Consent records** — Append-only log with scope and version
- **Placement-performance metrics** — Per-quote A/B data feeding back into selection

## Output Template

```
CFD-TST-XXX: Testimonial — [Customer name]
Type: Testimonial
Date received: YYYY-MM-DD
Source trigger: [NPS-promoter | Day-30-milestone | Post-purchase | Renewal | Support | Referral]
Customer: [Name, Role, Company, Logo]

Verbatim text:
  "[The actual quote, lightly edited for clarity only]"

Original text (for audit):
  "[The raw response]"

Tags:
  Segment fit: [In-beachhead | Adjacent | Off-segment]
  Theme: [Speed | Cost | Activation | Quality | Reliability | Specific-use-case]
  Length: [Words / chars]

Consent:
  Scope: [Name? Role? Logo? Use-anywhere?]
  Approved by: [Customer name]
  Approved date: YYYY-MM-DD
  Approved version: vX

Placement eligibility:
  - Pricing page logo wall: [Yes/No]
  - Landing page hero: [Yes/No]
  - Feature page (which): [Yes/No]
  - Ad creative: [Yes/No]
  - Sales deck: [Yes/No]
  - Investor deck: [Yes/No]

Linked IDs: PER-XXX (segment), ADO-REF-YYY (if cultivated), CFD-ZZZ (interview source if applicable)
```

```
GTM-TST-XXX: Testimonial Placement — [Quote summary]
Type: Testimonial-Placement
Source: CFD-TST-AAA
Placement: [URL or surface, e.g., "/pricing — hero zone"]
Format: [Quote + Name + Role + Logo | Quote + Logo only | Quote in card]

Surrounding context:
  [What this testimonial sits next to — headline, CTA, product feature]

A/B test (if active):
  Variant A: [This testimonial]
  Variant B: [Alternative]
  Metric: [Click-through, signup-rate, etc.]
  Started: YYYY-MM-DD

Performance (if measured):
  [Per-quote conversion data]

Linked IDs: CFD-TST-AAA (source), GTM-YYY (page channel), KPI-ZZZ (placement metric)
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Heroic one-time harvest** | "We collected 20 testimonials in a sprint, then stopped" | Triggers run continuously; harvest is a system, not a project |
| **No consent record** | Publishing without explicit approval | Consent record per testimonial, scope-explicit |
| **Marketing rewrite** | "I love [product]" rewritten from "It's pretty useful" | Light edits for clarity only; their voice |
| **No segment tagging** | All testimonials placed everywhere | Segment-relevant placement converts better; tag and target |
| **Stale walls** | Pricing page testimonials from 2 years ago | Refresh quarterly; rotate underperformers |
| **No placement measurement** | All testimonials treated as equally good | Some quotes convert 3× others; measure and prune |
| **Anonymous testimonials** | "VP at major fintech" with no name/logo | Pragmatists discount anonymous; named + logo or skip |
| **Off-segment testimonials during chasm crossing** | Visionary-startup quotes on a page targeting enterprise pragmatists | In-segment placements only during chasm crossing |

## Quality Gates

Before placing testimonials:

- [ ] Consent on record (scope explicit)
- [ ] Customer name + role + logo (or rationale for less)
- [ ] Segment tag applied
- [ ] Theme tag applied
- [ ] Light edit only (their voice preserved)
- [ ] Placement matches segment fit (in-beachhead testimonials for pragmatist surfaces)
- [ ] BR-POS-* constraints honored (no contradiction with positioning)
- [ ] Refresh cadence committed (quarterly minimum)

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Launch Channels (ORB)** | Testimonials are Owned-channel content + Borrowed-channel ad creative | Pricing-page testimonials = Owned; testimonial-style ads = Paid-Borrowed |
| **Alternatives Pages** | "Pick us if..." sections feature segment-relevant testimonials | Migration-from-X testimonial anchors the alt page |
| **Case Study Builder** | Strong testimonials surface case-study candidates | Repeat testimonialer with strong outcome → case study |
| **Cold Outreach (Tiered)** | Testimonials cited in Touch 2/3 of sequences | Tier 2 email includes in-segment testimonial |
| **Feedback Loop Setup** | Testimonial sources tie back to feedback channels | NPS promoters feed both feedback and testimonial flow |
| **Investor / Sales decks** | Logo wall + theme-curated testimonials | "Customers in segment X say..." |

## Detailed References

- BrianRWagner's `testimonial-collector` skill (ai-marketing-claude-code-skills)
- Sean D'Souza, *The Brain Audit* (using testimonials to overcome buying objections)
- Joanna Wiebe, Copy Hackers — testimonial-driven landing pages
- (No bundled `references/` — testimonials are the artifact)
