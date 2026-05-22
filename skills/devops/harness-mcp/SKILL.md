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

Comprehensive Harness MCP (Model Context Protocol) server integration for AI-powered CD operations, Git repository management, and pull request workflows with the Jira Orchestrator.

## Overview

The Harness MCP Server enables AI agents to interact with Harness tools using a unified protocol, providing endpoints for:
- **Connectors**: Get details, list catalogue, list with filtering
- **Pipelines**: List, get details, trigger executions
- **Executions**: Get details, list, fetch URLs
- **Dashboards**: List all, retrieve specific data
- **Repositories**: List, get details, track changes
- **Pull Requests**: Create, list, get details, track status checks
- **PR Activities**: Get comments, reviews, and activities

## Prerequisites

### Environment Variables

```bash
# Required Harness Configuration
export HARNESS_API_KEY="your-harness-api-key"
export HARNESS_DEFAULT_ORG_ID="your-org-id"
export HARNESS_DEFAULT_PROJECT_ID="your-project-id"
export HARNESS_BASE_URL="https://app.harness.io"  # Optional, defaults to this
export HARNESS_ACCOUNT_ID="your-account-id"
```

### Harness API Token Generation

1. Navigate to **Account Settings > API Keys** in Harness UI
2. Click **+ API Key** to create a new token
3. Set appropriate permissions (minimum: pipeline execution, connector management)
4. Copy the token and store securely

## MCP Server Configuration

### Claude Code Configuration

Add Harness MCP to your Claude Code configuration:

```json
{
  "mcpServers": {
    "harness": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/mcp-harness"
      ],
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

### Docker Configuration

```bash
docker run -e HARNESS_API_KEY=$HARNESS_API_KEY \
           -e HARNESS_DEFAULT_ORG_ID=$HARNESS_DEFAULT_ORG_ID \
           -e HARNESS_DEFAULT_PROJECT_ID=$HARNESS_DEFAULT_PROJECT_ID \
           harness/mcp-server:latest
```

### VS Code / Cursor Configuration

```json
{
  "mcp.servers": {
    "harness": {
      "command": "npx",
      "args": ["-y", "@harness/mcp-server"],
      "env": {
        "HARNESS_API_KEY": "${env:HARNESS_API_KEY}",
        "HARNESS_DEFAULT_ORG_ID": "${env:HARNESS_DEFAULT_ORG_ID}",
        "HARNESS_DEFAULT_PROJECT_ID": "${env:HARNESS_DEFAULT_PROJECT_ID}"
      }
    }
  }
}
```

## Available MCP Tools

### Connector Management

| Tool | Description |
|------|-------------|
| `harness_get_connector` | Get details of a specific connector |
| `harness_list_connectors` | List all connectors with filtering |
| `harness_get_connector_catalogue` | Get available connector types |

### Pipeline Operations

| Tool | Description |
|------|-------------|
| `harness_list_pipelines` | List pipelines in project |
| `harness_get_pipeline` | Get pipeline details and YAML |
| `harness_trigger_pipeline` | Trigger pipeline execution |

### Execution Tracking

| Tool | Description |
|------|-------------|
| `harness_get_execution` | Get execution details |
| `harness_list_executions` | List recent executions |
| `harness_get_execution_url` | Get execution dashboard URL |

### Dashboard Functions

| Tool | Description |
|------|-------------|
| `harness_list_dashboards` | List all dashboards |
| `harness_get_dashboard` | Get specific dashboard data |

### Repository Operations

| Tool | Description |
|------|-------------|
| `harness_get_repository` | Get details of a specific repository |
| `harness_list_repositories` | List all repositories in project |

### Pull Request Operations

| Tool | Description |
|------|-------------|
| `harness_get_pull_request` | Get details of a specific pull request |
| `harness_list_pull_requests` | List pull requests in a repository |
| `harness_create_pull_request` | Create a new pull request |
| `harness_get_pull_request_checks` | Get status checks for a PR |
| `harness_get_pull_request_activities` | Get comments and activities for a PR |

## Git & Pull Request Workflows

### Repository Management

```python
# List all repositories
repos = harness_list_repositories(
    org_id="${HARNESS_ORG_ID}",
    project_id="${HARNESS_PROJECT_ID}"
)

# Get specific repository details
repo = harness_get_repository(
    repo_id="my-application",
    org_id="${HARNESS_ORG_ID}",
    project_id="${HARNESS_PROJECT_ID}"
)
```

### Creating Pull Requests

```python
# Create a PR linked to a Jira issue
pr = harness_create_pull_request(
    repo_id="my-application",
    title="PROJ-123: Implement user authentication",
    source_branch="feature/PROJ-123-user-auth",
    target_branch="main",
    description="""
    ## Summary
    Implements user authentication feature.

    ## Jira Issue
    [PROJ-123](https://company.atlassian.net/browse/PROJ-123)

    ## Changes
    - Added login/logout endpoints
    - Implemented JWT token handling
    - Added authentication middleware
    - Unit tests included

    ## Testing
    - [x] Unit tests passing
    - [x] Integration tests passing
    - [ ] Manual testing required
    """
)

