---
name: gift-purchase-option
description: |
  Customer wants to purchase a course as a gift for someone else.
sample_size: 47
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 47
  avg_thread_length: 3.7
  top_phrases:
    - phrase: "let me know if"
      count: 28
      percent: 59.6
    - phrase: "if you have any"
      count: 22
      percent: 46.8
    - phrase: "me know if you"
      count: 15
      percent: 31.9
    - phrase: "know if you have"
      count: 15
      percent: 31.9
    - phrase: "please let me know"
      count: 14
      percent: 29.8
    - phrase: "email let me know"
      count: 11
      percent: 23.4
    - phrase: "using that email address"
      count: 11
      percent: 23.4
    - phrase: "you have any further"
      count: 10
      percent: 21.3
    - phrase: "have any further questions"
      count: 10
      percent: 21.3
    - phrase: "license to email let"
      count: 10
      percent: 21.3
---

# Gift Purchase Option

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hey Tanguy,"
- "Hey,"

Common core lines:
- "Thanks for reaching out!"
- "Please let me know if you have any further questions!"
- "I've transferred your license to [EMAIL]."

Common closings:
- "Please let me know if you have any further questions!"
- "Please let me know if they have trouble logging in or if you have any further questions!"
- "Please let me know if your friend has trouble logging in or if you have any further questions!"

## Phrases That Work (4-gram frequency)

- "let me know if" — 28 (59.6%)
- "if you have any" — 22 (46.8%)
- "me know if you" — 15 (31.9%)
- "know if you have" — 15 (31.9%)
- "please let me know" — 14 (29.8%)
- "email let me know" — 11 (23.4%)
- "using that email address" — 11 (23.4%)
- "you have any further" — 10 (21.3%)
- "have any further questions" — 10 (21.3%)
- "license to email let" — 10 (21.3%)

## Tone Guidance (observed)

- Openings trend toward: "Hi,"
- Closings often include: "Please let me know if you have any further questions!"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above