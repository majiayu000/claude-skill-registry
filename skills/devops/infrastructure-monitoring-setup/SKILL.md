---
name: infrastructure-monitoring-setup
description: |
  Configures automated infrastructure monitoring with mobile alerts (ntfy.sh and Home
  Assistant) and auto-recovery for common failures. Use when setting up monitoring,
  configuring mobile notifications, enabling auto-recovery, or troubleshooting alert
  delivery. Triggers on "setup monitoring", "configure alerts", "mobile notifications",
  "enable auto-recovery", "monitoring not working", or "not getting alerts". Works with
  infrastructure-monitor.sh script, systemd timer, ntfy.sh push notifications, and
  optional Home Assistant integration.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Edit
---

# Infrastructure Monitoring Setup Skill

Complete setup and configuration of automated infrastructure monitoring with mobile push notifications and auto-recovery capabilities.

## Quick Start

Quick setup for monitoring (5 minutes):

```bash
# 1. Create unique ntfy topic
TOPIC="infra-$(openssl rand -hex 8)"
echo "Your topic: $TOPIC"

# 2. Add to .env
echo "ALERT_ENABLED=true" >> /home/dawiddutoit/projects/network/.env
echo "NTFY_SERVER=https://ntfy.sh" >> /home/dawiddutoit/projects/network/.env
echo "NTFY_TOPIC=$TOPIC" >> /home/dawiddutoit/projects/network/.env
echo "AUTO_RECOVER=true" >> /home/dawiddutoit/projects/network/.env

# 3. Install systemd service
sudo cp /home/dawiddutoit/projects/network/systemd/infrastructure-monitor.* /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now infrastructure-monitor.timer

# 4. Test
/home/dawiddutoit/projects/network/scripts/infrastructure-monitor.sh
```

Then install ntfy app on phone and subscribe to your topic.

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Install ntfy Mobile App
   - 3.2 Configure Monitoring in .env
   - 3.3 Install Systemd Timer
   - 3.4 Test Monitoring and Alerts
   - 3.5 Configure Home Assistant Integration (Optional)
   - 3.6 Verify Auto-Recovery
   - 3.7 View Monitoring Logs
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## 1. When to Use This Skill

**Explicit Triggers:**
- "Setup monitoring"
- "Configure mobile alerts"
- "Enable auto-recovery"
- "Setup ntfy notifications"
- "Configure Home Assistant alerts"

**Implicit Triggers:**
- Want to be notified of infrastructure failures
- Need automated recovery for common issues
- Infrastructure has been down without detection
- Want proactive monitoring

**Debugging Triggers:**
- "Why am I not getting alerts?"
- "Is monitoring working?"
- "How to test notifications?"

## 2. What This Skill Does

1. **Mobile Alerts** - Configures ntfy.sh push notifications to phone
2. **Auto-Recovery** - Enables automatic fixes for common failures
3. **HA Integration** - Optional Home Assistant notification integration
4. **Systemd Service** - Installs timer to run monitoring every 5 minutes
5. **Tests Setup** - Verifies notifications and recovery work
6. **Logs Access** - Shows how to view monitoring logs
7. **Troubleshooting** - Diagnoses alert delivery issues

## 3. Instructions

### 3.1 Install ntfy Mobile App

**Install app:**
- Android: https://play.google.com/store/apps/details?id=io.heckel.ntfy
- iOS: https://apps.apple.com/us/app/ntfy/id1625396347

