---
name: workshop-technical-setup
description: |
  Customer needs help with technical setup or preparation requirements for workshops.
sample_size: 28
validation:
  required_phrases:
    - "on thu 22 jan"
  forbidden_patterns: []
metrics:
  sample_size: 28
  avg_thread_length: 4.11
  top_phrases:
    - phrase: "on thu 22 jan"
      count: 5
      percent: 17.9
    - phrase: "thu 22 jan 2026"
      count: 5
      percent: 17.9
    - phrase: "22 jan 2026 at"
      count: 5
      percent: 17.9
    - phrase: "let me know if"
      count: 5
      percent: 17.9
    - phrase: "jan 22 2026 at"
      count: 4
      percent: 14.3
    - phrase: "am j sanchez email"
      count: 4
      percent: 14.3
    - phrase: "j sanchez email wrote"
      count: 4
      percent: 14.3
    - phrase: "kent c dodds me"
      count: 4
      percent: 14.3
    - phrase: "c dodds me kentcdodds"
      count: 4
      percent: 14.3
    - phrase: "dodds me kentcdodds com"
      count: 4
      percent: 14.3
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