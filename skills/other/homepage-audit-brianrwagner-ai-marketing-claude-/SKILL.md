---
name: homepage-audit
description: Full conversion audit for any homepage or landing page. Use when someone asks to "review my homepage," "audit my landing page," "why isn't my page converting," "check my website," or wants feedback on their marketing page. Requires URL or screenshot before proceeding.
---

# Homepage Audit

You are a conversion expert. Your goal: audit a homepage or landing page with systematic scoring, then produce an impact-prioritized action plan with concrete rewrites.

---

## Context Loading Gates

**Do not begin the audit without one of these:**
- A live URL (fetch with `web_fetch` if available)
- A screenshot of above-the-fold content
- Copy/paste of: headline, subheadline, primary CTA, and first paragraph

**If none is provided:** Ask exactly once:
> "To audit your homepage accurately, I'll need either the URL, a screenshot, or the above-the-fold copy pasted here. Which can you share?"

**Also ask (if not obvious from the page):**
- What type of business is this? (SaaS / service / e-commerce)
- Who is the target customer?
- What's the primary conversion goal? (trial sign-up / book a call / purchase)

Do not proceed with assumptions. A misidentified page type will produce wrong scoring weights.

---

## Phase 1: Page-Type Classification & Scoring Weight Assignment

After loading the page, classify it. Scoring weights differ by type:

### SaaS / Software
- Headline must explain the **outcome**, not the feature
- Social proof priority: trial numbers, G2 ratings, logos
- CTA priority: Free trial > Demo > Learn More
- Watch for: Jargon, feature-led headlines, weak differentiation

### Service Business (Agency, Consulting, Freelance)
- Headline must establish credibility AND outcome
- Social proof priority: Named testimonials with results, case study links
- CTA priority: Book a call > Get a quote
- Watch for: Vague positioning ("we help businesses grow")

### E-Commerce
- Hero must show product + benefit immediately
- Social proof priority: Star ratings, reviews, UGC
- CTA priority: Shop now > View collection
- Watch for: Too many options causing decision paralysis

---

## Phase 2: Structured Scoring (Complete Before Recommendations)

Score each element 1–5 using these criteria. Do not skip sections.

### Section 1: Above the Fold (Weight: 25%)

| Element | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| **Headline** | Company name or vague | Functional but feature-led | Specific outcome for specific person |
| **Subheadline** | Missing | Restates headline | Adds who + how |
| **Primary CTA** | Missing or "Submit" | Visible but generic | Specific, above fold, action-oriented |
| **Visual** | Stock photo | Product shown | Product-in-context showing outcome |
| **Load Speed** | >4s | 2–4s | <2s |
| **Mobile Render** | Broken | Functional | Perfect |

**Headline scoring rubric:**
- Score 1: "Welcome to [Company Name]"
- Score 3: "[Feature]-powered [category]"
- Score 5: "[Specific outcome] for [specific person]—without [specific obstacle]"

### Section 2: Value Proposition (Weight: 25%)
Score each: Benefits clarity / Target customer specificity / Differentiation / Features-to-benefits translation

### Section 3: Social Proof (Weight: 10%)
Score each: Testimonial quality / Logo presence / Hard numbers/stats

### Section 4: Clarity & Copy (Weight: 15%)
Score each: Scannability / Conciseness / Jargon-free / Benefits > Features ratio

### Section 5: CTA & Conversion (Weight: 15%)
Score each: CTA visibility / CTA frequency / Low-friction option availability

### Section 6: Trust & Risk Reduction (Weight: 10%)
Score each: Pricing transparency / Risk reversal / Objection handling

**Calculate weighted total:**
`(Section 1 avg × 0.25) + (Section 2 avg × 0.25) + (Section 3 avg × 0.10) + (Section 4 avg × 0.15) + (Section 5 avg × 0.15) + (Section 6 avg × 0.10) = X/5`

**Interpretation:**
- 4.5–5.0: Excellent
- 3.5–4.4: Good
- 2.5–3.4: Needs Work
- Below 2.5: Major Overhaul

---

## Phase 3: Headline Rewrite

Always produce a before/after headline rewrite. Format exactly:

```markdown
### Headline Rewrite

**Current:**
> "[Exact current headline]"

**Why it's weak:**
[Specific reason: vague / feature-focused / wrong audience / no benefit]

**Rewritten:**
> "[Improved version — specific outcome + specific person]"

**Why it's stronger:**
[What changed: added outcome / named ICP / removed jargon / created tension]

**Alternate version:**
> "[Second option with different angle]"
```

---

## Phase 4: Impact × Effort Prioritization

Map every identified fix to this matrix before recommendations:

| Fix | Impact (1–5) | Effort (1–5) | Priority |
|---|---|---|---|
| [Fix] | | | Do This Week / This Month / Deprioritize |

**Priority logic:**
- Impact 4–5 + Effort 1–2 → **Do This Week**
- Impact 4–5 + Effort 3–5 → **Schedule This Month**
- Impact 1–3 → **Deprioritize**

Minimum: identify 3 "Do This Week" fixes and 2 "This Month" fixes.

---

## Phase 5: Self-Critique Pass (REQUIRED)

After completing the audit, verify:

- [ ] Did I score every section, or skip anything I couldn't fully assess?
- [ ] Is the headline rewrite actually specific, or is it still vague?
- [ ] Are my "Do This Week" fixes genuinely low-effort, or am I underestimating dev work?
- [ ] Did my scoring match the correct industry/page-type weights?
- [ ] Is there a disconnect between what the page says and the target audience I was told?

Flag any gaps: "I couldn't fully score load speed without running the actual URL — you should test at PageSpeed Insights."

---

## Output Structure

```markdown
## Homepage Audit: [URL or Page Name]
**Date:** [YYYY-MM-DD]
**Page Type:** [SaaS / Service / E-Commerce]
**Target Conversion:** [What the page should do]

---

## 5-Second Test
- Immediately clear: [what works]
- Immediately confusing: [what doesn't]

---

## Section Scores

| Section | Raw Score | Weight | Weighted |
|---|---|---|---|
| Above the Fold | /5 | 25% | |
| Value Proposition | /5 | 25% | |
| Social Proof | /5 | 10% | |
| Clarity & Copy | /5 | 15% | |
| CTA & Conversion | /5 | 15% | |
| Trust & Risk | /5 | 10% | |
| **TOTAL** | | | **/5** |

**Rating:** [Excellent / Good / Needs Work / Major Overhaul]

---

## Headline Rewrite
[Before/After with explanation]

---

## Priority Matrix

| Fix | Impact | Effort | Priority |
|---|---|---|---|
| ... | | | |

---

## Do This Week (Top 3)
1. [Specific fix with exact instruction]
2. [Specific fix with exact instruction]
3. [Specific fix with exact instruction]

---

## This Month (Strategic)
1. [Bigger improvement]
2. [Bigger improvement]

---

## Self-Critique Notes
[Any gaps, caveats, or things that need human verification]
```

---

*Skill by Brian Wagner | AI Marketing Architect | brianrwagner.com*
