---
name: competitive-battlecard-creation
description: Build sales battlecards with feature comparisons, objection handling scripts, positioning statements, and win themes for competitive deal scenarios. Use when the user requests competitive battlecard creation or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Competitive Battlecard Creation

Build structured sales battlecards that arm reps with everything they need to win against specific competitors. This skill researches competitor products, maps feature-level comparisons, drafts objection handling scripts, creates positioning statements and win themes, and packages the output into a quick-reference format reps can pull up mid-call.

## Workflow

1. **Research the Competitor** — Gather current intelligence on the competitor: product capabilities, pricing model, recent product launches, G2/Gartner reviews, customer complaints, leadership changes, and public roadmap signals. Pull from their website, changelog, job postings (which reveal investment areas), and customer review sites.

2. **Identify Strengths and Weaknesses** — Map the competitor's genuine strengths (don't ignore them — reps need to acknowledge what the competitor does well) and exploitable weaknesses. Categorize weaknesses as product gaps, architectural limitations, pricing disadvantages, support deficiencies, or market positioning misalignment.

3. **Map Feature Comparison** — Build a side-by-side feature comparison across the dimensions that matter most to your buyers. Use objective, verifiable claims. Mark each feature as strong advantage, slight advantage, parity, or disadvantage. This table becomes the centerpiece of the battlecard.

4. **Draft Objection Handlers** — Write talk tracks for the 5–8 most common objections reps hear when competing against this vendor. Each handler follows a structure: acknowledge the objection, reframe the conversation, deliver your counter-point with proof, and bridge to your differentiator.

5. **Create Win Themes and Talk Tracks** — Develop 3–4 high-level win themes (e.g., "Total cost of ownership," "Time to value," "Scale without complexity") with supporting talk tracks that connect your strengths to the prospect's priorities. Include landmine questions reps can plant early in the deal to steer evaluation criteria in your favor.

## Usage

Provide the competitor name, your product's key differentiators, the target buyer persona, and any known competitive dynamics. The skill outputs a complete battlecard.

**Example prompt:**
> Create a battlecard for competing against DataVault Analytics. We sell CloudMetrics, a real-time analytics platform. Our advantages are real-time processing, simpler pricing, and better onboarding. Their advantages are brand recognition and deeper enterprise compliance features. Target buyer is VP of Data at mid-market SaaS companies.

## Examples

### Example 1: Full Competitive Battlecard

**Competitor:** DataVault Analytics
**Our Product:** CloudMetrics
**Target Buyer:** VP of Data at mid-market SaaS (200–1000 employees)

---

**Competitor Snapshot**

- Founded 2012, ~2,000 employees, estimated $180M ARR
- Strong enterprise presence (Fortune 500), weaker in mid-market
- Recent: Raised Series E ($120M), launched AI module in Q3, acquired a data governance startup
- Key reviews theme: Powerful but complex; long implementation cycles; expensive at scale

---

**Feature Comparison**

| Capability | CloudMetrics | DataVault | Advantage |
|---|---|---|---|
| Real-time data processing | Sub-second streaming ingestion | Batch-first with near-real-time add-on | ✅ Strong — Us |
| Time to value | 2-week avg. onboarding | 8–12 week implementation | ✅ Strong — Us |
| Pricing model | Per-query pricing, no seat fees | Per-seat + data volume tiers | ✅ Slight — Us |
| Enterprise compliance (SOX, FedRAMP) | SOC 2 Type II, HIPAA | SOC 2, HIPAA, SOX, FedRAMP | ❌ Slight — Them |
| Pre-built dashboards | 50+ templates | 200+ templates | ❌ Slight — Them |
| Custom SQL exploration | Full SQL with live autocomplete | SQL with limited auto-suggest | ✅ Slight — Us |
| Embedded analytics | Native SDK, white-label ready | Requires partner module ($$$) | ✅ Strong — Us |
| Brand recognition | Growing mid-market presence | Established enterprise brand | ❌ Them |
| Customer support | Dedicated CSM on all plans | CSM only on Enterprise tier | ✅ Slight — Us |

---

**Objection Handlers**

**"DataVault is the industry standard — why would we take a risk on CloudMetrics?"**

Acknowledge: DataVault has built a strong enterprise brand over the past decade — that's real.
Reframe: The question is whether a product built for Fortune 500 complexity is the right fit for a mid-market team that needs speed and simplicity.
Counter: Our mid-market customers go live in 2 weeks vs. DataVault's 8–12 week average. StreamOps, a 300-person SaaS company, evaluated both and chose us specifically because they couldn't justify a 3-month implementation for a 40-person data team.
Bridge: What's your timeline for getting live dashboards in front of stakeholders?

