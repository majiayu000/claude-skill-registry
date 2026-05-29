---
name: access-locked-out
description: |
  Customer cannot log in, access course materials, or restore their account despite having purchased content.
sample_size: 878
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 878
  avg_thread_length: 3.68
  top_phrases:
    - phrase: "let me know if"
      count: 227
      percent: 25.9
    - phrase: "if you have any"
      count: 167
      percent: 19
    - phrase: "me know if you"
      count: 165
      percent: 18.8
    - phrase: "know if you have"
      count: 128
      percent: 14.6
    - phrase: "email let me know"
      count: 84
      percent: 9.6
    - phrase: "let us know if"
      count: 79
      percent: 9
    - phrase: "at the top of"
      count: 78
      percent: 8.9
    - phrase: "to purchase the course"
      count: 77
      percent: 8.8
    - phrase: "the top of https"
      count: 75
      percent: 8.5
    - phrase: "everything should be back"
      count: 73
      percent: 8.3
---

# Account Access Issues

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hello,"
- "Hey,"

Common core lines:
- "Best,"
- "Hi,"
- "Hello,"

Common closings:
- "Best,"
- "Thanks for the heads up! Everything should be back up and running smoothly now. Let us know if that's not the case."
- "If you have any trouble accessing the course, please let us know!"

## Phrases That Work (4-gram frequency)

- "let me know if" — 227 (25.9%)
- "if you have any" — 167 (19%)
- "me know if you" — 165 (18.8%)
- "know if you have" — 128 (14.6%)
- "email let me know" — 84 (9.6%)
- "let us know if" — 79 (9%)
- "at the top of" — 78 (8.9%)
- "to purchase the course" — 77 (8.8%)
- "the top of https" — 75 (8.5%)
- "everything should be back" — 73 (8.3%)

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