---
name: github
description: Comprehensive GitHub operations via gh CLI. Manage repositories, issues, pull requests, Actions workflows, code security, discussions, projects, gists, notifications, and more. Use for any GitHub-related task including creating PRs, reviewing code, managing issues, monitoring CI/CD, and analyzing security alerts.
---

# GitHub Operations Skill

Complete GitHub integration via the `gh` CLI. This skill provides 90+ operations covering all aspects of GitHub: repositories, issues, pull requests, Actions, security, discussions, projects, notifications, and more.

## Prerequisites

- **gh CLI installed**: Install from https://cli.github.com/
- **Authenticated**: Run `gh auth login` to authenticate
- **Verify**: Run `gh auth status` to confirm authentication

## Quick Reference

### Repository Operations

| Operation | Command |
|-----------|---------|
| Clone repo | `gh repo clone owner/repo` |
| Create repo | `gh repo create name --public/--private` |
| Fork repo | `gh repo fork owner/repo` |
| View repo | `gh repo view owner/repo` |
| List repos | `gh repo list owner` |
| Search repos | `gh search repos "query"` |

### Issue Operations

| Operation | Command |
|-----------|---------|
| Create issue | `gh issue create --title "..." --body "..."` |
| List issues | `gh issue list` |
| View issue | `gh issue view 123` |
| Close issue | `gh issue close 123` |
| Reopen issue | `gh issue reopen 123` |
| Comment | `gh issue comment 123 --body "..."` |

### Pull Request Operations

| Operation | Command |
|-----------|---------|
| Create PR | `gh pr create --title "..." --body "..."` |
| List PRs | `gh pr list` |
| View PR | `gh pr view 123` |
| Checkout PR | `gh pr checkout 123` |
| Merge PR | `gh pr merge 123` |
| Review PR | `gh pr review 123 --approve/--request-changes` |

### Actions Workflows

| Operation | Command |
|-----------|---------|
| List workflows | `gh workflow list` |
| Run workflow | `gh workflow run workflow.yml` |
| List runs | `gh run list` |
| View run | `gh run view 123` |
| Watch run | `gh run watch 123` |
| Download artifacts | `gh run download 123` |

---

## Detailed Operations by Category

## 1. Repository Management (repos)

### Get File Contents
Read files or directories from a repository.

```bash
# Read a specific file
gh api repos/{owner}/{repo}/contents/{path} | jq -r '.content' | base64 -d

# Simpler: use gh to browse
gh browse --repo owner/repo -- path/to/file

# Get raw file content
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 --decode
```

### Search Repositories
```bash
# Search public repositories
gh search repos "query" --limit 10

# Search with filters
gh search repos "language:python stars:>1000" --limit 20

# Search in specific org
gh search repos "org:microsoft language:typescript"
```

### Search Code
```bash
# Search code across repositories
gh search code "function authenticate" --limit 10

# Search in specific repo
gh search code "TODO" --repo owner/repo

# Search with file extension filter
gh search code "import pandas" --extension py
```

### Create Repository
```bash
# Create public repo
gh repo create my-repo --public --description "My new repo"

# Create private repo with README
gh repo create my-repo --private --add-readme

# Create from template
gh repo create my-repo --template owner/template-repo

# Create in organization
gh repo create org/my-repo --public
```

### Fork Repository
```bash
# Fork to your account
gh repo fork owner/repo

# Fork and clone
gh repo fork owner/repo --clone

# Fork to organization
gh repo fork owner/repo --org my-org
```

### Manage Branches
```bash
# List branches
gh api repos/{owner}/{repo}/branches --jq '.[].name'

# Create branch (via git)
git checkout -b new-branch && git push -u origin new-branch

# Delete branch
gh api -X DELETE repos/{owner}/{repo}/git/refs/heads/{branch}
```

### Get Commits
```bash
# List recent commits
gh api repos/{owner}/{repo}/commits --jq '.[] | {sha: .sha[:7], message: .commit.message, author: .commit.author.name}'

# Get specific commit
gh api repos/{owner}/{repo}/commits/{sha}

# List commits on branch
gh api "repos/{owner}/{repo}/commits?sha={branch}" --jq '.[] | .sha[:7] + " " + .commit.message'
```

