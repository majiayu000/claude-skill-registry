---
name: git-pr-creator
description: Create Git pull requests and optionally update JIRA tickets with comments and image attachments
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: pr-creation
---

## What I do

I implement a complete Git PR creation workflow with optional JIRA integration:

1. **Check JIRA Integration**: Ask user if JIRA is used for the project
2. **Create Pull Request**: Create a GitHub/GitLab PR with comprehensive description
3. **Use git-semantic-commits**: Format PR title following Conventional Commits specification
4. **Scan for Diagrams/Images**: Search for workflow-related images and diagrams
5. **Attach Images to JIRA**: Upload local/temporary images directly to JIRA (not just links)
6. **Add JIRA Comments**: Use `git-issue-updater` to create comments with PR details and attachments
7. **Update JIRA Status** (Optional): Use `jira-status-updater` to transition ticket status after manual merge


## When to use me

Use this workflow when:
- You've completed work on a feature or fix and need to create a PR
- You want to update JIRA tickets with PR information
- You have diagrams or images that need to be attached to JIRA (not just linked)
- You need to ensure JIRA tickets are updated with actual image files for visibility
- You want to maintain traceability between PRs and JIRA tickets

## Prerequisites

- Git repository with commits to push
- GitHub CLI (`gh`) or GitLab CLI (`glab`) installed and authenticated
- If using JIRA: Atlassian account with appropriate permissions
- JIRA cloud ID and project key
- Existing JIRA ticket(s) to update

## Steps

### Step 1: Check Git Status
- Verify current git status:
  ```bash
  git status
  ```
- Ensure all changes are committed
- Check for uncommitted changes that need attention

### Step 2: Ask About JIRA Integration
- Prompt the user: "Is JIRA used for this project? (yes/no)"
- If yes, proceed with JIRA integration steps
- If no, skip JIRA-related steps and only create the PR

### Step 3: Get JIRA Ticket Information (if JIRA is used)
- Ask the user for the JIRA ticket ID (e.g., "IBIS-101")
- Verify the ticket exists using Atlassian MCP tools
- Get the cloud ID if not provided

### Step 4: Create Pull Request
- Push the current branch to remote:
   ```bash
  git push -u origin <branch-name>
  ```
- **Use git-semantic-commits for PR title formatting**:
  - Format PR title following Conventional Commits specification
  - Examples: `feat: add login functionality`, `fix(auth): resolve session timeout`, `docs: update API documentation`
  - Include scope when relevant: `feat(api): add user authentication`, `fix(ui): resolve layout issue`
  - Use breaking change indicator if applicable: `feat!: change API signature` or `feat(api)!: breaking change to authentication`
- Create the PR with a comprehensive description:
   ```bash
  gh pr create --title "<PR Title>" --body "<PR Description>"
  ```
- PR description should include:
   - Overview of changes
   - JIRA ticket reference (if applicable)
   - Files changed
   - Testing performed
   - Screenshots/diagrams (as references)

### Step 5: Scan for Diagrams and Images
- Search for image files in the repository:
  ```bash
  # Common image locations
  find . -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.svg" \) -not -path "*/node_modules/*"
  
  # Check diagrams directory
  ls -la diagrams/
  
  # Check tmp directory
  ls -la /tmp/*.png /tmp/*.jpg /tmp/*.svg 2>/dev/null
  ```
- Identify workflow-related images:
  - Look for files with names like: `workflow`, `diagram`, `flow`, `process`, `architecture`
  - Check recent image creation timestamps
  - Ask user to confirm which images are relevant

### Step 6: Categorize Images
- For each image found, determine:
  - **Accessible images**: Hosted on public URLs or cloud storage (can be linked)
  - **Local/temporary images**: Files in `/tmp/`, local directories, or private servers (must be attached)

### Step 7: Upload Local Images to JIRA (if JIRA is used)

For each local/temporary image that needs to be shared on JIRA:

1. **Upload the image to JIRA**:
   Use Atlassian MCP tool `atlassian_addAttachmentToJiraIssue` with:
   - cloudId: The Atlassian cloud ID
   - issueIdOrKey: The JIRA ticket key
   - attachment: Path to the local image file
   
