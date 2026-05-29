---
name: certificate-request
description: |
  Customer asks about course completion certificates or LinkedIn certificate options.
sample_size: 209
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 209
  avg_thread_length: 3.12
  top_phrases:
    - phrase: "let me know if"
      count: 52
      percent: 24.9
    - phrase: "me know if you"
      count: 40
      percent: 19.1
    - phrase: "know if you have"
      count: 40
      percent: 19.1
    - phrase: "if you have any"
      count: 38
      percent: 18.2
    - phrase: "thanks for reaching out"
      count: 34
      percent: 16.3
    - phrase: "a certificate of completion"
      count: 29
      percent: 13.9
    - phrase: "please let me know"
      count: 24
      percent: 11.5
    - phrase: "you have any further"
      count: 21
      percent: 10
    - phrase: "have any further questions"
      count: 21
      percent: 10
    - phrase: "for your interest in"
      count: 16
      percent: 7.7
---

# Certificate Request

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hello,"
- "Hey,"

Common core lines:
- "Thanks for reaching out!"
- "Best,"
- "Hi,"

Common closings:
- "Best,"
- "Please let me know if you have any further questions!"
- "Yes - when you complete the course you'll have the option to claim your certificate."

## Phrases That Work (4-gram frequency)

- "let me know if" — 52 (24.9%)
- "me know if you" — 40 (19.1%)
- "know if you have" — 40 (19.1%)
- "if you have any" — 38 (18.2%)
- "thanks for reaching out" — 34 (16.3%)
- "a certificate of completion" — 29 (13.9%)
- "please let me know" — 24 (11.5%)
- "you have any further" — 21 (10%)
- "have any further questions" — 21 (10%)
- "for your interest in" — 16 (7.7%)

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