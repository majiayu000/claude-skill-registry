---
name: outdated-course-content
description: Handle reports of outdated course content. Use when a customer says material is old or no longer matches current technology.
metadata:
  trigger_phrases:
      - "handle reports"
      - "reports outdated"
      - "outdated course"
  related_skills: ["technical-issue-course-content", "course-content-locked", "course-difficulty-concern", "broken-link-404-error", "pricing-inquiry"]
  sample_size: "105"
  validation: |
    required_phrases:
      - "for the heads up"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 105\navg_thread_length: 2.61\ntop_phrases:\n  - phrase: \"for the heads up\"\n    count: 14\n    percent: 13.3\n  - phrase: \"thanks for the heads\"\n    count: 13\n    percent: 12.4\n  - phrase: \"if you have any\"\n    count: 12\n    percent: 11.4\n  - phrase: \"is up to date\"\n    count: 11\n    percent: 10.5\n  - phrase: \"know if you have\"\n    count: 11\n    percent: 10.5\n  - phrase: \"up to date and\"\n    count: 10\n    percent: 9.5\n  - phrase: \"thanks for reaching out\"\n    count: 9\n    percent: 8.6\n  - phrase: \"the course is up\"\n    count: 8\n    percent: 7.6\n  - phrase: \"course is up to\"\n    count: 8\n    percent: 7.6\n  - phrase: \"let me know if\"\n    count: 8\n    percent: 7.6"
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
- [ ] NOT introduce policy details that are not present in the verified response lines above.