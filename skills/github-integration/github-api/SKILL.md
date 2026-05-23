---
name: github-api
description: Access GitHub API using gh CLI in sandboxed environment - install binary, authenticate with tokens, query repos, PRs, issues, workflow runs, and download artifacts
version: 2025-11-06
related_skills:
  - starwards-ci-debugging (specific CI workflow debugging)
  - using-superpowers (announce skill usage)
---

# GitHub API Access

Access GitHub's API in sandboxed environment using GitHub CLI binary.

**Core principle:** Use existing gh if available (global or /tmp), install only if needed.

**Environment:** Requires `GITHUB_TOKEN` environment variable.

## When to Use

PR status/reviews, workflow runs/logs, issues, repository info, Actions data, artifacts, remote file contents.

## Quick Setup

Check for gh and set alias:

```bash
if command -v gh &> /dev/null; then
  GH="gh"
elif [ -f "/tmp/gh-install/gh_2.62.0_linux_amd64/bin/gh" ]; then
  GH="/tmp/gh-install/gh_2.62.0_linux_amd64/bin/gh"
else
  echo "gh not found. See INSTALL.md for installation instructions"
  exit 1
fi
$GH --version
$GH auth status
```

**If gh not found:** See [INSTALL.md](./INSTALL.md) for installation instructions.

## Essential Commands

After setup, use `$GH` alias:

```bash
$GH pr list --repo OWNER/REPO
$GH pr view <NUM> --repo OWNER/REPO
$GH pr checks <NUM> --repo OWNER/REPO
$GH issue list --repo OWNER/REPO
$GH run list --repo OWNER/REPO --status failure
$GH run view <RUN_ID> --repo OWNER/REPO
$GH api repos/OWNER/REPO/actions/runs/<RUN_ID>/jobs --jq '.jobs[] | select(.conclusion=="failure")'
$GH api repos/OWNER/REPO/actions/runs/<RUN_ID>/logs --paginate > /tmp/logs.zip
$GH repo view OWNER/REPO --json name,description,url
$GH api repos/OWNER/REPO/contents/path/to/file --jq -r '.content' | base64 -d
$GH api rate_limit
```

## Critical Constraints

**Works:** Binary install to /tmp, GITHUB_TOKEN auth, full path commands, file downloads, jq parsing, all REST endpoints

**Doesn't work:** `gh` without full path, `export` env vars, interactive commands, git credential helper

**Rate limits:** Authenticated 5000/hr, unauthenticated 60/hr

**Token must pre-exist** as `GITHUB_TOKEN` - cannot be set in session.

## Reference Documentation

Detailed guides in skill directory:
- [reference/pull-requests.md](./reference/pull-requests.md) - PR operations
- [reference/issues.md](./reference/issues.md) - Issue operations
- [reference/workflow-runs.md](./reference/workflow-runs.md) - CI/CD operations
- [reference/repository-info.md](./reference/repository-info.md) - Repository data
- [reference/raw-api-access.md](./reference/raw-api-access.md) - Direct REST API
- [reference/pagination.md](./reference/pagination.md) - Pagination strategies
- [reference/searching.md](./reference/searching.md) - Search syntax
- [reference/jq-patterns.md](./reference/jq-patterns.md) - JSON parsing patterns
- [EXAMPLES.md](./EXAMPLES.md) - Real-world workflows
- [ENDPOINTS.md](./ENDPOINTS.md) - Complete API endpoint reference

## Token Permissions

**Read-only:** Contents, Pull requests, Actions, Issues (Read)
**Write ops:** Add Write permissions for respective resources

## Troubleshooting

- **"command not found"** → Use full path `/tmp/gh-install/gh_2.62.0_linux_amd64/bin/gh`
- **"authentication failed"** → `printenv GITHUB_TOKEN | head -c 30`
- **"rate limit exceeded"** → `$GH api rate_limit`
- **"404 Not Found"** → Verify `OWNER/REPO` format
- **"Empty response"** → Add `--paginate`

## Best Practices

1. Always check for existing gh before installing (system-wide, then /tmp)
2. Binary persists in /tmp for entire session if installed there
3. Use `GH` alias variable in scripts
4. Parse with `--json` and `--jq` for programmatic access
5. Download files to /tmp to avoid permissions issues
6. Test with small queries before bulk operations

## Related Skills

starwards-ci-debugging, starwards-verification, starwards-workflow, using-superpowers

**Docs:** https://docs.github.com/en/rest | https://cli.github.com/manual/