2. **Get the attachment URL**:
   - The response will include the attachment URL hosted on JIRA
   - This URL is accessible within the JIRA ecosystem

3. **Store attachment URLs** for use in comments

### Step 8: Create JIRA Comments (if JIRA is used)

Create a comprehensive comment on the JIRA ticket with PR details using `atlassian_addCommentToJiraIssue`.

**Comment Template**:
```markdown
## Pull Request Created

**PR**: #<PR_NUMBER> - <PR_TITLE>
**URL**: <PR_URL>
**Branch**: <branch-name>

### Changes Summary
<Brief description of what was implemented>

### Files Modified
<list of key files changed>

### Diagrams/Visuals
<embed uploaded images using JIRA attachment format>

### Testing Performed
<test coverage and results>

### Review Request
@reviewer1 @reviewer2
```

### Step 9: Verify and Report

- Verify PR creation:
  ```bash
  gh pr view
  ```
- Verify JIRA comment (if applicable)
- Display summary:
  ```
  ✅ Pull request created successfully!
  ✅ Branch pushed to remote
  ✅ JIRA ticket updated (if applicable)
  ✅ Images attached to JIRA (if applicable)
  
  **PR Details**:
  - PR: #<number>
  - URL: <pr-url>
  - Title: <title>
  
  **JIRA Update**:
   - Ticket: <TICKET-KEY>
   - Comments added: Yes
   - Images attached: <count>
   ```

### Step 10: Update JIRA Ticket Status (Optional)

**Purpose**: Provide option to update JIRA ticket status after manual PR merge

**When to use**:
- PR was manually merged (not through pr-creation-workflow)
- You want to transition JIRA ticket to "Done" status
- You have merged the PR outside of the automated workflow

**Implementation**:
```bash
# Prompt user for status update
if [ "$JIRA_USED" = "yes" ] && [ -n "$JIRA_TICKET" ]; then
  read -p "Would you like to update JIRA ticket status after merge? (yes/no): " UPDATE_STATUS

  if [ "$UPDATE_STATUS" = "yes" ]; then
    echo ""
    echo "Updating JIRA ticket status..."
    echo "=========================================="

    # Use jira-status-updater integration
    # This provides automated status transitions with error handling

    # Get cloud ID
    CLOUD_ID="${ATLASSIAN_CLOUD_ID:-<your-cloud-id>}"

    # 1. Get available transitions
    TRANSITIONS=$(atlassian_getTransitionsForJiraIssue \
      --cloudId "$CLOUD_ID" \
      --issueIdOrKey "$JIRA_TICKET")

    # 2. Find target status (Done or Closed)
    TARGET_TRANSITION_ID=$(echo "$TRANSITIONS" | jq -r '.transitions[] | select(.to.name == "Done" or .to.name == "Closed") | .id' | head -1)
    TARGET_TRANSITION_NAME=$(echo "$TRANSITIONS" | jq -r '.transitions[] | select(.to.name == "Done" or .to.name == "Closed") | .to.name' | head -1)

    # 3. Get current status
    TICKET_DETAILS=$(atlassian_getJiraIssue \
      --cloudId "$CLOUD_ID" \
      --issueIdOrKey "$JIRA_TICKET")
    CURRENT_STATUS=$(echo "$TICKET_DETAILS" | jq -r '.fields.status.name')

    echo "Current status: $CURRENT_STATUS"
    echo "Target status: $TARGET_TRANSITION_NAME"

    # 4. Execute transition (if not already in target status)
    if [ "$CURRENT_STATUS" = "$TARGET_TRANSITION_NAME" ]; then
      echo "✅ Ticket already in target status: $TARGET_TRANSITION_NAME"
    elif [ -n "$TARGET_TRANSITION_ID" ]; then
      atlassian_transitionJiraIssue \
        --cloudId "$CLOUD_ID" \
        --issueIdOrKey "$JIRA_TICKET" \
        --transition "{\"id\": \"$TARGET_TRANSITION_ID\"}"

      if [ $? -eq 0 ]; then
        echo "✅ Successfully transitioned $JIRA_TICKET from $CURRENT_STATUS to $TARGET_TRANSITION_NAME"

        # 5. Add merge comment
        COMMIT_HASH=$(git rev-parse HEAD)
        COMMIT_AUTHOR=$(git log -1 --pretty=%an)
        COMMIT_DATE=$(git log -1 --date=iso8601 --pretty=%aI)

        COMMENT_BODY=$(cat <<EOF
## Pull Request Merged (Manual)

**PR**: #$PR_NUMBER - <pr-title>
**URL**: $PR_URL
**Branch**: $CURRENT_BRANCH

### Status Update
✅ Ticket transitioned from **$CURRENT_STATUS** to **$TARGET_TRANSITION_NAME**

### Merge Details
- **Commit**: \`$COMMIT_HASH\`
- **Author**: $COMMIT_AUTHOR
- **Date**: $COMMIT_DATE

### Files Changed
\`\`\`
$(git diff --stat HEAD~1 HEAD)
\`\`\`

### Work Completed
The pull request has been manually merged and the ticket has been closed.
EOF
)

        atlassian_addCommentToJiraIssue \
          --cloudId "$CLOUD_ID" \
          --issueIdOrKey "$JIRA_TICKET" \
          --commentBody "$COMMENT_BODY"

        if [ $? -eq 0 ]; then
          echo "✅ Added merge comment to $JIRA_TICKET"
        fi
      else
        echo "❌ Failed to transition $JIRA_TICKET"
        echo "   Check permissions and available transitions"
      fi
    else
      echo "⚠️  No 'Done' or 'Closed' transition available for $JIRA_TICKET"
      echo "   Available transitions:"
      echo "$TRANSITIONS" | jq -r '.transitions[] | "   - \(.to.name)"'
    fi

    echo "=========================================="
    echo ""
    echo "🔗 JIRA Ticket: https://<company>.atlassian.net/browse/$JIRA_TICKET"
  fi
fi
```

