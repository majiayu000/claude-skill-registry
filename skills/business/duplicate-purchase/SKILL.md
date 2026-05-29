---
name: duplicate-purchase
description: |
  Customer accidentally purchased the same course twice or purchased a duplicate license.
sample_size: 234
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 234
  avg_thread_length: 4.22
  top_phrases:
    - phrase: "let me know if"
      count: 78
      percent: 33.3
    - phrase: "me know if you"
      count: 56
      percent: 23.9
    - phrase: "5 10 business days"
      count: 53
      percent: 22.6
    - phrase: "if you have any"
      count: 51
      percent: 21.8
    - phrase: "take 5 10 business"
      count: 51
      percent: 21.8
    - phrase: "it may take 5"
      count: 49
      percent: 20.9
    - phrase: "may take 5 10"
      count: 49
      percent: 20.9
    - phrase: "10 business days for"
      count: 49
      percent: 20.9
    - phrase: "business days for the"
      count: 49
      percent: 20.9
    - phrase: "days for the refunded"
      count: 49
      percent: 20.9
---

# Duplicate Purchase

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hello,"
- "Hey,"

Common core lines:
- "It may take 5-10 business days for the refunded amount to show up in your account, depending on how quickly it's processed by your financial institution."
- "[EMAIL]"
- "Best,"

Common closings:
- "It may take 5-10 business days for the refunded amount to show up in your account, depending on how quickly it's processed by your financial institution."
- "Best,"
- "Let me know if you have any issues requesting login links using that email address."

## Phrases That Work (4-gram frequency)

- "let me know if" — 78 (33.3%)
- "me know if you" — 56 (23.9%)
- "5 10 business days" — 53 (22.6%)
- "if you have any" — 51 (21.8%)
- "take 5 10 business" — 51 (21.8%)
- "it may take 5" — 49 (20.9%)
- "may take 5 10" — 49 (20.9%)
- "10 business days for" — 49 (20.9%)
- "business days for the" — 49 (20.9%)
- "days for the refunded" — 49 (20.9%)

## Tone Guidance (observed)

- Openings trend toward: "Hi,"
- Closings often include: "It may take 5-10 business days for the refunded amount to show up in your account, depending on how quickly it's processed by your financial institution."

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above