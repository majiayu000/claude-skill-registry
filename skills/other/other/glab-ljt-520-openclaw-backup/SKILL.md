---
name: glab
description: GitLab CLI for managing issues, merge requests, CI/CD pipelines, and repositories. Use when: (1) Creating, reviewing, or merging MRs, (2) Managing GitLab issues, (3) Monitoring or triggering CI/CD pipelines, (4) Working with self-hosted GitLab instances, (5) Automating GitLab workflows from the command line. Requires GITLAB_TOKEN (recommend minimal scopes). The `glab api` command enables arbitrary API calls - use read-only tokens when possible.
homepage: https://github.com/bezko/openclaw-skills/tree/main/skills/glab
metadata:
  openclaw:
    requires:
      bins: [glab, jq]
      envs:
        - name: GITLAB_TOKEN
          description: GitLab personal access token. Recommend minimal scopes (read_api for read-only).
          secret: true
          required: true
        - name: GITLAB_HOST
          description: GitLab instance hostname (e.g., gitlab.example.org). Defaults to gitlab.com.
          required: false
        - name: TIMEOUT
          description: Pipeline/MR wait timeout in seconds. Defaults vary by script.
          required: false
        - name: INTERVAL
          description: Polling interval in seconds for watch scripts. Default 5-10s.
          required: false
    install:
      - id: brew
        kind: brew
        package: glab
        label: Install glab via Homebrew
      - id: apt
        kind: apt
        package: glab
        label: Install glab via apt
      - id: jq-brew
        kind: brew
        package: jq
        label: Install jq via Homebrew
      - id: jq-apt
        kind: apt
        package: jq
        label: Install jq via apt
---

# GitLab CLI (glab)

Official CLI for GitLab. Manage issues, merge requests, pipelines, and more from the terminal.

> **Source:** Inspired by [NikiforovAll/glab-skill](https://github.com/NikiforovAll/claude-code-rules/tree/main/plugins/handbook-glab/skills/glab-skill) on Smithery.

## ⚠️ Security Notice

**The `glab api` command provides unrestricted GitLab API access with your token.**

- A compromised or overly-permissive token can delete projects, modify settings, expose secrets
- **Recommendation:** Use tokens with minimal scopes:
  - `read_api` - Read-only operations
  - `api` - Full access (only when write operations needed)
- For automation, consider project-level tokens with limited scope
- Never use tokens with `sudo` scope unless required

## Prerequisites

**Required binaries:**
- `glab` - GitLab CLI
- `jq` - JSON processor (for scripts and API parsing)

**Required credentials:**
- `GITLAB_TOKEN` - GitLab personal access token

**Optional configuration:**
- `GITLAB_HOST` - Self-hosted GitLab instance (default: gitlab.com)

```bash
# Verify installation
glab --version
jq --version

# Authenticate (interactive)
glab auth login

# Or via environment
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
export GITLAB_HOST="gitlab.example.org"  # for self-hosted

# Verify auth
glab auth status
```

## Quick Reference

**Merge Requests:**
```bash
glab mr create --title "Fix" --description "Closes #123"
glab mr list --reviewer=@me          # MRs awaiting your review
glab mr checkout 123                  # Test MR locally
glab mr approve 123 && glab mr merge 123
```

**Issues:**
```bash
glab issue create --title "Bug" --label=bug
glab issue list --assignee=@me
glab issue close 456
```

**CI/CD:**
```bash
glab ci status                        # Current pipeline status
glab pipeline ci view                 # Watch pipeline live
glab ci lint                          # Validate .gitlab-ci.yml
glab ci retry                         # Retry failed pipeline
```

**Working Outside Repo:**
```bash
glab mr list -R owner/repo            # Specify repository
```

**Advanced API Access:**

See **references/api-advanced.md** for `glab api` usage. This command enables arbitrary GitLab API calls and should be used with appropriately-scoped tokens.

## Core Workflows

### Create and Merge MR

```bash
# 1. Push branch
git push -u origin feature-branch

# 2. Create MR
glab mr create --title "Add feature" --description "Implements X" --reviewer=alice,bob --label="enhancement"

# 3. After approval, merge
glab mr approve 123
glab mr merge 123 --remove-source-branch
```

### Review MR

```bash
# List MRs for review
glab mr list --reviewer=@me

# Checkout and test
glab mr checkout 123

# Approve or comment
glab mr approve 123
glab mr note 123 -m "Looks good, just one suggestion..."
```

### Monitor Pipeline

```bash
# Watch current branch pipeline
glab pipeline ci view

# Check specific pipeline
glab ci view 456

# View failed job logs
glab ci trace

# Retry
glab ci retry
```

## Self-Hosted GitLab

```bash
# Set default host
export GITLAB_HOST=gitlab.example.org

# Or per-command
glab mr list -R gitlab.example.org/owner/repo
```

## Scripts

| Script | Description |
|--------|-------------|
| `glab-mr-await.sh` | Wait for MR approval and successful pipeline |
| `glab-pipeline-watch.sh` | Monitor pipeline with exit codes for CI |

```bash
# Wait for MR to be approved and merged
./scripts/glab-mr-await.sh 123 --timeout 600

# Watch pipeline, exit 0 on success, 1 on failure
./scripts/glab-pipeline-watch.sh --timeout 300
```

**Script environment variables:**
- `TIMEOUT` - Max wait time in seconds (default varies by script)
- `INTERVAL` - Polling interval in seconds (default 5-10s)

## Troubleshooting

| Error | Fix |
|-------|-----|
| `command not found: glab` | Install glab |
| `command not found: jq` | Install jq |
| `401 Unauthorized` | Set `GITLAB_TOKEN` or run `glab auth login` |
| `404 Project Not Found` | Verify repo name and permissions |
| `not a git repository` | Use `-R owner/repo` flag |
| `source branch already has MR` | `glab mr list` to find existing |

For detailed troubleshooting, see **references/troubleshooting.md**.

## Progressive Disclosure

- **references/api-advanced.md** - `glab api` usage with security considerations
- **references/commands-detailed.md** - Full command reference with all flags
- **references/troubleshooting.md** - Detailed error scenarios and solutions

Load these when you need specific flag details or are debugging issues.

## Best Practices

1. Always verify auth: `glab auth status`
2. Use minimal-scope tokens for read operations
3. Link MRs to issues: "Closes #123" in description
4. Lint CI config before pushing: `glab ci lint`
5. Use `--output=json` for scripting
6. Most commands have `--web` to open in browser
