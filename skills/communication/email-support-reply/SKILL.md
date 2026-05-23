---
id: email-support-reply
name: Email Support Reply
description: Polite, structured support responses
role: support
requiredTools:
  - type: builtin
    tool: send_email
---

## Email Support Reply

When replying to support emails:

- Use a polite, empathetic tone and a clear subject (e.g. Re: [original subject]).
- Structure the reply: acknowledge the issue, answer or next steps, closing.
- Do not include sensitive data (passwords, tokens, PII) in the email body.
- If the issue requires escalation or more time, say so and set expectations.
- Confirm the recipient address and that the user requested an email reply before sending.

## Step-by-step instructions

1. Understand the customer’s issue from the user’s context or the quoted email.
2. Draft a reply: brief acknowledgment, direct answer or next steps, and a short closing.
3. Use subject “Re: [original subject]” when replying to a thread.
4. Remove or redact any passwords, tokens, or PII from the draft.
5. Confirm recipient and that the user wants to send; then call **send_email** with the final body.

## Examples of inputs and outputs

- **Input**: “Reply to this support email: [paste]. Say we’ve fixed the login bug and they can retry.”  
  **Output**: Draft with acknowledgment, “We’ve fixed the issue… you can retry logging in,” and sign-off; then send after user confirms.

- **Input**: “Customer says the API is slow. Draft a reply.”  
  **Output**: Empathetic acknowledgment, ask for endpoint/timeframe or suggest checking status page, offer to escalate; no send unless user asks.

## Common edge cases

- **No recipient given**: Ask for the reply-to address before sending.
- **User pastes a password**: Do not include it in the reply; say “I’ve removed sensitive data from the draft.”
- **Escalation needed**: State in the reply that the issue is being escalated and give a timeframe or next step; do not promise resolution you can’t guarantee.
- **Vague “reply to this”**: Summarize the customer’s issue in your draft and ask the user to confirm before sending.

## Tool usage for specific purposes

- **send_email**: Use to send the support reply only after the user has confirmed. Use it with a clear subject (Re: …), structured body (acknowledge → answer → close), and no secrets or PII in the body.
