# Simultaneous Launch Button (slb)

[![Go Version](https://img.shields.io/badge/go-1.21+-blue.svg)](https://golang.org)
[![License](https://img.shields.io/badge/License-MIT%2BOpenAI%2FAnthropic%20Rider-blue.svg)](LICENSE)
[![Build Status](https://github.com/Dicklesworthstone/slb/workflows/CI/badge.svg)](https://github.com/Dicklesworthstone/slb/actions)

A cross-platform CLI that implements a **two-person rule** for running potentially destructive commands from AI coding agents.

When an agent wants to run something risky (e.g., `rm -rf`, `git push --force`, `kubectl delete`, `DROP TABLE`), `slb` requires peer review and explicit approval before execution.

## Why This Exists

Coding agents can get tunnel vision, hallucinate, or misunderstand context. A second reviewer (ideally with a different model/tooling) catches mistakes before they become irreversible.

`slb` is built for **multi-agent workflows** where many agent terminals run in parallel and a single bad command could destroy work, data, or infrastructure.

## Key Features

- **Risk-Based Classification**: Commands are automatically classified by risk level
- **Client-Side Execution**: Commands run in YOUR shell environment (inheriting AWS credentials, kubeconfig, virtualenvs, etc.)
- **Command Hash Binding**: Approvals bind to the exact command via SHA-256 hash
- **SQLite Source of Truth**: Project state lives in `.slb/state.db`
- **Agent Mail Integration**: Notify reviewers and track audit trails via MCP Agent Mail
- **TUI Dashboard**: Interactive terminal UI for human reviewers

## Risk Tiers

| Tier | Approvals | Auto-approve | Examples |
|------|-----------|--------------|----------|
| **CRITICAL** | 2+ | Never | `rm -rf /`, `DROP DATABASE`, `terraform destroy`, `git push --force` |
| **DANGEROUS** | 1 | Never | `rm -rf ./build`, `git reset --hard`, `kubectl delete`, `DROP TABLE` |
| **CAUTION** | 0 | After 30s | `rm file.txt`, `git branch -d`, `npm uninstall` |
| **SAFE** | 0 | Immediately | `rm *.log`, `git stash`, `kubectl delete pod` |

## Quick Start

### Installation

#### Recommended: Homebrew (macOS/Linux)

```bash
brew install dicklesworthstone/tap/slb
```

This method provides:
- Automatic updates via `brew upgrade`
- Dependency management
- Easy uninstall via `brew uninstall`

#### Windows: Scoop

```powershell
scoop bucket add dicklesworthstone https://github.com/Dicklesworthstone/scoop-bucket
scoop install dicklesworthstone/slb
```

#### Alternative: Direct Download

Download the latest release for your platform:
- [Linux x86_64](https://github.com/Dicklesworthstone/slb/releases/latest/download/slb-linux-amd64)
- [macOS Intel](https://github.com/Dicklesworthstone/slb/releases/latest/download/slb-darwin-amd64)
- [macOS ARM](https://github.com/Dicklesworthstone/slb/releases/latest/download/slb-darwin-arm64)
- [Windows](https://github.com/Dicklesworthstone/slb/releases/latest/download/slb-windows-amd64.exe)

#### Alternative: Install Script

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/slb/main/scripts/install.sh?$(date +%s)" | bash
```

#### Build from Source

```bash
git clone https://github.com/Dicklesworthstone/slb.git
cd slb && make build
```

#### Go Install

```bash
go install github.com/Dicklesworthstone/slb/cmd/slb@latest
```

### Initialize a Project

```bash
cd /path/to/your/project
slb init
```

This creates a `.slb/` directory with:
- `state.db` - SQLite database for requests, reviews, and sessions
- `config.toml` - Project-specific configuration
- `pending/` - JSON files for pending requests (for watching/interop)

### Basic Workflow

```bash
# 1. Start a session (as an AI agent)
slb session start --agent "GreenLake" --program "claude-code" --model "opus"
# Returns: session_id and session_key

# 2. Run a dangerous command (blocks until approved)
slb run "rm -rf ./build" --reason "Clean build artifacts before fresh compile" --session-id <id>

# 3. Another agent reviews and approves
slb pending                    # See what's waiting for review
slb review <request-id>        # View full details
slb approve <request-id> --session-id <reviewer-id> --comment "Looks safe"

# 4. Original command executes automatically after approval
```

## Commands Reference

### Session Management

```bash
slb session start --agent <name> --program <prog> --model <model>
slb session end --session-id <id>
slb session resume --agent <name>              # Resume after crash
slb session list                               # Show active sessions
slb session heartbeat --session-id <id>        # Keep session alive
```

### Request & Run

```bash
# Primary command (atomic: check, request, wait, execute)
slb run "<command>" --reason "..." [--session-id <id>]

# Plumbing commands
slb request "<command>" --reason "..."         # Create request only
slb status <request-id> [--wait]               # Check status
slb pending [--all-projects]                   # List pending requests
slb cancel <request-id>                        # Cancel own request
```

### Review & Approve

```bash
slb review <request-id>                        # Show full details
slb approve <request-id> --session-id <id>     # Approve request
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
slb patterns list [--tier critical|dangerous|caution|safe]
slb patterns test "<command>"                  # Check what tier a command would be
slb patterns add --tier dangerous "<pattern>"  # Agents can add patterns
```

### Daemon & TUI

```bash
slb daemon start [--foreground]                # Start background daemon
slb daemon stop                                # Stop daemon
slb daemon status                              # Check daemon status
slb tui                                        # Launch interactive TUI
slb watch --session-id <id> --json             # Stream events for agents
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

[rate_limits]
max_pending_per_session = 5
max_requests_per_minute = 10

[notifications]
desktop_enabled = true
desktop_delay_seconds = 60

[daemon]
tcp_addr = ""                       # For Docker/remote agents
tcp_require_auth = true
```

## Default Patterns

### CRITICAL (2+ approvals)

| Pattern | Description |
|---------|-------------|
| `rm -rf /...` | Recursive delete on system paths |
| `DROP DATABASE/SCHEMA` | SQL database destruction |
| `TRUNCATE TABLE` | SQL data destruction |
| `terraform destroy` | Infrastructure destruction |
| `kubectl delete node/namespace/pv/pvc` | Kubernetes critical resources |
| `git push --force` | Force push (not with-lease) |
| `aws terminate-instances` | Cloud resource destruction |
| `dd ... of=/dev/` | Direct disk writes |

### DANGEROUS (1 approval)

| Pattern | Description |
|---------|-------------|
| `rm -rf` | Recursive force delete |
| `git reset --hard` | Discard all changes |
| `git clean -fd` | Remove untracked files |
| `kubectl delete` | Delete Kubernetes resources |
| `terraform destroy -target` | Targeted destroy |
| `DROP TABLE` | SQL table destruction |
| `chmod -R`, `chown -R` | Recursive permission changes |

### CAUTION (auto-approved after 30s)

| Pattern | Description |
|---------|-------------|
| `rm <file>` | Single file deletion |
| `git stash drop` | Discard stashed changes |
| `git branch -d` | Delete local branch |
| `npm/pip uninstall` | Package removal |

### SAFE (skip review)

| Pattern | Description |
|---------|-------------|
| `rm *.log`, `rm *.tmp`, `rm *.bak` | Temporary file cleanup |
| `git stash` | Stash changes (not drop) |
| `kubectl delete pod` | Pod deletion (pods are ephemeral) |
| `npm cache clean` | Cache cleanup |

## IDE Integration

### Claude Code Hooks

Add to your `AGENTS.md`:

```markdown
## SLB Integration

Before running any destructive command, use slb:

\`\`\`bash
# Instead of running directly:
rm -rf ./build

# Use slb:
slb run "rm -rf ./build" --reason "Clean build before fresh compile"
\`\`\`

All DANGEROUS and CRITICAL commands must go through slb review.
```

Generate Claude Code hooks:

```bash
slb integrations claude-hooks > ~/.claude/hooks.json
```

### Cursor Rules

Generate Cursor rules:

```bash
slb integrations cursor-rules > .cursorrules
```

## Shell Completions

```bash
# zsh (~/.zshrc)
eval "$(slb completion zsh)"

# bash (~/.bashrc)
eval "$(slb completion bash)"

# fish (~/.config/fish/config.fish)
slb completion fish | source
```

## Architecture

```
.slb/
├── state.db          # SQLite database (source of truth)
├── config.toml       # Project configuration
├── pending/          # JSON snapshots for watching
│   └── req-<uuid>.json
├── sessions/         # Session files
└── logs/             # Execution logs
    └── req-<uuid>.log
```

**Key Design Decision**: Client-side execution. The daemon is a NOTARY (verifies approvals) not an executor. Commands execute in the calling process's shell environment to inherit:
- AWS_PROFILE, AWS_ACCESS_KEY_ID
- KUBECONFIG
- Activated virtualenvs
- SSH_AUTH_SOCK
- Database connection strings

## Troubleshooting

### "Daemon not running" warning

This is expected - slb works without the daemon (file-based polling). Start the daemon for real-time updates:

```bash
slb daemon start
```

### "Active session already exists"

Resume your existing session instead of starting a new one:

```bash
slb session resume --agent "YourAgent" --create-if-missing
```

### Approval expired

Approvals have a TTL (30min default, 10min for CRITICAL). Re-request if expired:

```bash
slb run "<command>" --reason "..."  # Creates new request
```

### Command hash mismatch

The command was modified after approval. This is a security feature - re-request approval for the modified command.

## Safety Note

`slb` adds friction and peer review for dangerous actions. It does NOT replace:
- Least-privilege credentials
- Environment safeguards
- Proper access controls
- Backup strategies

Use slb as **defense in depth**, not your only protection.

## Claude Code Hook Integration

To integrate with Claude Code, `slb` provides a PreToolUse hook that intercepts Bash commands before execution.

### Quick Setup

```bash
# Install hook (generates script and updates Claude Code settings)
slb hook install

# Check installation status
slb hook status

# Test classification without executing
slb hook test "rm -rf ./build"
```

### How It Works

1. **Hook Script**: A Python script at `~/.slb/hooks/slb_guard.py` intercepts Bash tool calls
2. **Pattern Matching**: Commands are classified using embedded patterns (same as the daemon)
3. **Daemon Communication**: For approval checks, the hook connects to the SLB daemon via Unix socket
4. **Fail-Closed**: If SLB is unavailable, dangerous commands are blocked by default

### Hook Commands

```bash
slb hook generate                 # Generate hook script only
slb hook install [--global]       # Install to Claude Code settings
slb hook uninstall                # Remove hook from settings
slb hook status                   # Show installation status
slb hook test "<command>"         # Test command classification
```

The hook returns one of three actions to Claude Code:
- `allow` - Command proceeds without intervention
- `ask` - User is prompted (CAUTION tier)
- `block` - Command is blocked with message to use `slb request`

## Pattern Matching Engine

The pattern matching engine is the core of `slb`'s command classification system.

### Classification Algorithm

1. **Normalization**: Commands are parsed using shell-aware tokenization
   - Strips wrapper prefixes: `sudo`, `doas`, `env`, `time`, `nohup`, etc.
   - Extracts inner commands from `bash -c 'command'` patterns
   - Resolves paths: `./foo` → `/absolute/path/foo`

2. **Compound Command Handling**: Commands with `;`, `&&`, `||`, `|` are split and each segment is classified independently. The **highest risk segment determines the overall tier**.
   ```
   echo "done" && rm -rf /etc    →  CRITICAL (rm -rf /etc wins)
   ls && git status              →  SAFE (no dangerous patterns)
   ```

3. **Shell-Aware Splitting**: Separators inside quotes are preserved:
   ```
   psql -c "DELETE FROM users; DROP TABLE x;"  →  Single segment (SQL)
   echo "foo" && rm -rf /tmp                   →  Two segments
   ```

4. **Pattern Precedence**: Patterns are checked in order: SAFE → CRITICAL → DANGEROUS → CAUTION
   - First match wins within each tier
   - SAFE patterns skip review entirely

5. **Fail-Safe Parse Handling**: If command parsing fails (unbalanced quotes, complex escapes), the tier is **upgraded by one level**:
   - SAFE → CAUTION
   - CAUTION → DANGEROUS
   - DANGEROUS → CRITICAL

### Fallback Detection

For commands that wrap SQL (e.g., `psql -c "..."`, `mysql -e "..."`), pattern matching may not catch embedded statements. The engine includes fallback detection:

```
DELETE FROM ... (no WHERE clause)  →  CRITICAL
DELETE FROM ... WHERE ...          →  DANGEROUS
```

### Runtime Pattern Management

Agents can add patterns at runtime:

```bash
slb patterns add --tier dangerous "docker system prune"
slb patterns list --tier critical
slb patterns test "kubectl delete deployment nginx"
```

Pattern changes are persisted to SQLite and take effect immediately.

## Request Lifecycle

Requests follow a well-defined state machine with strict transition rules.

### State Diagram

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
     └────┬─────┘                                   └────┬─────┘
          │                                              │
   ┌──────┴──────┬──────────┐                 ┌─────────┴─────────┐
   ▼             ▼          ▼                 ▼                   ▼
┌────────┐  ┌─────────┐  ┌────────┐      ┌──────────┐       ┌──────────┐
│EXECUTED│  │EXEC_FAIL│  │TIMED_OUT│     │ APPROVED │       │ REJECTED │
└────────┘  └─────────┘  └────────┘      └──────────┘       └──────────┘
(terminal)   (terminal)   (terminal)
```

### Terminal States

Once a request reaches a terminal state, no further transitions are allowed:
- **EXECUTED**: Command completed successfully
- **EXECUTION_FAILED**: Command returned non-zero exit code
- **TIMED_OUT**: Command exceeded execution timeout
- **CANCELLED**: Request was cancelled by the requester
- **REJECTED**: Request was rejected by a reviewer

### Approval TTL

Approvals have a time-to-live to prevent stale approvals:
- **Standard requests**: 30 minutes (configurable)
- **CRITICAL requests**: 10 minutes (stricter by default)

If an approval expires before execution, the request must be re-approved.

## Execution Verification

Before any command executes, five security gates must pass:

### Gate 1: Status Check
Request must be in APPROVED state.

### Gate 2: Approval Expiry
Approval TTL must not have elapsed.

### Gate 3: Command Hash
SHA-256 hash of the command must match. This ensures the exact approved command is executed, with no modifications allowed after approval.

### Gate 4: Tier Consistency
Risk tier must still match (patterns may have changed since approval).

### Gate 5: First-Executor-Wins
Only one executor can claim the request. Atomic database transition prevents race conditions when multiple agents try to execute.

## Dry Run & Rollback

### Dry Run Pre-flight

For supported commands, `slb` can run a dry-run variant before the real execution:

```bash
# Supported dry-run variants:
terraform plan          # instead of terraform apply
kubectl diff            # instead of kubectl apply
git diff                # show what would change
```

Enable in config:
```toml
[general]
enable_dry_run = true
```

### Rollback State Capture

Before executing, `slb` can capture state for potential rollback:

```toml
[general]
enable_rollback_capture = true
max_rollback_size_mb = 100
```

Captured state includes:
- **Filesystem**: Tar archive of affected paths
- **Git**: HEAD commit, branch, dirty state, untracked files
- **Kubernetes**: YAML manifests of affected resources

Rollback:
```bash
slb rollback <request-id>           # Restore captured state
slb rollback <request-id> --force   # Force overwrite
```

## Daemon Architecture

The daemon provides real-time notifications and execution verification.

### IPC Communication

Primary communication uses Unix domain sockets:
```
/tmp/slb-<hash>.sock
```

The socket path includes a hash derived from the project path, allowing multiple project daemons to coexist.

### JSON-RPC Protocol

All daemon communication uses JSON-RPC 2.0:

```json
{"jsonrpc": "2.0", "method": "hook_query", "params": {"command": "rm -rf /"}, "id": 1}
```

Available methods:
- `hook_query` - Classify command and check approvals
- `hook_health` - Health check with pattern hash
- `verify_execution` - Check execution gates
- `subscribe` - Subscribe to request events

### TCP Mode (Docker/Remote)

For agents in containers or remote machines:

```toml
[daemon]
tcp_addr = "0.0.0.0:9876"
tcp_require_auth = true
tcp_allowed_ips = ["192.168.1.0/24"]
```

### Timeout Handling

When a request's approval window expires:

| Action | Behavior |
|--------|----------|
| `escalate` | Transition to ESCALATED, notify humans (default) |
| `auto_reject` | Automatically reject the request |
| `auto_approve_warn` | Auto-approve CAUTION tier with warning notification |

```toml
[general]
timeout_action = "escalate"
```

### Desktop Notifications

Native notifications on macOS (AppleScript), Linux (notify-send), and Windows (PowerShell):

```toml
[notifications]
desktop_enabled = true
desktop_delay_seconds = 60    # Wait before first notification
```

## Advanced Configuration

### Cross-Project Reviews

Allow reviewers from other projects:

```toml
[general]
cross_project_reviews = true
review_pool = ["agent-a", "agent-b", "human-reviewer"]
```

### Trusted Self-Approval

Designated agents can self-approve after a delay:

```toml
[agents]
trusted_self_approve = ["senior-agent", "lead-developer"]
trusted_self_approve_delay_seconds = 300    # 5 minute delay
```

### Conflict Resolution

When approvals and rejections conflict:

```toml
[general]
conflict_resolution = "any_rejection_blocks"  # Default
# Options: any_rejection_blocks | first_wins | human_breaks_tie
```

### Different Model Requirement

Require reviewers to use a different AI model:

```toml
[general]
require_different_model = true
different_model_timeout = 300    # Escalate to human after 5 min
```

### Rate Limiting

Prevent request floods:

```toml
[rate_limits]
max_pending_per_session = 5      # Max concurrent pending requests
max_requests_per_minute = 10     # Rate limit per session
rate_limit_action = "reject"     # reject | queue | warn
```

### Dynamic Quorum

Scale approval requirements based on active reviewers:

```toml
[patterns.critical]
dynamic_quorum = true
dynamic_quorum_floor = 2    # Minimum approvals even with few reviewers
```

### Webhook Notifications

Send events to external systems:

```toml
[notifications]
webhook_url = "https://slack.com/webhook/..."
```

Payload includes request details, classification, and event type.

## Security Design Principles

### Defense in Depth

`slb` implements multiple security layers:

1. **Pattern-based classification** - First line of defense
2. **Peer review requirement** - Human/agent oversight
3. **Command hash binding** - Tamper detection
4. **Approval TTL** - Prevent stale approvals
5. **Execution verification gates** - Pre-execution checks
6. **Audit logging** - Full traceability

### Cryptographic Guarantees

- **Command binding**: SHA-256 hash computed at request time, verified at execution
- **Review signatures**: HMAC signatures using session keys prevent review forgery
- **Session keys**: Generated per-session, never stored in plaintext

### Fail-Closed Behavior

When components fail:
- Daemon unreachable → Block dangerous commands (hook)
- Parse error → Upgrade tier by one level
- Approval expired → Require new approval
- Hash mismatch → Reject execution

### Audit Trail

Every action is logged to SQLite with:
- Timestamp
- Actor (session ID, agent name)
- Action type
- Request/review details
- Outcome

Query history:
```bash
slb history [--days 7] [--session <id>] [--status executed]
```

## Environment Variables

All config options can be set via environment:

| Variable | Description |
|----------|-------------|
| `SLB_MIN_APPROVALS` | Minimum approval count |
| `SLB_REQUEST_TIMEOUT` | Request timeout in seconds |
| `SLB_TIMEOUT_ACTION` | What to do on timeout |
| `SLB_DESKTOP_NOTIFICATIONS` | Enable desktop notifications |
| `SLB_WEBHOOK_URL` | Webhook notification URL |
| `SLB_DAEMON_TCP_ADDR` | TCP listen address |
| `SLB_TRUSTED_SELF_APPROVE` | Comma-separated trusted agents |

## Agent Event Streaming

The `slb watch` command provides real-time event streaming for agent workflows.

### Event Stream Format

Events are streamed as newline-delimited JSON (NDJSON) for easy programmatic consumption:

```bash
slb watch --session-id <id>
```

Output:
```json
{"type":"request_pending","request_id":"abc123","tier":"dangerous","command":"rm -rf ./build","ts":"..."}
{"type":"request_approved","request_id":"abc123","reviewer":"BlueLake","ts":"..."}
{"type":"request_executed","request_id":"abc123","exit_code":0,"ts":"..."}
```

### Event Types

| Event | Description |
|-------|-------------|
| `request_pending` | New request awaiting approval |
| `request_approved` | Request was approved |
| `request_rejected` | Request was rejected |
| `request_executed` | Approved request was executed |
| `request_timeout` | Request timed out waiting for approval |
| `request_cancelled` | Request was cancelled |

### Transport Modes

**Daemon IPC (preferred)**: Real-time streaming via Unix socket subscription when the daemon is running.

**Polling fallback**: If the daemon is unavailable, the command falls back to database polling at configurable intervals:

```bash
slb watch --poll-interval 5s
```

### Auto-Approve Mode

For reviewer agents, auto-approve CAUTION tier requests:

```bash
slb watch --session-id <id> --auto-approve-caution
```

## Request Attachments

Requests can include attachments to provide context for reviewers.

### Attachment Types

| Type | Description |
|------|-------------|
| `file` | File contents (base64 encoded) |
| `image` | Screenshots or diagrams (validated dimensions) |
| `command_output` | Output from context-gathering commands |

### Adding Attachments

```bash
# Attach file
slb request "DROP TABLE users" --reason "..." --attach ./schema.sql

# Attach image (screenshot)
slb request "kubectl delete deployment" --reason "..." --attach ./dashboard.png

# Attach command output
slb request "terraform destroy" --reason "..." --attach-cmd "terraform plan -destroy"
```

### Attachment Limits

```toml
[attachments]
max_file_size = 1048576        # 1MB
max_output_size = 102400       # 100KB
max_command_runtime = 10       # seconds
max_image_dimension = 4096     # pixels
```

### Viewing Attachments

```bash
slb show <request-id> --with-attachments
```

## Session Management

Sessions track agent identity and activity for audit and coordination.

### Session Lifecycle

```bash
# Start session (creates session_key for signing)
slb session start --agent "GreenLake" --program "claude-code" --model "opus"

# Resume after crash (preserves session_key)
slb session resume --agent "GreenLake" --create-if-missing

# Force resume (ends mismatched session)
slb session resume --agent "GreenLake" --force

# Heartbeat (update last_active for GC)
slb session heartbeat --session-id <id>

# End session gracefully
slb session end --session-id <id>
```

### Session Garbage Collection

Clean up stale sessions from crashed agents:

```bash
# Show what would be cleaned (dry run)
slb session gc --dry-run --threshold 30m

# Clean sessions inactive > 2 hours
slb session gc --threshold 2h --force

# Interactive cleanup (prompts for each)
slb session gc --threshold 1h
```

### Rate Limit Reset

Reset rate limits for a session (admin use):

```bash
slb session reset-limits --session-id <id>
```

## Emergency Override

For true emergencies, humans can bypass the approval process with extensive logging.

### Usage

```bash
# Interactive (prompts for confirmation)
slb emergency-execute "rm -rf /tmp/broken" --reason "System emergency: disk full"

# Non-interactive (requires hash acknowledgment)
HASH=$(echo -n "rm -rf /tmp/broken" | sha256sum | cut -d' ' -f1)
slb emergency-execute "rm -rf /tmp/broken" --reason "Emergency" --yes --ack $HASH
```

### Safeguards

1. **Mandatory reason**: Must provide `--reason` explaining the bypass
2. **Hash acknowledgment**: Non-interactive use requires command hash via `--ack`
3. **Extensive logging**: Command, reason, timestamp, and operator identity logged
4. **Rollback capture**: Optional state capture with `--capture-rollback`

### Audit Entry

Emergency executions create a permanent audit record:

```json
{
  "type": "emergency_execute",
  "command": "rm -rf /tmp/broken",
  "command_hash": "abc123...",
  "reason": "System emergency: disk full",
  "operator": "human",
  "timestamp": "2026-01-03T10:30:00Z",
  "exit_code": 0
}
```

## Outcome Tracking

Record execution feedback to improve pattern classification over time.

### Recording Outcomes

After execution, record whether the command caused problems:

```bash
# No problems
slb outcome record <request-id>

# Problems occurred
slb outcome record <request-id> --problems --description "Deleted wrong files"

# With rating and notes
slb outcome record <request-id> --rating 4 --notes "Worked as expected"
```

### Viewing Outcomes

```bash
# List recent outcomes
slb outcome list

# Only problematic executions
slb outcome list --problems-only --limit 50

# Statistics summary
slb outcome stats
```

### Statistics Output

```json
{
  "total_executions": 150,
  "problematic": 3,
  "success_rate": 0.98,
  "by_tier": {
    "critical": {"total": 10, "problems": 1},
    "dangerous": {"total": 50, "problems": 2},
    "caution": {"total": 90, "problems": 0}
  }
}
```

This data enables:
- Identifying patterns that should be upgraded/downgraded
- Detecting agents that frequently cause problems
- Improving justification quality requirements

## TUI Dashboard

The interactive terminal UI gives human reviewers an at-a-glance view of pending requests and agent activity.

### Launching

```bash
slb tui
```

### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  SLB Dashboard                                                       │
├─────────────────┬───────────────────────────────────────────────────┤
│  AGENTS         │  PENDING REQUESTS                                  │
│  ───────        │  ────────────────                                  │
│▸ GreenLake      │▸ abc123 CRITICAL rm -rf /etc      BlueLake 2m     │
│  BlueLake       │  def456 DANGEROUS git reset --hard GreenLake 5m   │
│  RedStone       │  ghi789 CAUTION   npm uninstall   RedStone 10m    │
│                 │                                                    │
├─────────────────┴───────────────────────────────────────────────────┤
│  ACTIVITY                                                            │
│  ────────                                                            │
│  10:30:15 GreenLake approved abc123                                  │
│  10:28:42 BlueLake requested def456 (DANGEROUS)                      │
│  10:25:00 RedStone executed xyz999 (exit 0)                          │
└─────────────────────────────────────────────────────────────────────┘
```

### Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Cycle focus between panels |
| `↑/↓` | Navigate within panel |
| `Enter` | View selected request details |
| `a` | Approve selected request |
| `r` | Reject selected request |
| `p` | Open pattern management |
| `h` | Open history view |
| `q` | Quit |

### Panel Details

**Agents Panel**: Active sessions with last activity time and pending request count.

**Pending Panel**: Requests awaiting approval, sorted by urgency (CRITICAL first).

**Activity Panel**: Real-time feed of approvals, rejections, and executions.

## History & Search

Browse and search the full audit history.

### Full-Text Search

```bash
# Search commands
slb history -q "rm -rf"

# Search with filters
slb history -q "database" --tier critical --status executed
```

### Filtering

```bash
# By status
slb history --status pending|approved|rejected|executed|cancelled

# By tier
slb history --tier critical|dangerous|caution|safe

# By agent
slb history --agent "GreenLake"

# By date
slb history --since 2026-01-01
slb history --since 2026-01-03T10:00:00Z

# Combined
slb history --tier critical --status executed --since 2026-01-01 --limit 100
```

### Detailed View

```bash
# Show full request details
slb show <request-id>

# Include all information
slb show <request-id> --with-reviews --with-execution --with-attachments
```

## Agent Mail Integration

SLB integrates with MCP Agent Mail for cross-agent notifications.

### Configuration

```toml
[integrations]
agent_mail_enabled = true
agent_mail_thread = "SLB-Reviews"    # Default thread for notifications
```

### Notification Events

| Event | Thread | Importance |
|-------|--------|------------|
| New CRITICAL request | SLB-Reviews | urgent |
| New DANGEROUS request | SLB-Reviews | normal |
| Request approved | SLB-Reviews | normal |
| Request rejected | SLB-Reviews | normal |
| Request executed | SLB-Reviews | low |
| Request timeout/escalation | SLB-Reviews | urgent |

### Message Format

New request notification:
```markdown
## Command Approval Request

**ID**: abc123
**Risk**: CRITICAL
**Command**: `rm -rf /etc`

### Justification
- Reason: Emergency cleanup
- Expected: Remove config files
- Goal: Reset system state
- Safety: Backed up to S3

---
To review: `slb review abc123`
To approve: `slb approve abc123 --session-id <your-session>`
```

### Manual Notification

Force send notification for a request:

```bash
slb notify <request-id> --via agent-mail
```

## Output Formats

All commands support structured output for programmatic use.

### JSON Mode

```bash
# Global flag
slb --output json pending

# Per-command
slb pending --json
slb history --json
slb session list --json
```

### Output Examples

**Pending requests (JSON)**:
```json
{
  "requests": [
    {
      "id": "abc123",
      "status": "pending",
      "tier": "critical",
      "command": "rm -rf /etc",
      "requestor": "GreenLake",
      "created_at": "2026-01-03T10:00:00Z",
      "approvals": 0,
      "required_approvals": 2
    }
  ],
  "count": 1
}
```

**Session start (JSON)**:
```json
{
  "session_id": "sess_abc123",
  "session_key": "key_xyz789",
  "agent_name": "GreenLake",
  "program": "claude-code",
  "model": "opus",
  "project_path": "/home/user/myproject",
  "started_at": "2026-01-03T10:00:00Z"
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Request not found |
| 4 | Permission denied |
| 5 | Timeout |
| 6 | Rate limited |

## Planning & Development

- Design doc: `PLAN_TO_MAKE_SLB.md`
- Agent rules: `AGENTS.md`
- Task tracking: `bd ready` (beads)
- Prioritization: `bv --robot-priority`

## Contributions

> *About Contributions:* Please don't take this the wrong way, but I do not accept outside contributions for any of my projects. I simply don't have the mental bandwidth to review anything, and it's my name on the thing, so I'm responsible for any problems it causes; thus, the risk-reward is highly asymmetric from my perspective. I'd also have to worry about other "stakeholders," which seems unwise for tools I mostly make for myself for free. Feel free to submit issues, and even PRs if you want to illustrate a proposed fix, but know I won't merge them directly. Instead, I'll have Claude or Codex review submissions via `gh` and independently decide whether and how to address them. Bug reports in particular are welcome. Sorry if this offends, but I want to avoid wasted time and hurt feelings. I understand this isn't in sync with the prevailing open-source ethos that seeks community contributions, but it's the only way I can move at this velocity and keep my sanity.

## License

MIT License (with OpenAI/Anthropic Rider) — see [LICENSE](LICENSE) for details.
