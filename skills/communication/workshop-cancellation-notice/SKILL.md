---
name: workshop-cancellation-notice
description: |
  Notification that a scheduled workshop or session has been cancelled.
sample_size: 1
validation:
  required_phrases:
    - "hi oscar the workshop"
  forbidden_patterns: []
metrics:
  sample_size: 1
  avg_thread_length: 19
  top_phrases:
    - phrase: "hi oscar the workshop"
      count: 1
      percent: 100
    - phrase: "oscar the workshop recording"
      count: 1
      percent: 100
    - phrase: "the workshop recording should"
      count: 1
      percent: 100
    - phrase: "workshop recording should be"
      count: 1
      percent: 100
    - phrase: "recording should be available"
      count: 1
      percent: 100
    - phrase: "should be available next"
      count: 1
      percent: 100
    - phrase: "be available next week"
      count: 1
      percent: 100
    - phrase: "available next week we"
      count: 1
      percent: 100
    - phrase: "next week we will"
      count: 1
      percent: 100
    - phrase: "week we will email"
      count: 1
      percent: 100
---

# Workshop Cancellation Notice

## Response Patterns (from samples)

Common openings:
- "Hi Oscar,"

Common core lines:
- "Hi Oscar,"
- "The workshop recording should be available next week, we will email you ASAP."
- "Thanks for your support,"

Common closings:
- "Taylor"

## Phrases That Work (4-gram frequency)

- "hi oscar the workshop" — 1 (100%)
- "oscar the workshop recording" — 1 (100%)
- "the workshop recording should" — 1 (100%)
- "workshop recording should be" — 1 (100%)
- "recording should be available" — 1 (100%)
- "should be available next" — 1 (100%)
- "be available next week" — 1 (100%)
- "available next week we" — 1 (100%)
- "next week we will" — 1 (100%)
- "week we will email" — 1 (100%)

## Tone Guidance (observed)

- Openings trend toward: "Hi Oscar,"
- Closings often include: "Taylor"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above