---
name: workshop-attendance-confirmation
description: |
  Confirmation emails and calendar invitations for workshop or cohort attendance.
sample_size: 29
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 29
  avg_thread_length: 4
  top_phrases:
    - phrase: "let me know if"
      count: 7
      percent: 24.1
    - phrase: "me know if you"
      count: 5
      percent: 17.2
    - phrase: "you need to know"
      count: 4
      percent: 13.8
    - phrase: "if you have any"
      count: 4
      percent: 13.8
    - phrase: "https egghead zoom us"
      count: 4
      percent: 13.8
    - phrase: "egghead zoom us j"
      count: 4
      percent: 13.8
    - phrase: "did you end up"
      count: 2
      percent: 6.9
    - phrase: "you end up finding"
      count: 2
      percent: 6.9
    - phrase: "end up finding the"
      count: 2
      percent: 6.9
    - phrase: "up finding the invite"
      count: 2
      percent: 6.9
---

# Workshop Attendance and Confirmations

## Response Patterns (from samples)

Common openings:
- "Hey,"
- "Hey Loren,"
- "Hey Karen,"

Common core lines:
- ">"
- "Best,"
- "Hey,"

Common closings:
- "Best,"
- "unsubscribe12333 Sowden Rd, Ste. B, PMB #97429 Houston, TX 77080-2059"
- "Let me know If you missed the event. Sorry to hear getting the link to join was not clear."

## Phrases That Work (4-gram frequency)

- "let me know if" — 7 (24.1%)
- "me know if you" — 5 (17.2%)
- "you need to know" — 4 (13.8%)
- "if you have any" — 4 (13.8%)
- "https egghead zoom us" — 4 (13.8%)
- "egghead zoom us j" — 4 (13.8%)
- "did you end up" — 2 (6.9%)
- "you end up finding" — 2 (6.9%)
- "end up finding the" — 2 (6.9%)
- "up finding the invite" — 2 (6.9%)

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