print(f"PR created: {pr.url}")
```

### Monitoring PR Status

```python
# Get PR details
pr = harness_get_pull_request(
    repo_id="my-application",
    pr_number=42
)

print(f"PR Status: {pr.state}")
print(f"Mergeable: {pr.mergeable}")
print(f"Conflicts: {pr.has_conflicts}")

# Get status checks (pipeline results)
checks = harness_get_pull_request_checks(
    repo_id="my-application",
    pr_number=42
)

for check in checks:
    print(f"  {check.name}: {check.status}")
```

### Retrieving PR Comments & Activities

```python
# Get all activities (comments, reviews, status changes)
activities = harness_get_pull_request_activities(
    repo_id="my-application",
    pr_number=42
)

for activity in activities:
    if activity.type == "comment":
        print(f"Comment by {activity.author}:")
        print(f"  File: {activity.file_path}:{activity.line_number}")
        print(f"  Body: {activity.body}")

    elif activity.type == "review":
        print(f"Review by {activity.author}: {activity.state}")
        # States: APPROVED, CHANGES_REQUESTED, COMMENTED

    elif activity.type == "status_change":
        print(f"Status changed to: {activity.new_status}")
```

### Syncing PR Activities to Jira

```python
# Sync PR comments to Jira
activities = harness_get_pull_request_activities(
    repo_id="my-application",
    pr_number=42
)

# Build summary for Jira comment
review_summary = []
for activity in activities:
    if activity.type == "review":
        review_summary.append(
            f"- **{activity.author}**: {activity.state}"
        )
    elif activity.type == "comment":
        review_summary.append(
            f"- Comment on `{activity.file_path}`: {activity.body[:100]}..."
        )

# Add summary to Jira
jira_add_comment(
    issue_key="PROJ-123",
    body=f"""
    ## PR Review Update

    **PR:** [#42 - Implement user auth]({pr.url})
    **Status:** {pr.state}

    ### Reviews & Comments
    {chr(10).join(review_summary)}
    """
)
```

### PR-to-Jira Status Mapping

Configure automatic status transitions based on PR events:

```yaml
# .jira/pr-sync.yml
pr_sync:
  enabled: true

  # Extract Jira keys from PR metadata
  jira_key_patterns:
    - title: "^([A-Z]+-\\d+)"          # PROJ-123: Title
    - branch: "feature/([A-Z]+-\\d+)"   # feature/PROJ-123
    - branch: "bugfix/([A-Z]+-\\d+)"    # bugfix/PROJ-456

  # Map PR events to Jira transitions
  transitions:
    pr_created:
      transition: "In Review"
      comment: "Pull request created: {pr_url}"

    pr_approved:
      transition: "Approved"
      comment: "PR approved by {approver}"

    pr_changes_requested:
      transition: "In Progress"
      comment: "Changes requested by {reviewer}"

    pr_merged:
      transition: "Done"
      comment: "PR merged to {target_branch}"

    pr_closed:
      transition: "Cancelled"
      comment: "PR closed without merging"

  # Fields to update
  fields:
    pr_url: "customfield_10200"
    pr_status: "customfield_10201"
    reviewers: "customfield_10202"
```

### Code Review Commenting Patterns

```python
# When a reviewer adds comments, sync to Jira
def sync_review_comments_to_jira(repo_id, pr_number, jira_key):
    activities = harness_get_pull_request_activities(
        repo_id=repo_id,
        pr_number=pr_number
    )

    # Group comments by file
    comments_by_file = {}
    for activity in activities:
        if activity.type == "comment":
            file = activity.file_path
            if file not in comments_by_file:
                comments_by_file[file] = []
            comments_by_file[file].append({
                "line": activity.line_number,
                "author": activity.author,
                "body": activity.body,
                "resolved": activity.resolved
            })

    # Format for Jira
    jira_body = "## Code Review Comments\n\n"
    for file, comments in comments_by_file.items():
        jira_body += f"### `{file}`\n"
        for c in comments:
            status = "✅" if c["resolved"] else "💬"
            jira_body += f"- {status} Line {c['line']} ({c['author']}): {c['body']}\n"

    jira_add_comment(issue_key=jira_key, body=jira_body)
