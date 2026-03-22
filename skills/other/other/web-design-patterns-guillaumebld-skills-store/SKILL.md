---
name: web-design-patterns
description: "Design patterns for website sections — heroes, cards, CTAs, trust signals, testimonials. Principle-based patterns that avoid AI-generated aesthetics. Pair with web-design-methodology for implementation."
---

# Web Design Patterns

Principle-based patterns for designing website sections that feel human-designed, not AI-generated. Each pattern teaches WHY and WHEN, not just templates to copy.

## What You Produce

Well-designed website sections: heroes, card layouts, CTAs, trust signals, and testimonials that match the business context and avoid the "AI skeleton" look.

## When to Read Which Reference

| Building this... | Read this reference |
|------------------|-------------------|
| Homepage hero, page headers, landing pages | `references/hero-patterns.md` |
| Service cards, team grids, pricing tiers, portfolios | `references/card-patterns.md` |
| Conversion sections, buttons, banner CTAs | `references/cta-patterns.md` |
| Credibility: badges, licences, reviews, guarantees | `references/trust-signals.md` |
| Customer reviews, social proof, quote sections | `references/testimonial-patterns.md` |

**Load on demand** — don't read all five for every project. Read the one(s) relevant to the current section.

## Cross-Cutting Principles

These apply to ALL patterns. Internalise these before reading any reference file.

### Anti-AI Patterns (Avoid These)

The "AI skeleton" that signals template-generated design:

1. **The sequence**: Hero → trust bar → 3 identical cards → features → stats → CTA → footer
2. **Democratic design**: Every element gets equal visual weight, no hierarchy
3. **Perfect symmetry**: Everything centred, perfectly aligned, no intentional asymmetry
4. **Identical repetition**: All cards same size, same structure, same padding, same shadow
5. **Generic copy**: "Learn More" as every CTA, "Quality Service You Can Trust" as every headline
6. **Decoration without purpose**: Floating shapes, random gradients, abstract blobs

### What Makes Design Feel Human

1. **One element clearly dominates** — hierarchy, not democracy
2. **Asymmetry is intentional** — not everything centred or balanced
3. **Specific, opinionated copy** — "Schedule Your Free Roof Inspection" not "Learn More"
4. **Visual weight guides the eye** — you know where to look first, second, third
5. **Restraint** — not every technique used, just the ones that serve the purpose
6. **Context-appropriate** — emergency plumber looks different from luxury hotel

### Ethical Rules

Non-negotiable across all patterns:

**On lead-gen sites (no real business data), NEVER fabricate:**
- Star ratings or review counts
- Specific years in business
- Licence or ABN numbers
- Named individuals or team members
- Exact customer counts

**Safe alternatives for lead-gen:**
- "Experienced Team" (not "25 Years Experience")
- "Highly Rated" (not "4.9 Stars (127 Reviews)")
- "Licensed & Insured" (not "QBCC License #1234567")

### Business Context Shapes Everything

The same section type looks completely different for different businesses:

| Business type | Design feel |
|---------------|-------------|
| Emergency services | Direct, immediate, phone-first |
| Luxury/hospitality | Spacious, refined, atmospheric |
| Trades/local services | Trustworthy, capable, genuine |
| Professional/corporate | Confident, clean, structured |
| Creative/agency | Distinctive, bold, personality-driven |

## Quick Pattern Examples

### Hero Approaches

**Image-dominant** (strong photography available):
- Let the image do the work, minimal text
- One clear focal point
- Text placement within image composition, not slapped on top

**Typography-dominant** (no strong imagery):
- Font choice, size, weight, spacing IS the design
- Generous whitespace as active design element
- Colour blocking or subtle texture instead of stock photos

**Split/balanced** (strong copy + strong imagery):
- One side dominates slightly — true 50/50 feels indecisive
- On mobile, order matters — which element first in vertical stack?

### Card Layout Decision

1. **Count items first** — wrong grid math creates orphan cards
2. **Check hierarchy** — is one item more important? Feature it at 2x size
3. **Content density** — image-heavy = fewer columns, text-heavy = more columns
4. **Orphan fix** — never leave 1 card alone on a row

### CTA Hierarchy

Match CTA urgency to business context:
- **Emergency services**: Phone number IS the CTA. Huge, high-contrast, tappable.
- **Professional services**: Lower commitment first. "Book a consultation."
- **Creative/agency**: Relationship-building. "View our work."

**Golden rule**: Make your case first, then ask for action. CTA appears AFTER value.

### Trust Signal Hierarchy

| Tier | Type | Example |
|------|------|---------|
| 1 (Strongest) | Specific, verifiable | "QBCC License #1234567" |
| 2 | Third-party validation | "4.8 stars (127 Google Reviews)" + link |
| 3 | Self-claimed | "Fully licensed and insured" |
| 4 (Weakest) | Generic assurances | "Quality guaranteed" |

One Tier 1 signal beats three Tier 4 signals. Distribute trust throughout the page — don't isolate in one section.

### Testimonial Approach

| Situation | Approach |
|-----------|----------|
| One powerful testimonial | Single featured quote, make it big |
| 3-6 good testimonials | Grid with variety, one featured |
| No real testimonials | Service promises, guarantees, process descriptions |

**Never use carousels** — users see 1 of 5 testimonials, <1% click controls. Show all or curate the best 3.

## Reference File Index

Each reference is a deep-dive (300-470 lines) with full principles, anti-patterns, implementation patterns, and business-specific guidance.

| File | Lines | Covers |
|------|-------|--------|
| `hero-patterns.md` | ~470 | Approach selection, constraint-based creativity, overlay techniques, responsive behaviour, page-specific heroes |
| `card-patterns.md` | ~550 | Layout decision framework, anti-sameness strategies, grid math, orphan handling, CSS patterns, business context |
| `cta-patterns.md` | ~420 | Action hierarchy, placement strategy, copy principles, visual design, mobile considerations, context-specific CTAs |
| `trust-signals.md` | ~490 | Trust psychology, trust hierarchy, context-sensitive trust, lead-gen vs client, placement strategy, anti-patterns |
| `testimonial-patterns.md` | ~350 | Social proof psychology, lead-gen ethics, design approach selection, content principles, placement, alternatives |