### Create/Update Files
```bash
# Create or update a file
gh api repos/{owner}/{repo}/contents/{path} \
  -X PUT \
  -f message="Commit message" \
  -f content="$(echo -n 'file content' | base64)" \
  -f branch="main"

# Update existing file (need sha)
SHA=$(gh api repos/{owner}/{repo}/contents/{path} --jq '.sha')
gh api repos/{owner}/{repo}/contents/{path} \
  -X PUT \
  -f message="Update file" \
  -f content="$(echo -n 'new content' | base64)" \
  -f sha="$SHA"
```

### Delete Files
```bash
# Delete a file
SHA=$(gh api repos/{owner}/{repo}/contents/{path} --jq '.sha')
gh api repos/{owner}/{repo}/contents/{path} \
  -X DELETE \
  -f message="Delete file" \
  -f sha="$SHA"
```

### Releases
```bash
# List releases
gh release list --repo owner/repo

# Get latest release
gh release view --repo owner/repo

# Get specific release
gh release view v1.0.0 --repo owner/repo

# Create release
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"

# Upload assets
gh release upload v1.0.0 ./dist/*.zip
```

### Tags
```bash
# List tags
gh api repos/{owner}/{repo}/tags --jq '.[].name'

# Get tag details
gh api repos/{owner}/{repo}/git/refs/tags/{tag}
```

### Repository Tree
```bash
# Get full repository tree
gh api repos/{owner}/{repo}/git/trees/main?recursive=1 --jq '.tree[] | select(.type=="blob") | .path'

# Get tree for specific directory
gh api repos/{owner}/{repo}/contents/{path} --jq '.[] | .name + (if .type == "dir" then "/" else "" end)'
```

---

## 2. Issues Management (issues)

### Create Issue
```bash
# Basic issue creation
gh issue create --title "Bug: Something is broken" --body "Description here"

# With labels and assignees
gh issue create --title "Feature request" --body "Details" --label "enhancement" --assignee "@me"

# With milestone
gh issue create --title "Task" --body "Description" --milestone "v1.0"

# Interactive mode
gh issue create
```

### List Issues
```bash
# List open issues
gh issue list

# List with filters
gh issue list --state closed --label "bug" --limit 50

# List assigned to me
gh issue list --assignee "@me"

# List by author
gh issue list --author username

# Search issues
gh issue list --search "is:open label:bug sort:updated-desc"
```

### Read Issue
```bash
# View issue details
gh issue view 123

# View with comments
gh issue view 123 --comments

# JSON output for parsing
gh issue view 123 --json title,body,state,labels,assignees
```

### Update Issue
```bash
# Edit title/body
gh issue edit 123 --title "New title" --body "New body"

# Add labels
gh issue edit 123 --add-label "priority:high,needs-review"

# Remove labels
gh issue edit 123 --remove-label "wontfix"

# Assign users
gh issue edit 123 --add-assignee username1,username2

# Set milestone
gh issue edit 123 --milestone "v2.0"
```

### Close/Reopen Issues
```bash
# Close issue
gh issue close 123

# Close with comment
gh issue close 123 --comment "Fixed in PR #456"

# Close as not planned
gh issue close 123 --reason "not planned"

# Reopen issue
gh issue reopen 123
```

### Issue Comments
```bash
# Add comment
gh issue comment 123 --body "This is my comment"

# Add comment from file
gh issue comment 123 --body-file ./comment.md

# Edit comment (via API)
gh api repos/{owner}/{repo}/issues/comments/{comment_id} \
  -X PATCH \
  -f body="Updated comment"
```

### Search Issues
```bash
# Search across all repos
gh search issues "memory leak" --limit 20

# Search in specific repo
gh search issues "bug" --repo owner/repo

# Advanced search
gh search issues "is:open is:issue label:bug author:username"
```

