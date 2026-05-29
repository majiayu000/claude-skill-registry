---
name: api-documentation-question
description: |
  Customer asks questions about API usage, code implementation, or technical documentation.
sample_size: 33
validation:
  required_phrases:
    - "insights can help others"
  forbidden_patterns: []
metrics:
  sample_size: 33
  avg_thread_length: 2.48
  top_phrases:
    - phrase: "insights can help others"
      count: 13
      percent: 39.4
    - phrase: "can help others too"
      count: 13
      percent: 39.4
    - phrase: "plus your questions and"
      count: 12
      percent: 36.4
    - phrase: "your questions and insights"
      count: 12
      percent: 36.4
    - phrase: "questions and insights can"
      count: 12
      percent: 36.4
    - phrase: "and insights can help"
      count: 12
      percent: 36.4
    - phrase: "help others too i"
      count: 9
      percent: 27.3
    - phrase: "others too i hope"
      count: 9
      percent: 27.3
    - phrase: "too i hope this"
      count: 9
      percent: 27.3
    - phrase: "i hope this helps"
      count: 9
      percent: 27.3
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