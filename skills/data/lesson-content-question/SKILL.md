---
name: lesson-content-question
description: Answer lesson-specific content questions. Use when a customer asks about a lesson, code example, or concept in a course.
metadata:
  trigger_phrases:
      - "answer lesson"
      - "lesson specific"
      - "specific content"
  related_skills: ["pricing-inquiry", "installment-payment-option", "continuing-education-credits", "api-documentation-question", "technical-issue-course-content"]
  sample_size: "414"
  validation: |
    required_phrases:
      - "thanks for reaching out"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 414\navg_thread_length: 2.5\ntop_phrases:\n  - phrase: \"thanks for reaching out\"\n    count: 49\n    percent: 11.8\n  - phrase: \"insights can help others\"\n    count: 47\n    percent: 11.4\n  - phrase: \"can help others too\"\n    count: 46\n    percent: 11.1\n  - phrase: \"your questions and insights\"\n    count: 43\n    percent: 10.4\n  - phrase: \"questions and insights can\"\n    count: 43\n    percent: 10.4\n  - phrase: \"and insights can help\"\n    count: 43\n    percent: 10.4\n  - phrase: \"plus your questions and\"\n    count: 42\n    percent: 10.1\n  - phrase: \"hope this helps best\"\n    count: 39\n    percent: 9.4\n  - phrase: \"help others too i\"\n    count: 38\n    percent: 9.2\n  - phrase: \"others too i hope\"\n    count: 38\n    percent: 9.2"
---
# Lesson Content Question

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hey there,"
- "Hello,"

Common core lines:
- ">>"
- "Best,"
- ">"

Common closings:
- "Best,"
- "Thanks!"
- "If you have coding questions, you can ask them in the community Discord channel we've set up here."

## Phrases That Work (4-gram frequency)

- "thanks for reaching out" — 49 (11.8%)
- "insights can help others" — 47 (11.4%)
- "can help others too" — 46 (11.1%)
- "your questions and insights" — 43 (10.4%)
- "questions and insights can" — 43 (10.4%)
- "and insights can help" — 43 (10.4%)
- "plus your questions and" — 42 (10.1%)
- "hope this helps best" — 39 (9.4%)
- "help others too i" — 38 (9.2%)
- "others too i hope" — 38 (9.2%)

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