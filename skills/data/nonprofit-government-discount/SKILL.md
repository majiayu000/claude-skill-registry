---
name: nonprofit-government-discount
description: Respond to nonprofit or government discount requests. Use when an organization asks about special pricing for nonprofit, education, or government.
metadata:
  trigger_phrases:
      - "respond nonprofit"
      - "nonprofit government"
      - "government discount"
  related_skills: ["student-discount-request", "discount-code-request", "pricing-inquiry", "continuing-education-credits", "installment-payment-option"]
  sample_size: "21"
  validation: |
    required_phrases:
      - "https github com epicweb"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 21\navg_thread_length: 4.33\ntop_phrases:\n  - phrase: \"https github com epicweb\"\n    count: 4\n    percent: 19\n  - phrase: \"github com epicweb dev\"\n    count: 4\n    percent: 19\n  - phrase: \"thanks for reaching out\"\n    count: 4\n    percent: 19\n  - phrase: \"com epicweb dev mcp\"\n    count: 3\n    percent: 14.3\n  - phrase: \"sep 17 2025 at\"\n    count: 3\n    percent: 14.3\n  - phrase: \"email wrote hello kent\"\n    count: 3\n    percent: 14.3\n  - phrase: \"please let me know\"\n    count: 3\n    percent: 14.3\n  - phrase: \"if you have any\"\n    count: 3\n    percent: 14.3\n  - phrase: \"thanks for your interest\"\n    count: 3\n    percent: 14.3\n  - phrase: \"for your interest in\"\n    count: 3\n    percent: 14.3"
---
# Nonprofit and Government Discounts

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hey Scott,"
- "Hey Monika,"

Common core lines:
- "wrote:"
- "Hey Scott,"
- "Hello Kent,"

Common closings:
- "Best,"
- "Mute EpicAI.pro emails | Unsubscribe | Update your profile | P.O. Box 562, American Fork, Utah 84003"
- "I can go ahead and create an invoice before purchase but It would be full price."

## Phrases That Work (4-gram frequency)

- "https github com epicweb" — 4 (19%)
- "github com epicweb dev" — 4 (19%)
- "thanks for reaching out" — 4 (19%)
- "com epicweb dev mcp" — 3 (14.3%)
- "sep 17 2025 at" — 3 (14.3%)
- "email wrote hello kent" — 3 (14.3%)
- "please let me know" — 3 (14.3%)
- "if you have any" — 3 (14.3%)
- "thanks for your interest" — 3 (14.3%)
- "for your interest in" — 3 (14.3%)

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