### Labels
```bash
# List labels
gh label list

# Create label
gh label create "priority:critical" --color FF0000 --description "Critical priority"

# Edit label
gh label edit "bug" --new-name "type:bug" --color 00FF00

# Delete label
gh label delete "old-label" --yes
```

### Sub-Issues (Parent/Child)
```bash
# Add sub-issue relationship via API
gh api graphql -f query='
mutation {
  addSubIssue(input: {issueId: "PARENT_ID", subIssueId: "CHILD_ID"}) {
    issue { number }
  }
}'
```

---

## 3. Pull Requests (pull_requests)

### Create Pull Request
```bash
# Basic PR creation
gh pr create --title "Add new feature" --body "Description"

# From specific branch to base
gh pr create --base main --head feature-branch --title "Title"

# Draft PR
gh pr create --title "WIP: Feature" --draft

# With reviewers
gh pr create --title "Feature" --reviewer user1,user2

# From fork
gh pr create --repo upstream/repo --head myuser:feature-branch
```

### List Pull Requests
```bash
# List open PRs
gh pr list

# List with filters
gh pr list --state merged --base main --limit 50

# List by author
gh pr list --author "@me"

# Search PRs
gh pr list --search "is:open review:required"
```

### Read Pull Request
```bash
# View PR details
gh pr view 123

# View with diff
gh pr diff 123

# View specific file diff
gh pr diff 123 -- path/to/file

# JSON output
gh pr view 123 --json title,body,state,reviewDecision,mergeable
```

### Update Pull Request
```bash
# Edit title/body
gh pr edit 123 --title "New title" --body "New body"

# Add labels
gh pr edit 123 --add-label "needs-review"

# Add reviewers
gh pr edit 123 --add-reviewer user1,team/reviewers

# Mark ready for review
gh pr ready 123
```

### Merge Pull Request
```bash
# Merge with merge commit
gh pr merge 123 --merge

# Squash merge
gh pr merge 123 --squash

# Rebase merge
gh pr merge 123 --rebase

# Auto-merge when checks pass
gh pr merge 123 --auto --squash

# Delete branch after merge
gh pr merge 123 --delete-branch
```

### PR Reviews
```bash
# Approve PR
gh pr review 123 --approve

# Request changes
gh pr review 123 --request-changes --body "Please fix X"

# Comment without approval
gh pr review 123 --comment --body "Looks good overall"

# View reviews
gh pr view 123 --json reviews --jq '.reviews[] | {author: .author.login, state: .state}'
```

### PR Comments
```bash
# Add comment to PR
gh pr comment 123 --body "Comment text"

# Add review comment on specific line (via API)
gh api repos/{owner}/{repo}/pulls/{pr}/comments \
  -f body="Review comment" \
  -f commit_id="SHA" \
  -f path="file.py" \
  -F line=42
```

### Update PR Branch
```bash
# Update branch with base
gh pr update-branch 123

# Via API
gh api repos/{owner}/{repo}/pulls/{pr}/update-branch -X PUT
```

### Search Pull Requests
```bash
# Search PRs
gh search prs "fix bug" --limit 20

# Search with filters
gh search prs "is:open review:approved base:main"
```

### Checkout PR
```bash
# Checkout PR locally
gh pr checkout 123

# Checkout to specific branch name
gh pr checkout 123 --branch my-review-branch
```

---

## 4. GitHub Actions (actions)

### List Workflows
```bash
# List all workflows
gh workflow list

# Show disabled workflows too
gh workflow list --all
```

### Run Workflow
```bash
# Trigger workflow
gh workflow run workflow.yml

# With inputs
gh workflow run workflow.yml -f param1=value1 -f param2=value2

# On specific branch
gh workflow run workflow.yml --ref feature-branch
```

### List Workflow Runs
```bash
# List recent runs
gh run list

# Filter by workflow
gh run list --workflow=ci.yml

# Filter by status
gh run list --status failure --limit 10

# Filter by branch
gh run list --branch main
```

### View Workflow Run
```bash
# View run details
gh run view 123456789

# View with job details
gh run view 123456789 --verbose

# JSON output
gh run view 123456789 --json status,conclusion,jobs
```

