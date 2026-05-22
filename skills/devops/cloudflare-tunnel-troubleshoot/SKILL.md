---
name: cloudflare-tunnel-troubleshoot
description: |
  Diagnoses and fixes Cloudflare Tunnel connectivity issues including stuck tunnels,
  failed connections, Error 1033, and tunnel registration problems. Use when remote
  access not working, tunnel shows disconnected in dashboard, Error 1033 on tunnel
  connection, or cloudflared container restarting. Triggers on "tunnel not connecting",
  "tunnel down", "Error 1033", "remote access broken", "fix tunnel", or "cloudflared
  not working". Works with Cloudflare Tunnel (cloudflared), QUIC connection health,
  and tunnel registration verification.
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Troubleshoot Cloudflare Tunnel Skill

Systematic diagnosis and resolution of Cloudflare Tunnel connectivity issues that prevent remote access to services.

## Quick Start

Quick diagnostic for tunnel issues:

```bash
# Check cloudflared container status
docker ps | grep cloudflared

# Check recent tunnel registrations (should be within 10 minutes)
docker logs cloudflared --tail 100 | grep "Registered tunnel"

# Check for errors
docker logs cloudflared --tail 50 | grep -i error

# Restart if stuck
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml restart cloudflared
```

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Check Cloudflared Container Status
   - 3.2 Verify Tunnel Token Configuration
   - 3.3 Check Recent Tunnel Registrations
   - 3.4 Analyze Tunnel Logs for Errors
   - 3.5 Verify Tunnel in Cloudflare Dashboard
   - 3.6 Test Remote Access
   - 3.7 Apply Fix
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## 1. When to Use This Skill

**Explicit Triggers:**
- "Tunnel not connecting"
- "Tunnel down"
- "Error 1033"
- "Remote access not working"
- "Fix Cloudflare Tunnel"
- "Cloudflared not working"

**Implicit Triggers:**
- Services work locally but not remotely
- Cloudflare dashboard shows tunnel as disconnected
- 502 Bad Gateway when accessing from internet
- Cloudflared container in restart loop

**Debugging Triggers:**
- "Why isn't remote access working?"
- "Why is tunnel disconnected?"
- "What is Error 1033?"

## 2. What This Skill Does

1. **Checks Container** - Verifies cloudflared container is running
2. **Validates Token** - Confirms CLOUDFLARE_TUNNEL_TOKEN is set
3. **Checks Registrations** - Verifies tunnel has registered recently (within 10 min)
4. **Analyzes Logs** - Searches for Error 1033, QUIC issues, connection failures
5. **Checks Dashboard** - Verifies tunnel status in Cloudflare Zero Trust
6. **Tests Access** - Attempts remote connection to verify tunnel routing
7. **Provides Fix** - Gives specific recovery commands

## 3. Instructions

### 3.1 Check Cloudflared Container Status

```bash
docker ps | grep cloudflared
```

Expected: Container status "Up" with uptime > 1 minute

**Check container health:**
```bash
docker inspect cloudflared --format='{{.State.Status}}: {{.State.Health.Status}}'
```

**If not running or unhealthy:**
```bash
# Check why it stopped
docker logs cloudflared --tail 100

# Restart
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d cloudflared
```

**If in restart loop:**
- Token likely invalid or missing
- Network connectivity issue
- Proceed to step 3.2

### 3.2 Verify Tunnel Token Configuration

Check token is set in environment:

```bash
docker exec cloudflared env | grep TUNNEL_TOKEN
```

Expected: Shows long base64-encoded token

**If empty or missing:**

1. Check .env file:
```bash
grep CLOUDFLARE_TUNNEL_TOKEN /home/dawiddutoit/projects/network/.env
```

2. Verify docker-compose.yml passes it:
```bash
grep -A5 "cloudflared:" /home/dawiddutoit/projects/network/docker-compose.yml | grep TUNNEL_TOKEN
```

3. Get new token from Cloudflare dashboard:
   - Go to: https://one.dash.cloudflare.com → Access → Tunnels
   - Click on tunnel → Configure
   - Copy token from command

4. Update .env and recreate container:
```bash
# Edit .env with new token
nano /home/dawiddutoit/projects/network/.env

# Recreate container
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d --force-recreate cloudflared
```

### 3.3 Check Recent Tunnel Registrations

Healthy tunnel registers connections every few minutes:

```bash
# Check recent registrations (last 100 lines)
docker logs cloudflared --tail 100 | grep "Registered tunnel"

# Check timestamp of most recent registration
docker logs cloudflared --tail 100 | grep "Registered tunnel" | tail -1
```

Expected: Registration within last 10 minutes

**If no recent registrations (older than 10 minutes):**
- Tunnel is stuck or disconnected
- QUIC connection may have failed
- Network connectivity issue

**Check QUIC connection health:**
```bash
docker logs cloudflared --tail 100 | grep -i quic
```

### 3.4 Analyze Tunnel Logs for Errors

Search for common error patterns:

```bash
# Check for Error 1033 (tunnel disconnected)
docker logs cloudflared --tail 100 | grep "1033"

# Check for general errors
docker logs cloudflared --tail 100 | grep -i error

# Check for authentication issues
docker logs cloudflared --tail 100 | grep -i "auth\|unauthorized\|forbidden"

# Check for network issues
docker logs cloudflared --tail 100 | grep -i "connect\|timeout\|dial"
```

