---
name: github
description: |
  Manage GitHub via GitHub CLI (gh): repos, issues, pull requests, Actions, releases,
  secrets/variables, projects, gists, searches, and API access.
  Auto-activates on: "gh", "github cli", "github issue", "github pr", "pull request",
  "github actions", "workflow", "run", "github release", "release", "gh api",
  "github repo", "github secret", "github variable", "ci status", "monitor ci",
  "check ci", "watch ci", "pr dashboard", "pr overview", "open prs", "my prs", "pr status".
license: MIT
compatibility: Requires GitHub CLI (gh) and authentication (gh auth login or GH_TOKEN). Targets GitHub-hosted repos.
metadata:
  version: "1.0"
---

# GitHub

GitHub operations via `gh`.

## Router

| User says | Load reference | Do |
|---|---|---|
| help / gh help / flags / options | `references/cli-help.md` | show CLI help safely |
| auth / login / token | `references/auth.md` | authenticate gh |
| repo / clone / fork / sync | `references/repo.md` | repository operations |
| issue / issues | `references/issue.md` | issue triage and management |
| pr / pull request / review | `references/pr.md` | PR create/review/merge workflows |
| actions / workflow / run | `references/actions.md` | GitHub Actions (workflows + runs) |
| ci / monitor ci / check ci / ci status / watch ci | `references/ci-monitor.md` | monitor CI checks with live polling (if user says bare "ci", ask: monitor checks or view workflows?) |
| pr dashboard / pr overview / open prs / my prs / pr status | `references/pr-dashboard.md` | PR overview with status classification |
| release / publish release | `references/release.md` | releases + assets + verification |
| release strategy / release format / versioning | `references/release-strategy.md` | versioning, title/description format, generation protocol |
| secrets / variables | `references/secrets-vars.md` | manage secrets and variables |
| project | `references/projects.md` | projects operations |
| gist | `references/gists.md` | gist operations |
| search | `references/search.md` | search repos/issues/prs/code |
| api | `references/api.md` | gh api (advanced) |
| extension | `references/extensions.md` | manage gh extensions |
| config | `references/config.md` | gh config basics |

## Safety Rules

- Confirm before any state-changing operation (create/edit/delete/merge/close).
- Never upload secrets as assets.
- Treat `gh api` as powerful: confirm before any write operation.
- Never delete or move published releases/tags unless explicitly requested.
- When creating PRs, always set an assignee: default to `@me` unless the user explicitly names someone else.
- When creating PRs, apply relevant existing labels when possible; auto-pick from PR context (title/body/branch + changed paths) and avoid creating new labels unless truly necessary.
- If labels must be created, retrieve existing labels first (`gh label list`), propose the minimal set consistent with repo naming, and confirm before `gh label create`.

## Confirmation Policy

Read-only commands are always OK.

Require confirmation:

- `gh issue create/edit/close/reopen/delete`
- `gh pr create/edit/close/merge/review`
- `gh repo create/edit/rename/archive/delete/sync`
- `gh release create/edit/delete`, `gh release upload`, `gh release delete-asset`
- `gh secret set/delete`, `gh variable set/delete`
- `gh run rerun`, `gh run cancel`
- `gh api` calls that mutate state (POST/PATCH/PUT/DELETE)

## Read-Only (No Confirmation Needed)

```bash
gh auth status
gh release list
gh release view <tag>
gh release view <tag> --web
gh help
gh pr checks <number> --json ...
gh run list --branch <branch> --json ...
gh run view <run-id>
gh run view <run-id> --log-failed
```
