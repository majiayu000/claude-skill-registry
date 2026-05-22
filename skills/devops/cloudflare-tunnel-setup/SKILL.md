---
name: cloudflare-tunnel-setup
description: |
  Sets up a new Cloudflare Tunnel from scratch for secure remote access to home network
  services. Use when creating a new tunnel, replacing an expired tunnel token, or setting
  up remote access for a fresh installation. Triggers on "setup cloudflare tunnel", "create
  tunnel", "new tunnel token", "configure remote access", "cloudflare tunnel from scratch",
  or "tunnel not configured". Works with .env, docker-compose.yml, and Cloudflare Zero Trust.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Cloudflare Tunnel Setup Skill

Interactive guide for setting up a new Cloudflare Tunnel from scratch.

## Quick Start

Run this skill when you need to:
1. Create a new Cloudflare Tunnel
2. Replace an expired or invalid tunnel token
3. Set up remote access for a fresh installation

**Minimum requirements:** Cloudflare account, domain on Cloudflare, Docker installed.

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Check Prerequisites
   - 3.2 Create Tunnel in Dashboard
   - 3.3 Configure Token in .env
   - 3.4 Restart Cloudflared Container
   - 3.5 Configure Public Hostnames
   - 3.6 Verify Connectivity
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Setup cloudflare tunnel"
- "Create a new tunnel"
- "Configure remote access"
- "Replace tunnel token"
- "Tunnel from scratch"

**Implicit Triggers:**
- Fresh installation of network infrastructure
- Tunnel token expired or invalid
- CLOUDFLARE_TUNNEL_TOKEN missing from .env
- Moving infrastructure to new hardware

**Debugging Triggers:**
- "Tunnel token not found"
- "cloudflared container won't start"
- "No CLOUDFLARE_TUNNEL_TOKEN in .env"

## What This Skill Does

1. **Checks Prerequisites** - Verifies .env exists and cloudflared is in docker-compose
2. **Guides Tunnel Creation** - Step-by-step instructions for Cloudflare dashboard
3. **Configures Token** - Adds tunnel token to .env file
4. **Restarts Container** - Restarts cloudflared to apply new token
5. **Guides Hostname Setup** - Instructions for configuring public hostnames
6. **Verifies Connectivity** - Confirms tunnel is connected and working

## Instructions

### 3.1 Check Prerequisites

**Step 1: Verify .env file exists**

```bash
ls -la /home/dawiddutoit/projects/network/.env
```

If missing, create from example:
```bash
cp /home/dawiddutoit/projects/network/.env.example /home/dawiddutoit/projects/network/.env
```

**Step 2: Check if CLOUDFLARE_TUNNEL_TOKEN exists**

```bash
grep -E "^CLOUDFLARE_TUNNEL_TOKEN" /home/dawiddutoit/projects/network/.env
```

**Possible outcomes:**
- Line exists with value: Token already configured (check if valid)
- Line exists but empty/placeholder: Needs real token
- Line not found: Token needs to be added

**Step 3: Verify docker-compose has cloudflared service**

```bash
grep -A 10 "cloudflared:" /home/dawiddutoit/projects/network/docker-compose.yml
```

If cloudflared service is missing, it needs to be added. See `references/reference.md` for service definition.

### 3.2 Create Tunnel in Dashboard

Provide these instructions to the user:

1. Go to: https://one.dash.cloudflare.com -> Access -> Tunnels
2. Click "Create a tunnel" -> Select "Cloudflared" connector
3. Name tunnel (e.g., "pi-home") -> Choose "Docker" as connector type
4. Copy the tunnel token (long base64 string after `--token`)
5. Save token securely

**Token format:** Base64-encoded JSON containing Account ID, Tunnel ID, and Secret.

### 3.3 Configure Token in .env

**Step 1: Check current token status**

```bash
grep "CLOUDFLARE_TUNNEL_TOKEN" /home/dawiddutoit/projects/network/.env
```

**Step 2: Add or update token**

If line exists, update it. If not, add it.

```bash
# If line exists, use sed to replace
# If not, append to file

# The token should look like:
# CLOUDFLARE_TUNNEL_TOKEN=eyJhIjoiYWJjZDEyMzQ...
```

Use the Edit tool to update `.env`:
- Look for existing `CLOUDFLARE_TUNNEL_TOKEN=` line
- Replace with new token value
- Or add new line if not present

**Validate token format:**

```bash
# Token should be base64 decodable
TUNNEL_TOKEN=$(grep "CLOUDFLARE_TUNNEL_TOKEN=" /home/dawiddutoit/projects/network/.env | cut -d'=' -f2)
echo "$TUNNEL_TOKEN" | base64 -d 2>/dev/null | python3 -c "import sys, json; d=json.load(sys.stdin); print('Valid token for account:', d.get('a', 'unknown'))"
```

