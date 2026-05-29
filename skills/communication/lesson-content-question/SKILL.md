---
name: lesson-content-question
description: |
  Customer asks specific questions about lesson content, code, or concepts.
sample_size: 414
validation:
  required_phrases:
    - "thanks for reaching out"
  forbidden_patterns: []
metrics:
  sample_size: 414
  avg_thread_length: 2.5
  top_phrases:
    - phrase: "thanks for reaching out"
      count: 49
      percent: 11.8
    - phrase: "insights can help others"
      count: 47
      percent: 11.4
    - phrase: "can help others too"
      count: 46
      percent: 11.1
    - phrase: "your questions and insights"
      count: 43
      percent: 10.4
    - phrase: "questions and insights can"
      count: 43
      percent: 10.4
    - phrase: "and insights can help"
      count: 43
      percent: 10.4
    - phrase: "plus your questions and"
      count: 42
      percent: 10.1
    - phrase: "hope this helps best"
      count: 39
      percent: 9.4
    - phrase: "help others too i"
      count: 38
      percent: 9.2
    - phrase: "others too i hope"
      count: 38
      percent: 9.2
---

# Lesson Content Question

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hey there,"
- "Hello,"

Common core lines:
- ">>"
- "Best,"
- ">"

Common closings:
- "Best,"
- "Thanks!"
- "If you have coding questions, you can ask them in the community Discord channel we've set up here."

## Phrases That Work (4-gram frequency)

- "thanks for reaching out" — 49 (11.8%)
- "insights can help others" — 47 (11.4%)
- "can help others too" — 46 (11.1%)
- "your questions and insights" — 43 (10.4%)
- "questions and insights can" — 43 (10.4%)
- "and insights can help" — 43 (10.4%)
- "plus your questions and" — 42 (10.1%)
- "hope this helps best" — 39 (9.4%)
- "help others too i" — 38 (9.2%)
- "others too i hope" — 38 (9.2%)

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