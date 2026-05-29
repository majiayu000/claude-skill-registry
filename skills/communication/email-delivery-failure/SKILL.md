---
name: email-delivery-failure
description: |
  Bounce-back or delivery failure notices for emails sent to customer addresses.
sample_size: 47
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 47
  avg_thread_length: 3.96
  top_phrases:
    - phrase: "let me know if"
      count: 12
      percent: 25.5
    - phrase: "if you have any"
      count: 12
      percent: 25.5
    - phrase: "me know if you"
      count: 10
      percent: 21.3
    - phrase: "you have any trouble"
      count: 7
      percent: 14.9
    - phrase: "using the email login"
      count: 6
      percent: 12.8
    - phrase: "the email login link"
      count: 6
      percent: 12.8
    - phrase: "email login link at"
      count: 6
      percent: 12.8
    - phrase: "login link at the"
      count: 6
      percent: 12.8
    - phrase: "link at the top"
      count: 6
      percent: 12.8
    - phrase: "at the top of"
      count: 6
      percent: 12.8
---

# Email Delivery Failure

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Yes, click \"unsubscribe from ai hero messages\" at the bottom of the email. Sorry for being noisy!"
- "It's still in review! Taking a bit longer than expected."

Common core lines:
- "If you have any trouble accessing the course, please let us know!"
- "Hi,"
- "Everything should be back up and running now - please try to request a new login link and let me know if you still don't receive it."

Common closings:
- "If you have any trouble accessing the course, please let us know!"
- "I apologize for the inconvenience!"
- "Yes, click \"unsubscribe from ai hero messages\" at the bottom of the email. Sorry for being noisy!"

## Phrases That Work (4-gram frequency)

- "let me know if" — 12 (25.5%)
- "if you have any" — 12 (25.5%)
- "me know if you" — 10 (21.3%)
- "you have any trouble" — 7 (14.9%)
- "using the email login" — 6 (12.8%)
- "the email login link" — 6 (12.8%)
- "email login link at" — 6 (12.8%)
- "login link at the" — 6 (12.8%)
- "link at the top" — 6 (12.8%)
- "at the top of" — 6 (12.8%)

## Tone Guidance (observed)

- Openings trend toward: "Hi,"
- Closings often include: "If you have any trouble accessing the course, please let us know!"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above