```

## Jira Connector Setup in Harness

### Step 1: Navigate to Connectors

1. Go to **Project Setup** > **Connectors**
2. Click **+ New Connector**
3. Select **Jira** under Ticketing Systems

### Step 2: Configure Basic Settings

```yaml
connector:
  name: jira-connector
  identifier: jira_connector
  orgIdentifier: default
  projectIdentifier: your_project
  type: Jira
  spec:
    jiraUrl: https://your-company.atlassian.net
```

### Step 3: Authentication Options

#### Option A: Username + API Key (Recommended for Cloud)

```yaml
spec:
  jiraUrl: https://your-company.atlassian.net
  auth:
    type: UsernamePassword
    spec:
      username: your.email@company.com
      passwordRef: jira_api_token  # Harness secret reference
```

**Required Scopes:**
- `read:jira-user`
- `read:jira-work`
- `write:jira-work`

#### Option B: Personal Access Token (Jira Server/Data Center)

```yaml
spec:
  jiraUrl: https://jira.internal.company.com
  delegateSelectors:
    - delegate-name
  auth:
    type: PersonalAccessToken
    spec:
      patRef: jira_pat_secret  # Harness secret reference
```

**Note:** Requires Harness Delegate version 78707+

#### Option C: OAuth (Advanced)

```yaml
spec:
  jiraUrl: https://api.atlassian.com/ex/jira/{cloud_id}
  auth:
    type: OAuth
    spec:
      clientId: your_oauth_client_id
      clientSecretRef: oauth_secret
      tokenEndpoint: https://auth.atlassian.com/oauth/token
```

### Step 4: Configure Delegate

Select Harness Delegates that have network access to your Jira instance:

```yaml
spec:
  delegateSelectors:
    - primary-delegate
    - backup-delegate
```

### Step 5: Test Connection

Click **Save and Continue** - Harness automatically tests the connection.

## Using Jira Steps in Pipelines

### Jira Create Step

```yaml
- step:
    name: Create Jira Issue
    identifier: createJiraIssue
    type: JiraCreate
    timeout: 5m
    spec:
      connectorRef: jira_connector
      projectKey: PROJ
      issueType: Task
      fields:
        - name: Summary
          value: "Deployment: <+pipeline.name> - <+pipeline.sequenceId>"
        - name: Description
          value: |
            Deployment triggered by: <+pipeline.triggeredBy.name>
            Environment: <+env.name>
            Service: <+service.name>
            Artifact: <+artifact.image>
        - name: Priority
          value: Medium
        - name: Labels
          value: ["deployment", "automation", "<+env.name>"]
```

### Jira Update Step

```yaml
- step:
    name: Update Jira Issue
    identifier: updateJiraIssue
    type: JiraUpdate
    timeout: 5m
    spec:
      connectorRef: jira_connector
      issueKey: <+pipeline.variables.jiraIssueKey>
      fields:
        - name: Status
          value: Done
        - name: customfield_10100
          value: <+artifact.tag>
      transitionTo:
        transitionName: Done
        status: Done
```

### Jira Approval Step

```yaml
- step:
    name: Jira Approval
    identifier: jiraApproval
    type: JiraApproval
    timeout: 1d
    spec:
      connectorRef: jira_connector
      projectKey: PROJ
      issueKey: <+pipeline.variables.jiraIssueKey>
      approvalCriteria:
        type: KeyValues
        spec:
          matchAnyCondition: true
          conditions:
            - key: Status
              operator: equals
              value: Approved
      rejectionCriteria:
        type: KeyValues
        spec:
          matchAnyCondition: true
          conditions:
            - key: Status
              operator: equals
              value: Rejected
```

## Integration with Jira Orchestrator

### Automatic Deployment Tracking

The `harness-jira-sync` agent automatically:
1. Extracts Jira issue keys from pipeline tags
2. Updates Jira with deployment status
3. Transitions issues based on deployment events
4. Records artifact versions and environment info

### Configuration

Add to `.jira/config.yml`:

```yaml
harness:
  account:
    account_id: "${HARNESS_ACCOUNT_ID}"
    org_id: "${HARNESS_ORG_ID}"
    project_id: "${HARNESS_PROJECT_ID}"
  api:
    base_url: "https://app.harness.io"
    api_key: "${HARNESS_API_KEY}"

  # MCP Integration
  mcp:
    enabled: true
    tools:
      - harness_get_connector
      - harness_list_pipelines
      - harness_get_execution
      - harness_list_executions

  # Jira Connector Reference
  jira_connector_ref: "jira_connector"

  # Sync Configuration
  sync:
    auto_create_issues: true
    auto_transition: true
    environments:
      dev: "In Development"
      staging: "In QA"
      prod: "Released"
```

### MCP Tool Usage Examples

```python
# Get Jira connector details
connector = harness_get_connector(
    connector_id="jira_connector",
    org_id="default",
    project_id="my_project"
)