### Get Run Logs
```bash
# View logs interactively
gh run view 123456789 --log

# Download logs
gh run view 123456789 --log > run.log

# Failed jobs only
gh run view 123456789 --log-failed
```

### Watch Running Workflow
```bash
# Watch run until completion
gh run watch 123456789

# Exit with run's exit code
gh run watch 123456789 --exit-status
```

### Rerun Workflows
```bash
# Rerun entire workflow
gh run rerun 123456789

# Rerun failed jobs only
gh run rerun 123456789 --failed

# Rerun with debug logging
gh run rerun 123456789 --debug
```

### Cancel Workflow Run
```bash
# Cancel running workflow
gh run cancel 123456789
```

### Download Artifacts
```bash
# Download all artifacts
gh run download 123456789

# Download specific artifact
gh run download 123456789 --name artifact-name

# Download to specific directory
gh run download 123456789 --dir ./artifacts
```

### List Artifacts
```bash
# List run artifacts
gh api repos/{owner}/{repo}/actions/runs/{run_id}/artifacts --jq '.artifacts[] | {name: .name, size: .size_in_bytes}'
```

### Delete Workflow Run Logs
```bash
gh api -X DELETE repos/{owner}/{repo}/actions/runs/{run_id}/logs
```

### Workflow Run Usage
```bash
gh api repos/{owner}/{repo}/actions/runs/{run_id}/timing
```

### List Jobs in Run
```bash
gh api repos/{owner}/{repo}/actions/runs/{run_id}/jobs --jq '.jobs[] | {name: .name, status: .status, conclusion: .conclusion}'
```

### Get Job Logs
```bash
gh api repos/{owner}/{repo}/actions/jobs/{job_id}/logs
```

---

## 5. Code Security (code_security)

### Code Scanning Alerts
```bash
# List code scanning alerts
gh api repos/{owner}/{repo}/code-scanning/alerts --jq '.[] | {number: .number, rule: .rule.id, severity: .rule.severity, state: .state}'

# Get specific alert
gh api repos/{owner}/{repo}/code-scanning/alerts/{alert_number}

# Filter by state
gh api "repos/{owner}/{repo}/code-scanning/alerts?state=open" --jq '.[] | {number: .number, rule: .rule.id}'

# Filter by severity
gh api "repos/{owner}/{repo}/code-scanning/alerts?severity=critical,high"
```

### Dismiss Code Scanning Alert
```bash
gh api repos/{owner}/{repo}/code-scanning/alerts/{alert_number} \
  -X PATCH \
  -f state="dismissed" \
  -f dismissed_reason="false positive"
```

---

## 6. Dependabot (dependabot)

### List Dependabot Alerts
```bash
# List all alerts
gh api repos/{owner}/{repo}/dependabot/alerts --jq '.[] | {number: .number, package: .dependency.package.name, severity: .security_advisory.severity}'

# Filter by severity
gh api "repos/{owner}/{repo}/dependabot/alerts?severity=critical,high"

# Filter by state
gh api "repos/{owner}/{repo}/dependabot/alerts?state=open"
```

### Get Specific Alert
```bash
gh api repos/{owner}/{repo}/dependabot/alerts/{alert_number}
```

### Dismiss Dependabot Alert
```bash
gh api repos/{owner}/{repo}/dependabot/alerts/{alert_number} \
  -X PATCH \
  -f state="dismissed" \
  -f dismissed_reason="tolerable_risk"
```

---

## 7. Secret Scanning (secret_protection)

### List Secret Scanning Alerts
```bash
# List alerts
gh api repos/{owner}/{repo}/secret-scanning/alerts --jq '.[] | {number: .number, secret_type: .secret_type, state: .state}'

# Filter by state
gh api "repos/{owner}/{repo}/secret-scanning/alerts?state=open"
```

### Get Secret Scanning Alert
```bash
gh api repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}
```

### Update Secret Scanning Alert
```bash
gh api repos/{owner}/{repo}/secret-scanning/alerts/{alert_number} \
  -X PATCH \
  -f state="resolved" \
  -f resolution="revoked"
```

