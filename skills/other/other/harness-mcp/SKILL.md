---
name: harness-mcp
description: Harness MCP (Model Context Protocol) server integration for AI-powered CD operations, pipeline management, Git repositories, pull requests, code review comments, and bidirectional Jira synchronization
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
dependencies:
  - harness-cd
  - jira-orchestration
triggers:
  - harness mcp
  - harness ai
  - harness connector
  - harness pipeline
  - harness jira
  - harness git
  - harness pr
  - harness pull request
  - harness repository
  - harness comment
  - harness workspace
  - harness multi-repo
  - harness create repo
  - mcp server
  - cd automation
  - harness confluence
  - documentation sync
  - link confluence
  - readme docs
  - issue documentation
---

# Harness MCP Skill

AI-powered CD operations, Git repository and pull request management via Harness MCP Server.

## Prerequisites

### Environment Variables
```bash
export HARNESS_API_KEY="your-api-key"
export HARNESS_DEFAULT_ORG_ID="your-org-id"
export HARNESS_DEFAULT_PROJECT_ID="your-project-id"
export HARNESS_BASE_URL="https://app.harness.io"
export HARNESS_ACCOUNT_ID="your-account-id"
```

### API Token Generation
1. Navigate to **Account Settings > API Keys** in Harness UI
2. Click **+ API Key**
3. Set permissions (minimum: pipeline execution, connector management)
4. Store securely

## MCP Server Configuration

### Claude Code
```json
{
  "mcpServers": {
    "harness": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-harness"],
      "env": {
        "HARNESS_API_KEY": "${HARNESS_API_KEY}",
        "HARNESS_DEFAULT_ORG_ID": "${HARNESS_DEFAULT_ORG_ID}",
        "HARNESS_DEFAULT_PROJECT_ID": "${HARNESS_DEFAULT_PROJECT_ID}",
        "HARNESS_BASE_URL": "${HARNESS_BASE_URL}"
      }
    }
  }
}
```

### Docker
```bash
docker run -e HARNESS_API_KEY=$HARNESS_API_KEY \
           -e HARNESS_DEFAULT_ORG_ID=$HARNESS_DEFAULT_ORG_ID \
           -e HARNESS_DEFAULT_PROJECT_ID=$HARNESS_DEFAULT_PROJECT_ID \
           harness/mcp-server:latest
```

## Available MCP Tools

| Category | Tool | Purpose |
|----------|------|---------|
| **Connectors** | `harness_get_connector`, `harness_list_connectors`, `harness_get_connector_catalogue` | Manage connectors |
| **Pipelines** | `harness_list_pipelines`, `harness_get_pipeline`, `harness_trigger_pipeline` | Pipeline operations |
| **Executions** | `harness_get_execution`, `harness_list_executions`, `harness_get_execution_url` | Track executions |
| **Dashboards** | `harness_list_dashboards`, `harness_get_dashboard` | Dashboard data |
| **Repos** | `harness_get_repository`, `harness_list_repositories` | Repository management |
| **Pull Requests** | `harness_get_pull_request`, `harness_list_pull_requests`, `harness_create_pull_request`, `harness_get_pull_request_checks`, `harness_get_pull_request_activities` | PR operations |

## Git & Pull Request Workflows

### List Repositories
```python
repos = harness_list_repositories(
    org_id="${HARNESS_ORG_ID}",
    project_id="${HARNESS_PROJECT_ID}"
)
```

### Create Pull Request
```python
pr = harness_create_pull_request(
    repo_id="my-application",
    title="PROJ-123: Feature title",
    source_branch="feature/PROJ-123",
    target_branch="main",
    description="## Summary\nImplements feature.\n## Jira\n[PROJ-123](https://company.atlassian.net/browse/PROJ-123)"
)
```

### Get PR Activities (Comments, Reviews)
```python
activities = harness_get_pull_request_activities(repo_id="my-app", pr_number=42)
for activity in activities:
    if activity.type == "comment":
        print(f"Comment by {activity.author} at {activity.file_path}:{activity.line_number}")
    elif activity.type == "review":
        print(f"Review by {activity.author}: {activity.state}")
```