**Example Output**:
```
Would you like to update JIRA ticket status after merge? (yes/no): yes

Updating JIRA ticket status...
==========================================
Current status: In Progress
Target status: Done

✅ Successfully transitioned IBIS-101 from In Progress to Done
✅ Added merge comment to IBIS-101
==========================================

🔗 JIRA Ticket: https://company.atlassian.net/browse/IBIS-101
```

## Image Handling Strategy


### For Accessible Images (Public URLs)
If the image is already hosted on a public URL (e.g., GitHub, S3, cloud storage):
- Embed directly in JIRA comment using markdown:
  ```markdown
  ![Diagram](https://example.com/workflow.png)
  ```
- No need to upload as attachment

### For Local/Temporary Images
If the image is a local file that won't be accessible from JIRA:
- **Must upload as attachment to JIRA**
- Use the `atlassian_addAttachmentToJiraIssue` tool
- Reference the uploaded image in the comment using the attachment URL

**Example**:
```bash
# Upload local image
atlassian_addAttachmentToJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey "IBIS-101" \
  --attachment "/tmp/workflow-diagram.png"

# Response returns attachment URL:
# https://yourcompany.atlassian.net/secure/attachment/12345/workflow-diagram.png

# Use this URL in the comment
```

**Correct JIRA Comment with Attachment**:
```markdown
### Workflow Diagram

![Workflow Diagram](https://company.atlassian.net/secure/attachment/12345/workflow-diagram.png)
```

**Incorrect JIRA Comment (local file path)**:
```markdown
### Workflow Diagram

![Workflow Diagram](/tmp/workflow-diagram.png)
```

## Examples

### Example 1: PR with JIRA Integration and Local Image

**User**: "Create a PR for the login feature. Yes, JIRA is used. Ticket is IBIS-101."

**Execution**:
1. Push branch `feature/login` to remote
2. Create PR #42 with title "Implement login feature"
3. Scan for images:
   - Found: `/tmp/login-flow.png` (local, not accessible)
   - Found: `diagrams/architecture.png` (local, not accessible)
