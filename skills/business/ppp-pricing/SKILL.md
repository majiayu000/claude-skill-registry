---
name: ppp-pricing
description: |
  Purchasing Power Parity pricing questions. Triggers on "PPP", "regional discount",
  "country discount", "can't afford", scholarship requests, or discount stacking questions.
sample_size: 715
validation:
  required_phrases:
    - "parity"
  forbidden_patterns:
    - "(?i)coupon"
    - "(?i)discount code"
    - "(?i)custom discount"
    - "(?i)special discount"
    - "(?i)extended this discount"
    - "(?i)free license"
metrics:
  sample_size: 715
  avg_thread_length: 2.90
  top_phrases:
    - phrase: "for your interest in"
      count: 147
      percent: 20.6
    - phrase: "thanks for your interest"
      count: 146
      percent: 20.4
    - phrase: "your interest in the"
      count: 136
      percent: 19.0
    - phrase: "interest in the course"
      count: 135
      percent: 18.9
    - phrase: "on the pricing page"
      count: 103
      percent: 14.4
    - phrase: "automatically show up on"
      count: 102
      percent: 14.3
    - phrase: "show up on the"
      count: 102
      percent: 14.3
    - phrase: "up on the pricing"
      count: 102
      percent: 14.3
    - phrase: "we offer parity pricing"
      count: 101
      percent: 14.1
    - phrase: "offer parity pricing in"
      count: 101
      percent: 14.1
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