# List recent pipeline executions
executions = harness_list_executions(
    pipeline_id="deploy_pipeline",
    limit=10
)

# Get specific execution details
execution = harness_get_execution(
    execution_id="abc123",
    org_id="default",
    project_id="my_project"
)
```

## Troubleshooting

### Connection Issues

| Issue | Solution |
|-------|----------|
| API Key invalid | Regenerate token in Harness UI |
| Network timeout | Check delegate connectivity |
| Permission denied | Verify API key permissions |
| Jira unreachable | Check firewall/proxy settings |

### Common Errors

```
Error: INVALID_CREDENTIAL
Solution: Verify HARNESS_API_KEY is correct and not expired

Error: DELEGATE_NOT_AVAILABLE
Solution: Ensure delegate is running and selected in connector

Error: JIRA_AUTHENTICATION_FAILED
Solution: Verify Jira credentials (email + API token or PAT)
```

### Debug Logging

Enable verbose logging:

```bash
export HARNESS_LOG_LEVEL=debug
export MCP_DEBUG=true
```

## Best Practices

1. **Use Secrets Management**: Store all credentials in Harness Secrets
2. **Delegate Selection**: Use delegates with direct network access to Jira
3. **Error Handling**: Configure retry strategies for transient failures
4. **Audit Trail**: Enable logging for all Jira operations
5. **Least Privilege**: Scope API tokens to minimum required permissions

## Multi-Repository Workspace Support

The Jira orchestrator supports VS Code workspaces with multiple repositories, enabling coordinated operations across all repos linked to a Jira issue.

### Workspace Detection

The system automatically detects repositories in:

1. **VS Code Workspace File** (`.code-workspace`)
2. **Git Repositories** in the current directory tree
3. **Git Submodules** in the main repository

### Configuration

Create `.jira/harness-workspace.yml` in your workspace root:

```yaml
harness:
  workspace:
    # Repositories in this workspace
    repositories:
      - identifier: frontend-app
        path: ./frontend
        jira_project: FRONT
        description: "React frontend application"

      - identifier: backend-api
        path: ./backend
        jira_project: BACK
        description: "Node.js API backend"

      - identifier: shared-libs
        path: ./libs
        jira_project: SHARED
        description: "Shared TypeScript libraries"

    # Auto-create repos if they don't exist
    auto_create_repos: true

    # Default branch for all repos
    default_branch: main

  # PR review settings
  review:
    # Review all PRs across workspace
    cross_repo_review: true

    # Auto-approve thresholds
    auto_approve:
      enabled: false
      max_files: 5
      excluded_patterns:
        - "*.md"
        - "*.txt"

  # Jira integration
  jira:
    sync_enabled: true
    aggregate_prs: true  # Show all PRs in single Jira comment
```

### Python API for Workspace Operations

```python
from lib.harness_code_api import HarnessCodeAPI

client = HarnessCodeAPI()

# Setup workspace repos (creates if missing)
repos = client.setup_workspace_repos([
    {"identifier": "frontend", "description": "React frontend", "path": "./frontend"},
    {"identifier": "backend", "description": "API backend", "path": "./backend"},
    {"identifier": "shared", "description": "Shared libs", "path": "./libs"}
])

# Get all PRs across workspace for a Jira issue
prs = client.get_workspace_prs(
    repo_identifiers=["frontend", "backend", "shared"],
    state="open",
    jira_key="PROJ-123"
)

# Review all PRs in workspace
results = client.review_workspace_prs(
    repo_identifiers=["frontend", "backend", "shared"],
    jira_key="PROJ-123",
    auto_approve=False
)
```

### Bash Functions for Workspace

```bash
source lib/harness-code-api.sh

# Detect repos in VS Code workspace
harness_detect_workspace_repos

# Show status of all workspace repos
harness_workspace_status

# Create PRs for all changed repos
harness_workspace_create_prs "PROJ-123" "main"
```

---

## Repository Creation

Create repositories programmatically via the Harness Code REST API.

### Create Repository via Python

```python
from lib.harness_code_api import HarnessCodeAPI

client = HarnessCodeAPI()

# Create a new repository
repo = client.create_repository(
    identifier="my-new-service",
    description="Microservice for user management",
    default_branch="main",
    is_public=False,
    readme=True,
    license="MIT",
    gitignore="Node"
)

print(f"Created: {repo['identifier']}")
```

### Create Repository via Bash

```bash
source lib/harness-code-api.sh