### 3.4 Restart Cloudflared Container

**Step 1: Restart the container**

```bash
cd /home/dawiddutoit/projects/network && docker compose restart cloudflared
```

Or if container doesn't exist yet:
```bash
cd /home/dawiddutoit/projects/network && docker compose up -d cloudflared
```

**Step 2: Check container is running**

```bash
docker ps | grep cloudflared
```

**Expected output:**
```
CONTAINER ID   IMAGE                         STATUS         NAMES
abc123...      cloudflare/cloudflared:latest Up X seconds   cloudflared
```

**Step 3: Check logs for successful connection**

```bash
docker logs cloudflared --tail 30
```

**Look for these success indicators:**
```
INF Registered tunnel connection connIndex=0 location=...
INF Registered tunnel connection connIndex=1 location=...
INF Registered tunnel connection connIndex=2 location=...
INF Registered tunnel connection connIndex=3 location=...
```

4 registered connections = healthy tunnel (2 connections per Cloudflare edge location)

**If errors appear:**
- `token is invalid`: Token was copied incorrectly or expired
- `already registered`: Another instance using same token (stop other instances)
- `network error`: Check internet connectivity

### 3.5 Configure Public Hostnames

After tunnel is connected, configure services in Cloudflare dashboard:

1. Go to: https://one.dash.cloudflare.com -> Access -> Tunnels
2. Click tunnel name -> Configure -> Public Hostname -> Add
3. For each service, enter subdomain, domain (temet.ai), Type (HTTP), and URL

**Example hostnames:**
| Service | Subdomain | URL |
|---------|-----------|-----|
| Pi-hole | pihole | pihole:80 |
| Webhook | webhook | webhook:9000 |
| Jaeger | jaeger | 192.168.68.135:16686 |

**URL patterns:**
- Docker container: `container:port` (e.g., pihole:80)
- Host service: `host-ip:port` (e.g., 192.168.68.135:16686)
- LAN device: `device-ip:port` (e.g., 192.168.68.105:80)

**Important:** Use HTTP (not HTTPS) for backends. Do NOT use `host.docker.internal` on Linux.

### 3.6 Verify Connectivity

**Step 1: Verify tunnel is registered**

```bash
docker logs cloudflared 2>&1 | grep -E "Registered tunnel|connIndex"
```

**Expected:** 4 "Registered tunnel connection" messages

**Step 2: Check tunnel status in dashboard**

```
Go to: https://one.dash.cloudflare.com
Navigate to: Access -> Tunnels
Status should show: "HEALTHY" with green indicator
```

**Step 3: Test external access (from mobile data or external network)**

```bash
# From a device NOT on home network:
curl -I https://pihole.temet.ai

# Expected: HTTP 302 (redirect to Cloudflare Access) or HTTP 200 (if no auth)
```

**Step 4: Run diagnostic script (optional)**

```bash
./scripts/cf-tunnel-config.sh show
```

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Docker-compose service definition, token format details |
| `examples/examples.md` | Example configurations for common setups |

## Expected Outcomes

**Success:**
- CLOUDFLARE_TUNNEL_TOKEN in .env
- cloudflared container running
- 4 tunnel connections registered in logs
- Tunnel shows "HEALTHY" in dashboard
- Services accessible via *.temet.ai from external network

**Partial Success:**
- Token configured but hostnames not set up (user reminder provided)
- Tunnel connected but services return 502 (backend configuration issue)

**Failure Indicators:**
- "token is invalid" in logs -> Re-copy token from dashboard
- Container restart loop -> Check token format
- 0 registered connections -> Network/firewall issue

## Requirements

**Environment:**
- Cloudflare account with domain
- Docker and Docker Compose installed
- Internet connectivity
- `.env` file in project root

**Accounts/Access:**
- Cloudflare dashboard access
- Zero Trust enabled (free tier works)

**Tools needed:**
- Read, Write, Edit (for .env configuration)
- Bash (for docker commands and verification)
- Grep (for checking existing configuration)

## Red Flags to Avoid

- [ ] Do not commit tunnel token to git (keep in .env only)
- [ ] Do not use `host.docker.internal` on Linux hosts
- [ ] Do not use HTTPS URLs for internal service backends
- [ ] Do not share tunnel tokens between environments
- [ ] Do not skip the verification step (3.6)
- [ ] Do not forget to configure public hostnames after tunnel connects
- [ ] Do not leave placeholder token values in .env

## Notes

- Tunnel tokens do not expire but can be revoked in dashboard
- Each tunnel can have multiple connectors (for redundancy)
- Tunnel configuration changes apply automatically (no restart needed)
- Use `./scripts/cf-tunnel-config.sh configure` to update ingress via API
- For authentication, use the `configure-google-oauth` skill after tunnel setup
- The existing `troubleshoot-tunnel-connectivity` skill handles issues with running tunnels
