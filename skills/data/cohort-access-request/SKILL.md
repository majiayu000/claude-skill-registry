---
name: cohort-access-request
description: Help with access to cohort materials and recordings. Use when a customer cannot find or access cohort content, workshop materials, or live session recordings.
metadata:
  trigger_phrases:
      - "access cohort"
      - "cohort materials"
      - "materials recordings"
  related_skills: ["course-content-locked", "access-locked-out", "technical-issue-course-content", "login-link", "outdated-course-content"]
  sample_size: "121"
  validation: |
    required_phrases:
      - "let me know if"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 121\navg_thread_length: 3.37\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 26\n    percent: 21.5\n  - phrase: \"me know if you\"\n    count: 18\n    percent: 14.9\n  - phrase: \"know if you have\"\n    count: 12\n    percent: 9.9\n  - phrase: \"https click convertkit mail\"\n    count: 11\n    percent: 9.1\n  - phrase: \"click convertkit mail com\"\n    count: 11\n    percent: 9.1\n  - phrase: \"convertkit mail com d0u0eq3vz2a0hoekdowamhzn73444hlh5xp3\"\n    count: 11\n    percent: 9.1\n  - phrase: \"convertkit mail2 com 4zume0z58lbeh5vepv3cxh3d7pv77\"\n    count: 10\n    percent: 8.3\n  - phrase: \"https click convertkit mail2\"\n    count: 9\n    percent: 7.4\n  - phrase: \"click convertkit mail2 com\"\n    count: 9\n    percent: 7.4\n  - phrase: \"have access to the\"\n    count: 8\n    percent: 6.6"
---
# Cohort or Workshop Access

## Response Patterns (from samples)

Common openings:
- "Hey,"
- "Hi,"
- "Hi there,"

Common core lines:
- ">>"
- ">>>"
- ">"

Common closings:
- "Best,"
- "Happy learning!"
- "No recording of the workshop itself will be available, but you'll find that EpicReact.Dev is much better than a simple workshop recording."

## Phrases That Work (4-gram frequency)

- "let me know if" — 26 (21.5%)
- "me know if you" — 18 (14.9%)
- "know if you have" — 12 (9.9%)
- "https click convertkit mail" — 11 (9.1%)
- "click convertkit mail com" — 11 (9.1%)
- "convertkit mail com d0u0eq3vz2a0hoekdowamhzn73444hlh5xp3" — 11 (9.1%)
- "convertkit mail2 com 4zume0z58lbeh5vepv3cxh3d7pv77" — 10 (8.3%)
- "https click convertkit mail2" — 9 (7.4%)
- "click convertkit mail2 com" — 9 (7.4%)
- "have access to the" — 8 (6.6%)

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