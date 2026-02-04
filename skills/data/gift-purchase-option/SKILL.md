---
name: gift-purchase-option
description: Guide gift purchases. Use when a customer wants to buy a course for someone else.
metadata:
  trigger_phrases:
      - "guide gift"
      - "gift purchases"
      - "purchases customer"
  related_skills: ["duplicate-purchase", "pricing-inquiry", "learning-path-guidance", "installment-payment-option", "course-difficulty-concern"]
  sample_size: "47"
  validation: |
    required_phrases:
      - "let me know if"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 47\navg_thread_length: 3.7\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 28\n    percent: 59.6\n  - phrase: \"if you have any\"\n    count: 22\n    percent: 46.8\n  - phrase: \"me know if you\"\n    count: 15\n    percent: 31.9\n  - phrase: \"know if you have\"\n    count: 15\n    percent: 31.9\n  - phrase: \"please let me know\"\n    count: 14\n    percent: 29.8\n  - phrase: \"email let me know\"\n    count: 11\n    percent: 23.4\n  - phrase: \"using that email address\"\n    count: 11\n    percent: 23.4\n  - phrase: \"you have any further\"\n    count: 10\n    percent: 21.3\n  - phrase: \"have any further questions\"\n    count: 10\n    percent: 21.3\n  - phrase: \"license to email let\"\n    count: 10\n    percent: 21.3"
---
# Gift Purchase Option

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hey Tanguy,"
- "Hey,"

Common core lines:
- "Thanks for reaching out!"
- "Please let me know if you have any further questions!"
- "I've transferred your license to [EMAIL]."

Common closings:
- "Please let me know if you have any further questions!"
- "Please let me know if they have trouble logging in or if you have any further questions!"
- "Please let me know if your friend has trouble logging in or if you have any further questions!"

## Phrases That Work (4-gram frequency)

- "let me know if" — 28 (59.6%)
- "if you have any" — 22 (46.8%)
- "me know if you" — 15 (31.9%)
- "know if you have" — 15 (31.9%)
- "please let me know" — 14 (29.8%)
- "email let me know" — 11 (23.4%)
- "using that email address" — 11 (23.4%)
- "you have any further" — 10 (21.3%)
- "have any further questions" — 10 (21.3%)
- "license to email let" — 10 (21.3%)

## Tone Guidance (observed)

- Openings trend toward: "Hi,"
- Closings often include: "Please let me know if you have any further questions!"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above
- [ ] NOT introduce policy details that are not present in the verified response lines above.