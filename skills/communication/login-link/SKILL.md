---
name: login-link
description: |
  Login link delivery issues. Triggers when customer can't access course,
  didn't receive login email, "magic link", "can't log in", or access problems.
sample_size: 999
validation:
  required_phrases:
    - "email"
    - "spam"
  forbidden_patterns:
    - "(?i)why"
metrics:
  sample_size: 999
  avg_thread_length: 3.59
  top_phrases:
    - phrase: "let me know if"
      count: 295
      percent: 29.5
    - phrase: "me know if you"
      count: 253
      percent: 25.3
    - phrase: "you ll need to"
      count: 244
      percent: 24.4
    - phrase: "if you have any"
      count: 238
      percent: 23.8
    - phrase: "to purchase the course"
      count: 178
      percent: 17.8
    - phrase: "ll need to enter"
      count: 172
      percent: 17.2
    - phrase: "enter the email address"
      count: 169
      percent: 16.9
    - phrase: "need to enter the"
      count: 168
      percent: 16.8
    - phrase: "to enter the email"
      count: 168
      percent: 16.8
    - phrase: "at the top of"
      count: 167
      percent: 16.7
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
