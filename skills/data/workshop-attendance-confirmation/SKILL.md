---
name: workshop-attendance-confirmation
description: Send workshop attendance confirmations. Use when a customer needs confirmation, calendar invites, or attendance details.
metadata:
  trigger_phrases:
      - "send workshop"
      - "workshop attendance"
      - "attendance confirmations"
  related_skills: ["workshop-cancellation-notice", "invoice-billing-statement", "cohort-schedule-inquiry", "certificate-request", "workshop-technical-setup"]
  sample_size: "29"
  validation: |
    required_phrases:
      - "let me know if"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 29\navg_thread_length: 4\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 7\n    percent: 24.1\n  - phrase: \"me know if you\"\n    count: 5\n    percent: 17.2\n  - phrase: \"you need to know\"\n    count: 4\n    percent: 13.8\n  - phrase: \"if you have any\"\n    count: 4\n    percent: 13.8\n  - phrase: \"https egghead zoom us\"\n    count: 4\n    percent: 13.8\n  - phrase: \"egghead zoom us j\"\n    count: 4\n    percent: 13.8\n  - phrase: \"did you end up\"\n    count: 2\n    percent: 6.9\n  - phrase: \"you end up finding\"\n    count: 2\n    percent: 6.9\n  - phrase: \"end up finding the\"\n    count: 2\n    percent: 6.9\n  - phrase: \"up finding the invite\"\n    count: 2\n    percent: 6.9"
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
- "unsubscribe12333 Sowden Rd, Ste. B, PMB #97429 Houston, TX [PHONE]"
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
- [ ] NOT introduce policy details that are not present in the verified response lines above.