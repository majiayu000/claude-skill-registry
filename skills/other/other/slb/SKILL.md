---
name: slb
description: "Simultaneous Launch Button - Two-person rule for destructive commands in multi-agent workflows. Risk-tiered classification, command hash binding, 5 execution gates, client-side execution with environment inheritance. Go CLI."
---

# SLB — Simultaneous Launch Button

A Go CLI that implements a **two-person rule** for running potentially destructive commands from AI coding agents. When an agent wants to run something risky (e.g., `rm -rf`, `git push --force`, `kubectl delete`, `DROP TABLE`), SLB requires peer review and explicit approval before execution.

## Why This Exists

Coding agents can get tunnel vision, hallucinate, or misunderstand context. A second reviewer (ideally with a different model/tooling) catches mistakes before they become irreversible.

SLB is built for **multi-agent workflows** where many agent terminals run in parallel and a single bad command could destroy work, data, or infrastructure.

## Critical Design: Client-Side Execution

**Commands run in YOUR shell environment**, not on a server. The daemon is a NOTARY (verifies approvals), not an executor. This means commands inherit:

- AWS_PROFILE, AWS_ACCESS_KEY_ID
- KUBECONFIG
- Activated virtualenvs
- SSH_AUTH_SOCK
- Database connection strings

## Risk Tiers

| Tier | Approvals | Auto-approve | Examples |
|------|-----------|--------------|----------|
| **CRITICAL** | 2+ | Never | `rm -rf /`, `DROP DATABASE`, `terraform destroy`, `git push --force` |
| **DANGEROUS** | 1 | Never | `rm -rf ./build`, `git reset --hard`, `kubectl delete`, `DROP TABLE` |
| **CAUTION** | 0 | After 30s | `rm file.txt`, `git branch -d`, `npm uninstall` |
| **SAFE** | 0 | Immediately | `rm *.log`, `git stash`, `kubectl delete pod` |

## Quick Start

### Installation

```bash
# One-liner
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/slb/main/scripts/install.sh | bash

# Or with go install
go install github.com/Dicklesworthstone/slb/cmd/slb@latest
```

### Initialize a Project

```bash
cd /path/to/project
slb init
```

Creates `.slb/` directory with:
- `state.db` - SQLite database (source of truth)
- `config.toml` - Project configuration
- `pending/` - JSON files for pending requests
- `logs/` - Execution logs

### Basic Workflow

```bash
# 1. Start a session (as an AI agent)
slb session start --agent "GreenLake" --program "claude-code" --model "opus"
# Returns: session_id and session_key

# 2. Run a dangerous command (blocks until approved)
slb run "rm -rf ./build" --reason "Clean build artifacts" --session-id <id>

# 3. Another agent reviews and approves
slb pending                    # See what's waiting
slb review <request-id>        # View full details
slb approve <request-id> --session-id <reviewer-id> --comment "Looks safe"

# 4. Original command executes automatically after approval
```

## Commands Reference

### Session Management

```bash
slb session start --agent <name> --program <prog> --model <model>
slb session end --session-id <id>
slb session resume --agent <name> --create-if-missing  # Resume after crash
slb session list                               # Show active sessions
slb session heartbeat --session-id <id>        # Keep session alive
slb session gc --threshold 2h                  # Clean stale sessions
```

### Request & Run

```bash
# Primary command (atomic: check, request, wait, execute)
slb run "<command>" --reason "..." --session-id <id>

# Plumbing commands
slb request "<command>" --reason "..."         # Create request only
slb status <request-id> --wait                 # Check/wait for status
slb pending --all-projects                     # List pending requests
slb cancel <request-id>                        # Cancel own request
```

### Review & Approve

```bash
slb review <request-id>                        # Show full details
slb approve <request-id> --session-id <id> --comment "..."
slb reject <request-id> --session-id <id> --reason "..."
```

### Execution

```bash
slb execute <request-id>                       # Execute approved request
slb emergency-execute "<cmd>" --reason "..."   # Human override (logged)
slb rollback <request-id>                      # Rollback if captured
```

### Pattern Management

```bash
slb patterns list --tier critical              # List patterns by tier
slb patterns test "<command>"                  # Check what tier a command gets
slb patterns add --tier dangerous "<pattern>"  # Add runtime pattern
```

### Daemon & TUI

