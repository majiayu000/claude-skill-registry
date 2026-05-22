---
name: jira-git-integration
description: Generic JIRA + Git workflow utilities for ticket management, branch creation, and integration
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: jira-git-integration
---

## What I do

I provide JIRA + Git integration utilities that can be used across multiple workflows:

1. **Get JIRA Resources**: Detect and retrieve Atlassian cloud ID, visible projects, and accessible resources
2. **Get JIRA User Info**: Retrieve current user's account ID for ticket assignment
3. **Create JIRA Tickets**: Create new tasks, stories, or bugs in specified JIRA projects
4. **Add JIRA Comments**: Add comments to existing JIRA tickets with Markdown formatting
5. **Upload Images to JIRA**: Upload local images as JIRA attachments and retrieve attachment URLs
6. **Generate JIRA Branch Names**: Create consistent branch names from JIRA tickets
7. **Fetch JIRA Issue Details**: Retrieve ticket information including status, assignee, description

## When to use me

Use this framework when:
- You need JIRA integration in a workflow
- You're creating a skill that requires JIRA ticket management
- You need to upload images to JIRA tickets
- You want to ensure consistent branch naming across JIRA workflows
- You need to add comments or attachments to JIRA tickets

This is a **framework skill** - it provides JIRA utilities that other skills use.

## Core Workflow Steps

### Step 1: Get Accessible Atlassian Resources

**Purpose**: Retrieve cloud ID and list of accessible Atlassian resources

**Tools Used**: `atlassian_getAccessibleAtlassianResources`

```bash
# Get accessible resources (includes cloud IDs)
atlassian_getAccessibleAtlassianResources
```

**Expected Output**:
```json
[
  {
    "id": "23594c42-08ff-4d2a-8065-6756e3590c37",
    "url": "https://company.atlassian.net",
    "name": "company",
    "scopes": ["read:jira-work", "write:jira-work", "read:confluence", "write:confluence"]
  }
]
```

**Extract Cloud ID**: Store the `id` field for use in subsequent JIRA operations

### Step 2: Get JIRA User Information

**Purpose**: Retrieve current user's account ID for ticket assignment

**Tools Used**: `atlassian_atlassianUserInfo`

```bash
# Get current user info
atlassian_atlassianUserInfo
```

**Expected Output**:
```json
{
  "account_id": "712020:1fe13d6b-e3ff-4455-9349-39a1f243e9bb",
  "email": "user@company.com",
  "name": "John Doe",
  "account_status": "active"
}
```

**Extract Account ID**: Store the `account_id` field for assigning tickets

### Step 3: Get Visible JIRA Projects

**Purpose**: List all JIRA projects the user has access to

**Tools Used**: `atlassian_getVisibleJiraProjects`

```bash
# Get visible projects
atlassian_getVisibleJiraProjects --cloudId <CLOUD_ID>
```

**Expected Output**:
```json
{
  "values": [
    {
      "key": "IBIS",
      "name": "Project Name",
      "id": "10205",
      "issueTypes": [
        {
          "name": "Task",
          "id": "10222"
        },
        {
          "name": "Story",
          "id": "10220"
        },
        {
          "name": "Bug",
          "id": "10223"
        }
      ]
    }
  ]
}
```

**Extract Project Key**: Store the `key` field (e.g., `IBIS`) for use in ticket creation

### Step 4: Create JIRA Ticket

**Purpose**: Create a new ticket in specified JIRA project

**Tools Used**: `atlassian_createJiraIssue`

```bash
# Create new ticket
atlassian_createJiraIssue \
  --cloudId <CLOUD_ID> \
  --projectKey <PROJECT_KEY> \
  --issueTypeName <ISSUE_TYPE> \
  --summary "<Ticket Title>" \
  --description "<Ticket Description>" \
  --assignee_account_id <USER_ACCOUNT_ID>
```

**Parameters**:
- `cloudId`: Atlassian cloud ID (from Step 1)
- `projectKey`: JIRA project key (e.g., `IBIS`)
- `issueTypeName`: Issue type name (e.g., `Task`, `Story`, `Bug`)
- `summary`: Short title for the ticket
- `description`: Detailed description in Markdown format
- `assignee_account_id`: User's account ID (from Step 2, optional)