### Sync PR Comments to Jira
```python
activities = harness_get_pull_request_activities(repo_id="my-app", pr_number=42)
review_summary = []
for activity in activities:
    if activity.type == "review":
        review_summary.append(f"- **{activity.author}**: {activity.state}")

jira_add_comment(issue_key="PROJ-123",
    body=f"## PR Review\n**PR:** [#{42}]({pr.url})\n**Status:** {pr.state}\n\n" + "\n".join(review_summary))
```

### PR-to-Jira Status Mapping
```yaml
pr_sync:
  enabled: true
  jira_key_patterns:
    - title: "^([A-Z]+-\\d+)"
    - branch: "feature/([A-Z]+-\\d+)"
  transitions:
    pr_created: { transition: "In Review", comment: "PR created: {pr_url}" }
    pr_approved: { transition: "Approved", comment: "PR approved by {approver}" }
    pr_merged: { transition: "Done", comment: "PR merged to {target_branch}" }
  fields:
    pr_url: "customfield_10200"
    pr_status: "customfield_10201"
    reviewers: "customfield_10202"
```

## Jira Connector Setup

### Create Connector
```yaml
connector:
  name: jira-connector
  identifier: jira_connector
  type: Jira
  spec:
    jiraUrl: https://your-company.atlassian.net
    auth:
      type: UsernamePassword
      spec:
        username: your.email@company.com
        passwordRef: jira_api_token
    delegateSelectors:
      - delegate-name
```

**Required Scopes:** `read:jira-user`, `read:jira-work`, `write:jira-work`

### Jira Create Step in Pipeline
```yaml
- step:
    name: Create Jira Issue
    type: JiraCreate
    spec:
      connectorRef: jira_connector
      projectKey: PROJ
      issueType: Task
      fields:
        - name: Summary
          value: "Deployment: <+pipeline.name> - <+pipeline.sequenceId>"
        - name: Priority
          value: Medium
```

### Jira Update Step
```yaml
- step:
    name: Update Jira Issue
    type: JiraUpdate
    spec:
      connectorRef: jira_connector
      issueKey: <+pipeline.variables.jiraIssueKey>
      fields:
        - name: Status
          value: Done
      transitionTo:
        transitionName: Done
        status: Done
```

### Jira Approval Step
```yaml
- step:
    name: Jira Approval
    type: JiraApproval
    spec:
      connectorRef: jira_connector
      issueKey: <+pipeline.variables.jiraIssueKey>
      approvalCriteria:
        matchAnyCondition: true
        conditions:
          - key: Status
            operator: equals
            value: Approved
```

## Integration with Jira Orchestrator

### Configuration
```yaml
harness:
  account:
    account_id: "${HARNESS_ACCOUNT_ID}"
    org_id: "${HARNESS_ORG_ID}"
    project_id: "${HARNESS_PROJECT_ID}"
  api:
    base_url: "https://app.harness.io"
    api_key: "${HARNESS_API_KEY}"
  mcp:
    enabled: true
    tools:
      - harness_get_connector
      - harness_list_pipelines
      - harness_get_execution
  jira_connector_ref: "jira_connector"
  sync:
    auto_create_issues: true
    auto_transition: true
    environments:
      dev: "In Development"
      staging: "In QA"
      prod: "Released"
```

### MCP Tool Usage
```python
connector = harness_get_connector(connector_id="jira_connector", org_id="default", project_id="my_project")
executions = harness_list_executions(pipeline_id="deploy_pipeline", limit=10)
execution = harness_get_execution(execution_id="abc123", org_id="default", project_id="my_project")
```

## REST API for PR Operations

### Base URL
```bash
HARNESS_CODE_API="${HARNESS_BASE_URL}/code/api/v1"
```

### Authentication
```bash
curl -H "x-api-key: ${HARNESS_API_KEY}" \
     -H "Content-Type: application/json" \
     "${HARNESS_CODE_API}/repos/{repo-ref}/pullreq/{pr-number}/comments"
```

