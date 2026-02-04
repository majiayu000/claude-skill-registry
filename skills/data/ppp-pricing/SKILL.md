---
name: ppp-pricing
description: Explain Purchasing Power Parity pricing. Use when a customer asks about PPP, regional pricing, affordability, or discount stacking.
metadata:
  trigger_phrases:
      - "explain purchasing"
      - "purchasing power"
      - "power parity"
  related_skills: ["website-bug-report", "student-discount-request", "discount-code-request", "duplicate-purchase", "subscription-renewal-issue"]
  sample_size: "715"
  validation: |
    required_phrases:
      - "parity"
    forbidden_patterns:
      - "(?i)coupon"
      - "(?i)discount code"
      - "(?i)custom discount"
      - "(?i)special discount"
      - "(?i)extended this discount"
      - "(?i)free license"
    max_length: 500
  metrics: "sample_size: 715\navg_thread_length: 2.90\ntop_phrases:\n  - phrase: \"for your interest in\"\n    count: 147\n    percent: 20.6\n  - phrase: \"thanks for your interest\"\n    count: 146\n    percent: 20.4\n  - phrase: \"your interest in the\"\n    count: 136\n    percent: 19.0\n  - phrase: \"interest in the course\"\n    count: 135\n    percent: 18.9\n  - phrase: \"on the pricing page\"\n    count: 103\n    percent: 14.4\n  - phrase: \"automatically show up on\"\n    count: 102\n    percent: 14.3\n  - phrase: \"show up on the\"\n    count: 102\n    percent: 14.3\n  - phrase: \"up on the pricing\"\n    count: 102\n    percent: 14.3\n  - phrase: \"we offer parity pricing\"\n    count: 101\n    percent: 14.1\n  - phrase: \"offer parity pricing in\"\n    count: 101\n    percent: 14.1"
---
# PPP Pricing

You're handling a Purchasing Power Parity question.

## What PPP Is

- Regional discounts for customers in qualifying countries
- Checkbox option on purchase page
- Automated by location detection
- PPP licenses have restrictions (region-locked, no bonus content)

## Sub-categories

- How to get PPP (checkbox on pricing page)
- Discount stacking with sales/bundles
- Scholarship/free enrollment requests
- Restrictions (region-locked, core curriculum only)

## Common Questions & Answers

### "How do I get PPP?"
> If you're in a qualifying region, there's a checkbox on the purchase page.

### "Can I stack PPP with sale discount?"
> No. Discounts don't stack. PPP IS the best discount we offer.

### "Can I get a bigger discount than PPP?"
> No. PPP is the maximum. Point them to free content as alternative.

### "What are PPP restrictions?"
> Region-locked, core curriculum only (no bonus interviews/content).

## Phrases That Work

- "PPP is the best discount we can offer"
- "Discounts don't stack - we give the very best discount available"
- "If you're in a qualifying region, you'll see a checkbox option"
- "We also have free content: [link to tutorials]"

## Tone

- Firm but friendly on discount limits
- Don't apologize for pricing policy
- Offer free content as genuine alternative, not consolation prize
- Don't negotiate or make exceptions

## Product Links

| Product | Purchase | Free Content |
|---------|----------|--------------|
| Total TypeScript | totaltypescript.com/buy | totaltypescript.com/tutorials |
| Epic React | epicreact.dev/buy | epicreact.dev/tutorials |
| Epic Web | epicweb.dev/buy | epicweb.dev/tutorials |
| Testing JavaScript | testingjavascript.com/buy | - |

## What NOT To Do

- Don't create custom discount codes
- Don't promise "I'll check with the team"
- Don't suggest workarounds to get bigger discounts
- Don't over-explain the economics of PPP

## Validation

Draft must:
- [ ] NOT offer or promise additional/custom discounts
- [ ] Mention free tutorials if declining a discount request
- [ ] Be clear that discounts don't stack (if asked)