```bash
slb daemon start --foreground                  # Start background daemon
slb daemon stop                                # Stop daemon
slb daemon status                              # Check daemon status
slb tui                                        # Launch interactive TUI
slb watch --session-id <id> --json             # Stream events (NDJSON)
```

### Claude Code Hook

```bash
slb hook install                               # Install PreToolUse hook
slb hook status                                # Check installation
slb hook test "<command>"                      # Test classification
slb hook uninstall                             # Remove hook
```

### History & Audit

```bash
slb history --tier critical --status executed  # Filter history
slb history -q "rm -rf"                        # Full-text search
slb show <request-id> --with-reviews           # Detailed view
slb outcome record <request-id> --problems     # Record feedback
slb outcome stats                              # Execution statistics
```

## Pattern Matching Engine

### Classification Algorithm

1. **Normalization**: Commands are parsed with shell-aware tokenization
   - Strips wrapper prefixes: `sudo`, `doas`, `env`, `time`, `nohup`
   - Extracts inner commands from `bash -c 'command'`
   - Resolves paths: `./foo` → `/absolute/path/foo`

2. **Compound Command Handling**: Commands with `;`, `&&`, `||`, `|` are split and each segment classified. **Highest risk segment wins**:
   ```
   echo "done" && rm -rf /etc    →  CRITICAL (rm -rf /etc wins)
   ls && git status              →  SAFE (no dangerous patterns)
   ```

3. **Shell-Aware Splitting**: Separators inside quotes preserved:
   ```
   psql -c "DELETE FROM users; DROP TABLE x;"  →  Single segment (SQL)
   echo "foo" && rm -rf /tmp                   →  Two segments
   ```

4. **Pattern Precedence**: SAFE → CRITICAL → DANGEROUS → CAUTION (first match wins)

5. **Fail-Safe Parse Handling**: If parsing fails, tier is **upgraded by one level**:
   - SAFE → CAUTION
   - CAUTION → DANGEROUS
   - DANGEROUS → CRITICAL

### Default Patterns

**CRITICAL (2+ approvals)**:
`rm -rf /...`, `DROP DATABASE/SCHEMA`, `TRUNCATE TABLE`, `terraform destroy`, `kubectl delete node/namespace/pv/pvc`, `git push --force`, `aws terminate-instances`, `dd ... of=/dev/`

**DANGEROUS (1 approval)**:
`rm -rf`, `git reset --hard`, `git clean -fd`, `kubectl delete`, `terraform destroy -target`, `DROP TABLE`, `chmod -R`, `chown -R`

**CAUTION (auto-approved after 30s)**:
`rm <file>`, `git stash drop`, `git branch -d`, `npm/pip uninstall`

**SAFE (skip review)**:
`rm *.log`, `rm *.tmp`, `git stash`, `kubectl delete pod`, `npm cache clean`

## Request Lifecycle

### State Machine

```
                    ┌─────────────┐
                    │   PENDING   │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐───────────────┐
           ▼               ▼               ▼               ▼
     ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
     │ APPROVED │    │ REJECTED │    │ CANCELLED│    │ TIMEOUT  │
     └────┬─────┘    └──────────┘    └──────────┘    └────┬─────┘
          │              (terminal)      (terminal)       │
          ▼                                               ▼
     ┌──────────┐                                   ┌──────────┐
     │EXECUTING │                                   │ESCALATED │
     └────┬─────┘                                   └──────────┘
          │
   ┌──────┴──────┬──────────┐
   ▼             ▼          ▼
┌────────┐  ┌─────────┐  ┌────────┐
│EXECUTED│  │EXEC_FAIL│  │TIMED_OUT│
└────────┘  └─────────┘  └────────┘
(terminal)   (terminal)   (terminal)
```

### Approval TTL

- **Standard requests**: 30 minutes (configurable)
- **CRITICAL requests**: 10 minutes (stricter)

If approval expires before execution, re-approval required.

## Execution Verification (5 Security Gates)

Before any command executes, five gates must pass:

| Gate | Check |
|------|-------|
| **1. Status** | Request must be in APPROVED state |
| **2. Expiry** | Approval TTL must not have elapsed |
| **3. Hash** | SHA-256 hash of command must match (tamper detection) |
| **4. Tier** | Risk tier must still match (patterns may have changed) |
| **5. First-Executor** | Atomic claim prevents race conditions |

## Dry Run & Rollback

