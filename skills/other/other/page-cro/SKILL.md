---
name: page-cro
model: standard
---

# Page CRO

> **WHAT**: Analyze and optimize marketing pages for higher conversion rates  
> **WHEN**: User wants to improve conversions on homepage, landing pages, pricing pages, feature pages, or blog posts; mentions "CRO," "page isn't converting," "improve conversions"  
> **KEYWORDS**: CRO, conversion rate optimization, improve conversions, page optimization, landing page optimization, why isn't this converting

## Reference Files

- `references/experiments.md` - A/B test ideas by page type (100+ experiments)


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install page-cro
```


---

## Workflow

### 1. Initial Assessment

Check for `.claude/product-marketing-context.md` first.

Identify:
- **Page Type**: Homepage, landing page, pricing, feature, blog, about
- **Primary Conversion Goal**: Sign up, request demo, purchase, subscribe, download
- **Traffic Context**: Where are visitors coming from? (organic, paid, email, social)

Ask if not clear:
- What's your current conversion rate and goal?
- Do you have user research, heatmaps, or session recordings?
- What have you already tried?

### 2. Analyze by Priority

Evaluate in order of impact:

#### Value Proposition Clarity (Highest Impact)
- Can a visitor understand what this is within 5 seconds?
- Is the primary benefit clear, specific, and differentiated?
- Is it written in customer language (not company jargon)?

#### Headline Effectiveness
- Does it communicate the core value proposition?
- Is it specific enough to be meaningful?
- Does it match the traffic source's messaging?

#### CTA Placement, Copy, and Hierarchy
- Is there one clear primary action?
- Is it visible without scrolling?
- Does button copy communicate value, not just action?

#### Visual Hierarchy and Scannability
- Can someone scanning get the main message?
- Are the most important elements visually prominent?
- Do images support or distract from the message?

#### Trust Signals and Social Proof
- Customer logos (especially recognizable ones)
- Testimonials (specific, attributed, with photos)
- Case study snippets with real numbers
- Review scores and counts

#### Objection Handling
- Price/value concerns addressed?
- "Will this work for my situation?" answered?
- Implementation difficulty explained?
- Risk reversal present?

#### Friction Points
- Too many form fields?
- Unclear next steps?
- Confusing navigation?
- Mobile experience issues?

### 3. Structure Recommendations

```
## Quick Wins (Implement Now)
[Easy changes with likely immediate impact]

## High-Impact Changes (Prioritize)
[Bigger changes requiring more effort but significant impact]

## Test Ideas
[Hypotheses worth A/B testing rather than assuming]

## Copy Alternatives
[For headlines and CTAs, provide 2-3 alternatives with rationale]
```

---

## Page-Specific Frameworks

### Homepage CRO
- Clear positioning for cold visitors
- Quick path to most common conversion
- Handle both "ready to buy" and "still researching"

### Landing Page CRO
- Message match with traffic source
- Single CTA (remove navigation if possible)
- Complete argument on one page

### Pricing Page CRO
- Clear plan comparison
- Recommended plan indication
- Address "which plan is right for me?" anxiety

### Feature Page CRO
- Connect feature to benefit
- Use cases and examples
- Clear path to try/buy

### Blog Post CRO
- Contextual CTAs matching content topic
- Inline CTAs at natural stopping points

---

## Common Issues Checklist

### Value Proposition
- [ ] Feature-focused instead of benefit-focused
- [ ] Too vague or too clever (sacrificing clarity)
- [ ] Trying to say everything instead of the most important thing

### Headlines
- [ ] Generic (could apply to any competitor)
- [ ] Abstract instead of concrete
- [ ] Mismatch with traffic source

### CTAs
- [ ] Weak button copy (Submit, Sign Up, Learn More)
- [ ] Too many competing CTAs
- [ ] Not visible above fold
- [ ] Missing from key decision points

### Trust
- [ ] No social proof
- [ ] Vague testimonials ("Great product!")
- [ ] Missing trust indicators near conversion points

### Friction
- [ ] Too many form fields
- [ ] Required fields that shouldn't be required
- [ ] Unclear what happens next
- [ ] Poor mobile experience

---

## CTA Strength Guide

**Weak (avoid):**
- Submit
- Sign Up  
- Learn More
- Click Here
- Get Started

**Strong (use):**
- Start Free Trial
- Get My Report
- See [Product] in Action
- Create Your First [Thing]
- Book My Demo

**Formula:** [Action Verb] + [What They Get] + [Qualifier if needed]

---

## Experiment Categories

See `references/experiments.md` for 100+ specific test ideas.

**Hero Section Tests:**
- Headline variations
- Visual format (screenshot vs. video vs. illustration)
- CTA button text and color
- Interactive demos

**Trust Signal Tests:**
- Logo placement and selection
- Testimonial format (text vs. video)
- Case study snippets

**Pricing Tests:**
- Number of tiers
- Annual vs. monthly default
- Plan recommendation badges
- Feature comparison format

**Form Tests:**
- Field count
- Multi-step vs. single
- Field enrichment
- Labels and placeholders

---

## NEVER

- Recommend changes without understanding traffic source
- Assume what works for one page works for all
- Skip asking about current conversion rate
- Ignore mobile experience
- Recommend removing navigation from homepage (only landing pages)
- Suggest fake urgency or scarcity
- Make recommendations without offering test alternatives

---

## Related Skills

- `copywriting` - Complete copy rewrites
- `marketing-psychology` - Psychological principles for conversion
- `marketing-ideas` - Tactical marketing approaches
