---
name: outdated-course-content
description: |
  Customer reports that course content is outdated or no longer accurate with current technology.
sample_size: 105
validation:
  required_phrases:
    - "for the heads up"
  forbidden_patterns: []
metrics:
  sample_size: 105
  avg_thread_length: 2.61
  top_phrases:
    - phrase: "for the heads up"
      count: 14
      percent: 13.3
    - phrase: "thanks for the heads"
      count: 13
      percent: 12.4
    - phrase: "if you have any"
      count: 12
      percent: 11.4
    - phrase: "is up to date"
      count: 11
      percent: 10.5
    - phrase: "know if you have"
      count: 11
      percent: 10.5
    - phrase: "up to date and"
      count: 10
      percent: 9.5
    - phrase: "thanks for reaching out"
      count: 9
      percent: 8.6
    - phrase: "the course is up"
      count: 8
      percent: 7.6
    - phrase: "course is up to"
      count: 8
      percent: 7.6
    - phrase: "let me know if"
      count: 8
      percent: 7.6
---

# Outdated Course Content

## Response Patterns (from samples)

Common openings:
- "Hello,"
- "Hi,"
- "Hi there,"

Common core lines:
- "Hello,"
- "Best,"
- "Thanks for reaching out!"

Common closings:
- "Best,"
- "Best wishes,"
- "Let me know if you have any other questions!"

## Phrases That Work (4-gram frequency)

- "for the heads up" — 14 (13.3%)
- "thanks for the heads" — 13 (12.4%)
- "if you have any" — 12 (11.4%)
- "is up to date" — 11 (10.5%)
- "know if you have" — 11 (10.5%)
- "up to date and" — 10 (9.5%)
- "thanks for reaching out" — 9 (8.6%)
- "the course is up" — 8 (7.6%)
- "course is up to" — 8 (7.6%)
- "let me know if" — 8 (7.6%)

## Tone Guidance (observed)

- Openings trend toward: "Hello,"
- Closings often include: "Best,"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above