---

## 8. Security Advisories (security_advisories)

### List Global Advisories
```bash
# List recent advisories
gh api /advisories --jq '.[] | {ghsa_id: .ghsa_id, severity: .severity, summary: .summary}'

# Filter by ecosystem
gh api "/advisories?ecosystem=npm" --jq '.[] | .ghsa_id'

# Filter by severity
gh api "/advisories?severity=critical"
```

### Get Specific Advisory
```bash
gh api /advisories/{ghsa_id}
```

### Repository Security Advisories
```bash
# List repo advisories
gh api repos/{owner}/{repo}/security-advisories

# Create draft advisory
gh api repos/{owner}/{repo}/security-advisories \
  -X POST \
  -f summary="Security issue" \
  -f description="Details" \
  -f severity="high"
```

---

## 9. Discussions (discussions)

### List Discussions
```bash
# Via GraphQL (discussions require GraphQL)
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    discussions(first: 10) {
      nodes {
        number
        title
        author { login }
        category { name }
      }
    }
  }
}' -f owner="{owner}" -f repo="{repo}"
```

### Get Discussion
```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    discussion(number: $number) {
      title
      body
      author { login }
      comments(first: 10) {
        nodes { body author { login } }
      }
    }
  }
}' -f owner="{owner}" -f repo="{repo}" -F number=123
```

### Create Discussion
```bash
# First get category ID
CATEGORY_ID=$(gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    discussionCategories(first: 10) {
      nodes { id name }
    }
  }
}' -f owner="{owner}" -f repo="{repo}" --jq '.data.repository.discussionCategories.nodes[0].id')

# Then create discussion
gh api graphql -f query='
mutation($repoId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
  createDiscussion(input: {repositoryId: $repoId, categoryId: $categoryId, title: $title, body: $body}) {
    discussion { number url }
  }
}'
```

### Discussion Categories
```bash
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    discussionCategories(first: 20) {
      nodes { id name description }
    }
  }
}' -f owner="{owner}" -f repo="{repo}"
```

---

## 10. Gists (gists)

### Create Gist
```bash
# Create public gist
gh gist create file.py --public --desc "My Python script"

# Create secret gist
gh gist create file1.py file2.py --desc "Multiple files"

# Create from stdin
echo "content" | gh gist create --filename "test.txt"
```

### List Gists
```bash
# List your gists
gh gist list

# List with limit
gh gist list --limit 50

# Public only
gh gist list --public
```

### View Gist
```bash
# View gist
gh gist view {gist_id}

# View specific file
gh gist view {gist_id} --filename file.py

# Raw content
gh gist view {gist_id} --raw
```

### Edit Gist
```bash
# Edit gist interactively
gh gist edit {gist_id}

# Add file to gist
gh gist edit {gist_id} --add newfile.py

# Remove file
gh gist edit {gist_id} --remove oldfile.py
```

### Delete Gist
```bash
gh gist delete {gist_id}
```

### Clone Gist
```bash
gh gist clone {gist_id}
```

---

## 11. Projects (projects)

### List Projects
```bash
# User projects
gh project list

# Organization projects
gh project list --owner org-name

# Closed projects too
gh project list --closed
```

### View Project
```bash
# View project details
gh project view {number}

# JSON output
gh project view {number} --format json
```

### Create Project
```bash
# Create project
gh project create --title "My Project"

# In organization
gh project create --title "Team Project" --owner org-name
```

### Project Items
```bash
# List items in project
gh project item-list {number}

# Add issue to project
gh project item-add {number} --url https://github.com/owner/repo/issues/123

# Add PR to project
gh project item-add {number} --url https://github.com/owner/repo/pull/456
```

### Edit Project Item
```bash
# Archive item
gh project item-archive {project_number} --id {item_id}

# Delete item
gh project item-delete {project_number} --id {item_id}

# Edit field value
gh project item-edit --project-id {project_id} --id {item_id} --field-id {field_id} --text "value"
```

