---
name: login-link
description: Provide login link help. Use when a customer cannot access courses and requests a login link or access email.
metadata:
  trigger_phrases:
      - "provide login"
      - "login link"
      - "link customer"
  related_skills: ["email-change", "website-bug-report", "invoice-billing-statement"]
  sample_size: "999"
  validation: |
    required_phrases:
      - "email"
      - "spam"
    forbidden_patterns:
      - "(?i)why"
    max_length: 500
  metrics: "sample_size: 999\navg_thread_length: 3.59\ntop_phrases:\n  - phrase: \"let me know if\"\n    count: 295\n    percent: 29.5\n  - phrase: \"me know if you\"\n    count: 253\n    percent: 25.3\n  - phrase: \"you ll need to\"\n    count: 244\n    percent: 24.4\n  - phrase: \"if you have any\"\n    count: 238\n    percent: 23.8\n  - phrase: \"to purchase the course\"\n    count: 178\n    percent: 17.8\n  - phrase: \"ll need to enter\"\n    count: 172\n    percent: 17.2\n  - phrase: \"enter the email address\"\n    count: 169\n    percent: 16.9\n  - phrase: \"need to enter the\"\n    count: 168\n    percent: 16.8\n  - phrase: \"to enter the email\"\n    count: 168\n    percent: 16.8\n  - phrase: \"at the top of\"\n    count: 167\n    percent: 16.7"
---
# Login Link Issues

Customer bought a course but can't get the magic link to access it.

## Diagnosis Steps

1. What email are they expecting the link at?
2. Is that the email their license is under?
3. Did the link actually send (check on your end)?

## Common Causes

- License is under different email than they're checking
- Link went to spam/junk folder
- Email provider blocking our sends
- Typo in email at purchase

## Response Patterns

### If you manually resent
Confirm you did it, which email, suggest spam folder check.

### If license is under different email
Tell them which email has the license, ask them to try that one.

### If link shows delivered on your end
Confirm delivery status, suggest spam check, offer to try again.

## Sub-categories

- Manual resend request
- License under the wrong email
- Spam/junk folder filtering
- Delivery confirmed on our side

## Phrases That Work

- "I just manually requested a login link for [email]"
- "It was processed and delivered successfully on our side"
- "Please check your spam folder"
- "I'm seeing your license under [email]"
- "Could you try requesting a login link using that email address?"

## Tone

- Acknowledge frustration without dwelling
- Be specific about what you did
- Always suggest spam folder (it's usually spam)
- Quick resolution focus

## What NOT To Do

- Don't blame their email provider
- Don't get into technical explanations of email delivery
- Don't make it sound like the problem is on their end (even if it is)

## Validation

Draft must:
- [ ] State what action was taken
- [ ] Reference the specific email address
- [ ] Suggest checking spam/junk folder
- [ ] NOT blame their email provider