### Key Endpoints
| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create Comment | POST | `/v1/repos/{repo}/pullreq/{pr}/comments` |
| Create Code Comment | POST | `/v1/repos/{repo}/pullreq/{pr}/comments` (with `path`, `line_start`, `line_end`) |
| Submit Review | POST | `/v1/repos/{repo}/pullreq/{pr}/reviews` |
| Add Reviewer | POST | `/v1/repos/{repo}/pullreq/{pr}/reviewers` |
| Merge PR | POST | `/v1/repos/{repo}/pullreq/{pr}/merge` |

### Create General Comment
```bash
curl -X POST "${HARNESS_CODE_API}/repos/${REPO}/pullreq/${PR}/comments" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"text": "Great work!"}'
```

### Create Code Comment
```bash
curl -X POST "${HARNESS_CODE_API}/repos/${REPO}/pullreq/${PR}/comments" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Consider adding null check",
    "path": "src/auth.ts",
    "line_start": 42,
    "line_end": 45,
    "line_start_new": true,
    "line_end_new": true
  }'
```

### Submit Review
```bash
curl -X POST "${HARNESS_CODE_API}/repos/${REPO}/pullreq/${PR}/reviews" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"commit_sha": "abc123", "decision": "approved"}'
```

**Decision Values:** `approved`, `changereq`, `reviewed`

### Merge PR
```bash
curl -X POST "${HARNESS_CODE_API}/repos/${REPO}/pullreq/${PR}/merge" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "squash",
    "source_sha": "abc123",
    "title": "feat: Add auth",
    "delete_source_branch": true
  }'
```

**Merge Methods:** `merge`, `squash`, `rebase`, `fast-forward`

## Bash Helper Functions

```bash
export HARNESS_CODE_API="${HARNESS_BASE_URL:-https://app.harness.io}/code/api/v1"

harness_pr_comment() {
  local repo="$1" pr="$2" text="$3"
  curl -s -X POST "${HARNESS_CODE_API}/repos/${repo}/pullreq/${pr}/comments" \
    -H "x-api-key: ${HARNESS_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"${text}\"}"
}

harness_pr_approve() {
  local repo="$1" pr="$2" commit_sha="$3"
  curl -s -X POST "${HARNESS_CODE_API}/repos/${repo}/pullreq/${pr}/reviews" \
    -H "x-api-key: ${HARNESS_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"commit_sha\": \"${commit_sha}\", \"decision\": \"approved\"}"
}

harness_pr_merge() {
  local repo="$1" pr="$2" method="${3:-squash}" source_sha="$4" title="$5"
  curl -s -X POST "${HARNESS_CODE_API}/repos/${repo}/pullreq/${pr}/merge" \
    -H "x-api-key: ${HARNESS_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"method\": \"${method}\", \"source_sha\": \"${source_sha}\", \"title\": \"${title}\", \"delete_source_branch\": true}"
}
```

## Python Client

```python
import requests, os
from typing import Optional, Literal

class HarnessCodeAPI:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.environ.get("HARNESS_API_KEY")
        self.base_url = base_url or os.environ.get("HARNESS_BASE_URL", "https://app.harness.io")
        self.api_url = f"{self.base_url}/code/api/v1"
        self.headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

    def create_comment(self, repo: str, pr_number: int, text: str, path: Optional[str] = None,
                      line_start: Optional[int] = None, line_end: Optional[int] = None,
                      parent_id: Optional[int] = None) -> dict:
        url = f"{self.api_url}/repos/{repo}/pullreq/{pr_number}/comments"
        data = {"text": text}
        if parent_id:
            data["parent_id"] = parent_id
        elif path and line_start:
            data.update({"path": path, "line_start": line_start, "line_end": line_end or line_start,
                        "line_start_new": True, "line_end_new": True})
        return requests.post(url, headers=self.headers, json=data).json()

    def submit_review(self, repo: str, pr_number: int, commit_sha: str,
                     decision: Literal["approved", "changereq", "reviewed"]) -> dict:
        url = f"{self.api_url}/repos/{repo}/pullreq/{pr_number}/reviews"
        data = {"commit_sha": commit_sha, "decision": decision}
        return requests.post(url, headers=self.headers, json=data).json()

    def approve(self, repo: str, pr_number: int, commit_sha: str) -> dict:
        return self.submit_review(repo, pr_number, commit_sha, "approved")

    def merge(self, repo: str, pr_number: int, source_sha: str,
             method: Literal["merge", "squash", "rebase", "fast-forward"] = "squash",
             title: Optional[str] = None, delete_source_branch: bool = True,
             dry_run: bool = False) -> dict:
        url = f"{self.api_url}/repos/{repo}/pullreq/{pr_number}/merge"
        data = {"method": method, "source_sha": source_sha, "delete_source_branch": delete_source_branch, "dry_run": dry_run}
        if title:
            data["title"] = title
        return requests.post(url, headers=self.headers, json=data).json()
```

