---
name: payment-method-issue
description: |
  Customer has issues with specific payment methods like credit cards, Apple Pay, or regional payment restrictions.
sample_size: 317
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 317
  avg_thread_length: 3.34
  top_phrases:
    - phrase: "let me know if"
      count: 45
      percent: 14.2
    - phrase: "me know if you"
      count: 42
      percent: 13.2
    - phrase: "thanks for reaching out"
      count: 41
      percent: 12.9
    - phrase: "know if you have"
      count: 36
      percent: 11.4
    - phrase: "if you have any"
      count: 35
      percent: 11
    - phrase: "payment via credit card"
      count: 30
      percent: 9.5
    - phrase: "i apologize for the"
      count: 29
      percent: 9.1
    - phrase: "only accept payment via"
      count: 27
      percent: 8.5
    - phrase: "accept payment via credit"
      count: 27
      percent: 8.5
    - phrase: "to purchase the course"
      count: 25
      percent: 7.9
---

# Payment Method Problem

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hello,"
- "Hey,"

Common core lines:
- "Thanks for reaching out!"
- "Hi,"
- "Thanks for your interest in the course!"

Common closings:
- "Best,"
- "Now go and make the world a better place :)"
- "It may take 5-10 business days for the refunded amount to show up in your account, depending on how quickly it's processed by your financial institution."

## Phrases That Work (4-gram frequency)

- "let me know if" — 45 (14.2%)
- "me know if you" — 42 (13.2%)
- "thanks for reaching out" — 41 (12.9%)
- "know if you have" — 36 (11.4%)
- "if you have any" — 35 (11%)
- "payment via credit card" — 30 (9.5%)
- "i apologize for the" — 29 (9.1%)
- "only accept payment via" — 27 (8.5%)
- "accept payment via credit" — 27 (8.5%)
- "to purchase the course" — 25 (7.9%)

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