# Create repository
harness_create_repo "my-service" "User management service" "main" "false"
```

### Ensure Repository Exists

The `ensure_repository_exists` method checks if a repo exists and creates it if not:

```python
# Will get existing or create new
repo = client.ensure_repository_exists(
    identifier="my-service",
    description="My service description"
)
```

### REST API for Repository Operations

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List Repos | GET | `/v1/repos` or `/v1/spaces/{space}/repos` |
| Get Repo | GET | `/v1/repos/{repo}` |
| Create Repo | POST | `/v1/repos` |
| Update Repo | PATCH | `/v1/repos/{repo}` |
| Delete Repo | DELETE | `/v1/repos/{repo}` |

### Create Repository Request Body

```json
{
  "identifier": "my-repo",
  "description": "Repository description",
  "default_branch": "main",
  "is_public": false,
  "parent_ref": "my-space",
  "readme": true,
  "license": "MIT",
  "gitignore": "Node"
}
```

---

## Harness REST API for PR Comments & Reviews

The Harness MCP Server provides **read** operations for PR activities, but for **write** operations (creating comments, submitting reviews, merging), use the Harness Code REST API directly.

### API Base URL

```bash
# Harness Code API (Gitness-based)
HARNESS_CODE_API="${HARNESS_BASE_URL}/code/api/v1"

# For Harness SaaS
HARNESS_CODE_API="https://app.harness.io/code/api/v1"
```

### Authentication

```bash
# All requests require the x-api-key header
curl -H "x-api-key: ${HARNESS_API_KEY}" \
     -H "Content-Type: application/json" \
     "${HARNESS_CODE_API}/repos/{repo-ref}/pullreq/{pr-number}/comments"
```

### REST API Endpoints for PR Operations

| Operation | Method | Endpoint |
|-----------|--------|----------|
| **Create Comment** | POST | `/v1/repos/{repo-ref}/pullreq/{pr-number}/comments` |
| **Update Comment** | PATCH | `/v1/repos/{repo-ref}/pullreq/{pr-number}/comments/{comment-id}` |
| **Delete Comment** | DELETE | `/v1/repos/{repo-ref}/pullreq/{pr-number}/comments/{comment-id}` |
| **Apply Suggestions** | POST | `/v1/repos/{repo-ref}/pullreq/{pr-number}/comments/apply-suggestions` |
| **Submit Review** | POST | `/v1/repos/{repo-ref}/pullreq/{pr-number}/reviews` |
| **Add Reviewer** | POST | `/v1/repos/{repo-ref}/pullreq/{pr-number}/reviewers` |
| **Merge PR** | POST | `/v1/repos/{repo-ref}/pullreq/{pr-number}/merge` |

---

### Creating PR Comments

#### General Comment (Conversation)

```bash
# Add a general comment to a PR
curl -X POST "${HARNESS_CODE_API}/repos/${REPO_REF}/pullreq/${PR_NUMBER}/comments" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great work on this implementation! A few suggestions below."
  }'
```

#### Code Comment (Inline on specific lines)

```bash
# Add a comment on specific lines of code
curl -X POST "${HARNESS_CODE_API}/repos/${REPO_REF}/pullreq/${PR_NUMBER}/comments" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Consider using a constant here for better maintainability.",
    "path": "src/services/auth.ts",
    "line_start": 42,
    "line_end": 45,
    "line_start_new": true,
    "line_end_new": true,
    "source_commit_sha": "abc123...",
    "target_commit_sha": "def456..."
  }'
```

#### Reply to Existing Comment

```bash
# Reply to an existing comment thread
curl -X POST "${HARNESS_CODE_API}/repos/${REPO_REF}/pullreq/${PR_NUMBER}/comments" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Good point, I will update this.",
    "parent_id": 12345
  }'
```

#### Comment Request Body Schema

```json
{
  "text": "string (required) - The comment content (Markdown supported)",
  "parent_id": "number (optional) - Parent comment ID for replies",
  "path": "string (optional) - File path for code comments",
  "line_start": "number (optional) - Starting line number",
  "line_end": "number (optional) - Ending line number",
  "line_start_new": "boolean - true=new file side, false=old file side",
  "line_end_new": "boolean - true=new file side, false=old file side",
  "source_commit_sha": "string (optional) - Source commit for code comments",
  "target_commit_sha": "string (optional) - Target commit for code comments"
}
```

---

### Submitting Reviews

#### Approve PR

```bash
# Approve the pull request
curl -X POST "${HARNESS_CODE_API}/repos/${REPO_REF}/pullreq/${PR_NUMBER}/reviews" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "commit_sha": "abc123def456...",
    "decision": "approved"
  }'
```

#### Request Changes

```bash
# Request changes on the pull request
curl -X POST "${HARNESS_CODE_API}/repos/${REPO_REF}/pullreq/${PR_NUMBER}/reviews" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "commit_sha": "abc123def456...",
    "decision": "changereq"
  }'
