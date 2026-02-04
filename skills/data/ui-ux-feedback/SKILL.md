---
name: ui-ux-feedback
description: Capture UI and UX feedback plus feature requests. Use when a customer shares design feedback or asks for product changes.
metadata:
  trigger_phrases:
      - "capture feedback"
      - "feedback plus"
      - "plus feature"
  related_skills: ["website-bug-report", "api-documentation-question", "partnership-collaboration-inquiry", "discount-code-request", "refund-request"]
  sample_size: "216"
  validation: |
    required_phrases:
      - "thanks for the feedback"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 216\navg_thread_length: 2.45\ntop_phrases:\n  - phrase: \"thanks for the feedback\"\n    count: 29\n    percent: 13.4\n  - phrase: \"thanks for reaching out\"\n    count: 16\n    percent: 7.4\n  - phrase: \"we will definitely consider\"\n    count: 15\n    percent: 6.9\n  - phrase: \"for the feedback we\"\n    count: 12\n    percent: 5.6\n  - phrase: \"the feedback we will\"\n    count: 12\n    percent: 5.6\n  - phrase: \"feedback we will definitely\"\n    count: 11\n    percent: 5.1\n  - phrase: \"will definitely consider that\"\n    count: 11\n    percent: 5.1\n  - phrase: \"let me know if\"\n    count: 9\n    percent: 4.2\n  - phrase: \"www totaltypescript com profile\"\n    count: 8\n    percent: 3.7\n  - phrase: \"thanks for the heads\"\n    count: 7\n    percent: 3.2"
---
# UI/UX Feedback or Feature Request

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hello,"
- "Hey,"

Common core lines:
- "Best,"
- "Hi,"
- "Hello,"

Common closings:
- "Best,"
- "Thanks for the feedback, we will definitely consider that."
- "Thanks for reaching out, but we politely decline."

## Phrases That Work (4-gram frequency)

- "thanks for the feedback" — 29 (13.4%)
- "thanks for reaching out" — 16 (7.4%)
- "we will definitely consider" — 15 (6.9%)
- "for the feedback we" — 12 (5.6%)
- "the feedback we will" — 12 (5.6%)
- "feedback we will definitely" — 11 (5.1%)
- "will definitely consider that" — 11 (5.1%)
- "let me know if" — 9 (4.2%)
- "www totaltypescript com profile" — 8 (3.7%)
- "thanks for the heads" — 7 (3.2%)

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