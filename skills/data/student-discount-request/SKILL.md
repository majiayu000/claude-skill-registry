---
name: student-discount-request
description: Respond to student discount inquiries. Use when a student or academic asks about educational pricing.
metadata:
  trigger_phrases:
      - "respond student"
      - "student discount"
      - "discount inquiries"
  related_skills: ["ppp-pricing"]
  sample_size: "114"
  validation: |
    required_phrases:
      - "thanks for your interest"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 114\navg_thread_length: 2.26\ntop_phrases:\n  - phrase: \"thanks for your interest\"\n    count: 33\n    percent: 28.9\n  - phrase: \"for your interest in\"\n    count: 33\n    percent: 28.9\n  - phrase: \"interest in the course\"\n    count: 33\n    percent: 28.9\n  - phrase: \"your interest in the\"\n    count: 28\n    percent: 24.6\n  - phrase: \"https www totaltypescript com\"\n    count: 23\n    percent: 20.2\n  - phrase: \"in the course we\"\n    count: 23\n    percent: 20.2\n  - phrase: \"to the pro package\"\n    count: 21\n    percent: 18.4\n  - phrase: \"thanks for reaching out\"\n    count: 20\n    percent: 17.5\n  - phrase: \"we don't currently offer\"\n    count: 17\n    percent: 14.9\n  - phrase: \"to upgrade to the\"\n    count: 16\n    percent: 14"
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
- [ ] NOT introduce policy details that are not present in the verified response lines above.