---
name: learning-path-guidance
description: |
  Customer asks for guidance on which courses to take in what order.
sample_size: 74
validation:
  required_phrases:
    - "https www totaltypescript com"
  forbidden_patterns: []
metrics:
  sample_size: 74
  avg_thread_length: 2.45
  top_phrases:
    - phrase: "https www totaltypescript com"
      count: 16
      percent: 21.6
    - phrase: "totaltypescript com typescript learning"
      count: 11
      percent: 14.9
    - phrase: "com typescript learning path"
      count: 11
      percent: 14.9
    - phrase: "www totaltypescript com typescript"
      count: 10
      percent: 13.5
    - phrase: "let me know if"
      count: 10
      percent: 13.5
    - phrase: "me know if you"
      count: 9
      percent: 12.2
    - phrase: "know if you have"
      count: 6
      percent: 8.1
    - phrase: "if you have anymore"
      count: 6
      percent: 8.1
    - phrase: "you have anymore questions"
      count: 5
      percent: 6.8
    - phrase: "have anymore questions best"
      count: 5
      percent: 6.8
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