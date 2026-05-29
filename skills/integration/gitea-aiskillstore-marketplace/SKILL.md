---
name: gitea
description: "Gitea operations via tea CLI. Use when user mentions: gitea, tea, or when git remote shows a Gitea instance."
---

# Gitea CLI (tea)

## When to Use This Skill

Use `tea` for Gitea repositories. To detect Gitea, check if the remote is not GitHub or GitLab:
```bash
git remote -v
```

If the remote doesn't contain `github.com` or `gitlab`, it may be a Gitea instance.

## Before Any Operation

Always verify authentication first:
```bash
tea login list
```

If not authenticated, guide the user to run `tea login add`.

## Behavioral Guidelines

1. **Creating PRs**: Always check for uncommitted changes first with `git status`
2. **CI Operations**: Check pipeline status before triggering new runs
3. **Use `--output`**: For machine-readable output, use `-o json` or `-o yaml`

## Command Reference

### Pull Requests
| Action | Command |
|--------|---------|
| Create | `tea pr create --title "Title" --description "Desc"` |
| List | `tea pr list` |
| View | `tea pr view <id>` |
| Checkout | `tea pr checkout <id>` |
| Merge | `tea pr merge <id>` |

### Issues
| Action | Command |
|--------|---------|
| Create | `tea issue create --title "Title" --body "Desc"` |
| List | `tea issue list` |
| List open | `tea issue list --state open` |
| View | `tea issue view <id>` |
| Close | `tea issue close <id>` |
| Comment | `tea issue comment <id> "Comment"` |

### Repository
| Action | Command |
|--------|---------|
| Clone | `tea repo clone <owner/repo>` |
| Fork | `tea repo fork <owner/repo>` |

### Output Formats
For JSON output (useful for scripting):
```bash
tea issue list -o json
tea pr list -o json
```
