---
name: conversion-audit
description: Audit pages for conversion optimization opportunities. Analyzes value props, CTAs, social proof, friction points, and mobile conversion to identify drop-off causes.
---

# Conversion Audit Skill

Comprehensive audit of landing pages, pricing pages, or any conversion-critical interface to identify optimization opportunities ranked by estimated impact.

## When to Use

Use `/conversion-audit` when you need to:
- Audit landing pages before launch
- Diagnose low conversion rates
- Identify friction in signup or checkout flows
- Evaluate pricing page effectiveness
- Assess mobile conversion experience
- Prioritize conversion improvements

## Instructions

### Phase 1: Page Structure Analysis

**Goal**: Evaluate overall page architecture and information hierarchy

**I will analyze:**

1. **Above-the-Fold Content**
   - Clear value proposition visible immediately?
   - Primary CTA above fold?
   - Social proof or trust signals present?
   - Visual hierarchy guides eye to CTA?

2. **Content Flow**
   - Logical progression: Problem → Solution → Proof → Action?
   - Objections addressed before asking for action?
   - Appropriate content density (not overwhelming)?

3. **CTA Placement**
   - Primary CTA repeated at logical intervals?
   - CTAs appear after value demonstrations?
   - Final CTA before footer?

**Scoring Rubric (1-5):**

| Score | Page Structure |
|-------|----------------|
| 5 | Clear value prop, CTA above fold, logical flow, objections addressed |
| 4 | Value prop clear, CTA visible, mostly logical flow |
| 3 | Value prop present but unclear, CTA below fold, some flow issues |
| 2 | Weak value prop, CTA hard to find, confusing structure |
| 1 | No clear value prop, no obvious CTA, chaotic layout |

---

### Phase 2: Copy Effectiveness

**Goal**: Evaluate headline, body copy, and microcopy quality

**Headline Assessment:**

```markdown
### Great Headlines
✅ **Clear benefit**: "Close deals 3x faster with AI-powered sales tools"
✅ **Specific outcome**: "Generate 10,000 leads per month on autopilot"
✅ **Problem/solution**: "Tired of losing customers at checkout? Fix it in 5 minutes"

### Weak Headlines
❌ **Vague**: "The best solution for your business"
❌ **Feature-first**: "Advanced AI-powered platform"
❌ **Jargon**: "Synergize your enterprise workflow ecosystem"
```

**I will check:**

1. **Headline**
   - States clear benefit or outcome?
   - Specific vs vague?
   - Customer language vs company jargon?
   - Creates curiosity or urgency?

2. **Subheadline**
   - Expands on headline promise?
   - Addresses "how" or "for whom"?
   - Builds credibility?

3. **Body Copy**
   - Benefit-driven vs feature-first?
   - Scannable (bullets, short paragraphs)?
   - Uses "you" vs "we"?
   - Addresses objections?

4. **CTA Copy**
   - Action-oriented verbs?
   - Value-focused (what user gets)?
   - Creates urgency without manipulation?

**Scoring Rubric (1-5):**

| Score | Copy Quality |
|-------|--------------|
| 5 | Compelling headline, benefit-focused, scannable, strong CTAs |
| 4 | Good headline, mostly benefits, readable, decent CTAs |
| 3 | Okay headline, mix of features/benefits, some jargon |
| 2 | Weak headline, feature-heavy, company-focused, vague CTAs |
| 1 | No clear message, jargon-heavy, confusing, weak/missing CTAs |

---

### Phase 3: Trust & Credibility Signals

**Goal**: Assess social proof and trust-building elements

**I will look for:**

1. **Social Proof Types**
   - Customer testimonials (with photos, names, roles)?
   - Logo bars (recognizable brands)?
   - Usage statistics ("10,000+ customers")?
   - Case studies or results?
   - Star ratings / reviews?
   - Press mentions / awards?

2. **Trust Signals**
   - Security badges (SSL, payment processors)?
   - Money-back guarantee?
   - Free trial / no credit card required?
   - Privacy policy link visible?
   - Contact information accessible?

3. **Authority Markers**
   - Expert credentials?
   - Industry certifications?
   - Media appearances?
   - Founding story / team bios?

**Optimal Placement:**
- Logo bar immediately after hero
- Testimonials mid-page after feature blocks
- Trust badges near forms/payment
- Reviews on pricing page
- Final social proof before closing CTA

**Scoring Rubric (1-5):**

| Score | Trust Signals |
|-------|---------------|
| 5 | Multiple types of social proof, well-placed, authentic, trust badges |
| 4 | Good social proof mix, mostly well-placed, some trust signals |
| 3 | Basic social proof (1-2 types), placement okay, few trust signals |
| 2 | Minimal social proof, poor placement, missing trust signals |
| 1 | No social proof, no trust signals, feels risky |

