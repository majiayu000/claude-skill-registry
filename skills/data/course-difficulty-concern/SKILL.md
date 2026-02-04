---
name: course-difficulty-concern
description: Advise on course difficulty and prerequisites. Use when a customer is unsure about the level or required knowledge.
metadata:
  trigger_phrases:
      - "advise course"
      - "course difficulty"
      - "difficulty prerequisites"
  related_skills: ["learning-path-guidance", "certificate-request", "pricing-inquiry", "continuing-education-credits", "lesson-content-question"]
  sample_size: "77"
  validation: |
    required_phrases:
      - "let me know if"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 77\navg_thread_length: 2.62\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 10\n    percent: 13\n  - phrase: \"me know if you\"\n    count: 8\n    percent: 10.4\n  - phrase: \"know if you have\"\n    count: 8\n    percent: 10.4\n  - phrase: \"if you have any\"\n    count: 8\n    percent: 10.4\n  - phrase: \"thanks for reaching out\"\n    count: 8\n    percent: 10.4\n  - phrase: \"thanks for the feedback\"\n    count: 5\n    percent: 6.5\n  - phrase: \"feedback and giving the\"\n    count: 5\n    percent: 6.5\n  - phrase: \"and giving the course\"\n    count: 5\n    percent: 6.5\n  - phrase: \"giving the course a\"\n    count: 5\n    percent: 6.5\n  - phrase: \"the course a go\"\n    count: 5\n    percent: 6.5"
---
# Course Difficulty or Prerequisites

## Response Patterns (from samples)

Common openings:
- "Hey,"
- "Hello,"
- "Hi there,"

Common core lines:
- "Thanks for reaching out!"
- "Best,"
- "Hey,"

Common closings:
- "Best,"
- "We've initiated a refund. It can take 5-10 days for the banks to reconcile and return the money to your account."
- "It may take 5-10 business days for the refunded amount to show up in your account, depending on how quickly it's processed by your financial institution."

## Phrases That Work (4-gram frequency)

- "let me know if" — 10 (13%)
- "me know if you" — 8 (10.4%)
- "know if you have" — 8 (10.4%)
- "if you have any" — 8 (10.4%)
- "thanks for reaching out" — 8 (10.4%)
- "thanks for the feedback" — 5 (6.5%)
- "feedback and giving the" — 5 (6.5%)
- "and giving the course" — 5 (6.5%)
- "giving the course a" — 5 (6.5%)
- "the course a go" — 5 (6.5%)

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