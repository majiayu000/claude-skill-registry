---
name: course-content-locked
description: Restore access to purchased course content. Use when a customer has paid but content is locked, missing, or inaccessible.
metadata:
  trigger_phrases:
      - "restore access"
      - "access purchased"
      - "purchased course"
  related_skills: ["technical-issue-course-content"]
  sample_size: "520"
  validation: |
    required_phrases:
      - "access the course"
      - "login link"
      - "restore purchases"
    forbidden_patterns:
      - "(?i)refund"
      - "(?i)chargeback"
      - "(?i)purchase order"
      - "(?i)wire transfer"
      - "(?i)bank transfer"
      - "(?i)vat number"
      - "(?i)invoice number"
    max_length: 500
  metrics: "sample_size: 520\navg_thread_length: 3.42\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 91\n    percent: 17.5\n  - phrase: \"me know if you\"\n    count: 77\n    percent: 14.8\n  - phrase: \"to access the course\"\n    count: 52\n    percent: 10\n  - phrase: \"know if you have\"\n    count: 50\n    percent: 9.6\n  - phrase: \"thanks for the heads\"\n    count: 50\n    percent: 9.6\n  - phrase: \"for the heads up\"\n    count: 50\n    percent: 9.6\n  - phrase: \"at the top of\"\n    count: 50\n    percent: 9.6\n  - phrase: \"you ll need to\"\n    count: 49\n    percent: 9.4\n  - phrase: \"if you have any\"\n    count: 48\n    percent: 9.2\n  - phrase: \"let us know if\"\n    count: 46\n    percent: 8.8"
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
- "me know if you" — 77 (14.8%)
- "to access the course" — 52 (10%)
- "know if you have" — 50 (9.6%)
- "thanks for the heads" — 50 (9.6%)
- "for the heads up" — 50 (9.6%)
- "at the top of" — 50 (9.6%)
- "you ll need to" — 49 (9.4%)
- "if you have any" — 48 (9.2%)
- "let us know if" — 46 (8.8%)

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
- [ ] NOT introduce policy details that are not present in the verified response lines above.
