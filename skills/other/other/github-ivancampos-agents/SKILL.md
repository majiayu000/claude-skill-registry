---
name: github
description: Use the GitHub CLI (`gh`) to inspect and manage repositories, pull requests, issues, workflows, releases, and API calls from the terminal. Use when a user asks to use `gh`/GitHub CLI, run GitHub repo or PR workflows, automate GitHub Actions from shell, or troubleshoot `gh` authentication and configuration.
---

# GitHub CLI

## Overview
Use `gh` for day-to-day GitHub operations from the terminal. Prefer read-only commands first, then run mutating commands only after clear user intent.

## Quick Start
1. Check installation and auth:
```bash
gh --version
gh auth status
```
2. Establish repository context:
```bash
scripts/gh_preflight.sh --repo owner/repo
```
3. If not in the target repository, pass `-R owner/repo` to commands.
4. Use `--json` with `--jq` or `--template` for automation-friendly output.

## Workflow
1. Establish context first.
- Determine GitHub host (`github.com` by default), repository, and branch.
- Run `scripts/gh_preflight.sh` before multi-step operations.
2. Read current state.
- Use `list`, `view`, and `status` subcommands before changing anything.
3. Apply requested mutation.
- For create/edit/merge/delete actions, restate the operation and require explicit confirmation unless the user already asked clearly.
4. Report stable identifiers.
- Return URLs and IDs for created or changed objects (PR number, issue number, run URL, release tag).

## Common Commands
- Repository:
  - `gh repo view`
  - `gh repo clone owner/repo`
  - `gh repo create`
  - `gh repo set-default owner/repo`
- Pull requests:
  - `gh pr list`
  - `gh pr view <number>`
  - `gh pr checkout <number>`
  - `gh pr create`
  - `gh pr review <number> --approve|--request-changes|--comment`
  - `gh pr merge <number>`
- Issues:
  - `gh issue list`
  - `gh issue view <number>`
  - `gh issue create`
  - `gh issue comment <number> --body "..."`
  - `gh issue close <number>`
- Actions:
  - `gh workflow list`
  - `gh workflow run <workflow>`
  - `gh run list`
  - `gh run watch <run-id>`
  - `gh run view <run-id> --log`
- Releases:
  - `gh release list`
  - `gh release view <tag>`
  - `gh release create <tag> [assets...]`
  - `gh release upload <tag> <file>`
- API:
  - `gh api repos/{owner}/{repo}/pulls --paginate`

For broader command coverage, read `references/command-map.md`.

## Safety Defaults
- Confirm before commands that change remote state:
  - `gh pr create|merge|close|reopen|ready`
  - `gh issue create|edit|close|reopen|delete`
  - `gh repo create|edit|archive|delete`
  - `gh release create|edit|delete`
  - `gh secret set|delete`
  - `gh variable set|delete`
  - `gh workflow run`
- Avoid destructive flags (`--delete-branch`, force flags) unless explicitly requested.
- Show exact command before bulk updates and prefer smallest safe scope.

## Structured Output
Use JSON output when parsing or summarizing results:

```bash
gh pr list --json number,title,url --jq '.[] | "\(.number)\t\(.title)\t\(.url)"'
gh issue list --json number,title,labels --template '{{range .}}{{printf "#%v %v\n" .number .title}}{{end}}'
```

## Troubleshooting
- Auth errors: `gh auth login` or `gh auth refresh`.
- Wrong account/host: `gh auth status --hostname github.com`, then `gh auth switch`.
- Unknown command options: `gh <command> <subcommand> --help`.
- Manual reference: `https://cli.github.com/manual/`.

## Resources
### scripts/
- `scripts/gh_preflight.sh`: Check `gh` availability, auth status, and repository context.

### references/
- `references/command-map.md`: Command map for repo, PR, issue, actions, release, and API operations.
