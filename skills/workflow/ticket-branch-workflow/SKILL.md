---
name: ticket-branch-workflow
description: Generic ticket-to-branch-to-PLAN workflow supporting multiple platforms (GitHub, JIRA)
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: ticket-branch
---

## What I do

I provide a generic ticket-to-branch-to-PLAN workflow that can be adapted for multiple platforms, delegating to framework skills:

1. **Analyze Request**: Parse user's statement to determine work type and required platform
2. **Detect Platform**: Identify if using GitHub issues or JIRA tickets (or both)
3. **Assign Labels/Type**: Use `git-issue-labeler` framework to determine appropriate labels (GitHub) or issue types (JIRA)
4. **Create Ticket**: Create a new ticket with assigned labels/issue type
5. **Generate Branch Name**: Create a consistent branch name from ticket number/ID
6. **Create Branch**: Create and checkout new git branch
7. **Create PLAN.md**: Generate a PLAN.md file with implementation structure
8. **Commit PLAN.md**: Use `git-semantic-commits` framework to format commit message
9. **Update Issue**: Use `git-issue-updater` framework to add progress comment with user, date, time
10. **Push Branch**: Push branch to remote repository

## When to use me

Use this framework when:
- You need to start a new feature, bug fix, or task tracked in a ticketing system
- You want a systematic approach with ticket creation, branching, planning, and syncing
- You're creating a workflow skill that includes ticket creation and branching
- You need to support both GitHub and JIRA ticketing

**Frameworks Used**:
- `git-issue-labeler` - For GitHub default label assignment (bug, enhancement, documentation, duplicate, good first issue, help wanted, invalid, question, wontfix)
- `git-semantic-commits` - For semantic commit message formatting (Conventional Commits specification)
- `git-issue-updater` - For updating issues with commit progress (user, date, time)
- `jira-git-integration` - For JIRA-specific operations when working with JIRA tickets (API, comments, attachments)

This is a **framework skill** - it provides ticket-to-branch logic that other skills extend.

## Core Workflow Steps

### Step 1: Analyze Request and Detect Platform

**Purpose**: Determine which ticketing platform to use

**Detection Logic**:
```bash
# Check for platform indicators
USER_INPUT="$1"

# GitHub indicators
if echo "$USER_INPUT" | grep -qi "github"; then
  PLATFORM="github"
# JIRA indicators
elif echo "$USER_INPUT" | grep -qi "jira"; then
  PLATFORM="jira"
# Auto-detect from context
elif git remote -v | grep -q "github.com"; then
  PLATFORM="github"
elif [ -f "pyproject.toml" ] || [ -f "package.json" ]; then
  # Could be either - ask user
  read -p "Use GitHub issues or JIRA tickets? (github/jira): " PLATFORM
fi

echo "Using platform: $PLATFORM"
```

**Platform Detection Summary**:

| Indicator | Platform |
|-----------|----------|
| User mentions "GitHub" | github |
| User mentions "JIRA" | jira |
| Remote URL is github.com | github |
| Project has JIRA integration | jira |
| Context suggests specific platform | detected from context |

### Step 2: Determine Labels/Issue Type Using git-issue-labeler

**Purpose**: Use git-issue-labeler framework to assign GitHub default labels or JIRA issue types

**Label Detection Logic** (Delegated to git-issue-labeler):
```bash
# git-issue-labeler will analyze the ticket title and description
# and determine appropriate labels for GitHub or issue types for JIRA
# Examples:
# - "Fix login error" → GitHub labels: bug
# - "Add dark mode" → GitHub labels: enhancement, good first issue
# - "Update documentation" → GitHub labels: documentation
# - JIRA: "Fix authentication" → Issue type: Bug
# - JIRA: "Add feature" → Issue type: Story
```

**Implementation**:
```bash
# For GitHub: git-issue-labeler returns GitHub default labels
# For JIRA: git-issue-labeler suggests issue type (Task, Story, Bug)
LABELS=$(git-issue-labeler --platform github --content "$TICKET_TITLE")

echo "Labels assigned: $LABELS"
```

