---
id: zendesk-support-tickets
name: Zendesk Support Tickets
description: Search tickets, draft replies, help center search
role: support
requiredTools:
  - type: mcpService
    serviceType: zendesk
---

## Zendesk Support Tickets

When handling support tickets in Zendesk:

- Search tickets using Zendesk query syntax (e.g. status:open, type:ticket, requester:email).
- Use get ticket details for full comment history before drafting a reply.
- When drafting a comment, use the draft comment tool; keep tone polite and structured.
- Search help center when the user asks for articles or self-service content.
- Summarize ticket status, requester, and key comments before suggesting or drafting replies.

## Step-by-step instructions

1. For “find tickets”: use Zendesk search with query syntax (e.g. status:open, requester:email@example.com).
2. For a specific ticket: get ticket details to read full thread and internal notes.
3. Summarize status, requester, and key comments before drafting; then use the draft comment tool with a polite, structured reply.
4. For “article” or self-service: search help center and cite articles; optionally use content in the draft.
5. Do not send or submit the reply unless the user explicitly asks to send; otherwise return the draft.

## Examples of inputs and outputs

- **Input**: “What open tickets does john@example.com have?”  
  **Output**: List of ticket IDs and subjects (and status) from search; optionally one-line summary per ticket.

- **Input**: “Draft a reply to ticket 12345.”  
  **Output**: Short summary of the ticket and a draft comment (acknowledge, answer, close); from get ticket + draft comment tool.

## Common edge cases

- **No tickets found**: Report “No tickets matching [query]” and suggest widening filters or checking requester/subdomain.
- **Ticket not found**: Say “Ticket [id] not found” and suggest checking ID or permissions.
- **User wants to send**: Only send/submit when the user explicitly confirms; otherwise provide draft only.
- **API/oauth error**: Report Zendesk error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **Search tickets**: Use for “open tickets”, “tickets for X”, or list views; use Zendesk query syntax (status, type, requester).
- **Get ticket**: Use before drafting a reply to get full thread and notes.
- **Draft comment**: Use to create the reply text; keep tone polite and structured; do not send unless user asks.
- **Search help center**: Use when the user asks for articles or self-service content to include in the reply.
