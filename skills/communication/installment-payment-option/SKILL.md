---
name: installment-payment-option
description: |
  Customer inquires about payment plans or installment options for course purchases.
sample_size: 70
validation:
  required_phrases:
    - "the opportunity to upgrade"
  forbidden_patterns: []
metrics:
  sample_size: 70
  avg_thread_length: 2.6
  top_phrases:
    - phrase: "the opportunity to upgrade"
      count: 15
      percent: 21.4
    - phrase: "opportunity to upgrade to"
      count: 15
      percent: 21.4
    - phrase: "to upgrade to the"
      count: 15
      percent: 21.4
    - phrase: "upgrade to the pro"
      count: 15
      percent: 21.4
    - phrase: "difference in pricing between"
      count: 15
      percent: 21.4
    - phrase: "have the opportunity to"
      count: 14
      percent: 20
    - phrase: "you'll have the opportunity"
      count: 13
      percent: 18.6
    - phrase: "package later on for"
      count: 13
      percent: 18.6
    - phrase: "later on for the"
      count: 13
      percent: 18.6
    - phrase: "in pricing between it"
      count: 13
      percent: 18.6
---

# Installment Payment Option

## Response Patterns (from samples)

Common openings:
- "Hey,"
- "Hi,"
- "Hey Peter,"

Common core lines:
- "Best,"
- "Thanks for your interest in the course!"
- "Thanks for reaching out!"

Common closings:
- "Best,"
- "The upgrade option is only available to move up to the Pro Testing package from whichever level you start on. So you can upgrade from Basic or Standard to Pro, but not from Basic to Standard as a half-step."
- "The upgrade option is only available to move up to the Pro package from whichever level you start on. So you can upgrade from Basic or Standard to Pro, but not from Basic to Standard as a half-step."

## Phrases That Work (4-gram frequency)

- "the opportunity to upgrade" — 15 (21.4%)
- "opportunity to upgrade to" — 15 (21.4%)
- "to upgrade to the" — 15 (21.4%)
- "upgrade to the pro" — 15 (21.4%)
- "difference in pricing between" — 15 (21.4%)
- "have the opportunity to" — 14 (20%)
- "you'll have the opportunity" — 13 (18.6%)
- "package later on for" — 13 (18.6%)
- "later on for the" — 13 (18.6%)
- "in pricing between it" — 13 (18.6%)

## Tone Guidance (observed)

- Openings trend toward: "Hey,"
- Closings often include: "Best,"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above