### Step 3: Create Ticket (Platform-Specific)

**Purpose**: Create a new ticket in the appropriate platform with labels from git-issue-labeler

#### GitHub Ticket Creation:
```bash
# Get current authenticated GitHub user
GITHUB_USER=$(gh api user --jq '.login')

# Create GitHub issue with labels from git-issue-labeler
ISSUE_OUTPUT=$(gh issue create \
  --title "<Ticket Title>" \
  --body "<Ticket Description>" \
  --label "$LABELS" \
  --assignee @me)

# Extract issue number and URL
ISSUE_NUMBER=$(echo "$ISSUE_OUTPUT" | grep -oE '#[0-9]+')
ISSUE_URL=$(gh issue view "$ISSUE_NUMBER" --json url --jq '.url')
```

**GitHub Issue Body Template**:
```markdown
## Description
<Detailed description of the issue>

## Type
<bug | feature | enhancement | documentation | task>

## Labels
- <label1>
- <label2>
- <label3>

## Context
<Additional context or background information>

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3

## Notes
<Additional notes or constraints>
```

#### JIRA Ticket Creation:

**Prerequisites**: Use `jira-git-integration` framework for JIRA utilities

```bash
# Get JIRA resources (from jira-git-integration)
CLOUD_ID=$(atlassian_getAccessibleAtlassianResources | jq -r '.[0].id')
PROJECT_KEY="<PROJECT_KEY>"  # e.g., IBIS
USER_ACCOUNT_ID=$(atlassian_atlassianUserInfo | jq -r '.account_id')

# Create JIRA ticket
ISSUE_OUTPUT=$(atlassian_createJiraIssue \
  --cloudId "$CLOUD_ID" \
  --projectKey "$PROJECT_KEY" \
  --issueTypeName "<Task | Story | Bug>" \
  --summary "<Ticket Title>" \
  --description "<Ticket Description>" \
  --assignee_account_id "$USER_ACCOUNT_ID")

# Extract ticket key
TICKET_KEY=$(echo "$ISSUE_OUTPUT" | jq -r '.key')
TICKET_URL="https://company.atlassian.net/browse/${TICKET_KEY}"
```

### Step 4: Generate Branch Name

**Purpose**: Create a consistent branch name from ticket

**Branch Naming Conventions**:

| Platform | Format | Example |
|----------|--------|----------|
| GitHub | `issue-<number>` or `feature/<number>-<title>` | `issue-123` or `feature/123-add-login` |
| JIRA | `PROJECT-NUM` or `feature/PROJECT-NUM` | `IBIS-101` or `feature/IBIS-101` |

**Implementation**:
```bash
# Generate branch name based on platform
if [ "$PLATFORM" = "github" ]; then
  # GitHub format
  BRANCH_NAME="issue-${ISSUE_NUMBER}"
  # Or descriptive format
  # BRANCH_NAME="feature/${ISSUE_NUMBER}-$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | head -c 30)"

elif [ "$PLATFORM" = "jira" ]; then
  # JIRA format
  BRANCH_NAME="${TICKET_KEY}"
  # Or descriptive format
  # BRANCH_NAME="feature/${TICKET_KEY}"
fi

echo "Branch name: $BRANCH_NAME"
```

**Branch Naming Rules**:
- Use lowercase
- Replace spaces with hyphens
- Include ticket number/key for traceability
- Keep branch names under 72 characters
- Use semantic prefixes (feature/, bugfix/, hotfix/) when appropriate

### Step 5: Create Branch

**Purpose**: Create and checkout new git branch

**Implementation**:
```bash
# Check if branch already exists
if git branch | grep -q "$BRANCH_NAME"; then
  echo "Branch $BRANCH_NAME already exists."
  read -p "Switch to existing branch? (y/n): " SWITCH_BRANCH
  if [ "$SWITCH_BRANCH" = "y" ]; then
    git checkout "$BRANCH_NAME"
  else
    echo "Aborting."
    exit 1
  fi
else
  # Create and checkout new branch
  git checkout -b "$BRANCH_NAME"
  echo "✅ Created and checked out branch: $BRANCH_NAME"
fi
```

