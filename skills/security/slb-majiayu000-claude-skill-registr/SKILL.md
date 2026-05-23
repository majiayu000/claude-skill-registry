---
name: slb
description: "Simultaneous Launch Button - two-person rule for destructive commands. Requires peer review before executing risky operations."
---

# SLB - Simultaneous Launch Button

A CLI that implements a two-person rule for running potentially destructive commands from AI coding agents. When an agent wants to run something risky, SLB requires peer review and approval before execution.

## Why Use SLB

Coding agents can hallucinate or misunderstand context. A second reviewer catches mistakes before they become irreversible. Essential for multi-agent workflows where a bad command could destroy work.

## Risk Tiers

| Tier | Approvals | Auto-approve | Examples |
|------|-----------|--------------|----------|
| **CRITICAL** | 2+ | Never | `rm -rf /`, `DROP DATABASE`, `terraform destroy` |
| **DANGEROUS** | 1 | Never | `rm -rf ./build`, `git reset --hard`, `DROP TABLE` |
| **CAUTION** | 0 | After 30s | `rm file.txt`, `git branch -d` |
| **SAFE** | 0 | Immediately | `rm *.log`, `git stash` |

## Quick Start

### Initialize in a Project

```bash
cd /path/to/project
slb init
```

Creates `.slb/` directory with:
- `state.db` - SQLite database
- `config.toml` - Configuration
- `pending/` - Pending request files

### Start a Session

```bash
slb session start --agent "GreenLake" --program "claude-code" --model "opus"
# Returns session_id and session_key
```

### Run a Dangerous Command

```bash
# Blocks until approved
slb run "rm -rf ./build" --reason "Clean build artifacts" --session-id <id>
```

### Review and Approve

```bash
# See pending requests
slb pending

# View request details
slb review <request-id>

# Approve the request
slb approve <request-id> --session-id <reviewer-id> --comment "Looks safe"

# Or reject
slb reject <request-id> --session-id <reviewer-id> --reason "Too risky"
```

## Commands

### Session Management

```bash
# Start a session
slb session start --agent "AgentName" --program "codex" --model "gpt-5"

# List sessions
slb session list

# End a session
slb session end <session-id>
```

### Running Commands

```bash
# Run with reason
slb run "git push --force" --reason "Force push after rebase" --session-id <id>

# Run with timeout override
slb run "terraform destroy" --reason "Tear down test env" --timeout 300s

# Dry run (classify only, don't execute)
slb run "rm -rf /tmp/test" --dry-run
```

### Reviewing

```bash
# List pending requests
slb pending

# List all requests
slb requests

# View specific request
slb review <request-id>

# Approve
slb approve <request-id> --session-id <id>

# Reject
slb reject <request-id> --session-id <id> --reason "Reason"
```

### TUI Dashboard

```bash
# Interactive review dashboard
slb tui

# Features:
# - See all pending requests
# - Review details
# - Approve/reject inline
```

## Configuration

`.slb/config.toml`:

```toml
[risk]
# Override risk levels for specific patterns
[[risk.overrides]]
pattern = "rm -rf ./node_modules"
tier = "safe"
reason = "Node modules are regenerated"

[timeouts]
caution_auto_approve = "30s"
request_expiry = "1h"

[notifications]
agent_mail = true
```

## Integration with Agent Mail

SLB can notify reviewers via MCP Agent Mail:

```bash
slb init --with-agent-mail

# Reviewers get inbox messages for pending requests
```

## Audit Trail

All requests, reviews, and executions are logged:

```bash
# View audit log
slb audit

# Export audit log
slb audit --export audit.json
```

## Status and Health

```bash
# Check SLB status
slb status

# Check system health
slb health
```

## Example Multi-Agent Workflow

```bash
# Agent 1 wants to run dangerous command
slb run "git push origin main --force" \
  --reason "Rebase complete, need to force push" \
  --session-id agent1-session

# Agent 2 reviews
slb pending
slb review REQ-123
slb approve REQ-123 --session-id agent2-session --comment "Verified rebase is clean"

# Original command executes automatically
```

## Command Classification

SLB automatically classifies commands based on:
- Command patterns (rm -rf, DROP, destroy, etc.)
- Arguments and flags
- Working directory context
- Historical data

Override with explicit tier:
```bash
slb run "custom-script.sh" --tier dangerous --reason "Modifies prod data"
```