### Dry Run Pre-flight

For supported commands, SLB can run a dry-run variant first:

| Command | Dry-run variant |
|---------|-----------------|
| `terraform apply` | `terraform plan` |
| `kubectl apply` | `kubectl diff` |
| `git push` | `git diff` (show what would change) |

```toml
[general]
enable_dry_run = true
```

### Rollback State Capture

Before executing, SLB can capture state:

```toml
[general]
enable_rollback_capture = true
max_rollback_size_mb = 100
```

**Captured state includes:**
- **Filesystem**: Tar archive of affected paths
- **Git**: HEAD commit, branch, dirty state, untracked files
- **Kubernetes**: YAML manifests of affected resources

```bash
slb rollback <request-id>           # Restore captured state
slb rollback <request-id> --force   # Force overwrite
```

## Configuration

Configuration is hierarchical (lowest to highest priority):
1. Built-in defaults
2. User config (`~/.slb/config.toml`)
3. Project config (`.slb/config.toml`)
4. Environment variables (`SLB_*`)
5. Command-line flags

### Example Configuration

```toml
[general]
min_approvals = 2
request_timeout = 1800              # 30 minutes
approval_ttl_minutes = 30
timeout_action = "escalate"         # or "auto_reject", "auto_approve_warn"
require_different_model = true      # Reviewer must use different AI model

[rate_limits]
max_pending_per_session = 5
max_requests_per_minute = 10

[notifications]
desktop_enabled = true
webhook_url = "https://slack.com/webhook/..."

[daemon]
tcp_addr = ""                       # For Docker/remote agents
tcp_require_auth = true

[agents]
trusted_self_approve = ["senior-agent"]
trusted_self_approve_delay_seconds = 300
```

## Advanced Configuration

### Cross-Project Reviews

```toml
[general]
cross_project_reviews = true
review_pool = ["agent-a", "agent-b", "human-reviewer"]
```

### Conflict Resolution

```toml
[general]
conflict_resolution = "any_rejection_blocks"  # Default
# Options: any_rejection_blocks | first_wins | human_breaks_tie
```

### Dynamic Quorum

```toml
[patterns.critical]
dynamic_quorum = true
dynamic_quorum_floor = 2    # Minimum approvals even with few reviewers
```

## Daemon Architecture

### IPC Communication

Unix domain sockets (project-specific):
```
/tmp/slb-<hash>.sock
```

### JSON-RPC Protocol

All daemon communication uses JSON-RPC 2.0:

```json
{"jsonrpc": "2.0", "method": "hook_query", "params": {"command": "rm -rf /"}, "id": 1}
```

**Available methods**: `hook_query`, `hook_health`, `verify_execution`, `subscribe`

### TCP Mode (Docker/Remote)

```toml
[daemon]
tcp_addr = "0.0.0.0:9876"
tcp_require_auth = true
tcp_allowed_ips = ["192.168.1.0/24"]
```

### Timeout Handling

| Action | Behavior |
|--------|----------|
| `escalate` | Transition to ESCALATED, notify humans (default) |
| `auto_reject` | Automatically reject the request |
| `auto_approve_warn` | Auto-approve CAUTION tier with warning |

## Agent Event Streaming

`slb watch` provides real-time NDJSON event streaming:

```bash
slb watch --session-id <id>
```

```json
{"type":"request_pending","request_id":"abc123","tier":"dangerous","command":"rm -rf ./build","ts":"..."}
{"type":"request_approved","request_id":"abc123","reviewer":"BlueLake","ts":"..."}
{"type":"request_executed","request_id":"abc123","exit_code":0,"ts":"..."}
```

**Event types**: `request_pending`, `request_approved`, `request_rejected`, `request_executed`, `request_timeout`, `request_cancelled`

### Auto-Approve Mode (for reviewer agents)

```bash
slb watch --session-id <id> --auto-approve-caution
```

## Request Attachments

Provide context for reviewers:

```bash
# Attach file
slb request "DROP TABLE users" --reason "..." --attach ./schema.sql

# Attach screenshot
slb request "kubectl delete deployment" --reason "..." --attach ./dashboard.png

# Attach command output
slb request "terraform destroy" --reason "..." --attach-cmd "terraform plan -destroy"
```

## Emergency Override

For true emergencies, humans can bypass with extensive logging:

