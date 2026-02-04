---
name: media-press-outreach
description: Handle media and press outreach. Use when journalists or podcast producers request interviews, features, or press information.
metadata:
  trigger_phrases:
      - "handle media"
      - "media press"
      - "press outreach"
  related_skills: ["partnership-collaboration-inquiry", "event-sponsorship-request", "api-documentation-question"]
  sample_size: "39"
  validation: |
    required_phrases:
      - "you ll have to"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 39\navg_thread_length: 2.97\ntop_phrases:\n  - phrase: \"you ll have to\"\n    count: 18\n    percent: 46.2\n  - phrase: \"we support any questions\"\n    count: 15\n    percent: 38.5\n  - phrase: \"support any questions related\"\n    count: 15\n    percent: 38.5\n  - phrase: \"any questions related to\"\n    count: 15\n    percent: 38.5\n  - phrase: \"for this kind of\"\n    count: 12\n    percent: 30.8\n  - phrase: \"this kind of collaboration\"\n    count: 12\n    percent: 30.8\n  - phrase: \"ll have to reach\"\n    count: 11\n    percent: 28.2\n  - phrase: \"have to reach out\"\n    count: 11\n    percent: 28.2\n  - phrase: \"questions related to the\"\n    count: 8\n    percent: 20.5\n  - phrase: \"related to the course\"\n    count: 8\n    percent: 20.5"
---
# Media and Press Outreach

## Response Patterns (from samples)

Common openings:
- "Hello,"
- "Hey Naomi,"
- "Hey Parker,"

Common core lines:
- ">"
- ">>>>"
- "Best,"

Common closings:
- "Best,"
- "We support any questions related to course and functionality, you’ll have to contact Matt directly for this kind of collaboration. We don’t have Matt’s email, you’ll have to reach out on his personal website or Twitter."
- "We support any questions related to course and functionality, you’ll have to contact Kent directly for this kind of collaboration. We don’t have Kent’s email, you’ll have to reach out on his personal website or Twitter."

## Phrases That Work (4-gram frequency)

- "you ll have to" — 18 (46.2%)
- "we support any questions" — 15 (38.5%)
- "support any questions related" — 15 (38.5%)
- "any questions related to" — 15 (38.5%)
- "for this kind of" — 12 (30.8%)
- "this kind of collaboration" — 12 (30.8%)
- "ll have to reach" — 11 (28.2%)
- "have to reach out" — 11 (28.2%)
- "questions related to the" — 8 (20.5%)
- "related to the course" — 8 (20.5%)

## Tone Guidance (observed)

- Openings trend toward: "Hello,"
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