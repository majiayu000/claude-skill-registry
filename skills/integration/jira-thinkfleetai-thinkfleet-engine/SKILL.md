---
name: jira
description: "Manage Jira issues, projects, and boards via the Atlassian REST API."
metadata: {"thinkfleetbot":{"emoji":"📋","requires":{"bins":["curl","jq"],"env":["JIRA_BASE_URL","JIRA_EMAIL","JIRA_API_TOKEN"]}}}
---

# Jira

Manage Jira issues, projects, and boards via the REST API.

## Environment Variables

- `JIRA_BASE_URL` - Jira instance URL (e.g. `https://yourorg.atlassian.net`)
- `JIRA_EMAIL` - Atlassian account email
- `JIRA_API_TOKEN` - API token (generate at https://id.atlassian.com/manage-profile/security/api-tokens)

## Auth header

All requests use Basic auth:

```bash
JIRA_AUTH=$(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)
```

## Search issues (JQL)

```bash
curl -s -H "Authorization: Basic $(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/3/search?jql=project%3DDEV%20AND%20status%3D%22In%20Progress%22&maxResults=10" | jq '.issues[] | {key, summary: .fields.summary, status: .fields.status.name}'
```

## Get issue details

```bash
curl -s -H "Authorization: Basic $(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)" \
  "$JIRA_BASE_URL/rest/api/3/issue/DEV-123" | jq '{key, summary: .fields.summary, status: .fields.status.name, assignee: .fields.assignee.displayName, description: .fields.description}'
```

## Create issue

```bash
curl -s -X POST -H "Authorization: Basic $(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/3/issue" \
  -d '{
    "fields": {
      "project": {"key": "DEV"},
      "summary": "Bug: Login page broken",
      "description": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Description here"}]}]},
      "issuetype": {"name": "Bug"}
    }
  }' | jq '{key: .key, self: .self}'
```

## Transition issue (change status)

```bash
# First get available transitions
curl -s -H "Authorization: Basic $(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)" \
  "$JIRA_BASE_URL/rest/api/3/issue/DEV-123/transitions" | jq '.transitions[] | {id, name}'

# Then transition
curl -s -X POST -H "Authorization: Basic $(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/3/issue/DEV-123/transitions" \
  -d '{"transition": {"id": "31"}}'
```

## Add comment

```bash
curl -s -X POST -H "Authorization: Basic $(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)" \
  -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/3/issue/DEV-123/comment" \
  -d '{"body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Comment from ThinkFleetBot"}]}]}}' | jq '{id: .id, created: .created}'
```

## List projects

```bash
curl -s -H "Authorization: Basic $(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)" \
  "$JIRA_BASE_URL/rest/api/3/project" | jq '.[] | {key, name}'
```

## Notes

- Jira Cloud uses API v3 with ADF (Atlassian Document Format) for descriptions/comments.
- Jira Server/Data Center may use API v2 with plain text or wiki markup.
- Rate limits apply; check response headers for `X-RateLimit-Remaining`.
- Always confirm before creating, transitioning, or deleting issues.
