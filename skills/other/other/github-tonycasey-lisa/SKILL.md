---
name: github
description: "GitHub and Git workflow helpers, Issues and Projects v2 management via gh CLI; triggers on 'github', 'create issue', 'list issues', 'github project', 'project board', 'sync tasks', 'create pr', 'pr checks', 'retrigger tests', 'bump version', 'push'."
---

## Purpose

Model-neutral helper for GitHub and Git workflows including Issues, Projects v2, PR management, CI triggers, and version bumping. Uses the `gh` CLI.

## Triggers

Use when the user says:
- "create a github issue", "create issue", "new issue"
- "list github issues", "show issues", "open issues"
- "close issue", "reopen issue", "assign issue"
- "github project", "project board", "kanban"
- "add to project", "update project field", "move to column"
- "sync tasks with github", "import github issues", "export tasks to github"
- "create a pr", "check pr status", "retrigger tests", "toggle test label", "pr checks", "bump version", "push to remote"

## Configuration

Uses existing `gh` CLI authentication. Verify with:
```bash
gh auth status
```

Alternatively, set `GITHUB_TOKEN` environment variable for CI/headless environments.

## How to use

### Issues

#### List Issues
```bash
# List open issues
lisa github issues list --repo owner/repo

# List with filters
lisa github issues list --repo owner/repo --state open --labels bug,urgent --assignee @me --limit 20

# List all issues (including closed)
lisa github issues list --repo owner/repo --state all
```

#### Create Issue
```bash
# Basic issue
lisa github issues create --repo owner/repo --title "Bug: Login fails"

# With body and labels
lisa github issues create --repo owner/repo --title "Feature: Dark mode" --body "Add dark mode support" --labels enhancement,ui

# With assignee
lisa github issues create --repo owner/repo --title "Task" --assignee username
```

#### View Issue
```bash
lisa github issues view --repo owner/repo 123
```

#### Close/Reopen Issue
```bash
# Close as completed
lisa github issues close --repo owner/repo 123

# Close as not planned
lisa github issues close --repo owner/repo 123 --reason not_planned

# Reopen
lisa github issues reopen --repo owner/repo 123
```

#### Assign Issue
```bash
lisa github issues assign --repo owner/repo 123 --to username
lisa github issues assign --repo owner/repo 123 --to user1,user2
```

#### Label Issue
```bash
# Add labels
lisa github issues label --repo owner/repo 123 --add bug,priority-high

# Remove labels
lisa github issues label --repo owner/repo 123 --remove wontfix

# Add and remove
lisa github issues label --repo owner/repo 123 --add in-progress --remove backlog
```

### Projects v2

#### List Projects
```bash
lisa github projects list --repo owner/repo
lisa github projects list --repo owner/repo --limit 10
```

#### View Project
```bash
lisa github projects view --repo owner/repo 1
```

#### List Project Items
```bash
lisa github projects items --repo owner/repo 1
lisa github projects items --repo owner/repo 1 --limit 50
```

#### List Project Fields
```bash
# Get available fields and their options (useful for set-field)
lisa github projects fields --repo owner/repo 1
```

#### Add Issue to Project
```bash
# Add issue #123 to project #1
lisa github projects add --repo owner/repo 1 123
```

#### Update Project Field
```bash
# Set status field (e.g., move to "In Progress" column)
lisa github projects set-field --repo owner/repo 1 ITEM_ID --field Status --value "In Progress"

# Set priority
lisa github projects set-field --repo owner/repo 1 ITEM_ID --field Priority --value "High"
```

**Note:** Use `projects fields` to get valid field names and options, and `projects items` to get item IDs.

### Sync (Bidirectional Task Sync)

Sync Lisa tasks with GitHub Issues. Supports import, export, or bidirectional sync.

#### Import GitHub Issues as Lisa Tasks
```bash
# Import all open issues from repo
lisa github sync --repo owner/repo --import

# Import issues with specific labels
lisa github sync --repo owner/repo --import --labels task,feature

# Preview import without making changes
lisa github sync --repo owner/repo --import --dry-run

# Specify group ID for Lisa tasks (default: owner-repo)
lisa github sync --repo owner/repo --import --group my-project
```

#### Export Lisa Tasks to GitHub Issues
```bash
# Export unlinked tasks as new GitHub issues
lisa github sync --repo owner/repo --export

# Preview export
lisa github sync --repo owner/repo --export --dry-run
```

#### Bidirectional Sync
```bash
# Full two-way sync (import + export + status updates)
lisa github sync --repo owner/repo

# Preview all changes
lisa github sync --repo owner/repo --dry-run
```

#### Status Mapping

| Lisa Status | GitHub State | GitHub Labels |
|-------------|--------------|---------------|
| `ready`/`todo` | open | (none) |
| `in-progress` | open | `in-progress` |
| `blocked` | open | `blocked` |
| `done` | closed | (none) |

