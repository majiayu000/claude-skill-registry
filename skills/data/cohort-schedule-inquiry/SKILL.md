---
name: cohort-schedule-inquiry
description: Share cohort schedule information. Use when a customer asks about dates, timing, or when the next cohort starts.
metadata:
  trigger_phrases:
      - "share cohort"
      - "cohort schedule"
      - "schedule information"
  related_skills: ["workshop-attendance-confirmation", "installment-payment-option", "cohort-access-request", "partnership-collaboration-inquiry", "pricing-inquiry"]
  sample_size: "83"
  validation: |
    required_phrases:
      - "let me know if"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 83\navg_thread_length: 3.01\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 12\n    percent: 14.5\n  - phrase: \"https www epicai pro\"\n    count: 11\n    percent: 13.3\n  - phrase: \"me know if you\"\n    count: 11\n    percent: 13.3\n  - phrase: \"https click convertkit mail\"\n    count: 10\n    percent: 12\n  - phrase: \"click convertkit mail com\"\n    count: 10\n    percent: 12\n  - phrase: \"know if you have\"\n    count: 9\n    percent: 10.8\n  - phrase: \"convertkit mail com v8u07n3lmosrhvpq9nebghv2edlllf9h03x2\"\n    count: 7\n    percent: 8.4\n  - phrase: \"convertkit mail com 68ulor4726a8h5738pnhohpl5rkkkh9hdqrv\"\n    count: 7\n    percent: 8.4\n  - phrase: \"brandon mcconnell email wrote\"\n    count: 7\n    percent: 8.4\n  - phrase: \"jun 16 2025 at\"\n    count: 7\n    percent: 8.4"
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
- [ ] NOT introduce policy details that are not present in the verified response lines above.