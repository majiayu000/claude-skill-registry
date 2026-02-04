---
name: broken-link-404-error
description: Address broken links and missing resources. Use when a customer reports a 404 or a link to course or website content is not working.
metadata:
  trigger_phrases:
      - "address broken"
      - "broken links"
      - "links missing"
  related_skills: ["website-bug-report", "technical-issue-course-content"]
  sample_size: "236"
  validation: |
    required_phrases:
      - "for the heads up"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 236\navg_thread_length: 2.96\ntop_phrases:\n  - phrase: \"for the heads up\"\n    count: 61\n    percent: 25.8\n  - phrase: \"thanks for the heads\"\n    count: 58\n    percent: 24.6\n  - phrase: \"let me know if\"\n    count: 44\n    percent: 18.6\n  - phrase: \"the heads up we'll\"\n    count: 17\n    percent: 7.2\n  - phrase: \"me know if you\"\n    count: 15\n    percent: 6.4\n  - phrase: \"let us know if\"\n    count: 15\n    percent: 6.4\n  - phrase: \"heads up we'll look\"\n    count: 14\n    percent: 5.9\n  - phrase: \"up we'll look into\"\n    count: 14\n    percent: 5.9\n  - phrase: \"know if you have\"\n    count: 13\n    percent: 5.5\n  - phrase: \"should be able to\"\n    count: 13\n    percent: 5.5"
---
# Broken Link or 404 Error

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hey,"
- "Hello! A fix for the invoice has been sent out. Can you retry https://epicreact.dev/invoice/ and let me know if that works for you?"

Common core lines:
- "Best,"
- ">>"
- "Hi,"

Common closings:
- "Best,"
- "Thanks for the heads up! We'll look into this ASAP."
- "Thanks for the heads up! Everything should be back up and running smoothly now. Let us know if that's not the case."

## Phrases That Work (4-gram frequency)

- "for the heads up" — 61 (25.8%)
- "thanks for the heads" — 58 (24.6%)
- "let me know if" — 44 (18.6%)
- "the heads up we'll" — 17 (7.2%)
- "me know if you" — 15 (6.4%)
- "let us know if" — 15 (6.4%)
- "heads up we'll look" — 14 (5.9%)
- "up we'll look into" — 14 (5.9%)
- "know if you have" — 13 (5.5%)
- "should be able to" — 13 (5.5%)

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