---
name: cohort-schedule-inquiry
description: |
  Customer asks about cohort schedules, timing, or when next cohort starts.
sample_size: 83
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 83
  avg_thread_length: 3.01
  top_phrases:
    - phrase: "let me know if"
      count: 12
      percent: 14.5
    - phrase: "https www epicai pro"
      count: 11
      percent: 13.3
    - phrase: "me know if you"
      count: 11
      percent: 13.3
    - phrase: "https click convertkit mail"
      count: 10
      percent: 12
    - phrase: "click convertkit mail com"
      count: 10
      percent: 12
    - phrase: "know if you have"
      count: 9
      percent: 10.8
    - phrase: "convertkit mail com v8u07n3lmosrhvpq9nebghv2edlllf9h03x2"
      count: 7
      percent: 8.4
    - phrase: "convertkit mail com 68ulor4726a8h5738pnhohpl5rkkkh9hdqrv"
      count: 7
      percent: 8.4
    - phrase: "brandon mcconnell email wrote"
      count: 7
      percent: 8.4
    - phrase: "jun 16 2025 at"
      count: 7
      percent: 8.4
---

# Cohort Schedule and Timing Inquiry

## Response Patterns (from samples)

Common openings:
- "Hey,"
- "Hello,"
- "Hi there,"

Common core lines:
- ">>"
- ">>>"
- ">"

Common closings:
- "Best,"
- ">>"
- "Let me know if you have any additional questions!"

## Phrases That Work (4-gram frequency)

- "let me know if" — 12 (14.5%)
- "https www epicai pro" — 11 (13.3%)
- "me know if you" — 11 (13.3%)
- "https click convertkit mail" — 10 (12%)
- "click convertkit mail com" — 10 (12%)
- "know if you have" — 9 (10.8%)
- "convertkit mail com v8u07n3lmosrhvpq9nebghv2edlllf9h03x2" — 7 (8.4%)
- "convertkit mail com 68ulor4726a8h5738pnhohpl5rkkkh9hdqrv" — 7 (8.4%)
- "brandon mcconnell email wrote" — 7 (8.4%)
- "jun 16 2025 at" — 7 (8.4%)

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