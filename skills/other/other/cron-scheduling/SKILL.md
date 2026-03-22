---
name: cron-scheduling
description: Schedule and manage recurring tasks with cron and systemd timers. Use when creating cron jobs, systemd timers, debugging why a scheduled job didn't run, handling timezones, or monitoring job failures.
---

# Cron & Scheduling

## Cron Syntax

```
┌───────── minute (0-59)
│ ┌─────── hour (0-23)
│ │ ┌───── day of month (1-31)
│ │ │ ┌─── month (1-12)
│ │ │ │ ┌─ day of week (0-7, 0 and 7 = Sunday)
│ │ │ │ │
* * * * * command
```

### Common schedules

```bash
* * * * *           # Every minute
*/5 * * * *         # Every 5 minutes
0 * * * *           # Every hour at :00
30 2 * * *          # Every day at 2:30 AM
0 9 * * 1           # Every Monday at 9:00 AM
0 0 1 * *           # First day of every month at midnight
0 3 * * 0           # Every Sunday at 3 AM
@reboot             # Run once at startup
@daily              # 0 0 * * *
@hourly             # 0 * * * *
```

## Crontab Management

```bash
crontab -e           # Edit crontab
crontab -l           # List crontab
sudo crontab -u www-data -e
crontab -l > crontab-backup-$(date +%Y%m%d).txt
```

### Best practices

```bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=admin@example.com

0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
*/5 * * * * /opt/scripts/healthcheck.sh || /opt/scripts/alert.sh "Health check failed"
* * * * * flock -n /tmp/myjob.lock /opt/scripts/slow-job.sh
```

## Systemd Timers

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Daily backup

[Service]
Type=oneshot
ExecStart=/opt/scripts/backup.sh
User=backup
StandardOutput=journal
StandardError=journal
```

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Run backup daily at 2 AM

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
systemctl list-timers
systemctl list-timers --all
systemctl status backup.service
journalctl -u backup.service --since today
sudo systemctl start backup.service   # run manually
sudo systemctl disable --now backup.timer
```

### OnCalendar syntax

```ini
OnCalendar=daily
OnCalendar=Mon *-*-* 09:00:00
OnCalendar=Mon..Fri *-*-* 08:00:00
OnCalendar=*-*-01 00:00:00       # Monthly
OnCalendar=0/6:00:00             # Every 6 hours
```

```bash
systemd-analyze calendar "Mon *-*-* 09:00:00"
systemd-analyze calendar --iterations=5 "Mon..Fri *-*-* 08:00:00"
```

## Monitoring and Debugging

```bash
systemctl status cron
grep CRON /var/log/syslog
journalctl -u cron --since today
# Test with cron's minimal environment:
env -i HOME=$HOME SHELL=/bin/sh PATH=/usr/bin:/bin /opt/scripts/backup.sh
```

### Job wrapper with logging

```bash
#!/bin/bash
set -euo pipefail
JOB_NAME="${1:?Usage: cron-wrapper.sh <job-name> <command> [args...]}"
shift
LOG_DIR="/var/log/cron-jobs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$JOB_NAME.log"
log() { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*" >> "$LOG_FILE"; }
log "START: $*"
START_TIME=$(date +%s)
if "$@" >> "$LOG_FILE" 2>&1; then
    log "SUCCESS ($(( $(date +%s) - START_TIME ))s)"
else
    EXIT_CODE=$?
    log "FAILED with exit code $EXIT_CODE"
    exit $EXIT_CODE
fi
```

## Tips

- Always redirect output: `>> /var/log/job.log 2>&1`
- Test with `env -i` to simulate cron's minimal environment
- Use `flock` to prevent overlapping runs
- Make all scheduled jobs idempotent
- `systemd-analyze calendar` to verify timer schedules
- Never schedule critical jobs 1:00-3:00 AM if DST applies — use UTC
- Log start time, end time, exit code of every job
- Prefer systemd timers over cron for production services (journald logging, Persistent=true)
