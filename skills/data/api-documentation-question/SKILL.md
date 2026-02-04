---
name: api-documentation-question
description: Answer API and technical documentation questions. Use when a customer asks about API usage, code implementation, or integration details.
metadata:
  trigger_phrases:
      - "answer api"
      - "api technical"
      - "technical documentation"
  related_skills: ["lesson-content-question", "pricing-inquiry", "workshop-technical-setup", "certificate-request", "installment-payment-option"]
  sample_size: "33"
  validation: |
    required_phrases:
      - "insights can help others"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 33\navg_thread_length: 2.48\ntop_phrases:\n  - phrase: \"insights can help others\"\n    count: 13\n    percent: 39.4\n  - phrase: \"can help others too\"\n    count: 13\n    percent: 39.4\n  - phrase: \"plus your questions and\"\n    count: 12\n    percent: 36.4\n  - phrase: \"your questions and insights\"\n    count: 12\n    percent: 36.4\n  - phrase: \"questions and insights can\"\n    count: 12\n    percent: 36.4\n  - phrase: \"and insights can help\"\n    count: 12\n    percent: 36.4\n  - phrase: \"help others too i\"\n    count: 9\n    percent: 27.3\n  - phrase: \"others too i hope\"\n    count: 9\n    percent: 27.3\n  - phrase: \"too i hope this\"\n    count: 9\n    percent: 27.3\n  - phrase: \"i hope this helps\"\n    count: 9\n    percent: 27.3"
---
# API or Technical Documentation Question

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hey,"
- "Hey there,"

Common core lines:
- "Best,"
- "I hope this helps!"
- "Hi,"

Common closings:
- "Best,"
- "Best wishes,"
- "Thanks!"

## Phrases That Work (4-gram frequency)

- "insights can help others" — 13 (39.4%)
- "can help others too" — 13 (39.4%)
- "plus your questions and" — 12 (36.4%)
- "your questions and insights" — 12 (36.4%)
- "questions and insights can" — 12 (36.4%)
- "and insights can help" — 12 (36.4%)
- "help others too i" — 9 (27.3%)
- "others too i hope" — 9 (27.3%)
- "too i hope this" — 9 (27.3%)
- "i hope this helps" — 9 (27.3%)

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