```

#### Comment-Only Review

```bash
# Submit a review without approval decision
curl -X POST "${HARNESS_CODE_API}/repos/${REPO_REF}/pullreq/${PR_NUMBER}/reviews" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "commit_sha": "abc123def456...",
    "decision": "reviewed"
  }'
```

#### Review Decision Types

| Decision | Description |
|----------|-------------|
| `approved` | Approve the PR for merge |
| `changereq` | Request changes before merge |
| `reviewed` | Mark as reviewed without approval/rejection |

---

### Adding Reviewers

```bash
# Add a reviewer to the PR
curl -X POST "${HARNESS_CODE_API}/repos/${REPO_REF}/pullreq/${PR_NUMBER}/reviewers" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "reviewer_id": 12345
  }'
```

---

### Merging Pull Requests

```bash
# Merge the pull request
curl -X POST "${HARNESS_CODE_API}/repos/${REPO_REF}/pullreq/${PR_NUMBER}/merge" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "squash",
    "source_sha": "abc123def456...",
    "title": "feat: Add user authentication (PR #42)",
    "message": "Implements user authentication with JWT tokens.\n\nCloses PROJ-123",
    "delete_source_branch": true,
    "bypass_rules": false,
    "dry_run": false
  }'
```

#### Merge Methods

| Method | Description |
|--------|-------------|
| `merge` | Create a merge commit |
| `squash` | Squash all commits into one |
| `rebase` | Rebase commits onto target |
| `fast-forward` | Fast-forward merge (if possible) |

#### Merge Options

| Option | Description |
|--------|-------------|
| `dry_run` | Test mergeability without merging |
| `dry_run_rules` | Validate branch protection rules |
| `bypass_rules` | Bypass protection rules (requires permission) |
| `delete_source_branch` | Delete source branch after merge |

---

### Bash Helper Functions

Add these to your shell profile or scripts:

```bash
# ~/.bashrc or ~/.zshrc

# Harness Code API base
export HARNESS_CODE_API="${HARNESS_BASE_URL:-https://app.harness.io}/code/api/v1"

# Create PR comment
harness_pr_comment() {
  local repo="$1"
  local pr="$2"
  local text="$3"

  curl -s -X POST "${HARNESS_CODE_API}/repos/${repo}/pullreq/${pr}/comments" \
    -H "x-api-key: ${HARNESS_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"${text}\"}"
}

# Create code comment on specific lines
harness_code_comment() {
  local repo="$1"
  local pr="$2"
  local file="$3"
  local line_start="$4"
  local line_end="$5"
  local text="$6"

  curl -s -X POST "${HARNESS_CODE_API}/repos/${repo}/pullreq/${pr}/comments" \
    -H "x-api-key: ${HARNESS_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
      \"text\": \"${text}\",
      \"path\": \"${file}\",
      \"line_start\": ${line_start},
      \"line_end\": ${line_end},
      \"line_start_new\": true,
      \"line_end_new\": true
    }"
}

# Submit review
harness_pr_review() {
  local repo="$1"
  local pr="$2"
  local decision="$3"  # approved, changereq, reviewed
  local commit_sha="$4"

  curl -s -X POST "${HARNESS_CODE_API}/repos/${repo}/pullreq/${pr}/reviews" \
    -H "x-api-key: ${HARNESS_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
      \"commit_sha\": \"${commit_sha}\",
      \"decision\": \"${decision}\"
    }"
}

# Approve PR
harness_pr_approve() {
  local repo="$1"
  local pr="$2"
  local commit_sha="$3"

  harness_pr_review "$repo" "$pr" "approved" "$commit_sha"
}

# Request changes
harness_pr_request_changes() {
  local repo="$1"
  local pr="$2"
  local commit_sha="$3"

  harness_pr_review "$repo" "$pr" "changereq" "$commit_sha"
}

# Merge PR
harness_pr_merge() {
  local repo="$1"
  local pr="$2"
  local method="${3:-squash}"
  local source_sha="$4"
  local title="$5"

  curl -s -X POST "${HARNESS_CODE_API}/repos/${repo}/pullreq/${pr}/merge" \
    -H "x-api-key: ${HARNESS_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
      \"method\": \"${method}\",
      \"source_sha\": \"${source_sha}\",
      \"title\": \"${title}\",
      \"delete_source_branch\": true
    }"
}
```

### Usage Examples

```bash
# Add a comment to PR #42
harness_pr_comment "my-repo" 42 "LGTM! Ready to merge."

# Add code comment on specific lines
harness_code_comment "my-repo" 42 "src/auth.ts" 50 55 "Consider adding null check here"

# Approve PR
harness_pr_approve "my-repo" 42 "abc123def456"

# Request changes
harness_pr_request_changes "my-repo" 42 "abc123def456"