**Description Template**:
```markdown
## Description
<Detailed description of the work>

## Type
<Task | Story | Bug>

## Context
<Additional background information>

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3

## Files to Modify
1. `path/to/file1.ts` - Description
2. `path/to/file2.tsx` - Description

## Notes
<Additional notes or constraints>
```

**Expected Output**:
```json
{
  "id": "12345",
  "key": "IBIS-101",
  "self": "https://api.atlassian.com/ex/jira/.../issue/12345"
}
```

**Extract Ticket Key**: Store the `key` field (e.g., `IBIS-101`) for reference

### Step 5: Add Comment to JIRA Ticket

**Purpose**: Add a comment to an existing JIRA ticket

**Tools Used**: `atlassian_addCommentToJiraIssue`

```bash
# Add comment
atlassian_addCommentToJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY> \
  --commentBody "<Comment Content>"
```

**Parameters**:
- `cloudId`: Atlassian cloud ID
- `issueIdOrKey`: Ticket key (e.g., `IBIS-101`)
- `commentBody`: Comment content in Markdown format

**Comment Templates**:

**PR Reference Comment**:
```markdown
## Pull Request Created

**PR**: #<PR_NUMBER> - <PR_TITLE>
**URL**: <PR_URL>
**Branch**: <branch-name>

### Changes Summary
<Brief description of changes>

### Files Modified
<list of key files changed>

### Quality Checks
- Linting: ✅ Passed
- Build: ✅ Passed
- Tests: ✅ Passed

### Review Request
@reviewer1 @reviewer2
```

**Implementation Update Comment**:
```markdown
## Implementation Started

Branch: <branch-name>
Status: In Progress

### Next Steps
1. <Step 1>
2. <Step 2>
3. <Step 3>
```

**Image-Embedded Comment**:
```markdown
## Diagrams/Visuals

### Workflow Diagram
![Workflow Diagram](https://company.atlassian.net/secure/attachment/12345/workflow.png)

### Architecture
![System Architecture](https://company.atlassian.net/secure/attachment/12346/architecture.png)
```

### Step 6: Upload Image to JIRA

**Purpose**: Upload a local image file as a JIRA attachment

**Tools Used**: `atlassian_addAttachmentToJiraIssue`

```bash
# Upload image
atlassian_addAttachmentToJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY> \
  --attachment <IMAGE_FILE_PATH>
```

**Parameters**:
- `cloudId`: Atlassian cloud ID
- `issueIdOrKey`: Ticket key (e.g., `IBIS-101`)
- `attachment`: Path to local image file (e.g., `/tmp/workflow.png`)

**Expected Output**:
```json
{
  "id": "10001",
  "filename": "workflow.png",
  "content": "image/png",
  "size": 12345,
  "self": "https://api.atlassian.com/ex/jira/.../attachment/10001"
  "thumbnail": "https://company.atlassian.net/secure/thumbnail/12345/workflow.png"
}
```

**Extract Attachment URL**: The `self` field provides the URL for embedding in comments

**Attachment URL Format**:
```
https://company.atlassian.net/secure/attachment/<ATTACHMENT_ID>/<FILENAME>
```

**Usage in Comments**:
```markdown
![Workflow Diagram](https://company.atlassian.net/secure/attachment/10001/workflow.png)
```

### Step 7: Generate JIRA Branch Name

**Purpose**: Create a consistent branch name from a JIRA ticket key

**Branch Naming Conventions**:

| Format | Example | Use Case |
|--------|----------|-----------|
| `PROJECT-NUM` | `IBIS-101` | Simple, direct reference |
| `feature/PROJECT-NUM` | `feature/IBIS-101` | Feature branch pattern |
| `feature/PROJECT-NUM-description` | `feature/IBIS-101-add-login` | Descriptive feature branch |
| `bugfix/PROJECT-NUM` | `bugfix/IBIS-102` | Bug fix branch |
| `hotfix/PROJECT-NUM` | `hotfix/IBIS-103` | Hotfix branch |

