---
id: email-follow-up
name: Email Follow-up
description: Professional follow-ups, templates
role: sales
requiredTools:
  - type: builtin
    tool: send_email
---

## Email Follow-up

When sending follow-up emails:

- Use a clear subject line and professional tone.
- Keep the body concise: purpose, key points, and call to action.
- Match the level of formality to the relationship (e.g. prospect vs. existing customer).
- Do not include sensitive data (passwords, tokens) in the body.
- Confirm recipient address and intent before sending.

## Step-by-step instructions

1. Confirm with the user: recipient address, purpose of the follow-up, and any key points or call to action.
2. Draft a short subject line (e.g. “Following up: [topic]”) and body (greeting, purpose, 1–3 bullets or short paragraph, CTA, sign-off).
3. Do not include passwords, API keys, or other secrets in the body.
4. Call **send_email** with the agreed recipient, subject, and body only after the user has confirmed or clearly requested sending.

## Examples of inputs and outputs

- **Input**: “Send a follow-up to john@example.com about the demo we discussed.”  
  **Output**: Propose subject and 2–3 sentence body; ask user to confirm before sending; then call send_email once confirmed.

- **Input**: “Draft a follow-up after a meeting with Acme.”  
  **Output**: Return the draft only (no send) unless the user explicitly asks to send it.

## Common edge cases

- **Missing recipient**: Ask for the email address before drafting or sending.
- **User says “send” without prior context**: Confirm recipient and purpose before sending.
- **Sensitive content in user’s request**: Do not put passwords, tokens, or PII in the email; remind the user and offer a redacted version.
- **Multiple recipients**: If the tool supports a single recipient, send to one and say you can repeat for others, or ask which one to use.

## Tool usage for specific purposes

- **send_email**: Use only for actually sending the follow-up after the user has confirmed recipient and content. Use it with a clear subject and plain-text or HTML body; never include secrets in the body.
