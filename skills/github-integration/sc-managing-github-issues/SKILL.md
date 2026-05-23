---
name: sc-managing-github-issues
version: 0.8.0
description: GitHub issue lifecycle management with worktree isolation
entry_point: /sc-github-issue
---

# Managing GitHub Issues Skill

Manage GitHub issues from listing to fixing to PR creation with clean worktree isolation.

## Commands

- `/sc-github-issue` - Main entry point for all issue operations

## Agents

- `sc-github-issue-intake` - List and fetch issue details
- `sc-github-issue-mutate` - Create and update issues
- `sc-github-issue-fix` - Implement fixes in isolated worktrees
- `sc-github-issue-pr` - Create pull requests

## Operations

- `--list [--repo owner/repo]` - List open issues
- `--create` - Create issue interactively
- `--update <id>` - Update issue fields
- `--fix --issue <id/url> [--yolo]` - Full fix workflow: fetch → confirm → worktree → implement → test → commit → push → PR

## Dependencies

- **Packages**: sc-git-worktree >= 0.6.0 (worktree operations)
- **CLI**: GitHub CLI (`gh`) version 2.0 or higher
- **Config**: Package manifest options (base-branch, branch-pattern, auto-pr)

## Configuration

Configuration via manifest options (defaults shown):

```yaml
options:
  base-branch:
    type: string
    default: "main"
  branch-pattern:
    type: string
    default: "fix-issue-{number}"
  auto-pr:
    type: boolean
    default: true
```

Users can override in `.claude/config.yaml`:

```yaml
packages:
  sc-github-issue:
    base-branch: develop
    branch-pattern: "hotfix/{number}"
    auto-pr: false

github:
  test_command: "npm test"
  pr_template: |
    ## Summary
    Fixes #{issue_number}
```

## Data Contracts

All agents return fenced JSON with v0.4 minimal envelope:

```json
{
  "success": true|false,
  "data": { /* operation results */ },
  "error": null|{
    "code": "ERROR.CODE",
    "message": "Human readable message",
    "recoverable": true|false,
    "suggested_action": "What to do next"
  }
}
```

## Safety

- Pre-flight `gh` CLI auth checks
- Approval gates before destructive ops (unless `--yolo`)
- Test failure prompts
- Actionable error messages with suggested actions
- Worktree isolation prevents contaminating main working directory

## Integration with sc-git-worktree

The `--fix` workflow creates isolated worktrees via the sc-git-worktree skill:

1. **Create**: `sc-worktree-create` agent creates `fix-issue-{number}` worktree
2. **Implement**: Fix implemented in isolated directory
3. **Commit & Push**: Changes committed and pushed from worktree
4. **Cleanup**: Manual cleanup via `/sc-git-worktree --cleanup` after PR merge

This ensures the main working directory remains clean during fix implementation.

## References

- `references/github-issue-apis.md` - GitHub CLI patterns
- `references/github-issue-checklists.md` - Workflow checklists
