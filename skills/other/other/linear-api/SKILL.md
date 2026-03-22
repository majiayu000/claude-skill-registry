---
name: linear
description: |
  Linear API integration with managed OAuth. Query and manage issues, projects, teams, cycles, and labels using GraphQL.
  Use this skill when users want to create, update, or query Linear issues, search for tasks, manage projects, or track work.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Linear

Access the Linear API with managed OAuth authentication. Query and manage issues, projects, teams, cycles, labels, and comments using GraphQL.

## Quick Start

```bash
# Get current user
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': '{ viewer { id name email } }'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/linear/graphql', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/linear/graphql
```

All requests use POST to the GraphQL endpoint. The gateway proxies requests to `api.linear.app` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
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

Manage your Linear OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=linear&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'linear'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "fda4dabb-9d62-47e3-9503-a2f29d0995df",
    "status": "ACTIVE",
    "creation_time": "2026-02-04T23:03:22.676001Z",
    "last_updated_time": "2026-02-04T23:03:51.239577Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "linear",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Linear connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': '{ viewer { id name } }'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/linear/graphql', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', 'fda4dabb-9d62-47e3-9503-a2f29d0995df')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

Linear uses a GraphQL API. All operations are sent as POST requests with a JSON body containing the `query` field.

### Viewer (Current User)

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ viewer { id name email } }"}
```

**Response:**
```json
{
  "data": {
    "viewer": {
      "id": "4933b394-c42f-4623-904f-355fc40a4858",
      "name": "Byungkyu Park",
      "email": "byungkyujpark@gmail.com"
    }
  }
}
```

### Organization

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ organization { id name urlKey } }"}
```

### Teams

#### List Teams

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ teams { nodes { id name key } } }"}
```

**Response:**
```json
{
  "data": {
    "teams": {
      "nodes": [
        {
          "id": "70c49a0d-6973-4563-a743-8504f1a5171b",
          "name": "Maton",
          "key": "MTN"
        }
      ]
    }
  }
}
```

#### Get Team

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ team(id: \"TEAM_ID\") { id name key issues { nodes { id identifier title } } } }"}
```

### Issues

#### List Issues

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issues(first: 10) { nodes { id identifier title state { name } priority createdAt } pageInfo { hasNextPage endCursor } } }"}
```

**Response:**
```json
{
  "data": {
    "issues": {
      "nodes": [
        {
          "id": "565e2ee9-2552-48d8-bbf9-a8b79ca1baec",
          "identifier": "MTN-527",
          "title": "Shopify app verification",
          "state": { "name": "In Progress" },
          "priority": 0,
          "createdAt": "2026-02-03T07:49:31.675Z"
        }
      ],
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "4c7b33c8-dabf-47ce-9d30-7f286f9463be"
      }
    }
  }
}
```

#### Get Issue by ID or Identifier

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issue(id: \"MTN-527\") { id identifier title description state { name } priority assignee { name } team { key name } createdAt updatedAt } }"}
```

#### Filter Issues

