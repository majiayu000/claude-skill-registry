---
name: jira
description: Jira Cloud REST API via curl. Use this skill to create, update, search, and manage issues, projects, and workflows in Jira.
vm0_secrets:
  - JIRA_API_TOKEN
vm0_vars:
  - JIRA_DOMAIN
  - JIRA_EMAIL
---

# Jira API

Use the Jira Cloud REST API via direct `curl` calls to manage **issues, projects, and workflows**.

> Official docs: `https://developer.atlassian.com/cloud/jira/platform/rest/v3/`

---

## When to Use

Use this skill when you need to:

- **Create issues** in Jira projects
- **Search issues** using JQL (Jira Query Language)
- **Update issues** (status, assignee, priority, etc.)
- **Get issue details** and comments
- **List projects** and their metadata
- **Transition issues** through workflow states
- **Add comments** to issues

---

## Prerequisites

1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Copy the generated token (you won't see it again)

```bash
export JIRA_DOMAIN="mycompany" # e.g., "mycompany" or "mycompany.atlassian.net"
export JIRA_EMAIL="you@example.com" # Your Atlassian account email
export JIRA_API_TOKEN="your-api-token" # API token from step 2
```

### Rate Limits

Jira Cloud has rate limits that vary by endpoint. For most REST API calls, expect limits around 100-500 requests per minute.

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq '.field'
> ```

## How to Use

All examples below assume `JIRA_DOMAIN`, `JIRA_EMAIL`, and `JIRA_API_TOKEN` are set.

Base URL: `https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3`

> Note: `${JIRA_DOMAIN%.atlassian.net}` strips the suffix if present, so both `mycompany` and `mycompany.atlassian.net` work.

---

### 1. Get Current User

Verify your authentication:

```bash
bash -c 'curl -s -X GET "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/myself" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json"'
```

---

### 2. List Projects

Get all projects you have access to:

```bash
bash -c 'curl -s -X GET "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/project" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json"'
```

---

### 3. Get Project Details

Get details for a specific project:

```bash
PROJECT_KEY="PROJ"

bash -c 'curl -s -X GET "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/project/${PROJECT_KEY}" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json"'
```

---

### 4. Get Issue Types for Project

List available issue types (Task, Bug, Story, etc.):

```bash
PROJECT_KEY="PROJ"

bash -c 'curl -s -X GET "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/project/${PROJECT_KEY}" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json"'
```

---

### 5. Search Issues with JQL

Search issues using Jira Query Language:

Write to `/tmp/jira_request.json`:

```json
{
  "jql": "project = PROJ AND status NOT IN (Done) ORDER BY created DESC",
  "maxResults": 10,
  "fields": ["key", "summary", "status", "assignee", "priority"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/search/jql" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json" --header "Content-Type: application/json" -d @/tmp/jira_request.json' | jq '.issues[] | {key, summary: .fields.summary, status: .fields.status.name, assignee: .fields.assignee.displayName, priority: .fields.priority.name}''
```

Common JQL examples:
- `project = PROJ` - Issues in project
- `assignee = currentUser()` - Your issues
- `status = "In Progress"` - By status
- `status NOT IN (Done, Closed)` - Exclude statuses
- `created >= -7d` - Created in last 7 days
- `labels = bug` - By label
- `priority = High` - By priority

---

### 6. Get Issue Details

Get full details of an issue:

```bash
ISSUE_KEY="PROJ-123"

bash -c 'curl -s -X GET "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/issue/${ISSUE_KEY}" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json"'
```

---

### 7. Create Issue

Create a new issue (API v3 uses Atlassian Document Format for description):

Write to `/tmp/jira_request.json`:

```json
{
  "fields": {
    "project": {"key": "PROJ"},
    "summary": "Bug: Login button not responding",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {"type": "text", "text": "The login button on the mobile app is not responding when tapped."}
          ]
        }
      ]
    },
    "issuetype": {"name": "Bug"}
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/issue" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json" --header "Content-Type: application/json" -d @/tmp/jira_request.json'
```

---

### 8. Create Issue with Priority and Labels

Create issue with additional fields:

Write to `/tmp/jira_request.json`:

```json
{
  "fields": {
    "project": {"key": "PROJ"},
    "summary": "Implement user authentication",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {"type": "text", "text": "Add OAuth2 authentication flow for the mobile app."}
          ]
        }
      ]
    },
    "issuetype": {"name": "Story"},
    "priority": {"name": "High"},
    "labels": ["backend", "security"]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/issue" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json" --header "Content-Type: application/json" -d @/tmp/jira_request.json'
