---
name: linux-services
description: Systemd service management and log access
---

# Linux Services Skill

Manage systemd services and access logs safely.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Check service status, view logs, and restart services when needed.

## Commands

### Service Status

```bash
systemctl status <service>
systemctl is-active <service>
systemctl is-enabled <service>
systemctl list-units --type=service --state=running
```

### Service Control

```bash
systemctl start <service>
systemctl stop <service>
systemctl restart <service>
systemctl reload <service>
```

### Log Access

```bash
journalctl -u <service> --no-pager -n 200
journalctl -u <service> --since "1 hour ago" --no-pager
journalctl -u <service> -f  # follow
```

## Service Restart Protocol

**Before restarting any service:**

1. **Capture current status**
   ```bash
   systemctl status myapp
   ```

2. **Capture recent logs**
   ```bash
   journalctl -u myapp --no-pager -n 50
   ```

3. **Present findings** to user

4. **Restart** (only after acknowledgment)
   ```bash
   systemctl restart myapp
   ```

5. **Verify service started**
   ```bash
   systemctl status myapp
   ```

## Workflow: Diagnose Service Issues

```bash
# 1. Check if service is running
systemctl is-active myapp

# 2. Get detailed status
systemctl status myapp

# 3. Check recent logs for errors
journalctl -u myapp --no-pager -n 100 | grep -i error

# 4. Check when it last started
systemctl show myapp --property=ActiveEnterTimestamp
```

## Workflow: Safe Restart

```bash
# 1. Pre-restart state
systemctl status myapp
journalctl -u myapp --no-pager -n 20

# 2. Restart
systemctl restart myapp

# 3. Verify
sleep 2
systemctl status myapp
journalctl -u myapp --since "1 minute ago" --no-pager
```

## Policies

- **Capture state before restart** - always log pre-restart status
- **Verify after restart** - confirm service is healthy
- **No blind restarts** - understand why restart is needed
- **Critical services** - extra caution with database, auth, networking services
- Report any failed restarts with full log output