# Merge with squash
harness_pr_merge "my-repo" 42 "squash" "abc123def456" "feat: Add authentication"
```

---

### Python Helper Class

```python
import requests
import os
from typing import Optional, Literal

class HarnessCodeAPI:
    """Harness Code REST API client for PR operations."""

    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.environ.get("HARNESS_API_KEY")
        self.base_url = base_url or os.environ.get("HARNESS_BASE_URL", "https://app.harness.io")
        self.api_url = f"{self.base_url}/code/api/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def create_comment(
        self,
        repo: str,
        pr_number: int,
        text: str,
        path: Optional[str] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
        parent_id: Optional[int] = None
    ) -> dict:
        """Create a comment on a pull request."""
        url = f"{self.api_url}/repos/{repo}/pullreq/{pr_number}/comments"

        data = {"text": text}

        if parent_id:
            data["parent_id"] = parent_id
        elif path and line_start:
            data.update({
                "path": path,
                "line_start": line_start,
                "line_end": line_end or line_start,
                "line_start_new": True,
                "line_end_new": True
            })

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def submit_review(
        self,
        repo: str,
        pr_number: int,
        commit_sha: str,
        decision: Literal["approved", "changereq", "reviewed"]
    ) -> dict:
        """Submit a review on a pull request."""
        url = f"{self.api_url}/repos/{repo}/pullreq/{pr_number}/reviews"

        data = {
            "commit_sha": commit_sha,
            "decision": decision
        }

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def approve(self, repo: str, pr_number: int, commit_sha: str) -> dict:
        """Approve a pull request."""
        return self.submit_review(repo, pr_number, commit_sha, "approved")

    def request_changes(self, repo: str, pr_number: int, commit_sha: str) -> dict:
        """Request changes on a pull request."""
        return self.submit_review(repo, pr_number, commit_sha, "changereq")

    def merge(
        self,
        repo: str,
        pr_number: int,
        source_sha: str,
        method: Literal["merge", "squash", "rebase", "fast-forward"] = "squash",
        title: Optional[str] = None,
        message: Optional[str] = None,
        delete_source_branch: bool = True,
        dry_run: bool = False
    ) -> dict:
        """Merge a pull request."""
        url = f"{self.api_url}/repos/{repo}/pullreq/{pr_number}/merge"

        data = {
            "method": method,
            "source_sha": source_sha,
            "delete_source_branch": delete_source_branch,
            "dry_run": dry_run
        }

        if title:
            data["title"] = title
        if message:
            data["message"] = message

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def add_reviewer(self, repo: str, pr_number: int, reviewer_id: int) -> dict:
        """Add a reviewer to a pull request."""
        url = f"{self.api_url}/repos/{repo}/pullreq/{pr_number}/reviewers"

        data = {"reviewer_id": reviewer_id}

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()


# Usage
if __name__ == "__main__":
    client = HarnessCodeAPI()

    # Add a comment
    client.create_comment(
        repo="my-app",
        pr_number=42,
        text="Great implementation! Consider adding unit tests."
    )

    # Add code comment
    client.create_comment(
        repo="my-app",
        pr_number=42,
        text="This could cause a null pointer exception",
        path="src/services/auth.ts",
        line_start=50,
        line_end=52
    )

    # Approve PR
    client.approve(repo="my-app", pr_number=42, commit_sha="abc123")

    # Merge with squash
    client.merge(
        repo="my-app",
        pr_number=42,
        source_sha="abc123",
        method="squash",
        title="feat: Add user authentication",
        delete_source_branch=True
    )
```

---

### Claude Code Review Workflow

Use these APIs to enable Claude to perform automated code reviews:

```python
from harness_code_api import HarnessCodeAPI

def claude_code_review(repo: str, pr_number: int, jira_key: str):
    """
    Claude-powered code review workflow.

    1. Fetch PR changes via MCP
    2. Analyze code for issues
    3. Add comments via REST API
    4. Submit review decision
    5. Update Jira with review status
    """
    client = HarnessCodeAPI()

    # Step 1: Get PR details via MCP
    pr = harness_get_pull_request(repo_id=repo, pr_number=pr_number)
    activities = harness_get_pull_request_activities(repo_id=repo, pr_number=pr_number)

    # Step 2: Analyze changes (Claude analyzes the diff)
    issues_found = []  # Claude populates this with issues

    # Step 3: Add code comments for each issue
    for issue in issues_found:
        client.create_comment(
            repo=repo,
            pr_number=pr_number,
            text=f"**{issue['severity']}**: {issue['message']}\n\n{issue['suggestion']}",
            path=issue['file'],
            line_start=issue['line_start'],
            line_end=issue['line_end']
        )

    # Step 4: Submit review decision
    if any(i['severity'] == 'critical' for i in issues_found):
        client.request_changes(repo, pr_number, pr.source_sha)
        review_status = "Changes Requested"
    elif issues_found:
        client.submit_review(repo, pr_number, pr.source_sha, "reviewed")
        review_status = "Reviewed with Comments"
    else:
        client.approve(repo, pr_number, pr.source_sha)
        review_status = "Approved"

    # Step 5: Update Jira
    jira_add_comment(
        issue_key=jira_key,
        body=f"""
        ## Code Review Complete

        **PR:** [#{pr_number}]({pr.url})
        **Status:** {review_status}
        **Issues Found:** {len(issues_found)}

        ### Issues by Severity
        - Critical: {sum(1 for i in issues_found if i['severity'] == 'critical')}
        - Warning: {sum(1 for i in issues_found if i['severity'] == 'warning')}
        - Info: {sum(1 for i in issues_found if i['severity'] == 'info')}
        """
    )

    return review_status
