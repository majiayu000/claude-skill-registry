---
name: marketing-cro
description: Conversion Rate Optimization - A/B testing methodology, landing page optimization, form design, statistical significance, and funnel analysis.
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

---

## When to Use This Skill

- **Landing page optimization**: Hero, CTA, proof, form optimization
- **A/B testing**: Hypothesis design, sample size, statistical significance
- **Funnel analysis**: Drop-off identification, micro-conversion mapping
- **Form optimization**: Field reduction, multi-step forms, friction removal
- **Trust/credibility**: Social proof, security signals, guarantees

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

---

## Core: Form Optimization

### Form Field Rules

| Rule | Why | Impact |
|------|-----|--------|
| **Minimum fields** | Every field = friction | -10% CVR per field (approx) |
| **Email first** | Captures partial submissions | +15-30% lead capture |
| **Labels above fields** | Faster scanning | +10% completion |
| **Single column** | Easier flow | +5-10% completion |
| **Inline validation** | Catch errors early | +22% completion |

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
- Run for at least 1-2 full business cycles (7-14 days)
- Don't peek and stop early (increases false positives)
- Document before test: hypothesis, primary metric, sample size, duration

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

## Core: Page Speed Optimization

### Speed Impact on Conversion

| Load Time | Impact |
|-----------|--------|
| 0-2 seconds | Baseline (optimal) |
| 3 seconds | -7% conversion |
| 5 seconds | -22% conversion |
| 10 seconds | -50%+ conversion |

*Source: Google/Akamai research, directional only*

### Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | <2.5s | 2.5-4s | >4s |
| **INP** (Interaction to Next Paint) | <200ms | 200-500ms | >500ms |
| **CLS** (Cumulative Layout Shift) | <0.1 | 0.1-0.25 | >0.25 |

### Quick Speed Wins

| Action | Impact | Effort |
|--------|--------|--------|
| Compress images | High | Low |
| Enable caching | High | Low |
| Remove unused scripts | Medium | Medium |
| Lazy load below-fold content | Medium | Low |
| Use CDN | High | Medium |
| Optimize fonts | Medium | Low |

---

## Quick Reference

| Task | Template | Location |
|------|----------|----------|
| Landing page audit | Page audit checklist | `templates/landing-audit.md` |
| A/B test plan | Test hypothesis doc | `templates/ab-test-plan.md` |
| Form audit | Form optimization | `templates/form-audit.md` |
| Funnel analysis | Funnel diagnostic | `templates/funnel-analysis.md` |
| Test prioritization | ICE scoring matrix | `templates/ice-scoring.md` |

---

## Decision Tree (CRO Triage)

```text
Low conversion rate?
├─ Check page speed first (if >3s, fix that)
├─ Check bounce rate
│   ├─ High bounce (>70%) → Message/audience mismatch
│   └─ Normal bounce → Continue diagnosis
├─ Check scroll depth
│   ├─ Low scroll → Above-fold problem
│   └─ Good scroll → Below-fold CTA/proof issue
├─ Check form analytics
│   ├─ Low form starts → CTA/offer problem
│   └─ High abandonment → Form friction
└─ Check mobile vs desktop
    ├─ Mobile worse → Mobile UX issues
    └─ Same → Universal issue

Form abandonment?
├─ Check which field causes drop-off
├─ Reduce fields to minimum
├─ Add progress indicator
├─ Add inline validation
└─ Test multi-step

Traffic but no clicks?
├─ CTA not visible → Move above fold
├─ CTA not compelling → Test copy
├─ Too many options → Simplify, single CTA
└─ Page too long → Add sticky CTA
```

---

## Operational SOPs

### Weekly CRO Review (30 minutes)

1. **Check conversion metrics**
   - Landing page CVR vs last week
   - Form completion rate
   - Funnel stage conversion rates

2. **Review active tests**
   - Current test status
   - Statistical significance check
   - Call winner if significant

3. **Prioritize next tests**
   - Score new ideas (ICE)
   - Plan next week's tests
   - Document learnings

### Monthly CRO Audit (2 hours)

1. **Full funnel analysis**
   - Map all conversion points
   - Identify top 3 drop-off points
   - Quantify opportunity (traffic × CVR gap)

2. **Heatmap/recording review**
   - Review 10-20 session recordings
   - Analyze click and scroll heatmaps
   - Document friction points

3. **Test performance review**
   - Win/loss ratio
   - Cumulative lift from tests
   - Update testing roadmap

4. **Competitive analysis**
   - Review competitor landing pages
   - Note new patterns/trends
   - Identify test ideas

---

## Templates

| Template | Purpose |
|----------|---------|
| [landing-audit.md](templates/landing-audit.md) | Full landing page audit |
| [ab-test-plan.md](templates/ab-test-plan.md) | A/B test planning |
| [form-audit.md](templates/form-audit.md) | Form optimization checklist |
| [funnel-analysis.md](templates/funnel-analysis.md) | Funnel diagnostic |
| [ice-scoring.md](templates/ice-scoring.md) | Test prioritization |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Testing too small changes** | Undetectable effect, wasted time | Test big, obvious changes first |
| **Stopping tests early** | False positives, bad decisions | Run to calculated sample size |
| **No hypothesis** | Random changes, no learnings | Document hypothesis before test |
| **Testing everything at once** | Can't isolate what worked | One variable at a time |
| **Ignoring mobile** | 60%+ traffic is mobile | Mobile-first optimization |
| **Copying competitors** | Different audience, context | Use for ideas, test your own |
| **Only A/B testing** | Misses qualitative insights | Combine with user research |

---

## Optional: AI / Automation

> **Note**: Core CRO fundamentals above work without AI. This section covers optional AI capabilities.

### AI-Powered CRO Tools

| Tool Type | Use Case | Examples |
|-----------|----------|----------|
| **AI copy generation** | Headline/CTA variants | Claude, GPT, Jasper |
| **Personalization** | Dynamic content by segment | Optimizely, VWO |
| **Predictive testing** | Predict winners faster | Evolv AI, Sentient |
| **Auto-optimization** | Multi-armed bandit | Google Optimize (sunset), VWO |

### When to Use AI

```text
HAVE thousands of daily conversions?
├─ YES → AI personalization can optimize in real-time
└─ NO → Stick to traditional A/B testing

NEED many variants quickly?
├─ YES → AI copy generation for variant ideation
└─ NO → Human copywriting with hypothesis

HAVE limited traffic?
├─ YES → Qualitative research over testing
└─ NO → Statistical A/B tests
```

---

## Related Skills

- [marketing-leads-generation](../marketing-leads-generation/SKILL.md) — Lead capture strategies
- [marketing-paid-advertising](../marketing-paid-advertising/SKILL.md) — Traffic sources
- [marketing-seo-technical](../marketing-seo-technical/SKILL.md) — Page speed, Core Web Vitals
- [software-ui-ux-design](../software-ui-ux-design/SKILL.md) — Design patterns
- [software-ux-research](../software-ux-research/SKILL.md) — User research methods

---

## Usage Notes (Claude)

- Stay operational: return checklists, audit results, test plans
- Always include statistical significance requirements for testing
- Recommend qualitative research for low-traffic sites
- Use benchmark ranges, not absolute numbers
- Do not invent conversion data; state "varies by industry" when uncertain
