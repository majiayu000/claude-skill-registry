---
name: prd-v10-case-study-builder
description: >
  Build customer case studies as marketing and chasm-crossing reference assets during PRD v1.0
  Market Adoption. Triggers on requests to build case studies, produce customer stories, create
  reference content, or when user asks "build a case study", "customer story", "reference
  account", "case study interview", "before/after story", "social proof page", "logo wall".
  Outputs CFD-CASE-* evidence entries, GTM-CASE-* marketing assets, and updates ADO-REF-* with
  story status.
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

# Case Study Builder

Position in workflow: v1.0 Mom Test Interview → **v1.0 Case Study Builder** → v1.0 Testimonial Collector, GTM channels

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | Short-format case (testimonial + 1-paragraph story + logo); single placement |
| **standard** | Full case study (1,500 words) + short and medium derivatives + customer-approved + 3 channel placements |
| **deep** | Long-form case (2,500–4,000 words) + multi-format derivatives (PDF, blog, video, conference talk) + measurable outcome quantified + outcome-attribution interview |

## What This Does

Turns customer success — already documented as CFD-* evidence and ADO-REF-* candidates — into structured **case studies**. Case studies are the pragmatist buyer's #1 reference signal: they need to see a customer in their segment achieving the outcome they want, with enough detail to make it credible.

This is an **operational** "doing" skill, not a strategy skill. The strategic question (which segment, what story angle, what outcome to highlight) was answered by [prd-v10-chasm-adoption-moore](../prd-v10-chasm-adoption-moore/SKILL.md). This skill produces the artifact.

## How It Works

1. **Identify candidate customers** — Pull from ADO-REF-* candidates and CFD-* entries with strong outcome quantification. Must satisfy:
   - In-beachhead (or in an adjacent segment where the story would still resonate)
   - Has a quantifiable outcome to talk about
   - Willing to be public (consent path is clear)
