---
name: invoice-billing-statement
description: |
  Billing statements, invoices, receipts, and payment confirmations for completed transactions.
sample_size: 488
validation:
  required_phrases:
    - "view a fully customized"
  forbidden_patterns: []
metrics:
  sample_size: 488
  avg_thread_length: 3.15
  top_phrases:
    - phrase: "view a fully customized"
      count: 163
      percent: 33.4
    - phrase: "a fully customized invoice"
      count: 163
      percent: 33.4
    - phrase: "fully customized invoice here"
      count: 162
      percent: 33.2
    - phrase: "customized invoice here https"
      count: 162
      percent: 33.2
    - phrase: "can view a fully"
      count: 159
      percent: 32.6
    - phrase: "you can view a"
      count: 151
      percent: 30.9
    - phrase: "logged in you can"
      count: 147
      percent: 30.1
    - phrase: "once you're logged in"
      count: 145
      percent: 29.7
    - phrase: "you're logged in you"
      count: 145
      percent: 29.7
    - phrase: "in you can view"
      count: 145
      percent: 29.7
---

# Invoice and Billing Statement

## Response Patterns (from samples)

Common openings:
- "Hi,"
- "Hello! A fix for the invoice has been sent out. Can you retry https://epicreact.dev/invoice/ and let me know if that works for you?"
- "Hello,"

Common core lines:
- "Once you're logged in, you can view a fully customized invoice here: https://testingjavascript.com/invoice."
- "Once you're logged in, you can view a fully customized invoice here: https://epicreact.dev/invoice."
- "From there, you can add any required information to the \"Prepared for\" section of the invoice."

Common closings:
- "Once you're logged in, you can view a fully customized invoice here: https://testingjavascript.com/invoice."
- "From there, you can add any required information to the \"Prepared for\" section of the invoice."
- "Happy coding!"

## Phrases That Work (4-gram frequency)

- "view a fully customized" — 163 (33.4%)
- "a fully customized invoice" — 163 (33.4%)
- "fully customized invoice here" — 162 (33.2%)
- "customized invoice here https" — 162 (33.2%)
- "can view a fully" — 159 (32.6%)
- "you can view a" — 151 (30.9%)
- "logged in you can" — 147 (30.1%)
- "once you're logged in" — 145 (29.7%)
- "you're logged in you" — 145 (29.7%)
- "in you can view" — 145 (29.7%)

## Tone Guidance (observed)

- Openings trend toward: "Hi,"
- Closings often include: "Once you're logged in, you can view a fully customized invoice here: https://testingjavascript.com/invoice."

## What NOT To Do

- Don't introduce policy details that are not present in the verified response lines above.
- Don't paraphrase or reframe the customer's question in a way that changes meaning.
- Don't add refund/discount promises unless they appear in the extracted responses for this topic.

## Validation

Draft must:
- [ ] Include at least one of the required phrases from the validation block
- [ ] Stay consistent with the observed response patterns above