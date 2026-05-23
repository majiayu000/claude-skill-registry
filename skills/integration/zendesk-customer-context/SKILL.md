---
id: zendesk-customer-context
name: Zendesk Customer Context
description: Ticket history, requester context
role: support
requiredTools:
  - type: mcpService
    serviceType: zendesk
---

## Zendesk Customer Context

When gathering customer context from Zendesk:

- Search tickets by requester (email or id) to see prior conversations.
- Use get ticket details to read full thread and internal notes.
- Summarize ticket history (open/closed, dates, subjects) before answering or escalating.
- When the user asks about a specific ticket, fetch details and summarize key points and status.
- Use help center search when the request is about documentation or known issues.

## Step-by-step instructions

1. For “context for customer X”: search tickets by requester (email or id); get details for the most relevant tickets.
2. Summarize ticket history: open vs closed, dates, subjects, and key resolution or escalation points.
3. For a specific ticket: get ticket details and summarize status, requester, and main comments/notes.
4. When the user asks about docs or known issues: search help center and cite articles in the summary.

## Examples of inputs and outputs

- **Input**: “What’s the ticket history for john@example.com?”  
  **Output**: Short list: ticket IDs, subjects, status, dates; optionally one line per ticket (e.g. “resolved”, “escalated”).

- **Input**: “Summarize ticket 12345.”  
  **Output**: Status, requester, subject, and key points from the thread and internal notes; from get ticket.

## Common edge cases

- **No tickets for requester**: Say “No tickets found for [email/id]” and suggest checking spelling or subdomain.
- **Ticket not found**: Say “Ticket [id] not found” and suggest checking ID or permissions.
- **Many tickets**: Summarize the most recent or relevant (e.g. open first, then recent closed); do not dump full content.
- **API/oauth error**: Report Zendesk error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **Search tickets (by requester)**: Use to find all tickets for a customer (email or id) for history and context.
- **Get ticket**: Use to read full thread and internal notes for one ticket before summarizing or escalating.
- **Search help center**: Use when the question is about documentation or known issues to cite in the summary.
