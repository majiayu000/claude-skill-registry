---
name: duplicate-purchase
description: Resolve duplicate purchases. Use when a customer bought the same course or license twice or was charged twice.
metadata:
  trigger_phrases:
      - "resolve duplicate"
      - "duplicate purchases"
      - "purchases customer"
  related_skills: ["subscription-renewal-issue", "refund-request", "ppp-pricing", "discount-code-request"]
  sample_size: "234"
  validation: |
    required_phrases:
      - "let me know if"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 234\navg_thread_length: 4.22\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 78\n    percent: 33.3\n  - phrase: \"me know if you\"\n    count: 56\n    percent: 23.9\n  - phrase: \"5 10 business days\"\n    count: 53\n    percent: 22.6\n  - phrase: \"if you have any\"\n    count: 51\n    percent: 21.8\n  - phrase: \"take 5 10 business\"\n    count: 51\n    percent: 21.8\n  - phrase: \"it may take 5\"\n    count: 49\n    percent: 20.9\n  - phrase: \"may take 5 10\"\n    count: 49\n    percent: 20.9\n  - phrase: \"10 business days for\"\n    count: 49\n    percent: 20.9\n  - phrase: \"business days for the\"\n    count: 49\n    percent: 20.9\n  - phrase: \"days for the refunded\"\n    count: 49\n    percent: 20.9"
---
# Duplicate Purchase

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hello,"
- "Hey,"

Common core lines:
- "It may take 5-10 business days for the refunded amount to show up in your account, depending on how quickly it's processed by your financial institution."
- "[EMAIL]"
- "Best,"

Common closings:
- "It may take 5-10 business days for the refunded amount to show up in your account, depending on how quickly it's processed by your financial institution."
- "Best,"
- "Let me know if you have any issues requesting login links using that email address."

## Phrases That Work (4-gram frequency)

- "let me know if" — 78 (33.3%)
- "me know if you" — 56 (23.9%)
- "5 10 business days" — 53 (22.6%)
- "if you have any" — 51 (21.8%)
- "take 5 10 business" — 51 (21.8%)
- "it may take 5" — 49 (20.9%)
- "may take 5 10" — 49 (20.9%)
- "10 business days for" — 49 (20.9%)
- "business days for the" — 49 (20.9%)
- "days for the refunded" — 49 (20.9%)

## Tone Guidance (observed)

- Openings trend toward: "Hi,"
- Closings often include: "It may take 5-10 business days for the refunded amount to show up in your account, depending on how quickly it's processed by your financial institution."

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above
- [ ] NOT introduce policy details that are not present in the verified response lines above.