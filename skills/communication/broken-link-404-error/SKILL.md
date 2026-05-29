---
name: broken-link-404-error
description: |
  Customer reports broken links, missing resources, or 404 errors on the website or in course materials.
sample_size: 236
validation:
  required_phrases:
    - "for the heads up"
  forbidden_patterns: []
metrics:
  sample_size: 236
  avg_thread_length: 2.96
  top_phrases:
    - phrase: "for the heads up"
      count: 61
      percent: 25.8
    - phrase: "thanks for the heads"
      count: 58
      percent: 24.6
    - phrase: "let me know if"
      count: 44
      percent: 18.6
    - phrase: "the heads up we'll"
      count: 17
      percent: 7.2
    - phrase: "me know if you"
      count: 15
      percent: 6.4
    - phrase: "let us know if"
      count: 15
      percent: 6.4
    - phrase: "heads up we'll look"
      count: 14
      percent: 5.9
    - phrase: "up we'll look into"
      count: 14
      percent: 5.9
    - phrase: "know if you have"
      count: 13
      percent: 5.5
    - phrase: "should be able to"
      count: 13
      percent: 5.5
---

# Broken Link or 404 Error

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hey,"
- "Hello! A fix for the invoice has been sent out. Can you retry https://epicreact.dev/invoice/ and let me know if that works for you?"

Common core lines:
- "Best,"
- ">>"
- "Hi,"

Common closings:
- "Best,"
- "Thanks for the heads up! We'll look into this ASAP."
- "Thanks for the heads up! Everything should be back up and running smoothly now. Let us know if that's not the case."

## Phrases That Work (4-gram frequency)

- "for the heads up" — 61 (25.8%)
- "thanks for the heads" — 58 (24.6%)
- "let me know if" — 44 (18.6%)
- "the heads up we'll" — 17 (7.2%)
- "me know if you" — 15 (6.4%)
- "let us know if" — 15 (6.4%)
- "heads up we'll look" — 14 (5.9%)
- "up we'll look into" — 14 (5.9%)
- "know if you have" — 13 (5.5%)
- "should be able to" — 13 (5.5%)

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