---
name: pricing-inquiry
description: |
  Customer asks about course pricing, pricing models, or pricing availability.
sample_size: 523
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 523
  avg_thread_length: 2.84
  top_phrases:
    - phrase: "let me know if"
      count: 90
      percent: 17.2
    - phrase: "me know if you"
      count: 86
      percent: 16.4
    - phrase: "know if you have"
      count: 86
      percent: 16.4
    - phrase: "if you have any"
      count: 53
      percent: 10.1
    - phrase: "thanks for reaching out"
      count: 52
      percent: 9.9
    - phrase: "https www totaltypescript com"
      count: 50
      percent: 9.6
    - phrase: "for your interest in"
      count: 43
      percent: 8.2
    - phrase: "thanks for your interest"
      count: 40
      percent: 7.6
    - phrase: "your interest in the"
      count: 40
      percent: 7.6
    - phrase: "interest in the course"
      count: 40
      percent: 7.6
---

# Pricing Information

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hey,"
- "Hello,"

Common core lines:
- "Thanks for reaching out!"
- "Best,"
- "Thanks for your interest in the course!"

Common closings:
- "Best,"
- "Please let me know if you have any further questions!"
- "Let me know if you have any additional questions!"

## Phrases That Work (4-gram frequency)

- "let me know if" — 90 (17.2%)
- "me know if you" — 86 (16.4%)
- "know if you have" — 86 (16.4%)
- "if you have any" — 53 (10.1%)
- "thanks for reaching out" — 52 (9.9%)
- "https www totaltypescript com" — 50 (9.6%)
- "for your interest in" — 43 (8.2%)
- "thanks for your interest" — 40 (7.6%)
- "your interest in the" — 40 (7.6%)
- "interest in the course" — 40 (7.6%)

## Tone Guidance (observed)

- Openings trend toward: "Hi,"
- Closings often include: "Best,"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above