---
name: claude-code-action
description: Knowledge base for creating and configuring Claude Code Action GitHub workflows
---

# Claude Code Action Workflow Guide

Reference guide for creating `anthropics/claude-code-action@v1` GitHub workflows.

## Authentication

Choose one authentication method:

| Method | Input | Use Case |
|--------|-------|----------|
| OAuth Token | `claude_code_oauth_token` | Recommended for most setups (requires Claude Pro or Max) |
| API Key | `anthropic_api_key` | Direct Anthropic API key from console.anthropic.com |
| AWS Bedrock | `aws_access_key_id` + `aws_secret_access_key` | AWS-hosted Claude |
| GCP Vertex | `gcp_project_id` + `gcp_region` + `gcp_workload_identity_provider` | Google Cloud Claude |

### Getting `CLAUDE_CODE_OAUTH_TOKEN`

Requires a **Claude Pro or Max subscription**.

1. Run locally:
   ```bash
   claude setup-token
   ```
2. Copy the output token
3. Add it as a GitHub repository secret:
   ```bash
   gh secret set CLAUDE_CODE_OAUTH_TOKEN
   ```
   Paste the token when prompted.

On macOS, Claude Code stores credentials in the encrypted Keychain (not a plain file). The `setup-token` command is the official way to extract a token for CI use.

### Repository Configuration

| Name | Type | Required For | How to Set |
|------|------|-------------|------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Secret | All Claude workflows | `gh secret set CLAUDE_CODE_OAUTH_TOKEN` |
| `ENABLE_CLAUDE_NIGHTLY` | Variable | Nightly workflows (opt-in) | `gh variable set ENABLE_CLAUDE_NIGHTLY --body "true"` |

## Workflow Patterns

### Interactive (PR/Issue mentions)

Triggered when users mention `@claude` in comments, reviews, or issues.

```yaml
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]
  pull_request_review:
    types: [submitted]
```

### CI Auto-Fix (Automation)

Triggered when a CI workflow fails. Automatically fixes the code.

```yaml
on:
  workflow_run:
    workflows: ["CI Quality Checks"]
    types: [completed]
```

Guard against infinite loops:

```yaml
if: |
  github.event.workflow_run.conclusion == 'failure' &&
  !startsWith(github.event.workflow_run.head_branch, 'claude-auto-fix-') &&
  github.event.workflow_run.head_branch != 'main' &&
  github.event.workflow_run.head_branch != 'staging' &&
  github.event.workflow_run.head_branch != 'dev'
```

### Nightly/Scheduled

Runs on a cron schedule for maintenance tasks (test improvement, coverage).

```yaml
on:
  schedule:
    - cron: '0 3 * * 1-5'  # 3 AM UTC weekdays
  workflow_dispatch:
```

Use opt-in guard:

```yaml
if: vars.ENABLE_CLAUDE_NIGHTLY == 'true'
```

## Standard Permissions Block

```yaml
permissions:
  contents: write
  pull-requests: write
  issues: write
  actions: read
  id-token: write
```

## Tool Allowlisting

Standard allowedTools for Lisa projects:

```
Edit,MultiEdit,Write,Read,Glob,Grep,Bash(git:*),Bash(npm:*),Bash(npx:*),Bash(bun:*),Bash(yarn:*),Bash(pnpm:*),Bash(gh:*)
```

This covers:

- **File operations**: Edit, MultiEdit, Write, Read, Glob, Grep
- **Git**: `Bash(git:*)` -- commit, push, branch, etc.
- **Package managers**: npm, npx, bun, yarn, pnpm
- **GitHub CLI**: `Bash(gh:*)` -- create PRs, issues, etc.

## Key Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `prompt` | No | Task instructions for Claude |
| `claude_code_oauth_token` | Yes* | OAuth token for authentication |
| `claude_args` | No | CLI args: `--allowedTools`, `--max-turns`, `--system-prompt`, `--mcp-config` |
| `branch_prefix` | No | Prefix for auto-created branches (e.g., `claude/nightly-`) |
| `additional_permissions` | No | Extra GitHub permissions (e.g., `actions: read`) |
| `max_turns` | No | Max agentic turns (via claude_args `--max-turns`) |
| `track_progress` | No | Enable progress tracking comments |
| `allowed_bots` | No | Comma-separated bot names allowed to trigger |
| `allowed_non_write_users` | No | Users without write access who can trigger |

## MCP Configuration

Pass MCP server config via `claude_args`:

```yaml
claude_args: |
  --mcp-config .mcp.json
```

Pass secrets to MCP servers via environment variables in the workflow.

## Patterns

### Duplicate PR Prevention

Before running nightly workflows, check for existing open PRs:

```yaml
- name: Check for existing PR
  id: check-pr
  uses: actions/github-script@v7
  with:
    script: |
      const pulls = await github.rest.pulls.list({
        owner: context.repo.owner,
        repo: context.repo.repo,
        state: 'open',
        per_page: 100,
      });
      const existing = pulls.data.find(pr =>
        pr.head.ref.startsWith('claude/nightly-') &&
        pr.title.toLowerCase().includes('your-keyword')
      );
      core.setOutput('has_existing_pr', existing ? 'true' : 'false');

- name: Run Claude
  if: steps.check-pr.outputs.has_existing_pr != 'true'
  uses: anthropics/claude-code-action@v1
```

### Cost Control

Use `--max-turns` to limit API usage:

```yaml
claude_args: |
  --max-turns 25
```

Recommended limits:

- Interactive (PR/issue): No limit (user-driven)
- CI auto-fix: 25 turns
- Nightly workflows: 30 turns

### Security

- Never hardcode secrets in workflow files
- Use `${{ secrets.* }}` for all sensitive values
- Sanitize dynamic content in prompts to prevent injection
- Use `allowed_bots` to control which bots can trigger Claude
