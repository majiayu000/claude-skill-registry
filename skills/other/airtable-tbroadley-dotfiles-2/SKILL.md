---
name: airtable
description: Access Airtable bases, tables, and records. Query data, search records, and read structured information.
---

# Airtable Integration

This skill provides access to Airtable bases and tables via the Airtable REST API.

## Setup Required

**Create a Personal Access Token:**

1. Go to https://airtable.com/create/tokens
2. Click "Create new token"
3. Give it a name (e.g., "Claude Code")
4. Add scopes:
   - `data.records:read` - Read records
   - `schema.bases:read` - Read base schema
5. Add access to the bases you want to query
6. Create and copy the token

Set the token as an environment variable:
```bash
export AIRTABLE_TOKEN="pat..."
```

## When to Use

Use this skill when the user:
- Asks about data stored in Airtable
- Wants to query or search Airtable records
- Needs to look up information in a base
- Mentions "Airtable" or specific base/table names

## API Endpoints

Base URL: `https://api.airtable.com/v0`

All requests need:
```bash
-H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

### List Bases

**Get All Bases**:
```bash
curl -s "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)" | jq '.bases[] | {name, id}'
```

### Get Base Schema

**Get Tables and Fields**:
```bash
curl -s "https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

### List Records

**Get Records from Table**:
```bash
curl -s "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

**With Pagination**:
```bash
curl -s "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}?pageSize=100" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

### Filter Records

**Using Formula Filter**:
```bash
curl -s -G "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}" \
  --data-urlencode "filterByFormula={Status}='Active'" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

**Multiple Conditions**:
```bash
curl -s -G "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}" \
  --data-urlencode "filterByFormula=AND({Status}='Active', {Priority}='High')" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

### Sort Records

```bash
curl -s -G "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}" \
  --data-urlencode "sort[0][field]=Created" \
  --data-urlencode "sort[0][direction]=desc" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

### Select Specific Fields

```bash
curl -s -G "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}" \
  --data-urlencode "fields[]=Name" \
  --data-urlencode "fields[]=Status" \
  --data-urlencode "fields[]=Due Date" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

### Get Single Record

```bash
curl -s "https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}/{RECORD_ID}" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

## Formula Syntax

Airtable formulas for filtering:

| Formula | Description |
|---------|-------------|
| `{Field}='Value'` | Exact match |
| `{Field}!='Value'` | Not equal |
| `FIND('text', {Field})` | Contains text |
| `{Field}>100` | Numeric comparison |
| `IS_AFTER({Date}, '2024-01-01')` | Date after |
| `IS_BEFORE({Date}, '2024-01-01')` | Date before |
| `{Checkbox}=TRUE()` | Checkbox is checked |
| `{Field}=BLANK()` | Field is empty |
| `AND(cond1, cond2)` | Both conditions |
| `OR(cond1, cond2)` | Either condition |
| `NOT(condition)` | Negation |

## Common Workflows

### List All Bases
```bash
curl -s "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)" | jq '.bases[] | {name, id}'
```

### Explore a Base's Structure
```bash
BASE_ID="appXXXXXXXX"
curl -s "https://api.airtable.com/v0/meta/bases/${BASE_ID}/tables" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)" | jq '.tables[] | {name, id, fields: [.fields[].name]}'
```

### Get Recent Records
```bash
BASE_ID="appXXXXXXXX"
TABLE="Tasks"
curl -s -G "https://api.airtable.com/v0/${BASE_ID}/${TABLE}" \
  --data-urlencode "sort[0][field]=Created" \
  --data-urlencode "sort[0][direction]=desc" \
  --data-urlencode "pageSize=10" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)" | jq '.records[] | .fields'
```

### Search for Records
```bash
BASE_ID="appXXXXXXXX"
TABLE="Contacts"
curl -s -G "https://api.airtable.com/v0/${BASE_ID}/${TABLE}" \
  --data-urlencode "filterByFormula=FIND('John', {Name})" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

### Filter by Status
```bash
curl -s -G "https://api.airtable.com/v0/${BASE_ID}/${TABLE}" \
  --data-urlencode "filterByFormula={Status}='In Progress'" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)" | jq '.records[] | {name: .fields.Name, status: .fields.Status}'
```

## Finding Base and Table IDs

**Base ID**: Found in the Airtable URL: `https://airtable.com/{BASE_ID}/...`
- Starts with `app`

**Table Name**: Use the exact table name from Airtable (URL-encode spaces)
- Or use table ID (starts with `tbl`) from the schema endpoint

**Record ID**: Starts with `rec`, found in record URLs or API responses

## Pagination

Responses are paginated (max 100 records per request). Use the `offset` parameter:

```bash
# First request
curl -s "https://api.airtable.com/v0/${BASE_ID}/${TABLE}?pageSize=100" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"

# If response includes "offset", use it for next page
curl -s "https://api.airtable.com/v0/${BASE_ID}/${TABLE}?pageSize=100&offset={OFFSET_FROM_RESPONSE}" \
  -H "Authorization: Bearer $(printenv AIRTABLE_TOKEN)"
```

## Notes

- Rate limit: 5 requests/second per base
- Max 100 records per request
- Field names are case-sensitive
- URL-encode table names with spaces
- Linked records return record IDs; fetch separately if needed
- Attachments return URLs that expire
