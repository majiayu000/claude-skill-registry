---
name: monitor-system
description: Monitor system health, detect errors, implement recovery procedures,
  restart failed processes, maintain audit logs. Use for system health checks, error
  recovery, process monitoring, or when user mentions "system status", "errors", "logs".
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
model: sonnet
---

# Monitor System Skill

**Version:** 1.0
**Last Updated:** 2026-01-12
**Purpose:** System health monitoring, error recovery, and comprehensive audit logging

---

## Overview

This skill provides autonomous system monitoring and self-healing capabilities for the AI Employee. It ensures 24/7 operation by:

- Monitoring health of all Watchers and MCP servers
- Detecting and recovering from errors automatically
- Restarting crashed processes
- Maintaining comprehensive audit logs
- Providing graceful degradation when services fail

---

## When to Use This Skill

**Auto-Activate When:**
- System health check is needed (every 5 minutes)
- Process failure is detected
- Error recovery is required
- Audit logs need to be reviewed or rotated
- User asks about system status

**Keywords:** "system status", "health check", "errors", "logs", "monitoring", "restart", "recovery"

---

## Core Responsibilities

### 1. Health Monitoring
- Check all Watcher processes (Gmail, WhatsApp, LinkedIn, etc.)
- Verify MCP server connectivity (Email, Xero, Social Media)
- Monitor disk space and network connectivity
- Calculate system health score (0-100)
- Run checks every 5 minutes

### 2. Error Detection & Recovery
- Monitor logs for errors across all systems
- Classify error severity (Critical/High/Medium/Low)
- Implement auto-recovery procedures
- Retry failed operations with exponential backoff
- Escalate to human after 3 failed attempts

### 3. Process Management
- Monitor critical process PIDs
- Auto-restart crashed processes
- Maintain process status tracking
- Alert user when manual intervention needed

### 4. Audit Logging
- Log all AI actions in structured JSON format
- Rotate logs daily, archive weekly
- Maintain retention policies by log type
- Provide log analysis capabilities

### 5. Graceful Degradation
- Queue operations when services are down
- Continue non-dependent operations
- Retry when services are restored
- Maintain system availability

---

## Workflow

### Health Check Cycle (Every 5 Minutes)

```
1. Run health_monitor.py
   ├─ Check Watcher processes (PID validation)
   ├─ Verify MCP server connectivity
   ├─ Check disk space (>10% free required)
   ├─ Verify network connectivity
   └─ Calculate health score

2. If health score < 80:
   ├─ Log warning
   ├─ Identify failing components
   └─ Trigger recovery procedures

3. If health score < 50:
   ├─ Create high-priority alert
   ├─ Attempt auto-recovery
   └─ Escalate to user if recovery fails

4. Update System_Status.md with results
```

### Error Recovery Flow

```
1. Error detected in logs
   ↓
2. Classify severity using error-catalog.md
   ↓
3. Select recovery procedure from recovery-procedures.md
   ↓
4. Attempt recovery (up to 3 times with exponential backoff)
   ↓
5. If successful: Log recovery, resume operations
   If failed: Create escalation alert for user
```

### Process Restart Flow

```
1. Process PID not found or unresponsive
   ↓
2. Log incident
   ↓
3. Attempt restart (watchdog_manager.py)
   ↓
4. Verify process started successfully
   ↓
5. If 3 restart attempts fail:
   └─ Create critical alert in /Needs_Action/
```

---

## File Structure

```
Vault/
├── Logs/
│   ├── system/
│   │   ├── health_checks.json
│   │   ├── incidents/
│   │   └── archives/
│   ├── actions/
│   │   ├── YYYY-MM-DD.json
│   │   └── archives/
│   ├── financial/
│   │   └── archives/
│   └── security/
│       └── archives/
├── System_Status.md
└── Needs_Action/
    └── ALERT_*.md (critical escalations)
```

---

## Key Reference Documents

### 1. error-catalog.md
Complete taxonomy of all error types with severity classifications and recovery strategies.

### 2. recovery-procedures.md
Step-by-step procedures for recovering from each error category.

### 3. health-check-matrix.md
Health scoring system with component weights and thresholds.

### 4. audit-log-schema.md
JSON schema for all log types with retention policies.

---

## Scripts

### health_monitor.py
**Purpose:** Continuous health monitoring
**Frequency:** Every 5 minutes
**Actions:**
- Check all process PIDs
- Test MCP server connectivity
- Monitor disk space
- Verify network
- Calculate health score
- Update System_Status.md