## Multi-Repository Workspace Support

### Configuration
```yaml
harness:
  workspace:
    repositories:
      - identifier: frontend-app
        path: ./frontend
        jira_project: FRONT
      - identifier: backend-api
        path: ./backend
        jira_project: BACK
    auto_create_repos: true
    default_branch: main
  review:
    cross_repo_review: true
  jira:
    sync_enabled: true
    aggregate_prs: true
```

### Python API
```python
from lib.harness_code_api import HarnessCodeAPI

client = HarnessCodeAPI()
repos = client.setup_workspace_repos([
    {"identifier": "frontend", "path": "./frontend"},
    {"identifier": "backend", "path": "./backend"}
])
prs = client.get_workspace_prs(repo_identifiers=["frontend", "backend"], state="open", jira_key="PROJ-123")
```

## Repository Creation

### Python
```python
repo = client.create_repository(
    identifier="my-service",
    description="User management service",
    default_branch="main",
    is_public=False,
    readme=True,
    license="MIT"
)
```

### REST API
| Operation | Method | Endpoint |
|-----------|--------|----------|
| List Repos | GET | `/v1/repos` |
| Get Repo | GET | `/v1/repos/{repo}` |
| Create Repo | POST | `/v1/repos` |
| Update Repo | PATCH | `/v1/repos/{repo}` |
| Delete Repo | DELETE | `/v1/repos/{repo}` |

## Confluence Documentation Integration

### Auto-Documentation
```python
from lib.confluence_doc_linker import ConfluenceDocLinker

linker = ConfluenceDocLinker()
docs = linker.ensure_issue_docs("PROJ-123")
linker.link_readme_to_confluence(readme_path="./README.md", jira_key="PROJ-123")
```

### Configuration
```yaml
documentation:
  confluence:
    base_url: "${CONFLUENCE_BASE_URL}"
    space_key: "ENG"
  auto_create:
    enabled: true
    on_work_start: true
  readme:
    auto_update: true
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Invalid API Key | Regenerate in Harness UI |
| Network timeout | Check delegate connectivity |
| Permission denied | Verify API key permissions |
| Jira unreachable | Check firewall/proxy |

### Debug Logging
```bash
export HARNESS_LOG_LEVEL=debug
export MCP_DEBUG=true
```

## Best Practices

1. Use Harness Secrets for credentials
2. Select delegates with direct Jira network access
3. Configure error handling with retries
4. Enable logging for all operations
5. Scope API tokens to minimum permissions

## Related Resources

- [Harness MCP Server](https://developer.harness.io/docs/platform/harness-aida/harness-mcp-server/)
- [Harness Code Repository](https://developer.harness.io/docs/code-repository/)
- [PR Review](https://developer.harness.io/docs/code-repository/pull-requests/review-pr/)
- [PR Merge](https://developer.harness.io/docs/code-repository/pull-requests/merge-pr/)
- [Jira Connector Setup](https://developer.harness.io/docs/platform/connectors/ticketing-systems/connect-to-jira/)
- [Jira Steps in CD](https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/cd-steps/ticketing-systems/create-jira-issues-in-cd-stages/)
