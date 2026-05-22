---
name: jira-communication
description: >
  Jira API operations via Python CLI scripts. AUTOMATICALLY TRIGGER when user
  mentions Jira URLs (https://jira.*/browse/*, https://*.atlassian.net/browse/*),
  issue keys (PROJ-123), or asks about Jira issues. Use when Claude needs to:
  (1) Search issues with JQL queries, (2) Get or update issue details,
  (3) Create new issues, (4) Transition issue status (e.g., "To Do" → "Done"),
  (5) Add comments, (6) Log work time (worklogs), (7) List sprints and sprint issues,
  (8) List boards and board issues, (9) Create or list issue links,
  (10) Discover available Jira fields, (11) Get user profile information,
  (12) Download attachments from issues.
  If authentication fails, offer interactive credential setup via jira-setup.py.
  Supports both Jira Cloud and Server/Data Center with automatic auth detection.
---

# Jira Communication

CLI scripts for Jira operations using `uv run`. All scripts support `--help`, `--json`, `--quiet`, `--debug`.

## Auto-Trigger

Trigger when user mentions:
- **Jira URLs**: `https://jira.*/browse/*`, `https://*.atlassian.net/browse/*`
- **Issue keys**: `PROJ-123`, `NRS-4167`

When triggered by URL → extract issue key → run `jira-issue.py get PROJ-123`

## Auth Failure Handling

When auth fails, offer: `uv run scripts/core/jira-setup.py` (interactive credential setup)

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/core/jira-setup.py` | Interactive credential config |
| `scripts/core/jira-validate.py` | Verify connection |
| `scripts/core/jira-issue.py` | Get/update issue details |
| `scripts/core/jira-search.py` | Search with JQL |
| `scripts/core/jira-worklog.py` | Time tracking |
| `scripts/core/jira-attachment.py` | Download attachments |
| `scripts/workflow/jira-create.py` | Create issues |
| `scripts/workflow/jira-transition.py` | Change status |
| `scripts/workflow/jira-comment.py` | Add comments |
| `scripts/workflow/jira-sprint.py` | List sprints |
| `scripts/workflow/jira-board.py` | List boards |
| `scripts/utility/jira-user.py` | User info |
| `scripts/utility/jira-fields.py` | Search fields |
| `scripts/utility/jira-link.py` | Issue links |

## Critical: Flag Ordering

Global flags **MUST** come **before** subcommand:
```bash
# Correct:  uv run scripts/core/jira-issue.py --json get PROJ-123
# Wrong:    uv run scripts/core/jira-issue.py get PROJ-123 --json
```

## Quick Examples

```bash
uv run scripts/core/jira-validate.py --verbose
uv run scripts/core/jira-search.py query "assignee = currentUser()"
uv run scripts/core/jira-issue.py get PROJ-123
uv run scripts/core/jira-worklog.py add PROJ-123 2h --comment "Work done"
uv run scripts/workflow/jira-transition.py do PROJ-123 "In Progress" --dry-run
```

## Related Skills

**jira-syntax**: For descriptions/comments. Jira uses wiki markup, NOT Markdown.

## References

- `references/jql-quick-reference.md` - JQL syntax
- `references/troubleshooting.md` - Setup and auth issues

## Authentication

**Cloud**: `JIRA_URL` + `JIRA_USERNAME` + `JIRA_API_TOKEN`
**Server/DC**: `JIRA_URL` + `JIRA_PERSONAL_TOKEN`

Config via `~/.env.jira` or env vars. Run `jira-validate.py --verbose` to verify.
