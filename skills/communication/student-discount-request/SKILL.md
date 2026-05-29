---
name: student-discount-request
description: |
  Student or academic inquirer asks about educational discounts.
sample_size: 114
validation:
  required_phrases:
    - "thanks for your interest"
  forbidden_patterns: []
metrics:
  sample_size: 114
  avg_thread_length: 2.26
  top_phrases:
    - phrase: "thanks for your interest"
      count: 33
      percent: 28.9
    - phrase: "for your interest in"
      count: 33
      percent: 28.9
    - phrase: "interest in the course"
      count: 33
      percent: 28.9
    - phrase: "your interest in the"
      count: 28
      percent: 24.6
    - phrase: "https www totaltypescript com"
      count: 23
      percent: 20.2
    - phrase: "in the course we"
      count: 23
      percent: 20.2
    - phrase: "to the pro package"
      count: 21
      percent: 18.4
    - phrase: "thanks for reaching out"
      count: 20
      percent: 17.5
    - phrase: "we don't currently offer"
      count: 17
      percent: 14.9
    - phrase: "to upgrade to the"
      count: 16
      percent: 14
---

# Student Discount Request

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hey,"
- "Hello,"

Common core lines:
- "Thanks for your interest in the course!"
- "Hi,"
- "Thanks for reaching out!"

Common closings:
- "Best,"
- "The upgrade option is only available to move up to the Pro package from whichever level you start on. So you can upgrade from Basic or Standard to Pro, but not from Basic to Standard as a half-step."
- "https://www.totaltypescript.com/tutorials"

## Phrases That Work (4-gram frequency)

- "thanks for your interest" — 33 (28.9%)
- "for your interest in" — 33 (28.9%)
- "interest in the course" — 33 (28.9%)
- "your interest in the" — 28 (24.6%)
- "https www totaltypescript com" — 23 (20.2%)
- "in the course we" — 23 (20.2%)
- "to the pro package" — 21 (18.4%)
- "thanks for reaching out" — 20 (17.5%)
- "we don't currently offer" — 17 (14.9%)
- "to upgrade to the" — 16 (14%)

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