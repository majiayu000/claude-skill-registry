# SLB Configuration — Reference

## Table of Contents
- [Configuration Hierarchy](#configuration-hierarchy)
- [Example Configuration](#example-configuration)
- [Advanced Configuration](#advanced-configuration)
- [Daemon Architecture](#daemon-architecture)
- [Dry Run & Rollback](#dry-run--rollback)
- [Troubleshooting](#troubleshooting)

---

## Configuration Hierarchy

Configuration is hierarchical (lowest to highest priority):
1. Built-in defaults
2. User config (`~/.slb/config.toml`)
3. Project config (`.slb/config.toml`)
4. Environment variables (`SLB_*`)
5. Command-line flags

---

## Example Configuration

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

---

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

---

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

---

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

---

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
