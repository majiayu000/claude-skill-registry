---
name: course-difficulty-concern
description: |
  Customer expresses concern about course difficulty level or prerequisite knowledge needed.
sample_size: 77
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 77
  avg_thread_length: 2.62
  top_phrases:
    - phrase: "let me know if"
      count: 10
      percent: 13
    - phrase: "me know if you"
      count: 8
      percent: 10.4
    - phrase: "know if you have"
      count: 8
      percent: 10.4
    - phrase: "if you have any"
      count: 8
      percent: 10.4
    - phrase: "thanks for reaching out"
      count: 8
      percent: 10.4
    - phrase: "thanks for the feedback"
      count: 5
      percent: 6.5
    - phrase: "feedback and giving the"
      count: 5
      percent: 6.5
    - phrase: "and giving the course"
      count: 5
      percent: 6.5
    - phrase: "giving the course a"
      count: 5
      percent: 6.5
    - phrase: "the course a go"
      count: 5
      percent: 6.5
---

# Course Difficulty or Prerequisites

## Response Patterns (from samples)

Common openings:
- "Hey,"
- "Hello,"
- "Hi there,"

Common core lines:
- "Thanks for reaching out!"
- "Best,"
- "Hey,"

Common closings:
- "Best,"
- "We've initiated a refund. It can take 5-10 days for the banks to reconcile and return the money to your account."
- "It may take 5-10 business days for the refunded amount to show up in your account, depending on how quickly it's processed by your financial institution."

## Phrases That Work (4-gram frequency)

- "let me know if" — 10 (13%)
- "me know if you" — 8 (10.4%)
- "know if you have" — 8 (10.4%)
- "if you have any" — 8 (10.4%)
- "thanks for reaching out" — 8 (10.4%)
- "thanks for the feedback" — 5 (6.5%)
- "feedback and giving the" — 5 (6.5%)
- "and giving the course" — 5 (6.5%)
- "giving the course a" — 5 (6.5%)
- "the course a go" — 5 (6.5%)

## Tone Guidance (observed)

- Openings trend toward: "Hey,"
- Closings often include: "Best,"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above