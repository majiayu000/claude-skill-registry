---
name: github
description: "GitHub operations via gh CLI. Use when user mentions: PR, pull request, github issue, workflow, actions, gh, or when git remote shows github.com."
---

# GitHub CLI (gh)

## When to Use This Skill

Use `gh` for GitHub repositories. To detect GitHub:
```bash
git remote -v | grep -i github.com
```

If the remote contains `github.com`, use this skill.

## Before Any Operation

Always verify authentication first:
```bash
gh auth status
```

If not authenticated, guide the user to run `gh auth login`.

## Behavioral Guidelines

1. **Creating PRs**: Always check for uncommitted changes first with `git status`
2. **Viewing PRs/Issues**: Use `--comments` flag when user wants full context
3. **CI Operations**: Check `gh run list` before triggering new workflows
4. **Use `--web`**: When the user might benefit from the browser UI
5. **PR descriptions**: Use HEREDOC for multi-line bodies to preserve formatting

## Command Reference

### Pull Requests
| Action | Command |
|--------|---------|
| Create | `gh pr create --title "Title" --body "Desc"` |
| Create draft | `gh pr create --draft --title "Title"` |
| List | `gh pr list` |
| View | `gh pr view <id>` |
| View with comments | `gh pr view <id> --comments` |
| Checkout | `gh pr checkout <id>` |
| Diff | `gh pr diff <id>` |
| Merge | `gh pr merge <id>` |
| Approve | `gh pr review <id> --approve` |

### Issues
| Action | Command |
|--------|---------|
| Create | `gh issue create --title "Title" --body "Desc"` |
| List | `gh issue list` |
| List mine | `gh issue list --assignee=@me` |
| View | `gh issue view <id>` |
| Close | `gh issue close <id>` |
| Comment | `gh issue comment <id> --body "Comment"` |

### Workflow Runs (CI/CD)
| Action | Command |
|--------|---------|
| List runs | `gh run list` |
| View run | `gh run view <id>` |
| View logs | `gh run view <id> --log` |
| Watch live | `gh run watch <id>` |
| Rerun failed | `gh run rerun <id> --failed` |

### Repository
| Action | Command |
|--------|---------|
| View info | `gh repo view` |
| Clone | `gh repo clone <owner/repo>` |
| Fork | `gh repo fork` |
| Open in browser | `gh repo view --web` |

### Advanced: API Calls
For operations not covered by CLI commands:
```bash
gh api repos/{owner}/{repo}/pulls/{id}/comments
```
