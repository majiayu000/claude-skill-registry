---
name: password-reset-issue
description: |
  Customer needs help resetting password or recovering locked account.
sample_size: 14
validation:
  required_phrases:
    - "let me know if"
  forbidden_patterns: []
metrics:
  sample_size: 14
  avg_thread_length: 3.14
  top_phrases:
    - phrase: "let me know if"
      count: 7
      percent: 50
    - phrase: "if you have any"
      count: 7
      percent: 50
    - phrase: "me know if you"
      count: 6
      percent: 42.9
    - phrase: "know if you have"
      count: 6
      percent: 42.9
    - phrase: "you used to purchase"
      count: 4
      percent: 28.6
    - phrase: "used to purchase the"
      count: 4
      percent: 28.6
    - phrase: "able to access the"
      count: 3
      percent: 21.4
    - phrase: "at the top of"
      count: 3
      percent: 21.4
    - phrase: "the top of https"
      count: 3
      percent: 21.4
    - phrase: "you'll need to enter"
      count: 3
      percent: 21.4
---

# Password Reset or Recovery

## Response Patterns (from samples)

Common openings:
- "Hey Arzu,"
- "Hi Alex,"
- "I was able to access the admin console this time, but I'd previously"

Common core lines:
- ">"
- "You can access the course using the \"Restore Purchases\" button at the top of https://epicreact.dev. You'll need to enter the email address you used to purchase the course to have a login link sent."
- "Let me know if you have any additional questions!"

Common closings:
- "Let me know if you have any additional questions!"
- "And for security reasons could you provide the last 4 digits of the card that you used to purchase the license?"
- "You can request a magic link anytime here: https://www.totaltypescript.com/login"

## Phrases That Work (4-gram frequency)

- "let me know if" — 7 (50%)
- "if you have any" — 7 (50%)
- "me know if you" — 6 (42.9%)
- "know if you have" — 6 (42.9%)
- "you used to purchase" — 4 (28.6%)
- "used to purchase the" — 4 (28.6%)
- "able to access the" — 3 (21.4%)
- "at the top of" — 3 (21.4%)
- "the top of https" — 3 (21.4%)
- "you'll need to enter" — 3 (21.4%)

## Tone Guidance (observed)

- Openings trend toward: "Hey Arzu,"
- Closings often include: "Let me know if you have any additional questions!"

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above