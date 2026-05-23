---
name: sc-commit-push-pr
version: 0.1.0
description: Commit staged changes, push to remote, and create PRs for GitHub and Azure DevOps
---

# sc-commit-push-pr Skill

Orchestrates the commit, push, and PR creation workflow using background agents.

## Capabilities

| Command | Description |
|---------|-------------|
| `/sc-commit-push-pr` | Full pipeline: commit, push, and create PR if needed |
| `/sc-create-pr` | Create PR from title/body (standalone) |

## Agent Delegation

| Step | Agent | Input | Output |
|------|-------|-------|--------|
| Commit & Push | `commit-push` | source/destination branches | PR status, URL, or conflict list |
| Create PR | `create-pr` | title, body, source, destination | PR info |

## Orchestration Logic

### `/sc-commit-push-pr` Flow

1. **Stage important files**
   - Prompt user if unclear which files to stage
   - Skip if no changes detected

2. **Invoke `commit-push` agent via Agent Runner**
   - Pass source/destination branch parameters
   - Parse fenced JSON response

3. **Handle response:**
   - If `pr_exists: true` → Return PR URL to user
   - If `needs_pr_text: true` → Prompt user for title/body, then invoke `create-pr`
   - If `error.code == "GIT.MERGE_CONFLICT"` → Guide user through conflict resolution

### `/sc-create-pr` Flow

1. **Accept title/body from user**
   - May be provided as arguments or prompted

2. **Invoke `create-pr` agent via Agent Runner**
   - Pass title, body, source, destination

3. **Return PR URL to user**

## Provider Support

- **GitHub** - Uses `gh` CLI for PR operations
- **Azure DevOps** - Uses REST API with `AZURE_DEVOPS_PAT`

Provider is auto-detected from git remote on each run.

## Configuration

### Required: Protected Branches

Create `.sc/shared-settings.yaml`:

```yaml
git:
  protected_branches:
    - main
    - develop
```

Or let the skill auto-detect from git-flow configuration.

### Credentials

Set environment variables:
- GitHub: `GITHUB_TOKEN` (or `gh auth login`)
- Azure DevOps: `AZURE_DEVOPS_PAT`

## Error Handling

| Error Code | Meaning | Recovery |
|------------|---------|----------|
| `GIT.MERGE_CONFLICT` | Merge conflicts detected | Resolve conflicts, re-run |
| `GIT.AUTH` | Authentication failure | Check credentials |
| `PR.CREATE_FAILED` | API error creating PR | Check permissions |
| `CONFIG.PROTECTED_BRANCH_NOT_SET` | Missing config | Create shared-settings.yaml |

## Storage

| Type | Path | Purpose |
|------|------|---------|
| Logs | `.claude/state/logs/sc-commit-push-pr/` | Runtime events, preflight results |
| Shared Settings | `.sc/shared-settings.yaml` | Protected branch configuration |
| Package Settings | `.sc/sc-commit-push-pr/settings.yaml` | Optional preferences |

## Related

- [Design Document](../../../../docs/design/commit-push-pr-design.md)
- [commit-push Agent](../../agents/commit-push.md)
- [create-pr Agent](../../agents/create-pr.md)