**Implementation**:
```bash
# Generate branch name from ticket key
TICKET_KEY="IBIS-101"

# Simple format
BRANCH_NAME="${TICKET_KEY}"  # IBIS-101

# Feature format
BRANCH_NAME="feature/${TICKET_KEY}"  # feature/IBIS-101

# Descriptive feature format
BRANCH_NAME="feature/${TICKET_KEY}-add-dark-mode"  # feature/IBIS-101-add-dark-mode

# Create and checkout branch
git checkout -b "${BRANCH_NAME}"
```

**Branch Naming Best Practices**:
- Use lowercase
- Replace spaces with hyphens
- Include ticket key for traceability
- Keep branch names under 72 characters
- Follow git branch naming conventions

### Step 8: Get JIRA Issue Details

**Purpose**: Retrieve detailed information about a JIRA ticket

**Tools Used**: `atlassian_getJiraIssue`

```bash
# Get issue details
atlassian_getJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY>
```

**Parameters**:
- `cloudId`: Atlassian cloud ID
- `issueIdOrKey`: Ticket key (e.g., `IBIS-101`)

**Expected Output**:
```json
{
  "key": "IBIS-101",
  "fields": {
    "summary": "Implement new feature",
    "status": {
      "name": "In Progress"
    },
    "assignee": {
      "accountId": "712020:1fe13d6b-e3ff-4455-9349-39a1f243e9bb",
      "displayName": "John Doe"
    },
    "description": {
      "type": "doc",
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "text": "Detailed description..."
            }
          ]
        }
      ]
    }
    }
  }
}
```

**Extract Information**:
- Ticket status
- Assignee information
- Description content
- Priority, labels, etc.

## Image Handling Strategy

### Image Detection Patterns

Search for images in these locations:
```bash
# Common image locations
./diagrams/**/*.png
./diagrams/**/*.svg

# Recent images in tmp
/tmp/*.png
/tmp/*.jpg

# Documentation images
./docs/images/**/*.png
./assets/images/**/*.png

# Workflow-related (by filename pattern)
**/*workflow*.png
**/*diagram*.png
**/*flow*.png
**/*architecture*.png
**/*sequence*.png
```

### Image Categorization

```bash
# Determine if image needs upload
if [[ "$image_path" =~ ^https?:// ]]; then
  # It's a URL - check if accessible
  if curl -s -o /dev/null -w "%{http_code}" "$image_path" | grep -q "200"; then
    TYPE="accessible_url"
  else
    TYPE="inaccessible_url"
  fi
else
  # It's a file path
  if [[ -f "$image_path" ]]; then
    TYPE="local_file"
  else
    TYPE="not_found"
  fi
fi
```

### Handling Each Image Type

| Type | Action |
|------|--------|
| accessible_url | Embed directly in JIRA comment |
| inaccessible_url | Download and upload as JIRA attachment |
| local_file | Upload as JIRA attachment |
| not_found | Warn user and skip |
 
### Step 9: Transition JIRA Ticket Status

**Purpose**: Update JIRA ticket status after PR merge

**Tools Used**: `atlassian_getTransitionsForJiraIssue`, `atlassian_transitionJiraIssue`

**Usage**:
```bash
# Get available transitions
TRANSITIONS=$(atlassian_getTransitionsForJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY>)

# Find "Done" or "Closed" transition
TARGET_TRANSITION_ID=$(echo "$TRANSITIONS" | jq -r '.transitions[] | select(.to.name == "Done" or .to.name == "Closed") | .id' | head -1)

# Execute transition
atlassian_transitionJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY> \
  --transition '{"id": "<TRANSITION_ID>"}')
```

**When to Use**:
- PR has been successfully merged
- Work is complete and ticket should be closed
- Automating workflow to eliminate manual status updates

**Integration**:
- Use with `jira-status-updater` skill for complete automation
- Use with `pr-creation-workflow` for integrated PR + status updates
- Use with `git-pr-creator` for optional status updates after manual merge

