---
name: ux-conversion
description: |
  This skill should be used when the user asks to 'improve UX', 'fix mobile experience',
  'optimize signup flow', 'increase conversions', 'design better CTAs', 'reduce form abandonment',
  'improve form UX', 'add trust signals', 'write microcopy', 'mobile-first design',
  'responsive layout', 'onboarding flow', 'reduce friction', 'improve checkout',
  or needs guidance on desktop/mobile UX patterns, conversion rate optimization,
  form design, CTA placement, user psychology, or high-converting user flows.
---

# UX & Conversion Optimization

Build interfaces that convert. This skill covers UX patterns for desktop/mobile, conversion optimization, and user psychology.

## Core Philosophy

1. **Every element earns its place** - Remove visual noise; minimize cognitive load
2. **Reduce friction ruthlessly** - Every click/field is a potential drop-off
3. **Mobile-first always** - 60%+ traffic is mobile; design smallest viewport first
4. **Data beats assumptions** - A/B test everything; use heatmaps and session recordings
5. **Speed is UX** - 1 second improvement = 7% conversion boost

## Quick Reference

| Topic | Key Principle | Details |
|-------|--------------|---------|
| **Forms** | Minimize fields; inline validation | [form-patterns.md](references/form-patterns.md) |
| **CTAs** | Specific, first-person, high-contrast | [cta-optimization.md](references/cta-optimization.md) |
| **Mobile** | 44px touch targets; thumb-zone primary actions | [mobile-patterns.md](references/mobile-patterns.md) |
| **Signup** | Time-to-value < 60s; progressive disclosure | [signup-flows.md](references/signup-flows.md) |
| **Trust** | Place near CTAs and checkout | [trust-signals.md](references/trust-signals.md) |
| **Copy** | Clarity over cleverness; action verbs | [microcopy.md](references/microcopy.md) |

## High-Impact Quick Wins

1. **Reduce form fields** to essentials only (42% lift from 15→5 fields)
2. **Use inline validation** with helpful error messages (22% success rate increase)
3. **Make CTAs specific** with first-person copy ("Get my report" > "Submit")
4. **Add progress indicators** to multi-step flows
5. **Place trust signals** near CTAs and checkout
6. **44px+ touch targets** on mobile with adequate spacing
7. **Offer guest checkout** prominently (62% of sites fail this)
8. **Get users to value** within 60 seconds of signup
9. **White space around CTAs** can boost conversions 232%
10. **Personalized CTAs** convert 42% better than generic

## Decision Framework

### When designing forms:
- Single column layout (always on mobile)
- Labels above fields (not placeholder-as-label)
- Smart defaults and autofill where possible
- Validate on blur, not on submit
- Mark optional fields, not required
- Group related fields logically

### When designing CTAs:
- High contrast against background
- Action verb + benefit: "Start my free trial"
- Large enough to tap (min 44px height)
- Isolated with generous padding/white space
- Repeat at end of long content

### When designing for mobile:
- Start at 320px, enhance upward
- Primary actions in bottom 1/3 (thumb zone)
- Reduce input: autofill, smart defaults, minimize typing
- Touch targets 44x44px minimum with spacing
- Compress images, lazy-load below fold

### When building signup/onboarding:
- Collect only essential info at signup (name, email, password)
- Use progress indicators ("Step 2 of 3")
- Get user to first "win" ASAP
- Personalize flow based on user type/goal (2-5 options)
- Provide skip option for experienced users
- Celebrate milestones to build momentum

### When adding trust signals:
- Security badges near payment/checkout
- Testimonials with real names, photos, specific results
- Social proof numbers ("10,000+ customers")
- Guarantees near CTAs to reduce hesitation
- Client logos for B2B credibility

## Anti-Patterns to Avoid

- Placeholder text as the only label (accessibility fail)
- Requiring account creation before showing value
- Credit card upfront for free trials
- Desktop-only optimization
- Generic CTAs ("Submit", "Click here")
- Validating only on form submit
- Hiding guest checkout option
- Tutorial overload on first visit
- Jargon and clever-but-unclear copy

## Responsive Breakpoints

```css
/* Mobile-first base styles */
.container { padding: 1rem; }

/* Tablet and up */
@media (min-width: 48em) {
  .container { padding: 2rem; max-width: 75rem; }
}

/* Desktop */
@media (min-width: 64em) {
  .container { /* desktop enhancements */ }
}
```

Break when content breaks, not at arbitrary device widths.

## Metrics That Matter

| Metric | Target | How to Improve |
|--------|--------|---------------|
| Conversion rate | 5-10%+ (avg is 2.35%) | Reduce friction, personalize CTAs |
| Form completion | 80%+ | Fewer fields, inline validation |
| Time to value | < 60 seconds | Streamline onboarding |
| Mobile bounce | < 40% | Speed, touch targets, thumb-zone design |
| Cart abandonment | < 70% | Guest checkout, trust signals, simplify |

For detailed patterns and examples, see the reference files in this skill.
