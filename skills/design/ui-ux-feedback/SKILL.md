---
name: ui-ux-feedback
description: |
  Customer provides feedback about user interface, design, or requests new features.
sample_size: 216
validation:
  required_phrases:
    - "thanks for the feedback"
  forbidden_patterns: []
metrics:
  sample_size: 216
  avg_thread_length: 2.45
  top_phrases:
    - phrase: "thanks for the feedback"
      count: 29
      percent: 13.4
    - phrase: "thanks for reaching out"
      count: 16
      percent: 7.4
    - phrase: "we will definitely consider"
      count: 15
      percent: 6.9
    - phrase: "for the feedback we"
      count: 12
      percent: 5.6
    - phrase: "the feedback we will"
      count: 12
      percent: 5.6
    - phrase: "feedback we will definitely"
      count: 11
      percent: 5.1
    - phrase: "will definitely consider that"
      count: 11
      percent: 5.1
    - phrase: "let me know if"
      count: 9
      percent: 4.2
    - phrase: "www totaltypescript com profile"
      count: 8
      percent: 3.7
    - phrase: "thanks for the heads"
      count: 7
      percent: 3.2
---

# UI/UX Feedback or Feature Request

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
- "Thanks for the feedback, we will definitely consider that."
- "Thanks for reaching out, but we politely decline."

## Phrases That Work (4-gram frequency)

- "thanks for the feedback" — 29 (13.4%)
- "thanks for reaching out" — 16 (7.4%)
- "we will definitely consider" — 15 (6.9%)
- "for the feedback we" — 12 (5.6%)
- "the feedback we will" — 12 (5.6%)
- "feedback we will definitely" — 11 (5.1%)
- "will definitely consider that" — 11 (5.1%)
- "let me know if" — 9 (4.2%)
- "www totaltypescript com profile" — 8 (3.7%)
- "thanks for the heads" — 7 (3.2%)

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