---
name: jira-api
description: |
  Comprehensive reference for Atlassian Jira REST API v3 documentation and best practices.
  Use when asking about Jira API endpoints, authentication, request/response formats, JQL queries,
  Atlassian Document Format (ADF), webhooks, error handling, rate limiting, and API usage patterns.
  Trigger terms: "Jira API endpoint", "how do I use the API", "JQL query", "ADF format",
  "API authentication", "API request", "webhook payload", "Jira REST API", "custom fields",
  "API rate limit", "API error", "expand fields", "pagination".
allowed-tools: WebFetch, Read, Bash
---

# Jira REST API v3 Documentation

## Purpose

This skill provides authoritative guidance on using the Atlassian Jira REST API v3, including endpoint references, authentication methods, request/response formats, query languages, and best practices for programmatic Jira automation and integration.

## Quick Start

To get started with the Jira API:

1. **Authenticate**: Use Basic Auth with API token (email:token in base64)
2. **Make a request**: `GET /rest/api/3/issue/{issueIdOrKey}`
3. **Parse response**: Standard JSON with issue details, changelog, and custom fields

For the project's `JiraClient` class:
```python
from jira_tool.client import JiraClient

client = JiraClient()
issue = client.get_issue("PROJ-123")
```

## Instructions

### Step 1: Understanding Jira REST API v3 Basics

The Jira REST API v3 is the current standard API for Jira Cloud. Key characteristics:
- **Base URL**: `https://{jira-instance}.atlassian.net/rest/api/3/`
- **Authentication**: Basic Auth with API tokens (not passwords)
- **Data Format**: JSON for requests and responses
- **Versioning**: v3 is the latest; v2 is deprecated

**Official Documentation**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/

### Step 2: Authentication Methods

#### Basic Auth with API Token (Recommended)

This is what the project uses. Steps:
1. Generate API token in Jira user settings (atlassian account)
2. Create header: `Authorization: Basic {base64(email:token)}`
3. Add `Accept: application/json` and `Content-Type: application/json` headers

```python
from base64 import b64encode

email = "user@example.com"
api_token = "your-api-token"
credentials = f"{email}:{api_token}"
auth_header = b64encode(credentials.encode()).decode()
headers = {
    "Authorization": f"Basic {auth_header}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
```

The `JiraClient` class handles this automatically:
```python
client = JiraClient(
    base_url="https://company.atlassian.net",
    username="user@example.com",
    api_token="token-from-atlassian"
)
```

#### OAuth 2.0

For third-party applications:
- Requires OAuth app registration
- More complex but better for user-facing integrations
- See references/reference.md for OAuth flow details

### Step 3: Core API Endpoints

Common endpoints you'll use frequently:

**Issue Operations**
- `GET /rest/api/3/issue/{issueIdOrKey}` - Get issue details
- `POST /rest/api/3/issues` - Create issue
- `PUT /rest/api/3/issue/{issueIdOrKey}` - Update issue
- `DELETE /rest/api/3/issue/{issueIdOrKey}` - Delete issue
- `POST /rest/api/3/issue/{issueIdOrKey}/comment` - Add comment

**Searching & Filtering**
- `GET /rest/api/3/search` - Search issues with JQL
- `POST /rest/api/3/issues/search` - Search (alternative POST method)

**Projects**
- `GET /rest/api/3/project` - List projects
- `GET /rest/api/3/project/{projectIdOrKey}` - Get project details

**Users**
- `GET /rest/api/3/users/search` - Search users
- `GET /rest/api/3/user?accountId={id}` - Get user details
- `GET /rest/api/3/myself` - Get current user

**Workflows & Transitions**
- `GET /rest/api/3/issue/{issueIdOrKey}/transitions` - Get available transitions
- `POST /rest/api/3/issue/{issueIdOrKey}/transitions` - Transition issue

**Custom Fields**
- `GET /rest/api/3/field` - List all fields (including custom)
- `GET /rest/api/3/field/search` - Search for fields

