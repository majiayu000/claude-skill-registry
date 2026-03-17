---
name: marketing-cro
description: Use when optimizing conversion rates, designing A/B tests, or improving landing pages. Covers A/B testing methodology, landing page optimization, form design, statistical significance, funnel analysis, and CRO prioritization frameworks.
---

# CRO — CONVERSION OPTIMIZATION OS (OPERATIONAL)

Built as a **no-fluff execution skill** for systematic conversion rate optimization.

**Structure**: Core CRO fundamentals first. Advanced testing in dedicated sections. AI/ML optimization in clearly labeled "Optional: AI / Automation" sections.

---

## Modern Best Practices (January 2026)

- Google Optimize sunset: Use VWO, Optimizely, or PostHog
- Statistical significance: https://www.evanmiller.org/ab-testing/
- CXL Institute: https://cxl.com/
- Baymard Institute UX: https://baymard.com/
- Cookie deprecation + stricter privacy defaults: prefer first-party measurement, validate assignment/tracking, and treat lifts as uncertain without clean instrumentation

---

## When to Use This Skill

- **Landing page optimization**: Hero, CTA, proof, form optimization
- **A/B testing**: Hypothesis design, sample size, statistical significance
- **Funnel analysis**: Drop-off identification, micro-conversion mapping
- **Form optimization**: Field reduction, multi-step forms, friction removal
- **Trust/credibility**: Social proof, security signals, guarantees

## When NOT to Use

- **Brand awareness campaigns** → Use [marketing-paid-advertising](../marketing-paid-advertising/SKILL.md)
- **User research methodology** → Use [software-ux-research](../software-ux-research/SKILL.md)
- **Product analytics setup** → Use [marketing-product-analytics](../marketing-product-analytics/SKILL.md)
- **SEO/organic traffic** → Use [marketing-seo-complete](../marketing-seo-complete/SKILL.md)

---

## Expert: CRO Mental Model (Quick Calibration)

Use this to avoid local wins / global losses.

- **CRO**: Increase the rate of valuable commitments (purchase, qualified lead, activation) while protecting business outcomes (revenue, margin, LTV, support load).
- **UX optimization**: Reduce friction/errors so users can do what they already intend; good UX does not guarantee better conversions.
- **Funnel optimization**: Optimize the system across steps and handoffs (traffic quality → intent match → page → form/checkout → sales/onboarding → retention).
- **Experimentation**: A causal learning method; not every decision belongs in a test.

Do not delegate these to A/B tests (even with infinite traffic): legal/compliance/ethics, dark patterns, misleading claims, and irreversible brand trust decisions.

---

## Core: CRO Framework

### The CRO Process

```text
1. ANALYZE → Identify conversion problems (data + qualitative)
2. HYPOTHESIZE → Form testable hypotheses
3. PRIORITIZE → Score by impact/effort (ICE/PIE)
4. TEST → Run A/B tests with statistical rigor
5. LEARN → Document results, iterate
6. IMPLEMENT → Roll out winners, test next
```

### Conversion Rate Benchmarks

| Page Type | Poor | Average | Good | Great |
|-----------|------|---------|------|-------|
| **Landing page** | <1% | 2-3% | 4-5% | >6% |
| **Checkout** | <40% | 50-60% | 65-75% | >80% |
| **Form completion** | <20% | 30-40% | 45-55% | >60% |
| **Add to cart** | <3% | 5-8% | 9-12% | >15% |

*Note: Benchmarks vary significantly by industry. Use as directional only.*

---

## Core: Landing Page Optimization

### Above-the-Fold Checklist

Every landing page needs these elements visible without scrolling:

| Element | Requirement | Common Issues |
|---------|-------------|---------------|
| **Headline** | Clear value proposition | Vague, company-focused |
| **Subheadline** | Specific benefit or outcome | Missing or weak |
| **Hero image/video** | Relevant, shows outcome | Stock photos, irrelevant |
| **CTA** | Prominent, action-oriented | Hidden, generic text |
| **Trust signal** | Logo strip, rating, or stat | Missing entirely |

