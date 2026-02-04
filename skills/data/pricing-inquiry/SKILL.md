---
name: pricing-inquiry
description: Answer pricing questions for courses. Use when a customer asks about current price, pricing model, or availability.
metadata:
  trigger_phrases:
      - "answer pricing"
      - "pricing questions"
      - "questions courses"
  related_skills: ["installment-payment-option", "student-discount-request", "lesson-content-question", "discount-code-request", "course-difficulty-concern"]
  sample_size: "523"
  validation: |
    required_phrases:
      - "let me know if"
    forbidden_patterns:
      - "(?i)price is \\\\\\\\$"
      - "(?i)we can (?:do|offer) \\\\\\\\$"
      - "(?i)discount code"
      - "(?i)coupon"
      - "(?i)promo code"
      - "(?i)custom discount"
      - "(?i)special discount"
    max_length: 500
  metrics: "sample_size: 523\navg_thread_length: 2.84\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 90\n    percent: 17.2\n  - phrase: \"me know if you\"\n    count: 86\n    percent: 16.4\n  - phrase: \"know if you have\"\n    count: 86\n    percent: 16.4\n  - phrase: \"if you have any\"\n    count: 53\n    percent: 10.1\n  - phrase: \"thanks for reaching out\"\n    count: 52\n    percent: 9.9\n  - phrase: \"https www totaltypescript com\"\n    count: 50\n    percent: 9.6\n  - phrase: \"for your interest in\"\n    count: 43\n    percent: 8.2\n  - phrase: \"thanks for your interest\"\n    count: 40\n    percent: 7.6\n  - phrase: \"your interest in the\"\n    count: 40\n    percent: 7.6\n  - phrase: \"interest in the course\"\n    count: 40\n    percent: 7.6"
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
- [ ] NOT introduce policy details that are not present in the verified response lines above.