2. **Run the case-study interview** — Extended Mom Test interview (45–60 min), focused on:
   - Before-state (specific past: what life was like, what tools, what cost)
   - Trigger (what changed; why they evaluated alternatives)
   - Evaluation (who they considered; how they chose)
   - Implementation (what happened in onboarding; what was hard)
   - After-state (specific present: quantified outcome, time/money saved, what they can do now they couldn't)
3. **Structure the story** — Situation → Complication → Question → Resolution (the McKinsey SCQR pattern):
   - **Situation**: where they were before
   - **Complication**: what broke / changed / hit a wall
   - **Question**: what they needed to figure out
   - **Resolution**: how they solved it (your product as one part of the answer, ideally credibly)
4. **Quantify outcome** — Specific numbers beat vague claims:
   - "Cut tier-selection time from 3 days to 30 minutes" beats "much faster"
   - "Saved $12k/year on tool consolidation" beats "saves money"
   - "85% activation rate (industry average 35%)" beats "great activation"
5. **Get customer review** — Send draft to customer for accuracy + tone + legal. Iterate until approved.
6. **Produce in 3 formats**:
   - **Short** (testimonial — 1–2 sentences + name + role + logo): for landing pages, pricing page, ad creative
   - **Medium** (1-paragraph + 3 bullet outcomes + logo + linked deeper): for "Customers" page, social, email
   - **Long** (1,500–2,500 word case study): for blog, sales enablement, sales call followup

## Example

Customer: Acme Logistics (beachhead segment: freight forwarders, 50-200 employees, US PNW). ADO-REF-002.

**Interview**: 50 minutes with Acme's VP Operations.

**Quantified outcome**:
- Tier-selection time: 3 days → 30 min (90% reduction)
- Annual savings from tool consolidation: $14k
- Onboarding time per new hire: 2 weeks → 3 days (after migrating to product)

**SCQR**:
- **Situation**: Acme used 4 disjointed tools to track shipments, with manual export every Friday for ops reporting
- **Complication**: Two new hires + a Q3 customer surge meant the manual export bottlenecked the team; ops director was working Saturdays to keep the dashboards current
- **Question**: How could Acme consolidate tooling without disrupting an in-flight Q4 customer onboarding?
- **Resolution**: Acme migrated to [product] over 3 weeks; consolidated 4 tools to 1; automated the Friday export. VP Operations reclaimed 6 hours/week. New hires onboard in 3 days instead of 2 weeks.

**Three formats produced**:
- **Short**: *"We replaced 4 tools with [product] and cut new-hire onboarding from 2 weeks to 3 days." — [Name], VP Ops, Acme Logistics*
- **Medium**: 1-paragraph + 3 bullet outcomes + Acme logo + "Read the full story →"
- **Long**: 1,800-word blog case study with screenshots, quotes, before/after metrics, and an embedded testimonial video.

## What You Get Back

- **CFD-CASE-\* entries** — One per case-study interview; the durable evidence record
- **GTM-CASE-\* entries** (one per produced format) — Marketing assets with placement plan
- **Updates to ADO-REF-\* entries** — Reference status: "draft pending" → "approved" → "published"
- **Customer approval record** — Signed approval + version-controlled draft history

## When to Use It

| Trigger | Mode |
|---------|------|
| First reference customer in beachhead is ready to talk | standard |
| Chasm-crossing push needs 3+ in-segment case studies | deep |
| Pricing-page logo wall expansion | quick (short format only) |
| Sales enablement asset for new segment | standard |
| Investor / partner update | standard |
| Customer success milestone (e.g., 1-year anniversary) | quick |

Do **not** use for: customers outside beachhead during chasm crossing (their story doesn't resonate with pragmatists); customers without consent (legal risk); customers without quantifiable outcomes (story will feel vague).

## Consumes

- **CFD-\* customer evidence** (Mom Test discipline) — Source for candidate selection
- **ADO-REF-\* candidates** (from prd-v10-chasm-adoption-moore) — Cultivated reference targets
- **ADO-BEACHHEAD-\*** — Defines "in-segment" for case priority
- **KPI-\* outcomes** — Defines what "outcome" means; case quantification must speak to these
- **GTM-\* positioning + offer** — Tone, voice, and value claims must match positioning
- **BR-POS-\*** — Constraints (e.g., "no enterprise procurement language")

## Produces

- **CFD-CASE-\* entries** in `SoT/SoT.customer_feedback.md`
- **GTM-CASE-\* entries** (with Type=Case-Asset) for each produced format
- **ADO-REF-\* updates** — Status, placement, consent tracking
- **CFD-\* gaps surfaced** — If outcome can't be quantified, log as research gap

## Output Template

```
CFD-CASE-XXX: Case Study — [Customer Name]
Type: Case-Study
Date: YYYY-MM-DD
Customer: [Logo / company name]
Customer fit: [In-beachhead | Adjacent segment]
Interview length: [minutes]
Interviewer: [Name]

Quantified outcome (the proof):
  Before: [Specific number / state]
  After: [Specific number / state]
  Delta: [%change or $ value]
  Time horizon: [over what period]

Story (SCQR):
  Situation: [Where they were before]
  Complication: [What changed / broke / hit a wall]
  Question: [What they needed to figure out]
  Resolution: [How it got solved — your product as part of the answer]

Quotes (verbatim, approved):
  - "[Quote]" — [Name, Role]
  - "[Quote]" — [Name, Role]

Customer approval:
  Approved by: [Name, Role]
  Approved version: vX
  Date: YYYY-MM-DD
  Scope: [logo only | quote | full case study | on-stage]

Linked formats:
  Short: GTM-CASE-AAA
  Medium: GTM-CASE-BBB
  Long: GTM-CASE-CCC

Linked IDs: ADO-REF-XXX (cultivation), PER-YYY (segment fit), KPI-ZZZ (outcome), CFD-AAA (interview source)
```

```
GTM-CASE-XXX: Case-Study Asset — [Format]
Type: Case-Asset
Format: [Short | Medium | Long]
Channel: [Landing page | Pricing page | Blog | Sales deck | Email | Ad creative]
Owner: [Person / role]
Status: [Draft | In review | Approved | Live]

Content: [The actual asset content — quote, paragraph, full case]

Placement plan:
  - [URL or section, e.g., "/pricing — Acme logo wall, position 3"]

Attribution: utm_campaign=case-<customer>

Linked IDs: CFD-CASE-AAA (parent case), ADO-REF-BBB (reference account), GTM-YYY (positioning)
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **No quantified outcome** | "Customer loves us!" | Specific numbers or skip; vague cases don't move pragmatists |
| **Wrong segment** | Featuring a startup case to a pragmatist enterprise audience | In-segment cases only during chasm crossing |
| **No customer approval on record** | Published with assumed approval | Always get signed approval; preserve version history |
| **Marketing voice override** | Customer's actual words rewritten into your marketing tone | Their voice; light edits for clarity only |
| **Single-format publish** | Long-form blog only | Three formats: short for placement, medium for browsing, long for depth |
| **One-and-done** | Case study published, never updated | Refresh quarterly with new outcome data; cases stale fast |
| **Featuring failures-rebranded-as-wins** | "We rebuilt their entire infrastructure" hides "we replaced a failed implementation" | Don't dress up bad stories; pragmatists smell it |

## Quality Gates

Before publishing:

- [ ] Customer in-beachhead or rationale for cross-segment placement
- [ ] Outcome quantified with specific numbers
- [ ] SCQR structure complete (Situation, Complication, Question, Resolution)
- [ ] Verbatim quotes with name + role
- [ ] Customer approval on record (scope explicit)
- [ ] Three formats produced (short, medium, long) — or rationale for fewer
- [ ] Placement plan per format
- [ ] Voice matches GTM- positioning (and customer's actual words)
- [ ] BR-POS-* constraints honored

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Launch Channels (ORB)** | Cases become Owned and Borrowed channel content | Blog case = Owned; co-marketing case = Borrowed |
| **Alternatives Pages** | Cases anchor "when to pick us" sections with real proof | Page references Acme case for migration-from-X story |
| **Cold Outreach (Tiered)** | Cases referenced in Touch 3 of sequences | Tier 1 outreach mentions in-segment case study |
| **Testimonial Collector** | Short-format derivatives are testimonial-shaped | Auto-eligible for testimonial walls |
| **AEO Audit** | Cases become AI-citation sources | High-traffic case pages cited by AI search |
| **Sales / Investor** | Direct asset for sales calls and investor updates | "Here's how Acme uses [product]" |

## Detailed References

- BrianRWagner's `case-study-builder` skill (ai-marketing-claude-code-skills)
- Joe Pulizzi, *Epic Content Marketing* (case study as content)
- Annette Franz, *Customer Understanding* (interview discipline)
- McKinsey's SCQR (Situation/Complication/Question/Resolution) framework
- (No bundled `references/` — the case study itself is the artifact)
