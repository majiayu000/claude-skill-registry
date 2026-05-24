---
name: agent-ops-github
description: "Bidirectional sync between agent-ops issues and GitHub Issues"
category: extended
invokes: [agent-ops-state, agent-ops-tasks]
invoked_by: []
state_files:
  read: [issues/*.md, focus.md]
  write: [issues/*.md, focus.md]
---
# agent-ops-github

Bidirectional sync between agent-ops issues and GitHub Issues. Push local issues to GitHub, pull from GitHub to local, and manage the connection.

**Tier:** 3 (Utility)  
**Works with or without `aoc` CLI installed**

---

## Use Cases

1. **Push issues to GitHub** — Share local issues with team or track in GitHub
2. **Pull issues from GitHub** — Import GitHub issues as local agent-ops issues
3. **Sync bidirectionally** — Keep local and GitHub in sync
4. **Import PR feedback** — Get code review comments as local issues
5. **Monitor external repos** — Track issues from dependencies

---

## CRITICAL: No Assumptions

Before any GitHub API operation, you MUST:

1. **Confirm repository details** — Ask user for `owner/repo` format
2. **Verify authentication** — Check GITHUB_TOKEN is set
3. **Confirm the operation** — Summarize what will be done
4. **Get explicit approval** — User must approve before API calls

### Mandatory Confirmation

```
I will {push/pull/sync} issues {to/from} github.com/{owner}/{repo}:
- Operation: {describe what will happen}
- Issues affected: {count or list}

This will make API calls to GitHub. Continue? [Y/N]
```

---

## Requirements

### Environment
- `GITHUB_TOKEN` environment variable (required)
- Token needs `repo` scope (or `public_repo` for public repos)

### How to Create a Token
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic) with `repo` scope
3. Add to `.env`: `GITHUB_TOKEN=ghp_xxxxxxxxxxxx`

---

## Issue Sync Procedure (with aoc CLI)

### Check Sync Status
```bash
# See sync overview between local and GitHub
aoc github sync status --repo owner/repo
```

### Push Local Issues to GitHub

```bash
# Push a single issue
aoc github sync push FEAT-0042 --repo owner/repo

# Push all todo issues
aoc github sync push-all --repo owner/repo --status todo

# Push all issues (dry run first)
aoc github sync push-all --repo owner/repo --dry-run

# Use visible metadata block (instead of hidden comment)
aoc github sync push FEAT-0042 --repo owner/repo --visible
```

### Pull Issues from GitHub

```bash
# Pull a single GitHub issue (dry run by default)
aoc github sync pull 123 --repo owner/repo

# Actually import it
aoc github sync pull 123 --repo owner/repo --no-dry-run

# Pull all issues with agent-ops label
aoc github sync pull-all --repo owner/repo

# Pull all (actually import)
aoc github sync pull-all --repo owner/repo --no-dry-run
```

### How Metadata Sync Works

When pushing to GitHub:
- **Title** → GitHub issue title
- **Description** → GitHub issue body
- **Acceptance criteria** → Checklist in body
- **Type** → Label: `type:feat`, `type:bug`, etc.
- **Priority** → Label: `priority:high`, `priority:medium`, etc.
- **Epic** → Label: `epic:{name}`
- **Status** → GitHub state: `todo/in_progress` → open, `done` → closed
- **Metadata** → Hidden YAML comment in body (or visible `<details>` block)

When pulling from GitHub:
- GitHub state → Status
- Labels → Type, priority, epic
- Body metadata → Full issue details
- Body → Description (metadata stripped)

---

## Fetch Issues Procedure (read-only)

### List Issues
```bash
# All open issues
aoc github issues list --repo owner/repo --state open

# All issues including closed
aoc github issues list --repo owner/repo --state all

# Search issues
aoc github issues search "feature request" --repo owner/repo

# Issues by label
aoc github issues by-label bug --repo owner/repo
```

### Get Issue with Comments
```bash
# Get issue #42 with all comments
aoc github issues get 42 --repo owner/repo --comments --json
```

### Pull Request Comments
```bash
# List PRs
aoc github pr list --repo owner/repo --state open

# PRs for a specific branch
aoc github pr list --repo owner/repo --branch feature/my-branch

# All comments for a PR
aoc github pr comments 123 --repo owner/repo --json

# Reviews for a PR
aoc github pr reviews 123 --repo owner/repo --json

# Everything for a PR (comments + reviews)
aoc github pr by-branch feature/my-branch --repo owner/repo --comments
```

---

## Procedure (without aoc CLI)

### Python Script Approach

```python
import os
import requests

# Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
OWNER = "owner"
REPO = "repo"
BASE_URL = "https://api.github.com"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# List issues
def list_issues(state="open"):
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/issues"
    params = {"state": state, "per_page": 100}
    
    all_issues = []
    while url:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        issues = resp.json()
        # Filter out pull requests (they appear in issues endpoint)
        all_issues.extend([i for i in issues if "pull_request" not in i])
        # Check for next page
        url = resp.links.get("next", {}).get("url")
        params = None
    
    return all_issues

# Create issue with metadata
def create_issue(title, body, labels):
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/issues"
    data = {"title": title, "body": body, "labels": labels}
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    return resp.json()
```

---

## GitHub Issue Body Format

When pushed to GitHub, the issue body contains:

```markdown
{Description from local issue}

## Acceptance Criteria
- [ ] First criterion
- [ ] Second criterion

<!-- agent-ops-metadata
id: FEAT-0042@abc123
confidence: normal
epic: agent-ops-cli
acceptance_criteria:
- First criterion
- Second criterion
depends_on:
- FEAT-0040
-->
```

The metadata block is hidden in the rendered view but preserved for sync.

For visible metadata (useful for transparency), use `--visible`:

```markdown
{Description}

<details>
<summary>Agent-Ops Metadata</summary>

yaml
id: FEAT-0042@abc123
...

</details>
```

---

## Labels Convention

| Local Field | GitHub Label |
|-------------|--------------|
| type: FEAT | `type:feat` |
| type: BUG | `type:bug` |
| type: CHORE | `type:chore` |
| priority: critical | `priority:critical` |
| priority: high | `priority:high` |
| priority: medium | `priority:medium` |
| priority: low | `priority:low` |
| epic: agent-ops-cli | `epic:agent-ops-cli` |
| (always added) | `agent-ops` |

---

## Rate Limiting

GitHub API has rate limits:
- **Authenticated:** 5,000 requests/hour
- **Search API:** 30 requests/minute

If rate limited, wait and retry. The client handles this automatically with retries.

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/expired token | Regenerate GITHUB_TOKEN |
| 403 Forbidden | Rate limit or no access | Wait or check permissions |
| 404 Not Found | Wrong repo or issue | Verify owner/repo/number |

---

## Integration with Other Skills

### With agent-ops-branch-workflow
```
1. Create working branch for issue
2. Work on the issue
3. Push issue to GitHub: aoc github sync push FEAT-0042 --repo owner/repo
4. Create PR referencing the GitHub issue
```

### With agent-ops-selective-copy
```
1. Complete work on feature
2. Push all done issues: aoc github sync push-all --repo owner/repo --status done
3. Create clean branch for PR
4. GitHub issue automatically closed when merged
```

---

## Examples

### Example 1: Push New Feature to GitHub

```bash
# First, dry run to see what will happen
aoc github sync push FEAT-0042 --repo myorg/myrepo --dry-run

# Output: Would create GitHub issue #... from FEAT-0042

# Actually push
aoc github sync push FEAT-0042 --repo myorg/myrepo

# Output: Created FEAT-0042 → #156
```

### Example 2: Sync All Active Work

```bash
# Push all in-progress issues
aoc github sync push-all --repo myorg/myrepo --status in_progress

# Output:
# Created: 2
# Updated: 1
# Skipped: 5
```

### Example 3: Import Team Issues

```bash
# See what would be imported
aoc github sync pull-all --repo myorg/myrepo

# Output shows issues with agent-ops label/metadata
# Actually import them
aoc github sync pull-all --repo myorg/myrepo --no-dry-run
```
