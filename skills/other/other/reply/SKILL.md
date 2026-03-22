---
name: reply
description: This skill should be used when the user asks to "reply to email", "respond to email", "draft reply", "email reply", or wants to respond to a specific message. Drafts replies with safety confirmation that never auto-sends.
triggers:
  - reply to email
  - respond to email
  - draft reply
  - email reply
---

# /email:reply - Draft Email Reply

Compose a professional reply to an email with safety gates.

## Usage

```
/email:reply <id>                    # Reply to email by ID
/email:reply <id> --tone casual      # Set reply tone
/email:reply <id> --all              # Reply to all recipients
/email:reply <id> "Confirm meeting"  # Include specific instructions
```

## When Invoked

1. Call `read_email` to understand the original message
2. Call `draft_reply` to generate the reply template
3. Show the full draft to the user for review
4. Ask for feedback — user can edit, adjust tone, or approve
5. Only call `send_email` with `confirm=true` after explicit user approval

## Safety Rules

- NEVER send without explicit "yes" / "send it" / "looks good" from the user
- Always show the complete draft before sending
- If user says "change" or "edit", revise the draft and show again
- Default to preview mode (confirm=false) on first pass

## Output Format

```
📝 Draft Reply to: alice@example.com
Subject: Re: Meeting Tomorrow

---
Hi Alice,

Thanks for the reminder. I'll be there at 3:30pm.

Best,
[Your name]
---

→ "Send" to send this reply
→ "Make it more formal" to adjust tone
→ "Add that I'll bring the notes" to modify content
→ "Cancel" to discard
```
