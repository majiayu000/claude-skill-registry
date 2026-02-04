---
name: website-bug-report
description: Handle website bug reports. Use when a customer reports site errors or platform issues.
metadata:
  trigger_phrases:
      - "handle website"
      - "website bug"
      - "bug reports"
  related_skills: ["broken-link-404-error", "technical-issue-course-content", "certificate-request", "ppp-pricing", "login-link", "access-locked-out"]
  sample_size: "286"
  validation: |
    required_phrases:
      - "thanks for the heads"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 286\navg_thread_length: 2.78\ntop_phrases:\n  - phrase: \"thanks for the heads\"\n    count: 69\n    percent: 24.1\n  - phrase: \"for the heads up\"\n    count: 69\n    percent: 24.1\n  - phrase: \"let us know if\"\n    count: 52\n    percent: 18.2\n  - phrase: \"let me know if\"\n    count: 35\n    percent: 12.2\n  - phrase: \"now let us know\"\n    count: 33\n    percent: 11.5\n  - phrase: \"the heads up we'll\"\n    count: 31\n    percent: 10.8\n  - phrase: \"heads up we'll look\"\n    count: 29\n    percent: 10.1\n  - phrase: \"up we'll look into\"\n    count: 29\n    percent: 10.1\n  - phrase: \"everything should be back\"\n    count: 26\n    percent: 9.1\n  - phrase: \"us know if you\"\n    count: 25\n    percent: 8.7"
---
# Website Bug Report

## Response Patterns (from samples)

Common openings:
- "Hello! A fix for the invoice has been sent out. Can you retry https://epicreact.dev/invoice/ and let me know if that works for you?"
- "Hey,"
- "Hello,"

Common core lines:
- "Best,"
- "Thanks for the heads up! We'll look into this ASAP."
- "Happy coding!"

Common closings:
- "Best,"
- "Thanks for the heads up! We'll look into this ASAP."
- "Happy coding!"

## Phrases That Work (4-gram frequency)

- "thanks for the heads" — 69 (24.1%)
- "for the heads up" — 69 (24.1%)
- "let us know if" — 52 (18.2%)
- "let me know if" — 35 (12.2%)
- "now let us know" — 33 (11.5%)
- "the heads up we'll" — 31 (10.8%)
- "heads up we'll look" — 29 (10.1%)
- "up we'll look into" — 29 (10.1%)
- "everything should be back" — 26 (9.1%)
- "us know if you" — 25 (8.7%)

## Tone Guidance (observed)

- Openings trend toward: "Hello! A fix for the invoice has been sent out. Can you retry https://epicreact.dev/invoice/ and let me know if that works for you?"
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