### Headline Formula

```text
[Outcome] + [Timeframe/Ease] + [Without Pain Point]

Examples:
"Get 10 qualified leads per week without cold calling"
"File your tax return in 15 minutes with expert review"
"Double your email conversions without hiring a copywriter"
```

### CTA Button Best Practices

| Do | Don't |
|----|----|
| "Start Free Trial" | "Submit" |
| "Get My Quote" | "Click Here" |
| "Book My Demo" | "Learn More" (bottom of funnel) |
| "Download the Guide" | "Send" |

**CTA Button Optimization:**

- Size: Large enough to tap on mobile (min 44px height)
- Color: Contrasts with page background
- Position: Above fold AND after key sections
- Text: First person ("Get My...") often outperforms second person
- Whitespace: Use spacing to isolate the primary CTA from competing elements; treat big lift claims as case-dependent and verify in your context

### Trust Elements Hierarchy

```text
STRONGEST TRUST SIGNALS (use at least 3):
├─ Customer logos (recognizable brands)
├─ Review score (4.5+ stars with count)
├─ Security badges (SSL, payment, compliance)
├─ Money-back guarantee
└─ Phone number visible

SUPPORTING TRUST SIGNALS:
├─ Customer testimonials (with photo, name, company)
├─ Case study snippets (specific metrics)
├─ "As seen in" media logos
├─ Team photos (for services)
├─ Live chat widget
└─ Physical address (for services)
```

### User-Generated Content (UGC)

UGC often increases conversions in SaaS and e-commerce, but lift magnitude varies widely by category, placement, and traffic intent.

| UGC Type | Placement | Impact |
|----------|-----------|--------|
| **Customer videos** | Hero or below fold | High trust, high engagement |
| **Review excerpts** | Near CTA | Reduces uncertainty |
| **Case study quotes** | Consideration section | Builds credibility |
| **Community mentions** | Footer or social proof bar | Volume signal |

**Implementation**: Pull from G2, Capterra, or in-app feedback. Verify permissions before use.

---

## Core: Form Optimization

### Form Field Rules

| Rule | Why | Impact |
|------|-----|--------|
| **Minimum fields** | Every field adds friction | Often lowers completion (magnitude varies) |
| **Email first** | Captures partial submissions | +15-30% lead capture |
| **Persistent labels** | Placeholders disappear, cause errors | +10% completion |
| **Single column** | Easier flow | +5-10% completion |
| **Inline validation** | Catch errors early | +22% completion |
| **Browser autofill** | Reduces typing, fewer errors | +15-20% completion |

**2026 Benchmark**: Average checkout = 5.1 steps, 11.3 fields (Baymard). Target ≤5 fields for lead gen.

### Field Priority (Ask Only What You Need)

| Priority | Field | When Required |
|----------|-------|---------------|
| 1 | Email | Always |
| 2 | Name | If personalization needed |
| 3 | Company | B2B only |
| 4 | Phone | Sales-ready leads only |
| 5 | Job title | Enterprise targeting |
| 6+ | Everything else | Gate behind progressive profiling |

### Multi-Step Form Pattern

```text
Step 1: Low commitment (email)
├─ "What's your email?"
├─ Progress indicator: 1 of 3
└─ CTA: "Continue"

Step 2: Qualifying info
├─ Company size / Industry
├─ Progress indicator: 2 of 3
└─ CTA: "Almost there"

Step 3: Contact info
├─ Name / Phone (optional)
├─ Progress indicator: 3 of 3
└─ CTA: "Get My [Deliverable]"
```

**Multi-step benefits:**
- Commitment and consistency principle
- Captures partial data (even if abandoned)
- Feels less overwhelming
- Can qualify leads progressively

---

## Core: A/B Testing Methodology

### Hypothesis Template

```text
IF we [change/add/remove X]
THEN [metric] will [increase/decrease] by [estimate]
BECAUSE [reasoning based on data/research]

Example:
IF we add customer logos to the hero section
THEN form conversion will increase by 15%
BECAUSE trust signals reduce perceived risk for new visitors
```