**Webhooks**
- `GET /rest/api/3/webhook` - List webhooks
- `POST /rest/api/3/webhook` - Create webhook
- `DELETE /rest/api/3/webhook/{id}` - Delete webhook

### Step 4: Request Formats and Parameters

#### Search with JQL (JQL Query Language)

Most powerful way to query issues:

```bash
GET /rest/api/3/search?jql=project=PROJ AND status="In Progress"&maxResults=50
```

**JQL Examples**:
```
# Recent issues
project = PROJ AND created >= -7d

# Assigned to me
assignee = currentUser()

# Status workflow
status in (Open, "In Progress") AND updated >= -1d

# Custom fields (need field ID)
customfield_10014 = "Epic Name"

# Text search
summary ~ "bug fix" OR description ~ "critical"

# Complex filtering
(project = PROJ OR project = OTHER)
  AND status != Done
  AND priority >= High
  AND created >= 2024-01-01
```

**JQL Functions**:
- `currentUser()` - Current authenticated user
- `endOfDay()`, `startOfDay()` - Date functions
- `now()` - Current timestamp
- `issueFunction()` - Advanced scripting

#### Query Parameters

Common parameters for `/search`:
- `jql` - JQL query string
- `startAt` - Pagination start (default 0)
- `maxResults` - Items per page (default 50, max 100)
- `fields` - Comma-separated field names to return
- `expand` - Additional data to include (changelog, transitions)
- `orderBy` - Sort order (e.g., "created DESC")

```python
# Using JiraClient
issues = client.search_issues(
    jql="project = PROJ AND status = Open",
    startAt=0,
    maxResults=100,
    expand=["changelog"]
)
```

#### Create Issue Request

Request body for POST `/rest/api/3/issues`:

```json
{
  "fields": {
    "project": {"key": "PROJ"},
    "summary": "Issue summary",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Description text"}]
        }
      ]
    },
    "issuetype": {"name": "Task"},
    "assignee": {"accountId": "user-account-id"},
    "priority": {"name": "High"},
    "labels": ["bug", "urgent"]
  }
}
```

#### Update Issue Request

PUT `/rest/api/3/issue/{issueKey}`:

```json
{
  "fields": {
    "summary": "Updated summary",
    "description": {"type": "doc", "version": 1, "content": []},
    "priority": {"name": "Medium"},
    "assignee": {"accountId": "new-user-id"}
  }
}
```

### Step 5: Expansion and Field Selection

Use `expand` parameter to include additional data:

```bash
GET /rest/api/3/issue/PROJ-123?expand=changelog,transitions
```

**Common expansions**:
- `changelog` - Issue change history (required for state duration analysis)
- `transitions` - Available workflow transitions
- `editmeta` - Metadata about what fields can be edited
- `names` - Human-readable field names

**Field Selection** - Return only needed fields:
```bash
GET /rest/api/3/search?fields=key,summary,status,assignee&maxResults=100
```

### Step 6: Pagination

For large result sets, use pagination:

```python
start_at = 0
max_results = 50
all_issues = []

while True:
    issues = client.search_issues(
        jql="project = PROJ",
        startAt=start_at,
        maxResults=max_results
    )
    all_issues.extend(issues)

    if len(issues) < max_results:
        break
    start_at += max_results
```

Response includes pagination metadata:
```json
{
  "startAt": 0,
  "maxResults": 50,
  "total": 523,
  "isLast": false,
  "values": [...]
}
```

### Step 7: Atlassian Document Format (ADF)

Rich text content (descriptions, comments) uses ADF. The project's `JiraDocumentBuilder` simplifies this:

```python
from jira_tool.formatter import JiraDocumentBuilder

doc = JiraDocumentBuilder()
doc.add_heading("Title", level=1)
doc.add_paragraph(doc.bold("Key"), doc.add_text(": "), doc.add_text("Value"))
doc.add_bullet_list(["Item 1", "Item 2"])
doc.add_code_block("code content", language="python")
adf = doc.build()  # Returns ADF dict for API
```