---

### Phase 4: Friction Point Analysis

**Goal**: Identify obstacles preventing conversion

**Common Friction Sources:**

1. **Form Friction**
   - Too many fields (>5 is risky)
   - Unnecessary required fields
   - No clear progress indicator (multi-step)
   - Unclear error messages
   - No autofill support
   - Asks for credit card when "free trial" promised

2. **Navigation Friction**
   - Too many exit points near conversion
   - Confusing navigation labels
   - Multiple CTAs competing
   - Dead ends (nowhere to go from page)

3. **Information Friction**
   - Pricing not transparent (must contact sales)
   - Key questions unanswered
   - Feature details too vague
   - No FAQ for common objections

4. **Technical Friction**
   - Slow page load (>3 seconds)
   - Broken links
   - Non-responsive on mobile
   - Layout shift/jank

**I will identify:**
- High-friction elements
- Estimated impact of removing each
- Prioritized fix list

**Scoring Rubric (1-5):**

| Score | Friction Level |
|-------|----------------|
| 5 | Minimal friction, smooth flow, clear path to conversion |
| 4 | Minor friction points, mostly smooth experience |
| 3 | Moderate friction, some confusing or frustrating elements |
| 2 | Significant friction, multiple blockers, frustrated users likely |
| 1 | Extremely high friction, barely usable, conversion unlikely |

---

### Phase 5: Mobile Conversion Assessment

**Goal**: Evaluate mobile-specific conversion factors

**I will check:**

1. **Mobile Layout**
   - Hero content fits mobile viewport?
   - CTA thumb-reachable (bottom-anchored)?
   - Text readable (min 16px)?
   - Images optimized for mobile?

2. **Mobile Forms**
   - Appropriate input types (tel, email)?
   - Keyboard-friendly?
   - Easy to tap (48px+ targets)?
   - Validation clear on small screen?

3. **Mobile Performance**
   - Fast load time (<3s)?
   - No layout shift?
   - Smooth scrolling?
   - Offline state handled?

4. **Mobile Trust**
   - Social proof visible on mobile?
   - Trust badges near mobile CTA?
   - Secure connection indicator?

**Scoring Rubric (1-5):**

| Score | Mobile Conversion |
|-------|-------------------|
| 5 | Excellent mobile experience, optimized for touch, fast, clear CTAs |
| 4 | Good mobile experience, minor issues, mostly optimized |
| 3 | Basic mobile responsive, some usability issues |
| 2 | Poor mobile experience, major usability problems, slow |
| 1 | Not mobile-friendly, unusable on small screens |

---

## Conversion Audit Checklist

### Hero Section
- [ ] Value proposition clear in 5 seconds?
- [ ] Headline states specific benefit?
- [ ] Subheadline expands on promise?
- [ ] Primary CTA above fold?
- [ ] Visual supports message?
- [ ] Social proof visible (logo bar)?

### Copy & Messaging
- [ ] Benefit-driven vs feature-first?
- [ ] Uses customer language, not jargon?
- [ ] Addresses "what's in it for me"?
- [ ] Scannable (bullets, short paragraphs)?
- [ ] Tells a story or paints picture?

### CTAs
- [ ] Visually prominent (color, size)?
- [ ] Action-oriented copy (not "Submit")?
- [ ] States value ("Start Free Trial")?
- [ ] Repeated at logical points?
- [ ] High contrast ratio (4.5:1+)?
- [ ] Large enough for mobile tap?

### Social Proof
- [ ] Customer testimonials with photos?
- [ ] Recognizable brand logos?
- [ ] Usage stats ("10,000+ users")?
- [ ] Reviews / star ratings?
- [ ] Case studies or results?
- [ ] Placed near CTAs?

### Trust Signals
- [ ] Security badges (SSL, payment)?
- [ ] Money-back guarantee?
- [ ] Free trial clearly stated?
- [ ] Privacy policy accessible?
- [ ] Contact info visible?
- [ ] No surprises (hidden fees)?

### Forms
- [ ] Minimal fields (≤5 for lead gen)?
- [ ] Only required fields required?
- [ ] Clear labels and placeholders?
- [ ] Inline validation?
- [ ] Progress indicator (multi-step)?
- [ ] Autofill/autocomplete?
- [ ] Error messages helpful?

### Page Flow
- [ ] Logical content progression?
- [ ] Objections addressed before CTA?
- [ ] No competing CTAs?
- [ ] Minimal navigation distractions?
- [ ] Scroll depth matches content?