### Sample Size Calculator

**Minimum sample size formula (simplified):**

```text
n = (16 × p × (1-p)) / MDE²

Where:
- n = sample per variant
- p = baseline conversion rate
- MDE = minimum detectable effect (e.g., 0.10 for 10% lift)

Example:
Baseline CVR: 3% (0.03)
MDE: 20% relative lift (looking for 3.6% or higher)

n = (16 × 0.03 × 0.97) / (0.006)²
n ≈ 12,933 per variant

Total traffic needed: ~26,000 visitors
```

**Quick reference:**

| Baseline CVR | 10% MDE | 20% MDE | 30% MDE |
|--------------|---------|---------|---------|
| 1% | 63,000 | 15,800 | 7,000 |
| 3% | 20,700 | 5,200 | 2,300 |
| 5% | 12,200 | 3,050 | 1,350 |
| 10% | 5,800 | 1,450 | 650 |

*Per variant. Multiply by 2 for total traffic needed.*

### Statistical Significance

**Requirements for valid test:**
- 95% confidence level (minimum)
- 80% power (default) unless you have a reason to change it
- Run for at least 1-2 full business cycles (7-14 days)
- Don't peek and stop early (increases false positives)
- Document before test: hypothesis, primary metric, guardrails, sample size, duration
- Avoid post-hoc slicing; pre-register segments or adjust for multiple comparisons

**Reality check (expert defaults):**
- Statistical significance does not mean the change is worth shipping (check practical impact + guardrails)
- Ignore "significant" results when experiment integrity is in doubt (tracking issues, traffic mix shifts, SRM, broken randomization)
- Stop early only for clear harm (guardrail breaches) or invalidity (instrumentation/assignment problems), not for "early wins"

### Experiment Integrity (2026 Default Checks)

- **Assignment sanity**: A/A test periodically; check SRM on day 1 and day 3
- **Tracking sanity**: confirm event definitions, dedupe, cross-domain, and consent-mode behavior before interpreting results
- **Contamination**: avoid showing multiple variants to the same user across devices/sessions; prefer stable IDs when possible
- **Change control**: freeze other major changes to the same flow during the test window

### CUPED: Faster Tests via Variance Reduction

CUPED (Controlled-experiment Using Pre-Existing Data) can reduce variance by **~40-60%**, allowing tests to reach significance faster.

| Aspect | Details |
|--------|---------|
| **How it works** | Uses pre-experiment user behavior to control for inherent variance |
| **Lookback window** | 1-2 weeks (optimal balance) |
| **Limitation** | Doesn't work for new users (no history) |
| **Platforms** | VWO, Optimizely, Statsig, Eppo, PostHog |

**When to use**: High-traffic sites where test velocity matters. See [advanced-testing.md](references/advanced-testing.md) for implementation details.

### Test Prioritization: ICE Framework

| Factor | Score (1-10) | Description |
|--------|--------------|-------------|
| **Impact** | | How much will this move the metric? |
| **Confidence** | | How sure are we this will work? |
| **Ease** | | How easy is this to implement? |
| **ICE Score** | | (Impact + Confidence + Ease) / 3 |

**ICE Score interpretation:**
- 8-10: High priority, test immediately
- 5-7: Medium priority, add to queue
- 1-4: Low priority, revisit later or skip

---

## Core: Funnel Analysis

### Funnel Diagnostic Framework

```text
STEP 1: Map your funnel
Page Visit → Key Action → Form Start → Form Complete → Confirmation

STEP 2: Measure drop-off at each step
├─ Page Visit to Key Action: ___% (bounce rate inverse)
├─ Key Action to Form Start: ___%
├─ Form Start to Complete: ___%
└─ Complete to Confirmation: ___%

STEP 3: Identify biggest drop-off
Biggest percentage drop = highest priority to fix

STEP 4: Diagnose root cause
├─ High bounce? → Relevance, load speed, messaging
├─ Low engagement? → Content, CTA visibility
├─ Form abandonment? → Form friction, trust
└─ Checkout drop? → Pricing, shipping, trust
```

