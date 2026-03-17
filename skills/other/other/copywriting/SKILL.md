---
name: copywriting
model: reasoning
---

# Copywriting

> **WHAT**: Write clear, compelling marketing copy that drives action  
> **WHEN**: User wants to write, rewrite, or improve copy for homepage, landing pages, pricing pages, feature pages, about pages, or product pages  
> **KEYWORDS**: write copy, improve copy, rewrite page, marketing copy, headline help, CTA copy, landing page copy, value proposition

## Reference Files

- `references/copy-frameworks.md` - Headline formulas, page templates, section types
- `references/natural-transitions.md` - Transitional phrases and signposting


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install copywriting
```


---

## Workflow

### 1. Gather Context

Check for `.claude/product-marketing-context.md` first. If not available, ask:

**Page Purpose**
- What type of page? (homepage, landing page, pricing, feature, about)
- What is the ONE primary action you want visitors to take?

**Audience**
- Who is the ideal customer?
- What problem are they solving?
- What objections do they have?
- What language do they use to describe their problem?

**Product/Offer**
- What are you selling?
- What makes it different?
- What's the key transformation?
- Any proof points (numbers, testimonials, case studies)?

**Traffic Context**
- Where is traffic coming from? (ads, organic, email)
- What do visitors already know before arriving?

### 2. Write Copy

Structure output by section:

```
## Above the Fold

### Headline
[Primary headline - your single most important message]

### Subheadline
[Expands on headline, adds specificity, 1-2 sentences]

### Primary CTA
[Action-oriented button text]

---

## [Section Name]

[Section copy]

---

## Final CTA

[Recap value, repeat CTA, risk reversal]
```

### 3. Provide Alternatives

For headlines and CTAs, offer 2-3 options:

```
**Headline Options:**
1. "[Copy A]" — [rationale: outcome-focused]
2. "[Copy B]" — [rationale: problem-focused]
3. "[Copy C]" — [rationale: proof-focused]
```

### 4. Include Meta Content

When relevant:
- Page title (for SEO)
- Meta description

---

## Core Principles

### Clarity Over Cleverness
If you have to choose between clear and creative, choose clear.

### Benefits Over Features
Features: What it does. Benefits: What that means for the customer.

### Specificity Over Vagueness
- Vague: "Save time on your workflow"
- Specific: "Cut your weekly reporting from 4 hours to 15 minutes"

### Customer Language Over Company Language
Use words your customers use. Mirror voice-of-customer from reviews, interviews, support tickets.

### One Idea Per Section
Each section should advance one argument. Build a logical flow down the page.

---

## Writing Style Rules

1. **Simple over complex** — "Use" not "utilize," "help" not "facilitate"
2. **Specific over vague** — Avoid "streamline," "optimize," "innovative"
3. **Active over passive** — "We generate reports" not "Reports are generated"
4. **Confident over qualified** — Remove "almost," "very," "really"
5. **Show over tell** — Describe the outcome instead of using adverbs
6. **Honest over sensational** — Never fabricate statistics or testimonials

---

## Headline Formulas (Quick Reference)

**Outcome-Focused:**
- "{Achieve outcome} without {pain point}"
- "Turn {input} into {outcome}"
- "[Outcome] in [timeframe]"

**Problem-Focused:**
- "Never {unpleasant event} again"
- "{Question highlighting pain point}?"
- "Stop [pain]. Start [pleasure]."

**Audience-Focused:**
- "{Product type} for {audience}"
- "You don't have to {skill} to {outcome}"

**Proof-Focused:**
- "[Number] [people] use [product] to [outcome]"

See `references/copy-frameworks.md` for complete formulas and page templates.

---

## CTA Guidelines

**Weak CTAs (avoid):**
- Submit, Sign Up, Learn More, Click Here, Get Started

**Strong CTAs (use):**
- Start Free Trial
- Get [Specific Thing]
- See [Product] in Action
- Create Your First [Thing]
- Download the Guide

**Formula:** [Action Verb] + [What They Get] + [Qualifier if needed]

---

## Page-Specific Guidance

| Page Type | Key Focus |
|-----------|-----------|
| Homepage | Serve multiple audiences without being generic; clear paths for different intents |
| Landing Page | Single message, single CTA; match headline to traffic source |
| Pricing Page | Help visitors choose the right plan; address "which is right for me?" |
| Feature Page | Connect feature → benefit → outcome; show use cases |
| About Page | Tell why you exist; connect mission to customer benefit |

---

## Quality Checklist

Before finalizing, check for:
- [ ] Jargon that could confuse outsiders?
- [ ] Sentences trying to do too much?
- [ ] Passive voice constructions?
- [ ] Exclamation points? (remove them)
- [ ] Marketing buzzwords without substance?
- [ ] Generic claims with no proof?

---

## NEVER

- Use exclamation points in headlines or body copy
- Write vague claims like "best-in-class" or "industry-leading"
- Fabricate statistics or testimonials
- Bury the value proposition below the fold
- Use jargon the customer wouldn't use
- Write passive voice when active is clearer
- Submit copy without providing alternatives for key elements

---

## Related Skills

- `page-cro` - Page structure and conversion optimization
- `marketing-psychology` - Apply psychological principles to copy
- `marketing-ideas` - Tactical marketing approaches
