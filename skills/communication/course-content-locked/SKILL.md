---
name: course-content-locked
description: |
  Customer purchased course but content is locked, unavailable, or not accessible as expected.
sample_size: 520
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 520
  avg_thread_length: 3.42
  top_phrases:
    - phrase: "let me know if"
      count: 91
      percent: 17.5
    - phrase: "me know if you"
      count: 58
      percent: 11.2
    - phrase: "to access the course"
      count: 52
      percent: 10
    - phrase: "know if you have"
      count: 50
      percent: 9.6
    - phrase: "thanks for the heads"
      count: 50
      percent: 9.6
    - phrase: "for the heads up"
      count: 50
      percent: 9.6
    - phrase: "at the top of"
      count: 50
      percent: 9.6
    - phrase: "if you have any"
      count: 48
      percent: 9.2
    - phrase: "let us know if"
      count: 46
      percent: 8.8
    - phrase: "able to access the"
      count: 45
      percent: 8.7
---

# Course Content Locked or Unavailable

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hello,"
- "Hi there,"

Common core lines:
- "Hi,"
- "Best,"
- "Hello,"

Common closings:
- "Best,"
- "Thanks for the heads up! Everything should be back up and running smoothly now. Let us know if that's not the case."
- "Your original purchase price will be removed from the upgrade to the full unrestricted version if you should choose to upgrade."

## Phrases That Work (4-gram frequency)

- "let me know if" — 91 (17.5%)
- "me know if you" — 58 (11.2%)
- "to access the course" — 52 (10%)
- "know if you have" — 50 (9.6%)
- "thanks for the heads" — 50 (9.6%)
- "for the heads up" — 50 (9.6%)
- "at the top of" — 50 (9.6%)
- "if you have any" — 48 (9.2%)
- "let us know if" — 46 (8.8%)
- "able to access the" — 45 (8.7%)

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