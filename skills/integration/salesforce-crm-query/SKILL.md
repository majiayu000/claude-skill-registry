---
id: salesforce-crm-query
name: Salesforce CRM Query
description: List objects, describe schema, run SOQL queries
role: sales
requiredTools:
  - type: mcpService
    serviceType: salesforce
---

## Salesforce CRM Query

When querying Salesforce data:

- Use **salesforce_list_objects** (tool name may have a suffix if multiple Salesforce servers exist) to discover standard and custom objects in the org.
- Use **salesforce_describe_object** to get fields and relationships for an object before querying.
- Use **salesforce_query** to run SOQL queries (read-only); build queries from the described schema.
- Follow a discovery-first workflow: list objects -> describe object -> query. All tools are read-only.
- Summarize records clearly; cite object and key fields; avoid dumping raw result sets unless asked.

## Step-by-step instructions

1. When the user asks about "accounts", "contacts", or an object name: if unsure of the exact API name, call **salesforce_list_objects** to find it.
2. Before running a query: call **salesforce_describe_object** for that object to get field names and types so the SOQL query uses valid fields.
3. Call **salesforce_query** with a SOQL string (e.g. SELECT Id, Name FROM Account LIMIT 10); use only fields from the describe result.
4. Summarize the returned records (count, key fields); for large result sets, summarize and offer to narrow.
5. Salesforce uses instance_url from the token; the tools use the correct instance automatically.

## Examples of inputs and outputs

- **Input**: "List recent accounts."  
  **Output**: Short list of Account records (Id, Name, and other requested fields) from **salesforce_query** with a SOQL like SELECT Id, Name FROM Account ORDER BY CreatedDate DESC LIMIT 10.

- **Input**: "What fields does the Contact object have?"  
  **Output**: List of field names and types from **salesforce_describe_object** for Contact; summarize key fields (e.g. Name, Email, AccountId).

## Common edge cases

- **Object not found**: Say "Object [name] not found" and suggest listing objects or checking the API name (e.g. custom objects have __c).
- **Invalid SOQL**: If the query fails, check field names against **salesforce_describe_object** and retry; report the error to the user.
- **Large result set**: SOQL has limits; summarize the first page and mention limits; do not assume all records were returned.
- **API/OAuth error**: Report that Salesforce returned an error and suggest reconnecting or retrying; ensure instance_url is used (handled by the integration).

## Tool usage for specific purposes

- **salesforce_list_objects**: Use when the user asks about "objects" or when you need to resolve an object API name.
- **salesforce_describe_object**: Use before building a SOQL query to get valid field names and types.
- **salesforce_query**: Use to run read-only SOQL; always use fields from describe; include LIMIT and ORDER BY as appropriate.
