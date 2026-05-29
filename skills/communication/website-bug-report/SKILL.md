---
name: website-bug-report
description: |
  Customer reports bugs, errors, or issues with the website platform.
sample_size: 286
validation:
  required_phrases:
    - "thanks for the heads"
  forbidden_patterns: []
metrics:
  sample_size: 286
  avg_thread_length: 2.78
  top_phrases:
    - phrase: "thanks for the heads"
      count: 69
      percent: 24.1
    - phrase: "for the heads up"
      count: 69
      percent: 24.1
    - phrase: "let us know if"
      count: 52
      percent: 18.2
    - phrase: "let me know if"
      count: 35
      percent: 12.2
    - phrase: "now let us know"
      count: 33
      percent: 11.5
    - phrase: "the heads up we'll"
      count: 31
      percent: 10.8
    - phrase: "heads up we'll look"
      count: 29
      percent: 10.1
    - phrase: "up we'll look into"
      count: 29
      percent: 10.1
    - phrase: "everything should be back"
      count: 26
      percent: 9.1
    - phrase: "us know if you"
      count: 25
      percent: 8.7
---

# Website Bug Report

## Response Patterns (from samples)

Common openings:
- "Hello! A fix for the invoice has been sent out. Can you retry https://epicreact.dev/invoice/ and let me know if that works for you?"
- "Hey,"
- "Hello,"

Common core lines:
- "Best,"
- "Thanks for the heads up! We'll look into this ASAP."
- "Happy coding!"

Common closings:
- "Best,"
- "Thanks for the heads up! We'll look into this ASAP."
- "Happy coding!"

## Phrases That Work (4-gram frequency)

- "thanks for the heads" — 69 (24.1%)
- "for the heads up" — 69 (24.1%)
- "let us know if" — 52 (18.2%)
- "let me know if" — 35 (12.2%)
- "now let us know" — 33 (11.5%)
- "the heads up we'll" — 31 (10.8%)
- "heads up we'll look" — 29 (10.1%)
- "up we'll look into" — 29 (10.1%)
- "everything should be back" — 26 (9.1%)
- "us know if you" — 25 (8.7%)

## Tone Guidance (observed)

- Openings trend toward: "Hello! A fix for the invoice has been sent out. Can you retry https://epicreact.dev/invoice/ and let me know if that works for you?"
- Closings often include: "Best,"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above