4. Upload images to JIRA:
   - Upload `/tmp/login-flow.png` → Gets attachment URL
   - Upload `diagrams/architecture.png` → Gets attachment URL
5. Create JIRA comment with embedded images

**JIRA Comment Created**:
```markdown
## Pull Request Created

**PR**: #42 - Implement login feature
**URL**: https://github.com/org/repo/pull/42
**Branch**: feature/login

### Changes Summary
Implemented user authentication with email/password login, session management, and password reset functionality.

### Files Modified
- src/auth/login.ts
- src/auth/session.ts
- src/components/LoginForm.tsx
- src/api/auth.ts

### Workflow Diagram

![Login Flow](https://company.atlassian.net/secure/attachment/10001/login-flow.png)

### Architecture

![System Architecture](https://company.atlassian.net/secure/attachment/10002/architecture.png)

### Testing Performed
- Unit tests: 100% coverage
- Integration tests: All passing
- Manual testing: Verified login flow end-to-end

### Review Request
@tech-lead @senior-dev
```

### Example 2: PR with Public URL Image

**User**: "Create a PR for the dashboard. Yes, JIRA is used. Ticket is IBIS-102."

**Execution**:
1. Push branch `feature/dashboard` to remote
2. Create PR #43
3. Scan for images:
   - Found: `https://cdn.example.com/dashboard-mockup.png` (public URL)
   - Found: `/tmp/notes.png` (local, not accessible)
4. Upload only local image to JIRA
5. Create JIRA comment with both public URL and embedded attachment

**JIRA Comment Created**:
```markdown
## Pull Request Created

**PR**: #43 - Implement dashboard
**URL**: https://github.com/org/repo/pull/43

### Changes Summary
Built responsive dashboard with data visualization and analytics.

### UI Mockup (Design Spec)

![Dashboard Mockup](https://cdn.example.com/dashboard-mockup.png)

### Technical Implementation Notes

![Notes](https://company.atlassian.net/secure/attachment/10003/notes.png)
```

### Example 3: PR without JIRA

**User**: "Create a PR for the bug fix. No, JIRA is not used."

**Execution**:
1. Push branch `fix/crash-issue` to remote
2. Create PR #44
3. Skip JIRA integration
4. Display summary

**Output**:
```
✅ Pull request created successfully!
✅ Branch pushed to remote

**PR Details**:
- PR: #44
- URL: https://github.com/org/repo/pull/44
- Title: Fix crash on login page

No JIRA integration requested.
```

## Image Detection and Categorization

### Detection Patterns