**Conflict Resolution:** When both Lisa and GitHub have changes, last-write-wins based on timestamps.

## I/O Contract (examples)

### Create Issue
```json
{
  "status": "ok",
  "action": "create",
  "issue": {
    "number": 123,
    "url": "https://github.com/owner/repo/issues/123",
    "title": "Bug: Login fails"
  }
}
```

### List Issues
```json
{
  "status": "ok",
  "action": "list",
  "issues": [
    {
      "number": 123,
      "title": "Bug: Login fails",
      "state": "open",
      "labels": ["bug"],
      "assignees": ["username"],
      "url": "https://github.com/owner/repo/issues/123",
      "createdAt": "2026-01-22T10:00:00Z",
      "updatedAt": "2026-01-22T10:00:00Z"
    }
  ],
  "total": 1
}
```

### View Issue
```json
{
  "status": "ok",
  "action": "view",
  "issue": {
    "number": 123,
    "title": "Bug: Login fails",
    "body": "Steps to reproduce...",
    "state": "open",
    "labels": ["bug"],
    "assignees": ["username"],
    "url": "https://github.com/owner/repo/issues/123",
    "createdAt": "2026-01-22T10:00:00Z",
    "updatedAt": "2026-01-22T10:00:00Z",
    "author": "reporter",
    "milestone": "v1.0"
  }
}
```

### List Projects
```json
{
  "status": "ok",
  "action": "list",
  "projects": [
    {
      "id": "PVT_kwDOABC123",
      "number": 1,
      "title": "Sprint Board",
      "url": "https://github.com/orgs/owner/projects/1",
      "closed": false,
      "shortDescription": "Current sprint tasks"
    }
  ],
  "total": 1
}
```

### Project Items
```json
{
  "status": "ok",
  "action": "items",
  "items": [
    {
      "id": "PVTI_abc123",
      "type": "ISSUE",
      "content": {
        "number": 123,
        "title": "Bug: Login fails",
        "url": "https://github.com/owner/repo/issues/123",
        "state": "OPEN"
      },
      "fieldValues": {
        "Status": "In Progress",
        "Priority": "High"
      }
    }
  ],
  "total": 1
}
```

### Project Fields
```json
{
  "status": "ok",
  "action": "fields",
  "fields": [
    {
      "id": "PVTF_abc123",
      "name": "Status",
      "dataType": "SINGLE_SELECT",
      "options": [
        { "id": "opt_1", "name": "Todo" },
        { "id": "opt_2", "name": "In Progress" },
        { "id": "opt_3", "name": "Done" }
      ]
    },
    {
      "id": "PVTF_def456",
      "name": "Priority",
      "dataType": "SINGLE_SELECT",
      "options": [
        { "id": "opt_a", "name": "Low" },
        { "id": "opt_b", "name": "Medium" },
        { "id": "opt_c", "name": "High" }
      ]
    }
  ]
}
```

### Sync Result
```json
{
  "status": "ok",
  "action": "sync",
  "direction": "bidirectional",
  "dryRun": false,
  "summary": {
    "imported": 3,
    "exported": 2,
    "updated": 1,
    "skipped": 5,
    "conflicts": 1
  },
  "imported": [
    { "title": "Bug: Login fails", "issueNumber": 123, "issueUrl": "https://github.com/owner/repo/issues/123" }
  ],
  "exported": [
    { "title": "Refactor auth module", "taskUuid": "abc123", "issueNumber": 456, "issueUrl": "https://github.com/owner/repo/issues/456" }
  ],
  "updated": [
    { "title": "Update docs", "taskUuid": "def789", "issueNumber": 101, "issueUrl": "https://github.com/owner/repo/issues/101" }
  ],
  "conflicts": [
    {
      "taskUuid": "ghi012",
      "taskTitle": "Fix tests",
      "issueNumber": 102,
      "reason": "Status mismatch: Lisa=\"in-progress\", GitHub=\"closed\"",
      "resolution": "remote",
      "localUpdatedAt": "2026-01-22T10:00:00Z",
      "remoteUpdatedAt": "2026-01-22T11:00:00Z"
    }
  ]
}
```

### Error
```json
{
  "status": "error",
  "error": "Not authenticated. Run: gh auth login"
}
```

## Workflow Examples

### Bug Triage Workflow
```bash
# 1. Create issue
lisa github issues create --repo owner/repo --title "Bug: Login fails" --labels bug,triage

# 2. Add to project board
lisa github projects add --repo owner/repo 1 123

# 3. Set initial status
lisa github projects set-field --repo owner/repo 1 ITEM_ID --field Status --value "Triage"

# 4. After investigation, update priority and move to backlog
lisa github issues label --repo owner/repo 123 --add priority-high --remove triage
lisa github projects set-field --repo owner/repo 1 ITEM_ID --field Status --value "Backlog"
```

