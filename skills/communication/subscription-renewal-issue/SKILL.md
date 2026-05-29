---
name: subscription-renewal-issue
description: |
  Customer has issues with automatic subscription renewals, unintended charges, or lack of renewal notification.
sample_size: 29
validation:
  required_phrases:
    - "is a one time"
  forbidden_patterns: []
metrics:
  sample_size: 29
  avg_thread_length: 3.21
  top_phrases:
    - phrase: "is a one time"
      count: 8
      percent: 27.6
    - phrase: "it can take 5"
      count: 7
      percent: 24.1
    - phrase: "can take 5 10"
      count: 7
      percent: 24.1
    - phrase: "take 5 10 days"
      count: 7
      percent: 24.1
    - phrase: "5 10 days for"
      count: 7
      percent: 24.1
    - phrase: "10 days for the"
      count: 7
      percent: 24.1
    - phrase: "days for the banks"
      count: 7
      percent: 24.1
    - phrase: "for the banks to"
      count: 7
      percent: 24.1
    - phrase: "the banks to reconcile"
      count: 6
      percent: 20.7
    - phrase: "banks to reconcile and"
      count: 6
      percent: 20.7
---

# Subscription Renewal Issue

## Response Patterns (from samples)

Common openings:
- "Hello,"
- "Hey,"
- "Hey Lenka,"

Common core lines:
- "Hello,"
- "Best,"
- "Hey,"

Common closings:
- "Best,"
- "We've initiated a refund. It can take 5-10 days for the banks to reconcile and return the money to your account."
- "It may take 5-10 business days for the refunded amount to show up in your account, depending on how quickly it's processed by your financial institution."

## Phrases That Work (4-gram frequency)

- "is a one time" — 8 (27.6%)
- "it can take 5" — 7 (24.1%)
- "can take 5 10" — 7 (24.1%)
- "take 5 10 days" — 7 (24.1%)
- "5 10 days for" — 7 (24.1%)
- "10 days for the" — 7 (24.1%)
- "days for the banks" — 7 (24.1%)
- "for the banks to" — 7 (24.1%)
- "the banks to reconcile" — 6 (20.7%)
- "banks to reconcile and" — 6 (20.7%)

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