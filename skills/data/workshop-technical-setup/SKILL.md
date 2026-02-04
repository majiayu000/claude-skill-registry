---
name: workshop-technical-setup
description: Help with workshop technical setup. Use when a customer asks about required setup, tools, or preparation.
metadata:
  trigger_phrases:
      - "workshop technical"
      - "technical setup"
      - "setup customer"
  related_skills: ["course-difficulty-concern", "api-documentation-question", "technical-issue-course-content", "workshop-attendance-confirmation", "lesson-content-question"]
  sample_size: "28"
  validation: |
    required_phrases:
      - "on thu 22 jan"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 28\navg_thread_length: 4.11\ntop_phrases:\n  - phrase: \"on thu 22 jan\"\n    count: 5\n    percent: 17.9\n  - phrase: \"thu 22 jan 2026\"\n    count: 5\n    percent: 17.9\n  - phrase: \"22 jan 2026 at\"\n    count: 5\n    percent: 17.9\n  - phrase: \"let me know if\"\n    count: 5\n    percent: 17.9\n  - phrase: \"jan 22 2026 at\"\n    count: 4\n    percent: 14.3\n  - phrase: \"am j sanchez email\"\n    count: 4\n    percent: 14.3\n  - phrase: \"j sanchez email wrote\"\n    count: 4\n    percent: 14.3\n  - phrase: \"kent c dodds me\"\n    count: 4\n    percent: 14.3\n  - phrase: \"c dodds me kentcdodds\"\n    count: 4\n    percent: 14.3\n  - phrase: \"dodds me kentcdodds com\"\n    count: 4\n    percent: 14.3"
---
# Workshop Technical Setup and Preparation

## Response Patterns (from samples)

Common openings:
- "Oh no 😢​"
- "Hello,"
- "Thank you!"

Common core lines:
- "wrote:"
- "– Kent"
- "Thanks for reaching out!"

Common closings:
- "If you have coding questions, you can ask them in the community Discord channel we've set up here."
- "Best,"
- "I am really sorry about this. I have changed the permissions so that the form can actually be filled now 😅"

## Phrases That Work (4-gram frequency)

- "on thu 22 jan" — 5 (17.9%)
- "thu 22 jan 2026" — 5 (17.9%)
- "22 jan 2026 at" — 5 (17.9%)
- "let me know if" — 5 (17.9%)
- "jan 22 2026 at" — 4 (14.3%)
- "am j sanchez email" — 4 (14.3%)
- "j sanchez email wrote" — 4 (14.3%)
- "kent c dodds me" — 4 (14.3%)
- "c dodds me kentcdodds" — 4 (14.3%)
- "dodds me kentcdodds com" — 4 (14.3%)

## Tone Guidance (observed)

- Openings trend toward: "Oh no 😢​"
- Closings often include: "If you have coding questions, you can ask them in the community Discord channel we've set up here."

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above
- [ ] NOT introduce policy details that are not present in the verified response lines above.