```

---

## Confluence Documentation Integration

The Jira orchestrator automatically creates and links Confluence documentation for all Jira work items. This ensures every issue, sub-issue, and PR has proper documentation.

### Automatic Documentation Creation

When work starts on a Jira issue, the following documentation is automatically created:

| Issue Type | Documents Created |
|------------|-------------------|
| Epic | TDD, Implementation Notes, Runbook, API Docs |
| Story | TDD, Implementation Notes |
| Task | Implementation Notes |
| Sub-task | Implementation Notes (linked to parent) |
| Bug | Implementation Notes |

### Python API for Documentation Linking

```python
from lib.confluence_doc_linker import ConfluenceDocLinker, DocumentationConfig

# Initialize linker
linker = ConfluenceDocLinker()

# Ensure documentation exists for an issue
docs = linker.ensure_issue_docs("PROJ-123")

# Create docs for sub-issues (linked to parent)
sub_docs = linker.ensure_sub_issue_docs(
    parent_jira_key="PROJ-123",
    sub_issue_keys=["PROJ-124", "PROJ-125", "PROJ-126"]
)

# Link README to Confluence
linker.link_readme_to_confluence(
    readme_path="./README.md",
    jira_key="PROJ-123"
)
```

### PR Documentation Integration

When creating or reviewing PRs, documentation links are automatically added:

```python
from lib.harness_code_api import HarnessCodeAPI
from lib.confluence_doc_linker import ConfluenceDocLinker

harness = HarnessCodeAPI()
linker = ConfluenceDocLinker()

# Link PR to documentation
linker.link_pr_to_docs(
    repo="my-service",
    pr_number=42,
    jira_key="PROJ-123",
    harness_client=harness
)
```

### README Documentation Section

READMEs are automatically updated with a Documentation section:

```markdown
## Documentation

**Jira Issue:** [PROJ-123](https://jira.company.com/browse/PROJ-123)

**Confluence Documentation:**
- [Technical Design: PROJ-123](https://confluence.company.com/pages/123)
- [Implementation Notes: PROJ-123](https://confluence.company.com/pages/124)
```

### Configuration

Create `.jira/doc-sync.yml` in your workspace:

```yaml
documentation:
  confluence:
    base_url: "${CONFLUENCE_BASE_URL}"
    space_key: "ENG"
    parent_pages:
      tdd: "12345678"
      impl_notes: "12345679"

  auto_create:
    enabled: true
    on_work_start: true
    on_pr_create: true

  readme:
    auto_update: true

  pr:
    add_doc_links: true
    update_on_merge: true
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CONFLUENCE_BASE_URL` | Yes | Confluence instance URL |
| `CONFLUENCE_SPACE_KEY` | No | Default space (default: ENG) |
| `CONFLUENCE_PARENT_PAGE_ID` | No | Default parent page for docs |
| `JIRA_BASE_URL` | Yes | Jira instance URL |

---

## Related Documentation

- [Harness MCP Server](https://developer.harness.io/docs/platform/harness-aida/harness-mcp-server/)
- [Harness Code Repository](https://developer.harness.io/docs/code-repository/)
- [Review PRs](https://developer.harness.io/docs/code-repository/pull-requests/review-pr/)
- [Merge PRs](https://developer.harness.io/docs/code-repository/pull-requests/merge-pr/)
- [Connect to Jira](https://developer.harness.io/docs/platform/connectors/ticketing-systems/connect-to-jira/)
- [Jira Connector Settings Reference](https://developer.harness.io/docs/platform/approvals/w_approval-ref/jira-connector-settings-reference/)
- [Create Jira Issues in CD Stages](https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/cd-steps/ticketing-systems/create-jira-issues-in-cd-stages/)
- [Confluence Documentation Patterns](../confluence/SKILL.md)
- [Documentation Sync Agent](../../agents/documentation-sync-agent.md)
