---
name: payment-method-issue
description: Resolve payment method problems. Use when a customer has trouble paying with a card, Apple Pay, or a regional payment option.
metadata:
  trigger_phrases:
      - "resolve payment"
      - "payment method"
      - "method problems"
  related_skills: ["invoice-billing-statement"]
  sample_size: "317"
  validation: |
    required_phrases:
      - "let me know if"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 317\navg_thread_length: 3.34\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 45\n    percent: 14.2\n  - phrase: \"me know if you\"\n    count: 42\n    percent: 13.2\n  - phrase: \"thanks for reaching out\"\n    count: 41\n    percent: 12.9\n  - phrase: \"know if you have\"\n    count: 36\n    percent: 11.4\n  - phrase: \"if you have any\"\n    count: 35\n    percent: 11\n  - phrase: \"payment via credit card\"\n    count: 30\n    percent: 9.5\n  - phrase: \"i apologize for the\"\n    count: 29\n    percent: 9.1\n  - phrase: \"only accept payment via\"\n    count: 27\n    percent: 8.5\n  - phrase: \"accept payment via credit\"\n    count: 27\n    percent: 8.5\n  - phrase: \"to purchase the course\"\n    count: 25\n    percent: 7.9"
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
- [ ] NOT introduce policy details that are not present in the verified response lines above.