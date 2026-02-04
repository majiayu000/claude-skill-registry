---
name: email-change
description: Transfer licenses to a new email address. Use when a customer wants to change account email, move a license, or update access after a job change.
metadata:
  trigger_phrases:
      - "transfer licenses"
      - "licenses new"
      - "new email"
  related_skills: ["team-license-purchase", "login-link", "access-locked-out", "corporate-invoice", "invoice-billing-statement"]
  sample_size: "2920"
  validation: |
    required_phrases:
      - "email"
      - "let me know"
    forbidden_patterns:
      - "(?i)why"
      - "(?i)reason"
    max_length: 500
  metrics: "sample_size: 2920\navg_thread_length: 2.93\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 2209\n    percent: 75.7\n  - phrase: \"me know if you\"\n    count: 2095\n    percent: 71.7\n  - phrase: \"know if you have\"\n    count: 1985\n    percent: 68.0\n  - phrase: \"if you have any\"\n    count: 1964\n    percent: 67.3\n  - phrase: \"i ve transferred your\"\n    count: 1765\n    percent: 60.4\n  - phrase: \"ve transferred your license\"\n    count: 1644\n    percent: 56.3\n  - phrase: \"transferred your license to\"\n    count: 1635\n    percent: 56.0\n  - phrase: \"your license to email\"\n    count: 1622\n    percent: 55.5\n  - phrase: \"email let me know\"\n    count: 1560\n    percent: 53.4\n  - phrase: \"to email let me\"\n    count: 1539\n    percent: 52.7"
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
- [ ] NOT explain HOW you transferred it