**Subscribe to topic:**
1. Open ntfy app
2. Tap "+" to add subscription
3. Enter topic: `infra-YOUR-RANDOM-ID` (you'll generate this in step 3.2)
4. Server: `https://ntfy.sh`
5. Tap "Subscribe"

**Note:** You need the topic ID from step 3.2 before subscribing. Come back here after generating it.

### 3.2 Configure Monitoring in .env

**Generate unique topic ID:**

```bash
TOPIC="infra-$(openssl rand -hex 8)"
echo "Your unique topic: $TOPIC"
```

Save this topic ID - you'll use it in the ntfy app.

**Add monitoring configuration to .env:**

```bash
# Navigate to project directory
cd /home/dawiddutoit/projects/network

# Add monitoring variables
cat >> .env << EOF

# Monitoring & Alerts
ALERT_ENABLED=true
NTFY_SERVER=https://ntfy.sh
NTFY_TOPIC=$TOPIC
AUTO_RECOVER=true
EOF
```

**Verify configuration:**

```bash
grep -A4 "Monitoring & Alerts" /home/dawiddutoit/projects/network/.env
```

Expected:
```
# Monitoring & Alerts
ALERT_ENABLED=true
NTFY_SERVER=https://ntfy.sh
NTFY_TOPIC=infra-a3f7d92b4c8e1f56
AUTO_RECOVER=true
```

**Configuration options:**

| Variable | Purpose | Default |
|----------|---------|---------|
| `ALERT_ENABLED` | Enable mobile push notifications | `false` |
| `NTFY_SERVER` | ntfy.sh server URL | `https://ntfy.sh` |
| `NTFY_TOPIC` | Unique topic for your alerts | None (required) |
| `AUTO_RECOVER` | Enable automatic recovery | `true` |

**To disable auto-recovery but keep alerts:**
```bash
# Edit .env
nano /home/dawiddutoit/projects/network/.env
# Change: AUTO_RECOVER=false
```

### 3.3 Install Systemd Timer

Install systemd service and timer to run monitoring every 5 minutes:

```bash
# Copy service files
sudo cp /home/dawiddutoit/projects/network/systemd/infrastructure-monitor.service /etc/systemd/system/
sudo cp /home/dawiddutoit/projects/network/systemd/infrastructure-monitor.timer /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start timer
sudo systemctl enable infrastructure-monitor.timer
sudo systemctl start infrastructure-monitor.timer
```

**Verify timer is active:**

```bash
# Check timer status
systemctl list-timers infrastructure-monitor.timer

# Check service status
sudo systemctl status infrastructure-monitor.timer
```

Expected:
```
● infrastructure-monitor.timer - Run infrastructure monitoring every 5 minutes
     Loaded: loaded (/etc/systemd/system/infrastructure-monitor.timer; enabled)
     Active: active (waiting) since...
```

**Timer configuration:**
- Runs every 5 minutes
- Starts 1 minute after boot
- Persistent (survives reboots)

### 3.4 Test Monitoring and Alerts

**Test monitoring script:**

```bash
# Run monitoring manually
/home/dawiddutoit/projects/network/scripts/infrastructure-monitor.sh
```

Expected output shows:
- Docker containers checked
- Tunnel connectivity tested
- Service health verified
- Network interface status
- Alert sent to ntfy topic

**Test alert delivery:**

Within 30 seconds, you should receive push notification on phone with infrastructure status.

**If no notification received:**

Check ntfy topic subscription:
```bash
# Test sending to topic directly
curl -d "Test from infrastructure monitoring" https://ntfy.sh/$TOPIC
```

If direct curl works but monitoring doesn't:
- Check ALERT_ENABLED=true in .env
- Verify NTFY_TOPIC matches app subscription
- Check script has network access

### 3.5 Configure Home Assistant Integration (Optional)

**Why use Home Assistant integration:**
- Centralized home automation alerts
- Can trigger automations based on infrastructure status
- Redundancy with ntfy.sh
- Integration with existing HA notifications

**Prerequisites:**
- Home Assistant running and accessible
- HA mobile app installed (for notify.mobile_app_* service)

**Step 1: Create Long-Lived Access Token**

1. Go to Home Assistant: http://192.168.68.123:8123
2. Click your profile (bottom left)
3. Scroll to "Long-Lived Access Tokens"
4. Click "Create Token"
5. Name: "Infrastructure Monitoring"
6. Copy token (shown only once)

**Step 2: Find Notification Service Name**

1. In Home Assistant: Developer Tools → Services
2. Filter by "notify"
3. Find your mobile app service: `notify.mobile_app_your_phone`

**Step 3: Add to .env**

```bash
# Edit .env
nano /home/dawiddutoit/projects/network/.env

# Add HA configuration
HA_NOTIFICATIONS_ENABLED=true
HA_BASE_URL=http://192.168.68.123:8123
HA_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
HA_NOTIFY_SERVICE=notify.mobile_app_your_phone
```

**Step 4: Test HA Notifications**

```bash
# Run monitoring (should send to both ntfy and HA)
/home/dawiddutoit/projects/network/scripts/infrastructure-monitor.sh
```

Check you receive notification in Home Assistant companion app.

**Troubleshooting HA notifications:**

```bash
# Test HA API access
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://192.168.68.123:8123/api/

# Test notification service
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test from infrastructure monitoring"}' \
  http://192.168.68.123:8123/api/services/notify/mobile_app_your_phone
```

### 3.6 Verify Auto-Recovery

Monitor logs to see auto-recovery in action:

```bash
# View live monitoring logs
sudo journalctl -u infrastructure-monitor.service -f

# Or check persistent log
tail -f /var/log/infrastructure-monitor.log
```

**Auto-recovery capabilities:**

| Issue | Detection | Recovery Action |
|-------|-----------|----------------|
| Stuck cloudflared | No registrations in 10 min | Restart cloudflared container |
| Docker network isolation | Ping fails between containers | Recreate bridge network |
| Inactive Ethernet | WiFi used instead of eth0 | Activate Ethernet connection |
| Service failures | HTTP health checks fail | Restart affected containers |

**Test auto-recovery:**

```bash
# Simulate stuck tunnel
docker stop cloudflared

# Wait 5 minutes (next monitoring run)
# Check logs - should show tunnel restarted

# Verify tunnel recovered
docker ps | grep cloudflared
docker logs cloudflared | grep "Registered tunnel"
```

### 3.7 View Monitoring Logs

**View systemd service logs:**

```bash
# Live monitoring logs
sudo journalctl -u infrastructure-monitor.service -f

# Last 50 lines
sudo journalctl -u infrastructure-monitor.service -n 50

# Logs from today
sudo journalctl -u infrastructure-monitor.service --since today

# Logs with timestamps
sudo journalctl -u infrastructure-monitor.service -o short-iso
```

**View persistent log file:**

```bash
# Live tail
tail -f /var/log/infrastructure-monitor.log

# Last 100 lines
tail -100 /var/log/infrastructure-monitor.log

# Search for errors
grep -i error /var/log/infrastructure-monitor.log

# Search for recoveries
grep -i "recovered" /var/log/infrastructure-monitor.log
```

**Check timer schedule:**

```bash
# Show next run time
systemctl list-timers infrastructure-monitor.timer

# Show timer configuration
systemctl cat infrastructure-monitor.timer
```

**Monitoring controls:**

```bash
# Stop monitoring temporarily
sudo systemctl stop infrastructure-monitor.timer

# Restart monitoring
sudo systemctl start infrastructure-monitor.timer

# Disable monitoring (survives reboot)
sudo systemctl disable infrastructure-monitor.timer

# Re-enable monitoring
sudo systemctl enable infrastructure-monitor.timer
```

## 4. Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Monitoring architecture, recovery strategies, ntfy.sh details |
| `examples/examples.md` | Example configurations, alert formats, log outputs |
| `scripts/test-notifications.sh` | Test script for alert delivery |

## 5. Expected Outcomes

**Success:**
- ntfy app receives push notifications
- Monitoring runs every 5 minutes
- Auto-recovery fixes common failures within 5 minutes
- Logs show monitoring activity
- Home Assistant notifications working (if configured)

**Partial Success:**
- Monitoring runs but alerts not received (check topic subscription)
- Alerts received but auto-recovery disabled (set AUTO_RECOVER=true)

**Failure Indicators:**
- No notifications received after 10 minutes
- Timer not running (check systemctl status)
- Script fails with errors (check logs)
- HA notifications not working (check token/service name)

## 6. Requirements

- Infrastructure server running Linux with systemd
- Mobile device with ntfy app installed
- Internet connectivity for ntfy.sh
- .env file with monitoring configuration
- Home Assistant (optional, for HA integration)

## 7. Red Flags to Avoid

- [ ] Do not use public/guessable ntfy topic (security risk)
- [ ] Do not share ntfy topic publicly (anyone can subscribe)
- [ ] Do not disable monitoring without alternative alerting
- [ ] Do not ignore persistent alerts (investigate root cause)
- [ ] Do not run monitoring script too frequently (causes noise)
- [ ] Do not commit .env with ntfy topic to git (privacy)
- [ ] Do not use AUTO_RECOVER=false without manual monitoring

## Notes

- Monitoring checks run every 5 minutes via systemd timer
- ntfy.sh is free and doesn't require account
- Topic ID should be random and private (security by obscurity)
- Auto-recovery attempts fixes before alerting as critical
- Alert levels: 🔴 Critical (manual intervention), ⚠️ Warning (recovery in progress)
- HA integration is optional and works alongside ntfy.sh
- Logs persist across reboots at /var/log/infrastructure-monitor.log
- Maximum detection time: 5 minutes (timer interval)
- Monitoring survives server reboots (systemd timer enabled)
- Use infrastructure-health-check skill for manual on-demand checks
