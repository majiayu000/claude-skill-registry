---
name: learning-path-guidance
description: Recommend learning paths. Use when a customer asks which courses to take and in what order.
metadata:
  trigger_phrases:
      - "recommend learning"
      - "learning paths"
      - "paths customer"
  related_skills: ["course-difficulty-concern", "pricing-inquiry", "gift-purchase-option", "certificate-request", "lesson-content-question"]
  sample_size: "74"
  validation: |
    required_phrases:
      - "https www totaltypescript com"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 74\navg_thread_length: 2.45\ntop_phrases:\n  - phrase: \"https www totaltypescript com\"\n    count: 16\n    percent: 21.6\n  - phrase: \"totaltypescript com typescript learning\"\n    count: 11\n    percent: 14.9\n  - phrase: \"com typescript learning path\"\n    count: 11\n    percent: 14.9\n  - phrase: \"www totaltypescript com typescript\"\n    count: 10\n    percent: 13.5\n  - phrase: \"let me know if\"\n    count: 10\n    percent: 13.5\n  - phrase: \"me know if you\"\n    count: 9\n    percent: 12.2\n  - phrase: \"know if you have\"\n    count: 6\n    percent: 8.1\n  - phrase: \"if you have anymore\"\n    count: 6\n    percent: 8.1\n  - phrase: \"you have anymore questions\"\n    count: 5\n    percent: 6.8\n  - phrase: \"have anymore questions best\"\n    count: 5\n    percent: 6.8"
---
# Learning Path and Course Sequencing

## Response Patterns (from samples)

Common openings:
- "Hello,"
- "Hey,"
- "Hi there,"

Common core lines:
- ">>"
- ">"
- "Best,"

Common closings:
- "Best,"
- "P.S. I'm in the process of improving the onboarding experience with the workshop app. Part of that is a new tutorial that uses the app to teach you how to use it! Check it out here: epicweb.dev/tips/setup-the-epic-workshop-app-tutorial-xrh8i"
- "Happy learning!"

## Phrases That Work (4-gram frequency)

- "https www totaltypescript com" — 16 (21.6%)
- "totaltypescript com typescript learning" — 11 (14.9%)
- "com typescript learning path" — 11 (14.9%)
- "www totaltypescript com typescript" — 10 (13.5%)
- "let me know if" — 10 (13.5%)
- "me know if you" — 9 (12.2%)
- "know if you have" — 6 (8.1%)
- "if you have anymore" — 6 (8.1%)
- "you have anymore questions" — 5 (6.8%)
- "have anymore questions best" — 5 (6.8%)

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