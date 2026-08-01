# SLB Commands — Complete Reference

## Table of Contents
- [Session Management](#session-management)
- [Request & Run](#request--run)
- [Review & Approve](#review--approve)
- [Execution](#execution)
- [Pattern Management](#pattern-management)
- [Daemon & TUI](#daemon--tui)
- [Claude Code Hook](#claude-code-hook)
- [History & Audit](#history--audit)
- [Exit Codes](#exit-codes)

---

## Session Management

```bash
slb session start --agent <name> --program <prog> --model <model>
slb session end --session-id <id>
slb session resume --agent <name> --create-if-missing  # Resume after crash
slb session list                               # Show active sessions
slb session heartbeat --session-id <id>        # Keep session alive
slb session gc --threshold 2h                  # Clean stale sessions
```

---

## Request & Run

```bash
# Primary command (atomic: check, request, wait, execute)
slb run "<command>" --reason "..." --session-id <id>

# Plumbing commands
slb request "<command>" --reason "..."         # Create request only
slb status <request-id> --wait                 # Check/wait for status
slb pending --all-projects                     # List pending requests
slb cancel <request-id>                        # Cancel own request
```

---

## Review & Approve

```bash
slb review <request-id>                        # Show full details
slb approve <request-id> --session-id <id> --comment "..."
slb reject <request-id> --session-id <id> --reason "..."
```

---

## Execution

```bash
slb execute <request-id>                       # Execute approved request
slb emergency-execute "<cmd>" --reason "..."   # Human override (logged)
slb rollback <request-id>                      # Rollback if captured
slb rollback <request-id> --force              # Force overwrite
```

---

## Pattern Management

```bash
slb patterns list --tier critical              # List patterns by tier
slb patterns test "<command>"                  # Check what tier a command gets
slb patterns add --tier dangerous "<pattern>"  # Add runtime pattern
```

---

## Daemon & TUI

```bash
slb daemon start --foreground                  # Start background daemon
slb daemon stop                                # Stop daemon
slb daemon status                              # Check daemon status
slb tui                                        # Launch interactive TUI
slb watch --session-id <id> --json             # Stream events (NDJSON)
slb watch --session-id <id> --auto-approve-caution  # Auto-approve CAUTION tier
```

---

## Claude Code Hook

```bash
slb hook install                               # Install PreToolUse hook
slb hook status                                # Check installation
slb hook test "<command>"                      # Test classification
slb hook uninstall                             # Remove hook

# Generate IDE integrations
slb integrations claude-hooks > ~/.claude/hooks.json
slb integrations cursor-rules > .cursorrules
```

---

## History & Audit

```bash
slb history --tier critical --status executed  # Filter history
slb history -q "rm -rf"                        # Full-text search
slb show <request-id> --with-reviews           # Detailed view
slb outcome record <request-id> --problems     # Record feedback
slb outcome stats                              # Execution statistics
```

---

## Request Attachments

```bash
# Attach file
slb request "DROP TABLE users" --reason "..." --attach ./schema.sql

# Attach screenshot
slb request "kubectl delete deployment" --reason "..." --attach ./dashboard.png

# Attach command output
slb request "terraform destroy" --reason "..." --attach-cmd "terraform plan -destroy"
```

---

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

---

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
