---
name: troubleshooting-guide
description: Эксперт по troubleshooting гайдам. Используй для создания диагностических процедур, FAQ и решения проблем.
---

# Troubleshooting Guide Creator

Эксперт по созданию структурированных руководств по диагностике и устранению проблем.

## Core Principles

### Problem-Centric Structure

```yaml
troubleshooting_principles:
  - principle: "Start with clear problem statements and symptoms"
    reason: "Users need to quickly identify if guide applies to their issue"

  - principle: "Use If-Then logic flows for decision trees"
    reason: "Systematic elimination of possible causes"

  - principle: "Organize solutions by likelihood and impact"
    reason: "Try simple/common fixes first, escalate to complex"

  - principle: "Follow logical diagnostic sequence (simple to complex)"
    reason: "Minimize time to resolution"

  - principle: "Include verification steps after each fix"
    reason: "Confirm the issue is actually resolved"

  - principle: "Provide rollback instructions"
    reason: "Allow safe recovery if fix causes new issues"
```

### User Experience Focus

- Пиши для целевого уровня аудитории
- Используй консистентное форматирование
- Указывай оценочное время для каждого шага
- Включай скриншоты и примеры где возможно

---

## Standard Guide Template

```markdown
# Troubleshooting: [Problem Title]

**Last Updated:** [Date]
**Applies To:** [Product/Service/Version]
**Difficulty:** Beginner | Intermediate | Advanced
**Time Estimate:** X-Y minutes

---

## Problem Statement

### Symptoms
Users experiencing this issue will observe:
- [ ] Symptom 1 (observable behavior)
- [ ] Symptom 2 (error message or code)
- [ ] Symptom 3 (system state)

### Error Messages
```
[Exact error message or code]
```

### Affected Components
- Component A
- Component B

### Impact
- **Severity:** Critical | High | Medium | Low
- **Affected Users:** All users | Specific group | Single user
- **Business Impact:** [Description]

---

## Quick Checks (2-5 minutes)

Before diving into detailed troubleshooting, verify these common causes:

### Check 1: [Most Common Cause]
**Time:** 30 seconds

```bash
# Command to verify
[diagnostic command]
```

**Expected Output:** [What you should see]
**If this fails:** Continue to Check 2

### Check 2: [Second Most Common Cause]
**Time:** 1 minute

[Steps to verify]

---

## Diagnostic Steps

### Step 1: Gather Information

Collect the following before proceeding:
- [ ] Error logs from [location]
- [ ] System configuration from [location]
- [ ] User actions that triggered the issue

```bash
# Commands to gather diagnostic info
[command 1]
[command 2]
```

### Step 2: Identify the Root Cause

Use this decision tree to identify the cause:

```
Start
  │
  ├─ Is [condition A] true?
  │    ├─ YES → Go to Solution A
  │    └─ NO → Continue
  │
  ├─ Is [condition B] true?
  │    ├─ YES → Go to Solution B
  │    └─ NO → Continue
  │
  └─ None of the above → Escalate to Support
```

---

## Solutions

### Solution A: [Fix Name]
**Difficulty:** Easy
**Time:** 5 minutes
**Risk:** Low

#### Prerequisites
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

#### Steps

1. **Step 1 Title**
   ```bash
   [command]
   ```
   Expected output: [description]

2. **Step 2 Title**
   [Instructions]

3. **Step 3 Title**
   [Instructions]

#### Verify Fix
```bash
[verification command]
```
**Success Indicator:** [What to look for]

#### Rollback (if needed)
```bash
[rollback command]
```

---

### Solution B: [Fix Name]
**Difficulty:** Medium
**Time:** 15 minutes
**Risk:** Medium

[Same structure as Solution A]

---

## Prevention

To prevent this issue from recurring:

1. **Monitoring:** Set up alerts for [metric]
2. **Configuration:** Ensure [setting] is properly configured
3. **Process:** Follow [procedure] when making changes
4. **Training:** Educate team on [best practice]

---

## Escalation

If the above solutions don't resolve the issue:

### When to Escalate
- [ ] Issue persists after trying all solutions
- [ ] Data loss or security concern identified
- [ ] Multiple users affected simultaneously

### Information to Provide
- [ ] Time issue started
- [ ] Steps already attempted
- [ ] Diagnostic logs collected
- [ ] Business impact assessment

### Contact
- **Support Team:** [Contact info]
- **Escalation Path:** [Who to contact]
- **SLA:** [Expected response time]

---

## Related Resources

- [Link to related guide]
- [Link to documentation]
- [Link to FAQ]

---

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| [Date] | [Name] | Initial version |
| [Date] | [Name] | Added Solution C |
```

---

## Diagnostic Patterns

### Layer-by-Layer Approach