**Common error patterns:**

| Error | Meaning | Fix |
|-------|---------|-----|
| Error 1033 | Tunnel disconnected/stuck | Restart cloudflared container |
| `context deadline exceeded` | Network timeout | Check internet connectivity |
| `unauthorized` | Invalid tunnel token | Get new token from dashboard |
| `failed to connect to edge` | Can't reach Cloudflare | Check firewall/network |
| `no such host` | DNS resolution failure | Check DNS settings |

### 3.5 Verify Tunnel in Cloudflare Dashboard

Check tunnel status in Cloudflare Zero Trust:

1. Go to: https://one.dash.cloudflare.com
2. Navigate to: Access → Tunnels
3. Find your tunnel in list

**Expected status:** "Healthy" with green indicator

**If "Down" or "Unhealthy":**
- Tunnel not connected from server side
- Proceed to restart (step 3.7)

**Check tunnel routes:**
1. Click tunnel name → Configure
2. Verify Public Hostname routes are configured
3. Expected routes:
   - pihole.temet.ai → https://caddy:443
   - ha.temet.ai → https://caddy:443
   - jaeger.temet.ai → https://caddy:443
   - etc.

### 3.6 Test Remote Access

Test accessing a service from internet (not local WiFi):

**From mobile (using cellular data, not WiFi):**
```
https://pihole.temet.ai
```

Expected: Cloudflare Access login page appears (or service if already authenticated)

**Alternatively, use external proxy:**
```bash
# Test from external service
curl -I --connect-timeout 10 https://pihole.temet.ai
```

**If connection fails:**
- 502 Bad Gateway → Tunnel not routing correctly
- Timeout → Tunnel not connected
- Connection refused → Cloudflared not running
- SSL error → Certificate issue (different skill)

### 3.7 Apply Fix

**Fix A: Stuck Tunnel (most common)**

Restart cloudflared container:

```bash
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml restart cloudflared
```

Wait 30 seconds, then verify:
```bash
docker logs cloudflared --tail 20 | grep "Registered tunnel"
```

Expected: Fresh registrations appearing

**Fix B: Invalid Token**

Get new token and recreate container:

```bash
# 1. Get new token from dashboard:
#    https://one.dash.cloudflare.com → Access → Tunnels → Configure

# 2. Update .env
nano /home/dawiddutoit/projects/network/.env
# Add: CLOUDFLARE_TUNNEL_TOKEN="new-token-here"

# 3. Recreate container
docker compose -f /home/dawiddutoit/projects/network/docker-compose.yml up -d --force-recreate cloudflared

# 4. Verify
docker logs cloudflared --tail 20
```

**Fix C: Network Connectivity Issue**

Check internet connectivity:

```bash
# Test connectivity to Cloudflare
docker exec cloudflared ping -c 3 1.1.1.1

# Test DNS resolution
docker exec cloudflared nslookup cloudflare.com

# Check container network
docker network inspect network_default
```

If network issues found, may need to recreate Docker network (see Docker network troubleshooting).

**Fix D: Complete Tunnel Reset**

If all else fails, full reset:

```bash
# Stop all services
cd /home/dawiddutoit/projects/network && \
docker compose down

# Recreate network
docker network rm network_default
docker network create network_default

# Start services
docker compose up -d

# Monitor tunnel connection
docker logs cloudflared -f
```

Watch for "Registered tunnel" messages appearing.

## 4. Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Cloudflare Tunnel architecture, Error 1033 details, QUIC protocol |
| `examples/examples.md` | Example log outputs, common scenarios |

## 5. Expected Outcomes

**Success:**
- Cloudflared container running and healthy
- Recent tunnel registrations (within 10 minutes)
- Tunnel shows "Healthy" in Cloudflare dashboard
- Remote access works with OAuth prompt
- No Error 1033 in logs

**Partial Success:**
- Tunnel connecting but routes not configured (add routes in dashboard)
- Tunnel working but intermittent (network instability)

**Failure Indicators:**
- Cloudflared container not running or restarting
- No tunnel registrations in logs
- Error 1033 persists after restart
- Remote access returns 502 Bad Gateway

## 6. Requirements

- Docker running with cloudflared container
- Valid Cloudflare Tunnel token
- Internet connectivity from server
- Cloudflare Zero Trust account
- Tunnel configured in Cloudflare dashboard

## 7. Red Flags to Avoid

- [ ] Do not delete tunnel in Cloudflare dashboard (creates orphaned token)
- [ ] Do not expose ports 80/443 if tunnel not working (security risk)
- [ ] Do not skip checking logs before restart (miss root cause)
- [ ] Do not restart tunnel repeatedly (causes rate limiting)
- [ ] Do not test remote access from local WiFi (use cellular/external)
- [ ] Do not confuse tunnel token with API token (different credentials)
- [ ] Do not modify tunnel routes without updating Caddyfile

## Notes

- Tunnel registrations should occur every few minutes (QUIC keep-alive)
- Error 1033 typically indicates stuck/stale tunnel process
- Tunnel uses outbound QUIC connection (no inbound ports needed)
- Maximum tunnel downtime before auto-disconnect: ~10 minutes
- Automated monitoring (infrastructure-monitor.sh) detects stuck tunnels
- Tunnel routes are configured in Cloudflare dashboard, not locally
- Use `infrastructure-health-check` skill for comprehensive diagnostics
