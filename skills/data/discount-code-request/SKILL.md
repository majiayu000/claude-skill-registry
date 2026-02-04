---
name: discount-code-request
description: Respond to discount or coupon requests. Use when a customer asks for a promo code or special pricing.
metadata:
  trigger_phrases:
      - "respond discount"
      - "discount coupon"
      - "coupon requests"
  related_skills: ["ppp-pricing", "subscription-renewal-issue", "duplicate-purchase"]
  sample_size: "388"
  validation: |
    required_phrases:
      - "thanks for reaching out"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 388\navg_thread_length: 2.87\ntop_phrases:\n  - phrase: \"thanks for reaching out\"\n    count: 65\n    percent: 16.8\n  - phrase: \"https www totaltypescript com\"\n    count: 50\n    percent: 12.9\n  - phrase: \"let me know if\"\n    count: 43\n    percent: 11.1\n  - phrase: \"me know if you\"\n    count: 38\n    percent: 9.8\n  - phrase: \"if you have any\"\n    count: 34\n    percent: 8.8\n  - phrase: \"interest in the course\"\n    count: 29\n    percent: 7.5\n  - phrase: \"is no longer available\"\n    count: 29\n    percent: 7.5\n  - phrase: \"for your interest in\"\n    count: 27\n    percent: 7\n  - phrase: \"know if you have\"\n    count: 26\n    percent: 6.7\n  - phrase: \"to upgrade to the\"\n    count: 26\n    percent: 6.7"
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
- [ ] NOT introduce policy details that are not present in the verified response lines above.