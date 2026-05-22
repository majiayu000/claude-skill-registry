---
name: gitlab
description: "GitLab operations via glab CLI. Use when user mentions: MR, merge request, gitlab issue, pipeline, CI status, glab, or when git remote shows gitlab.com or self-hosted GitLab."
---

# GitLab CLI (glab)

## When to Use This Skill

Use `glab` for GitLab repositories. To detect GitLab:
```bash
git remote -v | grep -i gitlab
```

If the remote contains `gitlab.com` or a known GitLab instance, use this skill.

## Before Any Operation

Always verify authentication first:
```bash
glab auth status
```

If not authenticated, guide the user to run `glab auth login`.

## Behavioral Guidelines

1. **Creating MRs**: Always check for uncommitted changes first with `git status`
2. **Viewing MRs/Issues**: Prefer `--comments` flag when user wants full context
3. **CI Operations**: Check `glab ci status` before suggesting `glab ci run`
4. **Use `--web`**: When the user might benefit from the browser UI

## Command Reference

### Merge Requests
| Action | Command |
|--------|---------|
| Create | `glab mr create --title "Title" --description "Desc"` |
| Create draft | `glab mr create --draft --title "Title"` |
| List | `glab mr list` |
| View | `glab mr view <id>` |
| View with comments | `glab mr view <id> --comments` |
| Checkout | `glab mr checkout <id>` |
| Merge | `glab mr merge <id>` |
| Approve | `glab mr approve <id>` |

### Issues
| Action | Command |
|--------|---------|
| Create | `glab issue create --title "Title" --description "Desc"` |
| List | `glab issue list` |
| List mine | `glab issue list --assignee=@me` |
| View | `glab issue view <id>` |
| Close | `glab issue close <id>` |
| Comment | `glab issue note <id> --message "Comment"` |

### CI/CD Pipelines
| Action | Command |
|--------|---------|
| Status | `glab ci status` |
| List | `glab ci list` |
| View logs | `glab ci trace` |
| Run new | `glab ci run` |
| Retry failed | `glab ci retry` |

### Repository
| Action | Command |
|--------|---------|
| View info | `glab repo view` |
| Clone | `glab repo clone <repo>` |
| Open in browser | `glab repo view --web`|