**Branch Verification**:
```bash
# Verify we're on the correct branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" = "$BRANCH_NAME" ]; then
  echo "✅ Confirmed on branch: $BRANCH_NAME"
else
  echo "❌ Error: Not on expected branch"
  exit 1
fi
```

### Step 6: Create PLAN.md

**Purpose**: Generate a comprehensive plan document for the work

**PLAN.md Template**:
```markdown
# Plan: <Ticket Title>

## Overview
Brief description of what this issue implements or fixes.

## Ticket Reference
<if github>
- Issue: #<ISSUE_NUMBER>
- URL: <ISSUE_URL>
- Labels: <label1>, <label2>
</if>

<if jira>
- Ticket: <TICKET_KEY>
- URL: <TICKET_URL>
- Type: <Task | Story | Bug>
</if>

## Files to Modify
1. `src/path/to/file1.ts` - Description of changes
2. `src/path/to/file2.tsx` - Description of changes
3. `src/path/to/file3.ts` - Description of changes
4. `README.md` - Documentation updates (if applicable)

## Approach
Detailed steps or methodology for implementation:

### Phase 1: Analysis
- <Step 1>
- <Step 2>

### Phase 2: Implementation
- <Step 1>
- <Step 2>
- <Step 3>

### Phase 3: Testing
- <Step 1>
- <Step 2>

## Success Criteria
- [ ] All files modified correctly
- [ ] No build errors
- [ ] All tests pass
- [ ] Code review completed
- [ ] Documentation updated

## Notes
Any additional notes, constraints, or considerations.

## Dependencies
- [ ] External dependency 1
- [ ] External dependency 2

## Risks
- <Risk 1>: Mitigation strategy
- <Risk 2>: Mitigation strategy
```

**Implementation**:
```bash
# Create PLAN.md file
cat > PLAN.md <<EOF
# Plan: $TICKET_TITLE

## Overview
$OVERVIEW_TEXT

## Ticket Reference
<platform-specific references>

## Files to Modify
<list of files>

## Approach
<implementation steps>

## Success Criteria
- [ ] All files modified correctly
- [ ] No build errors
- [ ] All tests pass

## Notes
<additional notes>
EOF

echo "✅ Created PLAN.md"
```

### Step 7: Commit PLAN.md Using git-semantic-commits

**Purpose**: Commit PLAN.md as the first commit on the new branch with semantic formatting

**Implementation**:
```bash
# Stage PLAN.md
git add PLAN.md

# Format commit message using git-semantic-commits
if [ "$PLATFORM" = "github" ]; then
  COMMIT_MSG=$(git-semantic-commits --type docs --scope plan --subject "Add PLAN.md for #${ISSUE_NUMBER}")
  git commit -m "$COMMIT_MSG"
elif [ "$PLATFORM" = "jira" ]; then
  COMMIT_MSG=$(git-semantic-commits --type docs --scope plan --subject "Add PLAN.md for ${TICKET_KEY}")
  git commit -m "$COMMIT_MSG"
fi

# Verify commit
git log --oneline -1

echo "✅ Committed PLAN.md with semantic format"
```

### Step 8: Update Issue with Commit Progress Using git-issue-updater

**Purpose**: Add progress comment to GitHub issue or JIRA ticket with commit details

**Implementation**:
```bash
# Update issue with commit progress using git-issue-updater
if [ "$PLATFORM" = "github" ]; then
  git-issue-updater --issue "$ISSUE_NUMBER" --platform github
elif [ "$PLATFORM" = "jira" ]; then
  git-issue-updater --ticket "$TICKET_KEY" --platform jira
fi

echo "✅ Issue updated with progress comment"
```

### Step 9: Push Branch to Remote

**Purpose**: Push the new branch to the remote repository

**Implementation**:
```bash
# Push branch with upstream tracking
git push -u origin "$BRANCH_NAME"

# Verify push success
if [ $? -eq 0 ]; then
  echo "✅ Branch pushed to remote"
  echo "   Remote: origin/$BRANCH_NAME"
else
  echo "❌ Failed to push branch"
  exit 1
fi
```

