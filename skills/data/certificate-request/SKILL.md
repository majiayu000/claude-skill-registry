---
name: certificate-request
description: Provide guidance on completion certificates. Use when a customer asks for a course certificate or LinkedIn certificate details.
metadata:
  trigger_phrases:
      - "provide guidance"
      - "guidance completion"
      - "completion certificates"
  related_skills: ["website-bug-report"]
  sample_size: "209"
  validation: |
    required_phrases:
      - "let me know if"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 209\navg_thread_length: 3.12\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 52\n    percent: 24.9\n  - phrase: \"me know if you\"\n    count: 40\n    percent: 19.1\n  - phrase: \"know if you have\"\n    count: 40\n    percent: 19.1\n  - phrase: \"if you have any\"\n    count: 38\n    percent: 18.2\n  - phrase: \"thanks for reaching out\"\n    count: 34\n    percent: 16.3\n  - phrase: \"a certificate of completion\"\n    count: 29\n    percent: 13.9\n  - phrase: \"please let me know\"\n    count: 24\n    percent: 11.5\n  - phrase: \"you have any further\"\n    count: 21\n    percent: 10\n  - phrase: \"have any further questions\"\n    count: 21\n    percent: 10\n  - phrase: \"for your interest in\"\n    count: 16\n    percent: 7.7"
---
# Certificate Request

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hello,"
- "Hey,"

Common core lines:
- "Thanks for reaching out!"
- "Best,"
- "Hi,"

Common closings:
- "Best,"
- "Please let me know if you have any further questions!"
- "Yes - when you complete the course you'll have the option to claim your certificate."

## Phrases That Work (4-gram frequency)

- "let me know if" — 52 (24.9%)
- "me know if you" — 40 (19.1%)
- "know if you have" — 40 (19.1%)
- "if you have any" — 38 (18.2%)
- "thanks for reaching out" — 34 (16.3%)
- "a certificate of completion" — 29 (13.9%)
- "please let me know" — 24 (11.5%)
- "you have any further" — 21 (10%)
- "have any further questions" — 21 (10%)
- "for your interest in" — 16 (7.7%)

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