### Project Fields
```bash
# List fields
gh project field-list {number}

# Create field
gh project field-create {number} --name "Priority" --data-type SINGLE_SELECT
```

---

## 12. Notifications (notifications)

### List Notifications
```bash
# List unread notifications
gh api notifications --jq '.[] | {id: .id, reason: .reason, title: .subject.title, repo: .repository.full_name}'

# All notifications
gh api "notifications?all=true"

# Participating only
gh api "notifications?participating=true"
```

### Mark as Read
```bash
# Mark specific notification as read
gh api -X PATCH notifications/threads/{thread_id}

# Mark all as read
gh api -X PUT notifications

# Mark repo notifications as read
gh api -X PUT repos/{owner}/{repo}/notifications
```

### Notification Details
```bash
gh api notifications/threads/{thread_id}
```

### Manage Subscription
```bash
# Subscribe to thread
gh api -X PUT notifications/threads/{thread_id}/subscription \
  -f ignored=false

# Unsubscribe
gh api -X PUT notifications/threads/{thread_id}/subscription \
  -f ignored=true

# Delete subscription
gh api -X DELETE notifications/threads/{thread_id}/subscription
```

---

## 13. Users (users)

### Get Current User
```bash
gh api user
```

### Search Users
```bash
# Search users
gh search users "username" --limit 10

# Filter by type
gh search users "type:user location:USA"

# Search organizations
gh search users "type:org language:python"
```

### Get User Profile
```bash
gh api users/{username}
```

---

## 14. Organizations (organizations)

### Search Organizations
```bash
gh search repos "org:{org-name}" --limit 10
```

### Get Organization Details
```bash
gh api orgs/{org}
```

### List Org Members
```bash
gh api orgs/{org}/members --jq '.[].login'
```

### List Org Repos
```bash
gh repo list {org} --limit 100
```

### Get Teams
```bash
gh api orgs/{org}/teams --jq '.[].name'
```

### Get Team Members
```bash
gh api orgs/{org}/teams/{team_slug}/members --jq '.[].login'
```

---

## 15. Stargazers (stargazers)

### Star Repository
```bash
gh api -X PUT user/starred/{owner}/{repo}
```

### Unstar Repository
```bash
gh api -X DELETE user/starred/{owner}/{repo}
```

### List Starred Repos
```bash
# Your starred repos
gh api user/starred --jq '.[].full_name'

# User's starred repos
gh api users/{username}/starred --jq '.[].full_name'
```

### Check if Starred
```bash
# Returns 204 if starred, 404 if not
gh api user/starred/{owner}/{repo}
```

---

## 16. Context Information (context)

### Get Authenticated User
```bash
gh api user --jq '{login: .login, name: .name, email: .email, company: .company}'
```

### Authentication Status
```bash
gh auth status
```

### Check Scopes
```bash
gh auth status --show-token 2>&1 | grep -i scope
```

---

## Error Handling

### Common Errors and Solutions

| Error | Solution |
|-------|----------|
| `gh: command not found` | Install gh CLI: https://cli.github.com/ |
| `not logged in` | Run `gh auth login` |
| `HTTP 404` | Check repo/resource exists and you have access |
| `HTTP 403` | Check permissions/scopes, may need `gh auth refresh` |
| `HTTP 422` | Invalid parameters, check API docs |
| `rate limit exceeded` | Wait or authenticate for higher limits |

### Check Rate Limits
```bash
gh api rate_limit --jq '.resources.core | {limit: .limit, remaining: .remaining, reset: .reset}'
```

---

## Script Integration

This skill includes helper scripts in the `scripts/` directory:

- `github_helper.py` - Python utilities for complex operations
- `batch_operations.sh` - Bash scripts for bulk actions

See `reference.md` for complete documentation.

## Notes

- Always verify authentication before operations: `gh auth status`
- Use `--json` flag for programmatic output
- Use `--jq` for filtering JSON responses
- GraphQL API is required for some features (discussions, projects v2)
- Rate limits apply: 5000 requests/hour authenticated, 60/hour unauthenticated
