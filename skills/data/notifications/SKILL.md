---
name: notifications
description: View and manage sync notifications - import completions, discrepancies, sync failures. Filter by type and severity, show details, dismiss notifications.
---

# Notifications Command

View and manage sync notifications - import completions, discrepancies, sync failures, and more.

## Usage

```bash
/sw:notifications                     # List pending notifications
/sw:notifications --all               # Include dismissed notifications
/sw:notifications --type sync-failure # Filter by type
/sw:notifications --severity warning  # Filter by severity
/sw:notifications show <id>           # Show notification details
/sw:notifications dismiss <id>        # Dismiss a notification
/sw:notifications dismiss-all         # Dismiss all pending notifications
```

## Arguments

- `--all`: Include dismissed notifications in the list
- `--type <type>`: Filter by notification type:
  - `import-complete`: Import job finished
  - `discrepancy`: Code-spec discrepancy detected
  - `sync-failure`: Sync operation failed
  - `drift`: Status drift detected
  - `job-complete`: Scheduled job finished
- `--severity <level>`: Filter by severity: `info`, `warning`, `critical`
- `--json`: Output as JSON for scripting

## Subcommands

### list (default)

Lists notifications with severity emoji, title, and age.

```
📬 PENDING NOTIFICATIONS (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

notif-abc123   ❗ CRITICAL   GitHub sync failed           2m ago
notif-def456   ⚠️ WARNING    2 discrepancies in FS-045    1h ago
notif-ghi789   ℹ️ INFO       107 items imported           3h ago

Use '/sw:notifications show <id>' to view details
Use '/sw:notifications dismiss <id>' to dismiss
```

### show <id>

Shows full notification details including data payload.

```
📬 NOTIFICATION DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID:        notif-abc123
Type:      sync-failure
Severity:  ❗ critical
Title:     GitHub sync failed
Message:   Rate limit exceeded. Retry in 15 minutes.
Created:   2025-12-01 12:00:00 (2m ago)

Data:
  platform: github
  error: Rate limit exceeded
  retryAfter: 900
```

### dismiss <id>

Dismisses a single notification.

```
✅ Dismissed notification notif-abc123

Remaining: 2 pending notifications
```

### dismiss-all

Dismisses all pending notifications with confirmation.

```
⚠️ This will dismiss 3 pending notifications.
Proceed? [y/N]: y

✅ Dismissed 3 notifications
```

## Related

- `/sw:sync-monitor`: Dashboard showing notification summary
- `/sw:discrepancies`: View and act on discrepancy notifications
