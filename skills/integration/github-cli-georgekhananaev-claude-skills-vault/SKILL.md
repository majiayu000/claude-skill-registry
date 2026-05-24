---
name: github-cli
description: Safety-first GitHub CLI skill wrapping `gh` (v2.86+). Use when performing GitHub operations — PRs, issues, releases, repos, Actions, API calls. Enforces risk classification with mandatory confirmation for destructive/forbidden operations.
author: George Khananaev
---

# GitHub CLI

Safety-first wrapper for GitHub CLI (`gh`). Every command is classified by risk level before execution.

## When to Use

- User asks to create, list, merge, or close PRs
- User asks to manage issues, releases, or repos
- User asks to check CI/CD status or workflow runs
- User asks to call the GitHub API via `gh api`
- User asks to manage GitHub Actions secrets or variables

## Prerequisites

1. **Install:** `brew install gh` or see https://cli.github.com
2. **Auth:** `gh auth login`
3. **Verify:** `gh --version` (requires v2.86+)
4. **Scopes:** `gh auth status` — confirm `repo`, `read:org` scopes minimum

## Safety Model

Every `gh` command falls into one of four risk tiers:

| Tier | Action Required | Examples |
|------|----------------|----------|
| **Safe** | Execute immediately | `gh pr list`, `gh issue view`, `gh repo view` |
| **Write** | Inform user, then execute | `gh pr create`, `gh issue create`, `gh release create` |
| **Destructive** | `AskUserQuestion` BEFORE executing | `gh pr merge`, `gh pr close`, `gh release delete` |
| **Forbidden** | Multi-step validation, NEVER auto-confirm | `gh repo delete`, `gh repo transfer`, visibility changes |

See [references/safety-rules.md](references/safety-rules.md) for the full classification and confirmation templates.

## Decision Flow

```
Command received
  → Classify risk tier (see Quick Reference)
  → Safe?        Execute immediately
  → Write?       Inform user what will happen → execute
  → Destructive? AskUserQuestion with options → wait for answer → execute or cancel
  → Forbidden?   Warn → require typed confirmation → final confirm → execute or cancel
```

## Quick Reference

### Safe (read-only, execute immediately)

| Command | Description |
|---------|-------------|
| `gh pr list` | List pull requests |
| `gh pr view` | View PR details |
| `gh pr checks` | View CI status |
| `gh pr diff` | View PR diff |
| `gh issue list` | List issues |
| `gh issue view` | View issue details |
| `gh repo view` | View repo info |
| `gh repo list` | List repos |
| `gh repo clone` | Clone a repo |
| `gh release list` | List releases |
| `gh release view` | View release details |
| `gh run list` | List workflow runs |
| `gh run view` | View run details |
| `gh run view --log` | View run logs |
| `gh workflow list` | List workflows |
| `gh workflow view` | View workflow details |
| `gh run download` | Download workflow artifacts |
| `gh api` (GET) | Read-only API calls |
| `gh auth status` | Check auth |
| `gh browse` | Open repo in browser |
| `gh status` | Check your GitHub dashboard |
| `gh gist list` | List your gists |
| `gh gist view` | View gist details |
| `gh label list` | List labels |
| `gh search repos` | Search repos |
| `gh search issues` | Search issues |
| `gh search prs` | Search PRs |
| `gh search code` | Search code |

### Write (inform, then execute)

| Command | Description |
|---------|-------------|
| `gh pr create` | Create PR |
| `gh pr edit` | Edit PR metadata |
| `gh pr comment` | Comment on PR |
| `gh pr review` | Submit review |
| `gh pr ready` | Mark PR as ready |
| `gh pr checkout` | Check out a PR branch locally |
| `gh issue create` | Create issue |
| `gh issue edit` | Edit issue |
| `gh issue comment` | Comment on issue |
| `gh issue reopen` | Reopen a closed issue |
| `gh issue pin` | Pin an issue |
| `gh issue unpin` | Unpin an issue |
| `gh label create` | Create label |
| `gh label edit` | Edit label |
| `gh release create` | Create release |
| `gh repo create` | Create new repo |
| `gh repo edit` | Edit repo settings (non-visibility) |
| `gh repo fork` | Fork a repo |
| `gh repo rename` | Rename a repository |
| `gh gist create` | Create a new gist |
| `gh gist edit` | Edit an existing gist |
| `gh run rerun` | Re-run workflow |
| `gh workflow enable` | Enable workflow |
| `gh workflow disable` | Disable workflow |
| `gh workflow run` | Manually trigger a workflow |
| `gh secret set` | Set secret |
| `gh variable set` | Set variable |
| `gh api -X POST/PUT/PATCH` | Write API calls |

### Destructive (AskUserQuestion required)

| Command | Description |
|---------|-------------|
| `gh pr merge` | Merge PR (irreversible in most workflows) |
| `gh pr close` | Close PR |
| `gh issue close` | Close issue |
| `gh issue delete` | Delete issue (permanent) |
| `gh issue transfer` | Transfer issue to another repo |
| `gh release delete` | Delete release |
| `gh label delete` | Delete label |
| `gh repo archive` | Archive repo |
| `gh secret delete` | Delete secret |
| `gh variable delete` | Delete variable |
| `gh auth logout` | Log out of GitHub CLI |
| `gh run cancel` | Cancel running workflow |
| `gh api -X DELETE` | Delete API calls |