```bash
# Interactive (prompts for confirmation)
slb emergency-execute "rm -rf /tmp/broken" --reason "System emergency: disk full"

# Non-interactive (requires hash acknowledgment)
HASH=$(echo -n "rm -rf /tmp/broken" | sha256sum | cut -d' ' -f1)
slb emergency-execute "rm -rf /tmp/broken" --reason "Emergency" --yes --ack $HASH
```

**Safeguards**: Mandatory reason, hash acknowledgment, extensive logging, optional rollback capture.

## Outcome Tracking

Record execution feedback to improve pattern classification:

```bash
slb outcome record <request-id>                          # Success
slb outcome record <request-id> --problems --description "Deleted wrong files"
slb outcome stats                                        # Statistics
```

## TUI Dashboard

```bash
slb tui
```

```
┌─────────────────────────────────────────────────────────────────────┐
│  SLB Dashboard                                                       │
├─────────────────┬───────────────────────────────────────────────────┤
│  AGENTS         │  PENDING REQUESTS                                  │
│  ───────        │  ────────────────                                  │
│▸ GreenLake      │▸ abc123 CRITICAL rm -rf /etc      BlueLake 2m     │
│  BlueLake       │  def456 DANGEROUS git reset --hard GreenLake 5m   │
├─────────────────┴───────────────────────────────────────────────────┤
│  ACTIVITY                                                            │
│  10:30:15 GreenLake approved abc123                                  │
│  10:28:42 BlueLake requested def456 (DANGEROUS)                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Keys**: `Tab` (cycle panels), `↑/↓` (navigate), `Enter` (view), `a` (approve), `r` (reject), `q` (quit)

## Claude Code Hook Integration

```bash
# Install hook
slb hook install

# Hook actions returned to Claude Code:
# - allow: Command proceeds
# - ask: User prompted (CAUTION tier)
# - block: Blocked with message to use `slb request`
```

Generate IDE integrations:

```bash
slb integrations claude-hooks > ~/.claude/hooks.json
slb integrations cursor-rules > .cursorrules
```

## Security Design Principles

### Defense in Depth (6 layers)

1. Pattern-based classification
2. Peer review requirement
3. Command hash binding (SHA-256)
4. Approval TTL
5. Execution verification gates
6. Audit logging

### Cryptographic Guarantees

- **Command binding**: SHA-256 hash verified at execution
- **Review signatures**: HMAC using session keys
- **Session keys**: Generated per-session, never stored in plaintext

### Fail-Closed Behavior

- Daemon unreachable → Block dangerous commands (hook)
- Parse error → Upgrade tier by one level
- Approval expired → Require new approval
- Hash mismatch → Reject execution

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error |
| `2` | Invalid arguments |
| `3` | Request not found |
| `4` | Permission denied |
| `5` | Timeout |
| `6` | Rate limited |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SLB_MIN_APPROVALS` | Minimum approval count |
| `SLB_REQUEST_TIMEOUT` | Request timeout in seconds |
| `SLB_TIMEOUT_ACTION` | What to do on timeout |
| `SLB_DESKTOP_NOTIFICATIONS` | Enable desktop notifications |
| `SLB_WEBHOOK_URL` | Webhook notification URL |
| `SLB_DAEMON_TCP_ADDR` | TCP listen address |
| `SLB_TRUSTED_SELF_APPROVE` | Comma-separated trusted agents |

## Troubleshooting

### "Daemon not running" warning

SLB works without daemon (file-based polling). Start for real-time:

```bash
slb daemon start
```

### "Active session already exists"

```bash
slb session resume --agent "YourAgent" --create-if-missing
```

### Approval expired

Re-request:
```bash
slb run "<command>" --reason "..."
```

### Command hash mismatch

Command was modified after approval. Re-request for the modified command.

## Safety Note

SLB adds friction and peer review for dangerous actions. It does NOT replace:
- Least-privilege credentials
- Environment safeguards
- Proper access controls
- Backup strategies

Use SLB as **defense in depth**, not your only protection.

## Integration with Flywheel

| Tool | Integration |
|------|-------------|
| **Agent Mail** | Notify reviewers via inbox; track audit trails |
| **BV** | Track SLB requests as beads |
| **CASS** | Search past SLB decisions across sessions |
| **DCG** | DCG blocks automatically; SLB adds peer review layer |
| **NTM** | Coordinate review across agent terminals |
