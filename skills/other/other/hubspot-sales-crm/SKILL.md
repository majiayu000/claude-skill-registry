---
id: hubspot-sales-crm
name: HubSpot Sales CRM
description: Contacts, companies, deals pipeline
role: sales
requiredTools:
  - type: mcpService
    serviceType: hubspot
---

## HubSpot Sales CRM

When using HubSpot for sales:

- List or search contacts, companies, and deals to answer pipeline and relationship questions.
- Use get contact/company/deal for full details before summarizing.
- When reporting pipeline, group deals by stage or owner and summarize amounts or counts.
- For contact lookup, prefer search by email or name; then use get for full record.
- Keep property names and IDs consistent with HubSpot’s schema in responses.

## Step-by-step instructions

1. For contact/company/deal lookup: search by email, name, or identifier; then use get for the full record before summarizing.
2. For pipeline: list deals with filters (stage, owner); group by stage or owner and summarize counts and amounts.
3. For relationships: use get contact/company/deal and follow associations (e.g. contact’s companies, company’s deals).
4. Keep property names and IDs as in HubSpot; summarize in plain language but cite key IDs when relevant.

## Examples of inputs and outputs

- **Input**: “What’s the status of deal X?”  
  **Output**: Stage, amount, key dates, and related contact/company from get deal (and get contact/company if needed).

- **Input**: “Pipeline by stage this month.”  
  **Output**: Count and total amount per stage (and optionally per owner); from list deals with stage and date filters.

## Common edge cases

- **Record not found**: Say “No [contact/company/deal] found for [identifier]” and suggest checking ID or search term.
- **Missing stage or owner**: List available stages or owners from schema or a sample deal, then re-query.
- **Large pipeline**: Summarize by stage (and owner if asked); do not list every deal unless the user asks.
- **API/oauth error**: Report that HubSpot returned an error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **Search**: Use for contact/company/deal lookup by email, name, or other identifier; then get for full details.
- **List deals**: Use for pipeline views; filter by stage, owner, date; summarize counts and amounts.
- **Get contact/company/deal**: Use for full record and associations (e.g. contact’s companies, deal’s contact).