### Forbidden (multi-step validation)

| Command | Description |
|---------|-------------|
| `gh repo delete` | Delete repository (PERMANENT) |
| `gh repo transfer` | Transfer repo ownership |
| `gh repo edit --visibility` | Change repo visibility |
| Bulk destructive loops | Any loop running delete/close/merge |

## Workflow Patterns

### Pull Requests

```bash
# List open PRs
gh pr list

# Create PR (Write — inform user first)
gh pr create --title "feat: add auth" --body "$(cat <<'EOF'
## Summary
- Add JWT authentication middleware

## Test plan
- [ ] Unit tests pass
- [ ] Manual login flow verified
EOF
)"

# View PR with checks
gh pr view 42
gh pr checks 42

# Merge PR (Destructive — AskUserQuestion first)
gh pr merge 42 --squash --delete-branch
```

### Issues

```bash
# List issues with filters
gh issue list --label bug --assignee @me
gh issue list --state closed --limit 10

# Create issue (Write)
gh issue create --title "Bug: login fails" --body "Steps to reproduce..." --label bug

# View issue
gh issue view 123

# Close issue (Destructive — confirm first)
gh issue close 123 --reason completed
```

### Releases

```bash
# List releases
gh release list

# Create release (Write — inform user)
gh release create v1.2.0 --generate-notes --title "v1.2.0"

# Create release with assets
gh release create v1.2.0 ./dist/*.tar.gz --title "v1.2.0" --notes "Release notes here"

# Delete release (Destructive — confirm first)
gh release delete v1.2.0
```

### CI/CD & Actions

```bash
# List recent runs
gh run list --limit 10

# View specific run
gh run view 12345

# View logs for failed run
gh run view 12345 --log-failed

# Re-run failed jobs (Write)
gh run rerun 12345 --failed

# Cancel running workflow (Destructive — confirm)
gh run cancel 12345

# Manage secrets (Write for set, Destructive for delete)
gh secret set API_KEY --body "sk-..."
gh secret list
```

### Repository

```bash
# View repo info
gh repo view

# Create repo (Write)
gh repo create my-app --public --clone

# Clone
gh repo clone owner/repo

# Fork (Write)
gh repo fork owner/repo --clone

# Archive (Destructive — confirm first)
gh repo archive owner/repo
```

### API

```bash
# GET (Safe)
gh api repos/owner/repo/pulls
gh api repos/owner/repo/issues/123/comments

# POST (Write)
gh api repos/owner/repo/issues -f title="Bug" -f body="Description"

# DELETE (Destructive — confirm first)
gh api repos/owner/repo/issues/123/labels/bug -X DELETE
```

## AskUserQuestion Integration

For **Destructive** operations, use `AskUserQuestion` with tailored options:

### PR Merge Example

```
Question: "How should PR #42 'feat: add auth' be merged?"
Options:
  - "Squash and merge" — Combine all commits into one
  - "Create merge commit" — Preserve commit history
  - "Rebase and merge" — Rebase onto base branch
  - "Cancel" — Do not merge
```

### PR/Issue Close Example

```
Question: "Close PR #42 'feat: add auth'?"
Options:
  - "Close only" — Close without deleting branch
  - "Close and delete branch" — Close PR and remove source branch
  - "Cancel" — Keep open
```

### Delete Example

```
Question: "Delete release v1.2.0?"
Options:
  - "Delete release only" — Keep the git tag
  - "Delete release and tag" — Remove both release and git tag
  - "Cancel" — Keep release
```

For **Forbidden** operations, follow the triple-confirmation protocol in [references/safety-rules.md](references/safety-rules.md).

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `gh: command not found` | Not installed | `brew install gh` |
| `authentication required` | Not logged in | `gh auth login` |
| `HTTP 403` | Insufficient scopes | `gh auth refresh -s scope` |
| `HTTP 404` | Repo not found or no access | Check repo name and permissions |
| `HTTP 422` | Validation failed | Check required fields, branch exists |
| `HTTP 409` | Merge conflict | Resolve conflicts first |
| `HTTP 429` | Rate limited | Wait, or use `--limit` to reduce calls |
| `GraphQL: ...` | API query error | Check field names and types |

## CLI Flags Reference

| Flag | Description |
|------|-------------|
| `--json fields` | Output specific JSON fields |
| `--jq expr` | Filter JSON with jq expressions |
| `--template tmpl` | Format output with Go templates |
| `-R owner/repo` | Target a different repo |
| `--limit N` | Limit results |
| `--state open\|closed\|all` | Filter by state |
| `--label name` | Filter by label |
| `--assignee user` | Filter by assignee |
| `--author user` | Filter by author |
| `--web` | Open in browser |

## Shell Safety

- **No interactive mode:** Never use `-i` or `--interactive` flags
- **No pagers:** Always pipe to `cat` if output may trigger a pager: `gh pr list | cat`
- **Timeouts:** Set reasonable timeouts for commands that could hang
- **Quote arguments:** Always quote multi-word arguments and heredoc bodies
- **Never pass `--yes`** to forbidden operations — always require explicit confirmation

## Integration

Pairs with:
- **code-quality** — Review code before PR creation
- **brainstorm** — Design features before opening issues
- **codex-cli** — Second-opinion audit before merging PRs
- **gemini-cli** — Alternative AI review for PR changes