**Branch URL Display**:
```bash
# Construct and display branch URL
REMOTE_URL=$(git remote get-url origin)
BRANCH_URL="${REMOTE_URL%.git}/tree/${BRANCH_NAME}"

echo ""
echo "Branch URL: $BRANCH_URL"
```

### Step 9: Display Summary

**Purpose**: Show user all of work completed with framework skill usage

**Summary Template**:
```
✅ Workflow completed successfully!

**Frameworks Used**:
- `git-issue-labeler`: Labels assigned
- `git-semantic-commits`: Commit message formatted
- `git-issue-updater`: Issue updated with progress
- `jira-git-integration`: JIRA operations (if applicable)

**Ticket Details**:
<if github>
- Issue: #<ISSUE_NUMBER>
- URL: <ISSUE_URL>
- Labels: <labels> (via git-issue-labeler)
</if>

<if jira>
- Ticket: <TICKET_KEY>
- URL: <TICKET_URL>
- Type: <Task | Story | Bug> (via git-issue-labeler)
</if>

**Branch**:
- Name: $BRANCH_NAME
- Remote: origin/$BRANCH_NAME
- URL: <branch-url>

**PLAN.md**:
- Created: Yes
- Committed: Yes (with semantic format via git-semantic-commits)
- Pushed: Yes

**Issue Update**:
- Comment added: Yes (via git-issue-updater)
- User: <commit-author>
- Date: <commit-date>
- Time: <commit-time>

**Next Steps**:
1. Review and update PLAN.md as needed
2. Start implementation following plan
3. Make commits with clear messages (use git-semantic-commits)
4. Run quality checks (linting, tests, builds)
5. Update issue with progress (use git-issue-updater)
6. Create pull request when implementation is complete

**Ready to start implementation! 🚀**
```
✅ Workflow completed successfully!

**Ticket Details**:
<if github>
- Issue: #<ISSUE_NUMBER>
- URL: <ISSUE_URL>
- Labels: <label1>, <label2>
</if>

<if jira>
- Ticket: <TICKET_KEY>
- URL: <TICKET_URL>
- Type: <Task | Story | Bug>
</if>

**Branch**:
- Name: $BRANCH_NAME
- Remote: origin/$BRANCH_NAME
- URL: <branch-url>

**PLAN.md**:
- Created: Yes
- Committed: Yes
- Pushed: Yes

**Next Steps**:
1. Review and update PLAN.md as needed
2. Start implementation following the plan
3. Make commits with clear messages
4. Run quality checks (linting, tests, builds)
5. Update this ticket with progress comments (optional)
6. Create pull request when implementation is complete

**Ready to start implementation! 🚀**
```

## Ticket Type Detection

### Bug/Defect Indicators
Keywords: `fix`, `error`, `doesn't work`, `broken`, `crash`, `fails`, `issue`, `problem`, `incorrect`, `wrong`, `bug`

### Feature Indicators
Keywords: `add`, `implement`, `create`, `new`, `support`, `introduce`, `build`, `develop`

### Enhancement Indicators
Keywords: `improve`, `optimize`, `refactor`, `update`, `enhance`, `better`, `faster`, `cleaner`

### Documentation Indicators
Keywords: `document`, `readme`, `docs`, `guide`, `explain`, `tutorial`, `wiki`, `comment`

### Task/Chore Indicators
Keywords: `setup`, `configure`, `deploy`, `clean`, `organize`, `maintenance`, `chore`, `update dependencies`

## Platform-Specific Considerations

