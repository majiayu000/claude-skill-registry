---
name: partnership-collaboration-inquiry
description: Handle partnership and collaboration inquiries. Use when a third party asks about partnerships, promotions, or collaborations.
metadata:
  trigger_phrases:
      - "handle partnership"
      - "partnership collaboration"
      - "collaboration inquiries"
  related_skills: ["event-sponsorship-request", "media-press-outreach", "discount-code-request", "api-documentation-question", "student-discount-request"]
  sample_size: "485"
  validation: |
    required_phrases:
      - "support any questions related"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 485\navg_thread_length: 3.06\ntop_phrases:\n  - phrase: \"support any questions related\"\n    count: 177\n    percent: 36.5\n  - phrase: \"any questions related to\"\n    count: 177\n    percent: 36.5\n  - phrase: \"we support any questions\"\n    count: 162\n    percent: 33.4\n  - phrase: \"questions related to the\"\n    count: 152\n    percent: 31.3\n  - phrase: \"related to the course\"\n    count: 152\n    percent: 31.3\n  - phrase: \"to the course and\"\n    count: 152\n    percent: 31.3\n  - phrase: \"the course and platform\"\n    count: 151\n    percent: 31.1\n  - phrase: \"course and platform functionality\"\n    count: 151\n    percent: 31.1\n  - phrase: \"https bsky app profile\"\n    count: 151\n    percent: 31.1\n  - phrase: \"and platform functionality but\"\n    count: 150\n    percent: 30.9"
---
# Partnership and Collaboration Inquiry

## Response Patterns (from samples)

Common openings:
- "Hi there,"
- "Hey,"
- "Hello,"

Common core lines:
- "Best,"
- "https://x.com/mattpocockuk"
- "https://bsky.app/profile/mattpocock.com"

Common closings:
- "Best,"
- "Thanks for reaching out, but we politely decline."
- "We support any questions related to course and functionality, you’ll have to contact Matt directly for this kind of collaboration. We don’t have Matt’s email, you’ll have to reach out on his personal website or Twitter."

## Phrases That Work (4-gram frequency)

- "support any questions related" — 177 (36.5%)
- "any questions related to" — 177 (36.5%)
- "we support any questions" — 162 (33.4%)
- "questions related to the" — 152 (31.3%)
- "related to the course" — 152 (31.3%)
- "to the course and" — 152 (31.3%)
- "the course and platform" — 151 (31.1%)
- "course and platform functionality" — 151 (31.1%)
- "https bsky app profile" — 151 (31.1%)
- "and platform functionality but" — 150 (30.9%)

## Tone Guidance (observed)

- Openings trend toward: "Hi there,"
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