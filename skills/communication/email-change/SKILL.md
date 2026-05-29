---
name: email-change
description: |
  Transfer license to different email. Triggers when customer wants to 
  change email, move license, update account email, or mentions leaving job.
sample_size: 2920
validation:
  required_phrases:
    - "email"
    - "let me know"
  forbidden_patterns:
    - "(?i)why"
    - "(?i)reason"
metrics:
  sample_size: 2920
  avg_thread_length: 2.93
  top_phrases:
    - phrase: "let me know if"
      count: 2209
      percent: 75.7
    - phrase: "me know if you"
      count: 2095
      percent: 71.7
    - phrase: "know if you have"
      count: 1985
      percent: 68.0
    - phrase: "if you have any"
      count: 1964
      percent: 67.3
    - phrase: "i ve transferred your"
      count: 1765
      percent: 60.4
    - phrase: "ve transferred your license"
      count: 1644
      percent: 56.3
    - phrase: "transferred your license to"
      count: 1635
      percent: 56.0
    - phrase: "your license to email"
      count: 1622
      percent: 55.5
    - phrase: "email let me know"
      count: 1560
      percent: 53.4
    - phrase: "to email let me"
      count: 1539
      percent: 52.7
---

# Email Address Change

You're handling an email change request. This is our most common ticket.

## What They Want

Transfer their course license from one email to another. Usually:
- Leaving a job (work email → personal)
- Typo on original purchase
- Consolidating accounts

## Response Pattern

1. Confirm you've done it (past tense, not "I will")
2. Tell them the new email
3. Offer help if issues

That's it. Don't over-explain the process.

## Phrases That Work

- "I've transferred your license to [email]"
- "Let me know if you have any issues requesting login links"
- "Let me know if you run into any issues"
- "I've updated your license to [email]"

## Before You Can Act

If you can't find their license:
1. ASK which email they purchased with
2. Don't guess
3. Don't apologize excessively
4. Just ask directly

## Tone

- Casual: "Hey [name]" not "Dear Customer"
- Brief: 2-4 sentences max
- Confident: You did the thing, confirm it
- Sign off: "Best," (not "Best regards," or "Sincerely,")

## What NOT To Do

- Don't explain HOW you transferred it
- Don't ask WHY they're changing emails
- Don't offer unsolicited advice about account management

## Variants

| Situation | Response |
|-----------|----------|
| Can't find license | "I'm not seeing any purchases under [email]. What email did you use to purchase?" |
| Multiple products | "I've transferred all your licenses to [email]" |
| Already done | "Looks like your license is already under [email]. Let me know if you're having issues accessing it." |

## Validation

Draft must:
- [ ] Confirm the transfer happened (past tense)
- [ ] Reference the new email address
- [ ] Offer follow-up help
