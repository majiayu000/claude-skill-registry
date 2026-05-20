---
name: compose
description: This skill should be used when the user asks to "compose email", "write email", "send email to", "new email", or wants to draft and send a new message. Composes emails with a two-phase safety gate that never auto-sends.
triggers:
  - compose email
  - write email
  - send email to
  - new email
---

# /email:compose - Compose New Email

Write and send a new email (not a reply) with safety gates.

## Usage

```
/email:compose                           # Interactive compose
/email:compose to@example.com "Subject"  # Quick compose with recipient and subject
```

## When Invoked

1. Ask user for recipient, subject, and body (if not provided)
2. Call `compose_email` without `confirm` to generate a preview
3. Show the full preview to the user for review
4. Ask for feedback — user can edit recipients, subject, body, or approve
5. Only call `compose_email` with `confirm=true` after explicit user approval

## Safety Rules

- NEVER send without explicit "yes" / "send it" / "looks good" from the user
- Always show the complete preview before sending
- If user says "change" or "edit", revise and show again
- Default to preview mode (confirm=false) on first pass

## Output Format

```
New Email Preview
To: alice@example.com
Subject: Meeting Request

---
Hi Alice,

I'd like to schedule a meeting to discuss the Q2 roadmap.
Would Thursday at 2pm work for you?

Best regards
---

> "Send" to send this email
> "Add CC: bob@example.com" to add recipients
> "Change subject to..." to modify
> "Cancel" to discard
```
