---
name: discount-code-request
description: |
  Customer requests discount codes, coupon codes, or promotional pricing.
sample_size: 388
validation:
  required_phrases:
    - "thanks for reaching out"
  forbidden_patterns: []
metrics:
  sample_size: 388
  avg_thread_length: 2.87
  top_phrases:
    - phrase: "thanks for reaching out"
      count: 65
      percent: 16.8
    - phrase: "https www totaltypescript com"
      count: 50
      percent: 12.9
    - phrase: "let me know if"
      count: 43
      percent: 11.1
    - phrase: "me know if you"
      count: 38
      percent: 9.8
    - phrase: "if you have any"
      count: 34
      percent: 8.8
    - phrase: "interest in the course"
      count: 29
      percent: 7.5
    - phrase: "is no longer available"
      count: 29
      percent: 7.5
    - phrase: "for your interest in"
      count: 27
      percent: 7
    - phrase: "know if you have"
      count: 26
      percent: 6.7
    - phrase: "to upgrade to the"
      count: 26
      percent: 6.7
---

# Discount Code Request

## Response Patterns (from samples)

Common openings:
- "Hey,"
- "Hi there,"
- "Hello,"

Common core lines:
- "Thanks for reaching out!"
- "Best,"
- "Thanks for your interest in the course!"

Common closings:
- "Best,"
- "I hope you’ll still consider enrolling in our training. If you have any other questions or if there’s anything else I can assist you with, please let me know."
- "Alternatively, if you'd like to start with either the Basic or Standard Testing packages now, you'll have the opportunity to upgrade to the Pro Testing package later on for the current difference in pricing between it and your initial purchase tier."

## Phrases That Work (4-gram frequency)

- "thanks for reaching out" — 65 (16.8%)
- "https www totaltypescript com" — 50 (12.9%)
- "let me know if" — 43 (11.1%)
- "me know if you" — 38 (9.8%)
- "if you have any" — 34 (8.8%)
- "interest in the course" — 29 (7.5%)
- "is no longer available" — 29 (7.5%)
- "for your interest in" — 27 (7%)
- "know if you have" — 26 (6.7%)
- "to upgrade to the" — 26 (6.7%)

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