### Sprint Planning Workflow
```bash
# List items in backlog
lisa github projects items --repo owner/repo 1 --limit 50

# Move selected items to sprint
lisa github projects set-field --repo owner/repo 1 ITEM_ID --field Status --value "Todo"
lisa github issues assign --repo owner/repo 123 --to developer
```

### Task Sync Workflow
```bash
# 1. Start of day: Import any new GitHub issues as Lisa tasks
lisa github sync --repo owner/repo --import

# 2. Work on tasks in Lisa (status updates tracked automatically)
lisa tasks update "Fix login bug" --status in-progress

# 3. End of day: Export new tasks and sync status changes
lisa github sync --repo owner/repo

# 4. Check what would sync before running
lisa github sync --repo owner/repo --dry-run
```

## Git Workflows

### Check PR Status
```bash
# View PR checks
gh pr checks <PR_NUMBER> --repo <owner/repo>

# View PR details
gh pr view <PR_NUMBER> --repo <owner/repo>
```

### Retrigger CI Tests
When a PR test fails and a fix is pushed, tests don't automatically re-run. Toggle the "TEST" label to trigger:

```bash
# Remove and re-add TEST label to trigger CI
gh pr edit <PR_NUMBER> --repo <owner/repo> --remove-label "TEST"
sleep 2
gh pr edit <PR_NUMBER> --repo <owner/repo> --add-label "TEST"
```

### Check CircleCI Pipeline Status

**Prerequisites:** Set `CIRCLE_TOKEN` environment variable, or have CircleCI CLI configured at `~/.circleci/cli.yml`.

```bash
# Get latest pipeline for a branch
curl -s -H "Circle-Token: ${CIRCLE_TOKEN}" \
  "https://circleci.com/api/v2/project/gh/<owner>/<repo>/pipeline?branch=<BRANCH>" \
  | jq '.items[0] | {number, state, created_at}'

# Get workflow status for a pipeline
curl -s -H "Circle-Token: ${CIRCLE_TOKEN}" \
  "https://circleci.com/api/v2/pipeline/<PIPELINE_ID>/workflow" \
  | jq '.items[] | {name, status}'
```

### Poll CI Until Completion
```bash
# Poll current branch
lisa pr checks <PR_NUMBER>

# Or use gh CLI directly
gh pr checks <PR_NUMBER> --watch
```

### Bump Version
Bump the semantic version in package.json before pushing:

```bash
# Bump minor version (default): 1.2.3 → 1.3.0
lisa bump-version

# Bump patch version: 1.2.3 → 1.2.4
lisa bump-version patch

# Bump major version: 1.2.3 → 2.0.0
lisa bump-version major
```

#### Configuration

Control version bumping via `LISA_AUTO_BUMP_VERSION` in `.lisa/.env`:

| Value | Behavior |
|-------|----------|
| `true` (default) | Enabled, defaults to `minor` bump |
| `false` | Disabled, bump commands are skipped |
| `patch` / `minor` / `major` | Enabled with that bump type as the default |

```bash
# In .lisa/.env:
LISA_AUTO_BUMP_VERSION=false        # Disable version bumping
LISA_AUTO_BUMP_VERSION=patch        # Default to patch bumps
```

A CLI argument always overrides the env default: `lisa bump-version major` bumps major regardless of the env setting.

### Workflow: Push with Version Bump

1. **Bump version** (default: minor):

   ```bash
   lisa bump-version
   ```

2. **Commit the version bump**:

   ```bash
   git add package.json
   git commit -m "chore: bump version to $(node -p "require('./package.json').version")"
   ```

3. **Push to remote**:

   ```bash
   git push
   ```

### Workflow: PR Test Failure

1. **Identify the failure** - Check CircleCI logs or GitHub checks
2. **Push a fix** - Commit and push the fix to the branch
3. **Retrigger tests** - Toggle the TEST label:

   ```bash
   gh pr edit <PR_NUMBER> --repo <owner/repo> --remove-label "TEST" && \
   sleep 2 && \
   gh pr edit <PR_NUMBER> --repo <owner/repo> --add-label "TEST"
   ```
4. **Monitor** - Watch for the new pipeline to complete

## Cross-model checklist

- Claude: Use JSON output for parsing; concise instructions
- Gemini: Explicit commands; minimal formatting
- All models: Always include --repo flag; parse JSON responses

## Notes

- Requires `gh` CLI v2.0+ or `GITHUB_TOKEN` environment variable
- Requires CircleCI CLI/token for pipeline status
- Projects v2 uses GraphQL API (requires appropriate permissions)
- Rate limits apply per GitHub API policies
- `--repo` flag is always required (no auto-detection)
- TEST label triggers CI workflow via GitHub Actions/CircleCI integration

## See Also

- `/pr` skill for PR creation, polling, and review comment workflows
- `/jira` skill for Jira integration (similar command structure)
- `/tasks` skill for Lisa's internal task management
