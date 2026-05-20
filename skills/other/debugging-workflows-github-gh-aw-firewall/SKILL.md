---
name: debugging-workflows
description: Debug GitHub Actions workflows by downloading logs, analyzing summaries, and understanding how agentic workflows and the AWF firewall work together.
allowed-tools: Bash(gh:*), Bash(curl:*), Bash(npx:*), Bash(node:*), Bash(cat:*), Bash(ls:*), Bash(grep:*), Bash(jq:*), Read
---

# Debugging Workflows Skill

Use this skill when you need to debug GitHub Actions workflows, download workflow logs or summaries, or understand how agentic workflows and the AWF firewall work together.

## Quick Start

### Download Workflow Logs

Use the `download-workflow-logs.ts` script to download logs from a workflow run:

```bash
# Download logs from the latest workflow run
npx tsx .github/skills/debugging-workflows/download-workflow-logs.ts

# Download logs from a specific run ID
npx tsx .github/skills/debugging-workflows/download-workflow-logs.ts --run-id 1234567890

# Download logs from a specific workflow
npx tsx .github/skills/debugging-workflows/download-workflow-logs.ts --workflow test-integration.yml

# Save logs to a specific directory
npx tsx .github/skills/debugging-workflows/download-workflow-logs.ts --output ./my-logs
```

### Download Workflow Summary

Use the `download-workflow-summary.ts` script to get a summary of workflow runs:

```bash
# Get summary of latest workflow runs
npx tsx .github/skills/debugging-workflows/download-workflow-summary.ts

# Get summary for a specific workflow run
npx tsx .github/skills/debugging-workflows/download-workflow-summary.ts --run-id 1234567890

# Get summary for a specific workflow file
npx tsx .github/skills/debugging-workflows/download-workflow-summary.ts --workflow test-integration.yml

# Get summary as JSON
npx tsx .github/skills/debugging-workflows/download-workflow-summary.ts --format json
```

## GitHub CLI Commands

The `gh` CLI is essential for debugging workflows. Here are the most useful commands:

### List Workflow Runs

```bash
# List recent workflow runs
gh run list --limit 10

# List runs for a specific workflow
gh run list --workflow test-integration.yml --limit 10

# List only failed runs
gh run list --status failure --limit 10

# List runs in JSON format for parsing
gh run list --json databaseId,name,status,conclusion,createdAt --limit 10
```

### View Workflow Run Details

```bash
# View a specific run
gh run view <run-id>

# View run with job details
gh run view <run-id> --verbose

# View run as JSON
gh run view <run-id> --json jobs,conclusion,status
```

### Download Run Logs

```bash
# Download all logs for a run
gh run download <run-id>

# Download specific artifact
gh run download <run-id> --name <artifact-name>

# Download to specific directory
gh run download <run-id> --dir ./logs
```

### Watch a Running Workflow

```bash
# Watch a workflow run in real-time
gh run watch <run-id>

# Watch with exit code (useful for CI)
gh run watch <run-id> --exit-status
```

### Re-run Failed Jobs

```bash
# Re-run failed jobs only
gh run rerun <run-id> --failed

# Re-run all jobs
gh run rerun <run-id>
```

## Understanding Agentic Workflows

### What are Agentic Workflows?

Agentic workflows are GitHub Actions workflows that use AI agents (like GitHub Copilot or Claude) to perform tasks. They are defined using **markdown + YAML frontmatter** format in `.github/workflows/*.md` files and compiled to GitHub Actions YAML (`.lock.yml` files).

### Key Components

1. **Workflow File Format**: `.github/workflows/<name>.md`
   - YAML frontmatter for configuration
   - Markdown body for AI instructions
   - Compiles to `.github/workflows/<name>.lock.yml`

2. **Triggers** (`on:` field):
   - Standard GitHub events: `issues`, `pull_request`, `push`, `schedule`
   - Command triggers: `/mention` in issues/comments
   - `workflow_dispatch` for manual triggers

3. **Safe Outputs**: Controlled way for AI to create GitHub entities
   - `create-issue:` - Create GitHub issues
   - `create-pull-request:` - Create PRs with git patches
   - `add-comment:` - Add comments to issues/PRs
   - `add-labels:` - Add labels to issues/PRs
   - `create-discussion:` - Create GitHub discussions

4. **Tools Configuration** (`tools:` field):
   - `github:` - GitHub API tools
   - `agentic-workflows:` - Workflow introspection tools
   - `edit:` - File editing tools
   - `web-fetch:` / `web-search:` - Web access tools
   - `bash:` - Shell command tools

### Compiling Workflows

```bash
# Compile all workflows
gh aw compile

# Compile a specific workflow
gh aw compile <workflow-name>

# Compile with strict security checks
gh aw compile --strict
```

### Debugging Agentic Workflows

```bash
# View status of all agentic workflows
gh aw status

# Download and analyze logs from previous runs
gh aw logs <workflow-name> --json

# Audit a specific run for issues
gh aw audit <run-id> --json
```

### Common Issues

1. **Missing Tool Calls**: Check `missing_tools` in audit output
2. **Safe Output Failures**: Review `safe_outputs.jsonl` artifact
3. **Permission Issues**: Verify `permissions:` block in frontmatter
4. **Network Blocked**: Check `network:` configuration for allowed domains

## Understanding the AWF Firewall

### What is AWF?

AWF (Agent Workflow Firewall) is a tool that provides L7 (HTTP/HTTPS) egress control for GitHub Copilot CLI and other agents. It restricts network access to a whitelist of approved domains using Squid proxy and Docker containers.

