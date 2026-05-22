---
name: service-monitoring-setup
description: Autonomous setup and management of external service monitoring using UptimeRobot (HTTP endpoint monitoring) and Healthchecks.io (heartbeat/Dead Man's Switch monitoring). Use when setting up monitoring for Cloud Run Jobs, VM services, or investigating monitoring configuration issues. Includes Pushover integration, validated API patterns, and dual-service architecture.
---

# Service Monitoring Setup

## Overview

This skill provides validated patterns for setting up external service monitoring using two complementary services:

- **Healthchecks.io** - Dead Man's Switch monitoring for ephemeral workloads (Cloud Run Jobs)
- **UptimeRobot** - HTTP endpoint monitoring for persistent services (VMs, Cloud Run Services)

**Key Principle**: Never monitor from the same infrastructure being monitored. Both services run externally on separate infrastructure to avoid single points of failure.

**Cost**: $0/month using free tiers of both services for complete monitoring coverage.

## When to Use This Skill

Use this skill when:

- Setting up monitoring for Cloud Run Jobs (heartbeat monitoring)
- Configuring HTTP endpoint monitoring for VM services
- Investigating why monitoring alerts aren't working
- Troubleshooting Pushover integration with monitoring services
- User mentions "monitoring", "uptime", "healthcheck", "dead man's switch", or "alerts"
- Validating monitoring service API integration before production use

## Monitoring Architecture Decision Tree

```
Is the workload ephemeral (runs and exits)?
├─ YES → Use Healthchecks.io (Dead Man's Switch)
│   ├─ Job pings on success
│   ├─ No ping within timeout → Alert
│   └─ Free tier: 20 checks, user-defined timeouts
│
└─ NO → Is it a persistent HTTP endpoint?
    └─ YES → Use UptimeRobot (HTTP polling)
        ├─ Service pings endpoint every N minutes
        ├─ No response → Alert
        └─ Free tier: 50 monitors, 5-minute intervals
```

**Recommended Architecture**: Use BOTH services for dual-pipeline monitoring

- Healthchecks.io: Cloud Run Jobs (data collection jobs)
- UptimeRobot: VM HTTP endpoints (persistent services)

## Quick Start

### Healthchecks.io (Dead Man's Switch)

```python
# /// script
# dependencies = ["requests"]
# ///

import os
from scripts.healthchecks_client import HealthchecksClient

# Get API key from Doppler
api_key = os.popen(
    "doppler secrets get HEALTHCHECKS_API_KEY --project claude-config --config dev --plain"
).read().strip()

client = HealthchecksClient(api_key)

# Create check for Cloud Run Job
result = client.create_check(
    name="Ethereum Collector Job",
    timeout=7200,  # 2 hours
    grace=600,     # 10 minutes grace period
    tags="production ethereum",
    channels="*"   # All notification channels
)

ping_url = result["ping_url"]
print(f"Add to Cloud Run Job environment: HEALTHCHECK_PING_URL={ping_url}")

# In your Cloud Run Job script:
# import requests
# requests.get(os.getenv("HEALTHCHECK_PING_URL"))  # On success
# requests.get(f"{os.getenv('HEALTHCHECK_PING_URL')}/fail")  # On failure
```

### UptimeRobot (HTTP Monitoring)

```python
# /// script
# dependencies = ["requests"]
# ///

import os
from scripts.uptimerobot_client import UptimeRobotClient

# Get API key from Doppler
api_key = os.popen(
    "doppler secrets get UPTIMEROBOT_API_KEY --project claude-config --config dev --plain"
).read().strip()

client = UptimeRobotClient(api_key)

# Create HTTP monitor for VM service
result = client.create_monitor(
    friendly_name="Production API Endpoint",
    url="https://your-vm-ip:8000/health",
    type=1,  # HTTP(S)
    interval=300,  # 5 minutes (free tier)
    alert_contacts=client.get_pushover_contact_id()  # Type 9 Pushover contact
)

print(f"Monitor created: {result['monitor']['id']}")
```

## UptimeRobot Operations

### Authentication

UptimeRobot API v2 uses POST data authentication:

```python
def _request(self, endpoint: str, data: Dict) -> Dict:
    data["api_key"] = self.api_key
    data["format"] = "json"
    response = requests.post(f"{self.base_url}/{endpoint}", data=data)
    response.raise_for_status()
    result = response.json()
    if result.get("stat") != "ok":
        raise Exception(f"UptimeRobot API error: {result}")
    return result
```

### Free Tier Capabilities

- **Monitors**: 50 HTTP/HTTPS monitors
- **Check Interval**: 5 minutes (minimum)
- **Alert Contacts**: Unlimited (email, Pushover, Slack, webhook)
- **Limitations**:
  - Heartbeat monitoring requires Pro ($7/mo)
  - Rate limiting: 10 req/min (429 error with Retry-After: 47s header)
  - Use exponential backoff for bulk operations

### Common Operations

**List Monitors**:

```python
monitors = client.get_monitors()
for monitor in monitors:
    print(f"{monitor['friendly_name']}: {monitor['url']} - {monitor['status']}")
```

**Create Monitor**:

```python
result = client.create_monitor(
    friendly_name="API Health Check",
    url="https://api.example.com/health",
    type=1,  # HTTP(S)
    interval=300,  # 5 minutes
    alert_contacts=pushover_id
)
```

**Delete Monitor**:

```python
client.delete_monitor(monitor_id="801762241")
```

**Get Pushover Contact ID**:

```python
pushover_id = client.get_pushover_contact_id()
if not pushover_id:
    print("⚠️ Pushover not configured - see Pushover Integration Setup")
```

### Monitor Types

- `1` = HTTP(S) - Checks endpoint response
- `2` = Keyword - Checks for specific text in response
- `3` = Ping - ICMP ping
- `4` = Port - TCP port check

## Healthchecks.io Operations

### Authentication

Healthchecks.io API v3 uses X-Api-Key header authentication:

```python
headers = {
    "X-Api-Key": api_key,
    "Content-Type": "application/json"
}
response = requests.get(f"{base_url}/checks/", headers=headers)
```

### Free Tier Capabilities

- **Checks**: 20 checks
- **Timeout**: User-defined (any duration)
- **Grace Period**: User-defined buffer before alert
- **Integrations**: Email, Pushover, Slack, Discord, webhooks (all free)
- **Ping Mechanism**: Simple HTTP GET to unique ping URL

### Common Operations

**List Checks**:

```python
checks = client.get_checks()
for check in checks:
    print(f"{check['name']}: {check['status']} - {check['ping_url']}")
```

**Create Check**:

```python
result = client.create_check(
    name="Daily Backup Job",
    timeout=86400,  # 24 hours
    grace=3600,     # 1 hour grace
    tags="backup production",
    channels=pushover_id  # Or "*" for all channels
)
ping_url = result["ping_url"]
```

**Ping Check (Success)**:

```python
# From your job/script
import requests
requests.get(ping_url)
```

**Ping Check (Failure)**:

```python
requests.get(f"{ping_url}/fail")
```

**Delete Check**:

```python
client.delete_check(check_uuid="6a991157-552d-4c2c-b972-d43de0a96bff")
```

### Dead Man's Switch Pattern

Perfect for ephemeral workloads (Cloud Run Jobs, cron jobs):

```
Job Lifecycle:
1. Job starts
2. Job executes work
3. Job pings Healthchecks.io on success
4. If no ping within timeout → Alert

Advantages:
- No always-on endpoint needed
- Works with ephemeral infrastructure
- Simple integration (one HTTP GET)
- Catches job crashes, hangs, or scheduling failures
```

## Pushover Integration Setup

**Important**: Pushover integration must be configured via web UI first. API can only list and assign existing integrations, not create them.

### Prerequisites

1. Create Pushover account at https://pushover.net (30-day trial, then $5 one-time)
2. Install Pushover app on mobile device
3. Note your User Key from Pushover dashboard

### UptimeRobot Pushover Setup

1. Go to https://uptimerobot.com/dashboard
2. Click "My Settings" → "Alert Contacts"
3. Click "Add Alert Contact"
4. Select "Pushover" (may appear as type 9 in API)
5. Enter your Pushover User Key
6. Complete verification
7. Verify with: `client.get_pushover_contact_id()` (should return numeric ID)

**API Note**: Pushover contacts appear as type=9 in UptimeRobot API responses.

### Healthchecks.io Pushover Setup

1. Go to https://healthchecks.io/projects
2. Navigate to "Integrations" → "Add Integration"
3. Select "Pushover"
4. Enter your Pushover User Key and API Token/Key
5. Save integration
6. Verify with: `client.get_pushover_channel_id()` (should return UUID)

**API Note**: Pushover channels use kind code "po" (abbreviated), not "pushover".

**Common Issue**: If `get_pushover_contact_id()` or `get_pushover_channel_id()` returns `None`, Pushover is not configured. Complete setup steps above via web UI.

## Troubleshooting

### UptimeRobot Issues

**429 Too Many Requests**:

- Free tier has rate limits (10 req/min empirically validated)
- Response includes `Retry-After` header (observed: 47 seconds)
- Response includes `X-RateLimit-Remaining` header (counts down from 9 to 0)
- Add exponential backoff between operations
- Use bulk operations where available

**Rate Limit Example**:

```python
import time
from requests.exceptions import HTTPError

try:
    result = client.get_monitors()
except HTTPError as e:
    if e.response.status_code == 429:
        retry_after = int(e.response.headers.get('Retry-After', 60))
        print(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        result = client.get_monitors()  # Retry
```

**Heartbeat Monitoring Not Available**:

- Free tier only supports HTTP polling
- Use Healthchecks.io for heartbeat monitoring (free)

**Pushover Alerts Not Working**:

- Verify: `client.get_pushover_contact_id()` returns a value
- If `None`, complete Pushover setup steps via web UI
- Check alert contact is enabled (status=2)
- Confirm Pushover app is installed on device

### Healthchecks.io Issues

**400 Bad Request on Check Creation**:

- **Root Cause**: All fields are optional per official docs. Use minimal payload.
- **Solution**: Only provide `name`, `timeout`, and `grace`:

```python
result = client.create_check(
    name="My Check",
    timeout=3600,   # seconds (required)
    grace=600       # seconds (recommended)
)
# All other fields are optional
```

- Avoid complex payloads with undocumented fields
- Official docs: https://healthchecks.io/docs/api/

**Ping Not Recording**:

- Verify ping URL is correct (from `create_check` response)
- Check HTTP GET succeeds (200 OK)
- View check details in dashboard to see ping history

**API Field Mismatches**:

- API v3 response format may differ from documentation
- Use empirical validation (create test check, inspect response)
- Key fields: `ping_url`, `uuid`, `update_url`

## Production Deployment Pattern

```python
# /// script
# dependencies = ["requests"]
# ///

import os
import requests
from scripts.healthchecks_client import HealthchecksClient
from scripts.uptimerobot_client import UptimeRobotClient

# Get API keys from Doppler
healthchecks_key = os.popen(
    "doppler secrets get HEALTHCHECKS_API_KEY --project claude-config --config dev --plain"
).read().strip()

uptimerobot_key = os.popen(
    "doppler secrets get UPTIMEROBOT_API_KEY --project claude-config --config dev --plain"
).read().strip()

# Initialize clients
hc_client = HealthchecksClient(healthchecks_key)
ur_client = UptimeRobotClient(uptimerobot_key)

# Get Pushover integration IDs
hc_pushover = hc_client.get_pushover_channel_id()
ur_pushover = ur_client.get_pushover_contact_id()

if not hc_pushover or not ur_pushover:
    print("⚠️ WARNING: Pushover not configured for one or both services")
    print("Alerts will only go to email until Pushover is set up via web UI")

# Setup Cloud Run Job monitoring (Dead Man's Switch)
job_check = hc_client.create_check(
    name="Ethereum Data Collection Job",
    timeout=7200,  # 2 hours
    grace=600,     # 10 minutes
    tags="production ethereum cloud-run",
    channels=hc_pushover if hc_pushover else "*"
)

print(f"Cloud Run Job Ping URL: {job_check['ping_url']}")
print("Add to Cloud Run Job environment variables:")
print(f"  HEALTHCHECK_PING_URL={job_check['ping_url']}")

# Setup VM HTTP endpoint monitoring
vm_monitor = ur_client.create_monitor(
    friendly_name="VM API Endpoint",
    url="https://your-vm-ip:8000/health",
    type=1,
    interval=300,
    alert_contacts=ur_pushover if ur_pushover else None
)

print(f"VM Monitor ID: {vm_monitor['monitor']['id']}")
print("Monitoring active - will check every 5 minutes")
```

## Resources

### Bundled Scripts

- **scripts/healthchecks_client.py** - Production-ready Healthchecks.io API client
- **scripts/uptimerobot_client.py** - Production-ready UptimeRobot API client

Both scripts include:

- Type hints for all methods
- Error handling with descriptive exceptions
- Retry logic recommendations
- Idiomatic API patterns validated through empirical testing

### Validation Evidence

All patterns in this skill have been empirically validated:

- `/tmp/probe/uptimerobot/PROBE_REPORT.md` - UptimeRobot API validation results
- `/tmp/probe/healthchecks-io/PROBE_REPORT.md` - Healthchecks.io API validation results
- 10 total probe scripts (5 per service)
- All core operations tested against live APIs

### API Documentation

- **UptimeRobot**: https://uptimerobot.com/api/
- **Healthchecks.io**: https://healthchecks.io/docs/api/

### Service Comparison

| Feature                  | Healthchecks.io   | UptimeRobot           |
| ------------------------ | ----------------- | --------------------- |
| **Free tier checks**     | 20                | 50 HTTP monitors      |
| **Heartbeat monitoring** | ✅ Free           | ❌ Pro only ($7/mo)   |
| **HTTP monitoring**      | ❌                | ✅ Free               |
| **Pushover alerts**      | ✅ Free           | ✅ Free               |
| **API**                  | v3, modern        | v2, established       |
| **Best for**             | Dead Man's Switch | HTTP endpoint polling |

**Recommendation**: Use BOTH for dual-pipeline architecture ($0/month total cost).
