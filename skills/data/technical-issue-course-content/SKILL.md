---
name: technical-issue-course-content
description: Troubleshoot technical issues with course materials. Use when a customer reports video, code, or content not working.
metadata:
  trigger_phrases:
      - "troubleshoot technical"
      - "technical issues"
      - "issues course"
  related_skills: ["course-content-locked", "website-bug-report", "broken-link-404-error"]
  sample_size: "596"
  validation: |
    required_phrases:
      - "thanks for the heads up"
      - "let me know if"
    forbidden_patterns:
      - "(?i)works on my machine"
      - "(?i)can't reproduce"
      - "(?i)cannot reproduce"
      - "(?i)user error"
      - "(?i)your fault"
      - "(?i)not our problem"
    max_length: 500
  metrics: "sample_size: 596\navg_thread_length: 3.15\ntop_phrases:\n  - phrase: \"for the heads up\"\n    count: 79\n    percent: 13.3\n  - phrase: \"thanks for the heads\"\n    count: 78\n    percent: 13.1\n  - phrase: \"the heads up we'll\"\n    count: 58\n    percent: 9.7\n  - phrase: \"heads up we'll look\"\n    count: 58\n    percent: 9.7\n  - phrase: \"up we'll look into\"\n    count: 58\n    percent: 9.7\n  - phrase: \"let me know if\"\n    count: 49\n    percent: 8.2\n  - phrase: \"we'll look into this\"\n    count: 44\n    percent: 7.4\n  - phrase: \"look into this asap\"\n    count: 41\n    percent: 6.9\n  - phrase: \"thanks for the feedback\"\n    count: 40\n    percent: 6.7\n  - phrase: \"thanks for reaching out\"\n    count: 36\n    percent: 6.0"
---
# Technical Issue with Course Content

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Thanks for the feedback, it's not perfect for sure. We recommend using VS Code or similar locally if the inline editor is aggravating."
- "Hello,"

Common core lines:
- "Hi,"
- "Thanks for the heads up! We'll look into this ASAP."
- "Best,"

Common closings:
- "Best,"
- "Thanks for the heads up! We'll look into this ASAP."
- "Thanks for the feedback, it's not perfect for sure. We recommend using VS Code or similar locally if the inline editor is aggravating."

## Phrases That Work (4-gram frequency)

- "for the heads up" — 79 (13.3%)
- "thanks for the heads" — 78 (13.1%)
- "the heads up we'll" — 58 (9.7%)
- "heads up we'll look" — 58 (9.7%)
- "up we'll look into" — 58 (9.7%)
- "let me know if" — 49 (8.2%)
- "we'll look into this" — 44 (7.4%)
- "look into this asap" — 41 (6.9%)
- "thanks for the feedback" — 40 (6.7%)
- "thanks for reaching out" — 36 (6.0%)

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