### Architecture Overview

```
┌─────────────────────────────────────────┐
│  Host (GitHub Actions Runner / Local)   │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │   Firewall CLI (awf)              │ │
│  │   - Parse arguments                │ │
│  │   - Generate Squid config          │ │
│  │   - Start Docker Compose           │ │
│  └────────────────────────────────────┘ │
│           │                              │
│           ▼                              │
│  ┌──────────────────────────────────┐   │
│  │   Docker Compose                 │   │
│  │  ┌────────────────────────────┐  │   │
│  │  │  Squid Proxy Container     │  │   │
│  │  │  - Domain ACL filtering    │  │   │
│  │  │  - HTTP/HTTPS proxy        │  │   │
│  │  └────────────────────────────┘  │   │
│  │           ▲                       │   │
│  │  ┌────────┼───────────────────┐  │   │
│  │  │ Agent Container            │  │   │
│  │  │ - Full filesystem access   │  │   │
│  │  │ - iptables redirect        │  │   │
│  │  │ - All traffic → Squid      │  │   │
│  │  └────────────────────────────┘  │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Key Containers

- **`awf-squid`** - Squid proxy container (IP: 172.30.0.10)
  - Filters HTTP/HTTPS traffic based on domain allowlist
  - Logs all traffic decisions

- **`awf-agent`** - Agent execution container (IP: 172.30.0.20)
  - Runs the actual command/agent
  - Has iptables rules to redirect traffic to Squid
  - Full filesystem access via `/host` mount

### Traffic Flow

1. Command runs in agent container
2. All HTTP/HTTPS traffic → iptables DNAT → Squid proxy
3. Squid checks domain against allowlist
4. Allowed → forward to destination
5. Blocked → return 403 Forbidden

### Squid Log Analysis

```bash
# View Squid access log (shows traffic decisions)
docker exec awf-squid cat /var/log/squid/access.log

# Find blocked domains
docker exec awf-squid grep "TCP_DENIED" /var/log/squid/access.log | awk '{print $3}' | sort -u

# Count blocked by domain
docker exec awf-squid grep "TCP_DENIED" /var/log/squid/access.log | awk '{print $3}' | sort | uniq -c | sort -rn

# Real-time blocked traffic
docker exec awf-squid tail -f /var/log/squid/access.log | grep --line-buffered TCP_DENIED
```

### Squid Decision Codes

- `TCP_TUNNEL:HIER_DIRECT` = **ALLOWED** (HTTPS)
- `TCP_MISS:HIER_DIRECT` = **ALLOWED** (HTTP)
- `TCP_DENIED:HIER_NONE` = **BLOCKED**

### Running Commands Through Firewall

```bash
# Basic usage
sudo awf --allow-domains github.com 'curl https://api.github.com'

# With debug logging
sudo awf --allow-domains github.com --log-level debug 'your-command'

# Keep containers for inspection
sudo awf --allow-domains github.com --keep-containers 'your-command'
```

### Preserved Logs Locations

**With `--keep-containers`:**
- Squid: `/tmp/awf-<timestamp>/squid-logs/access.log`
- Agent: `/tmp/awf-<timestamp>/agent-logs/`

**Normal execution (after cleanup):**
- Squid: `/tmp/squid-logs-<timestamp>/access.log`
- Agent: `/tmp/awf-agent-logs-<timestamp>/`

```bash
# Find preserved logs
ls -ldt /tmp/awf-* /tmp/squid-logs-* 2>/dev/null | head -5

# View preserved Squid logs
sudo cat $(ls -t /tmp/squid-logs-*/access.log 2>/dev/null | head -1)
```

## Debugging Workflow Failures

### Step-by-Step Process

1. **Identify the failing workflow run**
   ```bash
   gh run list --status failure --limit 5
   ```

2. **Get run details**
   ```bash
   gh run view <run-id> --verbose
   ```

3. **Download logs**
   ```bash
   gh run download <run-id> --dir ./logs
   # Or use the script:
   npx tsx .github/skills/debugging-workflows/download-workflow-logs.ts --run-id <run-id>
   ```

4. **Analyze the failure**
   - Check job logs for error messages
   - Look for timeout issues
   - Check for permission errors
   - Review network-related errors

5. **For agentic workflows, audit the run**
   ```bash
   gh aw audit <run-id> --json
   ```

6. **If firewall-related, check Squid logs**
   ```bash
   # If containers are still running
   docker exec awf-squid cat /var/log/squid/access.log
   
   # Or check preserved logs
   sudo cat /tmp/squid-logs-*/access.log
   ```

### Common Failure Patterns

#### Permission Denied
```
Error: Resource not accessible by integration
```
**Fix:** Check `permissions:` in workflow frontmatter

#### Domain Blocked
```
curl: (56) Recv failure: Connection reset by peer
```
**Fix:** Add domain to `--allow-domains` or `network:` configuration

#### Timeout
```
Error: The operation was canceled.
```
**Fix:** Increase `timeout-minutes` in workflow configuration

#### Missing Tool
```
Tool 'xyz' not found
```
**Fix:** Add tool to `tools:` configuration in workflow frontmatter

## Related Documentation

- [Architecture](../../../docs/architecture.md) - System architecture details
- [Troubleshooting](../../../docs/troubleshooting.md) - Common issues and solutions
- [GitHub Actions Integration](../../../docs/github_actions.md) - CI/CD setup
- [Logging Documentation](../../../LOGGING.md) - Comprehensive logging guide
- [Debug Firewall Skill](../debug-firewall/SKILL.md) - Firewall-specific debugging