Search for images in these locations:
```bash
# Project diagrams
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

### Categorization Logic

```bash
# Check if URL is accessible
if [[ "$image_path" =~ ^https?:// ]]; then
  # It's a URL - test if accessible
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

### Handling Each Type
- **accessible_url**: Embed directly in JIRA comment
- **inaccessible_url**: Download and upload as JIRA attachment
- **local_file**: Upload as JIRA attachment
- **not_found**: Warn user and skip

## Atlassian MCP Tools Reference

### atlassian_getAccessibleAtlassianResources
```bash
atlassian_getAccessibleAtlassianResources
```
Returns: List of accessible Atlassian resources with cloud IDs

### atlassian_addAttachmentToJiraIssue
```bash
atlassian_addAttachmentToJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY> \
  --attachment <file-path>
```
Returns: Attachment metadata including URL

### atlassian_addCommentToJiraIssue
```bash
atlassian_addCommentToJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY> \
  --commentBody <markdown-content>
```
Returns: Comment ID and details

### atlassian_getJiraIssue
```bash
atlassian_getJiraIssue \
  --cloudId <CLOUD_ID> \
  --issueIdOrKey <TICKET_KEY>
```
Returns: Issue details including status, assignee, etc.

## Best Practices

- Always confirm JIRA usage with the user before proceeding
- **Use git-semantic-commits for PR title formatting** to ensure consistent semantic versioning
- **Follow Conventional Commits specification**: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
- **Include scopes** in PR titles to identify affected components (e.g., feat(api):, fix(ui):)
- **Use breaking change indicator** (!) when appropriate: `feat!: breaking API change`
- Upload local/temporary images as JIRA attachments, don't link to local paths
- **Use git-issue-updater for consistent JIRA ticket comments** with user, date, time, and PR details
- Use descriptive filenames for images before uploading
- Organize images in a `diagrams/` directory for consistency
- Include PR number and brief description in JIRA comments
- Tag relevant team members in JIRA comments using `@username`
- Verify image accessibility before embedding URLs
- Clean up temporary images after uploading to JIRA
- Keep JIRA comments concise and well-formatted
- Always verify that the PR was created successfully
- Test JIRA attachments by opening the URL in a browser

## Common Issues

### Image Upload Fails
**Issue**: `atlassian_addAttachmentToJiraIssue` returns an error

**Solution**:
- Verify file path is correct
- Check file size limits (JIRA typically limits to 10-100MB per attachment)
- Ensure you have permission to add attachments to the issue
- Verify the file is not corrupted

### JIRA Comment Not Visible
**Issue**: Comment added but doesn't display images

**Solution**:
- Use the attachment URL returned by the upload API
- Don't use local file paths in comments
- Ensure markdown syntax is correct:
  ```markdown
  ![Alt text](attachment-url)
  ```

### Too Many Images
**Issue**: Too many images found in the repository

**Solution**:
- Ask user which images are relevant
- Filter by timestamp (e.g., images created in last hour)
- Focus on workflow-related images
- Allow user to select specific images to upload

### Branch Not Pushed
**Issue**: PR creation fails because branch isn't on remote

**Solution**:
```bash
# Push current branch with upstream tracking
git push -u origin $(git branch --show-current)
```

### JIRA Ticket Not Found
**Issue**: Cannot access the specified JIRA ticket

**Solution**:
- Verify the ticket ID format (e.g., IBIS-101)
- Check that you have access to the JIRA project
- Use `atlassian_getVisibleJiraProjects` to list accessible tickets
- Verify the cloud ID is correct

## Troubleshooting Checklist

Before creating PR:
- [ ] All changes are committed
- [ ] Current branch is correct
- [ ] Branch name follows conventions
- [ ] User confirmed JIRA usage (yes/no)
- [ ] PR title follows Conventional Commits format (if applicable)

Before JIRA integration (if yes):
- [ ] JIRA ticket ID is valid
- [ ] Atlassian MCP tools are available
- [ ] User has permissions to comment/attach
- [ ] Cloud ID is configured

Before image handling:
- [ ] Image files exist and are accessible
- [ ] Image sizes are within limits
- [ ] User has confirmed which images to include
- [ ] Local images will be uploaded as attachments

After completion:
- [ ] PR is created and accessible
- [ ] PR description is complete
- [ ] JIRA comment is added (if applicable)
- [ ] Images are properly embedded (not broken links)
- [ ] Summary is displayed to user

## Related Commands

```bash
# Check git status
git status

# View current branch
git branch --show-current

# Push branch with upstream
git push -u origin $(git branch --show-current)

# Create PR
gh pr create --title "Title" --body "Description"

# View PR
gh pr view

# List PRs
gh pr list

# Find recent images
find . -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.svg" \) -mtime -1

# Find images by pattern
find . -name "*workflow*.png" -o -name "*diagram*.png"

# Check file type
file workflow.png

# Get image dimensions
identify workflow.png
```

## Related Skills

- **JIRA Integration**:
  - `jira-git-integration`: For JIRA utilities, comments, and image uploads
  - `jira-status-updater`: For automated JIRA ticket status transitions after PR merge
- **Git Frameworks**:
  - `git-semantic-commits`: For semantic commit message formatting and PR title conventions
  - `git-issue-updater`: For consistent issue/ticket update functionality with user, date, time
- **PR Workflows**:
  - `pr-creation-workflow`: For generic PR creation workflow
  - `nextjs-pr-workflow`: For Next.js-specific PR workflows
- **Issue Management**:
  - `git-issue-creator`: For creating GitHub issues with branches
- **Diagram Creation**:
  - `ascii-diagram-creator`: For creating workflow diagrams
