---
name: invoice-billing-statement
description: Provide receipts and billing statements. Use when a customer needs an invoice, receipt, or payment confirmation for a completed purchase.
metadata:
  trigger_phrases:
      - "provide receipts"
      - "receipts billing"
      - "billing statements"
  related_skills: ["corporate-invoice", "email-change", "payment-method-issue", "login-link"]
  sample_size: "488"
  validation: |
    required_phrases:
      - "view a fully customized"
    forbidden_patterns: []
    max_length: 500
  metrics: "sample_size: 488\navg_thread_length: 3.15\ntop_phrases:\n  - phrase: \"view a fully customized\"\n    count: 163\n    percent: 33.4\n  - phrase: \"a fully customized invoice\"\n    count: 163\n    percent: 33.4\n  - phrase: \"fully customized invoice here\"\n    count: 162\n    percent: 33.2\n  - phrase: \"customized invoice here https\"\n    count: 162\n    percent: 33.2\n  - phrase: \"can view a fully\"\n    count: 159\n    percent: 32.6\n  - phrase: \"you can view a\"\n    count: 151\n    percent: 30.9\n  - phrase: \"logged in you can\"\n    count: 147\n    percent: 30.1\n  - phrase: \"once you're logged in\"\n    count: 145\n    percent: 29.7\n  - phrase: \"you're logged in you\"\n    count: 145\n    percent: 29.7\n  - phrase: \"in you can view\"\n    count: 145\n    percent: 29.7"
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
- [ ] NOT introduce policy details that are not present in the verified response lines above.