**Expert note**: The "biggest drop-off" is not always the best target. Confirm it's a defect (not intentional filtering), not a measurement artifact, and not caused upstream (traffic quality / offer mismatch).

### Micro-Conversion Mapping

| Funnel Stage | Micro-Conversions to Track |
|--------------|---------------------------|
| **Awareness** | Scroll depth, time on page, video views |
| **Interest** | CTA hover, tab/section views, resource clicks |
| **Consideration** | Pricing page visit, comparison page, demo video |
| **Decision** | Form start, add to cart, checkout start |
| **Conversion** | Form complete, purchase, signup |

### Heatmap & Recording Analysis

**What to look for:**
- **Click heatmaps**: Are users clicking CTAs? Clicking non-clickable elements?
- **Scroll maps**: Where do users stop scrolling? Key content below fold?
- **Session recordings**: Where do users hesitate? Rage clicks? Form confusion?
- **Form analytics**: Which fields cause abandonment? Error patterns?

---

## Reference: Triage, Speed, SOPs

For page speed targets, CRO triage decision tree, operating cadence, and anti-patterns, see `references/triage-and-ops.md`.

---

## Templates

| Template | Purpose |
|----------|---------|
| [landing-audit.md](assets/landing-audit.md) | Full landing page audit |
| [ab-test-plan.md](assets/ab-test-plan.md) | A/B test planning |
| [form-audit.md](assets/form-audit.md) | Form optimization checklist |
| [funnel-analysis.md](assets/funnel-analysis.md) | Funnel diagnostic |
| [ice-scoring.md](assets/ice-scoring.md) | Test prioritization |

---

## Expert: Hypothesis Quality (Silent Failure Checklist)

A good CRO hypothesis is not "change X to raise CVR." It must specify mechanism and risk.

**Strong hypothesis includes:**
- Which constraint it targets: clarity, trust, motivation, friction
- Who it's for: segment/intent/channel/device (at least one)
- What moves: primary metric + guardrails (value, quality, downstream)
- Why it should work: evidence + mechanism (not vibes)

**How CRO fails silently (common):**
- Conversions go up but value goes down (lower-quality leads, higher refunds/chargebacks, worse retention)
- Overall looks flat but a high-value segment is harmed (mix effects hide damage)
- "Win" is novelty or seasonality; it doesn't repeat

Use `assets/ab-test-plan.md` to pre-register guardrails and invalidation criteria.

---

## References

| Reference | Description |
|-----------|-------------|
| [advanced-testing.md](references/advanced-testing.md) | CUPED, sequential testing, MAB |
| [ai-automation.md](references/ai-automation.md) | AI personalization, tool stack |
| [triage-and-ops.md](references/triage-and-ops.md) | Page speed, triage, SOPs, anti-patterns |

---

## International Markets

This skill uses US/UK defaults. For international CRO:

| Need | See Skill |
|------|-----------|
| Regional payment methods | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| Cultural trust signals | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| Regional CTA adaptation | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| RTL/localized design | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |

**Auto-triggers**: When your query mentions regional markets or cultural adaptation, both skills load automatically.

---

## Related Skills

- [marketing-geo-localization](../marketing-geo-localization/SKILL.md) — International markets, cultural CRO
- [marketing-leads-generation](../marketing-leads-generation/SKILL.md) — Lead capture strategies
- [marketing-paid-advertising](../marketing-paid-advertising/SKILL.md) — Traffic sources
- [marketing-seo-complete](../marketing-seo-complete/SKILL.md) — Page speed, Core Web Vitals
- [software-ui-ux-design](../software-ui-ux-design/SKILL.md) — Design patterns
- [software-ux-research](../software-ux-research/SKILL.md) — User research methods

---

## Usage Notes (Claude)

- Stay operational: return checklists, audit results, test plans
- Always include statistical significance requirements for testing
- Recommend qualitative research for low-traffic sites
- Use benchmark ranges, not absolute numbers
- Do not invent conversion data; state "varies by industry" when uncertain
