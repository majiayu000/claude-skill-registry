---
name: workshop-cancellation-notice
description: Notify about workshop cancellations. Use when a scheduled workshop or session is canceled or rescheduled.
metadata:
  trigger_phrases:
      - "notify about"
      - "about workshop"
      - "workshop cancellations"
  related_skills: ["workshop-attendance-confirmation", "subscription-renewal-issue", "workshop-technical-setup"]
  sample_size: "1"
  validation: |
    required_phrases:
      - "hi oscar the workshop"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 1\navg_thread_length: 19\ntop_phrases:\n  - phrase: \"hi oscar the workshop\"\n    count: 1\n    percent: 100\n  - phrase: \"oscar the workshop recording\"\n    count: 1\n    percent: 100\n  - phrase: \"the workshop recording should\"\n    count: 1\n    percent: 100\n  - phrase: \"workshop recording should be\"\n    count: 1\n    percent: 100\n  - phrase: \"recording should be available\"\n    count: 1\n    percent: 100\n  - phrase: \"should be available next\"\n    count: 1\n    percent: 100\n  - phrase: \"be available next week\"\n    count: 1\n    percent: 100\n  - phrase: \"available next week we\"\n    count: 1\n    percent: 100\n  - phrase: \"next week we will\"\n    count: 1\n    percent: 100\n  - phrase: \"week we will email\"\n    count: 1\n    percent: 100"
---
# Workshop Cancellation Notice

## Response Patterns (from samples)

Common openings:
- "Hi there,"

Common core lines:
- "Hi there,"
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

- Openings trend toward: "Hi there,"
- Closings often include: "Taylor"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above
- [ ] NOT introduce policy details that are not present in the verified response lines above.