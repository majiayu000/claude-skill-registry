---
name: caddy-subdomain-add
description: |
  Interactively adds a new subdomain to the network infrastructure by gathering service
  details, configuring domains.toml, and applying changes. Use when you need to add a
  new service, create a subdomain, expose a new application, or set up reverse proxy
  for a service. Triggers on "add subdomain", "new subdomain", "add service to network",
  "expose service", "create domain for", "set up reverse proxy", or "add [name] to
  infrastructure". Works with domains.toml, manage-domains.sh, and Cloudflare Tunnel.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Add Subdomain Skill

Interactive guide for adding new subdomains to the network infrastructure.

## Quick Start

**Minimal Request:** "Add grafana running on port 3001"

**Full Request Example:**
```
Add a new subdomain:
- Name: Grafana Dashboard
- Subdomain: grafana
- Backend: 192.168.68.135:3001
- HTTPS: yes
- Auth: yes
```

**Result:** Service accessible at https://grafana.temet.ai with Google OAuth protection.

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Gather Service Information
   - 3.2 Validate Input
   - 3.3 Determine Configuration
   - 3.4 Add to domains.toml
   - 3.5 Apply Changes
   - 3.6 Manual Tunnel Step
   - 3.7 Verify Setup
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Integration Points](#6-integration-points)
7. [Expected Benefits](#7-expected-benefits)
8. [Requirements](#8-requirements)
9. [Red Flags to Avoid](#9-red-flags-to-avoid)

## When to Use This Skill

**Explicit Triggers:**
- "Add a subdomain for [service]"
- "Create subdomain [name]"
- "Add [service] to the network"
- "Set up reverse proxy for [service]"
- "Expose [service] externally"

**Implicit Triggers:**
- Setting up a new Docker container that needs external access
- Installing new software that requires HTTPS
- Configuring a new IoT device for remote access

**Debugging Triggers:**
- "Why can't I access [service].temet.ai?"
- "How do I add HTTPS to my service?"

## What This Skill Does

1. **Gathers Information** - Asks interactive questions about the service
2. **Validates Input** - Checks subdomain format, IP addresses, ports
3. **Suggests Defaults** - Recommends settings based on service type
4. **Configures domains.toml** - Adds service entry with correct options
5. **Applies Changes** - Runs manage-domains.sh to generate configs
6. **Provides Tunnel Instructions** - Guides user through manual Cloudflare step
7. **Verifies Setup** - Tests DNS, HTTPS, and authentication

## Instructions

### 3.1 Gather Service Information

Ask the user for the following details (provide examples):

**Required:**
| Field | Question | Example |
|-------|----------|---------|
| name | What is the display name for this service? | "Grafana Dashboard" |
| subdomain | What subdomain do you want? (without .temet.ai) | "grafana" |
| backend | Where is the service running? (IP:port or container:port) | "192.168.68.135:3001" or "grafana:3000" |

**Service Type (for intelligent defaults):**
| Type | Description |
|------|-------------|
| web | Standard web application (default settings) |
| docker | Docker container on the same network |
| iot | IoT device (needs header stripping) |
| api | API service (may need custom headers) |
| external | Service on different machine on LAN |

### 3.2 Validate Input

Use the validation script to check subdomain and backend:
```bash
python3 .claude/skills/add-subdomain/scripts/validate-subdomain.py grafana 192.168.68.135:3001
```

**Rules:**
- Subdomain: lowercase alphanumeric + hyphens, max 63 chars, no leading/trailing hyphens
- Backend: IP:port (e.g., `192.168.68.135:3001`) or container:port (e.g., `grafana:3000`)
- Check for duplicates before adding

### 3.3 Determine Configuration

Use service type to select defaults (see `references/reference.md` for full matrix):

| Type | enable_https | enable_http | require_auth | Special |
|------|--------------|-------------|--------------|---------|
| web | true | false | true | proxy_headers |
| docker | true | false | true | container:port backend |
| iot | false | true | true | strip_cf_headers |
| external | true | false | true | LAN IP backend |
| self-signed | true | false | true | tls_insecure |
| public | false | true | false | no auth |

### 3.4 Add to domains.toml

**Location:** `/home/dawiddutoit/projects/network/domains.toml`

**Steps:**
1. Read current domains.toml
2. Find appropriate section (Core Infrastructure, IoT Devices, or Utility Services)
3. Append new service entry before the Advanced Configuration section
4. Use Edit tool to add the entry

**Template:**
```toml
[[services]]
name = "{name}"
subdomain = "{subdomain}"
backend = "{backend}"
enable_https = {enable_https}
enable_http = {enable_http}
dns_ip = "{dns_ip}"
require_auth = {require_auth}
{optional_fields}
```

### 3.5 Apply Changes

Run the management script:

```bash
cd /home/dawiddutoit/projects/network && ./scripts/manage-domains.sh apply
```

**Expected output:**
```
=== Applying Domain Configuration ===

Validating configuration...
[checkmark] Configuration is valid

Generating Caddyfile...
[checkmark] Caddyfile generated successfully

Updating Pi-hole DNS entries...
[checkmark] Pi-hole DNS entries updated

Syncing Cloudflare Access applications...
[checkmark] Cloudflare Access synced successfully

Reloading Caddy configuration...
[checkmark] Caddy reloaded successfully

Restarting Pi-hole to apply DNS changes...
[checkmark] Pi-hole restarted successfully
```

### 3.6 Manual Tunnel Step

Provide clear instructions for the Cloudflare Tunnel configuration:

```
MANUAL STEP REQUIRED: Add Cloudflare Tunnel Route

1. Go to: https://one.dash.cloudflare.com
2. Navigate to: Access -> Tunnels
3. Click on tunnel: "pi-home" (or your tunnel name)
4. Click "Configure" -> "Public Hostname" -> "Add a public hostname"
5. Enter:
   - Subdomain: {subdomain}
   - Domain: temet.ai
   - Type: {HTTP or HTTPS}
   - URL: {backend_for_tunnel}

   For HTTPS services: https://caddy:443
   For HTTP-only services: http://caddy:80 or direct to service

6. Click "Save hostname"
```

**Tunnel Backend Selection:**
| Service Type | Tunnel URL |
|-------------|------------|
| HTTPS enabled | `https://caddy:443` |
| HTTP only (IoT) | Direct to service: `http://192.168.68.XXX:80` |
| Docker container | `https://caddy:443` or `http://caddy:80` |

### 3.7 Verify Setup

After tunnel configuration, run verification:

**1. DNS Resolution (local):**
```bash
dig @192.168.68.135 {subdomain}.temet.ai +short
```
Expected: Returns the dns_ip configured

**2. HTTPS Certificate:**
```bash
echo | openssl s_client -servername {subdomain}.temet.ai \
  -connect {subdomain}.temet.ai:443 2>/dev/null | \
  openssl x509 -noout -dates -issuer
```
Expected: Valid certificate from Let's Encrypt

**3. HTTP Response:**
```bash
curl -I https://{subdomain}.temet.ai
```
Expected: HTTP/2 200 or 302 (redirect to login)

**4. Service List:**
```bash
./scripts/manage-domains.sh list
```
Expected: New service appears in list

## Supporting Files

| File | Purpose |
|------|---------|
| `references/reference.md` | Complete configuration options reference |
| `examples/examples.md` | Common service configuration examples |
| `scripts/validate-subdomain.py` | Pre-validation of subdomain and backend |

**Validation Script Usage:**
```bash
python3 .claude/skills/add-subdomain/scripts/validate-subdomain.py grafana 192.168.68.135:3001
```

## Expected Outcomes

**Success:**
- Service entry added to domains.toml
- Caddyfile regenerated with new service block
- Pi-hole DNS entry created
- Cloudflare Access application created (if require_auth=true)
- Caddy reloaded with new certificate
- Service accessible at https://{subdomain}.temet.ai

**Partial Success:**
- Configuration applied but tunnel not configured (user reminder provided)
- Certificate pending (may take 1-2 minutes)

**Failure Indicators:**
- domains.toml syntax error -> validate and fix
- Caddy reload failed -> check Caddyfile syntax
- DNS not resolving -> check Pi-hole logs
- Certificate error -> check Cloudflare API token

## Integration Points

This skill integrates with:

| Component | Purpose |
|-----------|---------|
| `domains.toml` | Central configuration source |
| `manage-domains.sh` | Applies configuration changes |
| `generate-caddyfile.py` | Generates Caddyfile from domains.toml |
| `generate-pihole-dns.py` | Updates Pi-hole DNS entries |
| `sync-cloudflare-access.py` | Creates/updates Access applications |
| Cloudflare Tunnel | Manual public hostname configuration |

**Related Skills:**
- `setup-new-domain-services` - For adding new top-level domains
- `troubleshoot-ssl-certificates` - For certificate issues
- `diagnose-cloudflare-access` - For authentication problems

## Expected Benefits

| Metric | Before | After |
|--------|--------|-------|
| Time to add service | 15-30 min (manual) | 2-5 min (guided) |
| Configuration errors | Common (manual editing) | Rare (validated) |
| Documentation needed | Multiple files | Single skill reference |
| Consistency | Variable | Standardized |

## Requirements

**Environment:**
- Docker running with caddy, pihole containers
- Cloudflare tunnel connected
- Valid `.env` with API tokens

**Tools needed:**
- Read, Write, Edit (for domains.toml)
- Bash (for apply script and verification)
- Grep (for duplicate checking)

## Red Flags to Avoid

- [ ] Do not add duplicate subdomains (check first)
- [ ] Do not use uppercase in subdomain names
- [ ] Do not forget the manual tunnel step
- [ ] Do not skip verification after apply
- [ ] Do not use `host.docker.internal` on Linux (use actual IP)
- [ ] Do not enable both HTTPS and HTTP unless specifically needed
- [ ] Do not set require_auth=false unless service must be public
- [ ] Do not skip tls_insecure for services with self-signed certs

## Notes

- The Pi IP is typically `192.168.68.135` for services running on the Pi
- IoT devices need `strip_cf_headers = true` to work properly
- Services with self-signed certs need `tls_insecure = true`
- Root redirects (like `/admin/`) use `root_redirect` option
- The tunnel step is manual because Cloudflare API for tunnels is complex
- Always run `./scripts/manage-domains.sh list` to see current services