### GitHub Issues
- Use labels (not issue types)
- Assign issues to yourself (`--assignee @me`)
- Issue numbers are numeric (e.g., #123)
- Use `#` prefix in references
- Supports emoji in descriptions

### JIRA Tickets
- Use issue types (Task, Story, Bug)
- Use project keys (e.g., IBIS, DA, ML)
- Ticket keys are PROJECT-NUM format (e.g., IBIS-101)
- Supports rich text descriptions
- Requires cloud ID for API calls

## Best Practices

- **Ticket Titles**: Be concise and descriptive (under 72 characters preferred)
- **Ticket Descriptions**: Include context, acceptance criteria, and files affected
- **Labels/Types**: Use appropriate categorization for discoverability
- **Branch Names**: Include ticket reference for traceability
- **PLAN.md First**: Always create PLAN.md as first commit
- **Remote Push**: Push branch immediately after committing PLAN.md
- **Auto-Checkout**: Always checkout to new branch automatically
- **Clear Messaging**: Provide clear confirmation at each step

## Common Issues

### Platform Not Detected

**Issue**: Cannot determine if using GitHub or JIRA

**Solution**:
```bash
# Ask user to specify platform
read -p "Which platform? (github/jira): " PLATFORM

# Or detect from context
if git remote -v | grep -q "github.com"; then
  PLATFORM="github"
fi
```

### Branch Already Exists

**Issue**: Branch with same name already exists

**Solution**:
```bash
# Ask user what to do
echo "Branch $BRANCH_NAME already exists."
echo "1. Switch to existing branch"
echo "2. Create with different name"
echo "3. Cancel"

read -p "Choose option (1/2/3): " CHOICE

case $CHOICE in
  1)
    git checkout "$BRANCH_NAME"
    ;;
  2)
    read -p "Enter new branch name: " NEW_BRANCH_NAME
    git checkout -b "$NEW_BRANCH_NAME"
    BRANCH_NAME="$NEW_BRANCH_NAME"
    ;;
  3)
    echo "Cancelled."
    exit 0
    ;;
esac
```

### Push Fails

**Issue**: Branch push fails due to network or authentication

**Solution**:
```bash
# Check git remote
git remote -v

# Verify authentication
if [ "$PLATFORM" = "github" ]; then
  gh auth status
fi

# Retry push
git push -u origin "$BRANCH_NAME"
```

## Troubleshooting Checklist

Before creating ticket:
- [ ] Platform is detected (GitHub or JIRA)
- [ ] Ticket type/labels are determined
- [ ] User has appropriate permissions
- [ ] Remote repository is configured

After ticket creation:
- [ ] Ticket number/key is captured
- [ ] Ticket URL is accessible
- [ ] Ticket is assigned to correct user
- [ ] Labels/issue types are correct

After branch creation:
- [ ] Branch name is generated correctly
- [ ] Branch is checked out successfully
- [ ] Current branch is confirmed
- [ ] No uncommitted changes from previous work

After PLAN.md creation:
- [ ] PLAN.md file is created
- [ ] PLAN.md follows template structure
- [ ] All sections are populated

After commit:
- [ ] PLAN.md is staged
- [ ] Commit message is clear and includes ticket reference
- [ ] Commit is successful

After push:
- [ ] Branch is pushed to remote
- [ ] Branch is accessible via URL
- [ ] Upstream tracking is set

## Related Commands

```bash
# Get current authenticated GitHub user
gh api user --jq '.login'

# Create GitHub issue
gh issue create --title "Title" --body "Description" --label "bug,enhancement" --assignee @me

# View GitHub issue
gh issue view <issue-number>

# Create and checkout branch
git checkout -b <branch-name>

# Commit changes
git add <files>
git commit -m "Commit message"

# Push branch with upstream
git push -u origin <branch-name>

# View branches
git branch -a

# Check git status
git status
```

## Relevant Skills

**Framework Skills Used**:
- `git-issue-labeler` - For GitHub default label assignment
- `git-semantic-commits` - For semantic commit message formatting
- `git-issue-updater` - For updating issues with commit progress
- `jira-git-integration` - For JIRA utilities and operations

**Skills that use this framework**:
- `git-issue-creator` - GitHub issue creation with semantic commit formatting
- `jira-git-workflow` - JIRA ticket creation with semantic commit formatting

Additional related skills:
- `pr-creation-workflow` - For PR creation workflows
- `nextjs-pr-workflow` - For Next.js-specific PR workflows
- `git-pr-creator` - For Git PR creation with JIRA integration
