---
id: intercom-customer-conversations
name: Intercom Customer Conversations
description: Search contacts and conversations, reply to customers
role: support
requiredTools:
  - type: mcpService
    serviceType: intercom
---

## Intercom Customer Conversations

When handling customer conversations in Intercom:

- Use **intercom_search_contacts** (tool name may have a suffix if multiple Intercom servers exist) with shortcut params (email, name, externalId) or a query object to find contacts.
- Use **intercom_get_conversation** or **intercom_search_conversations** (contactId, state, createdAfter, updatedAfter) to get conversation context before replying.
- Use **intercom_reply_conversation** to send replies as an admin; keep tone polite and structured.
- Summarize conversation state (open/closed) and key messages before drafting or sending a reply.
- For search, use shortcut params when possible (email, name, contactId, state); use full query object only when needed.

## Step-by-step instructions

1. For "find contact X": call **intercom_search_contacts** with email or name; use **intercom_get_contact** for full details if needed.
2. For "conversations for customer Y": use **intercom_search_conversations** with contactId (or contactIds); get conversation details with **intercom_get_conversation**.
3. Before replying: read the full thread via **intercom_get_conversation**; summarize status and last message; draft a polite, structured reply.
4. Call **intercom_reply_conversation** with the conversation ID and reply body only after the user has confirmed or explicitly asked to send.
5. Do not include sensitive data (passwords, tokens, PII) in replies.

## Examples of inputs and outputs

- **Input**: "What open conversations does john@example.com have?"  
  **Output**: List of conversation IDs and state from **intercom_search_conversations** (contactId or email search); optionally one-line summary per conversation.

- **Input**: "Draft a reply to conversation 12345 saying we've fixed the issue."  
  **Output**: Short summary of the conversation and a draft reply (acknowledge, answer, close); use **intercom_reply_conversation** only if the user asks to send.

## Common edge cases

- **No contact found**: Say "No contact found for [email/name]" and suggest checking spelling or trying another identifier.
- **No conversations**: Report "No conversations found" for that contact and suggest state or date filters.
- **User wants to send**: Only call **intercom_reply_conversation** when the user explicitly confirms; otherwise return the draft only.
- **Query format**: Use shortcut params (email, name, contactId, state, createdAfter, updatedAfter) for search; avoid invalid fields like contact_id or q.
- **API/OAuth error**: Report the error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **intercom_search_contacts**: Use for "find contact by email/name"; use email, name, or externalId shortcuts.
- **intercom_get_contact**: Use for full contact details after search.
- **intercom_search_conversations**: Use for "conversations for customer" or by state/date; use contactId, state, createdAfter, updatedAfter.
- **intercom_get_conversation**: Use to read full thread before drafting a reply.
- **intercom_reply_conversation**: Use to send the reply only after user confirmation; keep tone polite and structured.
