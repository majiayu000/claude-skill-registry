---
name: refund-request
description: Handle refund requests. Use when a customer asks for a refund, money back, or to cancel a purchase or subscription.
metadata:
  trigger_phrases:
      - "handle refund"
      - "refund requests"
      - "requests customer"
  related_skills: ["duplicate-purchase", "subscription-renewal-issue"]
  sample_size: "1433"
  validation: |
    required_phrases:
      - "refund"
      - "5-10"
    forbidden_patterns:
      - "(?i)why"
      - "(?i)feedback"
    max_length: 500
  metrics: "sample_size: 1433\navg_thread_length: 2.76\ntop_phrases:\n  - phrase: \"it may take 5-10\"\n    count: 840\n    percent: 58.6\n  - phrase: \"may take 5-10 business\"\n    count: 840\n    percent: 58.6\n  - phrase: \"take 5-10 business days\"\n    count: 840\n    percent: 58.6\n  - phrase: \"business days for the\"\n    count: 839\n    percent: 58.5\n  - phrase: \"show up in your\"\n    count: 839\n    percent: 58.5\n  - phrase: \"up in your account\"\n    count: 839\n    percent: 58.5\n  - phrase: \"5-10 business days for\"\n    count: 838\n    percent: 58.5\n  - phrase: \"to show up in\"\n    count: 838\n    percent: 58.5\n  - phrase: \"account depending on how\"\n    count: 837\n    percent: 58.4\n  - phrase: \"by your financial institution\"\n    count: 837\n    percent: 58.4"
---
# Refund Request

You're handling a refund request. We have a 30-day no-questions policy.

## What They Want

Money back. Don't make it complicated.

## Response Pattern

1. Confirm refund is initiated (PAST TENSE - it's done, not "I will")
2. Set expectation: 5-10 days for bank processing
3. Done. Maybe wish them well.

## The 5-10 Days Rule

**ALWAYS mention the 5-10 day timeframe. Every single time.**

This prevents follow-up tickets asking "where's my money?"

## Phrases That Work

- "We've initiated a refund"
- "It can take 5-10 days for the banks to reconcile and return the money"
- "I've gone ahead with the refund"

## Tone

- Matter-of-fact, not apologetic
- Don't ask why they want a refund
- Don't try to save the sale
- Don't guilt trip ("sorry to see you go")
- Brief: 2-3 sentences is perfect

## Variants

| Situation | Adjustment |
|-----------|------------|
| Slow response | Lead with "Sorry about the wait on this one!" |
| Within 30 days | Can mention: "We always refund within 30 days" |
| Upgrading to different product | End with "Enjoy the [new product]!" |

## What NOT To Do

- Don't ask for feedback
- Don't offer alternatives unless they asked
- Don't explain refund policy unless relevant
- Don't say "I'm processing" - say "We've initiated" (it's done)

## Validation

Draft must:
- [ ] Confirm refund is initiated (past tense)
- [ ] Mention 5-10 days processing time
- [ ] NOT guilt trip or ask why
