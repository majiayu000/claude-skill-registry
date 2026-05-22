---
name: apollo
description: |
  Apollo.io API integration with managed OAuth. Search and enrich people and companies, manage contacts and accounts. Use this skill when users want to prospect, enrich leads, or manage sales data.
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
---

# Apollo

Access the Apollo.io API with managed OAuth authentication. Search people and organizations, enrich contacts, and manage your sales pipeline.

## Quick Start

```bash
# Search for people at a company
curl -s -X POST 'https://gateway.maton.ai/apollo/v1/mixed_people/api_search' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{"q_organization_name": "Google", "per_page": 10}'
```

## Base URL

```
https://gateway.maton.ai/apollo/{native-api-path}
```

Replace `{native-api-path}` with the actual Apollo API endpoint path. The gateway proxies requests to `api.apollo.io` and automatically injects your API key.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Apollo connections at `https://ctrl.maton.ai`.

### List Connections

```bash
curl -s -X GET 'https://ctrl.maton.ai/connections?app=apollo&status=ACTIVE' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### Create Connection

```bash
curl -s -X POST 'https://ctrl.maton.ai/connections' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{"app": "apollo"}'
```

### Get Connection

```bash
curl -s -X GET 'https://ctrl.maton.ai/connections/{connection_id}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

**Response:**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "apollo",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
curl -s -X DELETE 'https://ctrl.maton.ai/connections/{connection_id}' \
  -H 'Authorization: Bearer YOUR_API_KEY'
```

### Specifying Connection

If you have multiple Apollo connections, specify which one to use with the `Maton-Connection` header:

```bash
curl -s -X POST 'https://gateway.maton.ai/apollo/v1/mixed_people/api_search' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Maton-Connection: 21fd90f9-5935-43cd-b6c8-bde9d915ca80' \
  -d '{"q_organization_name": "Google", "per_page": 10}'
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### People

#### Search People

```bash
POST /apollo/v1/mixed_people/api_search
Content-Type: application/json

{
  "q_organization_name": "Google",
  "page": 1,
  "per_page": 25
}
```

#### Enrich Person by Email

```bash
POST /apollo/v1/people/match
Content-Type: application/json

{
  "email": "john@example.com"
}
```

#### Enrich Person by LinkedIn

```bash
POST /apollo/v1/people/match
Content-Type: application/json

{
  "linkedin_url": "https://linkedin.com/in/johndoe"
}
```

### Organizations

#### Search Organizations

```bash
POST /apollo/v1/organizations/search
Content-Type: application/json

{
  "q_organization_name": "Google",
  "page": 1,
  "per_page": 25
}
```

#### Enrich Organization

```bash
POST /apollo/v1/organizations/enrich
Content-Type: application/json

{
  "domain": "google.com"
}
```

### Contacts

#### Search Contacts

```bash
POST /apollo/v1/contacts/search
Content-Type: application/json

{
  "page": 1,
  "per_page": 25
}
```

#### Create Contact

```bash
POST /apollo/v1/contacts
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "organization_name": "Acme Corp"
}
```

#### Update Contact

```bash
PUT /apollo/v1/contacts/{contactId}
Content-Type: application/json

{
  "first_name": "Jane"
}
```

### Accounts

#### Search Accounts

```bash
POST /apollo/v1/accounts/search
Content-Type: application/json

{
  "page": 1,
  "per_page": 25
}
```

#### Create Account

```bash
POST /apollo/v1/accounts
Content-Type: application/json

{
  "name": "Acme Corp",
  "domain": "acme.com"
}
```

### Sequences

#### Search Sequences

```bash
POST /apollo/v1/emailer_campaigns/search
Content-Type: application/json

{
  "page": 1,
  "per_page": 25
}
```

#### Add Contact to Sequence

```bash
POST /apollo/v1/emailer_campaigns/{campaignId}/add_contact_ids
Content-Type: application/json

{
  "contact_ids": ["contact_id_1", "contact_id_2"]
}
```

### Labels

#### List Labels

```bash
GET /apollo/v1/labels
```

## Search Filters

Common search parameters:
- `q_organization_name` - Company name
- `q_person_title` - Job title
- `person_locations` - Array of locations
- `organization_num_employees_ranges` - Employee count ranges
- `q_keywords` - General keyword search

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/apollo/v1/mixed_people/api_search',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      q_organization_name: 'Google',
      per_page: 10
    })
  }
);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/apollo/v1/mixed_people/api_search',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'q_organization_name': 'Google', 'per_page': 10}
)
```

## Notes

- Pagination uses `page` and `per_page` in POST body
- Most list endpoints use POST with `/search` suffix
- Email enrichment consumes credits
- `people/search` and `mixed_people/search` are deprecated - use `mixed_people/api_search`

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Apollo connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Apollo API |

## Resources

- [Apollo API Overview](https://docs.apollo.io/reference/introduction)
- [Search People](https://docs.apollo.io/reference/people-api-search.md)
- [Enrich Person](https://docs.apollo.io/reference/people-enrichment.md)
- [Search Organizations](https://docs.apollo.io/reference/organization-search.md)
- [Enrich Organization](https://docs.apollo.io/reference/organization-enrichment.md)
- [Create Contact](https://docs.apollo.io/reference/create-a-contact.md)
- [LLM Reference](https://docs.apollo.io/llms.txt)