Filter by state type:

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issues(first: 10, filter: { state: { type: { eq: \"started\" } } }) { nodes { id identifier title state { name type } } } }"}
```

Filter by title:

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issues(first: 10, filter: { title: { containsIgnoreCase: \"bug\" } }) { nodes { id identifier title } } }"}
```

#### Search Issues

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ searchIssues(first: 10, term: \"shopify\") { nodes { id identifier title } } }"}
```

#### Create Issue

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "mutation { issueCreate(input: { teamId: \"TEAM_ID\", title: \"New issue title\", description: \"Issue description\" }) { success issue { id identifier title state { name } } } }"}
```

**Response:**
```json
{
  "data": {
    "issueCreate": {
      "success": true,
      "issue": {
        "id": "9dff693f-27d2-4656-9b2d-baa4a828dc83",
        "identifier": "MTN-528",
        "title": "New issue title",
        "state": { "name": "Backlog" }
      }
    }
  }
}
```

#### Update Issue

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "mutation { issueUpdate(id: \"ISSUE_ID\", input: { title: \"Updated title\", priority: 2 }) { success issue { id identifier title priority } } }"}
```

### Projects

#### List Projects

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ projects(first: 10) { nodes { id name state createdAt } } }"}
```

### Cycles

#### List Cycles

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ cycles(first: 10) { nodes { id name number startsAt endsAt } } }"}
```

### Labels

#### List Labels

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ issueLabels(first: 20) { nodes { id name color } } }"}
```

**Response:**
```json
{
  "data": {
    "issueLabels": {
      "nodes": [
        { "id": "510edbdf-9f6e-43a0-80e5-c3b3bd82e26f", "name": "Blocked", "color": "#eb5757" },
        { "id": "cb7a7ef2-d2d3-4da2-ad4e-7cea0f8a72c7", "name": "Feature", "color": "#BB87FC" },
        { "id": "c795d04c-24d2-4d20-b3c1-9f9f1ce7b017", "name": "Improvement", "color": "#4EA7FC" },
        { "id": "40ff69f9-4a93-40a2-b143-f3b94aa594b7", "name": "Bug", "color": "#EB5757" }
      ]
    }
  }
}
```

### Workflow States

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ workflowStates(first: 20) { nodes { id name type team { key } } } }"}
```

**Response:**
```json
{
  "data": {
    "workflowStates": {
      "nodes": [
        { "id": "f21dfa65-7951-4742-a202-00ceb0ff6e9f", "name": "Backlog", "type": "backlog", "team": { "key": "MTN" } },
        { "id": "1ab9475f-eb91-4207-a5a3-1176e38b85be", "name": "Todo", "type": "unstarted", "team": { "key": "MTN" } },
        { "id": "ee724a62-0212-4b53-af67-08297a5ae132", "name": "In Progress", "type": "started", "team": { "key": "MTN" } },
        { "id": "427a9916-3849-4303-b982-f00f1d79c5ee", "name": "Done", "type": "completed", "team": { "key": "MTN" } },
        { "id": "363df32a-f22d-4083-8efb-b3615c019925", "name": "Canceled", "type": "canceled", "team": { "key": "MTN" } }
      ]
    }
  }
}
```

### Users

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ users(first: 20) { nodes { id name email active } } }"}
```

### Comments

#### List Comments

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "{ comments(first: 10) { nodes { id body createdAt issue { identifier } user { name } } } }"}
```

#### Create Comment

```bash
POST /linear/graphql
Content-Type: application/json

{"query": "mutation { commentCreate(input: { issueId: \"ISSUE_ID\", body: \"Comment text here\" }) { success comment { id body } } }"}
```

## Pagination

Linear uses Relay-style cursor-based pagination with `first/after` and `last/before` arguments.

```bash
# First page
POST /linear/graphql
{"query": "{ issues(first: 10) { nodes { id identifier title } pageInfo { hasNextPage endCursor } } }"}

# Next page using endCursor
POST /linear/graphql
{"query": "{ issues(first: 10, after: \"CURSOR_VALUE\") { nodes { id identifier title } pageInfo { hasNextPage endCursor } } }"}
```

Response includes `pageInfo`:

```json
{
  "data": {
    "issues": {
      "nodes": [...],
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "4c7b33c8-dabf-47ce-9d30-7f286f9463be"
      }
    }
  }
}
```

## Code Examples

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/linear/graphql', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: `{ issues(first: 10) { nodes { id identifier title state { name } } } }`
  })
});
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/linear/graphql',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'query': '{ issues(first: 10) { nodes { id identifier title state { name } } } }'
    }
)
data = response.json()
```

## Notes

- Linear uses GraphQL exclusively (no REST API)
- Issue identifiers like `MTN-527` can be used in place of UUIDs for the `id` parameter
- Priority values: 0 = No priority, 1 = Urgent, 2 = High, 3 = Medium, 4 = Low
- Workflow state types: `backlog`, `unstarted`, `started`, `completed`, `canceled`
- The GraphQL schema is introspectable at `https://api.linear.app/graphql`
- Use `searchIssues(term: "...")` for full-text search across issues
- Some mutations (delete, create labels/projects) may require additional OAuth scopes. If you receive a scope error, contact Maton support at support@maton.ai with the specific operations/APIs you need and your use-case

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Linear connection or GraphQL validation error |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient OAuth scope for the operation |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Linear API |

GraphQL errors are returned in the `errors` array:

```json
{
  "errors": [
    {
      "message": "Invalid scope: `write` required",
      "extensions": {
        "type": "forbidden",
        "code": "FORBIDDEN",
        "statusCode": 403
      }
    }
  ]
}
```

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `linear`. For example:

- Correct: `https://gateway.maton.ai/linear/graphql`
- Incorrect: `https://gateway.maton.ai/graphql`

## Resources

- [Linear API Overview](https://linear.app/developers)
- [Linear GraphQL Getting Started](https://linear.app/developers/graphql)
- [Linear GraphQL Schema (Apollo Studio)](https://studio.apollographql.com/public/Linear-API/schema/reference?variant=current)
- [Linear API and Webhooks](https://linear.app/docs/api-and-webhooks)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