```markdown
## Network Connectivity Troubleshooting

### Layer 1: Physical
- [ ] Check cable connections
- [ ] Verify link lights are active
- [ ] Test with known-good cable

### Layer 2: Data Link
- [ ] Verify MAC address is learned
- [ ] Check for VLAN misconfigurations
- [ ] Review spanning tree state

### Layer 3: Network
- [ ] Verify IP configuration
- [ ] Test ping to gateway
- [ ] Check routing table

### Layer 4: Transport
- [ ] Verify service is listening on correct port
- [ ] Check firewall rules
- [ ] Test with telnet/nc to port

### Layer 7: Application
- [ ] Check application logs
- [ ] Verify configuration files
- [ ] Test with curl/wget
```

### Binary Elimination Method

```markdown
## Identifying Faulty Component

Use binary search to isolate the issue:

### Step 1: Test Midpoint
Test the system at the midpoint of the data flow:

```
[Client] → [Load Balancer] → [App Server] → [Database]
                  ↑
            Test here first
```

**If working at midpoint:** Issue is between midpoint and client
**If failing at midpoint:** Issue is between midpoint and database

### Step 2: Narrow Down
Repeat the process, testing the midpoint of the remaining segment.

### Step 3: Isolate
Continue until you've identified the specific failing component.
```

### Symptom-Based Decision Tree

```markdown
## Application Not Responding

```
┌─ Can you reach the server at all?
│
├─ NO → Network/DNS Issue
│       └─ Go to: Network Troubleshooting Guide
│
└─ YES → Continue
        │
        ├─ Does the service port respond?
        │
        ├─ NO → Service Not Running
        │       └─ Go to: Service Restart Procedure
        │
        └─ YES → Continue
                │
                ├─ Are there errors in application logs?
                │
                ├─ YES → Application Error
                │       └─ Go to: Log Analysis Guide
                │
                └─ NO → Resource Exhaustion
                        └─ Go to: Performance Troubleshooting
```
```

---

## Log Analysis Guide

### Common Log Locations

```yaml
linux_logs:
  system:
    - /var/log/syslog
    - /var/log/messages
    - journalctl -xe

  application:
    - /var/log/[app-name]/
    - ~/.pm2/logs/
    - docker logs [container]

  web_server:
    nginx:
      - /var/log/nginx/error.log
      - /var/log/nginx/access.log
    apache:
      - /var/log/apache2/error.log
      - /var/log/httpd/error_log

  database:
    postgresql:
      - /var/log/postgresql/
    mysql:
      - /var/log/mysql/error.log
```

### Log Analysis Commands

```bash
# Find errors in last 100 lines
tail -100 /var/log/app.log | grep -i error

# Find errors with timestamp
grep -i error /var/log/app.log | tail -50

# Watch log in real-time
tail -f /var/log/app.log | grep --line-buffered -i error

# Count errors by type
grep -i error /var/log/app.log | sort | uniq -c | sort -rn | head -20

# Find entries around specific time
awk '/2024-01-15 14:3[0-5]/' /var/log/app.log

# Extract specific fields (JSON logs)
cat /var/log/app.json | jq 'select(.level == "error") | {time, message}'

# Search compressed logs
zgrep -i error /var/log/app.log.*.gz
```

### Error Pattern Recognition

```markdown
## Common Error Patterns

### Connection Errors
```
Pattern: "Connection refused" | "ECONNREFUSED" | "Connection timed out"
Cause: Service not running or firewall blocking
Fix: Check service status, verify port, check firewall rules
```

### Memory Errors
```
Pattern: "Out of memory" | "OOM" | "Cannot allocate memory"
Cause: Process exhausting available RAM
Fix: Increase memory, optimize application, add swap
```

### Disk Errors
```
Pattern: "No space left on device" | "ENOSPC" | "Disk full"
Cause: Filesystem at capacity
Fix: Clean old files, increase disk, enable log rotation
```

### Permission Errors
```
Pattern: "Permission denied" | "EACCES" | "Operation not permitted"
Cause: Insufficient file/directory permissions
Fix: Check ownership, verify permissions, check SELinux/AppArmor
```

### Database Errors
```
Pattern: "Too many connections" | "Connection pool exhausted"
Cause: Connection leak or undersized pool
Fix: Close unused connections, increase pool size, fix leaks
```
```

---

## Specific Problem Templates

### API Not Responding

```markdown
# Troubleshooting: API Not Responding

## Quick Diagnosis Script

```bash
#!/bin/bash
# api-health-check.sh

API_URL="${1:-http://localhost:8080}"
TIMEOUT=5

echo "=== API Health Check ==="
echo "Target: $API_URL"
echo

# 1. DNS Resolution
echo "1. DNS Resolution..."
if host=$(dig +short $(echo $API_URL | sed 's|.*://||' | cut -d'/' -f1 | cut -d':' -f1) 2>/dev/null); then
    echo "   ✅ DNS resolves to: $host"
else
    echo "   ❌ DNS resolution failed"
fi