### Mobile Optimization
- [ ] Responsive on all screen sizes?
- [ ] CTA thumb-reachable?
- [ ] Touch targets ≥ 48px?
- [ ] Text readable (≥16px)?
- [ ] Fast load time (<3s)?
- [ ] Form mobile-optimized?

### Technical
- [ ] Page loads quickly (<3s)?
- [ ] No broken links/images?
- [ ] No layout shift/jank?
- [ ] Works across browsers?
- [ ] HTTPS/secure?

### Dark Pattern Check
- [ ] No fake urgency ("Only 2 left!")?
- [ ] No hidden fees?
- [ ] Easy to cancel?
- [ ] No confirm-shaming?
- [ ] No trick questions?
- [ ] Respects user autonomy?

---

## Output Format

```markdown
## Conversion Audit Report

### Overall Score: [X]/25

| Category | Score | Priority |
|----------|-------|----------|
| Page Structure | [1-5] | [High/Med/Low] |
| Copy Effectiveness | [1-5] | [High/Med/Low] |
| Trust & Credibility | [1-5] | [High/Med/Low] |
| Friction Level | [1-5] | [High/Med/Low] |
| Mobile Conversion | [1-5] | [High/Med/Low] |

---

### Critical Issues (Fix Immediately)

1. **Missing Value Proposition**
   - **Problem**: Headline doesn't communicate clear benefit
   - **Impact**: Users leave without understanding what you do
   - **Fix**: Rewrite headline: "Close deals 3x faster with AI-powered sales tools"
   - **Estimated Lift**: +20-30% conversion

2. **CTA Below Fold**
   - **Problem**: Primary CTA not visible without scrolling
   - **Impact**: Users don't know what action to take
   - **Fix**: Add CTA button to hero section
   - **Estimated Lift**: +15-25% conversion

---

### High-Priority Improvements

3. **No Social Proof Above Fold**
   - **Problem**: Missing trust signals in hero
   - **Impact**: Users question legitimacy
   - **Fix**: Add logo bar of recognizable clients below hero
   - **Estimated Lift**: +10-15% conversion

4. **Form Too Long**
   - **Problem**: 8 required fields for free trial
   - **Impact**: High abandonment rate
   - **Fix**: Reduce to email + password only, collect rest later
   - **Estimated Lift**: +25-35% completion

---

### Medium-Priority Improvements

5. **Weak CTA Copy**
   - **Problem**: Button says "Submit" instead of value-driven copy
   - **Impact**: Doesn't motivate action
   - **Fix**: Change to "Start Free Trial - No Credit Card Required"
   - **Estimated Lift**: +5-10% conversion

---

### Low-Priority Enhancements

6. **Missing FAQ Section**
   - **Problem**: Common questions not addressed
   - **Impact**: Some users need more info before converting
   - **Fix**: Add FAQ section before final CTA
   - **Estimated Lift**: +2-5% conversion

---

### Mobile-Specific Issues

- [ ] CTA too small for thumb (36px, needs 48px)
- [ ] Text size too small (14px, needs 16px min)
- [ ] Form fields crammed together

---

### Strengths (Don't Change)

✅ Clear, benefit-driven headline
✅ Testimonials include photos and full names
✅ Fast page load time (1.2s)
✅ No dark patterns detected

---

### Prioritized Action Plan

**Phase 1: Quick Wins (1-2 hours)**
1. Fix CTA visibility - move above fold
2. Shorten form to 3 fields
3. Update CTA copy to value-driven
**Estimated Combined Lift**: +40-60%

**Phase 2: Trust Building (1 day)**
4. Add logo bar social proof
5. Add security badges near form
6. Add money-back guarantee statement
**Estimated Combined Lift**: +15-25%

**Phase 3: Polish (2-3 days)**
7. Rewrite body copy to be more benefit-focused
8. Add FAQ section
9. Optimize mobile experience
**Estimated Combined Lift**: +10-20%

**Total Potential Lift**: +65-105% conversion improvement
```

---

## Integration with Other Skills

- **/copywriting-guide** - Fix copy issues identified in audit
- **/cta-optimizer** - Improve CTA design and placement
- **/social-proof** - Add appropriate trust signals
- **/mobile-patterns** - Fix mobile-specific issues

---

## Notes

- Audit against real user behavior data when available (heatmaps, session recordings)
- Test assumptions with A/B tests - estimated lifts are guidelines
- Prioritize by impact vs effort (quick wins first)
- Re-audit after significant changes
- Mobile conversion often 2-3x lower than desktop - optimize separately
- Dark patterns may boost short-term conversion but harm long-term trust
