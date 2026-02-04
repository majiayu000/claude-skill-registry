---
name: access-locked-out
description: Restore access for customers who are locked out of their account or courses. Use when a paying customer cannot log in, access materials, or restore purchases.
metadata:
  trigger_phrases:
      - "restore access"
      - "access customers"
      - "customers who"
  related_skills: ["email-change", "website-bug-report"]
  sample_size: "878"
  validation: |
    required_phrases:
      - "used to purchase the"
      - "login link"
    forbidden_patterns:
      - "(?i)chargeback"
      - "(?i)purchase order"
      - "(?i)wire transfer"
      - "(?i)bank transfer"
      - "(?i)tax invoice"
      - "(?i)vat number"
      - "(?i)invoice number"
    max_length: 500
  metrics: "sample_size: 878\navg_thread_length: 3.68\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 227\n    percent: 25.9\n  - phrase: \"if you have any\"\n    count: 167\n    percent: 19\n  - phrase: \"me know if you\"\n    count: 165\n    percent: 18.8\n  - phrase: \"know if you have\"\n    count: 128\n    percent: 14.6\n  - phrase: \"let us know if\"\n    count: 79\n    percent: 9\n  - phrase: \"at the top of\"\n    count: 78\n    percent: 8.9\n  - phrase: \"to purchase the course\"\n    count: 77\n    percent: 8.8\n  - phrase: \"the top of https\"\n    count: 75\n    percent: 8.5\n  - phrase: \"everything should be back\"\n    count: 73\n    percent: 8.3\n  - phrase: \"used to purchase the\"\n    count: 73\n    percent: 8.3"
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
- "let us know if" — 79 (9%)
- "at the top of" — 78 (8.9%)
- "to purchase the course" — 77 (8.8%)
- "the top of https" — 75 (8.5%)
- "everything should be back" — 73 (8.3%)
- "used to purchase the" — 73 (8.3%)

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