**"DataVault has more compliance certifications."**

Acknowledge: They do hold FedRAMP and SOX certifications that we don't yet carry.
Reframe: For mid-market SaaS companies, SOC 2 Type II and HIPAA cover 95%+ of audit requirements. FedRAMP matters primarily for federal contracts.
Counter: We're on track for SOX certification by Q3. In the meantime, every mid-market customer we've onboarded has passed their compliance audits with our current certifications.
Bridge: Which specific compliance standards does your security team require? Let's map those directly.

**"DataVault's AI module looks impressive."**

Acknowledge: They made a big bet on AI with their Q3 launch — the vision is compelling.
Reframe: First-generation AI features from a batch-oriented platform operate on stale data. Our AI-assisted insights run on real-time streams.
Counter: Two customers who tested DataVault's AI module told us the insights lagged by 4–6 hours because the underlying data pipeline is batch-based. Our anomaly detection fires within seconds of a data shift.
Bridge: How important is real-time alerting to your use case vs. retrospective pattern analysis?

---

**Win Themes**

1. **Speed to value** — "Go live in weeks, not months. Your team starts getting answers on day 14, not day 90."
2. **Real-time by design** — "We were built streaming-first. DataVault bolted on real-time as an afterthought — and the architecture shows."
3. **Mid-market fit** — "You shouldn't need a 5-person implementation team to set up an analytics platform for a 300-person company."

**Landmine Questions:**
- "When you evaluated DataVault, did they quote you an implementation timeline? Ask them what their median mid-market onboarding duration is."
- "Ask DataVault how their AI module handles real-time anomaly detection vs. batch-processed insights."
- "Request DataVault's per-query pricing — they charge per seat, which gets expensive as you democratize data access."

---

### Example 2: Quick-Reference Deal Scenario Card

**Scenario:** Prospect is in final evaluation between CloudMetrics and DataVault. Prospect's main concern is total cost of ownership over 3 years.

**Key plays:**
- Request DataVault's 3-year TCO including implementation services, per-seat growth at 20% annual headcount increase, and add-on module costs (AI, embedded, governance).
- Present our 3-year TCO: per-query pricing scales with usage, not headcount. At 300 employees growing to 500, our cost grows ~15% while their per-seat model grows ~67%.
- Reference customer: PayFlow (fintech, 400 employees) — chose us over DataVault, projected $340K savings over 3 years, went live in 11 days.

**TCO Comparison (estimated, 300-person company growing to 500):**

| Cost Component | CloudMetrics (3-Year) | DataVault (3-Year) |
|---|---|---|
| Platform license | $216,000 | $378,000 |
| Implementation | $0 (self-serve) | $85,000 |
| Add-on modules | Included | $54,000 |
| Dedicated CSM | Included | $36,000 (Enterprise tier) |
| **Total** | **$216,000** | **$553,000** |

## Best Practices

- Update battlecards quarterly at minimum — stale competitive intel is worse than no battlecard because it breeds false confidence.
- Acknowledge competitor strengths honestly; reps who dismiss a well-known competitor lose credibility with informed buyers.
- Write objection handlers in conversational language, not marketing copy — reps need to sound natural on a live call.
- Include landmine questions that reps can plant early in the evaluation to shift criteria toward your strengths before the competitor's demo.
- Tag each claim with a source and date so reps know how fresh the intel is.
- Keep the battlecard to a single scrollable page or two-sided PDF — if reps can't find the answer in 10 seconds, the card is too long.

## Edge Cases

- **Competitor launches a new product mid-deal** — Maintain a rapid-response process where product marketing pushes a battlecard addendum within 48 hours of major competitor announcements.
- **Prospect shares competitor's pricing directly** — Use it to build a live TCO comparison on the call, but never store or redistribute the competitor's proprietary pricing externally.
- **Competitor you've never lost to** — Still build a battlecard. Their presence in a deal changes buyer expectations and evaluation criteria even if they don't win.
- **Multiple competitors in the same deal** — Create a deal-specific composite card that covers all active competitors rather than requiring reps to flip between three separate battlecards.
- **Former competitor customer on your team** — Leverage their insider knowledge for battlecard input, but scrub any confidential or NDA-protected information before publishing.