# 2. Port Connectivity
echo "2. Port Connectivity..."
PORT=$(echo $API_URL | grep -oP ':\K[0-9]+' || echo "80")
HOST=$(echo $API_URL | sed 's|.*://||' | cut -d'/' -f1 | cut -d':' -f1)
if nc -z -w $TIMEOUT $HOST $PORT 2>/dev/null; then
    echo "   ✅ Port $PORT is open"
else
    echo "   ❌ Port $PORT is not reachable"
fi

# 3. HTTP Response
echo "3. HTTP Response..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout $TIMEOUT "$API_URL/health" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ Health endpoint returns 200"
elif [ -n "$HTTP_CODE" ] && [ "$HTTP_CODE" != "000" ]; then
    echo "   ⚠️  Health endpoint returns $HTTP_CODE"
else
    echo "   ❌ No HTTP response"
fi

# 4. Response Time
echo "4. Response Time..."
RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" --connect-timeout $TIMEOUT "$API_URL/health" 2>/dev/null)
if (( $(echo "$RESPONSE_TIME < 1" | bc -l) )); then
    echo "   ✅ Response time: ${RESPONSE_TIME}s"
else
    echo "   ⚠️  Slow response: ${RESPONSE_TIME}s"
fi

echo
echo "=== Check Complete ==="
```

## Decision Tree

```
API Not Responding
       │
       ├─ Can you ping the server?
       │   ├─ NO → Check network/DNS
       │   └─ YES ↓
       │
       ├─ Is the service running?
       │   ├─ NO → Start/restart service
       │   └─ YES ↓
       │
       ├─ Is the port listening?
       │   ├─ NO → Check service configuration
       │   └─ YES ↓
       │
       ├─ Does health check pass?
       │   ├─ NO → Check dependencies (DB, cache)
       │   └─ YES ↓
       │
       └─ Check application logs for errors
```
```

### Database Connection Issues

```markdown
# Troubleshooting: Database Connection Failed

## Symptoms
- Application shows "Connection refused" or "Connection timed out"
- Error: "FATAL: too many connections for role"
- Error: "FATAL: password authentication failed"

## Quick Checks

### 1. Verify Database is Running
```bash
# PostgreSQL
sudo systemctl status postgresql
pg_isready -h localhost -p 5432

# MySQL
sudo systemctl status mysql
mysqladmin -u root -p ping
```

### 2. Test Connection
```bash
# PostgreSQL
psql -h localhost -U username -d database -c "SELECT 1"

# MySQL
mysql -h localhost -u username -p -e "SELECT 1"
```

### 3. Check Connection Count
```sql
-- PostgreSQL
SELECT count(*) FROM pg_stat_activity;
SELECT max_connections FROM pg_settings WHERE name = 'max_connections';

-- MySQL
SHOW STATUS LIKE 'Threads_connected';
SHOW VARIABLES LIKE 'max_connections';
```

## Solutions

### Solution 1: Restart Connection Pool
```bash
# If using PgBouncer
sudo systemctl restart pgbouncer

# Application restart
sudo systemctl restart myapp
```

### Solution 2: Clear Idle Connections
```sql
-- PostgreSQL: Kill idle connections older than 10 minutes
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
  AND state_change < NOW() - INTERVAL '10 minutes';
```

### Solution 3: Increase Max Connections
```sql
-- PostgreSQL (requires restart)
ALTER SYSTEM SET max_connections = 200;

-- MySQL (can be done live)
SET GLOBAL max_connections = 200;
```
```

---

## Quality Assurance Checklist

### Pre-Publication Review

```markdown
## Troubleshooting Guide Quality Checklist

### Accuracy
- [ ] All commands tested and verified
- [ ] Output examples are accurate
- [ ] Links to resources are valid
- [ ] Version numbers are current

### Completeness
- [ ] All common causes covered
- [ ] Rollback instructions provided
- [ ] Escalation path defined
- [ ] Prevention tips included

### Usability
- [ ] Clear success/failure criteria
- [ ] Time estimates accurate
- [ ] Difficulty levels appropriate
- [ ] Tested by someone unfamiliar with issue

### Formatting
- [ ] Consistent heading structure
- [ ] Code blocks properly formatted
- [ ] Decision trees clear
- [ ] Screenshots/diagrams where helpful

### Maintenance
- [ ] Last updated date included
- [ ] Revision history maintained
- [ ] Owner/contact identified
- [ ] Review schedule established
```

---

## Лучшие практики

1. **Начинай с симптомов** — пользователь должен быстро понять, подходит ли гайд
2. **Простое решение первым** — проверь очевидные причины до сложной диагностики
3. **Включай verification steps** — как понять, что проблема решена
4. **Документируй rollback** — возможность отката если fix не помог
5. **Указывай время** — пользователь должен знать сколько займёт каждый шаг
6. **Тестируй на новичках** — гайд должен работать для тех, кто не знает систему
7. **Обновляй регулярно** — устаревший гайд хуже чем его отсутствие
8. **Включай escalation path** — когда и к кому обращаться
