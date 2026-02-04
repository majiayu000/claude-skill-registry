---
name: installment-payment-option
description: Answer payment plan questions. Use when a customer asks about installments or split payments for a course.
metadata:
  trigger_phrases:
      - "answer payment"
      - "payment plan"
      - "plan questions"
  related_skills: ["pricing-inquiry", "lesson-content-question", "student-discount-request", "continuing-education-credits", "discount-code-request"]
  sample_size: "70"
  validation: |
    required_phrases:
      - "the opportunity to upgrade"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 70\navg_thread_length: 2.6\ntop_phrases:\n  - phrase: \"the opportunity to upgrade\"\n    count: 15\n    percent: 21.4\n  - phrase: \"opportunity to upgrade to\"\n    count: 15\n    percent: 21.4\n  - phrase: \"to upgrade to the\"\n    count: 15\n    percent: 21.4\n  - phrase: \"upgrade to the pro\"\n    count: 15\n    percent: 21.4\n  - phrase: \"difference in pricing between\"\n    count: 15\n    percent: 21.4\n  - phrase: \"have the opportunity to\"\n    count: 14\n    percent: 20\n  - phrase: \"you'll have the opportunity\"\n    count: 13\n    percent: 18.6\n  - phrase: \"package later on for\"\n    count: 13\n    percent: 18.6\n  - phrase: \"later on for the\"\n    count: 13\n    percent: 18.6\n  - phrase: \"in pricing between it\"\n    count: 13\n    percent: 18.6"
---
# Installment Payment Option

## Response Patterns (from samples)

Common openings:
- "Hey,"
- "Hi,"
- "Hey Peter,"

Common core lines:
- "Best,"
- "Thanks for your interest in the course!"
- "Thanks for reaching out!"

Common closings:
- "Best,"
- "The upgrade option is only available to move up to the Pro Testing package from whichever level you start on. So you can upgrade from Basic or Standard to Pro, but not from Basic to Standard as a half-step."
- "The upgrade option is only available to move up to the Pro package from whichever level you start on. So you can upgrade from Basic or Standard to Pro, but not from Basic to Standard as a half-step."

## Phrases That Work (4-gram frequency)

- "the opportunity to upgrade" — 15 (21.4%)
- "opportunity to upgrade to" — 15 (21.4%)
- "to upgrade to the" — 15 (21.4%)
- "upgrade to the pro" — 15 (21.4%)
- "difference in pricing between" — 15 (21.4%)
- "have the opportunity to" — 14 (20%)
- "you'll have the opportunity" — 13 (18.6%)
- "package later on for" — 13 (18.6%)
- "later on for the" — 13 (18.6%)
- "in pricing between it" — 13 (18.6%)

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