```

---

### 9. Update Issue

Update an existing issue:

```bash
ISSUE_KEY="PROJ-123"
```

Write to `/tmp/jira_request.json`:

```json
{
  "fields": {
    "summary": "Updated: Login button not responding on iOS",
    "priority": {"name": "Highest"},
    "labels": ["bug", "ios", "urgent"]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/issue/${ISSUE_KEY}" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json" --header "Content-Type: application/json" -d @/tmp/jira_request.json'
```

Returns 204 No Content on success.

---

### 10. Get Available Transitions

Get possible status transitions for an issue:

```bash
ISSUE_KEY="PROJ-123"

bash -c 'curl -s -X GET "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/issue/${ISSUE_KEY}/transitions" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json"'
```

---

### 11. Transition Issue (Change Status)

Move issue to a different status:

```bash
ISSUE_KEY="PROJ-123"
TRANSITION_ID="31" # Get from transitions endpoint
```

Write to `/tmp/jira_request.json`:

```json
{
  "transition": {
    "id": "<your-transition-id>"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/issue/${ISSUE_KEY}/transitions" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json" --header "Content-Type: application/json" -d @/tmp/jira_request.json'
```

Returns 204 No Content on success.

---

### 12. Add Comment

Add a comment to an issue:

```bash
ISSUE_KEY="PROJ-123"
```

Write to `/tmp/jira_request.json`:

```json
{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {"type": "text", "text": "Investigated and found the root cause. Working on a fix."}
        ]
      }
    ]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/issue/${ISSUE_KEY}/comment" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json" --header "Content-Type: application/json" -d @/tmp/jira_request.json'
```

---

### 13. Get Issue Comments

List all comments on an issue:

```bash
ISSUE_KEY="PROJ-123"

bash -c 'curl -s -X GET "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/issue/${ISSUE_KEY}/comment" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json"'
```

---

### 14. Assign Issue

Assign an issue to a user:

```bash
ISSUE_KEY="PROJ-123"
ACCOUNT_ID="5b10ac8d82e05b22cc7d4ef5" # Get from /rest/api/3/user/search
```

Write to `/tmp/jira_request.json`:

```json
{
  "accountId": "<your-account-id>"
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/issue/${ISSUE_KEY}/assignee" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json" --header "Content-Type: application/json" -d @/tmp/jira_request.json'
```

---

### 15. Search Users

Find users by email or name:

Write to `/tmp/jira_search.txt`:

```
john
```

```bash
bash -c 'curl -s -G "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/user/search" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}" --header "Accept: application/json" --data-urlencode "query@/tmp/jira_search.txt"'
```

---

### 16. Delete Issue

Delete an issue (use with caution):

```bash
ISSUE_KEY="PROJ-123"

bash -c 'curl -s -X DELETE "https://${JIRA_DOMAIN%.atlassian.net}.atlassian.net/rest/api/3/issue/${ISSUE_KEY}" -u "${JIRA_EMAIL}:${JIRA_API_TOKEN}"'
```

Returns 204 No Content on success.

---

## Atlassian Document Format (ADF)

Jira API v3 uses ADF for rich text fields like `description` and `comment.body`. Basic structure:

```json
{
  "type": "doc",
  "version": 1,
  "content": [
  {
  "type": "paragraph",
  "content": [
  {"type": "text", "text": "Plain text"},
  {"type": "text", "text": "Bold text", "marks": [{"type": "strong"}]},
  {"type": "text", "text": "Code", "marks": [{"type": "code"}]}
  ]
  },
  {
  "type": "bulletList",
  "content": [
  {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Item 1"}]}]},
  {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Item 2"}]}]}
  ]
  },
  {
  "type": "codeBlock",
  "attrs": {"language": "python"},
  "content": [{"type": "text", "text": "print('hello')"}]
  }
  ]
}
```

---

## Guidelines

1. **Use JQL for complex queries**: JQL is powerful for filtering issues by any field combination
2. **Check transitions first**: Before changing status, get available transitions for the issue
3. **Handle pagination**: Use `startAt` and `maxResults` for large result sets
4. **Use account IDs**: Jira Cloud uses account IDs (not usernames) for user references
5. **ADF for rich text**: API v3 requires Atlassian Document Format for description and comments
6. **Rate limiting**: Implement exponential backoff if you receive 429 responses
