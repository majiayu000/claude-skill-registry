---
id: hubspot-marketing-contacts
name: HubSpot Marketing Contacts
description: Contact lists, segmentation, campaigns
role: marketing
requiredTools:
  - type: mcpService
    serviceType: hubspot
---

## HubSpot Marketing Contacts

When using HubSpot for marketing contacts:

- List or search contacts with relevant properties for segmentation questions.
- Use get contact for full details when the user asks about a specific person or email.
- When asked about lists or segments, summarize contact counts and key properties.
- For campaign context, relate contacts to companies or deals when that helps the answer.
- Prefer search when the user provides an email, name, or other identifier.

## Step-by-step instructions

1. For “find contact X”: use search (email, name, or identifier); then get contact for full details if needed.
2. For lists/segments: list or search contacts with filters or properties; summarize counts and key properties.
3. For campaign context: relate contacts to companies or deals via HubSpot tools when the question asks for it.
4. Always return concise summaries (counts, key fields) rather than raw dumps; cite filters used.

## Examples of inputs and outputs

- **Input**: “Who is john@example.com in HubSpot?”  
  **Output**: Short summary from get contact: name, email, key properties, and company/deal if relevant.

- **Input**: “How many contacts do we have in segment Y?”  
  **Output**: Count and brief description of the segment (filters/properties); from list or search with those filters.

## Common edge cases

- **No contact found**: Say “No contact found for [identifier]” and suggest checking spelling or trying another field.
- **Vague “segment”**: Ask which list, property, or filter they mean; or list available properties and let them choose.
- **Large result set**: Summarize count and a sample (e.g. first 5–10) with key properties; do not dump hundreds of contacts.
- **API/oauth error**: Tell the user the HubSpot request failed and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **Search contacts**: Use when the user gives an email, name, or other identifier; then get contact for full details.
- **List contacts**: Use for “how many”, “list by property”, or segment-style questions with filters.
- **Get contact**: Use after search or when the user asks for full details for one contact.
- **Companies/deals**: Use when the question ties contacts to companies or deals (campaign, account).