**ADF Structure**:
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "heading",
      "attrs": {"level": 1},
      "content": [{"type": "text", "text": "Heading"}]
    },
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Paragraph"}]
    }
  ]
}
```

**Common ADF nodes**:
- `heading` - Headings (levels 1-6)
- `paragraph` - Text paragraphs
- `bulletList` / `orderedList` - Lists
- `codeBlock` - Code blocks
- `panel` - Info panels (info, note, warning, success, error)
- `blockquote` - Block quotes
- `table` - Tables

See references/reference.md for comprehensive ADF examples.

### Step 8: Error Handling and Status Codes

Common HTTP status codes:

| Code | Meaning | Handling |
|------|---------|----------|
| 200 | Success | Parse response normally |
| 201 | Created | Resource created successfully |
| 204 | No Content | Successful but empty response |
| 400 | Bad Request | Check request format/parameters |
| 401 | Unauthorized | Check authentication credentials |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Issue/resource doesn't exist |
| 429 | Too Many Requests | Rate limited - implement backoff |
| 500 | Server Error | Retry with exponential backoff |

**Error Response Format**:
```json
{
  "errorMessages": ["Error message"],
  "errors": {
    "fieldName": "Field-specific error"
  }
}
```

The `JiraClient` includes automatic retry logic for 429, 500, 502, 503, 504:
```python
client = JiraClient(max_retries=3)  # Automatic exponential backoff
```

### Step 9: Rate Limiting

Jira Cloud has rate limits:
- **Anonymous requests**: Limited
- **Authenticated**: Higher limits (typically 10 requests/second)
- **Header**: `X-RateLimit-*` headers in response

Check rate limit headers:
```python
response = client.session.get(url)
print(response.headers.get('X-RateLimit-Limit'))
print(response.headers.get('X-RateLimit-Remaining'))
print(response.headers.get('X-RateLimit-Reset'))
```

Best practices:
- Use `maxResults=100` in searches (fewer requests)
- Cache results when possible
- Implement exponential backoff on 429 (the client does this)
- Batch operations when possible

### Step 10: Custom Fields

Custom fields have IDs (e.g., `customfield_10014`). They vary per instance.

**Discover custom fields**:
```bash
GET /rest/api/3/field
```

```python
# Using JiraClient
fields = client.list_fields()
epic_field = client.get_epic_link_field()  # Auto-discovers common field IDs
```

**Use in queries and updates**:
```bash
# In JQL
GET /rest/api/3/search?jql=customfield_10014="Epic Name"

# In updates
PUT /rest/api/3/issue/PROJ-123
{
  "fields": {
    "customfield_10014": "Epic Name"
  }
}
```

### Step 11: Common Patterns and Recipes

**Create Issue Under Epic**:
```python
from jira_tool.formatter import JiraDocumentBuilder

doc = JiraDocumentBuilder()
doc.add_paragraph(doc.add_text("Issue description"))
adf = doc.build()

issue_data = {
    "fields": {
        "project": {"key": "PROJ"},
        "summary": "New issue",
        "description": adf,
        "issuetype": {"name": "Task"},
        "customfield_10014": "PROJ-1"  # Epic Link field
    }
}
response = client.create_issue(issue_data)
```

**Bulk Update Issues**:
```python
# Get issues
issues = client.search_issues(
    jql="project = PROJ AND status = Open",
    maxResults=100
)

# Update each
for issue in issues:
    client.update_issue(
        issue["key"],
        {"fields": {"priority": {"name": "High"}}}
    )
```

**Transition Workflow**:
```python
# Get available transitions
transitions = client.get_transitions("PROJ-123")

# Find the transition ID you want
for transition in transitions:
    if transition["name"] == "Done":
        transition_id = transition["id"]
        break

# Execute transition
client.transition_issue("PROJ-123", transition_id)
```

**Search and Export**:
```python
from jira_tool.analysis.formatters import format_as_csv

issues = client.search_issues(
    jql="project = PROJ AND created >= -7d",
    expand=["changelog"]
)