## Best Practices


- **Cloud ID**: Always retrieve cloud ID once per session
- **User Info**: Cache user account ID for assignment operations
- **Project Keys**: Use project keys (e.g., `IBIS`) consistently
- **Ticket References**: Always use ticket keys (e.g., `IBIS-101`) for traceability
- **Branch Naming**: Use consistent branch naming with ticket keys
- **Image Uploads**: Upload local/temporary images, don't link to local paths
- **Comment Formatting**: Use Markdown for rich formatting in JIRA comments
- **Error Handling**: Check for JIRA API errors and provide clear messages
- **Permissions**: Verify user has appropriate permissions for operations

## Common Issues

### Cloud ID Not Found

**Issue**: Cannot determine Atlassian cloud ID

**Solution**:
```bash
# Use getAccessibleAtlassianResources to find cloud ID
atlassian_getAccessibleAtlassianResources
```

### Project Not Found

**Issue**: JIRA project key is invalid or inaccessible

**Solution**:
```bash
# List visible projects to find correct key
atlassian_getVisibleJiraProjects --cloudId <CLOUD_ID>
```

### User Not Assigned

**Issue**: Ticket not assigned to current user

**Solution**:
```bash
# Get user account ID
atlassian_atlassianUserInfo

# Create ticket with assignee
atlassian_createJiraIssue --assignee_account_id <ACCOUNT_ID>
```

### Image Upload Fails

**Issue**: `atlassian_addAttachmentToJiraIssue` returns error

**Solution**:
- Verify file path is correct
- Check file size limits (JIRA typically limits to 10-100MB)
- Ensure you have permission to add attachments
- Verify file is not corrupted

### Branch Name Conflicts

**Issue**: Branch with same name already exists

**Solution**:
```bash
# Force create new branch
git checkout -B <branch-name>

# Or switch to existing branch
git checkout <existing-branch>
```

## Troubleshooting Checklist

Before JIRA operations:
- [ ] Cloud ID is available
- [ ] User account ID is retrieved
- [ ] Project key is valid
- [ ] Issue type is valid for project
- [ ] User has appropriate permissions

After ticket creation:
- [ ] Ticket number/key is captured
- [ ] Ticket URL is accessible
- [ ] Ticket is assigned to correct user
- [ ] Branch name is generated correctly

After comment/attachment operations:
- [ ] Comment is added successfully
- [ ] Images are uploaded to JIRA
- [ ] Attachment URLs are accessible
- [ ] Comments display formatting correctly

## Related Commands

```bash
# Get visible JIRA projects
atlassian_getVisibleJiraProjects --cloudId <CLOUD_ID>

# Get JIRA issue details
atlassian_getJiraIssue --cloudId <CLOUD_ID> --issueIdOrKey <TICKET_KEY>

# Add comment to JIRA issue
atlassian_addCommentToJiraIssue --cloudId <CLOUD_ID> --issueIdOrKey <TICKET_KEY> --commentBody "<markdown>"

# Upload attachment to JIRA
atlassian_addAttachmentToJiraIssue --cloudId <CLOUD_ID> --issueIdOrKey <TICKET_KEY> --attachment <file-path>

# Create JIRA ticket
atlassian_createJiraIssue --cloudId <CLOUD_ID> --projectKey <PROJECT_KEY> --issueTypeName "Task" --summary "Title" --description "<desc>"

# Get user info
atlassian_atlassianUserInfo

# Get accessible resources
atlassian_getAccessibleAtlassianResources
```

## Relevant Skills

Skills that use this JIRA integration framework:
- `git-pr-creator`: PR creation with JIRA comments and image uploads
- `jira-git-workflow`: JIRA ticket creation and branch management
- `nextjs-pr-workflow`: Next.js PR workflow with JIRA integration
- `jira-status-updater`: Automated JIRA ticket status transitions after PR merge

Additional related skills:
- `pr-creation-workflow`: Generic PR creation workflow
- `ticket-branch-workflow`: Ticket-to-branch-to-PLAN workflow