### error_handler.py
**Purpose:** Classify and recover from errors
**Actions:**
- Parse logs for errors
- Classify severity
- Execute recovery procedures
- Track recovery attempts
- Escalate failures

### log_aggregator.py
**Purpose:** Comprehensive audit logging
**Actions:**
- Collect logs from all sources
- Rotate logs daily
- Archive logs weekly
- Enforce retention policies
- Provide log analysis

### watchdog_manager.py
**Purpose:** Process monitoring and restart
**Actions:**
- Monitor critical process PIDs
- Detect crashes
- Auto-restart with exponential backoff
- Track restart attempts
- Create alerts after 3 failures

---

## Health Score Calculation

**Total: 100 points**

| Component | Weight | Check |
|-----------|--------|-------|
| Watchers | 30pts | All processes running |
| MCP Servers | 25pts | All servers responding |
| Disk Space | 15pts | >10% free |
| Network | 15pts | API connectivity |
| Logs | 10pts | Writing successfully |
| Vault Access | 5pts | Read/write permissions |

**Thresholds:**
- 90-100: Excellent (green)
- 80-89: Good (yellow - minor issues)
- 50-79: Degraded (orange - auto-recovery active)
- 0-49: Critical (red - user intervention needed)

---

## Error Recovery Strategies

### Process Crash
1. Log incident with timestamp, process name, exit code
2. Wait 5 seconds (exponential: 5s, 10s, 20s)
3. Execute restart command
4. Verify PID within 30 seconds
5. If 3 attempts fail: Create critical alert

### API Authentication Failure
1. Log authentication error
2. Attempt token refresh
3. If refresh fails: Request user reauth
4. Queue pending operations
5. Resume when auth restored

### Disk Space Low (<10% free)
1. Archive old logs immediately
2. Compress archived logs
3. Clean temp directories
4. If still low: Alert user

### Network Outage
1. Detect network failure
2. Queue all outbound operations
3. Continue local operations (file processing, etc.)
4. Retry network operations when connectivity restored

---

## Log Retention Policies

| Log Type | Retention | Archive | Purpose |
|----------|-----------|---------|---------|
| Actions | 90 days | Compress, keep 1 year | Audit trail |
| System | 60 days | Compress, keep 6 months | Debugging |
| Errors | 180 days | Compress, keep 2 years | Pattern analysis |
| Security | 365 days | Compress, keep 7 years | Compliance |
| Financial | 7 years | Compress, permanent | Legal requirement |

---

## Example Usage

### Check System Health
```bash
# Run manual health check
python .claude/skills/monitor-system/scripts/health_monitor.py

# View latest status
cat Vault/System_Status.md
```

### Review Error Logs
```bash
# View today's errors
cat Vault/Logs/system/incidents/$(date +%Y-%m-%d).json

# Search for specific error
grep "API_AUTH_FAILURE" Vault/Logs/system/*.json
```

### Restart Failed Process
```bash
# Manually restart a watcher
python .claude/skills/monitor-system/scripts/watchdog_manager.py restart gmail_watcher
```

---

## Success Criteria

**This skill is working correctly when:**
- [ ] Health checks run every 5 minutes automatically
- [ ] All processes monitored and restarted on failure
- [ ] Errors classified and recovery attempted
- [ ] Audit logs written in correct JSON format
- [ ] Log rotation happens daily
- [ ] System maintains 99%+ uptime over 7 days
- [ ] User receives alerts only for true failures (not false positives)

---

## Integration with Other Skills

**Dependencies:**
- All other skills must be operational (this monitors them)
- Requires access to all Watcher scripts
- Needs MCP server configurations
- Uses Business_Goals.md for alert priorities

**Provides to Others:**
- System health data for CEO briefings
- Error metrics for performance analysis
- Audit trail for all actions
- Recovery capabilities for all services

---

## Important Notes

1. **Runs continuously** - Health checks every 5 minutes
2. **Auto-recovery first** - Only escalate after 3 failed attempts
3. **Structured logging** - Always JSON format for parsing
4. **Retention compliance** - Financial logs keep 7 years
5. **Graceful degradation** - System remains partially functional during issues

---

## When NOT to Use This Skill

- User wants to view business performance (use generate-ceo-briefing)
- User wants to check task status (use process-tasks)
- User wants financial summary (use manage-accounting)

This skill is specifically for **system health and operations**, not business intelligence.

---

**Next Steps:** Reference the detailed documentation in /reference/ for implementation specifics and use the scripts in /scripts/ for actual monitoring operations.

**Maintenance:** Review error patterns monthly, update recovery procedures as needed, adjust health thresholds based on experience.