csv_output = format_as_csv(issues)
print(csv_output)
```

## Examples

### Example 1: Simple API Call - Get Issue

Using Jira REST API directly:
```bash
curl -X GET \
  "https://company.atlassian.net/rest/api/3/issue/PROJ-123" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

Using the project's client:
```python
from jira_tool.client import JiraClient

client = JiraClient()
issue = client.get_issue("PROJ-123")
print(f"Summary: {issue['fields']['summary']}")
print(f"Status: {issue['fields']['status']['name']}")
```

### Example 2: Advanced Search with JQL

Find all open bugs assigned to current user:
```bash
curl -X GET \
  "https://company.atlassian.net/rest/api/3/search" \
  -G --data-urlencode 'jql=project=PROJ AND type=Bug AND assignee=currentUser() AND status != Done' \
  -G --data-urlencode 'maxResults=100' \
  -G --data-urlencode 'expand=changelog' \
  -H "Authorization: Basic ..." \
  -H "Accept: application/json"
```

Using the client:
```python
from jira_tool.client import JiraClient

client = JiraClient()
issues = client.search_issues(
    jql='project = PROJ AND type = Bug AND assignee = currentUser() AND status != Done',
    maxResults=100,
    expand=['changelog']
)

for issue in issues:
    print(f"{issue['key']}: {issue['fields']['summary']}")
```

### Example 3: Create Issue with Rich Content

Create a detailed issue with formatted description:
```python
from jira_tool.client import JiraClient
from jira_tool.formatter import JiraDocumentBuilder

client = JiraClient()

# Build rich content
doc = JiraDocumentBuilder()
doc.add_heading("Issue Description", level=1)
doc.add_paragraph(doc.add_text("Background: "), doc.add_text("Detailed background"))
doc.add_heading("Steps to Reproduce", level=2)
doc.add_bullet_list([
    "Step 1",
    "Step 2",
    "Step 3"
])
doc.add_panel("error", doc.add_paragraph(doc.add_text("Expected error")))
adf_description = doc.build()

# Create issue
response = client.create_issue({
    "fields": {
        "project": {"key": "PROJ"},
        "summary": "Bug: Application crashes on login",
        "description": adf_description,
        "issuetype": {"name": "Bug"},
        "priority": {"name": "Highest"},
        "labels": ["critical", "regression"]
    }
})

print(f"Created issue: {response['key']}")
```

### Example 4: Analyze Issue State Durations

Use the project's state analyzer to track time in workflow states:
```python
from jira_tool.client import JiraClient
from jira_tool.analysis.state_analyzer import StateDurationAnalyzer

client = JiraClient()

# Search with changelog
issues = client.search_issues(
    jql="project = PROJ AND created >= -30d",
    expand=["changelog"]
)

# Analyze state transitions
analyzer = StateDurationAnalyzer()
durations = analyzer.analyze_issues(issues)

# Export results
csv_output = analyzer.format_as_csv(durations)
print(csv_output)
```

### Example 5: Handle Pagination

Efficiently fetch large result sets:
```python
from jira_tool.client import JiraClient

client = JiraClient()

start_at = 0
max_results = 50
total_fetched = 0
all_issues = []

while True:
    issues = client.search_issues(
        jql="project = PROJ",
        startAt=start_at,
        maxResults=max_results
    )

    all_issues.extend(issues)
    total_fetched += len(issues)

    # Check if we got fewer results than requested (last page)
    if len(issues) < max_results:
        break

    start_at += max_results
    print(f"Fetched {total_fetched} issues...")

print(f"Total issues: {total_fetched}")
```

## Requirements

- Python 3.8 or higher
- `requests` library (included in project)
- Valid Jira Cloud instance with REST API v3 access
- API token generated from Atlassian account settings
- Environment variables: `JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`

## See Also

- [reference.md](./references/reference.md) - Comprehensive API reference, ADF node types, webhook payloads, and field mappings
- [examples.md](./examples/examples.md) - Extended examples for complex scenarios, batch operations, and error handling
- Official Jira API Docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- Project JiraClient source: `src/jira_tool/client.py`
- Project ADF Builder: `src/jira_tool/formatter.py`
